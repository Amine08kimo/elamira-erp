# -*- coding: utf-8 -*-
"""
Settings Module - Module des paramètres
"""

from core.base_module import BaseModule
from .views import SettingsView


class SettingsModule(BaseModule):
    """Module de paramétrage de l'application"""
    
    __version__ = '1.0.0'
    __author__ = 'ElAmira Team'
    __description__ = 'Configuration et paramètres DZ'
    
    def get_name(self) -> str:
        return "Paramètres"
    
    def get_name_ar(self) -> str:
        return "الإعدادات"
    
    def get_icon(self) -> str:
        return "core/assets/icons/settings.png"
    
    def get_main_view_class(self):
        return SettingsView
    
    def get_action_menu(self) -> list:
        return []
    
    def initialize_db(self):
        """Pas de tables spécifiques"""
        print("  → Settings: Configuration")
