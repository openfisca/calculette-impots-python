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
from calculateur_impots.generated.variables_definitions import definition_by_variable_name


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

    # Required variables_saisies: V_ANREV, V_REGCO (tag "contexte"?)

    # src/tgvH.m:968:APPLI_AVIS : saisie contexte classe = 0 priorite = 10 categorie_TL = 20 restituee alias AVIS : "Application Avis" ;  # noqa
    # src/tgvH.m:970:APPLI_COLBERT : saisie contexte classe = 0 priorite = 0 categorie_TL = 0 restituee alias V_COLBERT : "Appli_Colbert" type BOOLEEN ;  # noqa
    # src/tgvH.m:973:APPLI_OCEANS : saisie contexte classe = 0 priorite = 0 categorie_TL = 0 restituee alias V_OCEANS : "Appli_Oceans" ;  # noqa

    # src/tgvH.m:2299:CODE_2042 : saisie contexte classe = 0 priorite = 0 categorie_TL = 0 alias V_CODE_2042 : "nouv cor: code majoration de la 2042 fourni par l interface" ;  # noqa
    # src/tgvH.m:5470:ITREDFRI : saisie contexte classe = 0 priorite = 0 categorie_TL = 0 restituee alias V_REDFRI : "ITRED de la decla finale avant application 1731 bis " type REEL ;  # noqa
    # src/tgvH.m:14401:V_ANCSDED : saisie contexte classe = 0 priorite = 10 categorie_TL = 20 alias ANCSDED : "Annee de revenu pour variation CSG" ;  # noqa
    # src/tgvH.m:14826:V_ROLCSG : saisie contexte classe = 0 priorite = 10 categorie_TL = 20 alias ROLCSG : "numero de role CSG" ;  # noqa
    # src/tgvH.m:14523:V_CALCULIR : saisie contexte classe = 0 priorite = 51 categorie_TL = 10 alias CALCULIR : "= 0 si saisie 2042 ILIAD , = 1 si CALCULIR sous ILIAD" ;  # noqa
    # src/tgvH.m:14524:V_CALCULMAJO : saisie contexte classe = 0 priorite = 51 categorie_TL = 10 alias CALCULMAJO : "pour appel Denature rappel" ;  # noqa
    # src/tgvH.m:14588:V_ETCVL : saisie contexte classe = 0 priorite = 51 categorie_TL = 10 alias ETCVL : "ISF : Variable relative a l etat civil " type BOOLEEN ;  # noqa
    # src/tgvH.m:14682:V_REGANT : saisie contexte classe = 0 priorite = 51 categorie_TL = 10 alias REGANT : "Valeur de REGCO evt -1 calculee " ;  # noqa

    # src/tgvH.m:14683:V_REGCO : saisie contexte classe = 0 priorite = 51 categorie_TL = 10 alias REGCO : "Valeur de REGCO calculee (Cf. VALREGCO)" ;  # noqa

    # src/tgvH.m:14880:V_TRCT : saisie contexte classe = 0 priorite = 51 categorie_TL = 10 alias TRCT : "Variable relative a la telecorrection" ;  # noqa

    saisie_variables = {}

    # src/tgvH.m:14604:V_IND_TRAIT : saisie contexte classe = 0 priorite = 10 categorie_TL = 20 alias IND_TRAIT : "indicateur de nature de trait. primitif ou correctif" ;  # noqa
    # 0 = primitif ?
    # 4 = calcul correctif mais utilisant d'autres calculs que le 5 ?
    # 5 = calcul correctif
    saisie_variables['V_IND_TRAIT'] = 0

    # src/tgvH.m:14211:VALREGCO : saisie revenu classe = 0 priorite = 20 categorie_TL = 10 cotsoc = 5 ind_abat = 0 acompte = 1 avfisc = 0 rapcat = 13 sanction = 0 nat_code = 1 alias 8ZA : "Regime d'imposition des non residents - Valeur 1, 2 ou 4" ;  # noqa
    # saisie_variables['VALREGCO'] = 1

    # src/tgvH.m:14404:V_ANREV : saisie contexte classe = 0 priorite = 10 categorie_TL = 20 alias ANREV : "Annee des revenus" type REEL ;  # noqa
    saisie_variables['V_ANREV'] = 2014

    # src/tgvH.m:14339:V_0DA : saisie famille classe = 0 priorite = 20 categorie_TL = 10 nat_code = 0 restituee alias 0DA : "Annee de naissance du declarant" type DATE_AAAA ;  # noqa
    # saisie_variables['V_0DA'] = 1980

    # src/tgvH.m:14317:V_0AC : saisie famille classe = 0 priorite = 20 categorie_TL = 10 nat_code = 0 alias 0AC : "Case a cocher : situation de famille Celibataire" type BOOLEEN ;  # noqa
    # saisie_variables['V_0AC'] = 1

    # Avoid division by 0
    saisie_variables['CARPENBAV'] = 1
    saisie_variables['CARPENBAC'] = 1

    if args.saisie_variables is not None:
        saisie_variables.update(iter_saisie_variables(args.saisie_variables))
    log.debug('saisie_variables: {}'.format(saisie_variables))

    base_variables_value_by_name = {}  # Override base variables values
    base_variables = {
        variable_name: base_variables_value_by_name.get(variable_name, 0)
        for variable_name, variable_definition in definition_by_variable_name.items()
        if core.is_base_variable(variable_name)
        }

    errors = verifs.get_errors(
        base_variables=base_variables,
        saisie_variables=saisie_variables,
        )
    if errors is not None:
        errors_definitions = load_errors_definitions()
        definition_by_error_name = pipe(errors_definitions, map(lambda d: (d['name'], d)), dict)
        print('errors: {}'.format(
            json.dumps(
                [
                    (error, definition_by_error_name.get(error, {}).get('description', 'No description found!'))
                    for error in unique(errors)  # Keep order
                    ],
                indent=4,
                ),
            ))

    formulas_functions = formulas.get_formulas(
        base_variables=base_variables,
        saisie_variables=saisie_variables,
        )

    for calculee_variable_name in args.calculee_variables:
        sanitized_calculee_variable = core.sanitized_variable_name(calculee_variable_name)
        try:
            requested_formula_result = formulas_functions[sanitized_calculee_variable]()
        except:
            log.exception('Error while calculating {}'.format(sanitized_calculee_variable))
        print('{} = {} ({})'.format(calculee_variable_name, requested_formula_result,
                                    core.get_variable_description(calculee_variable_name)))

    return 0


if __name__ == '__main__':
    sys.exit(main())
