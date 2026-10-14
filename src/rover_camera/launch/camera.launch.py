"""
Camera Launch File for Railway Inspection Rover.

Launches:
- Camera Publisher Node (Hardware / Sim)
- Image Processor Node (Calibration, Undistortion, IPM, Overlays)
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    rover_camera_dir = get_package_share_directory("rover_camera")
    params_file = os.path.join(rover_camera_dir, "config", "camera_params.yaml")

    use_sim_time = LaunchConfiguration("use_sim_time", default="false")

    declare_use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="false",
        description="Use simulation time if true",
    )

    # 1. Camera Publisher Node
    camera_publisher_node = Node(
        package="rover_camera",
        executable="camera_publisher",
        name="camera_publisher",
        output="screen",
        parameters=[params_file, {"use_sim_time": use_sim_time}],
    )

    # 2. Image Processor Node
    image_processor_node = Node(
        package="rover_camera",
        executable="image_processor",
        name="image_processor",
        output="screen",
        parameters=[params_file, {"use_sim_time": use_sim_time}],
    )

    ld = LaunchDescription()
    ld.add_action(declare_use_sim_time)
    ld.add_action(camera_publisher_node)
    ld.add_action(image_processor_node)

    return ld
