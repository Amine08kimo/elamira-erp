# -*- coding: utf-8 -*-
"""
Stock Controller - Logique métier pour la gestion du stock
"""

from typing import List, Optional
from .models import Product, StockQuant


class StockController:
    """Contrôleur pour la gestion du stock"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def create_product(self, product: Product) -> int:
        """
        Crée un nouveau produit
        
        Args:
            product: Objet Product à créer
            
        Returns:
            ID du produit créé
        """
        cursor = self.db.execute_query("""
            INSERT INTO product_product (
                name, name_ar, reference, barcode, description, description_ar,
                sale_price, cost_price, qty_available, tax_id, category_id, active
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            product.name, product.name_ar, product.reference, product.barcode,
            product.description, product.description_ar,
            product.sale_price, product.cost_price, product.qty_available,
            product.tax_id, product.category_id, product.active
        ))
        
        return cursor.lastrowid
    
    def get_all_products(self) -> List[Product]:
        """Récupère tous les produits actifs"""
        rows = self.db.fetch_all("""
            SELECT * FROM product_product 
            WHERE active = 1
            ORDER BY name
        """)
        
        return [self._row_to_product(row) for row in rows]
    
    def get_product(self, product_id: int) -> Optional[Product]:
        """Récupère un produit par ID"""
        row = self.db.fetch_one(
            "SELECT * FROM product_product WHERE id = ?",
            (product_id,)
        )
        
        return self._row_to_product(row) if row else None
    
    def update_product(self, product: Product) -> bool:
        """Met à jour un produit"""
        self.db.execute_query("""
            UPDATE product_product 
            SET name = ?, name_ar = ?, reference = ?, barcode = ?,
                description = ?, description_ar = ?,
                sale_price = ?, cost_price = ?, tax_id = ?,
                category_id = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            product.name, product.name_ar, product.reference, product.barcode,
            product.description, product.description_ar,
            product.sale_price, product.cost_price, product.tax_id,
            product.category_id, product.id
        ))
        
        return True
    
    def update_stock(self, product_id: int, quantity_delta: float) -> bool:
        """
        Met à jour le stock d'un produit
        
        Args:
            product_id: ID du produit
            quantity_delta: Variation de quantité (+ ou -)
        """
        self.db.execute_query("""
            UPDATE product_product 
            SET qty_available = qty_available + ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (quantity_delta, product_id))
        
        return True
    
    def search_products(self, query: str) -> List[Product]:
        """Recherche des produits par nom, référence ou code-barres"""
        rows = self.db.fetch_all("""
            SELECT * FROM product_product 
            WHERE (name LIKE ? OR reference LIKE ? OR barcode LIKE ?)
            AND active = 1
            ORDER BY name
            LIMIT 50
        """, (f'%{query}%', f'%{query}%', f'%{query}%'))
        
        return [self._row_to_product(row) for row in rows]
    
    def _row_to_product(self, row: dict) -> Product:
        """Convertit une ligne DB en objet Product"""
        return Product(
            id=row['id'],
            name=row['name'],
            name_ar=row.get('name_ar', ''),
            reference=row.get('reference', ''),
            barcode=row.get('barcode', ''),
            description=row.get('description', ''),
            description_ar=row.get('description_ar', ''),
            sale_price=row.get('sale_price', 0.0),
            cost_price=row.get('cost_price', 0.0),
            qty_available=row.get('qty_available', 0.0),
            qty_reserved=row.get('qty_reserved', 0.0),
            tax_id=row.get('tax_id'),
            category_id=row.get('category_id'),
            active=bool(row.get('active', 1)),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
