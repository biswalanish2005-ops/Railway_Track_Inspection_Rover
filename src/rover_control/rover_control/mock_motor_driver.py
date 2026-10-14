"""
Mock Motor Driver Interface for Railway Inspection Rover.

Abstracts hardware control and logs simulated motor commands.
Designed to be swapped for physical L298N GPIO/PWM driver in Phase 5
without changing higher-level motion control logic.
"""

from rclpy.logging import get_logger


class MockMotorDriver:
    """Simulated motor driver interface."""

    def __init__(self) -> None:
        self._logger = get_logger("mock_motor_driver")
        self._logger.info("Initialized Mock Motor Driver (Simulation Mode)")
        self.last_linear: float = 0.0
        self.last_angular: float = 0.0

    def set_velocity(self, linear_velocity: float, angular_velocity: float) -> None:
        """
        Log and store target simulated motor output.

        :param linear_velocity: Linear speed in m/s
        :param angular_velocity: Angular speed in rad/s
        """
        self.last_linear = linear_velocity
        self.last_angular = angular_velocity
        self._logger.debug(
            f"[MOCK MOTOR OUTPUT] Linear: {linear_velocity:+.3f} m/s | Angular: {angular_velocity:+.3f} rad/s"
        )

    def stop(self) -> None:
        """Immediately cut motor output signal."""
        self.last_linear = 0.0
        self.last_angular = 0.0
        self._logger.info("[MOCK MOTOR OUTPUT] Motor output disabled / Stopped (0.0 m/s)")
