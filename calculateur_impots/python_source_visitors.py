# -*- coding: utf-8 -*-


"""
Functions used to transpile the JSON AST nodes to Python source code.
Each function `visit_abc` handles a node of type 'abc' and returns either a string or None.
These functions are called by transpiler.core.
"""


import itertools
import json
import logging
import pprint
import textwrap

from m_language_parser.unloop_helpers import iter_unlooped_nodes
from toolz import concatv, interpose

from . import core


log = logging.getLogger(__name__)


# Helpers


def visit_infix_expression(node, operators={}):
    def interleave(*iterables):
        for values in itertools.zip_longest(*iterables, fillvalue=UnboundLocalError):
            for index, value in enumerate(values):
                if value != UnboundLocalError:
                    yield index, value

    tokens = [
        visit_node(operand_or_operator)
        if index == 0
        else operators.get(operand_or_operator, operand_or_operator)
        for index, operand_or_operator in interleave(node['operands'], node['operators'])
        ]
    # Transform product expressions into a lazy "and" expression in order to prevent a division by 0:
    if node['type'] == 'product_expression':
        tokens = concatv(
            interpose(
                el='and',
                seq=map(visit_node, node['operands'][:-1]),
                ),
            ['and'],
            tokens,
            )
    return '({})'.format(' '.join(map(str, tokens)))


# Main visitor


deep_level = 0


def visit_node(node, parenthesised=False):
    """Main visitor which calls the specific visitors below."""
    global deep_level
    visitor_name = 'visit_' + node['type']
    visitor = globals().get(visitor_name)
    if visitor is None:
        error_message = '"def {}(node):" is not defined, node = {}'.format(
            visitor_name,
            pprint.pformat(node, width=120),
            )
        raise NotImplementedError(error_message)
    nb_prefix_chars = len('DEBUG:' + __name__) + 1
    visitor_short_name = visitor_name[len('visit_'):]
    prefix = '> {}{}'.format(
        visitor_short_name + ' ' * (nb_prefix_chars - len(visitor_short_name) - 3) + ':',
        ' ' * deep_level * 4,
        )
    node_str = textwrap.indent(json.dumps(node, indent=4), prefix=prefix)[nb_prefix_chars:].lstrip()
    log.debug(
        '{}{}({})'.format(
            ' ' * deep_level * 4 + '={}=> '.format(deep_level),
            visitor_name,
            node_str,
            )
        )
    deep_level += 1
    result = visitor(node)
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
        visit_node(node['left_operand'], parenthesised=True),
        {'=': '=='}.get(node['operator'], node['operator']),
        visit_node(node['right_operand'], parenthesised=True),
        )


def visit_dans(node):
    return '{} {} {}'.format(
        visit_node(node['expression'], parenthesised=True),
        'not in' if node.get('negative_form') else 'in',
        visit_node(node['enumeration']),
        )


def visit_enumeration_values(node):
    return str(tuple(node['values']))


def visit_float(node):
    return str(node['value'])


def visit_formula(node):
    formula_name = node['name']
    sanitized_formula_name = core.sanitized_variable_name(formula_name)
    expression_source = visit_node(node['expression'])
    docstring_lines = []
    description = core.get_variable_description(formula_name)
    if description is not None:
        docstring_lines.append(description)
    if 'pour_formula' in node:
        docstring_lines.append('From {}'.format(node['pour_formula']['name']))
    source = """\
@cached
def {formula_name}():
    \"\"\"
{docstring}
    \"\"\"
    return {expression}
""".format(
        docstring=textwrap.indent('\n'.join(docstring_lines), prefix=4 * ' '),
        expression=expression_source,
        formula_name=sanitized_formula_name,
        )
    return (sanitized_formula_name, source)


def visit_function_call(node):
    return '{name}({arguments})'.format(
        arguments=', '.join(map(visit_node, node['arguments'])),
        name=node['name'],
        )


def visit_integer(node):
    return str(node['value'])


def visit_interval(node):
    return 'interval({}, {})'.format(int(node['first']), int(node['last']))


def visit_loop_expression(node):
    unlooped_loop_expressions_nodes = iter_unlooped_nodes(
        loop_variables_nodes=node['loop_variables'],
        node=node['expression'],
        )
    source = '[{}]'.format(
        ', '.join(map(visit_node, unlooped_loop_expressions_nodes)),
        )
    return source


def visit_pour_formula(node):
    def update_and_visit_node(node1):
        node1.update({'pour_formula': node['formula']})
        return visit_node(node1)
    return map(
        update_and_visit_node,
        iter_unlooped_nodes(
            loop_variables_nodes=node['loop_variables'],
            node=node['formula'],
            unloop_keys=['name'],
            ),
        )


def visit_product_expression(node):
    return visit_infix_expression(node)


def visit_regle(node):
    return map(
        lambda node1: {
            'applications': node['applications'],
            'sources': visit_node(node1) if node1['type'] == 'pour_formula' else [visit_node(node1)],
            },
        node['formulas'],
        )


def visit_sum_expression(node):
    return visit_infix_expression(node)


def visit_symbol(node):
    symbol = node['value']
    return 'saisie_variables.get({!r}, 0)'.format(symbol) \
        if core.is_saisie_variable(symbol) \
        else (
            'base_variables[{!r}]'.format(symbol)
            if core.is_base_variable(symbol) and not core.is_restituee_variable(symbol)
            else (
                '{}()'.format(core.sanitized_variable_name(symbol))
                if core.is_calculee_variable(symbol)
                else core.sanitized_variable_name(symbol)
                )
            )


def visit_ternary_operator(node):
    return '{} if {} else {}'.format(
        visit_node(node['value_if_true'], parenthesised=True),
        visit_node(node['condition'], parenthesised=True),
        visit_node(node['value_if_false'], parenthesised=True) if 'value_if_false' in node else 0,
        )


def visit_variable_const(node):
    return '{} = {}'.format(node['name'], node['value'])


def visit_verif(node):
    return '# verif {name}\n{assertions}\n'.format(
        assertions='\n'.join(
            """\
if {expression}:
    errors.append({error_name!r})
""".format(
                error_name=condition_node['error_name'],
                expression=visit_node(condition_node['expression']),
                )
            for condition_node in node['conditions']
            ),
        name=node['name'],
        )
