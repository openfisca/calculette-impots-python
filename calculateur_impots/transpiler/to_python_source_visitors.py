# -*- coding: utf-8 -*-


"""
Functions used to transpile the JSON AST nodes to Python source code.
Each function `visit_abc` handles a node of type 'abc' and returns either a string or None.
These functions are called by transpiler.core.
"""


# from functools import reduce
import itertools
import json
import logging
import pprint
import textwrap

from ..core import get_variable_type, mapcat
from .base import sanitized_variable_name
from .unloop_helpers import iter_unlooped_nodes


log = logging.getLogger(__name__)


# Helpers


def visit_infix_expression(node, operators={}):
    def merge(*iterables):
        for values in itertools.zip_longest(*iterables, fillvalue=UnboundLocalError):
            for index, value in enumerate(values):
                if value != UnboundLocalError:
                    yield index, value

    tokens = (
        visit_node(operand_or_operator)
        if index == 0
        else operators.get(operand_or_operator, operand_or_operator)
        for index, operand_or_operator in merge(node['operands'], node['operators'])
        )
    return ' '.join(map(str, tokens))


def iter_find_nodes(node, type, skip_type=None):
    """
    Iterates over all nodes matching `type` recursively in `node`.
    """
    if isinstance(node, dict):
        if node['type'] == type:
            yield node
        elif skip_type is None or node['type'] != skip_type:
            yield from iter_find_nodes(node=list(node.values()), skip_type=skip_type, type=type)
    elif isinstance(node, list):
        for child_node in node:
            if isinstance(child_node, (list, dict)):
                yield from iter_find_nodes(node=child_node, skip_type=skip_type, type=type)


# Main visitor


deep_level = 0


def visit_node(node, parenthesised=False):
    """
    Main transpilation function which calls the specific transpilation functions below.
    They are subfunctions to ensure they are never called directly.
    """
    global deep_level
    transpilation_function_name = 'visit_' + node['type']
    if transpilation_function_name not in globals():
        error_message = '"def {}(node):" is not defined, node = {}'.format(
            transpilation_function_name,
            pprint.pformat(node, width=120),
            )
        raise NotImplementedError(error_message)
    nb_prefix_chars = len('DEBUG:' + __name__) + 1
    transpilation_function_short_name = transpilation_function_name[len('visit_'):]
    prefix = '> {}{}'.format(
        transpilation_function_short_name + ' ' * (nb_prefix_chars - len(transpilation_function_short_name) - 3) + ':',
        ' ' * deep_level * 4,
        )
    node_str = textwrap.indent(json.dumps(node, indent=4), prefix=prefix)[nb_prefix_chars:].lstrip()
    log.debug(
        '{}{}({})'.format(
            ' ' * deep_level * 4 + '={}=> '.format(deep_level),
            transpilation_function_name,
            node_str,
            )
        )
    transpilation_function = globals()[transpilation_function_name]
    deep_level += 1
    result = transpilation_function(node)
    assert result is not None
    deep_level -= 1
    unparenthesised_node_types = ('float', 'function_call', 'integer', 'string', 'symbol')
    if parenthesised:
        assert isinstance(result, str), result
        if node['type'] not in unparenthesised_node_types:
            result = '({})'.format(result)
    log.debug(
        '{}<={}= {}'.format(
            ' ' * deep_level * 4,
            deep_level,
            textwrap.indent(result, prefix='> ')[1:].lstrip() if isinstance(result, str) else str(result),
            )
        )
    assert deep_level >= 0, deep_level
    return result


# Specific visitors


def visit_boolean_expression(node):
    return visit_infix_expression(node, operators={'et': 'and', 'ou': 'or'})


def visit_comparaison(node):
    return '{} {} {}'.format(
        visit_node(node['left_operand']),
        {'=': '=='}.get(node['operator'], node['operator']),
        visit_node(node['right_operand']),
        )


def visit_variable_const(node):
    return '{} = {}'.format(node['name'], node['value'])


def visit_dans(node):
    return '{} {} {}'.format(
        visit_node(node['expression'], parenthesised=True),
        'not in' if node.get('negative_form') else 'in',
        node['enumeration'],
        )


