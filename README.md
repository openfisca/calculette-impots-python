# Calculette Impôts traduite en Python

## Installation

Le langage Python 3 est utilisé.

Il est nécessaire d'avoir au préalable installé le paquet [calculette-impots-m-language-parser](https://git.framasoft.org/openfisca/calculette-impots-m-language-parser).

Ce paquet n'est pas publié sur le dépôt [PyPI](https://pypi.python.org/pypi) donc pour l'installer il faut passer par `git clone`.

```
git clone https://git.framasoft.org/openfisca/calculette-impots-python.git
cd calculette-impots-python
pip3 install --editable . --user
```

> L'option `--user` sert sur les systèmes GNU/Linux.

Un utilisateur plus expérimenté en Python peut utiliser
un [`virtualenv`](https://virtualenv.readthedocs.org/en/latest/) s'il le souhaite.

## Utilisation

Ce paquet installe une commande `calculette-impots` dans votre répertoire utilisateur.
Cela signifie que vous pouvez la taper dans un terminal et elle sera reconnue, sauf si elle a été installée
en dehors du "PATH".

Cette commande accepte des sous-commandes. Voyons son utilisation :

```
$ calculette-impots
Usage:
  calculette-impots calculate [--no-verifs] VARIABLE...
  calculette-impots info VARIABLE...
  calculette-impots (-h | --help)
  calculette-impots --version
```

### La sous-commande `info`

La sous-commande `info` permet d'afficher des informations sur les variables, en particulier leur type,
quelques attributs, leurs éventuelles dépendances et dépendances inverses.

Exemple :

```
$  $ calculette-impots info TSHALLOV
{
  "TSHALLOV": {
    "variable_definition": {
      "alias": "1AJ",
      "attributes": {
        "acompte": 1,
        "avfisc": 0,
        "categorie_TL": 20,
        "classe": 0,
        "cotsoc": 5,
        "ind_abat": 1,
        "nat_code": 0,
        "priorite": 10,
        "rapcat": 4,
        "sanction": 8
      },
      "description": "Salaires - Declarant 1",
      "name": "TSHALLOV",
      "restituee": true,
      "subtype": "revenu",
      "tgvh_linecol": [
        13637,
        1
      ],
      "type": "variable_saisie"
    },
    "variable_reverse_dependencies": [
      "ABTS1AJ",
      "INDPPEV",
      "INDREV1A8IR",
      [...]
    ]
  }
}
```

Certains bouts ont été coupés pour ne pas polluer le README.

Ceci était une variable de saisie mais on peut également obtenir des infos les variables calculées.

### La sous-commande `calculate`

Sans argument, la sous-commande `calculate` calcule toutes les variables restituées,
sans remplir aucune case de la déclaration. Cela équivaut à un célibataire sans enfants et sans revenu.

Il faut tout de même préciser une variable de saisie spéciale (`V_ANREV` pour "Annee des revenus") pour laquelle
on donne la valeur `2014` car ici on calcule les impôts de 2015 sur les revenus de 2014.
Si on ne le fait pas un "warning" nous le rappelle.

De plus, pour l'instant, on peut passer une autre option (`--no-verifs`) à la commande `calculette-impots`
pour ignorer les "vérifs", qui sont des tests validant la cohérence des calculs.

```
$ calculette-impots calculate V_ANREV=2014 --no-verifs
{
  "calculate_results": {
    "ABSPE": 9,
    "APPLI_BATCH": 1,
    "CIIMSI": 2,
    "CIRIRF": 2,
    [...]
  }
}
```

Le JSON de sortie est coupé ici pour ne pas surcharger le README.
Pour info on peut utiliser un outil comme [`jq`](https://stedolan.github.io/jq/) pour le manipuler.

Ceci était une simulation à vide, maintenant il serait intéressant de remplir les cases de la déclaration d'impôts.

## Cas-types

Tout d'abord il faut savoir qu'on peut demander à calculer une ou plusieurs variables en particulier.
Pour cela il suffit d'ajouter le nom des variables mais sans le signe "=".

```
$ calculette-impots calculate V_ANREV=2014 IRN IDRS2 --no-verifs
{
  "calculate_results": {
    "IDRS2": 0,
    "IRN": 0
  }
}
```

Il faut aussi savoir que la variable `IRN` correspond (grosso-modo) à l'impôt total. C'est pour cela qu'on la demande.

Testons à présent quelques cas-types.

- Un célibataire sans enfants gagnant 10000€ par an
```
$ calculette-impots calculate V_ANREV=2014 TSHALLOV=10000 IRN --no-verifs
{
  "calculate_results": {
    "IRN": 0
  }
}
```
- Un célibataire sans enfants gagnant 30000€ par an
```
$ calculette-impots calculate V_ANREV=2014 TSHALLOV=30000 IRN --no-verifs
{
  "calculate_results": {
    "IRN": 2461
  }
}
```
- Un couple marié (date du mariage 05/05/1980) sans enfants dont le déclarant 1 gagne 10000€ par an et le déclarant 2 gagne 20000€ par an
```
$ calculette-impots calculate V_ANREV=2014 TSHALLOV=10000 TSHALLOC=20000 V_0AM=1 V_0AX=05051980 IRN --no-verifs
{
  "calculate_results": {
    "IRN": 264
  }
}
```

## Simulateur en ligne

Pour comparer les résultats avec ceux du simulateur en ligne :
http://www3.finances.gouv.fr/calcul_impot/2015/simplifie/index.htm

Un script permet d'appeler le simulateur en ligne :

```
python3 calculette_impots/scripts/calculette_online.py
```

Cependant il n'est pas peaufiné au point d'accepter des arguments sur la ligne de commande.
Il faut donc l'éditer pour changer les valeurs.

De plus, les noms des variables ne sont pas les mêmes que dans le code source en langage M.
Ici ce sont les "aliases" qui sont définis dans le fichier `tgvH.m` (dans le projet [m-source-code](https://git.framasoft.org/openfisca/calculette-impots-m-source-code)).

Les contributions sont les bienvenues !

## Transpilation de l'AST JSON en Python

> Transpiler signifie compiler vers un autre langage de programmation.

Cette étape n'est utile que lorsque les fichiers JSON définissant l'AST changent.
Ceux-ci sont dans le dépôt [m-language-parser](https://git.framasoft.org/openfisca/calculette-impots-m-language-parser).

```
python3 calculette_impots/scripts/json_ast_to_python.py /path/to/calculette-impots-m-language-parser/json
```

## Qualité du code

```
flake8 --max-line-length 120 .
```
