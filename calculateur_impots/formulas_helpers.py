# -*- coding: utf-8 -*-


import math

from toolz.curried.operator import eq, ge, gt, ne
import infix


# M language functions


arr = round
inf = math.floor
null = eq(0)
positif = gt(0)
positif_ou_nul = ge(0)
present = ne(0)
somme = sum


# Division operator overload


def safe_divide(a, b):
    return 0 if b == 0 else a / b


div = infix.or_infix(safe_divide)


#
# class wrap_value(object):
#     def __init__(self, value):
#         self.value = value
#
#     def __add__(self, other):
#         return wrap_value(self.value + other.value)
#
#     def __sub__(self, other):
#         return wrap_value(self.value - other.value)
#
#     def __mul__(self, other):
#         return wrap_value(self.value * other.value)
#
#     def __lt__(self, other):
#         return wrap_value(self.value < other.value)
#
#     def __gt__(self, other):
#         return wrap_value(self.value > other.value)
#
#     def __truediv__(self, other):
#         # if other == 0:
#         #     import ipdb; ipdb.set_trace()
#         return wrap_value(0 if other.value == 0 else self.value / other.value)


# def wrap_function(func):
#     def apply(val):
#         return wrap_value(func(val.value))
#     return apply


# arr = wrap_function(round)
# inf = wrap_function(math.floor)
# null = wrap_function(eq(0))
# positif = wrap_function(gt(0))
# positif_ou_nul = wrap_function(ge(0))
# present = wrap_function(ne(0))
# somme = wrap_function(sum)
