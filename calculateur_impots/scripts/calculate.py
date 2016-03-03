#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import logging
import os
import sys

from toolz import keyfilter

# Note: absolute notation is used here since we are in a script.
from calculateur_impots import core
from calculateur_impots.generated.verif_regles import verif_regles


# Globals


args = None
script_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(script_name)

script_dir_name = os.path.dirname(os.path.abspath(__file__))


def iter_variables_calculees(variables_names):
    for variable_name in variables_names:
        variable_type = core.get_variable_type(variable_name)
        if variable_type != 'variable_calculee':
            parser.error('Variable "{}" is not a variable calculee'.format(variable_name))
        yield variable_name


def iter_variables_saisies(values):
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


def main():
    global args, parser
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Increase output verbosity')
    parser.add_argument('-d', '--debug', action='store_true', default=False, help='Display debug messages')
    parser.add_argument('calculees', default=['IINET'], metavar='variable', nargs='*', help='Variables calculées')
    parser.add_argument('--saisie', dest='saisies', metavar='nom=valeur', nargs='+', help='Variables saisies')
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose or args.debug else logging.WARNING, stream=sys.stdout)

    # Required variables_saisies: ANREV, REGCO (tag "contexte"?)
    # Set V_IND_TRAIT to "primitif" (value 0?)

    variables_saisies = dict(iter_variables_saisies(args.saisies)) \
        if args.saisies is not None \
        else {}
    verif_regles(variables_saisies)

    log.debug('variables_saisies: {}'.format(variables_saisies))
    core.evaluate_formulas(variables_saisies=variables_saisies)
    requested_variables_calculees = list(iter_variables_calculees(args.calculees))
    variables_calculees = core.evaluate_formulas(variables_saisies=variables_saisies)
    print(keyfilter(
        lambda key: key in requested_variables_calculees,
        variables_calculees,
        ))

    return 0


if __name__ == '__main__':
    sys.exit(main())
