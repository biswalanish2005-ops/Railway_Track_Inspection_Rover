"""
System Launch File for Railway Inspection Rover (Phase 1 Simulation).

Launches:
- Robot State Publisher (with URDF)
- Rover State Manager
- Motor Controller (with parameter YAML)
- RViz2 Visualization (if GUI display available)
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    rover_description_dir = get_package_share_directory("rover_description")
    rover_control_dir = get_package_share_directory("rover_control")

    urdf_file = os.path.join(rover_description_dir, "urdf", "rover.urdf")
    if not os.path.exists(urdf_file):
        urdf_file = os.path.join(rover_description_dir, "urdf", "rover.urdf.xacro")

    with open(urdf_file, "r") as f:
        robot_description_content = f.read()

    rviz_config_file = os.path.join(rover_description_dir, "rviz", "rover_view.rviz")
    params_file = os.path.join(rover_control_dir, "config", "rover_control_params.yaml")

    use_sim_time = LaunchConfiguration("use_sim_time", default="false")

    declare_use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="false",
        description="Use simulation time if true",
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            {
                "use_sim_time": use_sim_time,
                "robot_description": robot_description_content,
            }
        ],
    )

    rover_state_manager_node = Node(
        package="rover_control",
        executable="rover_state_manager",
        name="rover_state_manager",
        output="screen",
        parameters=[{"use_sim_time": use_sim_time}],
    )

    motor_controller_node = Node(
        package="rover_control",
        executable="motor_controller",
        name="motor_controller",
        output="screen",
        parameters=[params_file, {"use_sim_time": use_sim_time}],
    )

    ld = LaunchDescription()
    ld.add_action(declare_use_sim_time)
    ld.add_action(robot_state_publisher_node)
    ld.add_action(rover_state_manager_node)
    ld.add_action(motor_controller_node)

    # Launch RViz if DISPLAY environment variable is present
    if os.environ.get("DISPLAY"):
        rviz_node = Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            output="screen",
            arguments=["-d", rviz_config_file],
            parameters=[{"use_sim_time": use_sim_time}],
        )
        ld.add_action(rviz_node)

    return ld
