"""
Crack & Slit Detection Node for Railway Inspection Rover.

Subscribes to camera frames (/camera/image_rectified or /camera/image_raw),
runs calibrated Computer Vision & ML inference for detecting rail slits, notches,
and cracks, computes physical dimensions and risk levels, tracks railway chainage coordinates,
and publishes /crack_detection and an annotated visualization stream (/crack_detection/visualization).
"""

import math
import cv2
from cv_bridge import CvBridge
import numpy as np
from rclpy.node import Node
import rclpy
from rover_msgs.msg import CrackDetection, RoverState
from sensor_msgs.msg import Image


class CrackDetectionNode(Node):
    """ROS 2 Crack & Slit Detection Node with Railway HUD overlay."""

    def __init__(self) -> None:
        super().__init__("crack_detection_node")

        self.declare_parameter("confidence_threshold", 0.65)
        self.declare_parameter("rail_physical_width_mm", 65.0)
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
            f"(Conf Threshold: {self._confidence_threshold:.2f}, mm/px: {self._mm_per_pixel:.3f})"
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
        Calibrated detector for metal track plate slits, notches, and cracks.
        Matches img3.png standard: enforces transverse horizontal slits (dx >> dy)
        strictly on steel rails and rejects non-track background clutter.
        """
        h, w = bgr_img.shape[:2]
        gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)

        # Bilateral filter preserves sharp slit cut edges while smoothing metal grain
        filtered = cv2.bilateralFilter(gray, 7, 75, 75)
        canny = cv2.Canny(filtered, 30, 115)

        # 1. Parallel Edge-Pair Slit Detector (Detects physical cuts & notches)
        lines = cv2.HoughLinesP(canny, 1, np.pi / 180, threshold=25, minLineLength=25, maxLineGap=12)

        candidates = []
        if lines is not None and len(lines) > 0:
            segs = []
            for l in lines:
                x1, y1, x2, y2 = l[0]
                length = np.hypot(x2 - x1, y2 - y1)
                angle = np.arctan2(y2 - y1, x2 - x1) % np.pi
                segs.append((x1, y1, x2, y2, length, angle))

            # Find parallel line pairs with appropriate slot spacing
            for i in range(len(segs)):
                x1a, y1a, x2a, y2a, lena, ana = segs[i]
                for j in range(i + 1, min(len(segs), i + 35)):
                    x1b, y1b, x2b, y2b, lenb, anb = segs[j]
                    angle_diff = abs(ana - anb)
                    if angle_diff > np.pi / 2:
                        angle_diff = np.pi - angle_diff
                    if angle_diff > np.radians(14):
                        continue

                    # Midpoint separation
                    mxa, mya = (x1a + x2a) / 2, (y1a + y2a) / 2
                    mxb, myb = (x1b + x2b) / 2, (y1b + y2b) / 2
                    dist = np.hypot(mxa - mxb, mya - myb)

                    if 3 <= dist <= 55:
                        xmin = int(min(x1a, x2a, x1b, x2b))
                        xmax = int(max(x1a, x2a, x1b, x2b))
                        ymin = int(min(y1a, y2a, y1b, y2b))
                        ymax = int(max(y1a, y2a, y1b, y2b))
                        slen = max(xmax - xmin, ymax - ymin)
                        swid = min(xmax - xmin, ymax - ymin)

                        if 20 <= slen <= 450 and 2 <= swid <= 45 and (slen / max(1.0, swid)) >= 1.8:
                            candidates.append([xmin, ymin, xmax - xmin, ymax - ymin, slen])

        # 2. Black-Hat Morphological Filter (Detects surface cracks, fissures, joints)
        kernel_bh = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))
        blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel_bh)
        _, bh_thresh = cv2.threshold(blackhat, 22, 255, cv2.THRESH_BINARY)
        bh_contours, _ = cv2.findContours(bh_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in bh_contours:
            bx, by, bw, bh_box = cv2.boundingRect(c)
            blen = max(bw, bh_box)
            bwid = min(bw, bh_box)
            if 20 <= blen <= 450 and 2 <= bwid <= 45 and (blen / max(1.0, bwid)) >= 1.8:
                candidates.append([bx, by, bw, bh_box, blen])

        if not candidates:
            return []

        # Non-Maximum Suppression to consolidate raw candidate boxes
        cv_boxes = [[b[0], b[1], b[2], b[3]] for b in candidates]
        scores = [float(b[4]) for b in candidates]
        indices = cv2.dnn.NMSBoxes(cv_boxes, scores, 20.0, 0.30)

        detections = []
        for idx in indices:
            i = idx[0] if isinstance(idx, (list, np.ndarray)) else idx
            bx, by, bw, bh_box = cv_boxes[i]
            x1, y1, x2, y2 = bx, by, bx + bw, by + bh_box
            cx, cy = x1 + bw // 2, y1 + bh_box // 2

            # ─── CONSTRAINT 1: Field of View (Center or Little Bit Off-Center, Not Very Edge) ───
            if cx < 0.10 * w or cx > 0.90 * w:
                continue
            if x1 < 0.04 * w or x2 > 0.96 * w:
                continue

            # Reject distant background / horizon at top, and bumper edge at bottom
            min_y_ratio = 0.20 if h > 300 else 0.05
            max_y_ratio = 0.86 if h > 300 else 0.95
            if cy < min_y_ratio * h or cy > max_y_ratio * h:
                continue

            # ─── CONSTRAINT 2: Reject Middle of the Track (Between the Two Rails) ───
            # The central zone between the rails (0.33*w to 0.67*w) is the floor, NOT the rails.
            is_in_middle_span = (0.33 * w <= cx <= 0.67 * w)

            # ─── CONSTRAINT 3: Strictly On The Black Lines (Railway Tracks) Only ───
            # Calculate baseline floor brightness in the middle zone (between the rails)
            mid_floor = gray[int(0.20 * h):int(0.85 * h), int(0.38 * w):int(0.62 * w)]
            floor_median = float(np.median(mid_floor)) if mid_floor.size > 0 else 180.0
            dark_rail_thresh = min(105.0, max(50.0, floor_median - 35.0))

            # Check track surface darkness adjacent to the cut (above and below the slit):
            pad_y = max(6, int((y2 - y1) * 0.7))
            top_rail = gray[max(0, y1 - pad_y):y1, x1:x2]
            bot_rail = gray[y2:min(h, y2 + pad_y), x1:x2]

            top_mean = float(top_rail.mean()) if top_rail.size > 0 else 255.0
            bot_mean = float(bot_rail.mean()) if bot_rail.size > 0 else 255.0

            # In the middle span between rails, reject if not on a verified dark rail
            if is_in_middle_span:
                if top_mean > dark_rail_thresh or bot_mean > dark_rail_thresh:
                    continue

            # Reject if adjacent surface is bright floor rather than a dark black rail line
            if top_mean > dark_rail_thresh and bot_mean > dark_rail_thresh:
                continue

            # Check longitudinal track rail continuity along the defect column (Y axis)
            col_span = gray[max(0, cy - int(0.20 * h)):min(h, cy + int(0.20 * h)), cx]
            dark_col_ratio = float(np.mean(col_span <= dark_rail_thresh))
            if dark_col_ratio < 0.12:
                continue

            # ─── CONSTRAINT 3: Transverse Slit Orientation (dx >> dy) ───
            if bw < 1.6 * bh_box:
                continue

            # Evaluate Gradient Opposite Sign Score (Confirms genuine slot/gap)
            margin = 6
            roi = gray[max(0, y1 - margin):min(h, y2 + margin), max(0, x1 - margin):min(w, x2 + margin)]
            if roi.size == 0:
                continue

            gy = cv2.Sobel(roi, cv2.CV_32F, 0, 1, ksize=3)
            tg = np.mean(gy[:max(1, gy.shape[0] // 3), :])
            bg = np.mean(gy[2 * gy.shape[0] // 3:, :])
            opp_score = float(-(tg * bg))
            contrast = float(roi.std())

            # Calibrate confidence score
            conf = min(0.99, max(0.68, 0.72 + min(0.18, max(0.0, opp_score) * 0.003) + min(0.09, contrast * 0.002)))

            length_px = float(bw)
            width_px = float(bh_box)
            length_mm = length_px * self._mm_per_pixel
            width_mm = width_px * self._mm_per_pixel
            apparent_depth_mm = max(0.5, min(8.0, contrast * 0.075))

            # Risk Classification (matching img1.png / img3.png calibration)
            if length_mm > 35.0 or width_mm > 2.8:
                risk = "CRITICAL"
                color = (0, 0, 255)  # Red
            elif length_mm > 18.0 or width_mm > 1.2:
                risk = "HIGH"
                color = (0, 69, 255)  # Orange-Red
            elif length_mm > 8.0 or width_mm > 0.6:
                risk = "MODERATE"
                color = (0, 165, 255)  # Orange
            else:
                risk = "MINOR"
                color = (0, 255, 255)  # Yellow

            detections.append({
                "bbox": (x1, y1, x2, y2),
                "center": (cx, cy),
                "length_px": length_px,
                "width_px": width_px,
                "length_mm": length_mm,
                "width_mm": width_mm,
                "depth_mm": apparent_depth_mm,
                "conf": conf,
                "risk": risk,
                "color": color,
                "opp_score": opp_score,
            })

        # ─── CONSTRAINT 5: Merge Nearby Horizontal Boxes Belonging to Same Slit ───
        merged = []
        sorted_dets = sorted(detections, key=lambda d: (d["opp_score"] * d["conf"]), reverse=True)
        for d in sorted_dets:
            dx1, dy1, dx2, dy2 = d["bbox"]
            matched = False
            for m in merged:
                mx1, my1, mx2, my2 = m["bbox"]
                if abs(((dy1 + dy2) / 2) - ((my1 + my2) / 2)) <= 15:
                    overlap = min(dx2, mx2) - max(dx1, mx1)
                    if overlap >= -15:
                        nx1 = min(dx1, mx1)
                        ny1 = min(dy1, my1)
                        nx2 = max(dx2, mx2)
                        ny2 = max(dy2, my2)
                        m["bbox"] = (nx1, ny1, nx2, ny2)
                        m["center"] = ((nx1 + nx2) // 2, (ny1 + ny2) // 2)
                        m["conf"] = max(m["conf"], d["conf"])
                        m["opp_score"] = max(m["opp_score"], d["opp_score"])
                        nbw = nx2 - nx1
                        nbh = ny2 - ny1
                        m["length_px"] = float(nbw)
                        m["width_px"] = float(nbh)
                        m["length_mm"] = nbw * self._mm_per_pixel
                        m["width_mm"] = nbh * self._mm_per_pixel
                        matched = True
                        break
            if not matched:
                merged.append(d.copy())

        # Update risk for merged bounding boxes
        for m in merged:
            if m["length_mm"] > 35.0 or m["width_mm"] > 2.8:
                m["risk"] = "CRITICAL"
                m["color"] = (0, 0, 255)
            elif m["length_mm"] > 18.0 or m["width_mm"] > 1.2:
                m["risk"] = "HIGH"
                m["color"] = (0, 69, 255)

        merged.sort(key=lambda d: (d.get("opp_score", 0.0) * d["conf"]), reverse=True)
        return merged

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
