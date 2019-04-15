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

"""Module for Entity class."""

from typing import Text
from xml.etree.ElementTree import Element

import launch_frontend


class Entity(launch_frontend.Entity):
    """Single item in the intermediate XML front_end representation."""

    def __init__(self, xml_element: Element, **kwargs) -> Text:
        """Construnctor."""
        super().__init__(**kwargs)
        self.__xml_element = xml_element

    def __getattr__(self, name):
        """Abstraction of how to access the xml tree."""
        if name in self.__attributes:
            return self.__attributes[name]
        return_list = []
        for child in self.__xml_element:
            if child.tag == name:
                return_list.append(
                    Entity(child,
                           type_name=child.tag,
                           parent=self.__xml_element))
        if not return_list:
            raise AttributeError(
                'Can not find attribute {} in Entity {}'.format(
                    name, self.__type_name))
        return return_list
