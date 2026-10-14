# Autonomous Railway Track Inspection Rover

[![GitHub Pages](https://img.shields.io/badge/Live%20Web%20Dashboard-GitHub%20Pages-blue?style=for-the-badge&logo=github)](https://biswalanish2005-ops.github.io/Railway_Track_Inspection_Rover/)
[![ROS 2](https://img.shields.io/badge/ROS%202-Jazzy%20Jalisco-22314E?style=for-the-badge&logo=ros)](https://docs.ros.org/en/jazzy/)
[![Platform](https://img.shields.io/badge/Hardware-Raspberry%20Pi%205-C51A4A?style=for-the-badge&logo=raspberrypi)](https://www.raspberrypi.com/products/raspberry-pi-5/)

> 🌐 **Live Cloud Inspection Portal**: [https://biswalanish2005-ops.github.io/Railway_Track_Inspection_Rover/](https://biswalanish2005-ops.github.io/Railway_Track_Inspection_Rover/)
>
> 🚆 **Local Headless Rover IP**: `http://172.16.61.192:8080/` (or `http://student-desktop.local:8080/`)

An autonomous, ROS 2 Jazzy-based robotics software and hardware platform for real-time railway rail crack detection, IPM perspective-calibrated dimension measurement, persistent inspection record logging, and web-based remote monitoring.

---

## 1. Project Overview

The **Autonomous Railway Track Inspection Rover** moves along railway tracks, captures high-resolution imagery using a Raspberry Pi Camera Module 3 mounted at a 50° pitch angle relative to the ground plane, performs machine-learning crack detection, executes controlled stops upon defect detection, performs skeletonization-based physical measurement (length, width, apparent depth), logs inspection vaults to disk, and broadcasts telemetry to a web dashboard.

---

## 2. Hardware Requirements

- **Processor**: Raspberry Pi 5 (4GB or 8GB RAM)
- **Camera**: Raspberry Pi Camera Module 3 (CSI interface)
- **Chassis**: 4-wheel-drive rover chassis with track-flanged wheels
- **Actuators**: 4 × 12V DC Geared Motors
- **Motor Driver**: L298N Dual H-Bridge Motor Driver
- **Power System**:
  - 3S Lithium-ion Battery (11.1V - 12.6V, 2200mAh+)
  - 5V/5A High-Current Buck Converter (Step-Down to 5V DC for RPi 5 via USB-C/GPIO)
  - Common Ground Wire
  - 5A Inline Power Fuse & Power Toggle Switch

---

## 3. Software Requirements

- **Operating System**: Ubuntu 24.04 LTS (Noble Numbat)
- **ROS 2 Distribution**: ROS 2 Jazzy Jalisco
- **Language**: Python 3.12+ & C++ (ament_cmake interfaces)
- **Computer Vision**: OpenCV 4.x & NumPy
- **Image Bridge**: `cv_bridge`
- **Visualization**: RViz2 & HTML5 Web Dashboard

---

## 4. System & ROS 2 Architecture

### Node Diagram & Interface Flow

```text
Raspberry Pi Camera Module 3 / Sim
               │
               ▼
       [camera_publisher] ──► /camera/image_raw (sensor_msgs/Image)
               │              /camera/camera_info (sensor_msgs/CameraInfo)
               ▼
       [image_processor] ──► /camera/image_rectified (Calibration Undistort)
               │             /camera/rail_ipm (50° IPM Homography Top-Down)
               │             /camera/processed_overlay (Diagnostic Display)
               ▼
     [crack_detection_node] ──► /crack_detection (rover_msgs/CrackDetection)
               │
               ▼
   [inspection_manager_node] ──► /cmd_vel (geometry_msgs/Twist)
               │
               ├─────────────────────────────────────────┐
               ▼                                         ▼
      [motor_controller]                      [crack_measurement_node]
               │                                         │
               ▼                                         ▼
   (Mock / L298N Driver)                     /inspection_result
               │                                         │
               ▼                                         ▼
           [Rover]                               [data_logger_node]
                                                         │
                                                         ▼
                                             [remote_monitor_node]
                                                         │
                                                         ▼
                                                Web Dashboard (8080)
```

---

## 5. Autonomous State Machine

```text
       ┌──────────┐
       │   IDLE   │
       └────┬─────┘
            │ valid /cmd_vel
            ▼
       ┌──────────┐
       │  MOVING  │◄────────────────────────┐
       └────┬─────┘                         │
            │ crack detected (conf >= 0.75) │ auto-resume
            ▼                               │
       ┌──────────┐                         │
       │ SLOWING  │                         │
       └────┬─────┘                         │
            │ speed == 0                    │
            ▼                               │
       ┌──────────┐                         │
       │ INSPECTING─────────────────────────┘
       └────┬─────┘
            │ E-Stop Activated
            ▼
       ┌──────────┐     Reset Service Call     ┌──────────┐
       │ STOPPED  │───────────────────────────►│   IDLE   │
       └──────────┘                            └──────────┘
```

---

## 6. Installation & ROS 2 Workspace Setup

### Workspace Setup
```bash
mkdir -p ~/Desktop/Railway_Inspection_Rover/src
cd ~/Desktop/Railway_Inspection_Rover
colcon build --symlink-install
source install/setup.bash
```

---

## 7. Running the Autonomous Rover

### Full System Launch (All 10 Nodes)
```bash
source ~/Desktop/Railway_Inspection_Rover/install/setup.bash
ros2 launch rover_bringup rover_full_system.launch.py
```

### Keyboard Teleoperation Interface
```bash
source ~/Desktop/Railway_Inspection_Rover/install/setup.bash
ros2 run rover_control teleop_keyboard
```

---

## 8. Web Remote Monitoring Dashboard

Open any web browser on the local wireless network:

```text
http://<RASPBERRY_PI_IP>:8080
```

### Dashboard Features:
- Real-time telemetry (`state`, `speed`, `motor_enabled`, `watchdog`)
- Live MJPEG video stream (`/video_feed`) showing undistorted rail overlay
- ML crack detection metrics & severity ratings
- Web-based Emergency Stop & Clear buttons

---

## 9. Crack Measurement & Planar Calibration

### Homography & Physical Unit Conversion
Camera is mounted at **50° downward pitch angle**. Homography matrix $H$ maps the 50° trapezoidal ROI into an orthogonal top-down plane ($400 \times 600$ pixels).

Physical millimeter scale factor:
$$S = \frac{\text{rail\_physical\_width\_mm}}{\text{rail\_pixel\_width\_in\_ipm}} = \frac{70.0}{200.0} = 0.35 \text{ mm/pixel}$$

- **Crack Centerline Length**: $L_{\text{mm}} = N_{\text{skeleton\_pixels}} \times S$
- **Max Width**: $W_{\text{max\_mm}} = D_{\text{max\_px}} \times S$
- **Apparent Depth / Visual Severity**: Estimated relative shadow contrast drop ($\Delta I = I_{\text{mean}} - I_{\text{shadow}}$).

---

## 10. Inspection Data Storage Vault

Saved records structure:

```text
inspection/
└── YYYY_MM_DD/
    └── inspection_001/
        ├── original.jpg       # Raw image
        ├── processed.jpg      # Dimension overlay
        ├── crack_mask.jpg      # Binary segmentation mask
        └── result.json        # Detailed metadata record
```

Sample `result.json`:
```json
{
    "timestamp": "2026-10-07T13:30:00.123456",
    "inspection_id": "inspection_001",
    "confidence": 0.92,
    "length_mm": 42.5,
    "max_width_mm": 2.1,
    "avg_width_mm": 1.4,
    "apparent_depth_mm": 0.8,
    "severity": "MODERATE",
    "images": {
        "original": "original.jpg",
        "processed": "processed.jpg",
        "mask": "crack_mask.jpg"
    }
}
```

---

## 11. Final Hardware Integration & Safe Wiring Table

### Motor Driver Electrical Capability Check
> [!IMPORTANT]
> The L298N driver is rated for **2.0A continuous per channel** (3.0A peak).
> Connecting 2 DC motors in parallel per side means each channel supplies 2 motors.
> Ensure total stall current per side does not exceed **2.0A continuous** (or use separate drivers / BTN7960 high-current drivers for heavy rovers).

### Pin Connection Table

| Component | Connection | Raspberry Pi 5 / Power Source | Notes |
|---|---|---|---|
| Camera Module 3 | CSI Ribbon Cable | RPi 5 CSI Camera Port 0 | Ensure ribbon tape orientation |
| L298N IN1 | GPIO Pin | RPi 5 GPIO 17 (Pin 11) | Motor Left Direction |
| L298N IN2 | GPIO Pin | RPi 5 GPIO 27 (Pin 13) | Motor Left Direction |
| L298N IN3 | GPIO Pin | RPi 5 GPIO 22 (Pin 15) | Motor Right Direction |
| L298N IN4 | GPIO Pin | RPi 5 GPIO 23 (Pin 16) | Motor Right Direction |
| L298N ENA | Hardware PWM | RPi 5 GPIO 12 (PWM0, Pin 32) | Left Speed Control |
| L298N ENB | Hardware PWM | RPi 5 GPIO 13 (PWM1, Pin 33) | Right Speed Control |
| Motors (Left Side 1 & 2) | Parallel Terminal OUT1/OUT2 | L298N Left Channel | Connect in parallel |
| Motors (Right Side 3 & 4) | Parallel Terminal OUT3/OUT4 | L298N Right Channel | Connect in parallel |
| Battery Positive (+11.1V) | Main Supply | L298N +12V Terminal & Buck Input | Via 5A Fuse & Switch |
| Battery Ground (GND) | Common GND | L298N GND & Buck GND & RPi Pin 6 | **Common Ground Mandatory** |
| Buck Converter 5V Out | 5V DC Supply | RPi 5 USB-C / 5V GPIO (Pin 2) | Powers RPi 5 reliably |

---

## 12. Power Supply Architecture

```text
       3S Lithium-ion Battery (11.1V - 12.6V)
                         │
                  [ 5A Fuse & Switch ]
                         │
         ┌───────────────┴───────────────┐
         ▼                               ▼
  L298N Motor Driver             DC-DC Buck Converter
  (+12V Power Input)             (Step-Down 11.1V ──► 5.0V 5A)
         │                               │
         ▼                               ▼
  4 x DC Motors                   Raspberry Pi 5 (USB-C / 5V GPIO)
```

---

## 13. Safety & Operating Instructions

1. **Bench Testing First**: Always test software nodes with motors disconnected or rover lifted off track.
2. **Watchdog Safety**: Motor controller cuts speed if `/cmd_vel` is lost for $> 0.5\text{s}$.
3. **E-Stop Latches**: E-Stop requires explicit reset service call (`set_estop: false`) before returning to `IDLE`. Rover **never** moves automatically after reset.
4. **Boot Safety**: Motors remain disabled on startup until explicit movement commands arrive.
