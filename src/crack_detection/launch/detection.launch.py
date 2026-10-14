"""
Launch File for Railway Crack Detection System.

Launches:
- Crack Detection Node (ML Model inference & visualization)
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    crack_detection_dir = get_package_share_directory("crack_detection")
    params_file = os.path.join(
        crack_detection_dir, "config", "crack_detection_params.yaml"
    )

    use_sim_time = LaunchConfiguration("use_sim_time", default="false")

    declare_use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="false",
        description="Use simulation time if true",
    )

    crack_detection_node = Node(
        package="crack_detection",
        executable="crack_detection_node",
        name="crack_detection_node",
        output="screen",
        parameters=[params_file, {"use_sim_time": use_sim_time}],
    )

    ld = LaunchDescription()
    ld.add_action(declare_use_sim_time)
    ld.add_action(crack_detection_node)

    return ld
