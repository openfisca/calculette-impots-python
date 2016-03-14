# -*- coding: utf-8 -*-


from toolz import get_in


def get_variable_definition(variable_name, default=None):
    from .generated.variables_definitions import variable_definition_by_name
    return variable_definition_by_name.get(variable_name, default)


def get_variable_type(variable_name):
    """Return variable type given its name or None if `variable_name` is not a variable."""
    return get_variable_definition(variable_name, {}).get('type')


def is_constant(variable_name):
    from .generated import constants
    return variable_name in constants.__dict__


def is_base_variable(variable_name):
    return is_calculee_variable(variable_name) and \
        'base' in get_in(['attributes', 'tags'], get_variable_definition(variable_name, {}), default=[])


def is_calculee_variable(variable_name):
    return get_variable_type(variable_name) == 'variable_calculee'


def is_saisie_variable(variable_name):
    return get_variable_type(variable_name) == 'variable_saisie'
