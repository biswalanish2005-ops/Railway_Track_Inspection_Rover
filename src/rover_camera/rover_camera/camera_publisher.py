"""
Camera Publisher Node for Railway Inspection Rover.

Captures live camera frames from Raspberry Pi Camera Module 3 (IMX708 via libcamera/rpicam-vid),
or generates a synthetic railway camera feed in simulation mode.
Publishes /camera/image_raw and /camera/camera_info.
"""

import subprocess
import threading
import time
import cv2
from cv_bridge import CvBridge
import numpy as np
from rclpy.node import Node
import rclpy
from sensor_msgs.msg import CameraInfo, Image


class CameraPublisherNode(Node):
    """ROS 2 Camera Publisher Node."""

    def __init__(self) -> None:
        super().__init__("camera_publisher")

        # Declare Parameters
        self.declare_parameter("device_id", 0)
        self.declare_parameter("frame_width", 1280)
        self.declare_parameter("frame_height", 720)
        self.declare_parameter("fps", 30.0)
        self.declare_parameter("use_simulated_camera", False)
        self.declare_parameter("publish_camera_info", True)
        self.declare_parameter("frame_id", "camera_optical_frame")
        self.declare_parameter("camera_roi", "0.0,0.25,1.0,0.75")

        # Retrieve Parameters
        self._device_id = int(self.get_parameter("device_id").value)
        self._width = int(self.get_parameter("frame_width").value)
        self._height = int(self.get_parameter("frame_height").value)
        self._fps = float(self.get_parameter("fps").value)
        self._use_simulated = bool(self.get_parameter("use_simulated_camera").value)
        self._publish_info = bool(self.get_parameter("publish_camera_info").value)
        self._frame_id = str(self.get_parameter("frame_id").value)
        self._camera_roi = str(self.get_parameter("camera_roi").value).strip()

        self._bridge = CvBridge()
        self._cap = None
        self._proc = None
        self._latest_jpeg = None
        self._frame_lock = threading.Lock()
        self._reader_running = False
        self._sim_frame_count = 0
        self._ready_to_publish = False  # Gate: becomes True after startup grace period

        # ROS Publishers
        self._image_pub = self.create_publisher(Image, "/camera/image_raw", 10)
        self._info_pub = self.create_publisher(CameraInfo, "/camera/camera_info", 10)

        # Initialize Hardware Camera or Fallback to Simulation
        if not self._use_simulated:
            success = self._init_hardware_camera()
            if not success:
                self.get_logger().error(
                    "Hardware camera initialization FAILED and use_simulated_camera is FALSE! Aborting."
                )
                raise RuntimeError("Physical Raspberry Pi Camera Module 3 failed to initialize.")

        # Startup grace period: wait for rpicam-vid to buffer the first frame
        startup_grace = 1.5 if not self._use_simulated else 0.0
        self._grace_timer = None
        self._capture_timer_started = False
        if startup_grace > 0.0:
            self.get_logger().info(
                f"Camera startup grace period: {startup_grace}s — waiting for first JPEG frame..."
            )
            self._grace_timer = self.create_timer(startup_grace, self._on_startup_ready)
        else:
            self._ready_to_publish = True
            timer_period = 1.0 / self._fps
            self.create_timer(timer_period, self._capture_and_publish)

        mode_str = "SIMULATED RAILWAY" if self._use_simulated else "HARDWARE (RPi Cam V3 IMX708)"
        self.get_logger().info(
            f"Camera Publisher initialized in {mode_str} mode ({self._width}x{self._height} @ {self._fps} FPS)"
        )

    def _stream_reader_worker(self) -> None:
        """Background thread worker reading raw MJPEG stream from rpicam-vid."""
        bytes_buf = b""
        while self._reader_running and self._proc is not None and self._proc.poll() is None:
            try:
                chunk = self._proc.stdout.read(65536)
                if not chunk:
                    break
                bytes_buf += chunk
                while True:
                    a = bytes_buf.find(b"\xff\xd8")  # JPEG start marker
                    b = bytes_buf.find(b"\xff\xd9")  # JPEG end marker
                    if a != -1 and b != -1:
                        if b > a:
                            jpg = bytes_buf[a : b + 2]
                            bytes_buf = bytes_buf[b + 2 :]
                            with self._frame_lock:
                                self._latest_jpeg = jpg
                        else:
                            bytes_buf = bytes_buf[a:]
                            break
                    else:
                        break
                if len(bytes_buf) > 2 * 1024 * 1024:
                    bytes_buf = bytes_buf[-1024 * 1024 :]
            except Exception as e:
                time.sleep(0.01)

    def _on_startup_ready(self) -> None:
        """One-shot timer callback: starts the capture timer after grace period."""
        # Cancel ourselves so this only fires once
        if self._grace_timer is not None:
            self._grace_timer.cancel()
            self._grace_timer = None
        if self._capture_timer_started:
            return
        self._capture_timer_started = True
        self._ready_to_publish = True
        timer_period = 1.0 / self._fps
        self.create_timer(timer_period, self._capture_and_publish)
        self.get_logger().info(
            "Camera startup grace period complete. Publishing frames on /camera/image_raw"
        )

    def _init_hardware_camera(self) -> bool:
        """Attempt initialization of physical RPi Camera Module 3 (IMX708) via libcamera/rpicam-vid or V4L2."""
        # Method 1: Try rpicam-vid MJPEG pipe (Native RPi 5 libcamera / PiSP driver)
        try:
            cmd = [
                "rpicam-vid",
                "-t", "0",
                "--codec", "mjpeg",
                "--width", str(self._width),
                "--height", str(self._height),
                "--framerate", str(int(self._fps)),
                "--nopreview",
            ]
            if self._camera_roi:
                cmd.extend(["--roi", self._camera_roi])
            cmd.extend(["-o", "-"])
            self._proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=1024 * 1024
            )
            time.sleep(0.5)
            if self._proc.poll() is None:
                self._reader_running = True
                self._reader_thread = threading.Thread(target=self._stream_reader_worker, daemon=True)
                self._reader_thread.start()
                self.get_logger().info(
                    "Successfully initialized RPi Camera Module 3 via libcamera rpicam-vid pipeline."
                )
                return True
        except Exception as e:
            self.get_logger().warn(f"rpicam-vid pipeline initialization failed: {e}")
            self._proc = None

        # Method 2: OpenCV V4L2 fallback
        try:
            self._cap = cv2.VideoCapture(self._device_id, cv2.CAP_V4L2)
            if self._cap.isOpened():
                self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, self._width)
                self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self._height)
                self._cap.set(cv2.CAP_PROP_FPS, self._fps)
                ret, frame = self._cap.read()
                if ret and frame is not None:
                    self.get_logger().info(f"Successfully opened V4L2 camera device index {self._device_id}")
                    return True
                self._cap.release()
                self._cap = None
        except Exception as e:
            self.get_logger().warn(f"V4L2 camera initialization failed: {e}")
            self._cap = None

        return False

    def _generate_synthetic_rail_frame(self) -> np.ndarray:
        """
        Generate synthetic railway track camera frame with 50° perspective view,
        steel rail surface, sleepers/ties, ballast texture, and motion simulation.
        """
        self._sim_frame_count += 1
        h, w = self._height, self._width
        frame = np.full((h, w, 3), (80, 75, 70), dtype=np.uint8)

        # Ballast gravel background noise
        noise = np.random.randint(-15, 15, (h, w, 3), dtype=np.int16)
        frame = np.clip(frame.astype(np.int16) + noise, 0, 255).astype(np.uint8)

        # Draw moving railway sleepers (ties)
        offset = (self._sim_frame_count * 6) % 120
        for y_pos in range(-60 + offset, h + 120, 120):
            perspective_scale = 0.5 + 0.5 * (y_pos / h)
            sleeper_h = int(25 * perspective_scale)
            if 0 <= y_pos < h:
                x_left = int(w * (0.1 + 0.05 * (1.0 - y_pos / h)))
                x_right = int(w * (0.9 - 0.05 * (1.0 - y_pos / h)))
                cv2.rectangle(
                    frame,
                    (x_left, y_pos),
                    (x_right, min(h, y_pos + sleeper_h)),
                    (40, 50, 60),
                    -1,
                )

        # Draw left and right steel rails
        pts_left_rail = np.array(
            [
                [int(w * 0.32), 0],
                [int(w * 0.40), 0],
                [int(w * 0.36), h],
                [int(w * 0.22), h],
            ],
            np.int32,
        )

        pts_right_rail = np.array(
            [
                [int(w * 0.60), 0],
                [int(w * 0.68), 0],
                [int(w * 0.78), h],
                [int(w * 0.64), h],
            ],
            np.int32,
        )

        cv2.fillPoly(frame, [pts_left_rail], (180, 185, 190))
        cv2.fillPoly(frame, [pts_right_rail], (175, 180, 185))

        cv2.line(
            frame,
            (int(w * 0.36), 0),
            (int(w * 0.29), h),
            (230, 235, 240),
            4,
        )
        cv2.line(
            frame,
            (int(w * 0.64), 0),
            (int(w * 0.71), h),
            (225, 230, 235),
            4,
        )

        cv2.putText(
            frame,
            f"SIMULATED RPi CAM V3 [50 deg Pitch] | Frame: {self._sim_frame_count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 200),
            2,
        )

        return frame

    def _read_hardware_frame(self) -> np.ndarray:
        """Decode and return latest frame from rpicam-vid thread or OpenCV V4L2 capture."""
        jpg = None
        with self._frame_lock:
            if hasattr(self, "_latest_jpeg") and self._latest_jpeg is not None:
                jpg = self._latest_jpeg

        if jpg is not None:
            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            if frame is not None:
                return frame

        if self._cap is not None and self._cap.isOpened():
            ret, cv_img = self._cap.read()
            if ret and cv_img is not None:
                return cv_img

        return None

    def _capture_and_publish(self) -> None:
        """Capture or generate frame and publish ROS Image & CameraInfo messages."""
        if self._use_simulated:
            cv_img = self._generate_synthetic_rail_frame()
        else:
            cv_img = self._read_hardware_frame()
            if cv_img is None:
                self.get_logger().error("Failed to read frame from physical hardware camera!")
                return

        stamp = self.get_clock().now().to_msg()

        # Publish Image Message
        img_msg = self._bridge.cv2_to_imgmsg(cv_img, encoding="bgr8")
        img_msg.header.stamp = stamp
        img_msg.header.frame_id = self._frame_id
        self._image_pub.publish(img_msg)

        # Publish CameraInfo Message
        if self._publish_info:
            info_msg = CameraInfo()
            info_msg.header.stamp = stamp
            info_msg.header.frame_id = self._frame_id
            info_msg.width = self._width
            info_msg.height = self._height
            fx = 1000.0 * (self._width / 1280.0)
            fy = 1000.0 * (self._height / 720.0)
            cx = self._width / 2.0
            cy = self._height / 2.0
            info_msg.k = [fx, 0.0, cx, 0.0, fy, cy, 0.0, 0.0, 1.0]
            info_msg.d = [-0.15, 0.03, 0.0, 0.0, 0.0]
            info_msg.distortion_model = "plumb_bob"
            self._info_pub.publish(info_msg)

    def destroy_node(self) -> None:
        """Release camera resource on shutdown."""
        self._reader_running = False
        if self._proc is not None:
            try:
                self._proc.terminate()
                self._proc.wait(timeout=1.0)
            except Exception:
                pass
            self.get_logger().info("rpicam-vid process terminated.")
        if self._cap is not None and self._cap.isOpened():
            self._cap.release()
            self.get_logger().info("Hardware camera released.")
        super().destroy_node()


def main(args=None) -> None:
    rclpy.init(args=args)
    node = CameraPublisherNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
