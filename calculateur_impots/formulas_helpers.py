# -*- coding: utf-8 -*-


import math

from toolz.curried.operator import eq, ge, gt, ne


# M language functions


arr = round
inf = math.floor
null = eq(0)
positif = gt(0)
positif_ou_nul = ge(0)
present = ne(0)
somme = sum
