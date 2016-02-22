#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Transpile (roughly means convert) a JSON AST file to Python source code.
"""


from functools import reduce
from operator import itemgetter, or_
import argparse
import copy
import glob
import itertools
import json
import logging
import os
import pprint
import sys
import textwrap


# Globals


args = None
script_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(script_name)

script_dir_path = os.path.dirname(os.path.abspath(__file__))
generated_dir_path = os.path.abspath(os.path.join(script_dir_path, '..', 'generated'))

state = {
    'current_formula': None,
    'formula_dependencies': {},
    'formula_source': {},
    'is_in_pour_formula': False,
    'variable_definition': None,
    }


# Python helpers

list_ = list  # To use in ipdb since "list" is reserved to display the current source code.


def mapcat(function, sequence):
    return itertools.chain.from_iterable(map(function, sequence))


# Source code helper functions


def lines_to_python_source(sequence):
    return ''.join(itertools.chain.from_iterable(zip(sequence, itertools.repeat('\n'))))


def read_ast_json_file(json_file_name):
    json_file_path = os.path.join(args.json_dir, json_file_name)
    with open(json_file_path) as json_file:
        json_str = json_file.read()
    nodes = json.loads(json_str)
    assert isinstance(nodes, list)
    return nodes


def sanitized_variable_name(value):
    # Python variables must not begin with a digit.
    return '_' + value if value[0].isdigit() else value


def value_to_python_source(value):
    return pprint.pformat(value, width=120)


def write_source(file_name, json_file_name, original_file_name, transpilation_function):
    header = """\
# -*- coding: utf-8 -*-
# flake8: noqa


# WARNING: This file is automatically generated by a script. No not modify it by hand!

# Original files are "{}" and "{}"


