# Calculette Impôts traduite en Python

## Installation

Le langage Python 3 est utilisé.

Il est nécessaire d'avoir au préalable installé le paquet [calculette-impots-m-language-parser](https://git.framasoft.org/openfisca/calculette-impots-m-language-parser).

Puis installer ce paquet :

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
python3 calculette_impots/scripts/json_ast_to_python.py /path/to/calculette-impots-m-language-parser/json
```

## Utilisation

Ce paquet installe une commande `calculette-impots`.

Sans argument, `calculette-impots` calcule toutes les variables restituée,
sans remplir aucune case de la déclaration. Cela équivaut à un célibataire sans enfants et sans revenu.

Il faut tout de même préciser une variable de saisie spéciale (`V_ANREV` pour "Annee des revenus") pour laquelle
on donne la valeur `2014` car ici on calcule les impôts de 2015 sur les revenus de 2014.

De plus, pour l'instant, on peut passer une autre option (`--no-verifs`) à la commande `calculette-impots`
pour ignorer les "vérifs", qui sont des tests validant la cohérence des calculs.

```
$ calculette-impots --saisies V_ANREV=2014 --no-verifs
SEUILCIIMSI = 13956 (donnee equipe batch pour CNTDF : seuil imposition  tx normal CSG)
SEUILCIRIRF = 10676 (donnee equipe batch pour CNTDF : seuil imposition CSG CRDS)
PPENBJ = 360 (PPE:NOMBRE DE JOURS DE LA PERIODE)
TXTO = 80 (TAUX TO RESTITUE)
TXREGV = 80 (TAUX interets de retard + majo Regul assurance vie - 'avis)
ABSPE = 9 (indicateur abattements speciaux personnes agees)
INDGARD = 9 (Indicateur de plafonnement de frais de garde (AGARD))
MESGOUV2 = 6 (Indicateur beneficiaire mesures fiscales bas de bareme (simulateur))
MESGOUV = 3 (Indicateur beneficiaire des mesures fiscales de bas de bareme)
INDCEX = 3 (Indicateur Brav pour restit non imp presqu imposable et autre )
[...]
```

Les résultats sont triés par ordre décroissant sur les valeurs.
La sortie est coupée pour ne pas surcharger le README.

On peut changer le format de sortie en précision l'option `--output-format`, par exemple en JSON comme ceci :

```
$ calculette-impots --saisies V_ANREV=2014 --output-format=json --no-verifs
{"results": {"ABSPE": 9, "APPLI_BATCH": 1, "CIIMSI": 2, "CIRIRF": 2, "IND12": 3, "IND61IR": 3, "IND61PS": 3, "INDCEX": 3, "INDEFTS1": 1, "INDEFTS2": 1, "INDEFTS3": 1, "INDEFTS4": 1, "INDEFTSC": 1, "INDEFTSV": 1, "INDEXOGEN": 1, "INDGARD": 9, "INDIRPS": 1, "LIG1": 1, "LIG10": 1, "LIG10C": 1, "LIG10P": 1, "LIG10V": 1, "LIG2": 1, "LIG2052": 1, "LIG2501": 1, "LIGLOCSEUL": 1, "LIGNEMP": 1, "MESGOUV": 3, "MESGOUV2": 6, "NATMAJ": 1, "NATMAJC": 1, "NATMAJCDIS": 1, "NATMAJCVN": 1, "NATMAJGLOA": 1, "NATMAJP": 1, "NATMAJR": 1, "NATMAJREGV": 1, "NATMAJRSE1": 1, "NATMAJRSE2": 1, "NATMAJRSE3": 1, "NATMAJRSE4": 1, "NATMAJRSE5": 1, "NBFOTH": 1, "NBPT": 1.0, "NONLIGPS": 1, "PPENBJ": 360, "SEUILCIIMSI": 13956, "SEUILCIRIRF": 10676, "TXREGV": 80, "TXTO": 80}}
```

Le JSON résultant étant très compact on peut utiliser un outil comme [`jq`](https://stedolan.github.io/jq/)
pour le manipuler.

> À noter qu'avec la sortie au format JSON les résultats ne sont pas triés par valeur
> mais les clés du JSON sont triées par ordre alphabétique.

On peut demander à calculer seulement une ou plusieurs variables en particulier :

```
$ calculette-impots --saisies V_ANREV=2014 --calculees PPENBJ --no-verifs
PPENBJ = 360 (PPE:NOMBRE DE JOURS DE LA PERIODE)

$ calculette-impots --saisies V_ANREV=2014 --calculees PPENBJ LIGNEMP --no-verifs
PPENBJ = 360 (PPE:NOMBRE DE JOURS DE LA PERIODE)
LIGNEMP = 1 (Indicateur ligne impot net)
```

## Cas-types

Testons d'autres cas-types.

- Un célibataire sans enfants gagnant 10000€ par an
```
$ calculette-impots --saisies V_ANREV=2014 TSHALLOV=10000 --no-verifs --calculees IRN
IRN = 0 (Impot net ou restitution nette)
```
- Un célibataire sans enfants gagnant 30000€ par an
```
$ calculette-impots --saisies V_ANREV=2014 TSHALLOV=30000 --no-verifs --calculees IRN
IRN = 2461 (Impot net ou restitution nette)
```
- Un couple non marié sans enfants dont le déclarant 1 gagne 10000€ par an et le déclarant 2 gagne 20000€ par an
```
$ calculette-impots --saisies V_ANREV=2014 TSHALLOV=10000 TSHALLOC=20000 --no-verifs --calculees IRN
IRN = 2461 (Impot net ou restitution nette)
```
> Note: ce couple est censé remplir deux déclarations, la situation simulée ici n'est pas correcte et c'est la désactivation des vérifications qui rend possible ce calcul.

- Un couple marié (date du mariage `05/05/1980`) sans enfants dont le déclarant 1 gagne 10000€ par an et le déclarant 2 gagne 20000€ par an
```
$ calculette-impots --saisies V_ANREV=2014 TSHALLOV=10000 TSHALLOC=20000 V_0AM=1 V_0AX=05051980 --no-verifs --calculees IRN
IRN = 264 (Impot net ou restitution nette)
```

## Simulateur en ligne

Pour comparer les résultats avec ceux du simulateur en ligne :
http://www3.finances.gouv.fr/calcul_impot/2015/simplifie/index.htm

## Qualité du code

```
flake8 --max-line-length 120 .
```
