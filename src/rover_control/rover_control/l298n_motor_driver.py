"""
L298N Real Motor Driver Interface for Raspberry Pi 5.

Uses `lgpio` library (native RPi 5 RP1 GPIO controller) to drive 
L298N H-Bridge direction (IN1, IN2, IN3, IN4) and PWM speed (ENA, ENB).
"""

import time
from rclpy.logging import get_logger

try:
    import lgpio
    HAS_LGPIO = True
except ImportError:
    HAS_LGPIO = False


class L298NMotorDriver:
    """Hardware L298N Motor Driver using lgpio on Raspberry Pi 5."""

    def __init__(
        self,
        ena_pin: int = 12,
        enb_pin: int = 13,
        in1_pin: int = 17,
        in2_pin: int = 27,
        in3_pin: int = 22,
        in4_pin: int = 23,
        pwm_freq: int = 1000,
        max_duty_cycle: float = 0.85,
    ) -> None:
        self._logger = get_logger("l298n_motor_driver")
        self._ena = ena_pin
        self._enb = enb_pin
        self._in1 = in1_pin
        self._in2 = in2_pin
        self._in3 = in3_pin
        self._in4 = in4_pin
        self._pwm_freq = pwm_freq
        self._max_duty = max_duty_cycle

        self._chip = None
        self._initialized = False

        if HAS_LGPIO:
            for chip_num in [4, 0]:
                try:
                    self._chip = lgpio.gpiochip_open(chip_num)
                    break
                except Exception:
                    continue
            if self._chip is not None:
                try:
                    # Claim direction output pins
                    for pin in [self._in1, self._in2, self._in3, self._in4]:
                        lgpio.gpio_claim_output(self._chip, pin, 0)
                    # Claim PWM enable pins
                    lgpio.gpio_claim_output(self._chip, self._ena, 0)
                    lgpio.gpio_claim_output(self._chip, self._enb, 0)
                    self._initialized = True
                    self._logger.info(
                        f"Successfully initialized L298N GPIO via lgpio on RPi 5 "
                        f"(chip={self._chip}, ENA={self._ena}, ENB={self._enb}, IN1-4={self._in1},{self._in2},{self._in3},{self._in4})"
                    )
                except Exception as e:
                    self._logger.warn(f"lgpio pin claiming failed: {e}")
                    self._initialized = False
            else:
                self._logger.warn("Failed to open gpiochip (tried 4 and 0). Running in dry-run mode.")
        else:
            self._logger.warn("lgpio library not found. Running in dry-run hardware mode.")

    def set_velocity(self, linear_velocity: float, angular_velocity: float) -> None:
        """
        Convert linear (m/s) & angular (rad/s) velocities to differential 
        wheel speeds and apply PWM + Direction to L298N H-Bridge.
        """
        track_width = 0.20
        v_left = linear_velocity - (angular_velocity * track_width / 2.0)
        v_right = linear_velocity + (angular_velocity * track_width / 2.0)

        max_speed = 0.5
        duty_left = min(1.0, max(-1.0, v_left / max_speed)) * self._max_duty
        duty_right = min(1.0, max(-1.0, v_right / max_speed)) * self._max_duty

        self._set_channel(duty_left, self._in1, self._in2, self._ena)
        self._set_channel(duty_right, self._in3, self._in4, self._enb)

    def _set_channel(self, duty: float, in_a: int, in_b: int, en_pin: int) -> None:
        """Set direction pins and PWM duty cycle for one L298N channel."""
        if not self._initialized or self._chip is None:
            return

        if abs(duty) > 0.001:
            # Map normalized duty to PWM percentage with starting torque floor
            # Scaled down by 70% to enable gentle, steady crawl speed along track (~20% PWM at 0.06 m/s)
            speed_pct = 15.0 + abs(duty) * 50.0
            speed_pct = min(100.0, max(0.0, speed_pct))
        else:
            speed_pct = 0.0

        if duty > 0.001:
            lgpio.gpio_write(self._chip, in_a, 1)
            lgpio.gpio_write(self._chip, in_b, 0)
            lgpio.tx_pwm(self._chip, en_pin, self._pwm_freq, speed_pct)
        elif duty < -0.001:
            lgpio.gpio_write(self._chip, in_a, 0)
            lgpio.gpio_write(self._chip, in_b, 1)
            lgpio.tx_pwm(self._chip, en_pin, self._pwm_freq, speed_pct)
        else:
            lgpio.gpio_write(self._chip, in_a, 0)
            lgpio.gpio_write(self._chip, in_b, 0)
            lgpio.tx_pwm(self._chip, en_pin, self._pwm_freq, 0.0)

    def stop(self) -> None:
        """Immediately stop all motor outputs."""
        if self._initialized and self._chip is not None:
            for pin in [self._in1, self._in2, self._in3, self._in4]:
                lgpio.gpio_write(self._chip, pin, 0)
            lgpio.tx_pwm(self._chip, self._ena, self._pwm_freq, 0.0)
            lgpio.tx_pwm(self._chip, self._enb, self._pwm_freq, 0.0)
        self._logger.info("L298N motor output stopped.")

    def cleanup(self) -> None:
        """Release GPIO resources."""
        self.stop()
        if self._initialized and self._chip is not None:
            try:
                lgpio.gpiochip_close(self._chip)
            except Exception:
                pass
            self._initialized = False
