#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import json
import logging
import os
import pkg_resources
import sys

from toolz.curried import concatv, itemmap, keyfilter, mapcat, pipe, valmap

# Note: absolute notation is used here since we are in a script.

from calculateur_impots import core
# from calculateur_impots.generated import chap_ini_formulas, formulas
from calculateur_impots.generated import formulas
from calculateur_impots.generated.variables_definitions import variable_definition_by_name
# from calculateur_impots.generated.verif_regles import verif_regles


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


def main():
    global args, parser
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Increase output verbosity')
    parser.add_argument('-d', '--debug', action='store_true', default=False, help='Display debug messages')
    parser.add_argument('calculees', default=['IINETIR'], metavar='variable', nargs='*', help='Variables calculées')
    parser.add_argument('--saisie', dest='saisie_variables', metavar='nom=valeur', nargs='+', help='Variables saisies')
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.debug else (logging.INFO if args.verbose else logging.WARNING),
        stream=sys.stdout,
        )

    # Required variables_saisies: ANREV, REGCO (tag "contexte"?)
    # Set V_IND_TRAIT to "primitif" (value 0?)

    saisie_variables = dict(iter_saisie_variables(args.saisie_variables)) \
        if args.saisie_variables is not None \
        else {}
    log.debug('saisie_variables: {}'.format(saisie_variables))

    base_variables_value_by_name = {}  # Override base variables values
    base_variables = pipe(
        variable_definition_by_name,
        keyfilter(core.is_base_variable),
        itemmap(lambda item: (item[0], base_variables_value_by_name.get(item[0], 0))),
        )

    # Utilisé depuis chap-ini
    # src/tgvH.m:10943:RIDEFRIBIS : calculee : "Vaut 1 si reduction different de 0 et majo et un revenu 1731 bis " type REEL ;  # noqa
    # src/tgvH.m:52:10MINSC : calculee : "deductions hors droits d'auteur plafonnees" ;
    # src/tgvH.m:57:10MINSV : calculee : "deductions hors droits d'auteur plafonnees" ;
    # src/tgvH.m:12128:SHBA : calculee : "Somme des revenus categoriels nets hors BA" ; (chap-7)
    # src/tgvH.m:4019:INDCOLS : calculee restituee : "Indicateur avis CSG (colonne Contrib.sal. 2,5 %) ligne total net" ;  # noqa
    # src/tgvH.m:4024:INDCTXS : calculee restituee : "Indicateur avis CSG (contrib. salariale 2,5 %) degrevement" ;

    # Utilisé depuis chap-aff
    # src/chap-aff.m:3016:LIGBPTPGJ = positif(BPTP19WGWJ) * LIG1 * LIG2 * (1 - null(2 - V_REGCO)) * (1 - null(4 - V_REGCO));  # noqa
    # src/tgvH.m:1770:BPTP19WGWJ : calculee restituee : "Revenus au taux proportionnel 19% 3WG 3WJ" ;
    # src/tgvH.m:5649:LIGBPTPGJ : calculee restituee : "Indicateur plus values et creances imposees a 19 % (3WG, 3WJ)" ;

    # chap_ini_formulas_results = chap_ini_formulas.compute(
    #     base_variables=base_variables,
    #     saisie_variables=saisie_variables,
    #     )
    # log.debug('chap_ini_formulas_results: {}'.format(chap_ini_formulas_results))

    # m_language_parser_dir_path = pkg_resources.get_distribution('m_language_parser').location
    # formulas_dependencies_file_path = os.path.join(m_language_parser_dir_path, 'json', 'data',
    #                                                'formulas_dependencies.json')
    # with open(formulas_dependencies_file_path) as formulas_dependencies_file:
    #     formulas_dependencies_str = formulas_dependencies_file.read()
    # formulas_dependencies_by_name = json.loads(formulas_dependencies_str)
    # # log.debug(len(list(concat(formulas_dependencies_by_name.values()))))
    # formulas_dependencies_by_name = valmap(
    #     lambda variables_names: list(sorted(filter(
    #         lambda formula_name: (not core.is_saisie_variable(formula_name) and
    #                               not core.is_constant(formula_name) and
    #                               not core.is_base_variable(formula_name)),
    #         variables_names,
    #         ))),
    #     formulas_dependencies_by_name,
    #     )
    # # log.debug(len(list(concat(formulas_dependencies_by_name.values()))))
    #
    # # dependencies_cache = {}
    #
    # def get_dependencies(formula_name, missing_dependencies, depth=0):
    #     # if formula_name not in dependencies_cache:
    #     if formula_name in formulas_dependencies_by_name:
    #         dependencies = formulas_dependencies_by_name[formula_name]
    #         # log.debug('A:{}{} {}'.format(' ' * 2 * depth, formula_name, dependencies))
    #         if dependencies:
    #             result = list(concatv(
    #                 dependencies,
    #                 mapcat(
    #                     lambda formula_name: get_dependencies(formula_name, missing_dependencies, depth + 1),
    #                     dependencies,
    #                     ),
    #                 ))
    #             # log.debug('B:{}{} {} => {}'.format(' ' * 2 * depth, formula_name, dependencies, result))
    #             # dependencies_cache[formula_name] = result
    #             return result
    #         else:
    #             # dependencies_cache[formula_name] = dependencies
    #             return dependencies
    #     else:
    #         log.debug('C:{}{} => None (type: {}, attributes: {})'.format(' ' * 2 * depth, formula_name,
    #                   core.get_variable_type(formula_name),
    #                   core.get_variable_definition(formula_name, {}).get('attributes')))
    #         missing_dependencies.append(formula_name)
    #         # dependencies_cache[formula_name] = []
    #         return []
    #     # log.debug(len(dependencies_cache))
    #     # return dependencies_cache[formula_name]

    # requested_variable_name = args.calculees[0]
    # log.debug('requested_variable_name = {}'.format(requested_variable_name))
    # missing_dependencies = []
    # requested_variable_dependencies = set(get_dependencies(requested_variable_name, missing_dependencies))
    # import ipdb; ipdb.set_trace()

    formulas_results = formulas.compute(
        base_variables=base_variables,
        saisie_variables=saisie_variables,
        )
    log.debug('formulas_results: {}'.format(formulas_results))

    # variables_calculees = core.evaluate_formulas(module_name='formulas')
    #
    # verif_regles(variables_saisies)
    #
    # requested_variables_calculees = list(iter_variables_calculees(args.calculees))
    # variables_calculees = core.evaluate_formulas(module_name='formulas')
    # # FIXME Verify that variables_calculees has type "restituee".
    # print(keyfilter(
    #     lambda key: key in requested_variables_calculees,
    #     variables_calculees,
    #     ))

    return 0


if __name__ == '__main__':
    sys.exit(main())
