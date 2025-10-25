# -*- coding: utf-8 -*-
"""
CRM Module - Module de gestion de la relation client
"""

from core.base_module import BaseModule
from .views import CRMLeadListView


class CRMModule(BaseModule):
    """Module CRM pour la gestion des opportunités commerciales"""
    
    __version__ = '1.0.0'
    __author__ = 'ElAmira Team'
    __description__ = 'Gestion de la relation client et pipeline de ventes'
    
    def get_name(self) -> str:
        return "CRM"
    
    def get_name_ar(self) -> str:
        return "إدارة علاقات العملاء"
    
    def get_icon(self) -> str:
        return "core/assets/icons/crm.png"
    
    def get_main_view_class(self):
        return CRMLeadListView
    
    def get_action_menu(self) -> list:
        return [
            {
                'name': 'Nouvelle Opportunité',
                'name_ar': 'فرصة جديدة',
                'icon': 'icons/lead.png',
                'callback': None
            }
        ]
    
    def initialize_db(self):
        """Crée les tables pour le CRM"""
        
        # Table des étapes du pipeline
        self.db_manager.execute_query("""
            CREATE TABLE IF NOT EXISTS crm_stage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                name_ar TEXT,
                sequence INTEGER DEFAULT 10,
                fold BOOLEAN DEFAULT 0,
                probability REAL DEFAULT 0,
                active BOOLEAN DEFAULT 1
            )
        """)
        
        # Insérer les étapes par défaut
        stages = [
            ('Nouveau', 'جديد', 10, 0, 10.0),
            ('Qualifié', 'مؤهل', 20, 0, 30.0),
            ('Proposition', 'عرض', 30, 0, 60.0),
            ('Négociation', 'تفاوض', 40, 0, 80.0),
            ('Gagné', 'فاز', 50, 1, 100.0),
            ('Perdu', 'خسر', 60, 1, 0.0),
        ]
        
        for name, name_ar, seq, fold, prob in stages:
            self.db_manager.execute_query("""
                INSERT OR IGNORE INTO crm_stage (name, name_ar, sequence, fold, probability)
                VALUES (?, ?, ?, ?, ?)
            """, (name, name_ar, seq, fold, prob))
        
        # Table des opportunités (leads)
        self.db_manager.execute_query("""
            CREATE TABLE IF NOT EXISTS crm_lead (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                partner_id INTEGER,
                contact_name TEXT,
                email TEXT,
                phone TEXT,
                expected_revenue REAL DEFAULT 0,
                probability REAL DEFAULT 0,
                stage_id INTEGER DEFAULT 1,
                priority TEXT DEFAULT 'medium',
                date_deadline TIMESTAMP,
                date_closed TIMESTAMP,
                user_id INTEGER,
                team_id INTEGER,
                description TEXT,
                active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (partner_id) REFERENCES res_partner (id),
                FOREIGN KEY (stage_id) REFERENCES crm_stage (id)
            )
        """)
        
        print("  → Tables CRM créées")
