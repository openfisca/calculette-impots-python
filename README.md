# Calculette Impôts traduite en Python

## Installation

Le langage Python 3 est utilisé.

```
pip3 install --editable . --user
```

> L'option `--user` sert sur les systèmes GNU/Linux.

Un utilisateur plus expérimenté en Python peut utiliser
un [`virtualenv`](https://virtualenv.readthedocs.org/en/latest/) s'il le souhaite.

## Transpilation de l'AST JSON en Python

> Transpiler signifie compiler vers un autre langage de programmation.

Cette étape n'est utile que lorsque les fichiers JSON définissant l'AST changent.

```
python3 calculette_impots/scripts/json_ast_to_python.py /path/to/m-language-parser/json
```

## Utilisation

Exemple :

```
python3 calculette_impots/scripts/calculate.py PPE_SALAVDEFV
```

## Qualité du code

```
flake8 --max-line-length 120 .
```

## Simulateur en ligne

Pour comparer les résultats avec ceux du simulateur en ligne :
http://www3.finances.gouv.fr/calcul_impot/2015/simplifie/index.htm
