# -*- coding: utf-8 -*-


import importlib
import itertools

from .formulas_helpers import *  # noqa


saisies = None  # Global variable used by formulas, filled by `evaluate_formulas`


# Functional helpers


def mapcat(function, sequence):
    return itertools.chain.from_iterable(map(function, sequence))


# Core functions


def evaluate_formulas(variables_saisies=None):
    """
    Evaluate formulas and return results.
    Defer import of .generated.formulas module to inject `variables_saisies` in global variable.
    """
    if variables_saisies is None:
        variables_saisies = {}
    global saisies
    saisies = variables_saisies
    importlib.import_module(name='.generated.formulas', package='calculateur_impots')


def get_variable_type(variable_name):
    """Return variable type given its name or None if `variable_name` is not a variable."""
    from .generated.variables_definitions import variable_definition_by_name
    return variable_definition_by_name.get(variable_name, {}).get('type')
