#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Use finances.gouv.fr web simulator as an API to compute income taxes.

Based on a script by Adrien Fabre in [OpenFisca-France](https://github.com/openfisca/openfisca-france).
"""


import argparse
import json
import re
import sys

from lxml import etree
from toolz import merge
import requests


parser = None


def iter_results(root_node):
    ignored_input_hidden_names = (
        'blanc',  # white line only used for presentation
        'mesgouv2',  # explanations text block
        )
    for element in root_node.xpath('//input[@type="hidden"][@name]'):
        element_name = element.get('name').strip()
        if element_name in ignored_input_hidden_names:
            continue
        parent = element.getparent()
        parent_tag = parent.tag.lower()
        if parent_tag == 'table':
            tr = parent[parent.index(element) - 1]
            assert tr.tag.lower() == 'tr', tr
        else:
            assert parent_tag == 'tr', parent_tag
            tr = parent
        while True:
            description = etree.tostring(tr[1], encoding=str, method='text').strip().rstrip(u'*').strip()
            if description:
                break
            table = tr.getparent()
            tr = table[table.index(tr) - 1]
        yield {
            'name': element_name,
            'description': description,
            'value': float(element.get('value').strip()),
            }


def iter_saisie_variables(values):
    for value, words in map(lambda value: (value, value.strip('=').split('=', 1)), values):
        if len(words) == 1:
            parser.error('Missing value for variable saisie: "{}"'.format(value))
        elif len(words) > 2:
            parser.error('Invalid syntax for variable saisie: "{}"'.format(value))
        variable_name, variable_value = words
        variable_value = str(variable_value)
        yield variable_name, variable_value


def main():
    global parser
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-html', help='Output result page HTML to file')
    parser.add_argument('--saisies', dest='saisie_variables', metavar='nom=valeur', nargs='+', help='Variables saisies')
    parser.add_argument('--year', default='2015', type=int,
                        help='Calculer les impôts de l\'année N sur les revenus de l\'année N-1')
    args = parser.parse_args()

    cgi_url = 'http://www3.finances.gouv.fr/cgi-bin/calc-{}.cgi'.format(args.year)
    headers = {'User-Agent': 'Calculette-Impots-Python'}
    saisie_variables = {} if args.saisie_variables is None else dict(iter_saisie_variables(args.saisie_variables))
    default_saisie_variables = {
        # '0DA': '1965',
        # '1AJ': '15000',
        'pre_situation_famille': 'C',
        'pre_situation_residence': 'M',
        # 'simplifie': '1',
        }
    data = merge(default_saisie_variables, saisie_variables)
    response = requests.post(cgi_url, headers=headers, data=data)
    if args.output_html is not None:
        with open(args.output_html, 'w') as output_html_file:
            output_html_file.write(re.sub(
                pattern=r'=(.)/calcul_impot/2015/',
                repl=r'=\1http://www3.finances.gouv.fr/calcul_impot/2015/',
                string=response.text,
                ))
    root_node = etree.fromstring(response.text, etree.HTMLParser())
    results = list(iter_results(root_node))
    print(json.dumps(results, ensure_ascii=False, indent=2, sort_keys=True))

    return 0


if __name__ == "__main__":
    sys.exit(main())
