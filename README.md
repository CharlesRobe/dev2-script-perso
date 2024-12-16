
# Gestion d'Inventaire

Ce programme permet de gérer des fichiers CSV contenant des informations sur les stocks. Il offre trois fonctionnalités principales :
- Consolider plusieurs fichiers CSV en un seul fichier.
- Rechercher des informations spécifiques dans un fichier CSV.
- Générer un résumé des stocks par catégorie.

---

## Installation

### Prérequis
- Python 3.8 ou une version supérieure doit être installé.

### Instructions d'installation
1. Téléchargez ou clonez le projet à partir du dépôt :
   ```bash
   git clone <URL_DU_DEPOT>
   cd <NOM_DU_DEPOT>
   ```

2. (Optionnel) Créez un environnement virtuel pour isoler vos dépendances Python :
   ```bash
   python -m venv venv
   source venv/bin/activate   # Sous Linux/macOS
   venv\Scripts\activate    # Sous Windows
   ```

---

## Utilisation

Le programme fonctionne uniquement en ligne de commande et propose trois actions principales : consolider, chercher et résumer.

### Commande générale
```bash
python gestion_inventaire.py <action> [options]
```

### Actions disponibles

#### Consolider des fichiers
Fusionne tous les fichiers CSV valides d'un répertoire dans un fichier unique.

Options :
```bash
-d  # Chemin du répertoire contenant les fichiers CSV.
-o  # Chemin du fichier consolidé en sortie.
```

Exemple :
```bash
python gestion_inventaire.py consolider -d csv -o output/inventaire_fusionne.csv
```

#### Rechercher des informations
Rechercher des données dans un fichier CSV consolidé en utilisant un critère.

Options :
```bash
-b  # Chemin du fichier CSV à explorer.
-c  # Critère de recherche au format cle=valeur.
```

Exemple :
```bash
python gestion_inventaire.py chercher -b output/inventaire_fusionne.csv -c category=Electronics
```

#### Générer un résumé
Créer un résumé des stocks par catégorie à partir d'un fichier CSV.

Options :
```bash
-b  # Chemin du fichier CSV à résumer.
```

Exemple :
```bash
python gestion_inventaire.py résumer -b output/inventaire_fusionne.csv
```

---

## Format des fichiers CSV

Les fichiers doivent respecter le format suivant :
- Colonnes obligatoires : `name`, `quantity`, `price`, `category`.
- Séparateur : `;` (point-virgule).

Exemple de fichier valide :
```csv
name;quantity;price;category
Laptop;10;800;Electronics
Smartphone;20;500;Electronics
Table;5;150;Furniture
```

---

## Structure du projet

```plaintext
.
├── gestion_inventaire.py      # Script principal contenant les fonctionnalités.
├── test_gestion_inventaire.py # Tests unitaires pour valider les fonctionnalités.
├── csv/                       # Répertoire contenant les fichiers CSV d'entrée.
├── output/                    # Répertoire pour les fichiers générés.
└── README.md                  # Documentation du projet.
```

---

