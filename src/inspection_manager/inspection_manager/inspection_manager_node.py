"""
Inspection Manager Node for Railway Inspection Rover.

Orchestrates the automatic crack inspection workflow:
MOVING -> CRACK DETECTED -> CONTROLLED STOP -> STATIONARY CAPTURE & MEASUREMENT -> REPORT & SAVE -> RESUME.
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
        self.declare_parameter("inspection_hold_duration_sec", 3.0)
        self.declare_parameter("auto_resume_after_inspection", True)
        self.declare_parameter("inspection_speed", 0.2)

        # Retrieve Parameters
        self._hold_duration = float(
            self.get_parameter("inspection_hold_duration_sec").value
        )
        self._auto_resume = bool(
            self.get_parameter("auto_resume_after_inspection").value
        )
        self._crawl_speed = float(self.get_parameter("inspection_speed").value)

        # Internal Workflow State
        self._manager_state = "IDLE"  # IDLE, SEARCHING, SLOWING, INSPECTING, RESUMING
        self._last_detection_time = 0.0
        self._inspection_start_time = 0.0
        self._is_e_stopped = False

        # ROS 2 Subscribers
        self._rover_state_sub = self.create_subscription(
            RoverState, "/rover_state", self._rover_state_callback, 10
        )
        self._crack_sub = self.create_subscription(
            CrackDetection, "/crack_detection", self._crack_callback, 10
        )
        self._result_sub = self.create_subscription(
            InspectionResult, "/inspection_result", self._result_callback, 10
        )

        # ROS 2 Motion Publisher
        self._cmd_vel_pub = self.create_publisher(Twist, "/cmd_vel", 10)

        # Control Loop Timer (10 Hz)
        self.create_timer(0.1, self._workflow_loop)

        self.get_logger().info(
            f"Inspection Manager Node initialized (Crawl speed: {self._crawl_speed}m/s, Hold: {self._hold_duration}s)"
        )

    def _rover_state_callback(self, msg: RoverState) -> None:
        """Track e-stop safety state."""
        self._is_e_stopped = msg.emergency_stop_active

    def _crack_callback(self, msg: CrackDetection) -> None:
        """Handle incoming crack detection triggers."""
        if self._is_e_stopped:
            return

        if msg.crack_detected and msg.confidence >= 0.75:
            if self._manager_state == "SEARCHING":
                self.get_logger().warn(
                    f"[INSPECTION TRIGGERED] High-confidence crack detected ({msg.confidence*100:.1f}%). Initiating controlled stop..."
                )
                self._manager_state = "SLOWING"
                self._inspection_start_time = time.time()

    def _result_callback(self, msg: InspectionResult) -> None:
        """Handle completed inspection measurement payload."""
        self.get_logger().info(
            f"[INSPECTION RECORDED] ID: {msg.inspection_id} | Rating: {msg.severity_rating} | Length: {msg.crack_length_mm:.1f}mm"
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
            self.get_logger().info("Rover entering SEARCHING mode. Crawling at inspection speed.")

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
                self.get_logger().info("Rover stationary. Executing detailed high-resolution inspection & measurement...")

        elif self._manager_state == "INSPECTING":
            # Keep rover stopped during measurement capture
            twist.linear.x = 0.0
            self._cmd_vel_pub.publish(twist)

            if (now - self._inspection_start_time) >= (1.0 + self._hold_duration):
                if self._auto_resume:
                    self._manager_state = "RESUMING"
                    self.get_logger().info("Inspection complete. Resuming track inspection...")
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
