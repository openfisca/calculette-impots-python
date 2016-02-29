# -*- coding: utf-8 -*-


import inspect
import sys


def get_visitor(node, module_name):
    visitor_name = 'visit_' + node['type']
    module = sys.modules[module_name]
    module_visitors = filter(lambda member: member[0].startswith('visit_'), inspect.getmembers(module))
    visitor = dict(module_visitors).get(visitor_name)
    return visitor


def sanitized_variable_name(value):
    # Python variables must not begin with a digit.
    return '_' + value if value[0].isdigit() else value
