#remplacer les * par son identifiant
from pymongo import MongoClient
from bson.objectid import ObjectId
c=MongoClient("mongo2.iem", port=27017, username="********", password="********",
authSource="********", authMechanism="SCRAM-SHA-1")
db=c.********
from pprint import pprint 

#affiche le nombre de billet vendus pour les films ayant une note > a 9
sommebillets = 0
films = db.CentreFilm.find({"notation": {"$gt": 9}})
for film in films:
    sommebillets += film.get("nbEntree", 0)

print("Le nombre total de billets vendus pour les films ayant une note supérieure à 9 est de:", int(sommebillets))