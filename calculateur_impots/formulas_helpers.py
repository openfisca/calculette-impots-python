# -*- coding: utf-8 -*-


import math

from m_language_parser import dependencies_helpers
from toolz.curried import first

from . import core


"""Functions used by formulas"""


# M language functions


arr = round

inf = math.floor


def null(value):
    return int(value == 0)


def positif(value):
    return int(value > 0)


def positif_ou_nul(value):
    return int(value >= 0)


def present(value):
    return int(value != 0)


somme = sum


# Cache decorator

# FIXME Do not use a global variable.
result_by_formula_name_cache = {}


def cache_result(formula_function):
    formula_name = formula_function.__name__

    def new_formula_function():
        if formula_name not in result_by_formula_name_cache:
            result = formula_function()
            result_by_formula_name_cache[formula_name] = result
        return result_by_formula_name_cache[formula_name]

    return new_formula_function


def inspect():
    ok_variable_tuples = inspect_cache(predicate=lambda x: x == 2461)
    ok_variable_names = map(first, ok_variable_tuples)
    first_ok_variable_name = first(ok_variable_names)
    # import ipdb; ipdb.set_trace()
    return find_restituee_variables_depending_on(first_ok_variable_name)


def inspect_cache(predicate=None, restituee=False):
    return [
        (
            formula_name,
            result,
            core.get_variable_description(formula_name),
            core.get_variable_applications(formula_name),
            )
        for formula_name, result in result_by_formula_name_cache.items()
        if ((not restituee or core.is_restituee_variable(formula_name)) and
            # core.is_variable_in_application(formula_name, 'batch') and
            (predicate(result) if predicate is not None else True))
        ]


def find_restituee_variables_depending_on(formula_name):
    restituee_variables = core.find_restituee_variables()
    for restituee_variable in restituee_variables:
        formula_dependencies = []
        dependencies_helpers.build_formula_dependencies(
            formula_dependencies=formula_dependencies,
            formula_name=formula_name,
            )
    return formula_dependencies
