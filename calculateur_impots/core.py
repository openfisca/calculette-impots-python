# -*- coding: utf-8 -*-


import inspect
import logging

from . import formulas
from .generated.variables_definitions import variable_definition_by_name


log = logging.getLogger(__name__)


VARIABLE_SAISIE_DEFAULT_VALUE = 0


def find_definition(variable_name):
    assert variable_name in variable_definition_by_name, \
        'Definition not found for variable "{}"'.format(variable_name)
    return variable_definition_by_name[variable_name]


def find_formula(variable_name):
    return formulas.__dict__.get(variable_name)


def has_tag(tag, variable_definition):
    return tag in variable_definition.get('attributes', {}).get('tags', [])


def interval(first, last):
    return range(first, last + 1)


def load_environment():
    formulas.load_formulas()


class Simulation(object):
    def __init__(self, value_by_variable_name=None):
        self.value_by_variable_name = {} if value_by_variable_name is None else value_by_variable_name

    def calculate(self, variable_name):
        variable_definition = find_definition(variable_name)
        if variable_definition['type'] == 'variable_calculee':
            if variable_name not in self.value_by_variable_name:
                formula = find_formula(variable_name)
                if formula is None:
                    error_message = 'Formula not found for variable "{}"'.format(variable_name)
                    if has_tag('base', variable_definition):
                        log.warning(error_message + ' => use value 0')
                        value = 0
                    else:
                        raise ValueError(error_message)
                else:
                    formula_args_names = inspect.getargspec(formula).args
                    formula_args = list(map(self.calculate, formula_args_names))
                    value = formula(*formula_args)
                self.value_by_variable_name[variable_name] = value
            value = self.value_by_variable_name[variable_name]
        elif variable_definition['type'] == 'variable_saisie':
            value = self.value_by_variable_name.get(variable_name, VARIABLE_SAISIE_DEFAULT_VALUE)
        else:
            raise NotImplementedError(variable_definition)
        return value
