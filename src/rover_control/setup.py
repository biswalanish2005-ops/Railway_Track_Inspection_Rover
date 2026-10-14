from glob import glob
import os
from setuptools import find_packages, setup

package_name = "rover_control"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "config"), glob("config/*.yaml")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="student",
    maintainer_email="student@todo.todo",
    description="Control and state management nodes for Railway Inspection Rover",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "motor_controller = rover_control.motor_controller:main",
            "rover_state_manager = rover_control.rover_state_manager:main",
            "teleop_keyboard = rover_control.teleop_keyboard:main",
        ],
    },
)
