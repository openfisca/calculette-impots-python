#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from collections import defaultdict
import argparse
import json
import logging
import os
import sys

from toolz.curried import get, map, unique, valfilter

from calculette_impots import loaders
from calculette_impots.generated import formulas, verifs
from calculette_impots.variables_definitions import VariablesDefinitions


args = None
script_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(script_name)

constants = loaders.load_constants()
variables_definitions = VariablesDefinitions(constants=constants)


def iter_saisie_variables(values):
    global variables_definitions
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
        if not variables_definitions.is_saisie(variable_name):
            parser.error('Variable "{}" is not a variable saisie'.format(variable_name))
        yield variable_name, variable_value


def main():
    global args, constants, parser, variables_definitions

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Increase output verbosity')
    parser.add_argument('-d', '--debug', action='store_true', default=False, help='Display debug messages')
    parser.add_argument('--calculees', dest='calculee_variables', metavar='variable', nargs='+',
                        help='Variables calculées')
    parser.add_argument('--saisies', dest='saisie_variables', metavar='nom=valeur', nargs='+', help='Variables saisies')
    parser.add_argument('--no-verifs', action='store_true', default=False, help='Skip verifs step')
    parser.add_argument('--output-format', choices=['text', 'json'], default='text', help='Output format')
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.debug else (logging.INFO if args.verbose else logging.WARNING),
        stream=sys.stdout,
        )

    warning_messages_by_section = defaultdict(list)

    if args.calculee_variables is None:
        calculee_variable_names = variables_definitions.filter_by_subtype('restituee')
    else:
        calculee_variable_names = args.calculee_variables
        for calculee_variable_name in calculee_variable_names:
            if not variables_definitions.has_subtype(calculee_variable_name, 'restituee'):
                warning_messages_by_section['saisies'].append(
                    'Variable "{}" is not a variable of type "calculee restituee"'.format(calculee_variable_name)
                    )

    saisie_variables = {} if args.saisie_variables is None else dict(iter_saisie_variables(args.saisie_variables))
    if 'V_ANREV' not in saisie_variables:
        warning_messages_by_section['saisies'].append(
            'V_ANREV should be given as a "saisie" variable. Hint: --saisie V_ANREV=2014'
            )

    result_by_formula_name_cache = {}
    formulas_functions = formulas.get_formulas(
        cache=result_by_formula_name_cache,
        constants=constants,
        saisie_variables=saisie_variables,
        )

    if not args.no_verifs:
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

    results = {}
    for calculee_variable_name in calculee_variable_names:
        try:
            result = formulas_functions[calculee_variable_name]()
        except:
            log.exception('Error while calculating {}'.format(calculee_variable_name))
        else:
            results[calculee_variable_name] = result
    if args.calculee_variables is None:
        results = valfilter(lambda val: val > 0, results)

    if args.output_format == 'text':
        for section, warning_messages in warning_messages_by_section.items():
            for warning_message in warning_messages:
                log.warning('{}:{}'.format(section, warning_message))
        for calculee_variable_name, result in reversed(sorted(results.items(), key=get(1))):
            print('{} = {} ({})'.format(calculee_variable_name, result,
                                        variables_definitions.get_description(calculee_variable_name)))
    elif args.output_format == 'json':
        print(json.dumps(
            {'results': results, 'warnings': warning_messages_by_section},
            sort_keys=True,
            ))
    else:
        raise NotImplementedError()

    return 0


if __name__ == '__main__':
    sys.exit(main())
