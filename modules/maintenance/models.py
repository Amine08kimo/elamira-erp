# -*- coding: utf-8 -*-
"""
Maintenance Models - Modèles pour Maintenance Machines à Coudre
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class MaintenanceIntervention:
    """
    Intervention de Maintenance
    Pour machines à coudre - préventive ou corrective
    """
    id: Optional[int] = None
    name: str = ""  # Ex: "Maintenance préventive JUKI DDL-8700"
    
    # Type et statut
    intervention_type: str = "preventive"  # preventive, corrective, warranty
    state: str = "draft"  # draft, scheduled, in_progress, done, cancelled
    priority: str = "normal"  # low, normal, high, urgent
    
    # Machine concernée
    machine_id: Optional[int] = None
    machine_name: str = ""
    machine_serial: str = ""
    
    # Client
    partner_id: Optional[int] = None
    partner_name: str = ""
    partner_phone: str = ""
    
    # Dates
    date_scheduled: Optional[datetime] = None
    date_start: Optional[datetime] = None
    date_end: Optional[datetime] = None
    date_next: Optional[datetime] = None  # Prochaine maintenance
    
    # Détails technique
    description: str = ""  # Description du problème
    work_done: str = ""  # Travaux effectués
    recommendations: str = ""  # Recommandations
    
    # Technicien
    technician_id: Optional[int] = None
    technician_name: str = ""
    
    # Pièces utilisées
    parts_used: str = ""  # JSON des pièces
    
    # Financier
    labor_cost: float = 0.0  # Coût main d'œuvre
    parts_cost: float = 0.0  # Coût pièces
    total_cost: float = 0.0  # Total
    
    # Durée
    duration_hours: float = 0.0  # Durée en heures
    
    # Contrat
    contract_id: Optional[int] = None
    under_warranty: bool = False
    
    # Métadonnées
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    
    # Notes
    internal_notes: str = ""
    customer_notes: str = ""


@dataclass
class MaintenanceContract:
    """
    Contrat de Maintenance
    Maintenance préventive planifiée
    """
    id: Optional[int] = None
    name: str = ""  # Ex: "Contrat annuel - ATELIER MODERNE"
    reference: str = ""  # Ex: "MAINT-2024-001"
    
    # Client
    partner_id: int = 0
    partner_name: str = ""
    
    # Type et statut
    contract_type: str = "annual"  # monthly, quarterly, annual
    state: str = "draft"  # draft, active, expired, cancelled
    
    # Dates
    date_start: datetime = field(default_factory=datetime.now)
    date_end: Optional[datetime] = None
    
    # Périodicité
    frequency: str = "monthly"  # weekly, monthly, quarterly, annual
    next_intervention: Optional[datetime] = None
    
    # Machines couvertes
    machines_count: int = 0
    machines_list: str = ""  # JSON liste machines
    
    # Financier
    monthly_cost: float = 0.0
    total_amount: float = 0.0
    invoiced_amount: float = 0.0
    
    # Services inclus
    preventive_maintenance: bool = True
    corrective_maintenance: bool = False
    parts_included: bool = False
    priority_support: bool = False
    
    # Interventions
    interventions_count: int = 0
    interventions_max: int = 12  # Nombre max par an
    
    # Notes
    description: str = ""
    terms: str = ""  # Conditions du contrat
    
    # Métadonnées
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None


@dataclass
class MachinePart:
    """
    Pièce de Rechange pour Machine à Coudre
    """
    id: Optional[int] = None
    name: str = ""  # Ex: "Aiguille industrielle DB×1"
    name_ar: str = ""
    reference: str = ""  # Référence fabricant
    
    # Catégorie
    category: str = "accessory"  # accessory, motor, electronic, mechanical
    part_type: str = ""  # aiguille, canette, moteur, courroie, etc.
    
    # Compatibilité
    compatible_machines: str = ""  # JSON liste machines compatibles
    brand: str = ""  # Marque
    
    # Stock
    quantity: int = 0
    min_quantity: int = 5  # Seuil alerte
    location: str = ""  # Emplacement stock
    
    # Prix
    purchase_price: float = 0.0
    sale_price: float = 0.0
    tax_rate: float = 19.0
    
    # Caractéristiques
    specifications: str = ""  # Spécifications techniques
    image_url: str = ""
    
    # Fournisseur
    supplier_id: Optional[int] = None
    supplier_name: str = ""
    supplier_ref: str = ""
    
    # Métadonnées
    active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None


@dataclass
class MaintenancePlanning:
    """
    Planning de Maintenance
    """
    id: Optional[int] = None
    
    # Machine
    machine_id: int = 0
    machine_name: str = ""
    
    # Type maintenance
    maintenance_type: str = "preventive"
    
    # Périodicité
    frequency: str = "monthly"  # weekly, monthly, quarterly, annual
    frequency_value: int = 1  # Tous les X mois/semaines
    
    # Prochaine intervention
    next_date: Optional[datetime] = None
    last_date: Optional[datetime] = None
    
    # Durée estimée
    estimated_hours: float = 2.0
    
    # Responsable
    technician_id: Optional[int] = None
    technician_name: str = ""
    
    # Contrat lié
    contract_id: Optional[int] = None
    
    # Statut
    active: bool = True
    
    # Checklist
    checklist: str = ""  # JSON checklist maintenance
    
    # Notes
    notes: str = ""
