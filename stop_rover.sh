#!/bin/bash
# Autonomous Railway Track Inspection Rover — Remote Stop & Emergency Halt Script
# Halts all inspection processes, camera pipelines, and writes 0V to all motor GPIO pins.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/inspection/rover.pid"

echo "[*] Halting Autonomous Railway Inspection Rover..."

# Kill running python rover display/controller processes
pkill -INT -f "rover_camera_display.py" 2>/dev/null || true
sleep 0.5
pkill -TERM -f "rover_camera_display.py" 2>/dev/null || true
pkill -TERM -f "rpicam-vid" 2>/dev/null || true

# Force kill any stubborn lingering instances
sleep 0.5
pkill -9 -f "rover_camera_display.py" 2>/dev/null || true
pkill -9 -f "rpicam-vid" 2>/dev/null || true

if [ -f "$PID_FILE" ]; then
    rm -f "$PID_FILE"
fi

# Hardware safety: Drive all L298N GPIO pins to LOW (0V) and release them
python3 - << 'EOF'
import sys
try:
    import lgpio
    # Raspberry Pi 5 uses gpiochip 4 for 40-pin header
    chip = 4
    try:
        h = lgpio.gpiochip_open(chip)
    except Exception:
        chip = 0
        h = lgpio.gpiochip_open(chip)

    # Pins: ENA=12, ENB=13, IN1=17, IN2=27, IN3=22, IN4=23
    for pin in [12, 13, 17, 27, 22, 23]:
        try:
            lgpio.gpio_claim_output(h, pin, 0)
            lgpio.gpio_write(h, pin, 0)
            lgpio.gpio_free(h, pin)
        except Exception:
            pass
    lgpio.gpiochip_close(h)
    print("🔒 [HARDWARE SAFETY] All L298N motor driver pins grounded (0V) & freed.")
except Exception as e:
    print(f"[!] GPIO shutdown note: {e}")
EOF

echo "✅ Autonomous Railway Rover and camera pipeline halted cleanly."
