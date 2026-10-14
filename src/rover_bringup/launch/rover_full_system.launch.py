"""
Full Autonomous System Launch File for Railway Inspection Rover (Phase 5).

Brings up all perception, ML detection, measurement, motion control, state management,
data logging, remote web dashboard, and RViz visualization nodes concurrently.
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    # Directories
    rover_bringup_dir = get_package_share_directory("rover_bringup")
    rover_description_dir = get_package_share_directory("rover_description")
    rover_control_dir = get_package_share_directory("rover_control")
    rover_camera_dir = get_package_share_directory("rover_camera")
    crack_det_dir = get_package_share_directory("crack_detection")
    crack_meas_dir = get_package_share_directory("crack_measurement")
    insp_mgr_dir = get_package_share_directory("inspection_manager")

    # Parameters
    control_params = os.path.join(rover_control_dir, "config", "rover_control_params.yaml")
    camera_params = os.path.join(rover_camera_dir, "config", "camera_params.yaml")
    det_params = os.path.join(crack_det_dir, "config", "crack_detection_params.yaml")
    meas_params = os.path.join(crack_meas_dir, "config", "measurement_params.yaml")
    insp_params = os.path.join(insp_mgr_dir, "config", "inspection_manager_params.yaml")

    # URDF & RViz Config
    urdf_file = os.path.join(rover_description_dir, "urdf", "rover.urdf")
    with open(urdf_file, "r") as f:
        robot_description_content = f.read()

    rviz_config = os.path.join(rover_description_dir, "rviz", "rover_view.rviz")
    use_sim_time = LaunchConfiguration("use_sim_time", default="false")

    ld = LaunchDescription()

    # 1. Robot State Publisher
    ld.add_action(
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            output="screen",
            parameters=[{"robot_description": robot_description_content}],
        )
    )

    # 2. Rover State Manager
    ld.add_action(
        Node(
            package="rover_control",
            executable="rover_state_manager",
            name="rover_state_manager",
            output="screen",
        )
    )

    # 3. Motor Controller
    ld.add_action(
        Node(
            package="rover_control",
            executable="motor_controller",
            name="motor_controller",
            output="screen",
            parameters=[control_params],
        )
    )

    # 4. Camera Publisher
    ld.add_action(
        Node(
            package="rover_camera",
            executable="camera_publisher",
            name="camera_publisher",
            output="screen",
            parameters=[camera_params],
        )
    )

    # 5. Image Processor (Undistortion, IPM, CLAHE)
    ld.add_action(
        Node(
            package="rover_camera",
            executable="image_processor",
            name="image_processor",
            output="screen",
            parameters=[camera_params],
        )
    )

    # 6. ML Crack Detection Node
    ld.add_action(
        Node(
            package="crack_detection",
            executable="crack_detection_node",
            name="crack_detection_node",
            output="screen",
            parameters=[det_params],
        )
    )

    # 7. Crack Measurement Node
    ld.add_action(
        Node(
            package="crack_measurement",
            executable="crack_measurement_node",
            name="crack_measurement_node",
            output="screen",
            parameters=[meas_params],
        )
    )

    # 8. Inspection Manager Node
    ld.add_action(
        Node(
            package="inspection_manager",
            executable="inspection_manager_node",
            name="inspection_manager_node",
            output="screen",
            parameters=[insp_params],
        )
    )

    # 9. Data Logger Node
    ld.add_action(
        Node(
            package="data_logger",
            executable="data_logger_node",
            name="data_logger_node",
            output="screen",
        )
    )

    # 10. Remote Web Monitor Node
    ld.add_action(
        Node(
            package="remote_monitor",
            executable="remote_monitor_node",
            name="remote_monitor_node",
            output="screen",
        )
    )

    # 11. RViz2 (if DISPLAY environment variable present)
    if os.environ.get("DISPLAY"):
        ld.add_action(
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                output="screen",
                arguments=["-d", rviz_config],
            )
        )

    return ld
