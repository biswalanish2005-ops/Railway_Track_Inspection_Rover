"""
Launch File for Railway Crack Measurement System.

Launches:
- Crack Measurement Node (Physical scaling, skeletonization & JSON data storage)
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    crack_measurement_dir = get_package_share_directory("crack_measurement")
    params_file = os.path.join(
        crack_measurement_dir, "config", "measurement_params.yaml"
    )

    use_sim_time = LaunchConfiguration("use_sim_time", default="false")

    declare_use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="false",
        description="Use simulation time if true",
    )

    crack_measurement_node = Node(
        package="crack_measurement",
        executable="crack_measurement_node",
        name="crack_measurement_node",
        output="screen",
        parameters=[params_file, {"use_sim_time": use_sim_time}],
    )

    ld = LaunchDescription()
    ld.add_action(declare_use_sim_time)
    ld.add_action(crack_measurement_node)

    return ld
