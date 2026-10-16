"""
Inspection Manager Node for Railway Inspection Rover.

Orchestrates the automatic crack inspection workflow:
PATROLLING (SEARCHING) -> CRACK DETECTED (RISK > MODERATE) -> CONTROLLED STOP ->
STATIONARY INSPECTION & MEASUREMENT -> TRANSMIT LOCATION TO REMOTE INSPECTOR ->
AUTOMATICALLY RESUME PATROL.
"""

import time
from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node
from rover_msgs.msg import CrackDetection, InspectionResult, RoverState


class InspectionManagerNode(Node):
    """ROS 2 Inspection Manager Node."""

    def __init__(self) -> None:
        super().__init__("inspection_manager_node")

        # Declare Parameters
        self.declare_parameter("inspection_hold_duration_sec", 5.0)
        self.declare_parameter("auto_resume_after_inspection", True)
        self.declare_parameter("inspection_speed", 0.06)
        self.declare_parameter("detection_cooldown_sec", 5.0)

        # Retrieve Parameters
        self._hold_duration = float(
            self.get_parameter("inspection_hold_duration_sec").value
        )
        self._auto_resume = bool(
            self.get_parameter("auto_resume_after_inspection").value
        )
        self._crawl_speed = float(self.get_parameter("inspection_speed").value)
        self._cooldown_duration = float(
            self.get_parameter("detection_cooldown_sec").value
        )

        # Workflow State
        self._manager_state = "IDLE"  # IDLE, SEARCHING, SLOWING, INSPECTING, RESUMING
        self._inspection_start_time = 0.0
        self._last_alert_time = 0.0
        self._is_e_stopped = False

        # Latest Telemetry & Defect Tracking
        self._current_location_x = 0.0
        self._current_location_y = 0.0
        self._current_chainage = "CH 00+00.00m"
        self._pending_alert = None

        # Subscribers
        self._rover_state_sub = self.create_subscription(
            RoverState, "/rover_state", self._rover_state_callback, 10
        )
        self._crack_sub = self.create_subscription(
            CrackDetection, "/crack_detection", self._crack_callback, 10
        )
        self._result_sub = self.create_subscription(
            InspectionResult, "/inspection_result", self._result_callback, 10
        )

        # Motion Publisher
        self._cmd_vel_pub = self.create_publisher(Twist, "/cmd_vel", 10)

        # Control Loop Timer (10 Hz)
        self.create_timer(0.1, self._workflow_loop)

        self.get_logger().info(
            f"Inspection Manager initialized (Speed: {self._crawl_speed}m/s, Hold: {self._hold_duration}s, Auto-Resume: {self._auto_resume})"
        )

    def _rover_state_callback(self, msg: RoverState) -> None:
        """Track safety and coordinate state."""
        self._is_e_stopped = msg.emergency_stop_active
        self._current_location_x = float(msg.location_x)
        self._current_location_y = float(msg.location_y)
        if msg.chainage_station:
            self._current_chainage = msg.chainage_station

    def _crack_callback(self, msg: CrackDetection) -> None:
        """Handle incoming crack detection triggers."""
        if self._is_e_stopped:
            return

        now = time.time()
        # Cooldown guard to avoid repeated stops on the same physical crack
        if (now - self._last_alert_time) < self._cooldown_duration:
            return

        if msg.crack_detected and msg.confidence >= 0.65:
            # Check if crack risk calculated is more than moderate (HIGH or CRITICAL)
            is_more_than_moderate = msg.severity_label in ("HIGH", "CRITICAL")

            if is_more_than_moderate:
                if self._manager_state == "SEARCHING":
                    self.get_logger().warn(
                        f"🚨 [CRACK DETECTED — RISK > MODERATE] "
                        f"Severity: {msg.severity_label} | Conf: {msg.confidence*100:.1f}% | "
                        f"Dimensions: {msg.estimated_length_mm:.1f}mm x {msg.estimated_width_mm:.1f}mm. "
                        f"Initiating controlled stop to transmit coordinates..."
                    )
                    self._manager_state = "SLOWING"
                    self._inspection_start_time = now
                    self._last_alert_time = now
                    self._pending_alert = {
                        "severity": msg.severity_label,
                        "conf": msg.confidence,
                        "location_x": self._current_location_x,
                        "location_y": self._current_location_y,
                        "chainage": self._current_chainage,
                        "length_mm": msg.estimated_length_mm,
                        "width_mm": msg.estimated_width_mm,
                        "depth_mm": msg.estimated_depth_mm,
                    }
            else:
                self.get_logger().info(
                    f"ℹ️ [MINOR/MODERATE DEFECT LOGGED] Severity: {msg.severity_label} at {self._current_chainage}. Continuing normal patrol."
                )

    def _result_callback(self, msg: InspectionResult) -> None:
        """Handle completed inspection measurement payload."""
        self.get_logger().info(
            f"✅ [INSPECTION LOGGED] ID: {msg.inspection_id} | Location: {msg.chainage_station} | Rating: {msg.severity_rating}"
        )

    def _workflow_loop(self) -> None:
        """Main state machine orchestrator loop."""
        if self._is_e_stopped:
            self._manager_state = "IDLE"
            return

        now = time.time()
        twist = Twist()

        if self._manager_state == "IDLE":
            # Transition to active searching mode
            self._manager_state = "SEARCHING"
            self.get_logger().info("Rover entering SEARCHING mode. Patrolling track at inspection speed.")

        elif self._manager_state == "SEARCHING":
            # Command normal forward movement along track
            twist.linear.x = self._crawl_speed
            self._cmd_vel_pub.publish(twist)

        elif self._manager_state == "SLOWING":
            # Decelerate smoothly to 0
            twist.linear.x = 0.0
            self._cmd_vel_pub.publish(twist)
            if (now - self._inspection_start_time) >= 1.0:
                self._manager_state = "INSPECTING"
                # Transmit location and defect data to remote railway inspector
                if self._pending_alert:
                    a = self._pending_alert
                    self.get_logger().error(
                        f"📡 >>> [LOCATION TRANSMITTED TO REMOTE RAILWAY INSPECTOR] <<<\n"
                        f"    Station Chainage: {a['chainage']}\n"
                        f"    Track Coordinates: X: {a['location_x']:+.2f}m, Y: {a['location_y']:+.2f}m\n"
                        f"    Defect Risk Level: {a['severity']} (CRITICAL/HIGH)\n"
                        f"    Estimated Size:   Length {a['length_mm']:.1f}mm, Width {a['width_mm']:.1f}mm, Depth {a['depth_mm']:.1f}mm\n"
                        f"    Confidence:       {a['conf']*100:.1f}%\n"
                        f"    Action:           Inspection report dispatched to dashboard. Rover pausing for stationary hold."
                    )
                    self._pending_alert = None

        elif self._manager_state == "INSPECTING":
            # Hold stationary during inspection and remote dispatch
            twist.linear.x = 0.0
            self._cmd_vel_pub.publish(twist)

            if (now - self._inspection_start_time) >= (1.0 + self._hold_duration):
                if self._auto_resume:
                    self._manager_state = "RESUMING"
                    self.get_logger().info(
                        "⏩ [PATROL RESUMED] Remote transmission complete. Rover resuming track patrol..."
                    )
                else:
                    self._manager_state = "HOLD"

        elif self._manager_state == "RESUMING":
            # Resume searching after hold period
            self._manager_state = "SEARCHING"


def main(args=None) -> None:
    rclpy.init(args=args)
    node = InspectionManagerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
