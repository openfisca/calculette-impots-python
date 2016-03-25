# -*- coding: utf-8 -*-


from . import loaders

from toolz.curried import keyfilter


class VariablesDefinitions(object):
    """Query `variables_definitions.json` file in a more convenient way."""

    def __init__(self, constants=None, definition_by_variable_name=None):
        self.constants = constants or loaders.load_constants()
        self.definition_by_variable_name = definition_by_variable_name or loaders.load_variables_definitions()

    def filter_by_subtype(self, subtype):
        return list(keyfilter(
            lambda variable_name: self.has_subtype(variable_name, subtype),
            self.definition_by_variable_name,
            ).keys())

    def get_description(self, variable_name, strict=False):
        default = None if strict else {}
        return self.definition_by_variable_name.get(variable_name, default).get('description')

    def get_type(self, variable_name, strict=False):
        default = None if strict else {}
        return self.definition_by_variable_name.get(variable_name, default).get('type')

    def has_subtype(self, variable_name, subtype, strict=False):
        default = None if strict else {}
        return subtype in self.definition_by_variable_name.get(variable_name, default).get('subtypes', [])

    def is_calculee(self, variable_name, subtype=None):
        return self.get_type(variable_name) == 'variable_calculee' and \
            (True if subtype is None else self.has_subtype(variable_name, subtype))

    def is_constant(self, variable_name):
        return variable_name in self.constants

    def is_saisie(self, variable_name):
        return self.get_type(variable_name) == 'variable_saisie'
