import csv
import os
import argparse
from typing import List, Dict

# Constantes pour les chemins par défaut
REPERTOIRE_DONNEES = "csv"
FICHIER_FUSIONNE =  "output/inventaire_fusionne.csv"


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


def rechercher_inventaire(chemin_fichier: str, filtre) -> List[Dict[str, str]]:
    """
    Recherche dans l'inventaire en fonction des filtres fournis.

    Args:
        chemin_fichier (str): Chemin du fichier CSV fusionné.
        filtre: tuple clé, valeur pour filtrer les données.
    """
    resultats = []
    print(chemin_fichier)
    with open(chemin_fichier, 'r', newline='') as fichier:
        lecteur = csv.DictReader(fichier, delimiter=';')
        if filtre[0] not in lecteur.fieldnames:
            raise KeyError(f"Clé '{filtre[0]}' non trouvée dans le fichier CSV.")
        for ligne in lecteur:
            if str(ligne[filtre[0]]) == str(filtre[1]):
                resultats.append(ligne)

    print(f"{'Nom':<20} | {'Quantité':<10} | {'Prix (€)':<10} | {'Catégorie':<15}")
    print("-" * 60)
    for ligne in resultats:
        print(f"{ligne['name']:<20} | {ligne['quantity']:<10} | {ligne['price']:<10} | {ligne['category']:<15}")


def fusionner_fichiers(repertoire: str, fichier_sortie: str):
    """
    Fusionne plusieurs fichiers CSV en un fichier unique.

    Args:
        repertoire (str): Chemin du répertoire contenant les fichiers CSV.
        fichier_sortie (str): Chemin du fichier CSV fusionné.
    """
    donnees_fusionnees = []
    colonnes_attendues = ["name", "quantity", "price", "category"]

    # Lecture de tous les fichiers CSV dans le répertoire
    for nom_fichier in os.listdir(repertoire):
        chemin_fichier = os.path.join(repertoire, nom_fichier)
        if nom_fichier.endswith('.csv'):
            with open(chemin_fichier, 'r', newline='', encoding='utf-8') as fichier:
                lecteur = csv.DictReader(fichier, delimiter=";")
                # Vérifier si les colonnes correspondent
                if lecteur.fieldnames != colonnes_attendues:
                    print(f"Les colonnes du fichier {nom_fichier} ne correspondent pas aux colonnes attendues.")
                    print(f"Colonnes trouvées : {lecteur.fieldnames}")
                    print(f"Colonnes attendues : {colonnes_attendues}")
                    continue
                for ligne in lecteur:
                    donnees_fusionnees.append(ligne)

    if donnees_fusionnees:
        # Écriture des données fusionnées dans le fichier de sortie
        with open(fichier_sortie, 'w', newline='', encoding='utf-8') as fichier:
            ecrivain = csv.DictWriter(fichier, fieldnames=colonnes_attendues, delimiter=";")
            ecrivain.writeheader()
            ecrivain.writerows(donnees_fusionnees)
        print(f"Fusion terminée. Données enregistrées dans {fichier_sortie}")
    else:
        print("Aucune donnée valide à fusionner.")


def generer_resume(chemin_fichier: str, fichier_sortie: str):
    """
    Génère un rapport récapitulatif et l'exporte en CSV.

    Args:
        chemin_fichier (str): Chemin du fichier CSV fusionné.
        fichier_sortie (str): Chemin du fichier de sortie.

    Raises:
        ValueError: Si le fichier source est vide ou mal formaté.
    """
    resume = {}

    with open(chemin_fichier, 'r', newline='', encoding='utf-8') as fichier:
        lecteur = csv.DictReader(fichier, delimiter=";")
        colonnes_attendues = ["name", "quantity", "price", "category"]

        # Vérifier si les colonnes correspondent
        if lecteur.fieldnames != colonnes_attendues:
            raise ValueError(f"Les colonnes du fichier source ne correspondent pas aux colonnes attendues.\n"
                             f"Colonnes trouvées : {lecteur.fieldnames}\n"
                             f"Colonnes attendues : {colonnes_attendues}")

        lignes = list(lecteur)
        if not lignes:
            raise ValueError(f"Le fichier source {chemin_fichier} est vide.")

        for ligne in lignes:
            category = ligne.get('category', 'Inconnu')
            quantite = int(ligne.get('quantity', 0))
            prix = float(ligne.get('price', 0))

            if category not in resume:
                resume[category] = {'quantity': 0, 'price': 0}

            resume[category]['quantity'] += quantite
            resume[category]['price'] += quantite * prix

    # Écriture du résumé dans le fichier de sortie
    with open(fichier_sortie, 'w', newline='', encoding='utf-8') as fichier:
        ecrivain = csv.DictWriter(fichier, fieldnames=['category', 'quantity', 'price'], delimiter=";")
        ecrivain.writeheader()
        for category, donnees in resume.items():
            ecrivain.writerow({
                'category': category,
                'quantity': donnees['quantity'],
                'price': donnees['price']
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
    parser.add_argument("-d", "--csv-directory", default=REPERTOIRE_DONNEES,
                        help="Répertoire contenant les fichiers CSV.")
    parser.add_argument("-o", "--output-file", default=FICHIER_FUSIONNE,
                        help="Chemin du fichier fusionné.")
    parser.add_argument("-c", "--critere", help="Critère de recherche pour l'action 'chercher' (ex : "
                                                "category=Electronics).")

    parser.add_argument("-b", "--base_file", help="Fichier a resumer' (ex : test.csv.)")

    args = parser.parse_args()

    # Assurer l'existence du répertoire csv
    os.makedirs(REPERTOIRE_DONNEES, exist_ok=True)

    # Confirmation interactive
    parametres = f"Action : {args.action}, Répertoire : {args.csv_directory}"
    if not confirmer_parametres(parametres):
        REPERTOIRE_DONNEES = input("Entrez le nouveau répertoire des données : ")
        FICHIER_FUSIONNE = input("Entrez le nouveau fichier de sortie : ")
        args.csv_directory = REPERTOIRE_DONNEES
        args.output_file = FICHIER_FUSIONNE

    # Exécution des actions en fonction de l'argument "action"
    if args.action == "consolider":
        fusionner_fichiers(args.csv_directory, args.output_file)

    elif args.action == "chercher":
        if not args.critere:
            print("Vous devez fournir un critère de recherche avec --critere.")
        else:
            cle, valeur = args.critere.split("=")
            rechercher_inventaire(args.base_file, (cle, valeur))

    elif args.action == "résumer":
        try:
            nom_fichier = args.base_file
            generer_resume(nom_fichier, "output/resume.csv")
        except ValueError as e:
            print(f"Erreur lors de la génération du résumé : {e}")


if __name__ == "__main__":
    main()
