# -*- coding: utf-8 -*-
"""
Classe Application Principale
Gère le cycle de vie de l'application PyQt6
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTranslator, QLocale
from PyQt6.QtGui import QFont
import sys
import os


class ElAmiraApplication(QApplication):
    """
    Classe principale de l'application ElAmira ERP.
    Hérite de QApplication et gère les paramètres globaux.
    """
    
    def __init__(self, argv):
        """
        Initialise l'application
        
        Args:
            argv: Arguments de ligne de commande
        """
        super().__init__(argv)
        
        # Configuration de base
        self.setApplicationName("ElAmira ERP")
        self.setOrganizationName("ElAmira")
        self.setOrganizationDomain("elamira.dz")
        self.setApplicationVersion("0.0.1")
        
        # Traducteur pour l'internationalisation
        self.translator = QTranslator()
        self.current_language = 'fr'
        
        # Configuration des polices
        self._setup_fonts()
    
    def _setup_fonts(self):
        """Configure les polices par défaut de l'application"""
        # Police système par défaut
        default_font = QFont("Segoe UI", 10)
        self.setFont(default_font)
    
    def load_translation(self, language_code: str) -> bool:
        """
        Charge les fichiers de traduction
        
        Args:
            language_code: Code de la langue ('fr' ou 'ar')
            
        Returns:
            True si la traduction a été chargée
        """
        translation_path = os.path.join(
            'core', 'assets', 'i18n', f'translations_{language_code}.qm'
        )
        
        if os.path.exists(translation_path):
            if self.translator.load(translation_path):
                self.installTranslator(self.translator)
                self.current_language = language_code
                print(f"✓ Traduction chargée: {language_code}")
                return True
        
        print(f"⚠ Fichier de traduction introuvable: {translation_path}")
        return False
    
    def get_current_language(self) -> str:
        """
        Retourne la langue courante
        
        Returns:
            Code de la langue ('fr' ou 'ar')
        """
        return self.current_language
