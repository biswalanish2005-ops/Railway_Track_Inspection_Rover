#!/bin/bash
# Autonomous Railway Track Inspection Rover — Status Check Script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/inspection/rover.pid"
LOG_FILE="$SCRIPT_DIR/inspection/rover.log"

IP_ADDR=$(hostname -I 2>/dev/null | awk '{print $1}')
if [ -z "$IP_ADDR" ]; then
    IP_ADDR="127.0.0.1"
fi
HOSTNAME=$(hostname 2>/dev/null || echo "student-desktop")

echo "========================================================================"
echo "  🚆 RAILWAY INSPECTION ROVER — SYSTEM STATUS"
echo "========================================================================"

ROVER_PIDS=$(pgrep -f "rover_camera_display.py" || true)

if [ -n "$ROVER_PIDS" ]; then
    echo "  Status:            🟢 RUNNING (PID: $ROVER_PIDS)"
    echo "  Raspberry Pi IP:   $IP_ADDR"
    echo "  Web Dashboard:     http://$IP_ADDR:8080/"
    echo "  Hostname:          http://$HOSTNAME.local:8080/"
    echo "------------------------------------------------------------------------"
    
    # Query live telemetry if web server is responding
    TELEMETRY=$(curl -s --max-time 1 "http://127.0.0.1:8080/api/telemetry" 2>/dev/null || true)
    if [ -n "$TELEMETRY" ]; then
        echo "  Live Telemetry:"
        echo "    $TELEMETRY" | python3 -m json.tool 2>/dev/null | sed 's/^/    /' || echo "    $TELEMETRY"
    fi

    echo "------------------------------------------------------------------------"
    if [ -f "$LOG_FILE" ]; then
        echo "  Recent Log Output (last 8 lines):"
        tail -n 8 "$LOG_FILE" | sed 's/^/    /'
    fi
else
    echo "  Status:            🔴 STOPPED (No active inspection process)"
    echo "  Raspberry Pi IP:   $IP_ADDR"
    echo "  To start rover:    ./start_rover.sh (interactive) or ./start_rover.sh -d (background)"
fi
echo "========================================================================"
