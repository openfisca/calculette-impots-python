#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import logging
import os
import sys

from calculateur_impots import core


# Globals


args = None
script_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(script_name)

script_dir_name = os.path.dirname(os.path.abspath(__file__))


def iter_variables_calculees(variables):
    for variable_name, value in iter_name_and_value(variables):
        if value is None:
            variable_definition = core.find_definition(variable_name)
            assert variable_definition['type'] == 'variable_calculee', \
                'Calculation requested for variable "{}" but type != "variable_calculee"'.format(variable_name)
            yield variable_name


def iter_variables_saisies(values):
    for variable_name, value in map(lambda value: value.split('=', 1), values):
        variable_definition = core.find_definition(variable_name)
        assert variable_definition['type'] == 'variable_saisie', \
            'Value provided for variable "{}" but type != "variable_saisie"'.format(variable_name)
        yield variable_name, value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Increase output verbosity')
    parser.add_argument('-d', '--debug', action='store_true', default=False, help='Display debug messages')
    parser.add_argument('--calculee', dest='calculees', default='IINET', metavar='variable', nargs='+',
                        help='Variables calculées')
    parser.add_argument('--saisie', dest='saisies', metavar='variable', nargs='+', help='Variables saisies')
    global args
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose or args.debug else logging.WARNING, stream=sys.stdout)

    variables_saisies = {variable_name: value for variable_name, value in iter_variables_saisies(args.saisies)} \
        if args.saisies is not None \
        else None

    core.calculate_formulas(variables_saisies=variables_saisies)

    calculees = [variable_name for variable_name in iter_variables_calculees(args.calculees)]
    print(calculees)
    # result = {
    #     variable_name: simulation.calculate(variable_name)
    #     for variable_name in variables_calculees
    #     }
    # print(result)

    return 0


if __name__ == '__main__':
    sys.exit(main())
