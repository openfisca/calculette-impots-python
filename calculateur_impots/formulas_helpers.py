# -*- coding: utf-8 -*-


import math

from m_language_parser import dependencies_helpers
from toolz.curried import first

from . import core
from .generated.variables_definitions import definition_by_variable_name


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
            # if result == 10561.16:
                # print(formula_name + ' == 10561.16')
                # import ipdb; ipdb.set_trace()
            result_by_formula_name_cache[formula_name] = result
        return result_by_formula_name_cache[formula_name]

    return new_formula_function


def inspect():
    ok_variable_tuples = inspect_cache(predicate=lambda x: x == 2461)
    ok_variable_names = list(map(first, ok_variable_tuples))
    print('restituee variables in batch depending on one of {}: {}'.format(
        ok_variable_names,
        '\n'.join(
            '{} {!r}'.format(
                formula_name,
                core.get_variable_description(formula_name),
                )
            for formula_name in filter(
                core.is_batch,
                find_restituee_variables_depending_on(ok_variable_names),
                )
            ) + '\n',
        ))


def inspect_cache(predicate=None):
    return [
        (
            formula_name,
            result,
            core.get_variable_description(formula_name),
            core.get_variable_applications(formula_name),
            )
        for formula_name, result in sorted(result_by_formula_name_cache.items())
        if (predicate(result) if predicate is not None else True)
        ]


def has_dependency(formula_name, dependency_formula_names, dependencies_by_formula_name):
    def walk_dependencies(formula_name, dependencies):
        if formula_name in dependencies:
            return False
        dependencies.add(formula_name)
        if formula_name in dependency_formula_names:
            return True
        formula_dependencies = dependencies_by_formula_name.get(formula_name)
        if formula_dependencies is not None:
            for dependency_name in formula_dependencies:
                if walk_dependencies(
                        dependencies=dependencies,
                        formula_name=dependency_name,
                        ):
                    return True
        return False

    return walk_dependencies(
        dependencies=set(),
        formula_name=formula_name,
        )


def find_restituee_variables_depending_on(formula_names):
    dependencies_by_formula_name = dependencies_helpers.load_dependencies_by_formula_name()
    # formulas_dependencies_by_formula_name = dependencies_helpers.filter_formulas_dependencies(
    #     definition_by_variable_name=definition_by_variable_name,
    #     dependencies_by_formula_name=dependencies_by_formula_name,
    #     )
    restituee_variable_names = core.find_restituee_variables()
    return list(filter(
        lambda restituee_variable_name: has_dependency(
            formula_name=restituee_variable_name,
            dependency_formula_names=formula_names,
            dependencies_by_formula_name=dependencies_by_formula_name,
            ),
        restituee_variable_names,
        ))
