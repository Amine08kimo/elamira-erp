# -*- coding: utf-8 -*-
"""
Sales Models - Modèles de données pour les ventes
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class Partner:
    """
    Modèle pour un partenaire (Client/Fournisseur)
    Inclut les champs fiscaux obligatoires algériens
    """
    id: Optional[int] = None
    name: str = ""
    name_ar: str = ""
    address: str = ""
    address_ar: str = ""
    phone: str = ""
    email: str = ""
    
    # Identifiants fiscaux DZ (obligatoires)
    nif: str = ""  # Numéro d'Identification Fiscale
    nis: str = ""  # Numéro d'Identification Statistique
    art: str = ""  # Article du Registre du Commerce
    
    is_customer: bool = True
    is_supplier: bool = False
    active: bool = True
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class SaleOrderLine:
    """Ligne d'une commande de vente"""
    id: Optional[int] = None
    order_id: Optional[int] = None
    product_id: int = 0
    product_name: str = ""
    description: str = ""
    quantity: float = 1.0
    price_unit: float = 0.0
    tax_id: Optional[int] = None  # TVA
    tax_rate: float = 0.0
    discount: float = 0.0
    
    # Calculés
    subtotal: float = 0.0  # HT
    tax_amount: float = 0.0
    total: float = 0.0  # TTC
    
    def calculate_amounts(self):
        """Calcule les montants de la ligne"""
        # Sous-total HT avec remise
        self.subtotal = self.quantity * self.price_unit * (1 - self.discount / 100)
        
        # Montant de la taxe
        self.tax_amount = self.subtotal * (self.tax_rate / 100)
        
        # Total TTC
        self.total = self.subtotal + self.tax_amount


@dataclass
class SaleOrder:
    """
    Commande/Facture de Vente
    Conforme aux normes de facturation algériennes
    Support: Facture, Proforma, Bon de Commande, Bon de Livraison
    """
    id: Optional[int] = None
    name: str = ""  # Numéro de facture (ex: INV00001)
    partner_id: int = 0
    partner_name: str = ""
    
    # Type de document
    document_type: str = "invoice"  # invoice, proforma, order, delivery
    
    date_order: datetime = field(default_factory=datetime.now)
    date_due: Optional[datetime] = None
    date_delivery: Optional[datetime] = None  # Pour bon de livraison
    
    state: str = "draft"  # draft, confirmed, done, cancelled
    
    # Lignes de commande
    order_lines: List[SaleOrderLine] = field(default_factory=list)
    
    # Montants
    amount_untaxed: float = 0.0  # Total HT
    amount_tax: float = 0.0      # Total TVA
    amount_tap: float = 0.0      # TAP (Taxe sur l'Activité Professionnelle)
    amount_stamp: float = 0.0    # Timbre fiscal
    amount_total: float = 0.0    # Total TTC
    
    # Notes et termes
    notes: str = ""
    payment_term: str = ""
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def calculate_totals(self):
        """Calcule tous les totaux de la commande"""
        self.amount_untaxed = 0.0
        self.amount_tax = 0.0
        
        for line in self.order_lines:
            line.calculate_amounts()
            self.amount_untaxed += line.subtotal
            self.amount_tax += line.tax_amount
        
        # Calculer TAP (2% du CA HT typiquement)
        # self.amount_tap = self.amount_untaxed * 0.02
        
        # Timbre fiscal (montant fixe, ex: 25 DA)
        # self.amount_stamp = 25.0
        
        # Total TTC
        self.amount_total = (
            self.amount_untaxed + 
            self.amount_tax + 
            self.amount_tap + 
            self.amount_stamp
        )