""".format(json_file_name, original_file_name)
    global args
    file_path = os.path.join(generated_dir_path, file_name)
    if os.path.exists(file_path) and not args.force and args.json is None:
        log.info('Output file "{}" exists => skip.'.format(file_path))
    elif args.json is None or json_file_name in args.json:
        log.info('Transpiling JSON file "{}" to Python file "{}"'.format(json_file_name, file_name))
        source = transpilation_function(json_file_name)
        with open(file_path, 'w') as output_file:
            output_file.write(header + source)


# General transpilation functions


def infix_expression_to_python_source(node, operators={}):
    def merge(*iterables):
        for values in itertools.zip_longest(*iterables, fillvalue=UnboundLocalError):
            for index, value in enumerate(values):
                if value != UnboundLocalError:
                    yield index, value

    tokens = (
        node_to_python_source(operand_or_operator)
        if index == 0
        else operators.get(operand_or_operator, operand_or_operator)
        for index, operand_or_operator in merge(node['operands'], node['operators'])
        )
    return ' '.join(map(str, tokens))


class TranspilationError(Exception):
    pass


deep_level = 0


def node_to_python_source(node, parenthesised=False):
    """
    Main transpilation function which calls the specific transpilation functions below.
    They are subfunctions to ensure they are never called directly.
    """

    def boolean_expression_to_python_source(node):
        return infix_expression_to_python_source(node, operators={'et': 'and', 'ou': 'or'})

    def comparaison_to_python_source(node):
        return '{} {} {}'.format(
            node_to_python_source(node['left_operand']),
            {'=': '=='}.get(node['operator'], node['operator']),
            node_to_python_source(node['right_operand']),
            )

    def dans_to_python_source(node):
        return '{} {} {}'.format(
            node_to_python_source(node['expression'], parenthesised=True),
            'not in' if node.get('negative_form') else 'in',
            node['enumeration'],
            )

    def enumeration_values_to_python_source(node):
        return str(tuple(node['values']))

    def expression_to_python_source(node):
        return node_to_python_source(node)

    def float_to_python_source(node):
        return str(node['value'])

    def formula_to_python_source(node):
        global state
        state['current_formula'] = []
        expression_source = node_to_python_source(node['expression'])
        dependencies = set(map(
            itemgetter('value'),
            iter_find_nodes(
                node=node,
                skip_type='loop_expression',  # loop_expression_to_python_source will handle its dependencies.
                type='symbol',
                ),
            ))
        formula_name = sanitized_variable_name(node['name'])
        state['formula_dependencies'][formula_name] = dependencies
        source = '{name} = {expression}'.format(
            expression=expression_source,
            name=formula_name,
            )
        state['formula_source'][formula_name] = source
        state['current_formula'] = None
        return None

    def function_call_to_python_source(node):
        m_function_name = node['name']
        python_function_name_by_m_function_name = {
            'abs': 'abs',
            # 'arr': '',
            # 'inf': '',
            'max': 'max',
            'min': 'min',
            # 'null': '',
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
            arguments=', '.join(map(node_to_python_source, node['arguments'])),
            name=python_function_name,
            )

    def integer_to_python_source(node):
        return str(node['value'])

    def interval_to_python_source(node):
        return 'interval({}, {})'.format(node['first'], node['last'])

    def loop_expression_to_python_source(node):
        def iter_unlooped_loop_expressions_nodes_and_dependencies():
            for unlooped_node in iter_unlooped_nodes(
                loop_variables_nodes=node['loop_variables'],
                node=node['expression'],
                ):
                dependencies = set(map(
                    itemgetter('value'),
                    iter_find_nodes(node=unlooped_node, type='symbol'),
                    ))
                yield unlooped_node, dependencies

        unlooped_loop_expressions_nodes, dependencies = zip(*iter_unlooped_loop_expressions_nodes_and_dependencies())
        dependencies = reduce(or_, dependencies)
        source = '[{}]'.format(
            ', '.join(map(node_to_python_source, unlooped_loop_expressions_nodes)),
            )
        global state
        state['current_formula'].append(dependencies)
        return source

    def loop_variable_to_python_source(node):
        return ' or '.join(
            '{} in {}'.format(
                node['name'],
                node_to_python_source(enumerations_node),
                )
            for enumerations_node in node['enumerations']
            )

    def pour_formula_to_python_source(node):
        for unlooped_formula_node in iter_unlooped_nodes(
            loop_variables_nodes=node['loop_variables'],
            node=node['formula'],
            unloop_keys=['name'],
            ):
            node_to_python_source(unlooped_formula_node)
        return None

    def product_expression_to_python_source(node):
        return infix_expression_to_python_source(node)

    def regle_to_python_source(node):
        for formula_node in node['formulas']:
            node_to_python_source(formula_node)
        return None

    def sum_expression_to_python_source(node):
        return infix_expression_to_python_source(node)

    def symbol_to_python_source(node):
        return sanitized_variable_name(node['value'])

    def ternary_operator_to_python_source(node):
        return '{} if {} else {}'.format(
            node_to_python_source(node['value_if_true'], parenthesised=True),
            node_to_python_source(node['condition'], parenthesised=True),
            node_to_python_source(node['value_if_false'], parenthesised=True) if 'value_if_false' in node else 0,
            )

    # End of specific transpilation functions, start of `node_to_python_source` function body

    global deep_level
    transpilation_function_name = node['type'] + '_to_python_source'
    if transpilation_function_name not in locals():
        error_message = '"def {}(node):" is not defined, node = {}'.format(
            transpilation_function_name,
            value_to_python_source(node),
            )
        raise NotImplementedError(error_message)
    nb_prefix_chars = len('DEBUG:' + script_name) + 1
    transpilation_function_short_name = transpilation_function_name[:-len('to_python_source') - 1]
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
    transpilation_function = locals()[transpilation_function_name]
    deep_level += 1
    try:
        source = transpilation_function(node)
    except (NotImplementedError, TranspilationError):
        # Bubble up all nested calls of node_to_python_source.
        raise
    except Exception:  # We really want to catch all exceptions to debug.
        raise TranspilationError(value_to_python_source(node))
    assert source is None or isinstance(source, str), (source, node)
    deep_level -= 1
    if source is not None and parenthesised and node['type'] not in ('integer', 'float', 'string', 'symbol'):
        source = '({})'.format(source)
    log.debug(
        '{}<={}= {}'.format(
            ' ' * deep_level * 4,
            deep_level,
            '' if source is None else textwrap.indent(source, prefix='> ')[1:].lstrip(),
            )
        )
    assert deep_level >= 0, deep_level
    return source


# Unloop functions


def enumeration_node_to_sequence(enumeration_node):
    if enumeration_node['type'] == 'enumeration_values':
        return enumeration_node['values']
    elif enumeration_node['type'] == 'interval':
        return range(enumeration_node['first'], enumeration_node['last'] + 1)
    else:
        raise NotImplementedError('Unknown type for enumeration_node = {}'.format(enumeration_node))


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


def iter_unlooped_nodes(node, loop_variables_nodes, unloop_keys=None):
    loop_variables_names, sequences = zip(*map(
        lambda loop_variable_node: (
            loop_variable_node['name'],
            mapcat(
                enumeration_node_to_sequence,
                loop_variable_node['enumerations'],
                ),
            ),
        loop_variables_nodes,
        ))
    loop_variables_values_list = itertools.product(*sequences)
    for loop_variables_values in loop_variables_values_list:
        value_by_loop_variable_name = dict(zip(loop_variables_names, loop_variables_values))
        yield unlooped(
            node=node,
            unloop_keys=unloop_keys,
            value_by_loop_variable_name=value_by_loop_variable_name,
            )


def unlooped(node, value_by_loop_variable_name, unloop_keys=None):
    """
    Replace loop variables names by values given by `value_by_loop_variable_name` in symbols recursively found
    in `node`.
    """
    new_node = copy.deepcopy(node)
    update_symbols(
        node=new_node,
        value_by_loop_variable_name=value_by_loop_variable_name,
        )
    if unloop_keys is not None:
        for key in unloop_keys:
            for loop_variable_name, loop_variable_value in value_by_loop_variable_name.items():
                new_node[key] = new_node[key].replace(loop_variable_name, str(loop_variable_value), 1)
    return new_node


def update_symbols(node, value_by_loop_variable_name):
    """
    This function mutates `node` and returns nothing. Better use the `unlooped` function.
    """
    if isinstance(node, dict):
        if node['type'] == 'symbol':
            for loop_variable_name, loop_variable_value in value_by_loop_variable_name.items():
                node['value'] = node['value'].replace(loop_variable_name, str(loop_variable_value), 1)
        else:
            update_symbols(
                node=list(node.values()),
                value_by_loop_variable_name=value_by_loop_variable_name,
                )
    elif isinstance(node, list):
        for child_node in node:
            update_symbols(
                node=child_node,
                value_by_loop_variable_name=value_by_loop_variable_name,
                )


# File transpilation functions


def load_chap_file(json_file_name):
    global args
    regles_nodes = filter(
        lambda node: args.application in node['applications'],
        read_ast_json_file(json_file_name),
        )
    for regle_node in regles_nodes:
        node_to_python_source(regle_node)


def tgvH_json_to_python_source(json_file_name):
    nodes = read_ast_json_file(json_file_name)
    variable_definition_by_name = {
        node['name']: node
        for node in nodes
        # if node['type'] in ('variable_calculee', 'variable_saisie')
        }
    global state
    state['variable_definition'] = variable_definition_by_name
    source = 'variable_definition_by_name = ' + value_to_python_source(variable_definition_by_name)
    return source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--application', default='batch', help='Application name')
    parser.add_argument('-d', '--debug', action='store_true', default=False, help='Display debug messages')
    parser.add_argument('-f', '--force', action='store_true', default=False, help='Transpile files which exist')
    parser.add_argument('--json', nargs='+', help='Transpile these JSON files only (give only file name)')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Increase output verbosity')
    parser.add_argument('json_dir', help='Directory containing the JSON AST files')
    global args
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.debug else (logging.INFO if args.verbose else logging.WARNING),
        stream=sys.stdout,
        )

    if args.json is not None:
        for json_file_name in args.json:
            json_file_path = os.path.join(args.json_dir, json_file_name)
            if not os.path.exists(json_file_path):
                parser.error('JSON file "{}" does not exist.'.format(json_file_path))

    if not os.path.isdir(generated_dir_path):
        os.mkdir(generated_dir_path)

    # chap-n

    source_by_chap_name = {}
    for json_file_path in sorted(glob.iglob(os.path.join(args.json_dir, 'chap-*.json'))):
        json_file_name = os.path.basename(json_file_path)
        file_name_head = os.path.splitext(json_file_name)[0]
        load_chap_file(json_file_name)

    # tgvH

    write_source(
        file_name='variables_definitions.py',
        json_file_name='tgvH.json',
        original_file_name='tgvH.m',
        transpilation_function=tgvH_json_to_python_source,
        )

    formulas_sources = []
    for formula_name, dependencies in state['formula_dependencies'].items():
        for dependency_name in dependencies:
            import ipdb; ipdb.set_trace()
            # if state['variable_definition'][dependency_name]['type'] == 'variable_calculee':

    return 0


if __name__ == '__main__':
    sys.exit(main())
