# -*- coding: utf-8 -*-


"""Functions to load JSON files distributed with this package."""


import json
import os
import pkg_resources

from toolz.curried import map, pipe


m_language_parser_dir_path = pkg_resources.get_distribution('calculette_impots_m_language_parser').location
json_dir_path = os.path.join(m_language_parser_dir_path, 'json')


# Functions to load data


def load_constants():
    return load_json(os.path.join(json_dir_path, 'constants.json'))


def load_errors_definitions():
    """Return `definition_by_error_name` dict from the file `errH.json`."""
    return pipe(
        load_json(os.path.join(json_dir_path, 'ast', 'errH.json')),
        map(lambda d: (d['name'], d)),  # Index by name and keep singleton value (groupby creates list values)
        dict,
        )


def load_formulas_dependencies():
    """Return `dependencies_by_formula_name` dict from the file `formulas_dependencies.json`."""
    return load_json(os.path.join(json_dir_path, 'formulas_dependencies.json'))


def load_json(file_path):
    with open(file_path) as file:
        file_str = file.read()
    return json.loads(file_str)


def load_variables_definitions():
    """Return `definition_by_variable_name` dict from the file `variables_definitions.json`."""
    return load_json(os.path.join(json_dir_path, 'variables_definitions.json'))
