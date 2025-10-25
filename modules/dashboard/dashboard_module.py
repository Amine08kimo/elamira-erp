# -*- coding: utf-8 -*-
"""
Module Dashboard - Tableau de Bord
Vue d'ensemble avec KPIs et statistiques
"""

from core.base_module import BaseModule
from .modern_dashboard import ModernDashboard


class DashboardModule(BaseModule):
    """Module de tableau de bord avec vue d'ensemble"""
    
    __version__ = '4.0.0'
    __author__ = 'ElAmira Team'
    __description__ = 'Tableau de bord moderne avec KPIs, alertes et graphiques'
    
    def get_name(self) -> str:
        return "Tableau de Bord"
    
    def get_name_ar(self) -> str:
        return "لوحة القيادة"
    
    def get_icon(self) -> str:
        return "core/assets/icons/dashboard.png"
    
    def get_main_view_class(self):
        return ModernDashboard
    
    def get_action_menu(self) -> list:
        # Le dashboard n'a pas d'actions "Nouveau"
        return []
    
    def initialize_db(self):
        """Le dashboard utilise les données des autres modules"""
        print("  → Dashboard: Pas de tables spécifiques")
