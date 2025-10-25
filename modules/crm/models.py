# -*- coding: utf-8 -*-
"""
CRM Models - Modèles pour la gestion de la relation client
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Lead:
    """
    Lead/Opportunité commerciale
    """
    id: Optional[int] = None
    name: str = ""  # Nom de l'opportunité
    partner_id: Optional[int] = None
    partner_name: str = ""
    
    # Contact
    contact_name: str = ""
    email: str = ""
    phone: str = ""
    
    # Informations commerciales
    expected_revenue: float = 0.0
    probability: float = 0.0  # 0-100%
    stage_id: int = 1
    priority: str = "medium"  # low, medium, high
    
    # Dates
    date_deadline: Optional[datetime] = None
    date_closed: Optional[datetime] = None
    
    # Suivi
    user_id: Optional[int] = None
    team_id: Optional[int] = None
    description: str = ""
    
    # État
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class CRMStage:
    """Étape du pipeline CRM"""
    id: Optional[int] = None
    name: str = ""
    name_ar: str = ""
    sequence: int = 10
    fold: bool = False  # Masqué par défaut dans Kanban
    probability: float = 0.0