def visit_enumeration_values(node):
    return str(tuple(node['values']))


def visit_float(node):
    return str(node['value'])


def visit_formula(node):
    # state['current_formula'] = []
    expression_source = visit_node(node['expression'])
    # dependencies = set(map(
    #     lambda node: sanitized_variable_name(node['value']),
    #     iter_find_nodes(
    #         node=node,
    #         skip_type='loop_expression',  # visit_loop_expression will handle its dependencies.
    #         type='symbol',
    #         ),
    #     ))
    formula_name = sanitized_variable_name(node['name'])
    # state['formulas_dependencies'][formula_name] = dependencies
    source = '{} = {}'.format(formula_name, expression_source)
    # state['formulas_sources'][formula_name] = source
    # state['current_formula'] = None
    return (formula_name, source)


def visit_function_call(node):
    m_function_name = node['name']
    python_function_name_by_m_function_name = {
        'abs': 'abs',
        'arr': 'round',
        # 'inf': '',
        'max': 'max',
        'min': 'min',
        'null': 'is_zero',
        # 'positif_ou_nul': '',
        'positif': 'is_positive',
        # 'present': '',
        'somme': 'sum',
        }
    # TODO When all functions will be handled, use this assertion.
    # assert m_function_name in python_function_name_by_m_function_name, \
    #     'Unknown M function name: "{}"'.format(m_function_name)
    # python_function_name = python_function_name_by_m_function_name[m_function_name]
    python_function_name = python_function_name_by_m_function_name.get(m_function_name, m_function_name)
    return '{name}({arguments})'.format(
        arguments=', '.join(map(visit_node, node['arguments'])),
        name=python_function_name,
        )


def visit_integer(node):
    return str(node['value'])


def visit_interval(node):
    return 'interval({}, {})'.format(node['first'], node['last'])


def visit_loop_expression(node):
    # def iter_unlooped_loop_expressions_nodes_and_dependencies():
    #     for unlooped_node in iter_unlooped_nodes(
    #             loop_variables_nodes=node['loop_variables'],
    #             node=node['expression'],
    #             ):
    #         dependencies = set(map(
    #             lambda node: sanitized_variable_name(node['value']),
    #             iter_find_nodes(node=unlooped_node, type='symbol'),
    #             ))
    #         yield unlooped_node, dependencies

    # unlooped_loop_expressions_nodes, dependencies = zip(*iter_unlooped_loop_expressions_nodes_and_dependencies())
    # dependencies = reduce(or_, dependencies)
    unlooped_loop_expressions_nodes = iter_unlooped_nodes(
        loop_variables_nodes=node['loop_variables'],
        node=node['expression'],
        )
    source = '[{}]'.format(
        ', '.join(map(visit_node, unlooped_loop_expressions_nodes)),
        )
    # state['current_formula'].append(dependencies)
    return source


def visit_loop_variable(node):
    return ' or '.join(
        '{} in {}'.format(
            node['name'],
            visit_node(enumerations_node),
            )
        for enumerations_node in node['enumerations']
        )


def visit_pour_formula(node):
    return map(visit_node, iter_unlooped_nodes(
            loop_variables_nodes=node['loop_variables'],
            node=node['formula'],
            unloop_keys=['name'],
            ))


def visit_product_expression(node):
    return visit_infix_expression(node)


def visit_regle(node):
    return map(
        lambda node1: visit_node(node1) if node1['type'] == 'pour_formula' else [visit_node(node1)],
        node['formulas'],
        )


def visit_sum_expression(node):
    return visit_infix_expression(node)


def visit_symbol(node):
    symbol = node['value']
    return 'saisies.get({!r}, 0)'.format(symbol) \
        if get_variable_type(symbol) == 'variable_saisie' else sanitized_variable_name(symbol)


def visit_ternary_operator(node):
    return '{} if {} else {}'.format(
        visit_node(node['value_if_true'], parenthesised=True),
        visit_node(node['condition'], parenthesised=True),
        visit_node(node['value_if_false'], parenthesised=True) if 'value_if_false' in node else 0,
        )


def visit_verif(node):
    pass
    # import ipdb; ipdb.set_trace()
