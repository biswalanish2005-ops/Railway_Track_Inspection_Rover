"""
Crack & Slit Detection Node for Railway Inspection Rover.

Subscribes to camera frames (/camera/image_rectified or /camera/image_raw),
runs calibrated Computer Vision & ML inference for detecting rail slits, notches,
and cracks, computes physical dimensions and risk levels, tracks railway chainage coordinates,
and publishes /crack_detection and an annotated visualization stream (/crack_detection/visualization).
"""

import math
import os
import sys
import cv2
from cv_bridge import CvBridge
import numpy as np
from rclpy.node import Node
import rclpy
from rover_msgs.msg import CrackDetection, RoverState
from sensor_msgs.msg import Image

# Ensure workspace root is in path for sharing calibrated detector
workspace_dir = os.path.expanduser("~/Desktop/Railway_Inspection_Rover")
if workspace_dir not in sys.path:
    sys.path.insert(0, workspace_dir)


class CrackDetectionNode(Node):
    """ROS 2 Crack & Slit Detection Node with Railway HUD overlay."""

    def __init__(self) -> None:
        super().__init__("crack_detection_node")

        self.declare_parameter("confidence_threshold", 0.65)
        self.declare_parameter("rail_physical_width_mm", 10.0)  # 1.0 cm standard tape width
        self.declare_parameter("mm_per_pixel", 0.35)
        self.declare_parameter("use_simulated_detector", False)
        self.declare_parameter("track_y_min_ratio", 0.08)
        self.declare_parameter("left_rail_x_min", 0.08)
        self.declare_parameter("left_rail_x_max", 0.45)
        self.declare_parameter("right_rail_x_min", 0.55)
        self.declare_parameter("right_rail_x_max", 0.88)

        self._confidence_threshold = float(
            self.get_parameter("confidence_threshold").value
        )
        self._rail_width_mm = float(
            self.get_parameter("rail_physical_width_mm").value
        )
        self._mm_per_pixel = float(
            self.get_parameter("mm_per_pixel").value
        )
        self._use_simulated = bool(
            self.get_parameter("use_simulated_detector").value
        )
        self._track_y_min_ratio = float(
            self.get_parameter("track_y_min_ratio").value
        )
        self._left_rail_x_min = float(
            self.get_parameter("left_rail_x_min").value
        )
        self._left_rail_x_max = float(
            self.get_parameter("left_rail_x_max").value
        )
        self._right_rail_x_min = float(
            self.get_parameter("right_rail_x_min").value
        )
        self._right_rail_x_max = float(
            self.get_parameter("right_rail_x_max").value
        )

        self._bridge = CvBridge()
        self._frame_count = 0

        # Rover Telemetry State & Location Coordinates (without LIDAR)
        self._location_x = 0.0
        self._location_y = 0.0
        self._chainage_str = "CH 00+00.00m"
        self._rover_state_str = "IDLE"

        # Subscribers
        self._rectified_sub = self.create_subscription(
            Image, "/camera/image_rectified", self._rectified_callback, 10
        )
        self._raw_sub = self.create_subscription(
            Image, "/camera/image_raw", self._raw_callback, 10
        )
        self._rover_state_sub = self.create_subscription(
            RoverState, "/rover_state", self._rover_state_callback, 10
        )

        # Publishers
        self._detection_pub = self.create_publisher(
            CrackDetection, "/crack_detection", 10
        )
        self._vis_pub = self.create_publisher(
            Image, "/crack_detection/visualization", 10
        )

        self._last_processed_stamp = None

        self.get_logger().info(
            f"Calibrated Crack & Slit Detection Node ACTIVE "
            f"(Conf Threshold: {self._confidence_threshold:.2f}, Tape Width: {self._rail_width_mm:.1f}mm)"
        )

    def _rover_state_callback(self, msg: RoverState) -> None:
        """Cache rover odometry coordinates and state."""
        self._location_x = float(msg.location_x)
        self._location_y = float(msg.location_y)
        self._chainage_str = msg.chainage_station if msg.chainage_station else f"CH 00+{abs(self._location_x):05.2f}m"
        self._rover_state_str = msg.current_state

    def _rectified_callback(self, msg: Image) -> None:
        """Primary callback when rectified stream is available."""
        self._process_frame(msg)

    def _raw_callback(self, msg: Image) -> None:
        """Fallback callback if rectified frames are not available."""
        if self._last_processed_stamp is not None:
            # Check if recently handled by rectified callback
            dt = abs(msg.header.stamp.sec - self._last_processed_stamp.sec)
            if dt < 0.05:
                return
        self._process_frame(msg)

    def _process_frame(self, msg: Image) -> None:
        """Process incoming image and run calibrated detection."""
        try:
            cv_img = self._bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        except Exception as e:
            self.get_logger().error(f"CvBridge decode error: {e}")
            return

        self._last_processed_stamp = msg.header.stamp
        self._frame_count += 1
        h, w = cv_img.shape[:2]

        # Run Real Slit & Crack Detection Engine
        detections = self._detect_slits_and_cracks(cv_img)

        # Filter against confidence threshold
        valid_dets = [d for d in detections if d["conf"] >= self._confidence_threshold]
        crack_detected = len(valid_dets) > 0

        # Best detection (highest risk / confidence)
        best_det = valid_dets[0] if valid_dets else None

        # 1. Build and Publish CrackDetection ROS Message
        det_msg = CrackDetection()
        det_msg.timestamp = msg.header.stamp
        det_msg.crack_detected = crack_detected
        det_msg.location_x = float(self._location_x)
        det_msg.location_y = float(self._location_y)
        det_msg.chainage_station = self._chainage_str

        if crack_detected and best_det is not None:
            det_msg.confidence = float(best_det["conf"])
            det_msg.bbox_x_min = float(best_det["bbox"][0])
            det_msg.bbox_y_min = float(best_det["bbox"][1])
            det_msg.bbox_x_max = float(best_det["bbox"][2])
            det_msg.bbox_y_max = float(best_det["bbox"][3])
            det_msg.center_x = float(best_det["center"][0])
            det_msg.center_y = float(best_det["center"][1])
            det_msg.estimated_pixel_length = float(best_det["length_px"])
            det_msg.estimated_pixel_width = float(best_det["width_px"])
            det_msg.estimated_length_mm = float(best_det["length_mm"])
            det_msg.estimated_width_mm = float(best_det["width_mm"])
            det_msg.estimated_depth_mm = float(best_det["depth_mm"])
            det_msg.severity_label = best_det["risk"]
        else:
            det_msg.confidence = 0.0
            det_msg.severity_label = "NONE"

        self._detection_pub.publish(det_msg)

        # 2. Build Annotated Railway Engineering Visualization Overlay
        vis_img = self._render_hud_overlay(cv_img, valid_dets)

        vis_msg = self._bridge.cv2_to_imgmsg(vis_img, encoding="bgr8")
        vis_msg.header = msg.header
        self._vis_pub.publish(vis_msg)

    def _detect_slits_and_cracks(self, bgr_img: np.ndarray) -> list[dict]:
        """
        Calibrated railway track slit, cut, and breakage detector.
        Strictly inspects black railway stripes; rejects track bed and frame borders.
        Calibrated with ground truth tape width = 1.0 cm (10.0 mm).
        """
        try:
            from rover_camera_display import detect_slits_and_cracks
            return detect_slits_and_cracks(bgr_img)
        except Exception:
            return []

    def _render_hud_overlay(self, frame: np.ndarray, detections: list[dict]) -> np.ndarray:
        """Render Railway Standard Inspection HUD with bounding boxes and coordinates."""
        vis = frame.copy()
        h, w = vis.shape[:2]

        # Draw detected cracks / slits
        for d in detections[:3]:  # Top detections
            x1, y1, x2, y2 = d["bbox"]
            color = d["color"]

            # Bounding box
            cv2.rectangle(vis, (x1, y1), (x2, y2), color, 3)
            cv2.circle(vis, d["center"], 5, (0, 255, 255), -1)

            # Label box
            label = f"{d['risk']} DEFECT | Conf: {d['conf']*100:.1f}%"
            dims = f"L: {d['length_mm']:.1f}mm | W: {d['width_mm']:.1f}mm | D: {d['depth_mm']:.1f}mm"

            box_w = 340
            cv2.rectangle(vis, (x1, max(0, y1 - 48)), (x1 + box_w, max(48, y1)), (18, 22, 30), -1)
            cv2.putText(vis, label, (x1 + 6, max(18, y1 - 28)), cv2.FONT_HERSHEY_SIMPLEX, 0.52, color, 2)
            cv2.putText(vis, dims, (x1 + 6, max(38, y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (255, 255, 255), 1)

        # Top Railway HUD Banner
        has_critical = any(d["risk"] in ("HIGH", "CRITICAL") for d in detections)
        if has_critical:
            status_text = "STATUS: CRACK DETECTED (RISK > MODERATE) — STOPPING"
            status_color = (0, 0, 255)
        elif detections:
            status_text = "STATUS: MINOR DEFECT LOGGED — PATROLLING"
            status_color = (0, 165, 255)
        else:
            status_text = f"STATUS: PATROLLING TRACK [{self._rover_state_str}]"
            status_color = (0, 255, 0)

        coord_str = f"LOC: [X: {self._location_x:+.2f}m, Y: {self._location_y:+.2f}m] | {self._chainage_str} | TRACK: L1 (MAIN)"

        # Top banner background
        cv2.rectangle(vis, (0, 0), (w, 68), (14, 18, 26), -1)
        cv2.putText(
            vis,
            f"RAILWAY ROVER — {coord_str}",
            (12, 24),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.52,
            (0, 220, 255),
            2,
        )
        cv2.putText(
            vis,
            f"{status_text} | Active Defects: {len(detections)}",
            (12, 52),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.50,
            status_color,
            2,
        )

        return vis


def main(args=None) -> None:
    rclpy.init(args=args)
    node = CrackDetectionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
