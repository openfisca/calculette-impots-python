# -*- coding: utf-8 -*-


import importlib

from toolz import keyfilter

from .formulas_helpers import *  # noqa


saisies = None  # Global variable used by formulas, filled by `evaluate_formulas`


# Core functions


def evaluate_formulas(variables_saisies=None):
    """
    Evaluate formulas and return results.
    Defer import of .generated.formulas module to inject `variables_saisies` in global variable.
    """
    from .generated.variables_definitions import variable_definition_by_name
    if variables_saisies is None:
        variables_saisies = {}
    global saisies
    saisies = variables_saisies
    formulas_module = importlib.import_module(name='.generated.formulas', package='calculateur_impots')
    variables_calculees = keyfilter(
        lambda key: key in variable_definition_by_name,
        formulas_module.__dict__,
        )
    return variables_calculees


def get_variable_type(variable_name):
    """Return variable type given its name or None if `variable_name` is not a variable."""
    from .generated.variables_definitions import variable_definition_by_name
    return variable_definition_by_name.get(variable_name, {}).get('type')
