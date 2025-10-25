# -*- coding: utf-8 -*-
"""
Stock Module - Module de gestion du stock
"""

from core.base_module import BaseModule
from .views import ProductKanbanView


class StockModule(BaseModule):
    """Module de gestion des produits et du stock"""
    
    __version__ = '1.0.0'
    __author__ = 'ElAmira Team'
    __description__ = 'Gestion des produits et inventaire'
    
    def get_name(self) -> str:
        return "Stock"
    
    def get_name_ar(self) -> str:
        return "المخزون"
    
    def get_icon(self) -> str:
        return "core/assets/icons/stock.png"
    
    def get_main_view_class(self):
        return ProductKanbanView
    
    def get_action_menu(self) -> list:
        return [
            {
                'name': 'Nouveau Produit',
                'name_ar': 'منتج جديد',
                'icon': 'icons/product.png',
                'callback': None
            }
        ]
    
    def initialize_db(self):
        """Crée les tables pour les produits"""
        
        # Table des produits
        self.db_manager.execute_query("""
            CREATE TABLE IF NOT EXISTS product_product (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                name_ar TEXT,
                ref TEXT,
                reference TEXT,
                barcode TEXT,
                description TEXT,
                description_ar TEXT,
                category TEXT,
                sale_price REAL DEFAULT 0,
                cost_price REAL DEFAULT 0,
                qty_available REAL DEFAULT 0,
                qty_reserved REAL DEFAULT 0,
                tax_id INTEGER,
                tax_rate REAL DEFAULT 19.0,
                category_id INTEGER,
                image BLOB,
                image_url TEXT,
                type TEXT DEFAULT 'product',
                active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (tax_id) REFERENCES account_tax (id)
            )
        """)
        
        # Ajouter colonnes si elles n'existent pas (migration)
        try:
            self.db_manager.execute_query("ALTER TABLE product_product ADD COLUMN ref TEXT")
        except:
            pass
        
        try:
            self.db_manager.execute_query("ALTER TABLE product_product ADD COLUMN category TEXT")
        except:
            pass
        
        try:
            self.db_manager.execute_query("ALTER TABLE product_product ADD COLUMN image_url TEXT")
        except:
            pass
        
        try:
            self.db_manager.execute_query("ALTER TABLE product_product ADD COLUMN type TEXT DEFAULT 'product'")
        except:
            pass
        
        try:
            self.db_manager.execute_query("ALTER TABLE product_product ADD COLUMN tax_rate REAL DEFAULT 19.0")
        except:
            pass
        
        print("  → Tables Stock créées")
