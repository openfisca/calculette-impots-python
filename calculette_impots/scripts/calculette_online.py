#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Use finances.gouv.fr web simulator as an API to compute income taxes.

Based on a script by Adrien Fabre in [OpenFisca-France](https://github.com/openfisca/openfisca-france).
"""


import json
import sys

import requests
from lxml import etree


def iter_results(root_node):
    for element in root_node.xpath('//input[@type="hidden"][@name]'):
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
            'name': element.get('name').strip(),
            'description': description,
            'value': float(element.get('value').strip()),
            }


def main():
    cgi_url = 'http://www3.finances.gouv.fr/cgi-bin/calc-2014.cgi'
    headers = {'User-Agent': 'Calculette-Impots-Python'}
    data = {
        '0DA': '1965',
        '1AJ': '15000',
        'pre_situation_famille': 'C',
        'pre_situation_residence': 'M',
        # 'simplifie': '1',
        }
    response = requests.post(cgi_url, headers=headers, data=data)
    root_node = etree.fromstring(response.text, etree.HTMLParser())
    results = list(iter_results(root_node))
    print(json.dumps(results, ensure_ascii=False, indent=2, sort_keys=True))

    return 0


if __name__ == "__main__":
    sys.exit(main())
