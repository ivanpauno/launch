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

from typing import Any
from typing import List
from typing import Optional
from typing import Text


class Entity:
    """Single item in the intermediate front_end representation."""

    def __init__(self, *,
                 type_name: Text = None,
                 parent: Optional['Entity'] = None) -> Text:
        """Construnctor."""
        self.__type_name = type_name
        self.__parent = parent
        self.__children = None

    @property
    def type_name(self) -> Text:
        """Get Entity type."""
        return self.__type_name

    @property
    def parent(self) -> Optional['Entity']:
        """Get Entity parent."""
        return self.__parent

    @property
    def children(self) -> Optional[List['Entity']]:
        """Get Entity children."""
        return self.__children

    def __getattr__(self, name: Text) -> Optional[Any]:
        """Get attribute."""
        raise NotImplementedError()
