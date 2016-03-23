#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import json
import logging
import os
import pkg_resources
import sys

from toolz.curried import map, pipe, unique

from calculateur_impots import core
from calculateur_impots.generated import formulas, verifs
# from calculateur_impots.generated.variables_definitions import definition_by_variable_name


# Globals


args = None
script_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(script_name)

script_dir_name = os.path.dirname(os.path.abspath(__file__))


def iter_saisie_variables(values):
    for value, words in map(lambda value: (value, value.strip('=').split('=', 1)), values):
        if len(words) == 1:
            parser.error('Missing value for variable saisie: "{}"'.format(value))
        elif len(words) > 2:
            parser.error('Invalid syntax for variable saisie: "{}"'.format(value))
        variable_name, variable_value = words
        try:
            variable_value = float(variable_value)
        except ValueError:
            parser.error('Variable "{}" value is not a float'.format(value))
        variable_type = core.get_variable_type(variable_name)
        if variable_type != 'variable_saisie':
            parser.error('Variable "{}" is not a variable saisie'.format(variable_name))
        yield variable_name, variable_value


def load_errors_definitions():
    m_language_parser_dir_path = pkg_resources.get_distribution('m_language_parser').location
    errors_definitions_file_path = os.path.join(m_language_parser_dir_path, 'json', 'ast', 'errH.json')
    with open(errors_definitions_file_path) as errors_definitions_file:
        errors_definitions_str = errors_definitions_file.read()
    errors_definitions = json.loads(errors_definitions_str)
    return errors_definitions


def main():
    global args, parser
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Increase output verbosity')
    parser.add_argument('-d', '--debug', action='store_true', default=False, help='Display debug messages')
    parser.add_argument('--calculees', dest='calculee_variables', metavar='variable', nargs='+',
                        help='Variables calculées')
    parser.add_argument('--saisies', dest='saisie_variables', metavar='nom=valeur', nargs='+', help='Variables saisies')
    parser.add_argument('--no-verifs', action='store_true', default=False, help='Skip verifs step')
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.debug else (logging.INFO if args.verbose else logging.WARNING),
        stream=sys.stdout,
        )

    for calculee_variable in args.calculee_variables:
        if not core.is_restituee_variable(calculee_variable):
            not_restituee_message = 'Variable "{}" is not a variable of type "calculee restituee"'.format(
                calculee_variable)
            log.warning(not_restituee_message)
            # parser.error(not_restituee_message)

    saisie_variables = {
        'V_ANREV': 2014,
        }
    if args.saisie_variables is not None:
        saisie_variables.update(iter_saisie_variables(args.saisie_variables))
    log.debug('saisie_variables: {}'.format(saisie_variables))

    result_by_formula_name_cache = {}
    formulas_functions = formulas.get_formulas(
        cache=result_by_formula_name_cache,
        saisie_variables=saisie_variables,
        )

    if not args.no_verifs:
        errors = verifs.get_errors(
            formulas=formulas_functions,
            saisie_variables=saisie_variables,
            )
        if errors is not None:
            errors_definitions = load_errors_definitions()
            definition_by_error_name = pipe(errors_definitions, map(lambda d: (d['name'], d)), dict)
            print('errors: {}'.format(
                json.dumps(
                    [
                        (
                            error,
                            definition_by_error_name.get(error, {}).get('description', 'No error description found'),
                            )
                        for error in unique(errors)  # Keep order
                        ],
                    indent=4,
                    ),
                ))

    for calculee_variable_name in args.calculee_variables:
        sanitized_calculee_variable = core.sanitized_variable_name(calculee_variable_name)
        # requested_formula_result = formulas_functions[sanitized_calculee_variable]()
        # print('{} = {} ({})'.format(calculee_variable_name, requested_formula_result,
        #                             core.get_variable_description(calculee_variable_name)))
        try:
            requested_formula_result = formulas_functions[sanitized_calculee_variable]()
        except:
            log.exception('Error while calculating {}'.format(sanitized_calculee_variable))
        else:
            print('{} = {} ({})'.format(calculee_variable_name, requested_formula_result,
                                        core.get_variable_description(calculee_variable_name)))

    return 0


if __name__ == '__main__':
    sys.exit(main())
