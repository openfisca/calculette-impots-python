# -*- coding: utf-8 -*-


from toolz import get_in, keyfilter


def find_restituee_variables():
    from .generated.variables_definitions import variable_definition_by_name
    return keyfilter(is_restituee_variable, variable_definition_by_name).keys()


def get_variable_applications(variable_name):
    return get_variable_definition(variable_name, {}).get('applications')


def get_variable_definition(variable_name, default=None):
    from .generated.variables_definitions import variable_definition_by_name
    return variable_definition_by_name.get(variable_name, default)


def get_variable_description(variable_name):
    return get_variable_definition(variable_name, {}).get('description')


def get_variable_type(variable_name):
    """Return variable type given its name or None if `variable_name` is not a variable."""
    return get_variable_definition(variable_name, {}).get('type')


def has_tag(tag, variable_name):
    return tag in get_in(['attributes', 'tags'], get_variable_definition(variable_name, {}), default=[])


def is_constant(variable_name):
    from .generated import constants
    return variable_name in constants.__dict__


def is_base_variable(variable_name):
    return is_calculee_variable(variable_name) and has_tag('base', variable_name)


def is_calculee_variable(variable_name):
    return get_variable_type(variable_name) == 'variable_calculee'


def is_restituee_variable(variable_name):
    return is_calculee_variable(variable_name) and has_tag('restituee', variable_name)


def is_saisie_variable(variable_name):
    return get_variable_type(variable_name) == 'variable_saisie'


def is_variable_in_application(variable_name, application_name):
    return application_name in get_variable_definition(variable_name, {}).get('applications', [])
