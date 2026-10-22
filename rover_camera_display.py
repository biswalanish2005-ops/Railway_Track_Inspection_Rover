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
rover_linear_speed = 0.08  # m/s crawl patrol speed (increased by ~35% from 0.06 m/s)
rover_location_x = 0.0     # meters along track
is_inspecting_hold = False
hold_start_time = 0.0
last_odom_time = time.time()
camera_roi = "0.0,0.25,1.0,0.75"  # Default sensor ROI: crops upper background clutter
track_y_min_ratio = 0.08          # Minimum vertical ratio on track
motor_enabled = False             # Physical motor drive toggle (DEFAULT: False in STANDBY until START clicked)
last_alert_cooldown_time = 0.0
last_inspected_x = -999.0         # Metric position (m) where the last defect was stopped and inspected
resume_patrol_time = 0.0          # Timestamp when rover resumed moving after inspection hold
MIN_CLEARING_DISTANCE = 0.70      # Forward travel distance (m) required to clear inspected defect
MIN_CLEARING_TIME = 10.0          # Active travel seconds required to clear inspected defect from FOV
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
            if control_path in sys.path:
                sys.path.remove(control_path)
            sys.path.insert(0, control_path)
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
                <div style="margin-top: 12px; padding-top: 10px; border-top: 1px solid #222f42;">
                    <div style="font-size: 11.5px; font-weight: 700; color: #94a3b8; margin-bottom: 6px; display: flex; justify-content: space-between;">
                        <span>PATROL SPEED PRESETS:</span>
                        <span id="current-speed-label" style="color: #38bdf8;">0.08 m/s (PATROL)</span>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px;">
                        <button onclick="setPatrolSpeed(0.06)" class="btn btn-snap" style="padding: 6px 4px; font-size: 11.5px;">🐢 0.06 m/s</button>
                        <button onclick="setPatrolSpeed(0.08)" class="btn btn-snap" style="padding: 6px 4px; font-size: 11.5px; border: 1px solid #38bdf8; color: #38bdf8;">🎯 0.08 m/s</button>
                        <button onclick="setPatrolSpeed(0.12)" class="btn btn-snap" style="padding: 6px 4px; font-size: 11.5px;">🐇 0.12 m/s</button>
                    </div>
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

        function setPatrolSpeed(val) {
            const toast = document.getElementById('control-toast');
            toast.innerText = '⚡ TRANSMITTING: SPEED -> ' + val.toFixed(2) + ' m/s';
            toast.style.background = '#0284c7';
            toast.style.color = '#ffffff';
            toast.style.display = 'block';

            fetch('/api/control?action=setspeed&val=' + val, { method: 'POST' })
                .then(r => r.json())
                .then(res => {
                    const label = document.getElementById('current-speed-label');
                    if (label) label.innerText = val.toFixed(2) + ' m/s';
                    setTimeout(updateTelemetry, 100);
                    setTimeout(() => { toast.style.display = 'none'; }, 2000);
                })
                .catch(err => {
                    toast.innerText = '❌ SPEED UPDATE FAILED: ' + err;
                    toast.style.background = '#dc2626';
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
        global motor_enabled, rover_location_x, hw_motor, current_state_str, is_inspecting_hold, rover_linear_speed
        global last_inspected_x, resume_patrol_time

        action = "unknown"
        driver = ensure_motor_driver()

        if "action=setspeed" in self.path:
            try:
                import urllib.parse
                qs = urllib.parse.urlparse(self.path).query
                params = urllib.parse.parse_qs(qs)
                if "val" in params:
                    rover_linear_speed = float(params["val"][0])
                elif "speed" in params:
                    rover_linear_speed = float(params["speed"][0])
                action = f"setspeed_{rover_linear_speed:.2f}"
                if driver and motor_enabled:
                    driver.set_velocity(rover_linear_speed, 0.0)
                print(f"⚡ [REMOTE WEB COMMAND] Rover patrol speed updated to {rover_linear_speed:.2f} m/s.")
            except Exception as e:
                print(f"[!] Error updating speed: {e}")
        elif "action=start" in self.path:
            motor_enabled = True
            is_inspecting_hold = False
            resume_patrol_time = time.time()
            last_inspected_x = rover_location_x
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
            last_inspected_x = -999.0
            resume_patrol_time = 0.0
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
    global camera_roi, track_y_min_ratio, is_headless, web_port, rover_linear_speed
    parser = argparse.ArgumentParser(description="Railway Inspection Rover Headless Remote Controller")
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run headless without opening OpenCV window (for remote SSH usage without display)."
    )
    parser.add_argument(
        "--speed",
        type=float,
        default=0.08,
        help="Rover patrol crawl velocity in m/s (default: 0.08 m/s, increased by ~35%% from 0.06 m/s)."
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
    parser.add_argument(
        "--autostart", "--start",
        action="store_true",
        help="Immediately start rover patrolling upon launch without waiting for web button or keypress."
    )
    args, _ = parser.parse_known_args()

    # Auto-detect headless mode if no DISPLAY environment variable
    if args.headless or not os.environ.get("DISPLAY"):
        is_headless = True
    else:
        is_headless = False

    web_port = args.port
    rover_linear_speed = args.speed

    if args.autostart:
        global motor_enabled, current_state_str
        motor_enabled = True
        current_state_str = "PATROLLING"


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
    Calibrated railway track slit, cut, and breakage detector.
    - Strictly inspects ONLY the black railway tape stripes (zero track bed detections).
    - Surface invariant: operates identically on dark brown/wood and light cream surfaces.
    - Calibrated with physical ground truth: Tape width = 1.0 cm (10.0 mm).
    """
    h, w = gray_frame.shape[:2]
    gray = cv2.cvtColor(gray_frame, cv2.COLOR_BGR2GRAY) if len(gray_frame.shape) == 3 else gray_frame

    # 1. FOV BOUNDS: Active Inspection Field of View
    # Center and slightly off-center (reject top horizon & bottom rover bumper)
    y_fov_min = int(0.20 * h)
    y_fov_max = int(0.82 * h)

    # 2. HORIZONTAL SLICE PROFILING: Identify dark stripe valleys (rails)
    step_y = 6
    sample_ys = list(range(y_fov_min, y_fov_max, step_y))

    stripe_segments = []
    for y in sample_ys:
        row = gray[y, :].astype(np.float32)
        row_s = cv2.GaussianBlur(row, (21, 1), 0).flatten()

        margin_x = int(0.04 * w)
        interior = row_s[margin_x : w - margin_x]
        if interior.size == 0:
            continue
        bg_val = float(np.percentile(interior, 70))

        # Black tape is substantially darker than surface across all backgrounds (wood or cream)
        tape_thresh = min(bg_val - 16.0, 115.0)

        is_dark = (row_s < tape_thresh) & (np.arange(w) >= margin_x) & (np.arange(w) <= w - margin_x)
        diffs = np.diff(is_dark.astype(np.int8))
        starts = np.where(diffs == 1)[0] + 1
        ends = np.where(diffs == -1)[0] + 1
        if is_dark[0]:
            starts = np.r_[0, starts]
        if is_dark[-1]:
            ends = np.r_[ends, w]

        for s, e in zip(starts, ends):
            sw = e - s
            if 18 <= sw <= int(0.42 * w):
                drop_l = row_s[max(0, s - 10)] - np.min(row_s[s:e])
                drop_r = row_s[min(w - 1, e + 10)] - np.min(row_s[s:e])
                if drop_l >= 12.0 and drop_r >= 12.0:
                    stripe_segments.append((y, (s + e) // 2, sw, float(np.min(row_s[s:e]))))

    if not stripe_segments:
        return []

    # 3. RAIL CLUSTERING: Group stripe segments into vertical rail lines
    xs = np.array([s[1] for s in stripe_segments])
    hist, bin_edges = np.histogram(xs, bins=np.arange(0, w + 30, 30))
    hist_smooth = cv2.GaussianBlur(hist.astype(np.float32), (5, 1), 0).flatten()

    peak_bin_indices = []
    for bi in range(len(hist_smooth)):
        if hist_smooth[bi] >= 3:
            is_peak = True
            if bi > 0 and hist_smooth[bi - 1] > hist_smooth[bi]:
                is_peak = False
            if bi < len(hist_smooth) - 1 and hist_smooth[bi + 1] > hist_smooth[bi]:
                is_peak = False
            if is_peak:
                peak_bin_indices.append(bi)

    rail_centers_x = [(bin_edges[bi] + bin_edges[bi + 1]) / 2.0 for bi in peak_bin_indices]

    # In rover dual-rail view, reject middle of track bed (between 0.42*w and 0.58*w)
    has_left = any(cx < 0.42 * w for cx in rail_centers_x)
    has_right = any(cx > 0.58 * w for cx in rail_centers_x)
    if has_left and has_right:
        rail_centers_x = [cx for cx in rail_centers_x if (cx < 0.42 * w or cx > 0.58 * w)]

    if len(rail_centers_x) > 2:
        def count_near(rc):
            return sum(1 for s in stripe_segments if abs(s[1] - rc) <= 45)
        rail_centers_x.sort(key=count_near, reverse=True)
        rail_centers_x = rail_centers_x[:2]

    detections = []

    # 4. DEFECT DETECTION ON EACH TRACKED RAIL
    for rail_x in rail_centers_x:
        rail_segs = [s for s in stripe_segments if abs(s[1] - rail_x) <= 45]
        if len(rail_segs) < 5:
            continue

        r_ys = np.array([s[0] for s in rail_segs], dtype=np.float32)
        r_xs = np.array([s[1] for s in rail_segs], dtype=np.float32)
        r_ws = np.array([s[2] for s in rail_segs], dtype=np.float32)

        poly = np.polyfit(r_ys, r_xs, 1)
        med_w_px = float(np.median(r_ws))

        # Ground Truth Calibration: Tape is 1.0 cm = 10.0 mm wide
        mm_per_px = 10.0 / max(10.0, med_w_px)

        y_start = max(y_fov_min, int(np.min(r_ys)))
        y_end = min(y_fov_max, int(np.max(r_ys)))

        spine_ys = list(range(y_start, y_end + 1, 2))
        half_w = max(4, int(med_w_px * 0.30))

        intensities = []
        vert_grads = []
        for y in spine_ys:
            cx = int(np.polyval(poly, y))
            if cx - half_w < 0 or cx + half_w >= w:
                intensities.append(255.0)
                vert_grads.append(0.0)
                continue

            patch = gray[y, cx - half_w : cx + half_w + 1].astype(np.float32)
            intensities.append(float(np.mean(patch)))

            if y >= 2 and y < h - 2:
                top_p = gray[y - 2, cx - half_w : cx + half_w + 1].astype(np.float32)
                bot_p = gray[y + 2, cx - half_w : cx + half_w + 1].astype(np.float32)
                vert_grads.append(float(np.mean(np.abs(bot_p - top_p))))
            else:
                vert_grads.append(0.0)

        intensities = np.array(intensities)
        vert_grads = np.array(vert_grads)

        tape_base = float(np.percentile(intensities, 20))
        dI = intensities - tape_base

        defect_indices = []
        for i, y_val in enumerate(spine_ys):
            cx = int(np.polyval(poly, y_val))
            if cx < 0.05 * w or cx > 0.95 * w:
                continue
            if dI[i] >= 24.0 or (vert_grads[i] >= 22.0 and dI[i] >= 8.0):
                defect_indices.append((y_val, cx, float(dI[i]), float(vert_grads[i])))

        if not defect_indices:
            continue

        clusters = []
        cur = [defect_indices[0]]
        for pt in defect_indices[1:]:
            if pt[0] - cur[-1][0] <= 8:
                cur.append(pt)
            else:
                if len(cur) >= 2:
                    clusters.append(cur)
                cur = [pt]
        if len(cur) >= 2:
            clusters.append(cur)

        for clust in clusters:
            cy_min = min(p[0] for p in clust)
            cy_max = max(p[0] for p in clust)
            gap_px = max(2, cy_max - cy_min)

            if gap_px > int(1.1 * med_w_px):
                continue

            mid_y = (cy_min + cy_max) // 2
            mid_x = int(np.polyval(poly, mid_y))

            if mid_x < 0.06 * w or mid_x > 0.94 * w:
                continue

            max_dI = max(p[2] for p in clust)
            max_gy = max(p[3] for p in clust)

            bx1 = max(0, int(mid_x - med_w_px * 0.52))
            bx2 = min(w, int(mid_x + med_w_px * 0.52))
            by1 = max(0, cy_min - 4)
            by2 = min(h, cy_max + 4)
            bw = bx2 - bx1
            bh = by2 - by1

            # Metric dimensions: Transverse length cannot exceed 10.0 mm
            if max_dI >= 25.0:
                length_mm = 10.0
            else:
                length_mm = min(10.0, max(4.0, (bw * mm_per_px) * 0.85))

            gap_mm = max(0.5, gap_px * mm_per_px)
            depth_mm = max(0.6, min(2.5, max_dI * 0.02 + max_gy * 0.03))

            conf = min(0.99, max(0.75, 0.78 + min(0.12, max_dI * 0.003) + min(0.09, max_gy * 0.003)))

            if length_mm >= 8.5 or gap_mm >= 2.2:
                risk = "CRITICAL"
                color = (0, 0, 255)
            elif length_mm >= 5.0 or gap_mm >= 1.2:
                risk = "HIGH"
                color = (0, 69, 255)
            elif length_mm >= 3.0:
                risk = "MODERATE"
                color = (0, 165, 255)
            else:
                risk = "MINOR"
                color = (0, 255, 255)

            rail_side = "LEFT" if mid_x < 0.5 * w else "RIGHT"

            detections.append({
                "bbox": (bx1, by1, bx2, by2),
                "center": (mid_x, mid_y),
                "length_px": float(bw),
                "width_px": float(bh),
                "length_mm": float(length_mm),
                "width_mm": float(gap_mm),
                "depth_mm": float(depth_mm),
                "conf": float(conf),
                "risk": risk,
                "color": color,
                "score": float(max_dI + max_gy),
                "rail": rail_side
            })

    # 5. MERGE OVERLAPPING DETECTIONS
    merged = []
    detections.sort(key=lambda d: d["score"], reverse=True)
    for d in detections:
        matched = False
        for m in merged:
            if abs(d["center"][1] - m["center"][1]) <= 25 and abs(d["center"][0] - m["center"][0]) <= 30:
                nx1 = min(d["bbox"][0], m["bbox"][0])
                ny1 = min(d["bbox"][1], m["bbox"][1])
                nx2 = max(d["bbox"][2], m["bbox"][2])
                ny2 = max(d["bbox"][3], m["bbox"][3])
                m["bbox"] = (nx1, ny1, nx2, ny2)
                m["center"] = ((nx1 + nx2) // 2, (ny1 + ny2) // 2)
                m["conf"] = max(m["conf"], d["conf"])
                m["length_mm"] = max(m["length_mm"], d["length_mm"])
                m["width_mm"] = max(m["width_mm"], d["width_mm"])
                matched = True
                break
        if not matched:
            merged.append(d)

    return merged


def render_display(frame_bgr: np.ndarray, detections: list[dict], fps: float, count: int) -> np.ndarray:
    """Renders the full annotated camera feed with bounding boxes, risk labels, and railway coordinates."""
    global rover_location_x, rover_linear_speed, is_inspecting_hold, hold_start_time, last_odom_time
    global hw_motor, motor_enabled, last_alert_cooldown_time, last_defect_info, current_state_str
    global last_inspected_x, resume_patrol_time, MIN_CLEARING_DISTANCE, MIN_CLEARING_TIME

    now = time.time()
    dt = now - last_odom_time
    last_odom_time = now

    h, w = frame_bgr.shape[:2]

    # Calculate distance traveled and active patrol time since the last defect was inspected
    dist_since_inspection = abs(rover_location_x - last_inspected_x)
    time_since_resume = (now - resume_patrol_time) if resume_patrol_time > 0 else 999.0

    # Are we currently rolling past the previously-inspected defect?
    # Enforces that the rover MUST move at least MIN_CLEARING_DISTANCE (0.70m) and 10s past the crack
    is_clearing_inspected = (dist_since_inspection < MIN_CLEARING_DISTANCE) or (time_since_resume < MIN_CLEARING_TIME)

    # Check for risk > MODERATE (HIGH or CRITICAL)
    has_high_risk = any(d["risk"] in ("HIGH", "CRITICAL") for d in detections)

    # Format Railway Chainage & Coordinate Standard
    km = int(abs(rover_location_x) // 1000)
    m = abs(rover_location_x) % 1000
    chainage_str = f"CH {km:02d}+{m:05.2f}m"
    coord_str = f"X: {rover_location_x:+.2f}m, Y: +0.00m"

    # Rover motion behavior state machine:
    # 1. Stationary Hold at Defect (5.0s countdown)
    if is_inspecting_hold:
        elapsed = now - hold_start_time
        if elapsed < 5.0:
            remaining = 5.0 - elapsed
            if hw_motor and motor_enabled:
                hw_motor.set_velocity(0.0, 0.0)
            state_label = f"HOLDING AT DEFECT [{remaining:.1f}s] — ALERT SENT TO INSPECTOR"
            current_state_str = f"HOLDING [{remaining:.1f}s]"
            state_color = (0, 0, 255)
        else:
            # 5.0s hold finished: immediately resume moving forward to clear past the crack
            is_inspecting_hold = False
            resume_patrol_time = now
            state_label = "INSPECTION COMPLETE — RESUMING PATROL PAST CRACK"
            current_state_str = "CLEARING_DEFECT"
            state_color = (0, 255, 120)
            if last_defect_info:
                last_defect_info["active"] = False
            if hw_motor and motor_enabled:
                hw_motor.set_velocity(rover_linear_speed, 0.0)
            print(f"⏩ [PATROL RESUMED] 5.0s hold complete. Rover driving forward past documented defect at {rover_linear_speed:.2f} m/s...")

    # 2. Trigger Inspection for a NEW crack (Only if NOT clearing previously-inspected crack)
    elif has_high_risk and not is_clearing_inspected:
        is_inspecting_hold = True
        hold_start_time = now
        last_inspected_x = rover_location_x
        resume_patrol_time = 0.0
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

    # 3. Active Patrolling / Clearing Mode
    else:
        if motor_enabled:
            # Advance location along track and drive physical motors
            rover_location_x += rover_linear_speed * dt
            if hw_motor:
                hw_motor.set_velocity(rover_linear_speed, 0.0)

            if is_clearing_inspected:
                state_label = f"CLEARING DOCUMENTED DEFECT (+{dist_since_inspection:.2f}m / {MIN_CLEARING_DISTANCE:.2f}m) — PATROLLING"
                current_state_str = "CLEARING_DEFECT"
                state_color = (0, 255, 120)
            else:
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

        # If this defect is already documented and being cleared, display in cyan/green
        if is_clearing_inspected and not is_inspecting_hold:
            box_color = (0, 255, 120)
            label = f"DOCUMENTED SLIT | Conf: {d['conf']*100:.1f}%"
            dims = f"CLEARING (+{dist_since_inspection:.2f}m / {MIN_CLEARING_DISTANCE:.2f}m)"
        else:
            box_color = d["color"]
            label = f"{d['risk']} DEFECT | Conf: {d['conf']*100:.1f}%"
            dims = f"L: {d['length_mm']:.1f}mm | W: {d['width_mm']:.1f}mm | D: {d['depth_mm']:.1f}mm"

        cv2.rectangle(vis, (x1, y1), (x2, y2), box_color, 3)
        cv2.circle(vis, d["center"], 5, (0, 255, 255), -1)

        box_w = 330
        cv2.rectangle(vis, (x1, max(0, y1 - 48)), (x1 + box_w, max(48, y1)), (15, 20, 28), -1)
        cv2.putText(vis, label, (x1 + 6, max(18, y1 - 28)), cv2.FONT_HERSHEY_SIMPLEX, 0.52, box_color, 2)
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

    # Automatically publish live IP to GitHub Pages in background and monitor for changes
    def _ip_publisher_worker():
        last_published_ip = None
        while running:
            try:
                curr_ip = get_local_ip()
                if curr_ip and not curr_ip.startswith("127.") and curr_ip != last_published_ip:
                    pub_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "publish_ip.py")
                    if os.path.isfile(pub_script):
                        res = subprocess.run([sys.executable, pub_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        if res.returncode == 0:
                            last_published_ip = curr_ip
            except Exception:
                pass
            time.sleep(30.0)

    threading.Thread(target=_ip_publisher_worker, daemon=True).start()

    print("=" * 72)
    print("  AUTONOMOUS RAILWAY TRACK INSPECTION ROVER — REMOTE CONTROLLER")
    print("=" * 72)
    print(f"  Mode:              {'HEADLESS (NO MONITOR NEEDED)' if is_headless else 'DESKTOP WINDOW + WEB'}")
    print(f"  Camera:            Raspberry Pi Camera Module 3 (IMX708)")
    print(f"  Speed:             {rover_linear_speed:.2f} m/s patrol crawl speed")
    print(f"  Initial State:     {'PATROLLING (ACTIVE)' if motor_enabled else 'STANDBY (WAITING FOR START)'}")
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
                    last_inspected_x = -999.0
                    resume_patrol_time = 0.0
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
