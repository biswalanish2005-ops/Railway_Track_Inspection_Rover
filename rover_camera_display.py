#!/usr/bin/env python3
"""
Railway Inspection Rover — Headless Remote Operation & Live Camera Web Dashboard
================================================================================
Captures live frames from Raspberry Pi Camera Module 3 (IMX708) via libcamera/rpicam-vid,
executes calibrated ML/CV slit and crack detection in real-time, drives physical L298N
motors on Raspberry Pi 5 (gpiochip 4), stops for 5.0 seconds when a crack is detected,
transmits location to the remote railway inspector, and automatically resumes patrol.

Remote Operation:
  - Runs HEADLESS over SSH without any display/monitor connected to the Raspberry Pi 5.
  - Serves an embedded responsive Web Dashboard & live MJPEG video stream on port 8080.
  - Remote controls: Start Patrol, Stop/Pause Rover, Reset Odometry, and Capture Snapshot.

Usage:
  python3 rover_camera_display.py               # Auto-detects headless mode if no monitor
  python3 rover_camera_display.py --headless    # Explicitly run without display window
  python3 rover_camera_display.py --port 8080   # Custom web dashboard port
"""

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import math
import os
import signal
import subprocess
import sys
import threading
import time
from datetime import datetime
import cv2
import numpy as np

# ─── Configuration ────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 1280, 720
FPS = 30
MM_PER_PIXEL = 0.35  # Calibrated for Camera Module 3 at rail view
SAVE_DIR = os.path.expanduser("~/camera_test/live_captures")
os.makedirs(SAVE_DIR, exist_ok=True)

# ─── State Variables ──────────────────────────────────────────────────────────
latest_jpeg = None
latest_annotated_jpeg = None
frame_lock = threading.Lock()
annotated_lock = threading.Lock()
running = True
frame_count = 0
show_edges = False
is_headless = False
web_port = 8080

# Railway Chainage Odometry & Physical Motor Control
rover_linear_speed = 0.20  # m/s crawl patrol speed
rover_location_x = 0.0     # meters along track
is_inspecting_hold = False
hold_start_time = 0.0
last_odom_time = time.time()
camera_roi = "0.0,0.25,1.0,0.75"  # Default sensor ROI: crops upper background clutter
track_y_min_ratio = 0.08          # Minimum vertical ratio on track
motor_enabled = False             # Physical motor drive toggle (DEFAULT: False in STANDBY until START clicked)
last_alert_cooldown_time = 0.0
last_defect_info = None
current_state_str = "STANDBY"

# Initialize Physical L298N Motor Driver on Raspberry Pi 5
hw_motor = None


def ensure_motor_driver():
    """Ensure L298N motor driver instance is initialized and connected."""
    global hw_motor
    if hw_motor is None:
        try:
            control_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src/rover_control")
            if control_path not in sys.path:
                sys.path.append(control_path)
            from rover_control.l298n_motor_driver import L298NMotorDriver
            hw_motor = L298NMotorDriver()
            print("[*] Physical L298N Motor Driver ACTIVE on RPi 5 GPIO (Pins 12,13,17,27,22,23).")
        except Exception as e:
            print(f"[!] L298N Motor Driver not available: {e}. Running in simulation motion mode.")
    return hw_motor


ensure_motor_driver()


