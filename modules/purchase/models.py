# -*- coding: utf-8 -*-
"""
Purchase Models - Modèles pour les achats fournisseurs
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class PurchaseOrderLine:
    """Ligne d'une commande d'achat (facture fournisseur)"""
    id: Optional[int] = None
    order_id: Optional[int] = None
    product_id: Optional[int] = None
    product_name: str = ""
    description: str = ""
    quantity: float = 1.0
    price_unit: float = 0.0
    tax_rate: float = 19.0  # TVA déductible
    subtotal: float = 0.0
    tax_amount: float = 0.0
    total: float = 0.0
    
    def calculate_amounts(self):
        """Calcule les montants de la ligne"""
        self.subtotal = self.quantity * self.price_unit
        self.tax_amount = self.subtotal * (self.tax_rate / 100)
        self.total = self.subtotal + self.tax_amount


@dataclass
class PurchaseOrder:
    """Commande d'achat / Facture fournisseur"""
    id: Optional[int] = None
    name: str = ""  # Numéro de facture
    partner_id: Optional[int] = None
    partner_name: str = ""
    
    # Référence fournisseur
    supplier_invoice_ref: str = ""  # Numéro facture fournisseur
    
    # Dates
    date_order: Optional[datetime] = None
    date_due: Optional[datetime] = None
    date_received: Optional[datetime] = None
    
    # État
    state: str = "draft"  # draft, confirmed, received, paid, cancelled
    
    # Montants (en DA)
    amount_untaxed: float = 0.0  # HT
    amount_tax: float = 0.0  # TVA déductible
    amount_total: float = 0.0  # TTC
    
    # Informations complémentaires
    notes: str = ""
    payment_term: str = ""
    
    # Lignes de commande
    lines: List[PurchaseOrderLine] = None
    
    # Métadonnées
    user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.lines is None:
            self.lines = []
        if self.date_order is None:
            self.date_order = datetime.now()
    
    def calculate_totals(self):
        """Calcule les totaux de la commande"""
        self.amount_untaxed = sum(line.subtotal for line in self.lines)
        self.amount_tax = sum(line.tax_amount for line in self.lines)
        self.amount_total = self.amount_untaxed + self.amount_tax
    
    def add_line(self, line: PurchaseOrderLine):
        """Ajoute une ligne à la commande"""
        line.calculate_amounts()
        self.lines.append(line)
        self.calculate_totals()
    
    def get_state_label(self) -> str:
        """Retourne le libellé du statut"""
        states = {
            'draft': 'Brouillon',
            'confirmed': 'Confirmée',
            'received': 'Réceptionnée',
            'paid': 'Payée',
            'cancelled': 'Annulée'
        }
        return states.get(self.state, self.state)
    
    def get_state_label_ar(self) -> str:
        """Retourne le libellé du statut en arabe"""
        states = {
            'draft': 'مسودة',
            'confirmed': 'مؤكد',
            'received': 'مستلم',
            'paid': 'مدفوع',
            'cancelled': 'ملغى'
        }
        return states.get(self.state, self.state)
