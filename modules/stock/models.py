# -*- coding: utf-8 -*-
"""
Stock Models - Modèles pour la gestion du stock
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Product:
    """Modèle pour un produit"""
    id: Optional[int] = None
    name: str = ""
    name_ar: str = ""
    reference: str = ""
    barcode: str = ""
    description: str = ""
    description_ar: str = ""
    
    # Prix
    sale_price: float = 0.0
    cost_price: float = 0.0
    
    # Stock
    qty_available: float = 0.0
    qty_reserved: float = 0.0
    
    # Taxes
    tax_id: Optional[int] = None
    
    # Catégorie
    category_id: Optional[int] = None
    
    # Image
    image: Optional[bytes] = None
    
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class StockQuant:
    """Quantité en stock pour un produit"""
    id: Optional[int] = None
    product_id: int = 0
    location_id: int = 1  # ID de l'emplacement
    quantity: float = 0.0
    reserved_quantity: float = 0.0
    updated_at: Optional[datetime] = None
