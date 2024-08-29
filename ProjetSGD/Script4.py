#remplacer les * par son identifiants
from pymongo import MongoClient
from bson.objectid import ObjectId
c=MongoClient("mongo2.iem", port=27017, username="********", password="********",
authSource="********", authMechanism="SCRAM-SHA-1")
db=c.******** 
from pprint import pprint 

#affiche la moyenne des notes des films
films = db.CentreFilm.find()# Récupérer la collection de films

sommenotes = 0
nbfilms = 0
# parcourt chaque film et calcul la somme des notes
for film in films:
    sommenotes += film.get('notation', 0)  # ajout note du film a la somme
    nbfilms += 1  # incrémente le nombre de films
# calcul moyenne des notes
if nbfilms > 0:
    moyenne = sommenotes / nbfilms
    print("La moyenne des notes des films est de:", moyenne)
else:
    print("Aucun film trouvé.")
