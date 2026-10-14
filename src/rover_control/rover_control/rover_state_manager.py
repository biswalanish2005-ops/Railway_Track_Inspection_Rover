"""
Rover State Manager Node for Railway Inspection Rover.

Manages rover high-level state machine, emergency stop service handling,
and system status publishing.
"""

from geometry_msgs.msg import TwistStamped
import rclpy
from rclpy.node import Node
from rover_msgs.msg import RoverState
from rover_msgs.srv import EmergencyStop


class RoverStateManagerNode(Node):
    """ROS 2 Node for high-level rover state machine and safety management."""

    def __init__(self) -> None:
        super().__init__("rover_state_manager")

        # State Variables
        self._current_state: str = "IDLE"
        self._emergency_stop_active: bool = False
        self._motor_enabled: bool = True
        self._watchdog_active: bool = False
        self._status_message: str = "System Initialized. Ready in IDLE state."

        self._actual_linear_speed: float = 0.0
        self._actual_angular_speed: float = 0.0
        self._requested_linear_speed: float = 0.0
        self._requested_angular_speed: float = 0.0

        # ROS 2 Publisher
        self._state_pub = self.create_publisher(RoverState, "/rover_state", 10)

        # ROS 2 Subscriber for Motor Feedback
        self._motor_status_sub = self.create_subscription(
            TwistStamped, "/motor_status", self._motor_status_callback, 10
        )

        # ROS 2 Service for Emergency Stop / Reset
        self._estop_service = self.create_service(
            EmergencyStop, "/emergency_stop", self._handle_emergency_stop
        )

        # State Publishing Timer (10 Hz)
        self.create_timer(0.1, self._publish_state)

        self.get_logger().info("Rover State Manager started successfully.")

    def _handle_emergency_stop(
        self, request: EmergencyStop.Request, response: EmergencyStop.Response
    ) -> EmergencyStop.Response:
        """Process Emergency Stop / Reset requests."""
        if request.set_estop:
            self._emergency_stop_active = True
            self._motor_enabled = False
            self._current_state = "STOPPED"
            self._status_message = f"E-STOP ACTIVATED: {request.reason}"
            self.get_logger().error(f"EMERGENCY STOP TRIGGERED! Reason: {request.reason}")
            response.success = True
            response.message = "Emergency stop activated. Motors disabled."
        else:
            self._emergency_stop_active = False
            self._motor_enabled = False  # Explicit reset required before movement
            self._current_state = "IDLE"
            self._status_message = f"E-STOP CLEARED: {request.reason}. System returned to IDLE."
            self.get_logger().info("Emergency stop cleared. Rover set to IDLE (motors safe).")
            response.success = True
            response.message = "Emergency stop cleared. System in IDLE state."

        return response

    def _motor_status_callback(self, msg: TwistStamped) -> None:
        """Receive motor status telemetry (linear.x = actual, linear.y = requested, angular.z = watchdog flag)."""
        self._actual_linear_speed = msg.twist.linear.x
        self._actual_angular_speed = msg.twist.angular.z
        self._requested_linear_speed = msg.twist.linear.y
        self._requested_angular_speed = msg.twist.angular.y
        self._watchdog_active = bool(msg.twist.linear.z > 0.5)

        # Execute state machine transition rules
        self._update_state_machine()

    def _update_state_machine(self) -> None:
        """Evaluate state transitions based on velocity, watchdog, and safety state."""
        if self._emergency_stop_active:
            self._current_state = "STOPPED"
            return

        is_moving_requested = (
            abs(self._requested_linear_speed) > 0.001
            or abs(self._requested_angular_speed) > 0.001
        )
        is_moving_actual = (
            abs(self._actual_linear_speed) > 0.001
            or abs(self._actual_angular_speed) > 0.001
        )

        if self._current_state in ("IDLE", "STOPPED"):
            if is_moving_requested and not self._watchdog_active:
                self._current_state = "MOVING"
                self._motor_enabled = True
                self._status_message = "Rover moving on commanded speed."
            else:
                if self._current_state != "STOPPED":
                    self._current_state = "IDLE"

        elif self._current_state == "MOVING":
            if not is_moving_requested or self._watchdog_active:
                self._current_state = "SLOWING"
                self._status_message = (
                    "Rover slowing down (command zeroed or watchdog triggered)."
                )

        elif self._current_state == "SLOWING":
            if not is_moving_actual:
                self._current_state = "IDLE"
                self._status_message = "Rover came to complete stop. System IDLE."
            elif is_moving_requested and not self._watchdog_active:
                self._current_state = "MOVING"
                self._status_message = "Rover resuming movement."

    def _publish_state(self) -> None:
        """Publish current rover state message."""
        msg = RoverState()
        msg.timestamp = self.get_clock().now().to_msg()
        msg.current_state = self._current_state
        msg.current_linear_speed = float(self._actual_linear_speed)
        msg.current_angular_speed = float(self._actual_angular_speed)
        msg.emergency_stop_active = self._emergency_stop_active
        msg.motor_enabled = self._motor_enabled
        msg.watchdog_active = self._watchdog_active
        msg.status_message = self._status_message

        self._state_pub.publish(msg)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = RoverStateManagerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
