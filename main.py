# -*- coding: utf-8 -*-
"""
Point d'Entrée Principal de l'Application ElAmira ERP
Application de gestion modulaire conforme aux normes algériennes

Auteur: ElAmira Team
Version: 0.0.1
Licence: Propriétaire - Nécessite une activation
"""

import sys
import os

# Ajouter le dossier racine au path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QMessageBox
from core.app import ElAmiraApplication
from core.database import DatabaseManager
from core.license_manager import LicenseManager
from core.module_loader import ModuleLoader
from core.main_window import MainWindow


def main():
    """
    Fonction principale de l'application
    """
    
    print("\n" + "="*60)
    print("ElAmira ERP - Système de Gestion d'Entreprise")
    print("Version 0.0.1 - Conforme aux normes algériennes")
    print("="*60 + "\n")
    
    # Créer l'application Qt
    app = ElAmiraApplication(sys.argv)
    
    # Charger la langue par défaut (français)
    app.load_translation('fr')
    
    # Initialiser la base de données
    print("→ Initialisation de la base de données...")
    db_path = os.path.join('database', 'odoo_clone_dz.db')
    db_manager = DatabaseManager(db_path)
    
    # Initialiser le gestionnaire de licences
    print("→ Vérification de la licence...")
    license_manager = LicenseManager(db_manager)
    license_status = license_manager.check_license()
    
    if license_status['is_valid']:
        print(f"✓ Licence valide: {license_status['company_name']}")
        print(f"  Type: {license_status['license_type']}")
        print(f"  Expire le: {license_status['expiry_date']}")
    else:
        print(f"⚠ {license_status['message']}")
        print("  Mode démo activé")
    
    # Charger les modules
    print("\n→ Chargement des modules...")
    module_loader = ModuleLoader(db_manager, modules_path='modules')
    modules = module_loader.load_modules()
    
    if not modules:
        QMessageBox.critical(
            None,
            "Erreur",
            "Aucun module n'a pu être chargé.\n"
            "Veuillez vérifier le dossier 'modules'."
        )
        return 1
    
    # Créer et afficher la fenêtre principale
    print("\n→ Lancement de l'interface...")
    main_window = MainWindow(db_manager, license_manager)
    main_window.load_modules(module_loader)
    main_window.showMaximized()
    
    print("\n" + "="*60)
    print("✓ Application lancée avec succès")
    print("="*60 + "\n")
    
    # Lancer la boucle d'événements
    exit_code = app.exec()
    
    # Nettoyage avant de quitter
    print("\n→ Fermeture de l'application...")
    db_manager.close()
    
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
