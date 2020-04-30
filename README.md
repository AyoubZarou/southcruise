**Installation**

##### Packages necessaires:
`pandas, numpy, django` à installer en utilisant le pip install de python (ie: `pip install django` ..)

##### Etapes pour lancer le serveur:
Pour lancer le serveur, il faudrait d'abord créer les bases de données et les populer, pour les créer les faudrait faire les 
migrations, ceci ce fait avec django sur la logne de commande comme suit:
```
python manage.py makemigrations
python manage.py migrate
```
La population des bases de données en suite se fait  en éxécutant les scripts `populate_databases.py`, `populate_registred_databses.py` et 
`set_country_notation.py`, les rôles sont les suivants:

`populate_databses.py`: mettre les données sur les pays et sur les startups dans la base de données
`populate_registred_databses`: mettre les données sur les entreprises cotées dans la base de données 
`set_country_notation.py`: mettre une notation par pays en cache, ceci étant en normalisant les données 
sur différents indices et les mettant sur la base de données pour chaque pays, pour que le notation finale des pays 
va être un aggrégat de ces données qui change en changeant le poids de chaque indice.
Ces deux étapes ne sont pas nécesaires comme il y a déjà une base de données sqlite populée dans la repo, elles ne sont pas possibles 
non plus comme les extraits excel et csv utilisés pour populer la base de données ne sont pas intégrées dans la répo
La prochaine étape est alors de lancer le serveur en local en utilisant toujours le système de management django 
```
python manage.py runserver
```
On va avoir ensuite un lien sur la ligne de commande à suivre pour accéder au site.


