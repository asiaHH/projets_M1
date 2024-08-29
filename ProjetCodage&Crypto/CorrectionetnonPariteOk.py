import os
import binascii
import random
from collections import Counter

def calculer_parite(mot, positions):
    parite = 0
    for i in positions:
        parite += (mot >> i) & 1
    return parite % 2

def verifier_mot(mot, c):
    erreurs = 0
    positions = [[3, 2, 1], [3, 2, 0], [2, 1, 0]]
    for i in range(3):
        if calculer_parite(mot, positions[i]) != c[i]:
            erreurs |= 1 << i
    return erreurs

def verifier_mot_avec_parite(mot_avec_parite):
    mot = mot_avec_parite >> 3
    c = [(mot_avec_parite >> 2) & 1, (mot_avec_parite >> 1) & 1, mot_avec_parite & 1]
    return verifier_mot(mot, c)

def corriger_erreur(mot_avec_parite, erreurs):
    # Trouver l'index du bit erroné
    index_bit_erreur = 0
    if ((erreurs & (1 << 0)) and (erreurs & (1 << 1)) and not (erreurs & (1 << 2))):
        index_bit_erreur = 6  # Le bit d'information a1 est erroné
    elif ((erreurs & (1 << 0)) and (erreurs & (1 << 1)) and (erreurs & (1 << 2))):
        index_bit_erreur = 5  # Le bit d'information a2 est erroné
    elif ((erreurs & (1 << 0)) and not (erreurs & (1 << 1)) and (erreurs & (1 << 2))):
        index_bit_erreur = 4  # Le bit d'information a3 est erroné
    elif (not (erreurs & (1 << 0)) and (erreurs & (1 << 1)) and (erreurs & (1 << 2))):
        index_bit_erreur = 3  # Le bit d'information a4 est erroné

    # Inverser le bit erroné
    mot_avec_parite ^= (1 << index_bit_erreur)

    return mot_avec_parite

def verifier_fichier(nom_fichier):
    mots_corriges = {}
    with open(nom_fichier, "rb") as fichier:
        mot_avec_parite = 0
        nombre_bits = 0
        nombre_erreurs = 0

        while (bit := fichier.read(1)) != b'':
            mot_avec_parite = (mot_avec_parite << 1) | (bit[0] & 1)
            nombre_bits += 1

            if nombre_bits == 7:
                erreurs = verifier_mot_avec_parite(mot_avec_parite)
                if erreurs:
                    print(f"Le mot avec parité {mot_avec_parite:07b} a une erreur ", end='')
                    if erreurs & (1 << 0): print("c1 ", end='')
                    if erreurs & (1 << 1): print("c2 ", end='')
                    if erreurs & (1 << 2): print("c3 ", end='')
                    print()
                    # Détection du bit d'erreur dans le mot d'information
                    if ((erreurs & (1 << 0)) and (erreurs & (1 << 1)) and not (erreurs & (1 << 2))):
                        print("Le bit d'information a1 est erroné\n")
                    if ((erreurs & (1 << 0)) and (erreurs & (1 << 1)) and (erreurs & (1 << 2))):
                        print("Le bit d'information a2 est erroné\n")
                    if ((erreurs & (1 << 0)) and not (erreurs & (1 << 1)) and (erreurs & (1 << 2))):
                        print("Le bit d'information a3 est erroné\n")
                    if (not (erreurs & (1 << 0)) and (erreurs & (1 << 1)) and (erreurs & (1 << 2))):
                        print("Le bit d'information a4 est erroné\n")
                    print()
                    mot_avec_parite = corriger_erreur(mot_avec_parite, erreurs)
                    mots_corriges[mot_avec_parite] = mot_avec_parite
                    nombre_erreurs += 1

                mot_avec_parite = 0
                nombre_bits = 0

        print(f"Nombre total d'erreurs : {nombre_erreurs}")
        return mots_corriges

