#remplacer les * par son identifiant
from pymongo import MongoClient
from bson.objectid import ObjectId
c=MongoClient("mongo2.iem", port=27017, username="********", password="********",
authSource="********", authMechanism="SCRAM-SHA-1")
db=c.******** 
from pprint import pprint 

# affiche la moyenne des commentaires des films
films = db.CentreFilm.find()# Récupérer la collection de films
# Initialiser le total des notes et le nombre de commentaires
sommenotes = 0
nbcommentaires = 0

# Parcourir chaque film dans la collection
for film in films:
    # Vérifier si le film a des commentaires
    if 'commentaires' in film:
        # Parcourir chaque commentaire dans le film
        for commentaire in film['commentaires']:
            # Vérifier si le commentaire a une note
            if 'note' in commentaire:
                sommenotes += commentaire['note']
                nbcommentaires += 1
# calcul moyenne des notes si des commentaires avec des notes ont été trouvés
if nbcommentaires != 0:
    moyenne = sommenotes / nbcommentaires
    print("Le total des notes est de :", sommenotes)
    print("Le nombre de commentaires avec des notes est de :", nbcommentaires)
    print("La moyenne des notes des commentaires est de :", moyenne)
else:
    print("Aucun commentaire avec une note n'a été trouvé.")
