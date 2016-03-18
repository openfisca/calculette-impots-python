# -*- coding: utf-8 -*-

import json
import math
import os
import pkg_resources

from toolz.curried import first

from . import core


"""Functions used by formulas"""


# M language functions


arr = round

inf = math.floor


def interval(first, last):
    return range(first, last + 1)


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


def cached(formula_function):
    formula_name = formula_function.__name__

    def cached_formula():
        if formula_name not in result_by_formula_name_cache:
            result = formula_function()
            result_by_formula_name_cache[formula_name] = result
        return result_by_formula_name_cache[formula_name]

    return cached_formula


# Dependencies helpres


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


def load_dependencies_by_formula_name():
    m_language_parser_dir_path = pkg_resources.get_distribution('m_language_parser').location
    variables_dependencies_file_path = os.path.join(m_language_parser_dir_path, 'json', 'data',
                                                    'formulas_dependencies.json')
    with open(variables_dependencies_file_path) as variables_dependencies_file:
        variables_dependencies_str = variables_dependencies_file.read()
    dependencies_by_formula_name = json.loads(variables_dependencies_str)
    return dependencies_by_formula_name


def has_dependency(formula_name, dependency_formula_names, dependencies_by_formula_name):
    def walk_dependencies(formula_name, visited_dependencies):
        if formula_name in visited_dependencies:
            return False
        visited_dependencies.add(formula_name)
        if formula_name in dependency_formula_names:
            return True
        formula_dependencies = dependencies_by_formula_name.get(formula_name)
        if formula_dependencies is not None:
            for dependency_name in formula_dependencies:
                if walk_dependencies(
                        visited_dependencies=visited_dependencies,
                        formula_name=dependency_name,
                        ):
                    return True
        return False

    return walk_dependencies(
        formula_name=formula_name,
        visited_dependencies=set(),
        )


def find_restituee_variables_depending_on(formula_names):
    dependencies_by_formula_name = load_dependencies_by_formula_name()
    restituee_variable_names = core.find_restituee_variables()
    return list(filter(
        lambda restituee_variable_name: has_dependency(
            formula_name=restituee_variable_name,
            dependency_formula_names=formula_names,
            dependencies_by_formula_name=dependencies_by_formula_name,
            ),
        restituee_variable_names,
        ))