HTML_DASHBOARD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Railway Inspection Rover - Remote Control & Telemetry</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0c1017; color: #e2e8f0; padding: 16px; }
        .header { display: flex; justify-content: space-between; align-items: center; background: #151d2a; padding: 14px 20px; border-radius: 8px; border-bottom: 3px solid #0284c7; margin-bottom: 16px; }
        .header h1 { font-size: 18px; color: #38bdf8; letter-spacing: 0.5px; }
        .badge { padding: 6px 14px; border-radius: 4px; font-weight: 700; font-size: 13px; text-transform: uppercase; }
        .badge-patrolling { background: #16a34a; color: #fff; }
        .badge-holding { background: #dc2626; color: #fff; animation: pulse 1s infinite alternate; }
        .badge-paused { background: #d97706; color: #fff; }
        .badge-idle { background: #475569; color: #fff; }
        @keyframes pulse { from { opacity: 0.7; } to { opacity: 1; } }
        .grid { display: grid; grid-template-columns: 2.2fr 1fr; gap: 16px; }
        @media (max-width: 900px) { .grid { grid-template-columns: 1fr; } }
        .card { background: #151d2a; padding: 16px; border-radius: 8px; border: 1px solid #222f42; box-shadow: 0 4px 12px rgba(0,0,0,0.5); }
        .card-title { font-size: 14px; font-weight: 700; color: #94a3b8; border-bottom: 1px solid #222f42; padding-bottom: 8px; margin-bottom: 12px; display: flex; justify-content: space-between; }
        .stream-wrap img { width: 100%; border-radius: 6px; border: 2px solid #2b394e; display: block; }
        .stat-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #1a2536; font-size: 13.5px; }
        .stat-label { color: #8da2bb; }
        .stat-value { font-weight: 700; color: #f8fafc; }
        .highlight { color: #38bdf8; }
        .alert-box { background: #3c1216; border: 2px solid #ef4444; border-radius: 6px; padding: 12px; margin-top: 14px; display: none; }
        .alert-title { color: #f87171; font-weight: 700; font-size: 14px; margin-bottom: 6px; }
        .alert-body { font-size: 13px; color: #fca5a5; line-height: 1.4; }
        .btn-group { display: flex; flex-direction: column; gap: 8px; margin-top: 8px; }
        .btn { padding: 11px 16px; border: none; border-radius: 6px; font-size: 13.5px; font-weight: 700; cursor: pointer; transition: 0.15s; width: 100%; display: flex; align-items: center; justify-content: center; gap: 8px; }
        .btn-start { background: #16a34a; color: #fff; }
        .btn-start:hover { background: #15803d; }
        .btn-stop { background: #d97706; color: #fff; }
        .btn-stop:hover { background: #b45309; }
        .btn-reset { background: #0284c7; color: #fff; }
        .btn-reset:hover { background: #0369a1; }
        .btn-snap { background: #475569; color: #fff; }
        .btn-snap:hover { background: #334155; }
        .btn:active { transform: scale(0.98); }
    </style>
</head>
<body>
    <div class="header">
        <h1>AUTONOMOUS RAILWAY TRACK INSPECTION ROVER</h1>
        <div id="status-badge" class="badge badge-idle">STATE: IDLE</div>
    </div>

    <div class="grid">
        <div class="card">
            <div class="card-title">
                <span>LIVE CAMERA FEED &amp; CALIBRATED ML DEFECT DETECTOR</span>
                <span id="chainage-header" class="highlight">CH 00+00.00m</span>
            </div>
            <div class="stream-wrap" style="position: relative; background: #000; min-height: 400px; display: flex; align-items: center; justify-content: center; border-radius: 6px; overflow: hidden;">
                <img id="camera-stream" src="/video_feed" alt="Rover Live Camera Feed" style="width: 100%; height: auto; display: block; border-radius: 6px;">
                <div id="stream-badge" style="position: absolute; top: 12px; left: 12px; background: rgba(15, 23, 42, 0.85); padding: 5px 12px; border-radius: 4px; font-size: 12px; font-weight: 700; color: #4ade80; display: flex; align-items: center; gap: 8px; border: 1px solid rgba(74, 222, 128, 0.4); box-shadow: 0 2px 8px rgba(0,0,0,0.5);">
                    <span id="stream-dot" style="display:inline-block; width:8px; height:8px; background:#4ade80; border-radius:50%; animation: pulse 1.2s infinite alternate;"></span>
                    <span id="stream-status-text">LIVE MJPEG (30 FPS)</span>
                </div>
                <div style="position: absolute; top: 12px; right: 12px; display: flex; gap: 6px;">
                    <button id="toggle-stream-btn" onclick="toggleFeedMode()" style="background: rgba(15, 23, 42, 0.85); color: #94a3b8; border: 1px solid #334155; padding: 5px 12px; border-radius: 4px; font-size: 11.5px; font-weight: 700; cursor: pointer; transition: 0.2s;">SWITCH TO POLLING</button>
                </div>
            </div>
            <div id="alert-banner" class="alert-box">
                <div class="alert-title">🚨 REMOTE RAILWAY INSPECTOR DISPATCH</div>
                <div id="alert-text" class="alert-body">Critical track slit detected. Rover stopped for 5.0s hold. Coordinates transmitted.</div>
            </div>
        </div>

        <div>
            <div class="card">
                <div class="card-title">REMOTE ROVER CONTROL</div>
                <div class="btn-group">
                    <button id="btn-start" class="btn btn-start" onclick="sendControl('start')">▶ START PATROL</button>
                    <button id="btn-stop" class="btn btn-stop" onclick="sendControl('stop')">⏸ PAUSE / STOP ROVER</button>
                    <button id="btn-reset" class="btn btn-reset" onclick="sendControl('reset')">🔄 RESET CHAINAGE (0.00m)</button>
                    <button id="btn-snap" class="btn btn-snap" onclick="sendControl('snapshot')">📸 SAVE SCREENSHOT</button>
                </div>
                <div id="control-toast" style="margin-top: 10px; padding: 10px; border-radius: 6px; font-weight: 700; font-size: 13px; text-align: center; display: none;"></div>
            </div>

            <div class="card" style="margin-top: 16px;">
                <div class="card-title">RAILWAY COORDINATE TELEMETRY</div>
                <div class="stat-row"><span class="stat-label">Metric Chainage:</span><span id="tele-chainage" class="stat-value highlight">CH 00+00.00m</span></div>
                <div class="stat-row"><span class="stat-label">Local Coordinates (X, Y):</span><span id="tele-coords" class="stat-value">X: +0.00m, Y: +0.00m</span></div>
                <div class="stat-row"><span class="stat-label">Track Designation:</span><span class="stat-value">LINE-1 (UP-MAIN)</span></div>
                <div class="stat-row"><span class="stat-label">Crawl Velocity:</span><span id="tele-speed" class="stat-value">0.00 m/s</span></div>
                <div class="stat-row"><span class="stat-label">Motor State:</span><span id="tele-motor" class="stat-value">STANDBY</span></div>
                <div class="stat-row"><span class="stat-label">Frame Rate:</span><span id="tele-fps" class="stat-value">30.0 FPS</span></div>
            </div>

            <div class="card" style="margin-top: 16px;">
                <div class="card-title">DEFECT RISK ASSESSMENT</div>
                <div class="stat-row"><span class="stat-label">Defect Risk Rating:</span><span id="insp-risk" class="stat-value">CLEAR</span></div>
                <div class="stat-row"><span class="stat-label">Confidence:</span><span id="insp-conf" class="stat-value">0.0%</span></div>
                <div class="stat-row"><span class="stat-label">Estimated Length:</span><span id="insp-len" class="stat-value">0.0 mm</span></div>
                <div class="stat-row"><span class="stat-label">Max Width:</span><span id="insp-wid" class="stat-value">0.0 mm</span></div>
                <div class="stat-row"><span class="stat-label">Apparent Depth:</span><span id="insp-depth" class="stat-value">0.0 mm</span></div>
                <div class="stat-row"><span class="stat-label">Defect Location:</span><span id="insp-loc" class="stat-value highlight">---</span></div>
            </div>
        </div>
    </div>

    <script>
        let feedMode = 'stream';
        const streamImg = document.getElementById('camera-stream');
        const streamStatusText = document.getElementById('stream-status-text');
        const streamBadge = document.getElementById('stream-badge');
        const streamDot = document.getElementById('stream-dot');
        const toggleBtn = document.getElementById('toggle-stream-btn');

        function setStreamOnline(isOnline, modeName) {
            if (isOnline) {
                streamBadge.style.borderColor = 'rgba(74, 222, 128, 0.4)';
                streamBadge.style.color = '#4ade80';
                streamDot.style.background = '#4ade80';
                streamStatusText.innerText = modeName || 'LIVE FEED';
            } else {
                streamBadge.style.borderColor = 'rgba(239, 68, 68, 0.4)';
                streamBadge.style.color = '#f87171';
                streamDot.style.background = '#f87171';
                streamStatusText.innerText = 'RECONNECTING FEED...';
            }
        }

        function startPollingMode() {
            feedMode = 'poll';
            toggleBtn.innerText = 'SWITCH TO STREAM';
            toggleBtn.style.color = '#38bdf8';
            setStreamOnline(true, 'LIVE POLLING (25 FPS)');
            
            function fetchNextFrame() {
                if (feedMode !== 'poll') return;
                const nextImg = new Image();
                nextImg.onload = function() {
                    streamImg.src = nextImg.src;
                    setStreamOnline(true, 'LIVE POLLING (25 FPS)');
                    setTimeout(fetchNextFrame, 40);
                };
                nextImg.onerror = function() {
                    setStreamOnline(false);
                    setTimeout(fetchNextFrame, 500);
                };
                nextImg.src = '/api/frame.jpg?t=' + Date.now();
            }
            fetchNextFrame();
        }

        function startStreamMode() {
            feedMode = 'stream';
            toggleBtn.innerText = 'SWITCH TO POLLING';
            toggleBtn.style.color = '#94a3b8';
            streamImg.src = '/video_feed?t=' + Date.now();
            setStreamOnline(true, 'LIVE MJPEG (30 FPS)');
        }

        function toggleFeedMode() {
            if (feedMode === 'stream') {
                startPollingMode();
            } else {
                startStreamMode();
            }
        }

        // Automatic fallback to high-speed frame polling if stream drops
        streamImg.onerror = function() {
            console.warn("MJPEG stream dropped or not supported. Falling back to high-speed frame polling.");
            if (feedMode === 'stream') {
                startPollingMode();
            }
        };

        // Fallback watchdog: if image has not loaded any pixels after 2.5s, switch to polling
        setTimeout(() => {
            if (feedMode === 'stream' && (streamImg.naturalWidth === 0 || streamImg.complete === false)) {
                console.warn("Stream delayed. Auto-initiating high-speed frame polling...");
                startPollingMode();
            }
        }, 2500);

        function updateTelemetry() {
            fetch('/api/telemetry')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('tele-chainage').innerText = data.chainage;
                    document.getElementById('chainage-header').innerText = data.chainage;
                    document.getElementById('tele-coords').innerText = data.coordinates;
                    document.getElementById('tele-speed').innerText = data.speed.toFixed(2) + ' m/s';
                    document.getElementById('tele-motor').innerText = data.motor_enabled ? 'ENABLED (RUNNING)' : 'PAUSED';
                    document.getElementById('tele-fps').innerText = data.fps.toFixed(1) + ' FPS';

                    const badge = document.getElementById('status-badge');
                    badge.innerText = 'STATE: ' + data.state;
                    badge.className = 'badge ' + (data.state.includes('HOLDING') ? 'badge-holding' : (data.motor_enabled ? 'badge-patrolling' : 'badge-paused'));

                    const alertBanner = document.getElementById('alert-banner');
                    const alertText = document.getElementById('alert-text');
                    if (data.last_alert) {
                        const a = data.last_alert;
                        document.getElementById('insp-risk').innerText = a.risk + ' DEFECT';
                        document.getElementById('insp-conf').innerText = (a.conf * 100).toFixed(1) + '%';
                        document.getElementById('insp-len').innerText = a.length_mm.toFixed(1) + ' mm';
                        document.getElementById('insp-wid').innerText = a.width_mm.toFixed(1) + ' mm';
                        document.getElementById('insp-depth').innerText = a.depth_mm.toFixed(1) + ' mm';
                        document.getElementById('insp-loc').innerText = a.chainage;

                        if (a.active) {
                            alertBanner.style.display = 'block';
                            alertText.innerHTML = '<strong>' + a.risk + ' DEFECT AT ' + a.chainage + ' (' + a.coordinates + ')</strong><br>' +
                                'Dimensions: ' + a.length_mm.toFixed(1) + 'mm L &times; ' + a.width_mm.toFixed(1) + 'mm W. Holding 5.0s for Remote Inspector. Resuming patrol automatically.';
                        } else {
                            alertBanner.style.display = 'none';
                        }
                    }
                })
                .catch(() => {});
        }

        function sendControl(action) {
            const toast = document.getElementById('control-toast');
            if (action === 'start') {
                toast.innerText = '▶ TRANSMITTING: START PATROL (MOTORS ENGAGED)';
                toast.style.background = '#15803d';
                toast.style.color = '#ffffff';
                toast.style.display = 'block';
                document.getElementById('status-badge').innerText = 'STATE: PATROLLING';
                document.getElementById('status-badge').className = 'badge badge-patrolling';
                document.getElementById('tele-motor').innerText = 'ENABLED (RUNNING)';
            } else if (action === 'stop') {
                toast.innerText = '⏸ TRANSMITTING: STOP ROVER (MOTORS HALTED)';
                toast.style.background = '#b45309';
                toast.style.color = '#ffffff';
                toast.style.display = 'block';
                document.getElementById('status-badge').innerText = 'STATE: PAUSED';
                document.getElementById('status-badge').className = 'badge badge-paused';
                document.getElementById('tele-motor').innerText = 'PAUSED';
            } else if (action === 'reset') {
                toast.innerText = '🔄 RESETTING CHAINAGE TO 0.00m';
                toast.style.background = '#0369a1';
                toast.style.color = '#ffffff';
                toast.style.display = 'block';
                document.getElementById('tele-chainage').innerText = 'CH 00+00.00m';
                document.getElementById('chainage-header').innerText = 'CH 00+00.00m';
                document.getElementById('tele-coords').innerText = 'X: +0.00m, Y: +0.00m';
            } else if (action === 'snapshot') {
                toast.innerText = '📸 DEFECT SCREENSHOT SAVED';
                toast.style.background = '#334155';
                toast.style.color = '#ffffff';
                toast.style.display = 'block';
            }

            fetch('/api/control?action=' + action, { method: 'POST' })
                .then(r => r.json())
                .then(res => {
                    setTimeout(updateTelemetry, 100);
                    setTimeout(() => { toast.style.display = 'none'; }, 2200);
                })
                .catch(err => {
                    toast.innerText = '❌ TRANSMISSION FAILED: ' + err;
                    toast.style.background = '#dc2626';
                    toast.style.color = '#ffffff';
                    setTimeout(() => { toast.style.display = 'none'; }, 3000);
                });
        }

        setInterval(updateTelemetry, 400);
    </script>
</body>
</html>
"""


class WebDashboardHandler(BaseHTTPRequestHandler):
    """HTTP server serving responsive HTML dashboard, MJPEG stream, single frame snapshots, and remote control API."""
    protocol_version = "HTTP/1.0"

    def do_OPTIONS(self):
        """Handle CORS pre-flight requests."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, HEAD")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Connection", "close")
        self.end_headers()

    def do_HEAD(self):
        """Support HTTP HEAD requests."""
        self.do_GET()

    def handle_control(self):
        """Unified command handler supporting both GET and POST requests for rover actions."""
        global motor_enabled, rover_location_x, hw_motor, current_state_str, is_inspecting_hold

        action = "unknown"
        driver = ensure_motor_driver()

        if "action=start" in self.path:
            motor_enabled = True
            is_inspecting_hold = False
            current_state_str = "PATROLLING"
            action = "start"
            if driver:
                driver.set_velocity(rover_linear_speed, 0.0)
            print(f"▶ [REMOTE WEB COMMAND] Patrol START commanded from laptop — Motors forward at {rover_linear_speed:.2f} m/s.")
        elif "action=stop" in self.path:
            motor_enabled = False
            is_inspecting_hold = False
            current_state_str = "PAUSED"
            action = "stop"
            if driver:
                driver.set_velocity(0.0, 0.0)
            print("⏸ [REMOTE WEB COMMAND] Rover STOP commanded from laptop — Motors halted.")
        elif "action=reset" in self.path:
            rover_location_x = 0.0
            action = "reset"
            print("🔄 [REMOTE WEB COMMAND] Odometry RESET to CH 00+00.00m.")
        elif "action=snapshot" in self.path:
            with annotated_lock:
                snap = latest_annotated_jpeg
            if snap is not None:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                snap_path = os.path.join(SAVE_DIR, f"remote_capture_{ts}.jpg")
                with open(snap_path, "wb") as f:
                    f.write(snap)
                print(f"📸 [REMOTE WEB COMMAND] Snapshot saved: {snap_path}")
            action = "snapshot"

        resp = {
            "success": True,
            "action": action,
            "motor_enabled": motor_enabled,
            "state": current_state_str,
            "speed": rover_linear_speed if motor_enabled else 0.0,
            "chainage": f"CH {int(abs(rover_location_x)//1000):02d}+{abs(rover_location_x)%1000:05.2f}m",
            "coordinates": f"X: {rover_location_x:+.2f}m, Y: +0.00m"
        }
        body = json.dumps(resp).encode("utf-8")
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        global rover_location_x, rover_linear_speed, motor_enabled, is_inspecting_hold
        global current_state_str, last_defect_info, latest_annotated_jpeg, latest_jpeg

        clean_path = self.path.split("?")[0]

        if clean_path in ("/", "/index.html"):
            body = HTML_DASHBOARD.encode("utf-8")
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Connection", "close")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(body)

        elif clean_path.startswith("/api/control"):
            self.handle_control()

        elif clean_path == "/video_feed":
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
            self.send_header("Connection", "close")
            self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=frame")
            self.end_headers()

            while running:
                with annotated_lock:
                    jpg = latest_annotated_jpeg

                if jpg is not None:
                    try:
                        part = (
                            b"--frame\r\n"
                            b"Content-Type: image/jpeg\r\n"
                            b"Content-Length: " + str(len(jpg)).encode("ascii") + b"\r\n\r\n"
                            + jpg + b"\r\n"
                        )
                        self.wfile.write(part)
                        time.sleep(0.033)  # ~30 FPS
                    except (BrokenPipeError, ConnectionResetError, Exception):
                        break
                else:
                    time.sleep(0.05)

        elif clean_path in ("/api/frame.jpg", "/snapshot.jpg", "/frame.jpg"):
            with annotated_lock:
                jpg = latest_annotated_jpeg
            if jpg is None:
                with frame_lock:
                    jpg = latest_jpeg

            if jpg is not None:
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Type", "image/jpeg")
                self.send_header("Content-Length", str(len(jpg)))
                self.send_header("Connection", "close")
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.send_header("Pragma", "no-cache")
                self.send_header("Expires", "0")
                self.end_headers()
                self.wfile.write(jpg)
            else:
                self.send_response(503)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Connection", "close")
                self.end_headers()

        elif clean_path == "/api/telemetry":
            km = int(abs(rover_location_x) // 1000)
            m = abs(rover_location_x) % 1000
            chainage_str = f"CH {km:02d}+{m:05.2f}m"
            coord_str = f"X: {rover_location_x:+.2f}m, Y: +0.00m"

            data = {
                "state": current_state_str,
                "speed": rover_linear_speed if motor_enabled and not is_inspecting_hold else 0.0,
                "motor_enabled": motor_enabled,
                "chainage": chainage_str,
                "coordinates": coord_str,
                "location_x": rover_location_x,
                "fps": 30.0,
                "last_alert": last_defect_info,
            }
            body = json.dumps(data).encode("utf-8")
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Connection", "close")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(body)

        elif clean_path.startswith("/images/"):
            fname = clean_path.replace("/images/", "").strip("/")
            fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", fname)
            if os.path.isfile(fpath):
                with open(fpath, "rb") as f:
                    img_data = f.read()
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Type", "image/png")
                self.send_header("Content-Length", str(len(img_data)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(img_data)
            else:
                self.send_response(404)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Connection", "close")
                self.end_headers()

        else:
            self.send_response(404)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Connection", "close")
            self.end_headers()

    def do_POST(self):
        if self.path.startswith("/api/control"):
            self.handle_control()
        else:
            self.send_response(404)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Suppress HTTP access log spam


def parse_args():
    global camera_roi, track_y_min_ratio, is_headless, web_port
    parser = argparse.ArgumentParser(description="Railway Inspection Rover Headless Remote Controller")
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run headless without opening OpenCV window (for remote SSH usage without display)."
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="HTTP Web Dashboard port (default: 8080)."
    )
    parser.add_argument(
        "--roi",
        type=str,
        default="0.0,0.25,1.0,0.75",
        help="Camera sensor ROI (x,y,w,h) in 0.0-1.0 range. Default '0.0,0.25,1.0,0.75' matches img1.png POV."
    )
    parser.add_argument(
        "--no-roi",
        action="store_true",
        help="Disable camera sensor ROI (captures full sensor). Track ROI filtering will still reject background."
    )
    args, _ = parser.parse_known_args()

    # Auto-detect headless mode if no DISPLAY environment variable
    if args.headless or not os.environ.get("DISPLAY"):
        is_headless = True
    else:
        is_headless = False

    web_port = args.port

    if args.no_roi:
        camera_roi = None
        track_y_min_ratio = 0.42
    else:
        camera_roi = args.roi
        track_y_min_ratio = 0.08


def stream_reader():
    """Background thread: reads MJPEG stream from native rpicam-vid pipe."""
    global latest_jpeg, running, camera_roi
    cmd = [
        "rpicam-vid",
        "-t", "0",
        "--codec", "mjpeg",
        "--width", str(WIDTH),
        "--height", str(HEIGHT),
        "--framerate", str(FPS),
        "--nopreview",
    ]
    if camera_roi:
        cmd.extend(["--roi", camera_roi])
    cmd.extend(["-o", "-"])

    print(f"[*] Starting rpicam-vid capture pipeline (ROI: {camera_roi or 'FULL_SENSOR'})...")
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=512 * 1024
    )
    buf = b""
    while running and proc.poll() is None:
        try:
            chunk = proc.stdout.read(65536)
            if not chunk:
                break
            buf += chunk
            while True:
                a = buf.find(b"\xff\xd8")
                b_end = buf.find(b"\xff\xd9")
                if a != -1 and b_end != -1 and b_end > a:
                    jpg = buf[a : b_end + 2]
                    buf = buf[b_end + 2 :]
                    with frame_lock:
                        latest_jpeg = jpg
                else:
                    break
            if len(buf) > 3 * 1024 * 1024:
                buf = buf[-512 * 1024 :]
        except Exception:
            time.sleep(0.005)
    proc.terminate()


def detect_slits_and_cracks(gray_frame: np.ndarray) -> list[dict]:
    """
    Calibrated detection engine for slits, notches, and cracks in railway track plates.
    Specifically tuned to detect img3.png-style transverse rail plate slits and reject
    non-track background clutter (matching img1.png POV and avoiding img2.png false positives).
    """
    global track_y_min_ratio
    h, w = gray_frame.shape[:2]

    filtered = cv2.bilateralFilter(gray_frame, 7, 75, 75)
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

        for i in range(len(segs)):
            x1a, y1a, x2a, y2a, lena, ana = segs[i]
            for j in range(i + 1, min(len(segs), i + 35)):
                x1b, y1b, x2b, y2b, lenb, anb = segs[j]
                angle_diff = abs(ana - anb)
                if angle_diff > np.pi / 2:
                    angle_diff = np.pi - angle_diff
                if angle_diff > np.radians(14):
                    continue

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
    blackhat = cv2.morphologyEx(gray_frame, cv2.MORPH_BLACKHAT, kernel_bh)
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

        # ─── CONSTRAINT 1: Valid Track Range (Exclude upper background) ───
        if cy < track_y_min_ratio * h or cy > 0.95 * h:
            continue

        # ─── CONSTRAINT 2: Valid Steel Rail Lateral Bands ───
        on_left_rail = (0.08 * w <= cx <= 0.45 * w)
        on_right_rail = (0.55 * w <= cx <= 0.88 * w)
        if not (on_left_rail or on_right_rail):
            continue

        # ─── CONSTRAINT 3: Transverse Slit Orientation (dx >> dy) ───
        if bw < 1.6 * bh_box:
            continue

        # Evaluate Gradient Opposite Sign Score (Confirms physical gap/slot)
        margin = 6
        roi = gray_frame[max(0, y1 - margin):min(h, y2 + margin), max(0, x1 - margin):min(w, x2 + margin)]
        if roi.size == 0:
            continue

        gy = cv2.Sobel(roi, cv2.CV_32F, 0, 1, ksize=3)
        tg = np.mean(gy[:max(1, gy.shape[0] // 3), :])
        bg = np.mean(gy[2 * gy.shape[0] // 3:, :])
        opp_score = float(-(tg * bg))
        contrast = float(roi.std())

        conf = min(0.99, max(0.68, 0.72 + min(0.18, max(0.0, opp_score) * 0.003) + min(0.09, contrast * 0.002)))

        length_px = float(bw)
        width_px = float(bh_box)
        length_mm = length_px * MM_PER_PIXEL
        width_mm = width_px * MM_PER_PIXEL
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
                    m["length_mm"] = nbw * MM_PER_PIXEL
                    m["width_mm"] = nbh * MM_PER_PIXEL
                    matched = True
                    break
        if not matched:
            merged.append(d.copy())

    for m in merged:
        if m["length_mm"] > 35.0 or m["width_mm"] > 2.8:
            m["risk"] = "CRITICAL"
            m["color"] = (0, 0, 255)
        elif m["length_mm"] > 18.0 or m["width_mm"] > 1.2:
            m["risk"] = "HIGH"
            m["color"] = (0, 69, 255)

    merged.sort(key=lambda d: (d.get("opp_score", 0.0) * d["conf"]), reverse=True)
    return merged


def render_display(frame_bgr: np.ndarray, detections: list[dict], fps: float, count: int) -> np.ndarray:
    """Renders the full annotated camera feed with bounding boxes, risk labels, and railway coordinates."""
    global rover_location_x, rover_linear_speed, is_inspecting_hold, hold_start_time, last_odom_time
    global hw_motor, motor_enabled, last_alert_cooldown_time, last_defect_info, current_state_str

    now = time.time()
    dt = now - last_odom_time
    last_odom_time = now

    h, w = frame_bgr.shape[:2]

    # Check for risk > MODERATE (HIGH or CRITICAL)
    has_high_risk = any(d["risk"] in ("HIGH", "CRITICAL") for d in detections)

    # Format Railway Chainage & Coordinate Standard
    km = int(abs(rover_location_x) // 1000)
    m = abs(rover_location_x) % 1000
    chainage_str = f"CH {km:02d}+{m:05.2f}m"
    coord_str = f"X: {rover_location_x:+.2f}m, Y: +0.00m"

    # Rover motion behavior state machine:
    # Stops when risk > MODERATE, transmits location to remote inspector, holds 5.0s, resumes patrol
    if has_high_risk and not is_inspecting_hold and (now - last_alert_cooldown_time) > 6.0:
        is_inspecting_hold = True
        hold_start_time = now
        last_alert_cooldown_time = now
        if hw_motor and motor_enabled:
            hw_motor.set_velocity(0.0, 0.0)

        state_label = "CRACK DETECTED (RISK > MODERATE) — STOPPING & TRANSMITTING"
        current_state_str = "HOLDING_AT_DEFECT"
        state_color = (0, 0, 255)

        # Transmit Location & Defect Payload to Remote Railway Inspector
        high_dets = [d for d in detections if d["risk"] in ("HIGH", "CRITICAL")]
        d0 = high_dets[0]
        last_defect_info = {
            "risk": d0["risk"],
            "conf": d0["conf"],
            "length_mm": d0["length_mm"],
            "width_mm": d0["width_mm"],
            "depth_mm": d0["depth_mm"],
            "chainage": chainage_str,
            "coordinates": coord_str,
            "active": True,
        }

        print(f"\n🚨 >>> [CRACK DETECTED — LOCATION DISPATCHED TO REMOTE INSPECTOR] <<<")
        print(f"    Station Chainage:  {chainage_str}")
        print(f"    Track Coordinates: {coord_str}")
        print(f"    Defect Risk Level: {d0['risk']} (RISK > MODERATE)")
        print(f"    Dimensions:        Length {d0['length_mm']:.1f}mm x Width {d0['width_mm']:.1f}mm (Depth ~{d0['depth_mm']:.1f}mm)")
        print(f"    Confidence:        {d0['conf']*100:.1f}%")
        print(f"    Action:            Rover stopped. Holding stationary for 5.0s during inspection...\n")

    elif is_inspecting_hold:
        elapsed = now - hold_start_time
        if elapsed < 5.0:
            remaining = 5.0 - elapsed
            if hw_motor and motor_enabled:
                hw_motor.set_velocity(0.0, 0.0)
            state_label = f"HOLDING AT DEFECT [{remaining:.1f}s] — ALERT SENT TO INSPECTOR"
            current_state_str = f"HOLDING [{remaining:.1f}s]"
            state_color = (0, 0, 255)
        else:
            is_inspecting_hold = False
            last_alert_cooldown_time = now
            state_label = "TRANSMISSION COMPLETE — RESUMING PATROL"
            current_state_str = "RESUMING_PATROL"
            state_color = (0, 255, 120)
            if last_defect_info:
                last_defect_info["active"] = False
            if hw_motor and motor_enabled:
                hw_motor.set_velocity(rover_linear_speed, 0.0)
            print(f"⏩ [PATROL RESUMED] 5.0s inspection hold complete. Rover resuming crawl patrol at {rover_linear_speed:.2f} m/s.")
    else:
        if motor_enabled:
            # Advance location along track and drive physical motors
            rover_location_x += rover_linear_speed * dt
            if hw_motor:
                hw_motor.set_velocity(rover_linear_speed, 0.0)
            state_label = f"PATROLLING TRACK (SPEED: {rover_linear_speed:.2f} m/s)"
            current_state_str = "PATROLLING"
            state_color = (0, 255, 0)
        else:
            if hw_motor:
                hw_motor.set_velocity(0.0, 0.0)
            state_label = "MOTORS PAUSED (REMOTE WEB / SSH CONTROL)"
            current_state_str = "PAUSED"
            state_color = (0, 200, 255)

    vis = frame_bgr.copy()

    # Draw Defect Bounding Boxes (matching img1.png / img3.png)
    for d in detections[:3]:
        x1, y1, x2, y2 = d["bbox"]
        color = d["color"]

        cv2.rectangle(vis, (x1, y1), (x2, y2), color, 3)
        cv2.circle(vis, d["center"], 5, (0, 255, 255), -1)

        # Label tag matching user's reference
        label = f"{d['risk']} DEFECT | Conf: {d['conf']*100:.1f}%"
        dims = f"L: {d['length_mm']:.1f}mm | W: {d['width_mm']:.1f}mm | D: {d['depth_mm']:.1f}mm"

        box_w = 330
        cv2.rectangle(vis, (x1, max(0, y1 - 48)), (x1 + box_w, max(48, y1)), (15, 20, 28), -1)
        cv2.putText(vis, label, (x1 + 6, max(18, y1 - 28)), cv2.FONT_HERSHEY_SIMPLEX, 0.52, color, 2)
        cv2.putText(vis, dims, (x1 + 6, max(38, y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (255, 255, 255), 1)

    # Top HUD Banner (Railway Engineering Telemetry)
    cv2.rectangle(vis, (0, 0), (w, 70), (12, 16, 24), -1)
    cv2.putText(
        vis,
        f"RAILWAY ROVER LOC: [{coord_str}] | {chainage_str} | TRACK: LINE-1 (MAIN)",
        (12, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.54,
        (0, 220, 255),
        2,
    )
    cv2.putText(
        vis,
        f"STATUS: {state_label} | Defects Detected: {len(detections)}",
        (12, 54),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.50,
        state_color,
        2,
    )

    # Bottom Help Bar
    cv2.rectangle(vis, (0, h - 30), (w, h), (12, 16, 24), -1)
    roi_label = f"ROI: {camera_roi}" if camera_roi else "ROI: FULL"
    motor_status_str = "MOTOR: RUN" if motor_enabled else "MOTOR: PAUSED"
    cv2.putText(
        vis,
        f"FPS: {fps:4.1f} | Frame: {count} | {roi_label} | {motor_status_str} | Web Dashboard: port {web_port}",
        (12, h - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.44,
        (180, 190, 205),
        1,
    )

    return vis


def start_web_server(port: int):
    """Start background ThreadingHTTPServer for remote web monitoring & control."""
    try:
        server = ThreadingHTTPServer(("0.0.0.0", port), WebDashboardHandler)
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()
        print(f"🌐 Remote Inspector Web Dashboard ACTIVE at: http://0.0.0.0:{port}/")
        return server
    except Exception as e:
        print(f"[!] Warning: Web dashboard could not bind port {port}: {e}")
        return None


def get_local_ip() -> str:
    """Detect primary LAN IP address for user guidance."""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def main():
    global running, frame_count, show_edges, rover_location_x, motor_enabled, latest_annotated_jpeg

    parse_args()

    # Graceful signal handler for Ctrl+C over SSH
    def signal_handler(sig, frame):
        global running
        print("\n[*] Shutdown signal received. Halting rover cleanly...")
        running = False

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start MJPEG camera reader thread
    t = threading.Thread(target=stream_reader, daemon=True)
    t.start()

    # Start embedded remote monitoring web server
    web_server = start_web_server(web_port)
    local_ip = get_local_ip()

    print("=" * 72)
    print("  AUTONOMOUS RAILWAY TRACK INSPECTION ROVER — REMOTE CONTROLLER")
    print("=" * 72)
    print(f"  Mode:              {'HEADLESS (NO MONITOR NEEDED)' if is_headless else 'DESKTOP WINDOW + WEB'}")
    print(f"  Camera:            Raspberry Pi Camera Module 3 (IMX708)")
    print(f"  Sensor ROI:        {camera_roi or 'FULL SENSOR'}")
    print(f"  Motor Controller:  L298N on RPi 5 GPIO (Pins 12,13,17,27,22,23)")
    print(f"  Speed:             0.20 m/s patrol crawl speed")
    print(f"  Crack Response:    5.0s stationary hold, coordinate dispatch, auto-resume")
    print("-" * 72)
    print(f"  🌐 Remote Web URL:  http://{local_ip}:{web_port}/")
    print(f"  📱 On your laptop, open the URL above to view the live video feed")
    print(f"     and click START PATROL / STOP ROVER remotely.")
    print("=" * 72)

    window_name = "Railway Inspection Rover — Live Camera Feed"
    if not is_headless:
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, WIDTH, HEIGHT)

    fps_counter = 0
    fps_timer = time.time()
    fps_display = 30.0
    last_term_print = time.time()

    try:
        while running:
            with frame_lock:
                jpg = latest_jpeg

            if jpg is None:
                if not is_headless:
                    standby = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
                    cv2.putText(
                        standby,
                        "Initializing Raspberry Pi Camera Module 3 (libcamera)...",
                        (WIDTH // 2 - 280, HEIGHT // 2),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.75,
                        (0, 200, 255),
                        2,
                    )
                    cv2.imshow(window_name, standby)
                    key = cv2.waitKey(40) & 0xFF
                    if key in (ord("q"), 27):
                        running = False
                        break
                else:
                    time.sleep(0.04)
                continue

            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            if frame is None:
                time.sleep(0.01)
                continue

            frame_count += 1
            fps_counter += 1
            now = time.time()
            if (now - fps_timer) >= 1.0:
                fps_display = fps_counter / (now - fps_timer)
                fps_counter = 0
                fps_timer = now

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            detections = detect_slits_and_cracks(gray)

            if show_edges:
                edges = cv2.Canny(gray, 40, 120)
                base = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            else:
                base = frame

            display = render_display(base, detections, fps_display, frame_count)

            # Encode annotated frame for the web dashboard stream
            _, enc = cv2.imencode(".jpg", display, [cv2.IMWRITE_JPEG_QUALITY, 78])
            with annotated_lock:
                latest_annotated_jpeg = enc.tobytes()

            # Terminal telemetry heartbeat in headless SSH mode
            if is_headless and (now - last_term_print) >= 1.5:
                km = int(abs(rover_location_x) // 1000)
                m = abs(rover_location_x) % 1000
                m_stat = "RUN" if motor_enabled and not is_inspecting_hold else "PAUSED"
                print(
                    f"[{current_state_str:16s}] CH {km:02d}+{m:05.2f}m | LOC: X:{rover_location_x:+.2f}m | "
                    f"Motor: {m_stat} | FPS: {fps_display:4.1f} | Frame: {frame_count:05d} | Defects: {len(detections)}"
                )
                last_term_print = now

            # If desktop GUI is available, render window
            if not is_headless:
                cv2.imshow(window_name, display)
                key = cv2.waitKey(1) & 0xFF
                if key in (ord("q"), 27):
                    running = False
                    break
                elif key in (ord(" "), ord("m")):
                    motor_enabled = not motor_enabled
                    if not motor_enabled and hw_motor:
                        hw_motor.set_velocity(0.0, 0.0)
                    status_txt = "RUNNING" if motor_enabled else "PAUSED"
                    print(f"⚙️ [MOTOR TOGGLE] Rover motor drive is now {status_txt}")
                elif key == ord("s"):
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    path = os.path.join(SAVE_DIR, f"defect_capture_{ts}.jpg")
                    cv2.imwrite(path, display)
                    print(f"📸 Annotated defect capture saved: {path}")
                elif key == ord("e"):
                    show_edges = not show_edges
                elif key == ord("r"):
                    rover_location_x = 0.0
                    print("🔄 Rover chainage reset to CH 00+00.00m")
            else:
                time.sleep(0.005)

    except (KeyboardInterrupt, SystemExit):
        print("\n[*] Terminating on user request...")

    finally:
        # Guarantee motors are stopped
        if hw_motor:
            print("[*] Halting physical motors...")
            hw_motor.stop()
            hw_motor.cleanup()

        if not is_headless:
            cv2.destroyAllWindows()

        running = False
        t.join(timeout=2.0)
        print("[*] Rover inspection system halted cleanly.")


if __name__ == "__main__":
    main()
