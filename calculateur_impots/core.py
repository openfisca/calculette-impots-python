# -*- coding: utf-8 -*-


from . import __definitions__, __formulas__


VARIABLE_SAISIE_DEFAULT_VALUE = 0


def find_definition(variable_name):
    assert variable_name in __definitions__.variable_definition_by_name, \
        'Definition not found for variable "{}"'.format(variable_name)
    return __definitions__.variable_definition_by_name[variable_name]


def find_formula(variable_name):
    assert variable_name in __formulas__.__dict__, 'Formula not found for variable "{}"'.format(variable_name)
    return __formulas__.__dict__[variable_name]


class Simulation(object):
    def __init__(self, value_by_variable_name=None):
        self.value_by_variable_name = {} if value_by_variable_name is None else value_by_variable_name

    def calculate(self, variable_name):
        variable_definition = find_definition(variable_name)
        if variable_definition['type'] == 'variable_calculee':
            if variable_name not in self.value_by_variable_name:
                formula = find_formula(variable_name)
                self.value_by_variable_name[variable_name] = formula(self)
            value = self.value_by_variable_name[variable_name]
        elif variable_definition['type'] == 'variable_saisie':
            value = self.value_by_variable_name.get(variable_name, VARIABLE_SAISIE_DEFAULT_VALUE)
        else:
            raise NotImplementedError(variable_definition)
        return value

    # __call__ = calculate
