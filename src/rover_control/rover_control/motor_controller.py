"""
Motor Controller Node for Railway Inspection Rover.

Subscribes to /cmd_vel, enforces velocity limits, applies acceleration/deceleration ramping,
implements command watchdog timeout, and interfaces with MockMotorDriver.
"""

import math
from geometry_msgs.msg import Twist, TwistStamped
import rclpy
from rclpy.node import Node

from rover_control.l298n_motor_driver import L298NMotorDriver
from rover_control.mock_motor_driver import MockMotorDriver
from rover_msgs.msg import RoverState


class MotorControllerNode(Node):
    """ROS 2 Motor Controller Node with velocity ramping and watchdog."""

    def __init__(self) -> None:
        super().__init__("motor_controller")

        # Declare ROS Parameters
        self.declare_parameter("max_linear_speed", 0.5)
        self.declare_parameter("max_angular_speed", 1.0)
        self.declare_parameter("acceleration_limit", 0.2)
        self.declare_parameter("deceleration_limit", 0.4)
        self.declare_parameter("cmd_timeout", 0.5)
        self.declare_parameter("control_frequency", 20.0)
        self.declare_parameter("use_simulated_motors", True)

        # Get ROS Parameters
        self._max_linear_speed = float(
            self.get_parameter("max_linear_speed").value
        )
        self._max_angular_speed = float(
            self.get_parameter("max_angular_speed").value
        )
        self._acceleration_limit = float(
            self.get_parameter("acceleration_limit").value
        )
        self._deceleration_limit = float(
            self.get_parameter("deceleration_limit").value
        )
        self._cmd_timeout = float(self.get_parameter("cmd_timeout").value)
        self._control_frequency = float(
            self.get_parameter("control_frequency").value
        )
        self._use_simulated_motors = bool(
            self.get_parameter("use_simulated_motors").value
        )

        # Driver abstraction
        if self._use_simulated_motors:
            self._motor_driver = MockMotorDriver()
        else:
            self._motor_driver = L298NMotorDriver()

        # Velocity State Variables
        self.requested_linear_velocity: float = 0.0
        self.requested_angular_velocity: float = 0.0
        self.actual_linear_velocity: float = 0.0
        self.actual_angular_velocity: float = 0.0

        # Safety & Watchdog State
        self._last_cmd_time = self.get_clock().now()
        self._watchdog_active: bool = False
        self._emergency_stop_active: bool = False

        # ROS 2 Subscribers
        self._cmd_vel_sub = self.create_subscription(
            Twist, "/cmd_vel", self._cmd_vel_callback, 10
        )
        self._rover_state_sub = self.create_subscription(
            RoverState, "/rover_state", self._rover_state_callback, 10
        )

        # ROS 2 Publisher for Telemetry / Feedback
        self._status_pub = self.create_publisher(
            TwistStamped, "/motor_status", 10
        )

        # Control Loop Timer
        timer_period = 1.0 / self._control_frequency
        self.create_timer(timer_period, self._control_loop)

        self.get_logger().info(
            f"Motor Controller initialized (Max linear: {self._max_linear_speed}m/s, "
            f"Max angular: {self._max_angular_speed}rad/s, Accel: {self._acceleration_limit}m/s², "
            f"Decel: {self._deceleration_limit}m/s², Timeout: {self._cmd_timeout}s)"
        )

    def _cmd_vel_callback(self, msg: Twist) -> None:
        """Callback for incoming /cmd_vel Twist messages."""
        if self._emergency_stop_active:
            self.get_logger().warn(
                "Received /cmd_vel command while EMERGENCY STOP is active. Ignoring."
            )
            return

        # Sanitize and clamp requested speeds
        raw_linear = msg.linear.x
        raw_angular = msg.angular.z

        self.requested_linear_velocity = max(
            -self._max_linear_speed, min(self._max_linear_speed, raw_linear)
        )
        self.requested_angular_velocity = max(
            -self._max_angular_speed, min(self._max_angular_speed, raw_angular)
        )

        self._last_cmd_time = self.get_clock().now()

        if self._watchdog_active:
            self._watchdog_active = False
            self.get_logger().info(
                "Command watchdog cleared by new /cmd_vel message."
            )

    def _rover_state_callback(self, msg: RoverState) -> None:
        """Callback for system state updates from state manager."""
        self._emergency_stop_active = msg.emergency_stop_active
        if self._emergency_stop_active:
            # Immediate cut on E-stop
            self.requested_linear_velocity = 0.0
            self.requested_angular_velocity = 0.0
            self.actual_linear_velocity = 0.0
            self.actual_angular_velocity = 0.0
            self._motor_driver.stop()

    def _control_loop(self) -> None:
        """Main velocity ramping and motor update loop."""
        now = self.get_clock().now()
        dt = 1.0 / self._control_frequency

        # Check Watchdog Timeout
        time_since_last_cmd = (now - self._last_cmd_time).nanoseconds / 1e9
        if time_since_last_cmd > self._cmd_timeout:
            if not self._watchdog_active:
                self._watchdog_active = True
                self.get_logger().warn(
                    f"Watchdog active: No /cmd_vel received for {time_since_last_cmd:.2f}s (> {self._cmd_timeout}s). Ramping down."
                )
            self.requested_linear_velocity = 0.0
            self.requested_angular_velocity = 0.0

        # Handle Emergency Stop state
        if self._emergency_stop_active:
            self.actual_linear_velocity = 0.0
            self.actual_angular_velocity = 0.0
            self._motor_driver.stop()
            self._publish_status()
            return

        # Calculate ramped velocity towards requested target
        self.actual_linear_velocity = self._ramp_velocity(
            current=self.actual_linear_velocity,
            target=self.requested_linear_velocity,
            dt=dt,
        )
        self.actual_angular_velocity = self._ramp_velocity(
            current=self.actual_angular_velocity,
            target=self.requested_angular_velocity,
            dt=dt,
        )

        # Output to Motor Driver (Simulated / Mock)
        self._motor_driver.set_velocity(
            self.actual_linear_velocity, self.actual_angular_velocity
        )

        # Publish Telemetry Feedback
        self._publish_status()

    def _ramp_velocity(
        self, current: float, target: float, dt: float
    ) -> float:
        """Apply acceleration/deceleration ramping to target velocity."""
        if math.isclose(current, target, abs_tol=1e-4):
            return target

        diff = target - current

        # Determine if speed magnitude is increasing (acceleration) or decreasing (deceleration)
        if (current >= 0.0 and diff > 0.0) or (current <= 0.0 and diff < 0.0):
            rate = self._acceleration_limit
        else:
            rate = self._deceleration_limit

        max_step = rate * dt

        if abs(diff) <= max_step:
            return target

        return current + math.copysign(max_step, diff)

    def _publish_status(self) -> None:
        """Publish status message containing actual, requested speeds and watchdog state."""
        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.twist.linear.x = float(self.actual_linear_velocity)
        msg.twist.linear.y = float(self.requested_linear_velocity)
        msg.twist.linear.z = 1.0 if self._watchdog_active else 0.0
        msg.twist.angular.z = float(self.actual_angular_velocity)
        msg.twist.angular.y = float(self.requested_angular_velocity)
        self._status_pub.publish(msg)

    def destroy_node(self) -> None:
        """Clean shutdown hook to stop motors."""
        self.get_logger().info("Shutting down Motor Controller Node. Stopping motors...")
        self._motor_driver.stop()
        super().destroy_node()


def main(args=None) -> None:
    rclpy.init(args=args)
    node = MotorControllerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
