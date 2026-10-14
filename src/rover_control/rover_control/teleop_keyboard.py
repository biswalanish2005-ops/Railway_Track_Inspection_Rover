"""
Keyboard Teleoperation Node for Railway Inspection Rover.

Allows manual teleoperation while strictly routing all commands through
/cmd_vel and calling the /emergency_stop service.
"""

import select
import sys
import termios
import tty
from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node
from rover_msgs.srv import EmergencyStop

USAGE_INSTRUCTIONS = """
======================================================
  Railway Rover Keyboard Teleoperation Interface
======================================================
  W : Forward (+0.1 m/s)
  S : Reverse (-0.1 m/s)
  A : Turn Left (+0.2 rad/s)
  D : Turn Right (-0.2 rad/s)
  K / X : Stop / Zero velocity
  SPACE : Trigger Emergency Stop
  R : Reset / Clear Emergency Stop
  Q / Ctrl+C : Quit Teleop
======================================================
"""


def get_key(settings) -> str:
    """Read single character keypress from stdin in raw mode."""
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ""
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


class TeleopKeyboardNode(Node):
    """ROS 2 Teleoperation Node."""

    def __init__(self) -> None:
        super().__init__("teleop_keyboard")

        self._cmd_vel_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self._estop_client = self.create_client(EmergencyStop, "/emergency_stop")

        self._target_linear: float = 0.0
        self._target_angular: float = 0.0

        self.get_logger().info("Keyboard Teleoperation initialized.")

    def send_estop(self, set_estop: bool, reason: str) -> None:
        """Call emergency stop service asynchronously."""
        if not self._estop_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().error("Emergency Stop service not available!")
            return

        req = EmergencyStop.Request()
        req.set_estop = set_estop
        req.reason = reason

        future = self._estop_client.call_async(req)
        future.add_done_callback(
            lambda f: self.get_logger().info(
                f"Service response: {f.result().message}"
            )
        )

    def publish_twist(self) -> None:
        """Publish current target Twist command."""
        twist = Twist()
        twist.linear.x = float(self._target_linear)
        twist.angular.z = float(self._target_angular)
        self._cmd_vel_pub.publish(twist)


def main(args=None) -> None:
    settings = termios.tcgetattr(sys.stdin)
    rclpy.init(args=args)
    node = TeleopKeyboardNode()

    print(USAGE_INSTRUCTIONS)

    try:
        while rclpy.ok():
            key = get_key(settings)

            if key.lower() == "w":
                node._target_linear += 0.1
                print(f"\rSpeed: Linear={node._target_linear:.2f} m/s, Angular={node._target_angular:.2f} rad/s    ", end="")
            elif key.lower() == "s":
                node._target_linear -= 0.1
                print(f"\rSpeed: Linear={node._target_linear:.2f} m/s, Angular={node._target_angular:.2f} rad/s    ", end="")
            elif key.lower() == "a":
                node._target_angular += 0.2
                print(f"\rSpeed: Linear={node._target_linear:.2f} m/s, Angular={node._target_angular:.2f} rad/s    ", end="")
            elif key.lower() == "d":
                node._target_angular -= 0.2
                print(f"\rSpeed: Linear={node._target_linear:.2f} m/s, Angular={node._target_angular:.2f} rad/s    ", end="")
            elif key.lower() in ("k", "x"):
                node._target_linear = 0.0
                node._target_angular = 0.0
                print("\rVelocity zeroed.                                                        ", end="")
            elif key == " ":
                node._target_linear = 0.0
                node._target_angular = 0.0
                node.send_estop(True, "Keyboard Spacebar Pressed")
                print("\n[E-STOP TRIGGERED]")
            elif key.lower() == "r":
                node.send_estop(False, "Keyboard R Pressed")
                print("\n[E-STOP CLEARED / RESET]")
            elif key.lower() == "q" or key == "\x03":
                break

            node.publish_twist()
            rclpy.spin_once(node, timeout_sec=0.01)

    except Exception as e:
        print(f"\nTeleop exception: {e}")
    finally:
        node.publish_twist()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
