#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""\
Calculette Impôts

Usage:
  calculette-impots calculate [--no-verifs] VARIABLE...
  calculette-impots info VARIABLE...
  calculette-impots EXTERNAL_COMMAND
  calculette-impots (-h | --help)
  calculette-impots --version
"""


from collections import defaultdict
import json
import pkg_resources
import subprocess
import sys

from docopt import docopt
from toolz.curried import unique, valfilter

from calculette_impots import loaders
from calculette_impots.generated import formulas, verifs
from calculette_impots.variables_definitions import VariablesDefinitions


arguments = None
constants = loaders.load_constants()
dependencies_by_formula_name = loaders.load_formulas_dependencies()
variables_definitions = VariablesDefinitions()


def calculate(calculee_variable_names=[], saisie_variables={}):
    global arguments

    warning_messages_by_section = defaultdict(list)

    nb_calculee_variable_names_requested = len(calculee_variable_names)
    if not calculee_variable_names:
        calculee_variable_names = variables_definitions.filter_calculees(kind='restituee')
    else:
        for calculee_variable_name in calculee_variable_names:
            if not variables_definitions.is_calculee(calculee_variable_name, kind='restituee'):
                warning_messages_by_section['saisies'].append(
                    'Variable "{}" is not a variable of type "calculee restituee"'.format(calculee_variable_name)
                    )

    if 'V_ANREV' not in saisie_variables:
        warning_messages_by_section['saisies'].append(
            'V_ANREV should be given as a "saisie" variable. Hint: V_ANREV=2014'
            )

    result_by_formula_name_cache = {}
    formulas_functions = formulas.get_formulas(
        cache=result_by_formula_name_cache,
        constants=constants,
        saisie_variables=saisie_variables,
        )

    if not arguments['--no-verifs']:
        errors = verifs.get_errors(
            formulas=formulas_functions,
            saisie_variables=saisie_variables,
            )
        if errors is not None:
            definition_by_error_name = loaders.load_errors_definitions()
            warning_messages_by_section['verif_errors'] = [
                (error, definition_by_error_name.get(error, {}).get('description'))
                for error in unique(errors)  # Keep order
                ]

    results = {
        calculee_variable_name: formulas_functions[calculee_variable_name]()
        for calculee_variable_name in calculee_variable_names
        }
    if nb_calculee_variable_names_requested == 0:
        results = valfilter(lambda val: val > 0, results)

    dump(
        valfilter(
            lambda val: val is not None,
            {
                'calculate_results': results,
                'warnings': warning_messages_by_section or None,
                },
            ),
        )


def dump(value):
    print(json.dumps(value, indent=2, sort_keys=True))


def get_variable_info(variable_name):
    variable_definition = variables_definitions.definition_by_variable_name.get(variable_name)
    if variable_definition is None:
        exit('The variable {!r} is not defined.'.format(variable_name))
    variable_dependencies = dependencies_by_formula_name.get(variable_name)
    if variable_dependencies is not None:
        variable_dependencies = sorted(variable_dependencies)
    variable_reverse_dependencies = sorted(valfilter(
        lambda val: variable_name in val,
        dependencies_by_formula_name,
        ).keys()) or None
    return valfilter(
        lambda val: val is not None,
        {
            'variable_definition': variable_definition,
            'variable_dependencies': variable_dependencies,
            'variable_reverse_dependencies': variable_reverse_dependencies,
            },
        )


def info(variable_names):
    dump({
        variable_name: get_variable_info(variable_name)
        for variable_name in variable_names
        })


def iter_calculate_variables(variables):
    for variable_str in variables:
        if '=' in variable_str:
            variable_name, variable_value = variable_str.strip('=').split('=', 1)
            if not variables_definitions.is_saisie(variable_name):
                exit('Variable "{}" is not a "saisie" variable'.format(variable_name))
            try:
                variable_value = float(variable_value)
            except ValueError:
                exit('In "{}={}" value is not a float'.format(variable_name, variable_value))
            yield 'variable_saisie', (variable_name, variable_value)
        else:
            if not variables_definitions.is_calculee(variable_str):
                exit('Variable "{}" is not a "calculee" variable'.format(variable_str))
            yield 'variable_calculee', variable_str


def main():
    global arguments

    package_name = 'calculette_impots'
    version = pkg_resources.require(package_name)[0].version
    arguments = docopt(__doc__, version='{} {}'.format(package_name, version))
    if arguments['calculate']:
        variables = list(iter_calculate_variables(arguments['VARIABLE']))
        calculate(
            calculee_variable_names=[
                variable_name
                for variable_type, variable_name in variables
                if variable_type == 'variable_calculee'
                ],
            saisie_variables=dict([
                pair
                for variable_type, pair in variables
                if variable_type == 'variable_saisie'
                ]),
            )
    elif arguments['info']:
        info(variable_names=arguments['VARIABLE'])
    elif arguments['EXTERNAL_COMMAND']:
        command = 'calculette-impots-{}'.format(arguments['EXTERNAL_COMMAND'])
        try:
            subprocess.run(command)
        except FileNotFoundError as exc:  # noqa
            print('error: External command {!r} not found in PATH'.format(command))
            if arguments['EXTERNAL_COMMAND'] == 'web-api':
                print('hint: Install the package "https://git.framasoft.org/openfisca/calculette-impots-web-api"')
            elif arguments['EXTERNAL_COMMAND'] == 'web-explorer':
                print('hint: Install the package "https://git.framasoft.org/openfisca/calculette-impots-web-explorer"')
    else:
        raise NotImplementedError(arguments)

    return 0


if __name__ == '__main__':
    sys.exit(main())
