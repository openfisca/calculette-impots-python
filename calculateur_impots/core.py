# -*- coding: utf-8 -*-


import importlib


# Formulas helpers


saisies = None  # Global variable used by formulas, filled by `calculate_formulas`


def is_positive(n):
    return n > 0


def is_zero(n):
    return n == 0


# Core functions


def calculate_formulas(variables_saisies=None):
    if variables_saisies is None:
        variables_saisies = {}
    global saisies
    saisies = variables_saisies
    importlib.import_module(name='.generated.formulas', package='calculateur_impots')
