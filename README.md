# Calculateur Impôts en Python

Ce projet utilise le langage Python 3.

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
