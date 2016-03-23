# -*- coding: utf-8 -*-

import math


"""Functions used by formulas"""


# M language functions translated to Python


arr = round

inf = math.floor


def interval(first, last):
    return range(first, last + 1)


def null(value):
    return int(value == 0)


def positif(value):
    return int(value > 0)


def positif_ou_nul(value):
    return int(value >= 0)


def present(value):
    return int(value != 0)


somme = sum


# Cache decorator


def cached(result_by_formula_name_cache):
    def cached_decorator(formula_function):
        formula_name = formula_function.__name__

        def cached_formula():
            if formula_name not in result_by_formula_name_cache:
                result = formula_function()
                result_by_formula_name_cache[formula_name] = result
            return result_by_formula_name_cache[formula_name]
        return cached_formula
    return cached_decorator
