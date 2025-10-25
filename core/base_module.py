# -*- coding: utf-8 -*-
"""
Classe de Base Abstraite pour tous les Modules
Tous les modules de l'application doivent hériter de cette classe
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from PyQt6.QtWidgets import QWidget


class BaseModule(ABC):
    """
    Classe abstraite définissant l'interface que tous les modules doivent implémenter.
    Cette architecture permet le chargement dynamique et l'extensibilité.
    """
    
    def __init__(self, db_manager):
        """
        Initialise le module avec une référence au gestionnaire de base de données
        
        Args:
            db_manager: Instance du DatabaseManager
        """
        self.db_manager = db_manager
        self._is_initialized = False
    
    @abstractmethod
    def get_name(self) -> str:
        """
        Retourne le nom d'affichage du module
        
        Returns:
            Le nom du module (ex: "Ventes", "Stock")
        """
        pass
    
    @abstractmethod
    def get_name_ar(self) -> str:
        """
        Retourne le nom d'affichage du module en arabe
        
        Returns:
            Le nom du module en arabe
        """
        pass
    
    @abstractmethod
    def get_icon(self) -> str:
        """
        Retourne le chemin vers l'icône du module
        
        Returns:
            Chemin relatif vers l'icône (ex: "core/assets/icons/sales.svg")
        """
        pass
    
    @abstractmethod
    def get_main_view_class(self):
        """
        Retourne la classe de la vue principale du module
        
        Returns:
            Une classe héritant de QWidget qui sera affichée quand le module est sélectionné
        """
        pass
    
    @abstractmethod
    def get_action_menu(self) -> List[Dict[str, any]]:
        """
        Retourne la liste des actions disponibles dans le menu "Nouveau"
        
        Returns:
            Liste de dictionnaires avec la structure:
            [
                {
                    'name': 'Nouvelle Facture',
                    'name_ar': 'فاتورة جديدة',
                    'icon': 'path/to/icon.svg',
                    'callback': self.create_invoice
                },
                ...
            ]
        """
        pass
    
    @abstractmethod
    def initialize_db(self):
        """
        Crée les tables spécifiques au module dans la base de données.
        Cette méthode est appelée au premier lancement ou lors de l'installation du module.
        """
        pass
    
    def get_module_info(self) -> Dict[str, any]:
        """
        Retourne les métadonnées du module
        
        Returns:
            Dictionnaire avec les informations du module
        """
        return {
            'name': self.get_name(),
            'name_ar': self.get_name_ar(),
            'icon': self.get_icon(),
            'version': getattr(self, '__version__', '1.0.0'),
            'author': getattr(self, '__author__', 'ElAmira Team'),
            'description': getattr(self, '__description__', ''),
            'depends': getattr(self, '__depends__', []),
        }
    
    def install(self):
        """
        Installe le module (crée les tables, insère les données par défaut)
        """
        if not self._is_initialized:
            print(f"Installation du module: {self.get_name()}")
            self.initialize_db()
            self._register_module()
            self._is_initialized = True
            print(f"✓ Module {self.get_name()} installé avec succès")
    
    def _register_module(self):
        """Enregistre le module dans la table ir_module_module"""
        module_info = self.get_module_info()
        
        # Vérifier si le module existe déjà
        existing = self.db_manager.fetch_one(
            "SELECT * FROM ir_module_module WHERE name = ?",
            (module_info['name'],)
        )
        
        if not existing:
            self.db_manager.execute_query("""
                INSERT INTO ir_module_module (name, display_name, state, version, author, icon_path, installed_at)
                VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                module_info['name'],
                module_info['name'],
                'installed',
                module_info['version'],
                module_info['author'],
                module_info['icon']
            ))
        else:
            self.db_manager.execute_query("""
                UPDATE ir_module_module 
                SET state = 'installed', updated_at = CURRENT_TIMESTAMP
                WHERE name = ?
            """, (module_info['name'],))
    
    def uninstall(self):
        """
        Désinstalle le module (met à jour le statut, ne supprime pas les données)
        """
        self.db_manager.execute_query("""
            UPDATE ir_module_module 
            SET state = 'uninstalled', updated_at = CURRENT_TIMESTAMP
            WHERE name = ?
        """, (self.get_name(),))
        print(f"✓ Module {self.get_name()} désinstallé")