def copier_fichier(nom_fichier_source, nom_fichier_destination):
    with open(nom_fichier_source, "rb") as fichier_source, open(nom_fichier_destination, "w") as fichier_destination:
        mot_avec_parite = 0
        nombre_bits = 0

        while (bit := fichier_source.read(1)) != b'':
            mot_avec_parite = (mot_avec_parite << 1) | (bit[0] & 1)
            nombre_bits += 1

            if nombre_bits == 7:
                erreurs = verifier_mot_avec_parite(mot_avec_parite)
                if erreurs:
                    mot_avec_parite = corriger_erreur(mot_avec_parite, erreurs)
                # Supprimer les bits de parité
                mot_sans_parite = (mot_avec_parite & 0b01111000) >> 3
                # Écrire le mot sans les bits de parité en binaire dans le fichier de destination
                fichier_destination.write(f"{mot_sans_parite:04b}")

                mot_avec_parite = 0
                nombre_bits = 0

    print("Copie du fichier terminée avec succès.")

def copier_fichier_convertir_ascii(nom_fichier_source, nom_fichier_destination):
    with open(nom_fichier_source, "r") as fichier_source, open(nom_fichier_destination, "w") as fichier_destination:
        ascii_data = ""

        while (bits := fichier_source.read(8)) != '':
            # Convertir les bits en un entier en base 2
            entier = int(bits, 2)
            # Convertir l'entier en caractère ASCII
            caractere_ascii = chr(entier)
            ascii_data += caractere_ascii

        fichier_destination.write(ascii_data)

    print("Conversion du fichier en ASCII terminée avec succès.")

def dechiffrement_vigenere(texte_chiffre, cle):
    alphabet_maj = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alphabet_min = 'abcdefghijklmnopqrstuvwxyz'
    cle = cle.upper()
    texte_clair = '' #chaine avec aura le texte dechiffre
    index_cle = 0 #suit la position actuel ds la cle

    for i in range(len(texte_chiffre)): #parcourt la lettre chiffré
        if texte_chiffre[i].isalpha():  # permet d'ignorer les caractères non alphabétiques
            if texte_chiffre[i].isupper():
                alphabet = alphabet_maj
                if texte_chiffre[i] not in alphabet:  # si  caractère n'est pas dans l'alphabet,on l'ignore
                    continue
                index_chiffre = alphabet.find(texte_chiffre[i])
                index_cle_actuel = alphabet.find(cle[index_cle % len(cle)])
            else:
                alphabet = alphabet_min
                if texte_chiffre[i] not in alphabet: 
                    continue
                index_chiffre = alphabet.find(texte_chiffre[i])
                index_cle_actuel = alphabet.find(cle[index_cle % len(cle)].lower())

            # Calculer l'index de la lettre 
            index_texte = (index_chiffre - index_cle_actuel) % len(alphabet)

            
            texte_clair += alphabet[index_texte]

            
            index_cle += 1
        else:
            texte_clair += texte_chiffre[i]  # Ajouter les caractères non alphabétiques sans les changer

    return texte_clair


def copier_Vigenere(nom_fichier_source, nom_fichier_destination, cle):
    with open(nom_fichier_source, "r") as fichier_source, open(nom_fichier_destination, "w") as fichier_destination:
        texte_chiffre = fichier_source.read()
        texte_dechiffre = dechiffrement_vigenere(texte_chiffre, cle)
        fichier_destination.write(texte_dechiffre)

def string_to_bits(s):
    result = ''.join(format(c, '08b') for c in bytearray(s, "utf-8"))
    return result

def convert_file_to_binary(source_file, destination_file):
    with open(source_file, 'r') as f:
        text = f.read()

    binary_text = string_to_bits(text)

    with open(destination_file, 'w') as f:
        f.write(binary_text)




def generate_binary_key(n):

    binary_string = ''.join(random.choice('01') for _ in range(n))

    return binary_string

def vernam_cipher(text, key):
    return "".join(format(int(text[i:i+8], 2) ^ int(key[i:i+8], 2), '08b') for i in range(0, len(text), 8))


def vernam_cipher_file(source_file, destination_file, key_file):

    with open(source_file, 'r') as f:
        text = f.read()

    #genere la clé binaire de la même longueur que le texte
    key = generate_binary_key(len(text))

    # realise le chiffrement de vernam
    ciphered_text = vernam_cipher(text, key)

    
    with open(destination_file, 'w') as f:
        f.write(ciphered_text)

    
    with open(key_file, 'w') as f:
        f.write(key)


