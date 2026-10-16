#!/bin/bash
# Autonomous Railway Track Inspection Rover — Headless Remote Start Script
# Runs headless without requiring an HDMI monitor or physical display.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

mkdir -p "$SCRIPT_DIR/inspection"
PID_FILE="$SCRIPT_DIR/inspection/rover.pid"
LOG_FILE="$SCRIPT_DIR/inspection/rover.log"

# Clean up stale processes if already running
if pgrep -f "rover_camera_display.py" > /dev/null; then
    echo "[!] A rover instance is already running. Stopping it first..."
    "$SCRIPT_DIR/stop_rover.sh" > /dev/null 2>&1 || true
    sleep 1
fi

# Detect primary Wi-Fi / LAN IP address
IP_ADDR=$(hostname -I 2>/dev/null | awk '{print $1}')
if [ -z "$IP_ADDR" ]; then
    IP_ADDR="127.0.0.1"
fi
HOSTNAME=$(hostname 2>/dev/null || echo "student-desktop")

echo "========================================================================"
echo "  🚆 AUTONOMOUS RAILWAY TRACK INSPECTION ROVER — HEADLESS MODE"
echo "========================================================================"
echo "  Raspberry Pi IP:       $IP_ADDR"
echo "  mDNS Hostname:         $HOSTNAME.local"
echo "  Web Dashboard:         http://$IP_ADDR:8080/"
echo "  Motor Controller:      L298N (GPIO Pins 12, 13, 17, 27, 22, 23)"
echo "  Camera:                Raspberry Pi Camera Module 3 (IMX708)"
echo "  Sensor ROI:            0.0,0.25,1.0,0.75 (Track Lateral Band)"
echo "  Patrol Speed:          0.06 m/s crawl speed (reduced by 70%)"
echo "  Crack Response:        5.0s stationary hold, remote dispatch, auto-resume"
echo "========================================================================"

# Check for background daemon flag (-d / --daemon / --background)
if [[ "$1" == "-d" || "$1" == "--daemon" || "$1" == "--background" ]]; then
    echo "[*] Starting Rover in BACKGROUND DAEMON mode..."
    setsid python3 -u rover_camera_display.py --headless < /dev/null > "$LOG_FILE" 2>&1 &
    ROVER_PID=$!
    echo "$ROVER_PID" > "$PID_FILE"
    sleep 2.5
    
    if kill -0 "$ROVER_PID" 2>/dev/null; then
        echo "✅ Rover started successfully in background! (PID: $ROVER_PID)"
        echo ""
        echo "🌐 Open the live dashboard on your laptop browser:"
        echo "   👉 http://$IP_ADDR:8080/"
        echo ""
        echo "Commands to manage the rover over SSH:"
        echo "   Check Status:       ./status_rover.sh"
        echo "   View Live Logs:     tail -f inspection/rover.log"
        echo "   Stop Rover:         ./stop_rover.sh"
    else
        echo "❌ Rover failed to start. Showing last log entries:"
        tail -n 20 "$LOG_FILE"
        exit 1
    fi
else
    # Interactive mode (runs directly in SSH terminal with live ASCII telemetry)
    echo "[*] Starting Rover in INTERACTIVE SSH mode..."
    echo "[*] Press Ctrl+C at any time to safely halt motors and exit."
    echo ""
    python3 rover_camera_display.py --headless
fi
