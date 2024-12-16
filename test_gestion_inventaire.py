import unittest
import os
import csv
from unittest.mock import patch
import io
from gestion_inventaire import fusionner_fichiers, rechercher_inventaire, generer_resume


def create_csv_file(path, header, rows):
    """Crée un fichier CSV pour les tests."""
    with open(path, "w", newline="", encoding="utf-8") as file:
        file.write("\n".join(header + rows))


class TestGestionInventaire(unittest.TestCase):
    def setUp(self):
        """Prépare les fichiers nécessaires pour les tests."""
        self.csv_dir = "test_csv"
        self.output_file = "test_output.csv"
        self.resume_file = "test_resume.csv"
        os.makedirs(self.csv_dir, exist_ok=True)

        # Fichiers de test
        create_csv_file(
            "test_csv/electronics.csv",
            ["name;quantity;price;category"],
            [
                "Laptop;10;800;Electronics",
                "Smartphone;20;500;Electronics",
                "Tablet;15;300;Electronics"
            ]
        )
        create_csv_file(
            "test_csv/furniture.csv",
            ["name;quantity;price;category"],
            [
                "Chair;50;45;Furniture",
                "Table;15;150;Furniture",
                "Sofa;5;700;Furniture"
            ]
        )
        create_csv_file("test_csv/empty.csv", ["name;quantity;price;category"], [])
        create_csv_file(
            "test_csv/malformed.csv",
            ["wrong_column1;wrong_column2"],
            [
                "Data1;Data2"
            ]
        )

    def tearDown(self):
        """Supprime les fichiers de test après chaque exécution."""
        for root, dirs, files in os.walk(self.csv_dir, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            os.rmdir(root)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        if os.path.exists(self.resume_file):
            os.remove(self.resume_file)

    def test_fusionner_fichiers(self):
        """Test la fusion des fichiers CSV valides."""
        fusionner_fichiers(self.csv_dir, self.output_file)
        self.assertTrue(os.path.exists(self.output_file))

        with open(self.output_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            rows = list(reader)
            self.assertEqual(len(rows), 6)
            self.assertEqual(rows[0]["name"], "Laptop")
            self.assertEqual(rows[-1]["name"], "Sofa")

    def test_rechercher_inventaire(self):
        """Vérifie que la recherche retourne les résultats affichés correctement."""
        fusionner_fichiers(self.csv_dir, self.output_file)

        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            rechercher_inventaire(self.output_file, ("category", "Electronics"))
            sortie = fake_stdout.getvalue()

        self.assertIn("Laptop", sortie)
        self.assertIn("Smartphone", sortie)
        self.assertIn("Tablet", sortie)
        self.assertIn("Electronics", sortie)
        self.assertNotIn("Furniture", sortie)

    def test_rechercher_inventaire_cle_inexistante(self):
        """Vérifie que la recherche avec une clé inexistante lève une KeyError."""
        fusionner_fichiers(self.csv_dir, self.output_file)

        with self.assertRaises(KeyError):
            rechercher_inventaire(self.output_file, ("unknown_key", "value"))

    def test_rechercher_inventaire_valeur_inexistante(self):
        """Vérifie que la recherche avec une valeur inexistante affiche uniquement l'en-tête."""
        fusionner_fichiers(self.csv_dir, self.output_file)

        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            rechercher_inventaire(self.output_file, ("category", "NonExistentCategory"))
            sortie = fake_stdout.getvalue()

        self.assertIn("Nom                  | Quantité   | Prix (€)   | Catégorie", sortie)
        self.assertNotIn("Laptop", sortie)
        self.assertNotIn("Electronics", sortie)

    def test_generer_resume(self):
        """Test la génération de résumé à partir d'un fichier valide."""
        fusionner_fichiers(self.csv_dir, self.output_file)
        generer_resume(self.output_file, self.resume_file)
        self.assertTrue(os.path.exists(self.resume_file))

        with open(self.resume_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            rows = list(reader)
            self.assertEqual(len(rows), 2)  # Deux catégories
            self.assertEqual(rows[0]["category"], "Electronics")
            self.assertEqual(int(rows[0]["quantity"]), 45)
            self.assertAlmostEqual(float(rows[0]["price"]), 22500.0)

    def test_generer_resume_fichier_vide(self):
        """Vérifie que la génération d'un résumé avec un fichier vide lève une ValueError."""
        with self.assertRaises(ValueError):
            generer_resume("test_csv/empty.csv", self.resume_file)

    def test_fusionner_fichiers_malformed(self):
        """Vérifie que les fichiers mal formés sont ignorés."""
        fusionner_fichiers(self.csv_dir, self.output_file)

        with open(self.output_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            rows = list(reader)
            self.assertEqual(len(rows), 6)  # Seulement les fichiers valides
            self.assertNotIn("wrong_column1", reader.fieldnames)
