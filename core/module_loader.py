# -*- coding: utf-8 -*-
"""
Chargeur Dynamique de Modules
Scanne le dossier /modules et charge tous les modules disponibles
"""

import os
import sys
import importlib
import inspect
from typing import List, Dict
from pathlib import Path
from core.base_module import BaseModule


class ModuleLoader:
    """
    Classe responsable du chargement dynamique des modules.
    Permet l'extensibilité et la modularité de l'application.
    """
    
    def __init__(self, db_manager, modules_path: str = "modules"):
        """
        Initialise le chargeur de modules
        
        Args:
            db_manager: Instance du DatabaseManager
            modules_path: Chemin vers le dossier des modules
        """
        self.db_manager = db_manager
        self.modules_path = modules_path
        self.loaded_modules: List[BaseModule] = []
    
    def load_modules(self) -> List[BaseModule]:
        """
        Charge tous les modules disponibles dans le dossier modules/
        
        Returns:
            Liste des instances de modules chargés
        """
        print("\n" + "="*60)
        print("CHARGEMENT DES MODULES")
        print("="*60)
        
        # Vérifier que le dossier modules existe
        if not os.path.exists(self.modules_path):
            print(f"✗ Dossier modules introuvable: {self.modules_path}")
            return []
        
        # Ajouter le dossier modules au path Python si nécessaire
        if self.modules_path not in sys.path:
            sys.path.insert(0, os.path.abspath(self.modules_path))
        
        # Scanner tous les sous-dossiers du dossier modules
        for item in os.listdir(self.modules_path):
            module_dir = os.path.join(self.modules_path, item)
            
            # Ignorer les fichiers et dossiers spéciaux
            if not os.path.isdir(module_dir) or item.startswith('_') or item.startswith('.'):
                continue
            
            # Vérifier qu'il y a un fichier __init__.py
            init_file = os.path.join(module_dir, '__init__.py')
            if not os.path.exists(init_file):
                print(f"⚠ Module {item} ignoré: pas de __init__.py")
                continue
            
            # Tenter de charger le module
            try:
                self._load_module(item)
            except Exception as e:
                print(f"✗ Erreur lors du chargement du module {item}: {e}")
                import traceback
                traceback.print_exc()
        
        print(f"\n✓ {len(self.loaded_modules)} module(s) chargé(s) avec succès")
        print("="*60 + "\n")
        
        return self.loaded_modules
    
    def _load_module(self, module_name: str):
        """
        Charge un module spécifique
        
        Args:
            module_name: Nom du dossier du module
        """
        print(f"\n→ Chargement du module: {module_name}")
        
        try:
            # Importer le package du module
            module_package = importlib.import_module(module_name)
            
            # Recharger pour avoir les dernières modifications
            importlib.reload(module_package)
            
            # Chercher une classe qui hérite de BaseModule dans le module
            module_class = None
            
            # Parcourir tous les membres du module
            for name, obj in inspect.getmembers(module_package):
                if inspect.isclass(obj) and issubclass(obj, BaseModule) and obj is not BaseModule:
                    module_class = obj
                    break
            
            if module_class is None:
                print(f"  ⚠ Aucune classe de module trouvée dans {module_name}")
                return
            
            # Instancier le module
            module_instance = module_class(self.db_manager)
            
            # Installer le module (créer les tables)
            module_instance.install()
            
            # Ajouter à la liste des modules chargés
            self.loaded_modules.append(module_instance)
            
            print(f"  ✓ {module_instance.get_name()} chargé")
            
        except Exception as e:
            print(f"  ✗ Erreur: {e}")
            raise
    
    def get_module_by_name(self, name: str) -> BaseModule:
        """
        Récupère un module par son nom
        
        Args:
            name: Nom du module
            
        Returns:
            Instance du module ou None
        """
        for module in self.loaded_modules:
            if module.get_name().lower() == name.lower():
                return module
        return None
    
    def get_installed_modules(self) -> List[Dict]:
        """
        Récupère la liste des modules installés depuis la base de données
        
        Returns:
            Liste des modules installés
        """
        return self.db_manager.fetch_all("""
            SELECT * FROM ir_module_module 
            WHERE state = 'installed' 
            ORDER BY name
        """)
    
    def reload_modules(self):
        """
        Recharge tous les modules (utile pour le développement)
        """
        self.loaded_modules.clear()
        return self.load_modules()
