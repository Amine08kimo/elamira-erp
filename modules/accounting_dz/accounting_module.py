# -*- coding: utf-8 -*-
"""
Accounting Module - Module Comptabilité DZ
Conforme au PCN et réglementations fiscales algériennes
"""

from core.base_module import BaseModule
from .views import AccountingMainView


class AccountingModule(BaseModule):
    """Module de comptabilité et finance pour l'Algérie"""
    
    __version__ = '1.0.0'
    __author__ = 'ElAmira Team'
    __description__ = 'Comptabilité conforme PCN et DGI algérienne'
    
    def get_name(self) -> str:
        return "Comptabilité"
    
    def get_name_ar(self) -> str:
        return "المحاسبة"
    
    def get_icon(self) -> str:
        return "core/assets/icons/accounting.png"
    
    def get_main_view_class(self):
        return AccountingMainView
    
    def get_action_menu(self) -> list:
        return [
            {
                'name': 'Nouvelle Écriture',
                'name_ar': 'قيد محاسبي جديد',
                'icon': 'icons/journal.png',
                'callback': None
            },
            {
                'name': 'Déclaration G12',
                'name_ar': 'تصريح G12',
                'icon': 'icons/g12.png',
                'callback': None
            }
        ]
    
    def initialize_db(self):
        """Crée les tables comptables"""
        
        # Table des pièces comptables
        self.db_manager.execute_query("""
            CREATE TABLE IF NOT EXISTS account_move (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                ref TEXT,
                date TIMESTAMP NOT NULL,
                journal_id INTEGER DEFAULT 1,
                state TEXT DEFAULT 'draft',
                amount_total REAL DEFAULT 0,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table des lignes d'écriture
        self.db_manager.execute_query("""
            CREATE TABLE IF NOT EXISTS account_move_line (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                move_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                pcn_account_id INTEGER NOT NULL,
                debit REAL DEFAULT 0,
                credit REAL DEFAULT 0,
                partner_id INTEGER,
                FOREIGN KEY (move_id) REFERENCES account_move (id),
                FOREIGN KEY (pcn_account_id) REFERENCES pcn_account (id),
                FOREIGN KEY (partner_id) REFERENCES res_partner (id)
            )
        """)
        
        # Table des déclarations G12
        self.db_manager.execute_query("""
            CREATE TABLE IF NOT EXISTS g12_declaration (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                period_start TIMESTAMP NOT NULL,
                period_end TIMESTAMP NOT NULL,
                state TEXT DEFAULT 'draft',
                ca_ht REAL DEFAULT 0,
                ca_exonere REAL DEFAULT 0,
                ca_total REAL DEFAULT 0,
                tva_19_base REAL DEFAULT 0,
                tva_19_amount REAL DEFAULT 0,
                tva_9_base REAL DEFAULT 0,
                tva_9_amount REAL DEFAULT 0,
                tva_collectee_total REAL DEFAULT 0,
                tva_deductible_immobilisations REAL DEFAULT 0,
                tva_deductible_biens REAL DEFAULT 0,
                tva_deductible_services REAL DEFAULT 0,
                tva_deductible_total REAL DEFAULT 0,
                tva_due REAL DEFAULT 0,
                tva_credit_report REAL DEFAULT 0,
                tva_a_payer REAL DEFAULT 0,
                tap_base REAL DEFAULT 0,
                tap_rate REAL DEFAULT 2.0,
                tap_amount REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        print("  → Tables Accounting créées")
