import csv
import os
import argparse
from typing import List, Dict

# Constantes pour les chemins par défaut
REPERTOIRE_DONNEES = "data"
FICHIER_FUSIONNE = "inventaire_fusionne.csv"

def confirmer_parametres(parametres: str) -> bool:
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

    Raises:
        ValueError: Si le fichier source est vide.
    """
    resume = {}

    with open(chemin_fichier, 'r', newline='') as fichier:
        lecteur = csv.DictReader(fichier)
        lignes = list(lecteur)
        if not lignes:
            raise ValueError(f"Le fichier source {chemin_fichier} est vide.")

        for ligne in lignes:
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
    """
    Point d'entrée principal. Fonctionne en ligne de commande avec un shell interactif en cas d'erreur.
    """
    global REPERTOIRE_DONNEES, FICHIER_FUSIONNE

    # Configuration des arguments via argparse
    parser = argparse.ArgumentParser(description="Automatisez la gestion de l'inventaire.")
    parser.add_argument("action", choices=["consolider", "chercher", "résumer"],
                        help="Action à effectuer : consolider, chercher ou résumer.")
    parser.add_argument("-d", "--data-directory", default=REPERTOIRE_DONNEES,
                        help="Répertoire contenant les fichiers CSV.")
    parser.add_argument("-o", "--output-file", default=FICHIER_FUSIONNE,
                        help="Chemin du fichier fusionné.")
    parser.add_argument("-c", "--critere", help="Critère de recherche pour l'action 'chercher' (ex : category=Electronics).")
    args = parser.parse_args()

    # Confirmation interactive
    parametres = f"Action : {args.action}, Répertoire : {args.data_directory}, Fichier : {args.output_file}"
    if not confirmer_parametres(parametres):
        REPERTOIRE_DONNEES = input("Entrez le nouveau répertoire des données : ")
        FICHIER_FUSIONNE = input("Entrez le nouveau fichier de sortie : ")
        args.data_directory = REPERTOIRE_DONNEES
        args.output_file = FICHIER_FUSIONNE

    # Exécution des actions en fonction de l'argument "action"
    if args.action == "consolider":
        fusionner_fichiers(args.data_directory, args.output_file)

    elif args.action == "chercher":
        if not args.critere:
            print("Vous devez fournir un critère de recherche avec --critere.")
        else:
            cle, valeur = args.critere.split("=")
            resultats = rechercher_inventaire(args.output_file, **{cle: valeur})
            print("Résultats de recherche :", resultats)

    elif args.action == "résumer":
        try:
            generer_resume(args.output_file, "rapport_resume.csv")
        except ValueError as e:
            print(f"Erreur lors de la génération du résumé : {e}")


if __name__ == "__main__":
    main()
