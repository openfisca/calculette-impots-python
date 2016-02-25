# -*- coding: utf-8 -*-


import pprint


# Main visitor


def visit_node(node, parenthesised=False):
    """
    Main transpilation function which calls the specific transpilation functions below.
    They are subfunctions to ensure they are never called directly.
    """
    transpilation_function_name = 'visit_' + node['type']
    if transpilation_function_name not in globals():
        error_message = '"def {}(node):" is not defined, node = {}'.format(
            transpilation_function_name,
            pprint.pformat(node, width=120),
            )
        raise NotImplementedError(error_message)
    transpilation_function = globals()[transpilation_function_name]
    result = transpilation_function(node)
    return result


# Specific visitors


# def visit_regle(node):
#     import ipdb; ipdb.set_trace()
