# Calculateur Impôts en Python

## Installation

Le langage Python 3 est utilisé.

```
pip3 install --editable . --user
```

> L'option `--user` sert sur les systèmes GNU/Linux.

Un utilisateur plus expérimenté en Python peut utiliser
un [`virtualenv`](https://virtualenv.readthedocs.org/en/latest/) s'il le souhaite.

## Utilisation

Exemple :

```
$ python3 calculateur_impots/scripts/calculate.py PPE_SALAVDEFV
```

## Transpilation de l'AST JSON en Python

> Transpiler signifie compiler vers un autre langage de programmation.

Cette étape n'est utile que lorsque les fichiers JSON définissant l'AST changent.

```
$ python3 calculateur_impots/scripts/json_ast_to_python.py /path/to/m-language-parser/json
```

## Qualité du code

```
$ flake8 --max-line-length 120 .
```
