#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import logging
import os
import sys

from toolz.curried import itemmap, keyfilter, pipe

from calculateur_impots import core
from calculateur_impots.generated import formulas
from calculateur_impots.generated.variables_definitions import variable_definition_by_name
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
    parser.add_argument('calculees', default=['IINET'], metavar='variable', nargs='*', help='Variables calculées')
    parser.add_argument('--saisie', dest='saisie_variables', metavar='nom=valeur', nargs='+', help='Variables saisies')
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.debug else (logging.INFO if args.verbose else logging.WARNING),
        stream=sys.stdout,
        )

    # Required variables_saisies: V_ANREV, V_REGCO (tag "contexte"?)
    # Set V_IND_TRAIT to "primitif" (value 0?)

    # src/tgvH.m:968:APPLI_AVIS : saisie contexte classe = 0 priorite = 10 categorie_TL = 20 restituee alias AVIS : "Application Avis" ;  # noqa
    # src/tgvH.m:970:APPLI_COLBERT : saisie contexte classe = 0 priorite = 0 categorie_TL = 0 restituee alias V_COLBERT : "Appli_Colbert" type BOOLEEN ;  # noqa
    # src/tgvH.m:973:APPLI_OCEANS : saisie contexte classe = 0 priorite = 0 categorie_TL = 0 restituee alias V_OCEANS : "Appli_Oceans" ;  # noqa
    # src/tgvH.m:2299:CODE_2042 : saisie contexte classe = 0 priorite = 0 categorie_TL = 0 alias V_CODE_2042 : "nouv cor: code majoration de la 2042 fourni par l interface" ;  # noqa
    # src/tgvH.m:5470:ITREDFRI : saisie contexte classe = 0 priorite = 0 categorie_TL = 0 restituee alias V_REDFRI : "ITRED de la decla finale avant application 1731 bis " type REEL ;  # noqa
    # src/tgvH.m:14401:V_ANCSDED : saisie contexte classe = 0 priorite = 10 categorie_TL = 20 alias ANCSDED : "Annee de revenu pour variation CSG" ;  # noqa
    # src/tgvH.m:14404:V_ANREV : saisie contexte classe = 0 priorite = 10 categorie_TL = 20 alias ANREV : "Annee des revenus" type REEL ;  # noqa
    # src/tgvH.m:14523:V_CALCULIR : saisie contexte classe = 0 priorite = 51 categorie_TL = 10 alias CALCULIR : "= 0 si saisie 2042 ILIAD , = 1 si CALCULIR sous ILIAD" ;  # noqa
    # src/tgvH.m:14524:V_CALCULMAJO : saisie contexte classe = 0 priorite = 51 categorie_TL = 10 alias CALCULMAJO : "pour appel Denature rappel" ;  # noqa
    # src/tgvH.m:14588:V_ETCVL : saisie contexte classe = 0 priorite = 51 categorie_TL = 10 alias ETCVL : "ISF : Variable relative a l etat civil " type BOOLEEN ;  # noqa
    # src/tgvH.m:14604:V_IND_TRAIT : saisie contexte classe = 0 priorite = 10 categorie_TL = 20 alias IND_TRAIT : "indicateur de nature de trait. primitif ou correctif" ;  # noqa
    # src/tgvH.m:14682:V_REGANT : saisie contexte classe = 0 priorite = 51 categorie_TL = 10 alias REGANT : "Valeur de REGCO evt -1 calculee " ;  # noqa
    # src/tgvH.m:14683:V_REGCO : saisie contexte classe = 0 priorite = 51 categorie_TL = 10 alias REGCO : "Valeur de REGCO calculee (Cf. VALREGCO)" ;  # noqa
    # src/tgvH.m:14826:V_ROLCSG : saisie contexte classe = 0 priorite = 10 categorie_TL = 20 alias ROLCSG : "numero de role CSG" ;  # noqa
    # src/tgvH.m:14880:V_TRCT : saisie contexte classe = 0 priorite = 51 categorie_TL = 10 alias TRCT : "Variable relative a la telecorrection" ;  # noqa

    # src/tgvH.m:14339:V_0DA : saisie famille classe = 0 priorite = 20 categorie_TL = 10 nat_code = 0 restituee alias 0DA : "Annee de naissance du declarant" type DATE_AAAA ;

    saisie_variables = dict(iter_saisie_variables(args.saisie_variables)) \
        if args.saisie_variables is not None \
        else {}
    # saisie_variables['V_IND_TRAIT'] = 0
    saisie_variables['V_ANREV'] = 2014
    log.debug('saisie_variables: {}'.format(saisie_variables))

    base_variables_value_by_name = {}  # Override base variables values
    base_variables = {
        variable_name: base_variables_value_by_name.get(variable_name, 0)
        for variable_name, variable_definition in variable_definition_by_name.items()
        if core.is_base_variable(variable_name)
        }

    # verif_regles(
    #     base_variables=base_variables,
    #     saisie_variables=saisie_variables,
    #     )

    # From ABPRi
    # ABPRV = arr((((1 - IND_APBV) * min(APBV, (
    #     PL_PB and PL_PB * APBV / somme([
    #         (APBV * (1 - IND_APBV)), (APBC * (1 - IND_APBC)), (APB1 * (1 - IND_APB1)), (APB2 * (1 - IND_APB2)),
    #         (APB3 * (1 - IND_APB3)), (APB4 * (1 - IND_APB4))
    #     ])
    # ))) + (IND_APBV * APBV)))

    # ABPRV : calculee : "Abattement brut avant ajustement (pensions retraites 10%)" ;
    # IND_APBV : calculee : "booleen application deduction minimale pensions" ;
    # APBV : calculee : "Minimum d'abattement 10% (PR)" ;
    # PL_PB : calculee : "plafond pensions a repartir" ;

    formulas_results = formulas.compute(
        base_variables=base_variables,
        saisie_variables=saisie_variables,
        )
    # log.debug('formulas_results: {}'.format(formulas_results))

    requested_variables_calculees = list(iter_variables_calculees(args.calculees))
    # FIXME Verify that variables_calculees has type "restituee".
    print(keyfilter(
        lambda key: key in requested_variables_calculees,
        formulas_results,
        ))

    return 0


if __name__ == '__main__':
    sys.exit(main())
