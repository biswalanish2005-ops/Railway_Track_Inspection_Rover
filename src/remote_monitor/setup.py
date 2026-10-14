from glob import glob
import os
from setuptools import find_packages, setup

package_name = "remote_monitor"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="student",
    maintainer_email="student@todo.todo",
    description="Remote web monitoring interface package for Railway Inspection Rover",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "remote_monitor_node = remote_monitor.remote_monitor_node:main",
        ],
    },
)
