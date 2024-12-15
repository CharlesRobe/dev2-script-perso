import csv
import os
from typing import List, Dict

# Constants for file paths
DATA_DIRECTORY = "csv"
CONSOLIDATED_FILE = "consolidated_inventory.csv"


def consolidate_files(input_directory: str, output_file: str):
    """
    Consolidates multiple CSV files into a single file.

    Args:
        input_directory (str): Path to the directory containing CSV files.
        output_file (str): Path to the output consolidated CSV file.
    """
    consolidated_data = []

    # Read all CSV files in the directory
    for file_name in os.listdir(input_directory):
        file_path = os.path.join(input_directory, file_name)
        if file_name.endswith('.csv'):
            with open(file_path, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    consolidated_data.append(row)

    if consolidated_data:
        # Write consolidated data to the output file
        with open(output_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=consolidated_data[0].keys())
            writer.writeheader()
            writer.writerows(consolidated_data)
        print(f"Consolidation complete. Data saved to {output_file}")
    else:
        print("No data to consolidate.")


def search_inventory(file_path: str, **filters) -> List[Dict[str, str]]:
    """
    Searches the inventory based on given filters.

    Args:
        file_path (str): Path to the consolidated CSV file.
        **filters: Key-value pairs for filtering data.

    Returns:
        List[Dict[str, str]]: List of matching rows.
    """
    results = []

    with open(file_path, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            match = all(str(row[key]) == str(value) for key, value in filters.items() if key in row)
            if match:
                results.append(row)

    return results


def generate_summary(file_path: str, output_file: str):
    """
    Generates a summary report and exports it as a CSV file.

    Args:
        file_path (str): Path to the consolidated CSV file.
        output_file (str): Path to the summary output file.
    """
    summary = {}

    with open(file_path, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            category = row.get('category', 'Unknown')
            quantity = int(row.get('quantity', 0))
            price = float(row.get('price', 0))

            if category not in summary:
                summary[category] = {'total_quantity': 0, 'total_value': 0}

            summary[category]['total_quantity'] += quantity
            summary[category]['total_value'] += quantity * price

    # Write summary to the output file
    with open(output_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['category', 'total_quantity', 'total_value'])
        writer.writeheader()
        for category, data in summary.items():
            writer.writerow({
                'category': category,
                'total_quantity': data['total_quantity'],
                'total_value': data['total_value']
            })
    print(f"Summary report generated: {output_file}")


import argparse

def main():
    parser = argparse.ArgumentParser(description="Automatisez la gestion de l'inventaire avec ce script.")
    subparsers = parser.add_subparsers(dest="command", help="Commandes disponibles")

    # Commande pour consolider les fichiers
    parser_consolidate = subparsers.add_parser("consolidate", help="Consolider les fichiers CSV")
    parser_consolidate.add_argument("-i", "--input", required=True, help="Répertoire contenant les fichiers CSV")
    parser_consolidate.add_argument("-o", "--output", required=True, help="Fichier de sortie consolidé")

    # Commande pour rechercher
    parser_search = subparsers.add_parser("search", help="Rechercher dans l'inventaire consolidé")
    parser_search.add_argument("-f", "--file", required=True, help="Fichier CSV consolidé")
    parser_search.add_argument("-c", "--category", help="Filtrer par catégorie")

    # Commande pour générer un rapport
    parser_summary = subparsers.add_parser("summary", help="Générer un rapport résumé")
    parser_summary.add_argument("-f", "--file", required=True, help="Fichier CSV consolidé")
    parser_summary.add_argument("-o", "--output", required=True, help="Fichier de sortie du résumé")

    args = parser.parse_args()

    if args.command == "consolidate":
        consolidate_files(args.input, args.output)
    elif args.command == "search":
        filters = {"category": args.category} if args.category else {}
        results = search_inventory(args.file, **filters)
        print("Résultats de la recherche :", results)
    elif args.command == "summary":
        generate_summary(args.file, args.output)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
