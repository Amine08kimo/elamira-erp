# -*- coding: utf-8 -*-
"""
Maintenance Controller - Gestion Logique Maintenance
"""

from datetime import datetime, timedelta
from typing import List, Optional
from .models import MaintenanceIntervention, MaintenanceContract, MachinePart, MaintenancePlanning


class MaintenanceController:
    """Contrôleur pour la gestion de la maintenance"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    # ========== INTERVENTIONS ==========
    
    def get_all_interventions(self, state=None) -> List[MaintenanceIntervention]:
        """Récupère toutes les interventions"""
        query = "SELECT * FROM maintenance_intervention WHERE 1=1"
        params = []
        
        if state:
            query += " AND state = ?"
            params.append(state)
        
        query += " ORDER BY date_scheduled DESC"
        
        results = self.db_manager.fetch_all(query, tuple(params) if params else None)
        return [MaintenanceIntervention(**row) for row in results]
    
    def get_intervention_by_id(self, intervention_id: int) -> Optional[MaintenanceIntervention]:
        """Récupère une intervention par ID"""
        result = self.db_manager.fetch_one(
            "SELECT * FROM maintenance_intervention WHERE id = ?",
            (intervention_id,)
        )
        return MaintenanceIntervention(**result) if result else None
    
    def create_intervention(self, data: dict) -> int:
        """Crée une nouvelle intervention"""
        query = """
            INSERT INTO maintenance_intervention (
                name, intervention_type, state, priority,
                machine_id, machine_name, machine_serial,
                partner_id, partner_name, partner_phone,
                date_scheduled, description,
                technician_id, technician_name,
                labor_cost, parts_cost, total_cost,
                duration_hours, under_warranty,
                created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        params = (
            data.get('name'),
            data.get('intervention_type', 'preventive'),
            data.get('state', 'draft'),
            data.get('priority', 'normal'),
            data.get('machine_id'),
            data.get('machine_name'),
            data.get('machine_serial'),
            data.get('partner_id'),
            data.get('partner_name'),
            data.get('partner_phone'),
            data.get('date_scheduled'),
            data.get('description'),
            data.get('technician_id'),
            data.get('technician_name'),
            data.get('labor_cost', 0.0),
            data.get('parts_cost', 0.0),
            data.get('total_cost', 0.0),
            data.get('duration_hours', 0.0),
            data.get('under_warranty', False),
            datetime.now()
        )
        
        return self.db_manager.execute_query(query, params)
    
    def update_intervention(self, intervention_id: int, data: dict):
        """Met à jour une intervention"""
        fields = []
        params = []
        
        for key, value in data.items():
            fields.append(f"{key} = ?")
            params.append(value)
        
        fields.append("updated_at = ?")
        params.append(datetime.now())
        params.append(intervention_id)
        
        query = f"UPDATE maintenance_intervention SET {', '.join(fields)} WHERE id = ?"
        self.db_manager.execute_query(query, tuple(params))
    
    def get_interventions_by_machine(self, machine_id: int) -> List[MaintenanceIntervention]:
        """Récupère l'historique des interventions pour une machine"""
        results = self.db_manager.fetch_all(
            """
            SELECT * FROM maintenance_intervention
            WHERE machine_id = ?
            ORDER BY date_scheduled DESC
            """,
            (machine_id,)
        )
        return [MaintenanceIntervention(**row) for row in results]
    
    def get_scheduled_interventions(self, date_from=None, date_to=None) -> List[MaintenanceIntervention]:
        """Récupère les interventions planifiées"""
        query = """
            SELECT * FROM maintenance_intervention
            WHERE state IN ('scheduled', 'in_progress')
        """
        params = []
        
        if date_from:
            query += " AND date_scheduled >= ?"
            params.append(date_from)
        
        if date_to:
            query += " AND date_scheduled <= ?"
            params.append(date_to)
        
        query += " ORDER BY date_scheduled ASC"
        
        results = self.db_manager.fetch_all(query, tuple(params) if params else None)
        return [MaintenanceIntervention(**row) for row in results]
    
    # ========== CONTRATS ==========
    
    def get_all_contracts(self, state=None) -> List[MaintenanceContract]:
        """Récupère tous les contrats"""
        query = "SELECT * FROM maintenance_contract WHERE 1=1"
        params = []
        
        if state:
            query += " AND state = ?"
            params.append(state)
        
        query += " ORDER BY date_start DESC"
        
        results = self.db_manager.fetch_all(query, tuple(params) if params else None)
        return [MaintenanceContract(**row) for row in results]
    
    def create_contract(self, data: dict) -> int:
        """Crée un nouveau contrat"""
        query = """
            INSERT INTO maintenance_contract (
                name, reference, partner_id, partner_name,
                contract_type, state, date_start, date_end,
                frequency, monthly_cost, total_amount,
                preventive_maintenance, corrective_maintenance,
                parts_included, priority_support,
                interventions_max, description, terms,
                created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        params = (
            data.get('name'),
            data.get('reference'),
            data.get('partner_id'),
            data.get('partner_name'),
            data.get('contract_type', 'annual'),
            data.get('state', 'draft'),
            data.get('date_start'),
            data.get('date_end'),
            data.get('frequency', 'monthly'),
            data.get('monthly_cost', 0.0),
            data.get('total_amount', 0.0),
            data.get('preventive_maintenance', True),
            data.get('corrective_maintenance', False),
            data.get('parts_included', False),
            data.get('priority_support', False),
            data.get('interventions_max', 12),
            data.get('description'),
            data.get('terms'),
            datetime.now()
        )
        
        return self.db_manager.execute_query(query, params)
    
    # ========== PIÈCES DE RECHANGE ==========
    
    def get_all_parts(self, category=None) -> List[MachinePart]:
        """Récupère toutes les pièces"""
        query = "SELECT * FROM machine_part WHERE active = 1"
        params = []
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        query += " ORDER BY name ASC"
        
        results = self.db_manager.fetch_all(query, tuple(params) if params else None)
        return [MachinePart(**row) for row in results]
    
    def get_low_stock_parts(self) -> List[MachinePart]:
        """Récupère les pièces en stock faible"""
        results = self.db_manager.fetch_all(
            """
            SELECT * FROM machine_part
            WHERE active = 1 AND quantity <= min_quantity
            ORDER BY quantity ASC
            """
        )
        return [MachinePart(**row) for row in results]
    
    def create_part(self, data: dict) -> int:
        """Crée une nouvelle pièce"""
        query = """
            INSERT INTO machine_part (
                name, name_ar, reference, category, part_type,
                compatible_machines, brand, quantity, min_quantity,
                purchase_price, sale_price, tax_rate,
                specifications, image_url, supplier_name,
                active, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        params = (
            data.get('name'),
            data.get('name_ar'),
            data.get('reference'),
            data.get('category', 'accessory'),
            data.get('part_type'),
            data.get('compatible_machines'),
            data.get('brand'),
            data.get('quantity', 0),
            data.get('min_quantity', 5),
            data.get('purchase_price', 0.0),
            data.get('sale_price', 0.0),
            data.get('tax_rate', 19.0),
            data.get('specifications'),
            data.get('image_url'),
            data.get('supplier_name'),
            True,
            datetime.now()
        )
        
        return self.db_manager.execute_query(query, params)
    
    def update_part_stock(self, part_id: int, quantity_change: int):
        """Met à jour le stock d'une pièce"""
        self.db_manager.execute_query(
            """
            UPDATE machine_part
            SET quantity = quantity + ?, updated_at = ?
            WHERE id = ?
            """,
            (quantity_change, datetime.now(), part_id)
        )
    
    # ========== STATISTIQUES ==========
    
    def get_maintenance_stats(self) -> dict:
        """Récupère les statistiques de maintenance"""
        # Interventions en cours
        pending = self.db_manager.fetch_one(
            "SELECT COUNT(*) as count FROM maintenance_intervention WHERE state IN ('scheduled', 'in_progress')"
        )
        
        # Interventions ce mois
        this_month = self.db_manager.fetch_one(
            """
            SELECT COUNT(*) as count FROM maintenance_intervention
            WHERE strftime('%Y-%m', date_scheduled) = strftime('%Y-%m', 'now')
            """
        )
        
        # Contrats actifs
        active_contracts = self.db_manager.fetch_one(
            "SELECT COUNT(*) as count FROM maintenance_contract WHERE state = 'active'"
        )
        
        # Pièces en stock faible
        low_stock = self.db_manager.fetch_one(
            "SELECT COUNT(*) as count FROM machine_part WHERE quantity <= min_quantity"
        )
        
        # Revenus ce mois
        revenue = self.db_manager.fetch_one(
            """
            SELECT COALESCE(SUM(total_cost), 0) as total FROM maintenance_intervention
            WHERE strftime('%Y-%m', date_scheduled) = strftime('%Y-%m', 'now')
            AND state = 'done'
            """
        )
        
        return {
            'pending_interventions': pending['count'] if pending else 0,
            'monthly_interventions': this_month['count'] if this_month else 0,
            'active_contracts': active_contracts['count'] if active_contracts else 0,
            'low_stock_parts': low_stock['count'] if low_stock else 0,
            'monthly_revenue': revenue['total'] if revenue else 0
        }
