import unittest
import os
import csv
from gestion_inventaire import fusionner_fichiers, rechercher_inventaire, generer_resume


class TestGestionInventaire(unittest.TestCase):
    """
    Classe de tests pour vérifier les fonctionnalités de gestion d'inventaire.
    """
    REPERTOIRE_TEST = "test_data"
    FICHIER_FUSIONNE = "test_inventaire_fusionne.csv"
    FICHIER_RESUME = "test_resume.csv"

    def setUp(self):
        """
        Prépare l'environnement de test en créant des fichiers de test.
        """
        os.makedirs(self.REPERTOIRE_TEST, exist_ok=True)

        # Création de fichiers CSV de test
        with open(os.path.join(self.REPERTOIRE_TEST, "electronique.csv"), "w", newline="") as fichier:
            writer = csv.writer(fichier)
            writer.writerow(["name", "quantity", "price", "category"])
            writer.writerow(["Laptop", "10", "800", "Electronics"])
            writer.writerow(["Smartphone", "20", "500", "Electronics"])

        with open(os.path.join(self.REPERTOIRE_TEST, "meubles.csv"), "w", newline="") as fichier:
            writer = csv.writer(fichier)
            writer.writerow(["name", "quantity", "price", "category"])
            writer.writerow(["Chaise", "50", "45", "Furniture"])
            writer.writerow(["Table", "15", "150", "Furniture"])

        # Fichier vide pour tester les cas particuliers
        with open(os.path.join(self.REPERTOIRE_TEST, "vide.csv"), "w", newline="") as fichier:
            writer = csv.writer(fichier)
            writer.writerow(["name", "quantity", "price", "category"])

    def tearDown(self):
        """
        Nettoie l'environnement de test en supprimant les fichiers générés.
        """
        for fichier in [self.FICHIER_FUSIONNE, self.FICHIER_RESUME]:
            if os.path.exists(fichier):
                os.remove(fichier)
        for fichier in os.listdir(self.REPERTOIRE_TEST):
            os.remove(os.path.join(self.REPERTOIRE_TEST, fichier))
        os.rmdir(self.REPERTOIRE_TEST)

    def test_fusionner_fichiers(self):
        """
        Vérifie que les fichiers sont correctement fusionnés.
        """
        fusionner_fichiers(self.REPERTOIRE_TEST, self.FICHIER_FUSIONNE)
        self.assertTrue(os.path.exists(self.FICHIER_FUSIONNE))
        with open(self.FICHIER_FUSIONNE, "r") as fichier:
            lecteur = csv.DictReader(fichier)
            lignes = list(lecteur)
            self.assertEqual(len(lignes), 4)  # 4 lignes valides dans les fichiers d'entrée

    def test_fusionner_fichier_vide(self):
        """
        Vérifie que la fusion fonctionne même avec un fichier vide.
        """
        fusionner_fichiers(self.REPERTOIRE_TEST, self.FICHIER_FUSIONNE)
        with open(self.FICHIER_FUSIONNE, "r") as fichier:
            lecteur = csv.DictReader(fichier)
            lignes = list(lecteur)
            self.assertGreater(len(lignes), 0)  # Les fichiers valides sont toujours fusionnés

    def test_rechercher_inventaire(self):
        """
        Vérifie que la recherche retourne les bonnes lignes.
        """
        fusionner_fichiers(self.REPERTOIRE_TEST, self.FICHIER_FUSIONNE)
        resultats = rechercher_inventaire(self.FICHIER_FUSIONNE, category="Furniture")
        self.assertEqual(len(resultats), 2)  # Deux éléments dans la catégorie "Furniture"
        self.assertEqual(resultats[0]["name"], "Chaise")

    def test_rechercher_aucun_resultat(self):
        """
        Vérifie le comportement lorsqu'aucun résultat ne correspond.
        """
        fusionner_fichiers(self.REPERTOIRE_TEST, self.FICHIER_FUSIONNE)
        resultats = rechercher_inventaire(self.FICHIER_FUSIONNE, category="Inconnu")
        self.assertEqual(len(resultats), 0)  # Aucun résultat attendu

    def test_generer_resume(self):
        """
        Vérifie que le rapport récapitulatif est généré correctement.
        """
        fusionner_fichiers(self.REPERTOIRE_TEST, self.FICHIER_FUSIONNE)
        generer_resume(self.FICHIER_FUSIONNE, self.FICHIER_RESUME)
        self.assertTrue(os.path.exists(self.FICHIER_RESUME))
        with open(self.FICHIER_RESUME, "r") as fichier:
            lecteur = csv.DictReader(fichier)
            lignes = list(lecteur)
            self.assertEqual(len(lignes), 2)  # Deux catégories : Electronics, Furniture

    def test_generer_resume_fichier_vide(self):
        """
        Vérifie le comportement lors de la tentative de génération d'un résumé sur un fichier vide.
        """
        fusionner_fichiers(self.REPERTOIRE_TEST, "vide.csv")
        with self.assertRaises(ValueError):  # À condition que votre fonction lève une exception pour les fichiers vides
            generer_resume("vide.csv", self.FICHIER_RESUME)


if __name__ == "__main__":
    unittest.main()
