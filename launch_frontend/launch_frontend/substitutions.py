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

"""Module for built-in front-end substitutions."""

from typing import Text

from launch import SomeSubstitutionsType
from launch.substitutions import EnvironmentVariable
from launch.substitutions import FindExecutable


def test(data):
    if len(data) > 1:
        raise AttributeError('Expected a len 1 list')
    return data[0]


def parse_list(string: Text):
    """Parse a list substitution."""
    if len(string) > 1:
        raise AttributeError('Expected a len 1 list.')
    string = string[0]
    pos = string.find('sep=')
    sep = ','
    if pos == 0:
        sep, string = string[4:].split(' ', 1)
    return string.split(sep)


def parse_find_executable(executable_name: SomeSubstitutionsType):
    """Return FindExecutable substitution."""
    return FindExecutable(executable_name)


def parse_env(data):
    """Return FindExecutable substitution."""
    if not data or len(data) > 2:
        raise AttributeError('env substitution expected 1 or 2 arguments')
    name = data[0]
    default = data[1] if len(data) == 2 else ''
    # print(name)
    # print(default)
    return EnvironmentVariable(name, default_value=default)


substitution_functions_dict = {
    'test': test,
    'list': parse_list,
    'env': parse_env}


def parse_substitutions(string):
    """Interpolate substitutions in a string."""
    # This scans from left to right. It pushes the position
    # of the opening brackets. When it finds a closing bracket
    # it pops and substitute.
    # The output is a list of substitutions and strings.
    subst_list = []
    pos = 0
    opening_brackets_pile = []
    last_substitution = dict({})
    while 1:
        ob = string.find('$(', pos)
        cb = string.find(')', pos)
        if ob >= 0 and ob < cb:
            # New opening bracket found
            if opening_brackets_pile:
                middle_string = None
                if pos > opening_brackets_pile[-1] + 2:
                    middle_string = string[pos:ob]
                else:
                    # Skip the key
                    _, middle_string = string[
                        opening_brackets_pile[-1]:ob].split(' ', 1)
                if middle_string:
                    try:
                        last_substitution[opening_brackets_pile[-1]].append(
                            middle_string)
                    except (TypeError, KeyError):
                        last_substitution[len(opening_brackets_pile)-1] = \
                            [middle_string]
                print(middle_string)
            opening_brackets_pile.append(ob)
            pos = ob + 2
            continue
        if cb >= 0:
            # New closing bracket found
            ob_pop = opening_brackets_pile.pop()
            subst_key, subst_value = string[ob_pop+2:cb].split(' ', 1)
            if subst_key not in substitution_functions_dict:
                # Unknown substitution
                raise RuntimeError(
                    'Invalid substitution type: {}'.format(subst_key))
            if len(opening_brackets_pile)+1 not in last_substitution:
                # Doesn't have a nested substitution inside.
                try:
                    last_substitution[len(opening_brackets_pile)].append(
                        substitution_functions_dict[subst_key]([subst_value]))
                except (TypeError, KeyError):
                    last_substitution[len(opening_brackets_pile)] = \
                        [substitution_functions_dict[subst_key]([subst_value])]
            else:
                # Have a nested substitution inside
                try:
                    last_substitution[len(opening_brackets_pile)].append(
                        substitution_functions_dict[subst_key](
                            last_substitution[len(opening_brackets_pile)+1]))
                except (TypeError, KeyError):
                    last_substitution[len(opening_brackets_pile)] = \
                        [substitution_functions_dict[subst_key](
                            last_substitution[len(opening_brackets_pile)+1])]
                del last_substitution[len(opening_brackets_pile)+1]
            if not opening_brackets_pile:
                # Is not nested inside other substitution
                subst_list.append(string[:ob_pop])
                subst_list.extend(last_substitution[0])
                string = string[cb+1:]
                pos = 0
                last_substitution = dict({})
            else:
                # Is still nested in other substitution
                pos = cb + 1
            continue
        if opening_brackets_pile:
            raise RuntimeError('Non matching substitution brackets.')
        return subst_list


if __name__ == '__main__':
    print(parse_substitutions('hola $(test como) $(test $(list 1,2,3)) $(env ads bsd)'))
