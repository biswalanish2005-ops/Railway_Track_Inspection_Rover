"""
Remote Monitoring Web Interface Node for Railway Inspection Rover.

Serves an embedded HTML5 web dashboard and live MJPEG video stream on port 8080.
Exposes real-time rover telemetry, standard railway chainage coordinates,
calibrated ML crack/slit detection bounding boxes, physical measurements,
urgent alert dispatches for defects > MODERATE risk, and Emergency Stop controls.
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
    <title>Autonomous Railway Track Inspection Rover - Remote Inspector Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f141f; color: #e1e6f0; margin: 0; padding: 20px; }
        .header { display: flex; justify-content: space-between; align-items: center; background: #182030; padding: 15px 25px; border-radius: 8px; border-bottom: 3px solid #00d2ff; }
        h1 { margin: 0; font-size: 20px; color: #00d2ff; letter-spacing: 0.5px; }
        .grid { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-top: 20px; }
        .card { background: #182030; padding: 18px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.4); border: 1px solid #253147; }
        .card-title { font-size: 15px; font-weight: bold; margin-bottom: 12px; color: #94a3b8; border-bottom: 1px solid #253147; padding-bottom: 8px; display: flex; justify-content: space-between; }
        .stream-container img { width: 100%; border-radius: 6px; border: 2px solid #2d3c54; display: block; }
        .badge { padding: 5px 12px; border-radius: 4px; font-weight: bold; font-size: 13px; text-transform: uppercase; }
        .badge-idle { background: #475569; color: #fff; }
        .badge-moving, .badge-searching { background: #0284c7; color: #fff; }
        .badge-slowing { background: #d97706; color: #fff; }
        .badge-inspecting { background: #dc2626; color: #fff; animation: pulse 1s infinite alternate; }
        .badge-resuming { background: #16a34a; color: #fff; }
        .badge-stopped { background: #b91c1c; color: #fff; }
        @keyframes pulse { from { opacity: 0.7; } to { opacity: 1; } }
        .stat-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #1e293b; font-size: 14px; }
        .stat-label { color: #94a3b8; }
        .stat-value { font-weight: bold; color: #f1f5f9; }
        .highlight { color: #38bdf8; }
        .alert-box { background: #3b1114; border: 2px solid #ef4444; border-radius: 6px; padding: 12px; margin-top: 15px; display: none; }
        .alert-title { color: #f87171; font-weight: bold; font-size: 14px; margin-bottom: 6px; display: flex; align-items: center; }
        .alert-body { font-size: 13px; line-height: 1.4; color: #fca5a5; }
        .btn { padding: 12px 20px; border: none; border-radius: 6px; font-size: 14px; font-weight: bold; cursor: pointer; transition: 0.2s; width: 100%; margin-top: 10px; }
        .btn-estop { background: #dc2626; color: #fff; }
        .btn-estop:hover { background: #b91c1c; }
        .btn-reset { background: #16a34a; color: #fff; }
        .btn-reset:hover { background: #15803d; }
    </style>
</head>
<body>
    <div class="header">
        <h1>AUTONOMOUS RAILWAY TRACK INSPECTION ROVER</h1>
        <div id="status-badge" class="badge badge-idle">SYSTEM IDLE</div>
    </div>

    <div class="grid">
        <div class="card">
            <div class="card-title">
                <span>LIVE CAMERA FEED & ML CRACK / SLIT DETECTOR</span>
                <span id="chainage-indicator" class="highlight">CH 00+00.00m</span>
            </div>
            <div class="stream-container">
                <img src="/video_feed" alt="Live Camera Video Stream">
            </div>
            <div id="alert-banner" class="alert-box">
                <div class="alert-title">🚨 REMOTE RAILWAY INSPECTOR DISPATCH</div>
                <div id="alert-text" class="alert-body">High-priority crack detected. Rover holding stationary at coordinates.</div>
            </div>
        </div>

        <div>
            <div class="card">
                <div class="card-title">RAILWAY COORDINATE TELEMETRY</div>
                <div class="stat-row"><span class="stat-label">Metric Chainage:</span><span id="tele-chainage" class="stat-value highlight">CH 00+00.00m</span></div>
                <div class="stat-row"><span class="stat-label">Local Coordinates (X, Y):</span><span id="tele-coords" class="stat-value">X: +0.00m, Y: +0.00m</span></div>
                <div class="stat-row"><span class="stat-label">Track Designation:</span><span class="stat-value">LINE-1 (UP-MAIN)</span></div>
                <div class="stat-row"><span class="stat-label">Rover State:</span><span id="tele-state" class="stat-value">IDLE</span></div>
                <div class="stat-row"><span class="stat-label">Linear Velocity:</span><span id="tele-speed" class="stat-value">0.00 m/s</span></div>
                <div class="stat-row"><span class="stat-label">Motor System:</span><span id="tele-motor" class="stat-value">READY</span></div>
            </div>

            <div class="card" style="margin-top: 20px;">
                <div class="card-title">DEFECT RISK ASSESSMENT</div>
                <div class="stat-row"><span class="stat-label">Last Defect ID:</span><span id="insp-det" class="stat-value">NONE</span></div>
                <div class="stat-row"><span class="stat-label">Detection Confidence:</span><span id="insp-conf" class="stat-value">0.0%</span></div>
                <div class="stat-row"><span class="stat-label">Defect Length:</span><span id="insp-len" class="stat-value">0.0 mm</span></div>
                <div class="stat-row"><span class="stat-label">Max Width:</span><span id="insp-max-w" class="stat-value">0.00 mm</span></div>
                <div class="stat-row"><span class="stat-label">Apparent Depth:</span><span id="insp-depth" class="stat-value">0.00 mm</span></div>
                <div class="stat-row"><span class="stat-label">Risk Level:</span><span id="insp-severity" class="stat-value">CLEAR</span></div>
                <div class="stat-row"><span class="stat-label">Defect Location:</span><span id="insp-loc" class="stat-value highlight">---</span></div>
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
                    document.getElementById('tele-motor').innerText = data.motor_enabled ? 'ENABLED' : 'DISABLED';
                    document.getElementById('tele-chainage').innerText = data.chainage;
                    document.getElementById('chainage-indicator').innerText = data.chainage;
                    document.getElementById('tele-coords').innerText = 'X: ' + (data.location_x >= 0 ? '+' : '') + data.location_x.toFixed(2) + 'm, Y: +0.00m';
                    
                    const badge = document.getElementById('status-badge');
                    badge.innerText = 'STATE: ' + data.state;
                    badge.className = 'badge badge-' + data.state.toLowerCase();

                    const alertBanner = document.getElementById('alert-banner');
                    const alertText = document.getElementById('alert-text');

                    if (data.last_inspection) {
                        const insp = data.last_inspection;
                        document.getElementById('insp-det').innerText = insp.id;
                        document.getElementById('insp-conf').innerText = (insp.conf * 100).toFixed(1) + '%';
                        document.getElementById('insp-len').innerText = insp.len_mm.toFixed(1) + ' mm';
                        document.getElementById('insp-max-w').innerText = insp.max_w_mm.toFixed(2) + ' mm';
                        document.getElementById('insp-depth').innerText = insp.depth_mm.toFixed(2) + ' mm';
                        document.getElementById('insp-severity').innerText = insp.severity;
                        document.getElementById('insp-loc').innerText = insp.chainage ? insp.chainage : data.chainage;

                        if (insp.severity === 'CRITICAL' || insp.severity === 'HIGH') {
                            alertBanner.style.display = 'block';
                            alertText.innerHTML = '<strong>' + insp.severity + ' DEFECT AT ' + (insp.chainage || data.chainage) + '</strong><br>' +
                                'Dimensions: ' + insp.len_mm.toFixed(1) + 'mm L &times; ' + insp.max_w_mm.toFixed(1) + 'mm W. Coordinates transmitted to Remote Inspector. Auto-resuming patrol.';
                        }
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
    protocol_version = "HTTP/1.1"
    node_ref = None

    def do_OPTIONS(self) -> None:
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, HEAD")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def do_HEAD(self) -> None:
        self.do_GET()

    def do_GET(self) -> None:
        clean_path = self.path.split("?")[0]
        node = WebRequestHandler.node_ref

        if clean_path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(HTML_DASHBOARD.encode("utf-8"))

        elif clean_path == "/api/telemetry":
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()

            data = {
                "state": node.current_state if node else "IDLE",
                "linear_speed": node.linear_speed if node else 0.0,
                "angular_speed": node.angular_speed if node else 0.0,
                "motor_enabled": node.motor_enabled if node else False,
                "watchdog": node.watchdog_active if node else False,
                "location_x": node.location_x if node else 0.0,
                "location_y": node.location_y if node else 0.0,
                "chainage": node.chainage_station if node else "CH 00+00.00m",
                "last_inspection": node.last_inspection_data if node else None,
            }
            self.wfile.write(json.dumps(data).encode("utf-8"))

        elif clean_path in ("/api/frame.jpg", "/snapshot.jpg", "/frame.jpg"):
            if node and node.latest_jpeg is not None:
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Type", "image/jpeg")
                self.send_header("Content-Length", str(len(node.latest_jpeg)))
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.send_header("Pragma", "no-cache")
                self.send_header("Expires", "0")
                self.end_headers()
                self.wfile.write(node.latest_jpeg)
            else:
                self.send_response(503)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()

        elif clean_path == "/video_feed":
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
            self.send_header("Connection", "close")
            self.send_header(
                "Content-Type", "multipart/x-mixed-replace; boundary=frame"
            )
            self.end_headers()

            while node and rclpy.ok():
                if node.latest_jpeg is not None:
                    try:
                        part = (
                            b"--frame\r\n"
                            b"Content-Type: image/jpeg\r\n"
                            b"Content-Length: " + str(len(node.latest_jpeg)).encode("ascii") + b"\r\n\r\n"
                            + node.latest_jpeg + b"\r\n"
                        )
                        self.wfile.write(part)
                        time.sleep(0.033)
                    except (BrokenPipeError, ConnectionResetError, Exception):
                        break
                else:
                    time.sleep(0.05)

        else:
            self.send_response(404)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

    def do_POST(self) -> None:
        if self.path.startswith("/api/estop"):
            set_val = "set=true" in self.path
            node = WebRequestHandler.node_ref
            if node:
                node.send_estop(set_val)

            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            msg = "Emergency stop triggered" if set_val else "Emergency stop cleared"
            self.wfile.write(json.dumps({"success": True, "message": msg}).encode("utf-8"))

    def log_message(self, format, *args) -> None:
        """Suppress standard HTTP server access log spam."""
        pass


class RemoteMonitorNode(Node):
    """ROS 2 Remote Monitoring Web Node with Live Bounding Boxes & Coordinates."""

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
        self.location_x = 0.0
        self.location_y = 0.0
        self.chainage_station = "CH 00+00.00m"
        self.latest_jpeg = None
        self.last_inspection_data = None

        # ROS 2 Subscribers
        self.create_subscription(RoverState, "/rover_state", self._state_cb, 10)
        self.create_subscription(
            InspectionResult, "/inspection_result", self._result_cb, 10
        )
        # Subscribe to Visualization Image (contains crack bounding boxes & HUD overlay)
        self.create_subscription(
            Image, "/crack_detection/visualization", self._vis_image_cb, 10
        )
        self.create_subscription(
            Image, "/camera/processed_overlay", self._fallback_image_cb, 10
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
        self.location_x = float(msg.location_x)
        self.location_y = float(msg.location_y)
        if msg.chainage_station:
            self.chainage_station = msg.chainage_station

    def _result_cb(self, msg: InspectionResult) -> None:
        self.last_inspection_data = {
            "id": msg.inspection_id,
            "conf": float(msg.confidence),
            "len_mm": float(msg.crack_length_mm),
            "max_w_mm": float(msg.crack_max_width_mm),
            "avg_w_mm": float(msg.crack_avg_width_mm),
            "depth_mm": float(msg.apparent_depth_mm),
            "severity": msg.severity_rating,
            "chainage": msg.chainage_station if msg.chainage_station else self.chainage_station,
        }

    def _vis_image_cb(self, msg: Image) -> None:
        try:
            cv_img = self._bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
            _, jpeg = cv2.imencode(".jpg", cv_img, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            self.latest_jpeg = jpeg.tobytes()
        except Exception as e:
            self.get_logger().error(f"Image compression error: {e}")

    def _fallback_image_cb(self, msg: Image) -> None:
        if self.latest_jpeg is None:
            self._vis_image_cb(msg)

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
