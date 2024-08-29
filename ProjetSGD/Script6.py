
#remplacer les * par son identifiant 
from pymongo import MongoClient
from bson.objectid import ObjectId
c=MongoClient("mongo2.iem", port=27017, username="********", password="********",
authSource="********", authMechanism="SCRAM-SHA-1")
db=c.********
from pprint import pprint 

#affiche des infos sur un film selon demande user
def afficher_info_film(film_id):
    film = db.CentreFilm.find_one({"id": film_id}) #recherche le film dans la collection en fonction de l'ID
    
    
    if film:#si le film existe
        print(f"Le film \"{film['titre']}\" raconte l'histoire \"{film['description']}\".")
        print(f"Le prix du billet pour ce film est de {film['prixBillet']} euros.")
        print(f"Il dure {film['duree']} heures.")
        print(f"Le genre est \"{film['genre']}\".")
        print(f"L'heure de diffusion est \"{film['heure']}\".")
        print("Les salles de diffusion sont :")
        for salle in film['salles']:
            print(f"- Salle {int(salle['numero'])}")
    else:
        print("Aucun film trouvé avec cet ID.")

def demander_autre_film():
    reponse = input("Souhaitez-vous obtenir des informations sur un autre film ? (oui/non): ")
    return reponse.lower() == 'oui'

while True:
    film_id = input("Entrez l'ID du film (10, 20, 30 ou 40) : ")

    if film_id in ['10', '20', '30', '40']:# verifie si id valide
        film_id = int(film_id)# convertit id en entier

        afficher_info_film(film_id)# affiche infos du film correspondant

        if not demander_autre_film(): # si user ne veut pas d'autres infos
            print("Au revoir !")
            break
    else:
        print("ID invalide. Veuillez entrer un ID parmi 10, 20, 30 ou 40.")