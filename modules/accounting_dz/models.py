# -*- coding: utf-8 -*-
"""
Accounting Models - Modèles comptables conformes DZ
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class AccountMove:
    """
    Pièce comptable (Écriture)
    Conforme au PCN algérien
    """
    id: Optional[int] = None
    name: str = ""  # Numéro de pièce
    ref: str = ""   # Référence externe
    date: datetime = field(default_factory=datetime.now)
    journal_id: int = 1
    state: str = "draft"  # draft, posted, cancelled
    
    # Lignes d'écriture
    line_ids: List['AccountMoveLine'] = field(default_factory=list)
    
    # Totaux
    amount_total: float = 0.0
    
    notes: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class AccountMoveLine:
    """Ligne d'écriture comptable"""
    id: Optional[int] = None
    move_id: Optional[int] = None
    name: str = ""  # Libellé
    pcn_account_id: int = 0  # Compte PCN
    debit: float = 0.0
    credit: float = 0.0
    partner_id: Optional[int] = None


@dataclass
class G12Declaration:
    """
    Déclaration G12 (TVA mensuelle/trimestrielle)
    Spécifique au marché algérien
    """
    id: Optional[int] = None
    name: str = ""
    period_start: datetime = field(default_factory=datetime.now)
    period_end: datetime = field(default_factory=datetime.now)
    state: str = "draft"  # draft, submitted
    
    # Chiffre d'affaires
    ca_ht: float = 0.0
    ca_exonere: float = 0.0
    ca_total: float = 0.0
    
    # TVA Collectée
    tva_19_base: float = 0.0
    tva_19_amount: float = 0.0
    tva_9_base: float = 0.0
    tva_9_amount: float = 0.0
    tva_collectee_total: float = 0.0
    
    # TVA Déductible
    tva_deductible_immobilisations: float = 0.0
    tva_deductible_biens: float = 0.0
    tva_deductible_services: float = 0.0
    tva_deductible_total: float = 0.0
    
    # TVA à payer/Crédit
    tva_due: float = 0.0
    tva_credit_report: float = 0.0
    tva_a_payer: float = 0.0
    
    # TAP
    tap_base: float = 0.0
    tap_rate: float = 2.0
    tap_amount: float = 0.0
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def calculate_totals(self):
        """Calcule tous les totaux de la déclaration"""
        # TVA Collectée
        self.tva_19_amount = self.tva_19_base * 0.19
        self.tva_9_amount = self.tva_9_base * 0.09
        self.tva_collectee_total = self.tva_19_amount + self.tva_9_amount
        
        # TVA Déductible
        self.tva_deductible_total = (
            self.tva_deductible_immobilisations +
            self.tva_deductible_biens +
            self.tva_deductible_services
        )
        
        # TVA Due
        self.tva_due = self.tva_collectee_total - self.tva_deductible_total
        
        # TVA à payer (avec crédit reporté)
        self.tva_a_payer = self.tva_due - self.tva_credit_report
        
        # TAP
        self.tap_amount = self.tap_base * (self.tap_rate / 100)
        
        # CA Total
        self.ca_total = self.ca_ht + self.ca_exonere
