# -*- coding: utf-8 -*-
"""
Sales Module - Module Ventes et Facturation
Conforme aux normes de facturation algériennes
"""

from core.base_module import BaseModule
from .views import SaleOrderListView


class SalesModule(BaseModule):
    """Module de gestion des ventes et facturation"""
    
    __version__ = '1.0.0'
    __author__ = 'ElAmira Team'
    __description__ = 'Gestion des ventes et facturation conforme DZ'
    
    def get_name(self) -> str:
        return "Ventes"
    
    def get_name_ar(self) -> str:
        return "المبيعات"
    
    def get_icon(self) -> str:
        return "core/assets/icons/sales.png"
    
    def get_main_view_class(self):
        return SaleOrderListView
    
    def get_action_menu(self) -> list:
        return [
            {
                'name': 'Nouvelle Facture',
                'name_ar': 'فاتورة جديدة',
                'icon': 'icons/invoice.png',
                'callback': None
            }
        ]
    
    def initialize_db(self):
        """Crée les tables pour les ventes"""
        
        # Table des partenaires (clients/fournisseurs)
        self.db_manager.execute_query("""
            CREATE TABLE IF NOT EXISTS res_partner (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                name_ar TEXT,
                address TEXT,
                address_ar TEXT,
                phone TEXT,
                email TEXT,
                nif TEXT,
                nis TEXT,
                art TEXT,
                is_customer BOOLEAN DEFAULT 1,
                is_supplier BOOLEAN DEFAULT 0,
                active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table des commandes de vente
        self.db_manager.execute_query("""
            CREATE TABLE IF NOT EXISTS sale_order (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                partner_id INTEGER NOT NULL,
                document_type TEXT DEFAULT 'invoice',
                date_order TIMESTAMP NOT NULL,
                date_due TIMESTAMP,
                date_delivery TIMESTAMP,
                state TEXT DEFAULT 'draft',
                amount_untaxed REAL DEFAULT 0,
                amount_tax REAL DEFAULT 0,
                amount_tap REAL DEFAULT 0,
                amount_stamp REAL DEFAULT 0,
                amount_total REAL DEFAULT 0,
                notes TEXT,
                payment_term TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (partner_id) REFERENCES res_partner (id)
            )
        """)
        
        # Ajouter colonnes si elles n'existent pas (migration)
        try:
            self.db_manager.execute_query("ALTER TABLE sale_order ADD COLUMN document_type TEXT DEFAULT 'invoice'")
        except:
            pass
        
        try:
            self.db_manager.execute_query("ALTER TABLE sale_order ADD COLUMN date_delivery TIMESTAMP")
        except:
            pass
        
        # Table des lignes de commande
        self.db_manager.execute_query("""
            CREATE TABLE IF NOT EXISTS sale_order_line (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER,
                product_name TEXT NOT NULL,
                description TEXT,
                quantity REAL NOT NULL DEFAULT 1,
                price_unit REAL NOT NULL DEFAULT 0,
                tax_id INTEGER,
                tax_rate REAL DEFAULT 0,
                discount REAL DEFAULT 0,
                subtotal REAL DEFAULT 0,
                tax_amount REAL DEFAULT 0,
                total REAL DEFAULT 0,
                FOREIGN KEY (order_id) REFERENCES sale_order (id),
                FOREIGN KEY (tax_id) REFERENCES account_tax (id)
            )
        """)
        
        print("  → Tables Sales créées")
