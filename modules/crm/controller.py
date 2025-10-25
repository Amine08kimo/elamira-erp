# -*- coding: utf-8 -*-
"""
CRM Controller - Logique métier pour la gestion CRM
"""

from typing import List, Optional
from datetime import datetime
from .models import Lead, CRMStage


class CRMController:
    """Contrôleur pour la gestion CRM"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def create_lead(self, lead: Lead) -> int:
        """
        Crée une nouvelle opportunité
        
        Args:
            lead: Objet Lead à créer
            
        Returns:
            ID du lead créé
        """
        cursor = self.db.execute_query("""
            INSERT INTO crm_lead (
                name, partner_id, contact_name, email, phone,
                expected_revenue, probability, stage_id, priority,
                date_deadline, user_id, description, active
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            lead.name, lead.partner_id, lead.contact_name,
            lead.email, lead.phone, lead.expected_revenue,
            lead.probability, lead.stage_id, lead.priority,
            lead.date_deadline.isoformat() if lead.date_deadline else None,
            lead.user_id, lead.description, lead.active
        ))
        
        return cursor.lastrowid
    
    def get_all_leads(self) -> List[Lead]:
        """Récupère toutes les opportunités actives"""
        rows = self.db.fetch_all("""
            SELECT l.*, p.name as partner_name
            FROM crm_lead l
            LEFT JOIN res_partner p ON l.partner_id = p.id
            WHERE l.active = 1
            ORDER BY l.created_at DESC
        """)
        
        return [self._row_to_lead(row) for row in rows]
    
    def get_leads_by_stage(self, stage_id: int) -> List[Lead]:
        """Récupère les leads d'une étape spécifique"""
        rows = self.db.fetch_all("""
            SELECT l.*, p.name as partner_name
            FROM crm_lead l
            LEFT JOIN res_partner p ON l.partner_id = p.id
            WHERE l.stage_id = ? AND l.active = 1
            ORDER BY l.probability DESC, l.expected_revenue DESC
        """, (stage_id,))
        
        return [self._row_to_lead(row) for row in rows]
    
    def update_lead(self, lead: Lead) -> bool:
        """Met à jour une opportunité"""
        self.db.execute_query("""
            UPDATE crm_lead SET
                name = ?, partner_id = ?, contact_name = ?,
                email = ?, phone = ?, expected_revenue = ?,
                probability = ?, stage_id = ?, priority = ?,
                date_deadline = ?, description = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            lead.name, lead.partner_id, lead.contact_name,
            lead.email, lead.phone, lead.expected_revenue,
            lead.probability, lead.stage_id, lead.priority,
            lead.date_deadline.isoformat() if lead.date_deadline else None,
            lead.description, lead.id
        ))
        
        return True
    
    def move_lead_to_stage(self, lead_id: int, stage_id: int) -> bool:
        """Déplace un lead vers une autre étape"""
        self.db.execute_query("""
            UPDATE crm_lead SET
                stage_id = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (stage_id, lead_id))
        
        return True
    
    def get_all_stages(self) -> List[CRMStage]:
        """Récupère toutes les étapes du pipeline"""
        rows = self.db.fetch_all("""
            SELECT * FROM crm_stage
            ORDER BY sequence
        """)
        
        return [self._row_to_stage(row) for row in rows]
    
    def get_pipeline_stats(self) -> dict:
        """Statistiques du pipeline CRM"""
        stats = {}
        
        # Nombre total de leads
        total = self.db.fetch_one("""
            SELECT COUNT(*) as count FROM crm_lead WHERE active = 1
        """)
        stats['total_leads'] = total['count'] if total else 0
        
        # Revenu attendu total
        revenue = self.db.fetch_one("""
            SELECT SUM(expected_revenue) as total
            FROM crm_lead WHERE active = 1
        """)
        stats['expected_revenue'] = revenue['total'] if revenue and revenue['total'] else 0
        
        # Taux de conversion (leads gagnés / total)
        won_stage = self.db.fetch_one("""
            SELECT id FROM crm_stage WHERE name = 'Gagné' LIMIT 1
        """)
        
        if won_stage:
            won = self.db.fetch_one("""
                SELECT COUNT(*) as count FROM crm_lead
                WHERE stage_id = ? AND active = 1
            """, (won_stage['id'],))
            stats['won_leads'] = won['count'] if won else 0
            
            if stats['total_leads'] > 0:
                stats['conversion_rate'] = (stats['won_leads'] / stats['total_leads']) * 100
            else:
                stats['conversion_rate'] = 0
        else:
            stats['won_leads'] = 0
            stats['conversion_rate'] = 0
        
        return stats
    
    def _row_to_lead(self, row: dict) -> Lead:
        """Convertit une ligne DB en Lead"""
        return Lead(
            id=row['id'],
            name=row['name'],
            partner_id=row.get('partner_id'),
            partner_name=row.get('partner_name', ''),
            contact_name=row.get('contact_name', ''),
            email=row.get('email', ''),
            phone=row.get('phone', ''),
            expected_revenue=row.get('expected_revenue', 0.0),
            probability=row.get('probability', 0.0),
            stage_id=row['stage_id'],
            priority=row.get('priority', 'medium'),
            date_deadline=datetime.fromisoformat(row['date_deadline']) if row.get('date_deadline') else None,
            user_id=row.get('user_id'),
            description=row.get('description', ''),
            active=bool(row.get('active', 1)),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def _row_to_stage(self, row: dict) -> CRMStage:
        """Convertit une ligne DB en CRMStage"""
        return CRMStage(
            id=row['id'],
            name=row['name'],
            name_ar=row.get('name_ar', ''),
            sequence=row['sequence'],
            fold=bool(row.get('fold', 0)),
            probability=row.get('probability', 0.0)
        )
