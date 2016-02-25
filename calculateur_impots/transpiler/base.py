# -*- coding: utf-8 -*-


def sanitized_variable_name(value):
    # Python variables must not begin with a digit.
    return '_' + value if value[0].isdigit() else value
