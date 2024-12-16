import csv
import os
from typing import List, Dict

# Constantes pour les chemins des fichiers
REPERTOIRE_DONNEES = "data"
FICHIER_FUSIONNE = "inventaire_fusionne.csv"


def confirmer_parametres(parametres: str):
    """
    Demande à l'utilisateur de confirmer les paramètres fournis.

    Args:
        parametres (str): Description des paramètres à confirmer.

    Returns:
        bool: True si l'utilisateur confirme, False sinon.
    """
    print(f"Est-ce bien ces paramètres : {parametres} ?")
    print("1. Oui")
    print("2. Non")
    choix = input("Répondez 1 ou 2 : ")
    return choix == "1"


def fusionner_fichiers(repertoire: str, fichier_sortie: str):
    """
    Fusionne plusieurs fichiers CSV en un fichier unique.

    Args:
        repertoire (str): Chemin du répertoire contenant les fichiers CSV.
        fichier_sortie (str): Chemin du fichier CSV fusionné.
    """
    donnees_fusionnees = []

    # Lecture de tous les fichiers CSV dans le répertoire
    for nom_fichier in os.listdir(repertoire):
        chemin_fichier = os.path.join(repertoire, nom_fichier)
        if nom_fichier.endswith('.csv'):
            with open(chemin_fichier, 'r', newline='') as fichier:
                lecteur = csv.DictReader(fichier)
                for ligne in lecteur:
                    donnees_fusionnees.append(ligne)

    if donnees_fusionnees:
        # Écriture des données fusionnées dans le fichier de sortie
        with open(fichier_sortie, 'w', newline='') as fichier:
            ecrivain = csv.DictWriter(fichier, fieldnames=donnees_fusionnees[0].keys())
            ecrivain.writeheader()
            ecrivain.writerows(donnees_fusionnees)
        print(f"Fusion terminée. Données enregistrées dans {fichier_sortie}")
    else:
        print("Aucune donnée à fusionner.")


def rechercher_inventaire(chemin_fichier: str, **filtres) -> List[Dict[str, str]]:
    """
    Recherche dans l'inventaire en fonction des filtres fournis.

    Args:
        chemin_fichier (str): Chemin du fichier CSV fusionné.
        **filtres: Paires clé-valeur pour filtrer les données.

    Returns:
        List[Dict[str, str]]: Liste des lignes correspondantes.
    """
    resultats = []

    with open(chemin_fichier, 'r', newline='') as fichier:
        lecteur = csv.DictReader(fichier)
        for ligne in lecteur:
            correspondance = all(str(ligne[cle]) == str(valeur) for cle, valeur in filtres.items() if cle in ligne)
            if correspondance:
                resultats.append(ligne)

    return resultats


def generer_resume(chemin_fichier: str, fichier_sortie: str):
    """
    Génère un rapport récapitulatif et l'exporte en CSV.

    Args:
        chemin_fichier (str): Chemin du fichier CSV fusionné.
        fichier_sortie (str): Chemin du fichier de sortie.
    """
    resume = {}

    with open(chemin_fichier, 'r', newline='') as fichier:
        lecteur = csv.DictReader(fichier)
        for ligne in lecteur:
            categorie = ligne.get('category', 'Inconnu')
            quantite = int(ligne.get('quantity', 0))
            prix = float(ligne.get('price', 0))

            if categorie not in resume:
                resume[categorie] = {'quantite_totale': 0, 'valeur_totale': 0}

            resume[categorie]['quantite_totale'] += quantite
            resume[categorie]['valeur_totale'] += quantite * prix

    # Écriture du résumé dans le fichier de sortie
    with open(fichier_sortie, 'w', newline='') as fichier:
        ecrivain = csv.DictWriter(fichier, fieldnames=['categorie', 'quantite_totale', 'valeur_totale'])
        ecrivain.writeheader()
        for categorie, donnees in resume.items():
            ecrivain.writerow({
                'categorie': categorie,
                'quantite_totale': donnees['quantite_totale'],
                'valeur_totale': donnees['valeur_totale']
            })
    print(f"Rapport récapitulatif généré : {fichier_sortie}")


def main():
    # Demander confirmation des paramètres
    parametres = f"Répertoire des données : {REPERTOIRE_DONNEES}, Fichier fusionné : {FICHIER_FUSIONNE}"
    if not confirmer_parametres(parametres):
        print("Veuillez relancer le programme avec les bons paramètres.")
        exit()

    # Assurer l'existence du répertoire
    os.makedirs(REPERTOIRE_DONNEES, exist_ok=True)

    # Fusionner les fichiers CSV
    fusionner_fichiers(REPERTOIRE_DONNEES, FICHIER_FUSIONNE)

    # Rechercher des produits spécifiques
    resultats_recherche = rechercher_inventaire(FICHIER_FUSIONNE, category="Electronics")
    print("Résultats de recherche :", resultats_recherche)

    # Générer un résumé
    generer_resume(FICHIER_FUSIONNE, "rapport_resume.csv")

if __name__ == "__main__":
    main()