from collections import Counter

def count_occurrences(text):
    letters = [[0, chr(i)] for i in range(256)]
    for char in text:
        letters[ord(char)][0] += 1
    return letters #renvoie le nb d'occurences de chaque caracteres


def build_tree(letters):
    # parcourt chaque element de la liste letters et les ajoute dans la liste nodes sous forme de tuple
    nodes = [(k, v) for (k, v) in letters]
    # on prend les deux noeuds (ou feuilles) de frequence le plus faible on en fait un noeud, de poids la somme des deux petits poids
    # on boucle jusqu'a qu'il reste au moins 2 noeuds
    while len(nodes) >= 2:
        small_min = (0, nodes[0]) # noeud des frequence min
        big_min = (1, nodes[1])
        for i in range(2, len(nodes)):
            if nodes[i][0] <= small_min[1][0]:  #si le poids du noeud i est inferieur au poids du noeud small_min alors on echange les deux
                big_min = small_min
                small_min = (i, nodes[i])
            elif nodes[i][0] <= big_min[1][0]:  # sinon si le poids du noeud i est inferieur au poids du noeud big_min alors on echange les deux
                big_min = (i, nodes[i])
        new_node = ( # on cree un nouveau noeud avec les deux noeuds de frequence min
            small_min[1][0] + big_min[1][0],  
            nodes[small_min[0]], 
            nodes[big_min[0]]
        )
        #  on ajoute le nouveau noeud
        nodes[small_min[0]] = new_node
        nodes.pop(big_min[0])

    #si il reste un seul noeud alors on le renvoie 
    return nodes[0]


def create_dict(tree):
    dictionnaire = [("", tree)]
    dictionary = {}
    while dictionnaire:
        code, node = dictionnaire.pop(0)  # on prend le premier element de la liste dictionnaire et on le supprime
        if len(node) == 2:  # si c'est une feuille alors on ajoute la lettre et son code dans le dictionnaire
            dictionary[node[1]] = code  
        elif len(node) == 3:  # sinon on ajoute les deux fils du noeud dans la liste dictionnaire
            # Gauche -> 0, droite -> 1
            dictionnaire.append((code + "0", node[1]))# on ajoute le fils gauche du noeud dans la liste dictionnaire
            dictionnaire.append((code + "1", node[2]))
    return dictionary



def compress_file(input_file):
    with open(input_file, 'r') as f:
        text = f.read()

    occurrences = count_occurrences(text)
    tree = build_tree(occurrences)
    dictionary = create_dict(tree)
    compressed_text = "".join(dictionary[char] for char in text)

    return compressed_text, dictionary

############a decommenter pour la partie compression:
#input_file = "lettreResultatVigenere.txt" #le fichier a compresser

#compressed_text, dictionary = compress_file(input_file)

#with open(input_file, 'r') as f:
 #   text = f.read()

#print("Nombre de bits avant compression: {} bits / Nombre de bits après compression : {} bits".format(len(text) * 8, len(compressed_text)))













def main():
   mots_corriges = verifier_fichier("lettre.txt") #affiche la position des erreurs
   #copier_fichier("lettre.txt", "lettreResultatTEST.txt") #copie le fichier avec les erreurs corrigées et supp les bits de parite
    #copier_fichier_convertir_ascii("lettreResultatTEST.txt", "lettreResultatASCII.txt")
    
    #copier_Vigenere("lettreResultatASCII.txt", "lettreResultatVigenere.txt", "python")
   #convert_file_to_binary("lettreResultatVigenere.txt", "lettreConversionBinaire.txt")
   #vernam_cipher_file('lettreConversionBinaire.txt', 'lettreResultatVernam2.txt', 'CleVernam2.txt')
   
    #nom_fichier = "lettreResultatVigenere.txt" #derniere partie attention a bien decommente a partir de la ligne 270
    



if __name__ == "__main__":
    main()