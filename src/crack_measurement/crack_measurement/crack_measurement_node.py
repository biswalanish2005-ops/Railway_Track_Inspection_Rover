"""
Crack Measurement Node for Railway Inspection Rover.

Executes physical crack length, maximum/average width, and apparent depth estimation
using camera calibration and planar homography. Saves inspection JSON metadata and images.
"""

from datetime import datetime
import json
import os
import cv2
from cv_bridge import CvBridge
import numpy as np
from rclpy.node import Node
import rclpy
from rover_msgs.msg import CrackDetection, InspectionResult
from sensor_msgs.msg import Image


class CrackMeasurementNode(Node):
    """ROS 2 Node for calibrated crack measurement and record storage."""

    def __init__(self) -> None:
        super().__init__("crack_measurement_node")

        # Declare Parameters
        self.declare_parameter("rail_physical_width_mm", 70.0)
        self.declare_parameter("ipm_output_width", 400)
        self.declare_parameter("ipm_output_height", 600)
        self.declare_parameter("storage_directory", "inspection")

        # Retrieve Parameters
        self._rail_mm = float(self.get_parameter("rail_physical_width_mm").value)
        self._ipm_w = int(self.get_parameter("ipm_output_width").value)
        self._ipm_h = int(self.get_parameter("ipm_output_height").value)
        self._storage_dir = str(self.get_parameter("storage_directory").value)

        self._bridge = CvBridge()

        # Cache Latest IPM Image
        self._latest_ipm = None
        self._latest_detection = None
        self._inspection_count = 0

        # ROS 2 Subscribers
        self._ipm_sub = self.create_subscription(
            Image, "/camera/rail_ipm", self._ipm_callback, 10
        )
        self._det_sub = self.create_subscription(
            CrackDetection, "/crack_detection", self._detection_callback, 10
        )

        # ROS 2 Publisher
        self._result_pub = self.create_publisher(
            InspectionResult, "/inspection_result", 10
        )

        self.get_logger().info(
            f"Crack Measurement Node initialized (Rail Reference: {self._rail_mm}mm, Storage: '{self._storage_dir}/')"
        )

    def _ipm_callback(self, msg: Image) -> None:
        """Cache latest perspective-corrected IPM image."""
        try:
            self._latest_ipm = self._bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        except Exception as e:
            self.get_logger().error(f"CvBridge error: {e}")

    def _detection_callback(self, msg: CrackDetection) -> None:
        """Process crack detection trigger and compute physical dimensions."""
        if not msg.crack_detected or self._latest_ipm is None:
            return

        self._latest_detection = msg
        self._process_measurement(msg)

    def _process_measurement(self, det: CrackDetection) -> None:
        """Perform skeletonization, scale conversion, and JSON report generation."""
        self._inspection_count += 1
        ipm = self._latest_ipm.copy()
        gray = cv2.cvtColor(ipm, cv2.COLOR_BGR2GRAY)

        # 1. Crack Segmentation & Binary Mask Extraction
        binary_mask = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 4
        )

        # Morphological Noise Filter
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        cleaned_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_OPEN, kernel)

        # 2. Skeletonization (Centerline extraction)
        skeleton = self._skeletonize(cleaned_mask)

        # 3. Physical Scale Factor Calculation (Homography Planar Conversion)
        # S = rail_physical_width_mm / rail_pixel_width_in_ipm
        # Rail head occupies ~50% of the IPM width
        rail_pixel_width = float(self._ipm_w * 0.5)
        mm_per_pixel = self._rail_mm / rail_pixel_width

        # 4. Crack Dimension Calculations
        skeleton_pixels = float(np.count_nonzero(skeleton))
        length_mm = skeleton_pixels * mm_per_pixel

        # Distance Transform for Width Estimation
        dist_transform = cv2.distanceTransform(cleaned_mask, cv2.DIST_L2, 5)
        if np.max(dist_transform) > 0:
            max_width_px = float(np.max(dist_transform) * 2.0)
            avg_width_px = float(np.mean(dist_transform[cleaned_mask > 0]) * 2.0)
        else:
            max_width_px = 3.0
            avg_width_px = 1.5

        max_width_mm = max_width_px * mm_per_pixel
        avg_width_mm = avg_width_px * mm_per_pixel

        # 5. Apparent Depth / Visual Severity Estimation (Contrast Shadow Depth)
        # RGB camera limitation disclaimer: Apparent depth is derived from pixel shadow intensity gradient
        roi_pixels = gray[cleaned_mask > 0]
        if len(roi_pixels) > 0:
            shadow_intensity_drop = float(np.mean(gray) - np.mean(roi_pixels))
            apparent_depth_mm = max(0.2, min(5.0, shadow_intensity_drop * 0.08))
        else:
            apparent_depth_mm = 0.5

        severity = self._determine_severity(length_mm, max_width_mm)

        # 6. Persistent Data Storage
        timestamp_str = datetime.now().strftime("%Y_%m_%d")
        folder_name = f"inspection_{self._inspection_count:03d}"
        save_path = os.path.join(self._storage_dir, timestamp_str, folder_name)
        os.makedirs(save_path, exist_ok=True)

        orig_img_path = os.path.join(save_path, "original.jpg")
        proc_img_path = os.path.join(save_path, "processed.jpg")
        mask_img_path = os.path.join(save_path, "crack_mask.jpg")
        json_path = os.path.join(save_path, "result.json")

        cv2.imwrite(orig_img_path, ipm)

        # Annotated Result Overlay
        processed_vis = ipm.copy()
        cv2.putText(
            processed_vis,
            f"Length: {length_mm:.1f} mm | Max Width: {max_width_mm:.2f} mm",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            2,
        )
        cv2.putText(
            processed_vis,
            f"Avg Width: {avg_width_mm:.2f} mm | Severity: {severity}",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 255),
            2,
        )
        cv2.imwrite(proc_img_path, processed_vis)
        cv2.imwrite(mask_img_path, cleaned_mask)

        # Save Metadata JSON
        record_json = {
            "timestamp": datetime.now().isoformat(),
            "inspection_id": folder_name,
            "confidence": float(det.confidence),
            "length_mm": round(length_mm, 2),
            "max_width_mm": round(max_width_mm, 2),
            "avg_width_mm": round(avg_width_mm, 2),
            "apparent_depth_mm": round(apparent_depth_mm, 2),
            "severity": severity,
            "images": {
                "original": "original.jpg",
                "processed": "processed.jpg",
                "mask": "crack_mask.jpg",
            },
        }

        with open(json_path, "w") as f:
            json.dump(record_json, f, indent=4)

        # 7. Publish Inspection Result Message
        res_msg = InspectionResult()
        res_msg.timestamp = det.timestamp
        res_msg.inspection_id = folder_name
        res_msg.crack_detected = True
        res_msg.confidence = det.confidence
        res_msg.crack_length_mm = float(length_mm)
        res_msg.crack_max_width_mm = float(max_width_mm)
        res_msg.crack_avg_width_mm = float(avg_width_mm)
        res_msg.apparent_depth_mm = float(apparent_depth_mm)
        res_msg.severity_rating = severity
        res_msg.image_saved_path = save_path
        res_msg.rover_state = "INSPECTING"

        self._result_pub.publish(res_msg)

        self.get_logger().info(
            f"[MEASUREMENT COMPLETED] ID: {folder_name} | Length: {length_mm:.1f}mm | Max Width: {max_width_mm:.2f}mm | Saved to '{save_path}/'"
        )

    def _skeletonize(self, binary_img: np.ndarray) -> np.ndarray:
        """Morphological thinning skeletonization."""
        size = np.size(binary_img)
        skel = np.zeros(binary_img.shape, np.uint8)
        img = binary_img.copy()

        element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        done = False

        while not done:
            eroded = cv2.erode(img, element)
            temp = cv2.dilate(eroded, element)
            temp = cv2.subtract(img, temp)
            skel = cv2.bitwise_or(skel, temp)
            img = eroded.copy()

            zeros = size - cv2.countNonZero(img)
            if zeros == size:
                done = True

        return skel

    def _determine_severity(self, length_mm: float, width_mm: float) -> str:
        """Classify crack severity based on physical thresholds."""
        if length_mm > 80.0 or width_mm > 3.0:
            return "CRITICAL"
        if length_mm > 35.0 or width_mm > 1.5:
            return "MODERATE"
        return "MINOR"


def main(args=None) -> None:
    rclpy.init(args=args)
    node = CrackMeasurementNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
