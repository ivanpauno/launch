#!/usr/bin/env python3

# Copyright 2019 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example of how to parse an xml."""

import xml.etree.ElementTree as ET
from pathlib import Path

from launch import LaunchDescription
from launch import LaunchService

from launch_frontend import parse_executable

from launch_ros import get_default_launch_description

from launch_xml import Entity


def main():
    """Parse node xml example."""
    tree = ET.parse(str(Path(__file__).parent / 'executable.xml'))
    root = tree.getroot()
    root_entity = Entity(root, type_name='executable', parent=None)
    executable = parse_executable(root_entity)
    ld = LaunchDescription()
    ld.add_action(executable)
    ls = LaunchService()
    ls.include_launch_description(get_default_launch_description())
    ls.include_launch_description(ld)
    return ls.run()


if __name__ == '__main__':
    main()