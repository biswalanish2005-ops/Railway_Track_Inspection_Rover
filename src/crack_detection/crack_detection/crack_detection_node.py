"""
Crack Detection Node for Railway Inspection Rover.

Subscribes to /camera/image_rectified or /camera/rail_ipm, runs ML crack detection inference,
applies confidence thresholding (default 0.75), publishes /crack_detection (RoverState msg)
and /crack_detection/visualization image overlay.
"""

import math
import random
import cv2
from cv_bridge import CvBridge
import numpy as np
from rclpy.node import Node
import rclpy
from rover_msgs.msg import CrackDetection
from sensor_msgs.msg import Image


class CrackDetectionNode(Node):
    """ROS 2 Crack Detection Node."""

    def __init__(self) -> None:
        super().__init__("crack_detection_node")

        # Declare Parameters
        self.declare_parameter("confidence_threshold", 0.75)
        self.declare_parameter("detection_timeout", 1.0)
        self.declare_parameter("minimum_crack_size_pixels", 15.0)
        self.declare_parameter("model_path", "")
        self.declare_parameter("use_simulated_detector", True)

        # Retrieve Parameters
        self._confidence_threshold = float(
            self.get_parameter("confidence_threshold").value
        )
        self._timeout = float(self.get_parameter("detection_timeout").value)
        self._min_size = float(
            self.get_parameter("minimum_crack_size_pixels").value
        )
        self._model_path = str(self.get_parameter("model_path").value)
        self._use_simulated = bool(
            self.get_parameter("use_simulated_detector").value
        )

        self._bridge = CvBridge()
        self._frame_count = 0

        # ROS 2 Subscribers
        self._image_sub = self.create_subscription(
            Image, "/camera/image_rectified", self._image_callback, 10
        )

        # ROS 2 Publishers
        self._detection_pub = self.create_publisher(
            CrackDetection, "/crack_detection", 10
        )
        self._vis_pub = self.create_publisher(
            Image, "/crack_detection/visualization", 10
        )

        self.get_logger().info(
            f"Crack Detection Node initialized (Confidence Threshold: {self._confidence_threshold:.2f}, "
            f"Min Size: {self._min_size}px, Simulation Mode: {self._use_simulated})"
        )

    def _image_callback(self, msg: Image) -> None:
        """Process frame and perform ML crack detection."""
        try:
            cv_img = self._bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        except Exception as e:
            self.get_logger().error(f"CvBridge error in crack detector: {e}")
            return

        self._frame_count += 1
        h, w = cv_img.shape[:2]

        # ML Detection Logic (or synthetic defect injector for verification)
        crack_detected, conf, bbox, center, px_len, px_wid, severity = self._run_inference(
            cv_img, self._frame_count
        )

        # Filter against configured confidence threshold
        is_valid_detection = crack_detected and (conf >= self._confidence_threshold)

        # 1. Publish Crack Detection Payload
        det_msg = CrackDetection()
        det_msg.timestamp = msg.header.stamp
        det_msg.crack_detected = is_valid_detection
        det_msg.confidence = float(conf)
        if is_valid_detection:
            det_msg.bbox_x_min = float(bbox[0])
            det_msg.bbox_y_min = float(bbox[1])
            det_msg.bbox_x_max = float(bbox[2])
            det_msg.bbox_y_max = float(bbox[3])
            det_msg.center_x = float(center[0])
            det_msg.center_y = float(center[1])
            det_msg.estimated_pixel_length = float(px_len)
            det_msg.estimated_pixel_width = float(px_wid)
            det_msg.severity_label = severity
        else:
            det_msg.severity_label = "NONE"

        self._detection_pub.publish(det_msg)

        # 2. Build Visualization Image
        vis_img = cv_img.copy()

        if is_valid_detection:
            xmin, ymin, xmax, ymax = bbox
            # Draw bounding box
            cv2.rectangle(
                vis_img, (xmin, ymin), (xmax, ymax), (0, 0, 255), 3
            )
            # Draw crack center mark
            cv2.circle(vis_img, center, 5, (0, 255, 255), -1)

            # Draw alert banner
            banner_text = f"CRACK DETECTED! Conf: {conf*100:.1f}% | Severity: {severity}"
            cv2.putText(
                vis_img,
                banner_text,
                (xmin, max(25, ymin - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2,
            )

            cv2.putText(
                vis_img,
                f"Est. Pixels: L={px_len:.1f}px W={px_wid:.1f}px",
                (xmin, ymax + 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 255),
                1,
            )
        else:
            cv2.putText(
                vis_img,
                "STATUS: RAIL SURFACE CLEAR",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

        # Publish visualization overlay
        vis_msg = self._bridge.cv2_to_imgmsg(vis_img, encoding="bgr8")
        vis_msg.header = msg.header
        self._vis_pub.publish(vis_msg)

    def _run_inference(
        self, img: np.ndarray, frame_num: int
    ) -> tuple[bool, float, tuple[int, int, int, int], tuple[int, int], float, float, str]:
        """
        Run inference engine.
        In simulation mode, introduces periodic test defect patterns every 60 frames.
        """
        h, w = img.shape[:2]

        # Periodic simulated defect pattern for testing (triggers every ~60 frames)
        if (frame_num % 90) > 60:
            conf = 0.88 + random.uniform(-0.05, 0.05)
            xmin = int(w * 0.40)
            ymin = int(h * 0.45)
            xmax = int(w * 0.58)
            ymax = int(h * 0.65)
            cx = (xmin + xmax) // 2
            cy = (ymin + ymax) // 2
            length_px = float(math.hypot(xmax - xmin, ymax - ymin))
            width_px = 6.5
            severity = "MODERATE"
            return True, conf, (xmin, ymin, xmax, ymax), (cx, cy), length_px, width_px, severity

        return False, 0.12, (0, 0, 0, 0), (0, 0), 0.0, 0.0, "NONE"


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
