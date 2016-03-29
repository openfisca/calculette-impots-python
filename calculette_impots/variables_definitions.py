# -*- coding: utf-8 -*-


from . import loaders


class VariablesDefinitions(object):
    """Query `variables_definitions.json` file in a more convenient way."""

    def __init__(self, constants=None, definition_by_variable_name=None):
        self.constants = constants or loaders.load_constants()
        self.definition_by_variable_name = definition_by_variable_name or loaders.load_variables_definitions()

    def filter_calculees(self, kind=None):
        return [
            variable_name
            for variable_name, definition in self.definition_by_variable_name.items()
            if self.is_calculee(variable_name, kind=kind)
            ]

    def get_description(self, variable_name, strict=False):
        default = None if strict else {}
        return self.definition_by_variable_name.get(variable_name, default).get('description')

    def get_type(self, variable_name, strict=False):
        default = None if strict else {}
        return self.definition_by_variable_name.get(variable_name, default).get('type')

    def is_calculee(self, variable_name, kind=None):
        return self.get_type(variable_name) == 'variable_calculee' and \
            (True if kind is None else self.definition_by_variable_name[variable_name].get(kind))

    def is_constant(self, variable_name):
        return variable_name in self.constants

    def is_saisie(self, variable_name):
        return self.get_type(variable_name) == 'variable_saisie'
