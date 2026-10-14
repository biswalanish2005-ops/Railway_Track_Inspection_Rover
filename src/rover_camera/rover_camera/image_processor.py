"""
Image Processor Node for Railway Inspection Rover.

Executes camera calibration undistortion, rail ROI extraction,
Inverse Perspective Mapping (IPM) homography transformation,
illumination normalization (CLAHE), noise reduction, and visual overlays.
"""

import cv2
from cv_bridge import CvBridge
import numpy as np
from rclpy.node import Node
import rclpy
from sensor_msgs.msg import CameraInfo, Image


class ImageProcessorNode(Node):
    """ROS 2 Node for camera calibration, IPM perspective transformation, and rail ROI processing."""

    def __init__(self) -> None:
        super().__init__("image_processor")

        # Declare ROS Parameters
        self.declare_parameter("roi_top_left_x", 0.20)
        self.declare_parameter("roi_top_left_y", 0.30)
        self.declare_parameter("roi_top_right_x", 0.80)
        self.declare_parameter("roi_top_right_y", 0.30)
        self.declare_parameter("roi_bottom_right_x", 0.90)
        self.declare_parameter("roi_bottom_right_y", 0.95)
        self.declare_parameter("roi_bottom_left_x", 0.10)
        self.declare_parameter("roi_bottom_left_y", 0.95)

        self.declare_parameter("ipm_output_width", 400)
        self.declare_parameter("ipm_output_height", 600)
        self.declare_parameter("rail_physical_width_mm", 70.0)

        self.declare_parameter("clahe_clip_limit", 2.0)
        self.declare_parameter("clahe_tile_grid_size", 8)
        self.declare_parameter("gaussian_blur_kernel", 5)

        # Retrieve Parameters
        self._load_parameters()

        # CV Bridge
        self._bridge = CvBridge()

        # Calibration Matrices (Default / Updated via CameraInfo)
        self._camera_matrix = np.array(
            [[1000.0, 0.0, 640.0], [0.0, 1000.0, 360.0], [0.0, 0.0, 1.0]],
            dtype=np.float32,
        )
        self._dist_coeffs = np.array([-0.15, 0.03, 0.0, 0.0, 0.0], dtype=np.float32)

        # CLAHE Equalizer
        self._clahe = cv2.createCLAHE(
            clipLimit=self._clahe_clip_limit,
            tileGridSize=(self._clahe_tile_size, self._clahe_tile_size),
        )

        # ROS 2 Subscribers
        self._image_sub = self.create_subscription(
            Image, "/camera/image_raw", self._image_callback, 10
        )
        self._info_sub = self.create_subscription(
            CameraInfo, "/camera/camera_info", self._camera_info_callback, 10
        )

        # ROS 2 Publishers
        self._rectified_pub = self.create_publisher(Image, "/camera/image_rectified", 10)
        self._ipm_pub = self.create_publisher(Image, "/camera/rail_ipm", 10)
        self._overlay_pub = self.create_publisher(Image, "/camera/processed_overlay", 10)

        self.get_logger().info(
            "Image Processor Node initialized. Ready for calibration undistortion and IPM extraction."
        )

    def _load_parameters(self) -> None:
        """Read configuration parameters from ROS parameter server."""
        self._tl_x = float(self.get_parameter("roi_top_left_x").value)
        self._tl_y = float(self.get_parameter("roi_top_left_y").value)
        self._tr_x = float(self.get_parameter("roi_top_right_x").value)
        self._tr_y = float(self.get_parameter("roi_top_right_y").value)
        self._br_x = float(self.get_parameter("roi_bottom_right_x").value)
        self._br_y = float(self.get_parameter("roi_bottom_right_y").value)
        self._bl_x = float(self.get_parameter("roi_bottom_left_x").value)
        self._bl_y = float(self.get_parameter("roi_bottom_left_y").value)

        self._ipm_w = int(self.get_parameter("ipm_output_width").value)
        self._ipm_h = int(self.get_parameter("ipm_output_height").value)
        self._rail_mm = float(self.get_parameter("rail_physical_width_mm").value)

        self._clahe_clip_limit = float(self.get_parameter("clahe_clip_limit").value)
        self._clahe_tile_size = int(self.get_parameter("clahe_tile_grid_size").value)
        self._blur_kernel = int(self.get_parameter("gaussian_blur_kernel").value)
        if self._blur_kernel % 2 == 0:
            self._blur_kernel += 1  # Ensure odd kernel size

    def _camera_info_callback(self, msg: CameraInfo) -> None:
        """Update intrinsic parameters from CameraInfo topic."""
        if len(msg.k) == 9:
            self._camera_matrix = np.array(msg.k, dtype=np.float32).reshape(3, 3)
        if len(msg.d) >= 4:
            self._dist_coeffs = np.array(msg.d, dtype=np.float32)

    def _image_callback(self, msg: Image) -> None:
        """Core Image Processing Pipeline."""
        try:
            raw_bgr = self._bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        except Exception as e:
            self.get_logger().error(f"CvBridge conversion error: {e}")
            return

        h, w = raw_bgr.shape[:2]

        # 1. Undistortion (Camera Calibration)
        rectified_bgr = cv2.undistort(raw_bgr, self._camera_matrix, self._dist_coeffs)

        # 2. Extract Rail ROI Polygon & Inverse Perspective Mapping (IPM)
        pts_src = np.float32(
            [
                [self._tl_x * w, self._tl_y * h],
                [self._tr_x * w, self._tr_y * h],
                [self._br_x * w, self._br_y * h],
                [self._bl_x * w, self._bl_y * h],
            ]
        )

        pts_dst = np.float32(
            [
                [0, 0],
                [self._ipm_w - 1, 0],
                [self._ipm_w - 1, self._ipm_h - 1],
                [0, self._ipm_h - 1],
            ]
        )

        homography_matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)
        ipm_bgr = cv2.warpPerspective(
            rectified_bgr, homography_matrix, (self._ipm_w, self._ipm_h)
        )

        # 3. Illumination Normalization & Contrast Enhancement (CLAHE)
        gray_ipm = cv2.cvtColor(ipm_bgr, cv2.COLOR_BGR2GRAY)
        clahe_enhanced = self._clahe.apply(gray_ipm)
        blurred = cv2.GaussianBlur(clahe_enhanced, (self._blur_kernel, self._blur_kernel), 0)

        # Convert enhanced IPM back to 3-channel for visualization
        ipm_enhanced_bgr = cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR)

        # 4. Construct Visual Diagnostic Overlay
        overlay_bgr = rectified_bgr.copy()
        pts_roi_int = pts_src.astype(np.int32).reshape((-1, 1, 2))
        cv2.polylines(overlay_bgr, [pts_roi_int], isClosed=True, color=(0, 255, 0), thickness=3)

        # Scale Factor Annotation (mm per pixel in top-down IPM view)
        mm_per_pixel = self._rail_mm / float(self._ipm_w * 0.4)  # Approx rail pixel fraction
        cv2.putText(
            overlay_bgr,
            f"ROI 50deg IPM Homography | Scale: ~{mm_per_pixel:.3f} mm/px",
            (20, h - 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )

        # Construct Quad-View Summary Image (2x2 Grid)
        raw_small = cv2.resize(raw_bgr, (w // 2, h // 2))
        overlay_small = cv2.resize(overlay_bgr, (w // 2, h // 2))
        ipm_small = cv2.resize(ipm_enhanced_bgr, (w // 2, h // 2))

        # Blank 4th tile for stats
        stats_tile = np.zeros((h // 2, w // 2, 3), dtype=np.uint8)
        cv2.putText(stats_tile, "RAILWAY INSPECTION PIPELINE", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.putText(stats_tile, f"Original Res: {w}x{h}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(stats_tile, f"IPM Size: {self._ipm_w}x{self._ipm_h}", (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(stats_tile, f"CLAHE Clip: {self._clahe_clip_limit}", (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(stats_tile, f"Gaussian Kernel: {self._blur_kernel}x{self._blur_kernel}", (20, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(stats_tile, "Status: PIPELINE ACTIVE", (20, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        top_row = np.hstack((raw_small, overlay_small))
        bottom_row = np.hstack((ipm_small, stats_tile))
        quad_view = np.vstack((top_row, bottom_row))

        # 5. Publish ROS Topics
        stamp = msg.header.stamp

        rect_msg = self._bridge.cv2_to_imgmsg(rectified_bgr, encoding="bgr8")
        rect_msg.header.stamp = stamp
        rect_msg.header.frame_id = msg.header.frame_id
        self._rectified_pub.publish(rect_msg)

        ipm_msg = self._bridge.cv2_to_imgmsg(ipm_enhanced_bgr, encoding="bgr8")
        ipm_msg.header.stamp = stamp
        ipm_msg.header.frame_id = msg.header.frame_id
        self._ipm_pub.publish(ipm_msg)

        quad_msg = self._bridge.cv2_to_imgmsg(quad_view, encoding="bgr8")
        quad_msg.header.stamp = stamp
        quad_msg.header.frame_id = msg.header.frame_id
        self._overlay_pub.publish(quad_msg)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = ImageProcessorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
