# -*- coding: utf-8 -*-
"""
Purchase Module - Module de gestion des achats fournisseurs
"""

from core.base_module import BaseModule
from .views import PurchaseOrderListView


class PurchaseModule(BaseModule):
    """Module Achats pour la gestion des commandes fournisseurs"""
    
    __version__ = '1.0.0'
    __author__ = 'ElAmira Team'
    __description__ = 'Gestion des achats et commandes fournisseurs avec mise à jour automatique du stock'
    
    def get_name(self) -> str:
        return "Achats"
    
    def get_name_ar(self) -> str:
        return "المشتريات"
    
    def get_icon(self) -> str:
        return "core/assets/icons/purchase.png"
    
    def get_main_view_class(self):
        return PurchaseOrderListView
    
    def get_action_menu(self) -> list:
        return [
            {
                'name': 'Nouvelle Commande',
                'name_ar': 'طلب جديد',
                'icon': 'icons/purchase.png',
                'callback': None
            }
        ]
    
    def initialize_db(self):
        """Crée les tables pour les achats"""
        
        # Table des commandes d'achat
        self.db_manager.execute_query("""
            CREATE TABLE IF NOT EXISTS purchase_order (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                partner_id INTEGER,
                supplier_invoice_ref TEXT,
                date_order TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_due TIMESTAMP,
                date_received TIMESTAMP,
                state TEXT DEFAULT 'draft',
                amount_untaxed REAL DEFAULT 0,
                amount_tax REAL DEFAULT 0,
                amount_total REAL DEFAULT 0,
                notes TEXT,
                payment_term TEXT,
                user_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (partner_id) REFERENCES res_partner (id)
            )
        """)
        
        # Table des lignes de commande d'achat
        self.db_manager.execute_query("""
            CREATE TABLE IF NOT EXISTS purchase_order_line (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER,
                product_name TEXT,
                description TEXT,
                quantity REAL DEFAULT 1,
                price_unit REAL DEFAULT 0,
                tax_rate REAL DEFAULT 19,
                subtotal REAL DEFAULT 0,
                tax_amount REAL DEFAULT 0,
                total REAL DEFAULT 0,
                FOREIGN KEY (order_id) REFERENCES purchase_order (id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES product_product (id)
            )
        """)
        
        # Ajouter la séquence pour les numéros de commande
        self.db_manager.execute_query("""
            INSERT OR IGNORE INTO ir_sequence (name, code, prefix, padding, next_number)
            VALUES ('Commandes Achat', 'purchase.order', 'PO', 5, 1)
        """)
        
        print("  → Tables Purchase créées")
