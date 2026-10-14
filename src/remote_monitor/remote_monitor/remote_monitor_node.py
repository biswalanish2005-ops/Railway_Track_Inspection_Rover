"""
Remote Monitoring Web Interface Node for Railway Inspection Rover.

Serves an embedded HTML5 web dashboard and live MJPEG video stream on port 8080.
Exposes real-time rover telemetry, ML crack detection alerts, physical measurements,
and web-based Emergency Stop / Reset controls over local network.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading
import time
import cv2
from cv_bridge import CvBridge
import rclpy
from rclpy.node import Node
from rover_msgs.msg import CrackDetection, InspectionResult, RoverState
from rover_msgs.srv import EmergencyStop
from sensor_msgs.msg import Image

HTML_DASHBOARD = """<!DOCTYPE html>
<html>
<head>
    <title>Autonomous Railway Inspection Rover - Monitoring Dashboard</title>
    <meta viewport="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121824; color: #e1e6f0; margin: 0; padding: 20px; }
        .header { display: flex; justify-content: space-between; align-items: center; background: #1b2333; padding: 15px 25px; border-radius: 8px; border-bottom: 3px solid #00d2ff; }
        h1 { margin: 0; font-size: 22px; color: #00d2ff; }
        .grid { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-top: 20px; }
        .card { background: #1b2333; padding: 20px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
        .card-title { font-size: 16px; font-weight: bold; margin-bottom: 15px; color: #a0aec0; border-bottom: 1px solid #2d3748; padding-bottom: 8px; }
        .stream-container img { width: 100%; border-radius: 6px; border: 2px solid #2d3748; }
        .badge { padding: 5px 12px; border-radius: 4px; font-weight: bold; font-size: 14px; text-transform: uppercase; }
        .badge-idle { background: #4a5568; color: #fff; }
        .badge-moving { background: #3182ce; color: #fff; }
        .badge-inspecting { background: #d69e2e; color: #fff; }
        .badge-stopped { background: #e53e3e; color: #fff; }
        .stat-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #2a3447; }
        .stat-label { color: #a0aec0; }
        .stat-value { font-weight: bold; }
        .btn { padding: 12px 20px; border: none; border-radius: 6px; font-size: 14px; font-weight: bold; cursor: pointer; transition: 0.2s; width: 100%; margin-top: 10px; }
        .btn-estop { background: #e53e3e; color: #fff; }
        .btn-estop:hover { background: #c53030; }
        .btn-reset { background: #38a169; color: #fff; }
        .btn-reset:hover { background: #2f855a; }
    </style>
</head>
<body>
    <div class="header">
        <h1>AUTONOMOUS RAILWAY TRACK INSPECTION ROVER</h1>
        <div id="status-badge" class="badge badge-idle">SYSTEM IDLE</div>
    </div>

    <div class="grid">
        <div class="card">
            <div class="card-title">LIVE CAMERA FEED & ML CRACK DETECTOR</div>
            <div class="stream-container">
                <img src="/video_feed" alt="Live Camera Video Stream">
            </div>
        </div>

        <div>
            <div class="card">
                <div class="card-title">ROVER TELEMETRY</div>
                <div class="stat-row"><span class="stat-label">Current State:</span><span id="tele-state" class="stat-value">IDLE</span></div>
                <div class="stat-row"><span class="stat-label">Linear Speed:</span><span id="tele-speed" class="stat-value">0.00 m/s</span></div>
                <div class="stat-row"><span class="stat-label">Angular Speed:</span><span id="tele-turn" class="stat-value">0.00 rad/s</span></div>
                <div class="stat-row"><span class="stat-label">Motor Status:</span><span id="tele-motor" class="stat-value">ENABLED</span></div>
                <div class="stat-row"><span class="stat-label">Watchdog:</span><span id="tele-watchdog" class="stat-value">INACTIVE</span></div>
            </div>

            <div class="card" style="margin-top: 20px;">
                <div class="card-title">INSPECTION MEASUREMENTS</div>
                <div class="stat-row"><span class="stat-label">Last Crack Detected:</span><span id="insp-det" class="stat-value">NONE</span></div>
                <div class="stat-row"><span class="stat-label">Confidence:</span><span id="insp-conf" class="stat-value">0.0%</span></div>
                <div class="stat-row"><span class="stat-label">Crack Length:</span><span id="insp-len" class="stat-value">0.0 mm</span></div>
                <div class="stat-row"><span class="stat-label">Max Width:</span><span id="insp-max-w" class="stat-value">0.00 mm</span></div>
                <div class="stat-row"><span class="stat-label">Avg Width:</span><span id="insp-avg-w" class="stat-value">0.00 mm</span></div>
                <div class="stat-row"><span class="stat-label">Apparent Depth:</span><span id="insp-depth" class="stat-value">0.00 mm</span></div>
                <div class="stat-row"><span class="stat-label">Severity:</span><span id="insp-severity" class="stat-value">CLEAR</span></div>
            </div>

            <div class="card" style="margin-top: 20px;">
                <div class="card-title">SAFETY CONTROLS</div>
                <button class="btn btn-estop" onclick="triggerEstop(true)">EMERGENCY STOP</button>
                <button class="btn btn-reset" onclick="triggerEstop(false)">CLEAR / RESET E-STOP</button>
            </div>
        </div>
    </div>

    <script>
        function updateTelemetry() {
            fetch('/api/telemetry')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('tele-state').innerText = data.state;
                    document.getElementById('tele-speed').innerText = data.linear_speed.toFixed(2) + ' m/s';
                    document.getElementById('tele-turn').innerText = data.angular_speed.toFixed(2) + ' rad/s';
                    document.getElementById('tele-motor').innerText = data.motor_enabled ? 'ENABLED' : 'DISABLED';
                    document.getElementById('tele-watchdog').innerText = data.watchdog ? 'ACTIVE' : 'INACTIVE';
                    
                    const badge = document.getElementById('status-badge');
                    badge.innerText = 'STATE: ' + data.state;
                    badge.className = 'badge badge-' + data.state.toLowerCase();

                    if (data.last_inspection) {
                        const insp = data.last_inspection;
                        document.getElementById('insp-det').innerText = insp.id;
                        document.getElementById('insp-conf').innerText = (insp.conf * 100).toFixed(1) + '%';
                        document.getElementById('insp-len').innerText = insp.len_mm.toFixed(1) + ' mm';
                        document.getElementById('insp-max-w').innerText = insp.max_w_mm.toFixed(2) + ' mm';
                        document.getElementById('insp-avg-w').innerText = insp.avg_w_mm.toFixed(2) + ' mm';
                        document.getElementById('insp-depth').innerText = insp.depth_mm.toFixed(2) + ' mm';
                        document.getElementById('insp-severity').innerText = insp.severity;
                    }
                });
        }

        function triggerEstop(enable) {
            fetch('/api/estop?set=' + enable, { method: 'POST' })
                .then(r => r.json())
                .then(res => alert(res.message));
        }

        setInterval(updateTelemetry, 500);
    </script>
</body>
</html>
"""


class WebRequestHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler serving Web Dashboard & MJPEG Stream."""

    node_ref = None

    def do_GET(self) -> None:
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_DASHBOARD.encode("utf-8"))

        elif self.path == "/api/telemetry":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            node = WebRequestHandler.node_ref
            data = {
                "state": node.current_state,
                "linear_speed": node.linear_speed,
                "angular_speed": node.angular_speed,
                "motor_enabled": node.motor_enabled,
                "watchdog": node.watchdog_active,
                "last_inspection": node.last_inspection_data,
            }
            self.wfile.write(json.dumps(data).encode("utf-8"))

        elif self.path == "/video_feed":
            self.send_response(200)
            self.send_header(
                "Content-Type", "multipart/x-mixed-replace; boundary=frame"
            )
            self.end_headers()

            node = WebRequestHandler.node_ref
            while True:
                if node.latest_jpeg is not None:
                    try:
                        self.wfile.write(b"--frame\r\n")
                        self.send_header("Content-Type", "image/jpeg")
                        self.send_header("Content-Length", str(len(node.latest_jpeg)))
                        self.end_headers()
                        self.wfile.write(node.latest_jpeg)
                        self.wfile.write(b"\r\n")
                        time.sleep(0.05)
                    except Exception:
                        break
                else:
                    time.sleep(0.1)

    def do_POST(self) -> None:
        if self.path.startswith("/api/estop"):
            set_val = "set=true" in self.path
            node = WebRequestHandler.node_ref
            node.send_estop(set_val)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            msg = "Emergency stop triggered" if set_val else "Emergency stop cleared"
            self.wfile.write(json.dumps({"success": True, "message": msg}).encode("utf-8"))

    def log_message(self, format, *args) -> None:
        """Suppress standard HTTP server access log spam."""
        pass


class RemoteMonitorNode(Node):
    """ROS 2 Remote Monitoring Web Node."""

    def __init__(self) -> None:
        super().__init__("remote_monitor_node")

        self.declare_parameter("port", 8080)
        self._port = int(self.get_parameter("port").value)

        self._bridge = CvBridge()

        # Telemetry State
        self.current_state = "IDLE"
        self.linear_speed = 0.0
        self.angular_speed = 0.0
        self.motor_enabled = True
        self.watchdog_active = False
        self.latest_jpeg = None
        self.last_inspection_data = None

        # ROS 2 Subscribers
        self.create_subscription(RoverState, "/rover_state", self._state_cb, 10)
        self.create_subscription(
            InspectionResult, "/inspection_result", self._result_cb, 10
        )
        self.create_subscription(
            Image, "/camera/processed_overlay", self._image_cb, 10
        )

        # Service Client for E-Stop
        self._estop_client = self.create_client(EmergencyStop, "/emergency_stop")

        # Set reference for web server
        WebRequestHandler.node_ref = self

        # Start HTTP Server in background thread
        self._server = HTTPServer(("0.0.0.0", self._port), WebRequestHandler)
        self._server_thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._server_thread.start()

        self.get_logger().info(
            f"Remote Monitoring Web Dashboard ACTIVE on http://0.0.0.0:{self._port}"
        )

    def _state_cb(self, msg: RoverState) -> None:
        self.current_state = msg.current_state
        self.linear_speed = float(msg.current_linear_speed)
        self.angular_speed = float(msg.current_angular_speed)
        self.motor_enabled = msg.motor_enabled
        self.watchdog_active = msg.watchdog_active

    def _result_cb(self, msg: InspectionResult) -> None:
        self.last_inspection_data = {
            "id": msg.inspection_id,
            "conf": float(msg.confidence),
            "len_mm": float(msg.crack_length_mm),
            "max_w_mm": float(msg.crack_max_width_mm),
            "avg_w_mm": float(msg.crack_avg_width_mm),
            "depth_mm": float(msg.apparent_depth_mm),
            "severity": msg.severity_rating,
        }

    def _image_cb(self, msg: Image) -> None:
        try:
            cv_img = self._bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
            _, jpeg = cv2.imencode(".jpg", cv_img, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            self.latest_jpeg = jpeg.tobytes()
        except Exception as e:
            self.get_logger().error(f"Image compression error: {e}")

    def send_estop(self, set_estop: bool) -> None:
        if not self._estop_client.wait_for_service(timeout_sec=1.0):
            return
        req = EmergencyStop.Request()
        req.set_estop = set_estop
        req.reason = "Web Dashboard Triggered"
        self._estop_client.call_async(req)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = RemoteMonitorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
