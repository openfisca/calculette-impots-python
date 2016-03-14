# -*- coding: utf-8 -*-


import math

from toolz.curried.operator import ge, gt, is_, ne


# M language functions


arr = round
inf = math.floor
null = is_(None)
positif = gt(0)
positif_ou_nul = ge(0)
present = ne(0)
somme = sum
