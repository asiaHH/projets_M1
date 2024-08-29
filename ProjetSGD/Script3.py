#remplacer les * par son identifiant
from pymongo import MongoClient
from bson.objectid import ObjectId
c=MongoClient("mongo2.iem", port=27017, username="********", password="********",
authSource="********", authMechanism="SCRAM-SHA-1")
db=c.********
from pprint import pprint 

films = db.CentreFilm.find()# recupere la collection de films
# affiche le pourcentage des acteurs ayant plus de 60 ans
sommeacteurs = 0
acteursPlus60 = 0

for film in films:
    for acteur in film['acteurs']:
        pprint(acteur)
        sommeacteurs += 1
        if acteur.get('age', 0) > 60:  # verifie si l'âge de l'acteur est > a 60 ans
            acteursPlus60 += 1

if sommeacteurs != 0:
    pourcentage = (acteursPlus60 / sommeacteurs) * 100
    print("Le pourcentage des acteurs ayant plus de 60 ans dans toute la collection est d'environs :", int(pourcentage), "%")
else:
    print("Aucun acteur trouvé dans la collection.")
