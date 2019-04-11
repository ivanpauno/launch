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

"""Module for Parser methods."""

import launch

import launch_ros

from .entity import Entity


def get_attr_or_default(entity, attr, default_value):
    """Return the attr value of entity or default_value."""
    try:
        return entity.__getattr__(attr)
    except AttributeError:
        return default_value


def get_attr_or_none(entity, attr):
    """Return the attr value of entity or None."""
    return get_attr_or_default(entity, attr, None)


def str_to_bool(string):
    """Convert xs::boolean to python bool."""
    if not string:
        return None
    if string == 'true':
        return True
    if string == 'false':
        return False
    raise RuntimeError('Expected "true" or "false", got {}'.format(string))


def get_dictionary_from_key_value_pairs(pairs):
    """Get dictionary from key-value pairs."""
    if not pairs:
        return None
    return {pair.name: pair.value for pair in pairs}


def evaluate_predicate(predicate):
    """Evaluate a predicate to true or false."""
    # TODO(ivanpauno): Implement me please
    return True


def filtrate_with_predicates(items):
    """Filter out elements depending on predicate condition."""
    # TODO(ivanpauno): Implement me please.
    # ret = []
    # for item in items:
    #     if_predicate = get_attr_or_none(item, 'if')
    #     unless_predicate = get_attr_or_none(item, 'unless')
    #     if evaluate_predicate(if_predicate) and \
    #        not evaluate_predicate(unless_predicate):
    #         ret.append(item)
    # return ret
    return items


def parse_executable(entity: Entity):
    """Parse executable tag."""
    cmd = entity.cmd
    print(cmd)
    cwd = get_attr_or_none(entity, 'cwd')
    name = get_attr_or_none(entity, 'name')
    shell = str_to_bool(get_attr_or_none(entity, 'shell'))
    prefix = get_attr_or_none(entity, 'launch-prefix')
    output = get_attr_or_none(entity, 'output')
    args = get_attr_or_none(entity, 'args')
    print(args)
    args = args.split(' ') if args else []
    if not type(args) == list:
        args = [args]
    print(args)
    env = get_dictionary_from_key_value_pairs(
        filtrate_with_predicates(get_attr_or_none(entity, 'env')))
    if_predicate = get_attr_or_none(entity, 'if')
    unless_predicate = get_attr_or_none(entity, 'unless')

    cmd_list = [cmd]
    print(cmd_list)
    cmd_list.extend(args)
    print(cmd_list)
    return launch.actions.ExecuteProcess(
        cmd=cmd_list,
        cwd=cwd,
        env=env,
        name=name,
        shell=shell,
        prefix=prefix,
        output=output)

    # if evaluate_predicate(if_predicate) and not \
    #    evaluate_predicate(unless_predicate):
    #     cmd = [cmd].extend(args)
    #     return launch.ExecuteProcess(
    #         cmd=cmd,
    #         cwd=cwd,
    #         env=env,
    #         name=name,
    #         shell=shell,
    #         prefix=prefix,
    #         output=output)
    # return None


def get_remap_rules_from_remap_list(remap_list):
    """Convert from remap list to remap rules."""
    if not remap_list:
        return None
    return [(remap.__getattr__('from'), remap.to) for
            remap in remap_list]


def get_nested_dictionary_from_nested_key_value_pairs(params):
    """Convert nested params in a nested dictionary."""
    # TODO(ivanpauno): If our schema checking is not powerfull enough
    # this could easely end in an infinite loop.
    # In that case, we should do some extra formal checking before processing.
    param_dict = dict({})
    for param in params:
        if hasattr(param, 'value'):
            param_dict[param.name] = param.value
        else:
            param_dict.update(
                {param.name: get_nested_dictionary_from_nested_key_value_pairs(
                    param.param)})
    return param_dict


def normalize_parameters(params):
    """Normalize parameters as expected by Node construnctor argument."""
    if not params:
        return None
    normalized_params = []
    params_without_from = []
    for param in params:
        if hasattr(param, 'from'):
            # TODO(ivanpauno):
            # 'from' attribute ignores 'name' attribute,
            # is not accepted to be nested,
            # and it can not have childs.
            # The first two things could be supported,
            # if 'SomeParameters' accept a file nested in
            # a dictionary as a value.
            # I'm not handling error.
            # if our schema definition is not good enough to
            # recognize this problems, we should handle them
            # as errors.
            normalized_params.append(param.__getattr__('from'))
            continue
        if hasattr(param, 'name'):
            params_without_from.append(param)
            continue
        raise RuntimeError('name or from attributes are needed')
    normalized_params.append(
        get_nested_dictionary_from_nested_key_value_pairs(params_without_from))
    return normalized_params


def parse_node(entity: Entity):
    """Parse node tag."""
    package = entity.package
    executable = entity.executable
    name = get_attr_or_none(entity, 'name')
    ns = get_attr_or_none(entity, 'ns')
    prefix = get_attr_or_none(entity, 'launch-prefix')
    output = get_attr_or_none(entity, 'output')
    args = get_attr_or_none(entity, 'args')
    args = args.split(' ') if args else None
    env = get_dictionary_from_key_value_pairs(
        filtrate_with_predicates(get_attr_or_none(entity, 'env')))
    remappings = get_remap_rules_from_remap_list(
        get_attr_or_none(entity, 'remap'))
    parameters = normalize_parameters(get_attr_or_none(entity, 'param'))
    # TODO(ivanpauno): Handle if and unless attributes.
    print(package)
    print(executable)
    print(name)
    print(ns)
    print(prefix)
    print(output)
    print(args)
    print(env)
    print(remappings)
    print(parameters)

    return launch_ros.actions.Node(
        package=package,
        node_executable=executable,
        node_name=name,
        node_namespace=ns,
        prefix=prefix,
        output=output,
        arguments=args,
        env=env,
        remappings=remappings,
        parameters=parameters)
