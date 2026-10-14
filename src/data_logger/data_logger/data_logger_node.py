"""
Data Logger Node for Railway Inspection Rover.

Logs all inspection events, rover state history, and telemetry to CSV summary table
and manages inspection data archives.
"""

import csv
from datetime import datetime
import os
from rclpy.node import Node
import rclpy
from rover_msgs.msg import CrackDetection, InspectionResult, RoverState


class DataLoggerNode(Node):
    """ROS 2 Data Logger Node."""

    def __init__(self) -> None:
        super().__init__("data_logger_node")

        self.declare_parameter("storage_directory", "inspection")
        self._storage_dir = str(self.get_parameter("storage_directory").value)
        os.makedirs(self._storage_dir, exist_ok=True)

        self._csv_path = os.path.join(self._storage_dir, "inspection_summary.csv")
        self._init_csv()

        # ROS 2 Subscribers
        self._state_sub = self.create_subscription(
            RoverState, "/rover_state", self._state_callback, 10
        )
        self._det_sub = self.create_subscription(
            CrackDetection, "/crack_detection", self._detection_callback, 10
        )
        self._result_sub = self.create_subscription(
            InspectionResult, "/inspection_result", self._result_callback, 10
        )

        self.get_logger().info(
            f"Data Logger initialized. Logging inspection summary to '{self._csv_path}'"
        )

    def _init_csv(self) -> None:
        """Initialize CSV header if file doesn't exist."""
        if not os.path.exists(self._csv_path):
            with open(self._csv_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "Timestamp",
                        "Inspection_ID",
                        "Confidence",
                        "Length_mm",
                        "Max_Width_mm",
                        "Avg_Width_mm",
                        "Apparent_Depth_mm",
                        "Severity",
                        "Saved_Path",
                    ]
                )

    def _state_callback(self, msg: RoverState) -> None:
        pass

    def _detection_callback(self, msg: CrackDetection) -> None:
        pass

    def _result_callback(self, msg: InspectionResult) -> None:
        """Append inspection record to CSV log file."""
        row = [
            datetime.now().isoformat(),
            msg.inspection_id,
            f"{msg.confidence:.3f}",
            f"{msg.crack_length_mm:.2f}",
            f"{msg.crack_max_width_mm:.2f}",
            f"{msg.crack_avg_width_mm:.2f}",
            f"{msg.apparent_depth_mm:.2f}",
            msg.severity_rating,
            msg.image_saved_path,
        ]

        try:
            with open(self._csv_path, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(row)
            self.get_logger().info(
                f"[CSV LOGGED] Recorded inspection {msg.inspection_id} to CSV summary."
            )
        except Exception as e:
            self.get_logger().error(f"Failed writing CSV record: {e}")


def main(args=None) -> None:
    rclpy.init(args=args)
    node = DataLoggerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
