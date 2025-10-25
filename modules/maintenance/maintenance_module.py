# -*- coding: utf-8 -*-
"""
Maintenance Module - Module Gestion Maintenance Machines à Coudre
"""

from core.base_module import BaseModule


class MaintenanceModule(BaseModule):
    """Module de gestion de la maintenance"""
    
    def __init__(self, db_manager, license_manager=None):
        super().__init__(db_manager)
        self.license_manager = license_manager
    
    def initialize_db(self):
        """Initialise les tables de maintenance"""
        
        # Table interventions
        self.db_manager.execute_query("""
            CREATE TABLE IF NOT EXISTS maintenance_intervention (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                intervention_type TEXT DEFAULT 'preventive',
                state TEXT DEFAULT 'draft',
                priority TEXT DEFAULT 'normal',
                
                machine_id INTEGER,
                machine_name TEXT,
                machine_serial TEXT,
                
                partner_id INTEGER,
                partner_name TEXT,
                partner_phone TEXT,
                
                date_scheduled TIMESTAMP,
                date_start TIMESTAMP,
                date_end TIMESTAMP,
                date_next TIMESTAMP,
                
                description TEXT,
                work_done TEXT,
                recommendations TEXT,
                
                technician_id INTEGER,
                technician_name TEXT,
                
                parts_used TEXT,
                
                labor_cost REAL DEFAULT 0.0,
                parts_cost REAL DEFAULT 0.0,
                total_cost REAL DEFAULT 0.0,
                
                duration_hours REAL DEFAULT 0.0,
                
                contract_id INTEGER,
                under_warranty INTEGER DEFAULT 0,
                
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP,
                
                internal_notes TEXT,
                customer_notes TEXT,
                
                FOREIGN KEY (machine_id) REFERENCES product_product(id),
                FOREIGN KEY (partner_id) REFERENCES res_partner(id),
                FOREIGN KEY (contract_id) REFERENCES maintenance_contract(id)
            )
        """)
        
        # Table contrats maintenance
        self.db_manager.execute_query("""
            CREATE TABLE IF NOT EXISTS maintenance_contract (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                reference TEXT UNIQUE,
                
                partner_id INTEGER NOT NULL,
                partner_name TEXT,
                
                contract_type TEXT DEFAULT 'annual',
                state TEXT DEFAULT 'draft',
                
                date_start TIMESTAMP,
                date_end TIMESTAMP,
                
                frequency TEXT DEFAULT 'monthly',
                next_intervention TIMESTAMP,
                
                machines_count INTEGER DEFAULT 0,
                machines_list TEXT,
                
                monthly_cost REAL DEFAULT 0.0,
                total_amount REAL DEFAULT 0.0,
                invoiced_amount REAL DEFAULT 0.0,
                
                preventive_maintenance INTEGER DEFAULT 1,
                corrective_maintenance INTEGER DEFAULT 0,
                parts_included INTEGER DEFAULT 0,
                priority_support INTEGER DEFAULT 0,
                
                interventions_count INTEGER DEFAULT 0,
                interventions_max INTEGER DEFAULT 12,
                
                description TEXT,
                terms TEXT,
                
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP,
                
                FOREIGN KEY (partner_id) REFERENCES res_partner(id)
            )
        """)
        
        # Table pièces de rechange
        self.db_manager.execute_query("""
            CREATE TABLE IF NOT EXISTS machine_part (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                name_ar TEXT,
                reference TEXT UNIQUE,
                
                category TEXT DEFAULT 'accessory',
                part_type TEXT,
                
                compatible_machines TEXT,
                brand TEXT,
                
                quantity INTEGER DEFAULT 0,
                min_quantity INTEGER DEFAULT 5,
                location TEXT,
                
                purchase_price REAL DEFAULT 0.0,
                sale_price REAL DEFAULT 0.0,
                tax_rate REAL DEFAULT 19.0,
                
                specifications TEXT,
                image_url TEXT,
                
                supplier_id INTEGER,
                supplier_name TEXT,
                supplier_ref TEXT,
                
                active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP,
                
                FOREIGN KEY (supplier_id) REFERENCES res_partner(id)
            )
        """)
        
        # Table planning maintenance
        self.db_manager.execute_query("""
            CREATE TABLE IF NOT EXISTS maintenance_planning (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                
                machine_id INTEGER NOT NULL,
                machine_name TEXT,
                
                maintenance_type TEXT DEFAULT 'preventive',
                
                frequency TEXT DEFAULT 'monthly',
                frequency_value INTEGER DEFAULT 1,
                
                next_date TIMESTAMP,
                last_date TIMESTAMP,
                
                estimated_hours REAL DEFAULT 2.0,
                
                technician_id INTEGER,
                technician_name TEXT,
                
                contract_id INTEGER,
                
                active INTEGER DEFAULT 1,
                
                checklist TEXT,
                notes TEXT,
                
                FOREIGN KEY (machine_id) REFERENCES product_product(id),
                FOREIGN KEY (contract_id) REFERENCES maintenance_contract(id)
            )
        """)
        
        # Séquence pour contrats
        self.db_manager.execute_query("""
            INSERT OR IGNORE INTO ir_sequence (name, code, prefix, padding, next_number)
            VALUES ('Contrats Maintenance', 'maintenance.contract', 'MAINT', 5, 1)
        """)
        
        print("  → Tables Maintenance créées")
    
    def get_views(self):
        """Retourne les vues du module"""
        from .views import (
            MaintenanceInterventionListView,
            MaintenanceContractListView,
            MachinePartListView,
            MaintenanceDashboardView
        )
        
        return {
            'Interventions': MaintenanceInterventionListView,
            'Contrats': MaintenanceContractListView,
            'Pièces de Rechange': MachinePartListView,
            'Dashboard Maintenance': MaintenanceDashboardView
        }
    
    def get_menu_items(self):
        """Retourne les items du menu"""
        return [
            {
                'name': '🔧 Dashboard',
                'view': 'Dashboard Maintenance',
                'icon': '📊'
            },
            {
                'name': '🛠️ Interventions',
                'view': 'Interventions',
                'icon': '🔧'
            },
            {
                'name': '📋 Contrats',
                'view': 'Contrats',
                'icon': '📄'
            },
            {
                'name': '🔩 Pièces de Rechange',
                'view': 'Pièces de Rechange',
                'icon': '⚙️'
            }
        ]
    
    def get_name(self):
        """Retourne le nom du module"""
        return "Maintenance"
    
    def get_name_ar(self):
        """Retourne le nom du module en arabe"""
        return "الصيانة"
    
    def get_icon(self):
        """Retourne le chemin de l'icône"""
        return "🔧"
    
    def get_main_view_class(self):
        """Retourne la classe de vue principale"""
        from .views import MaintenanceDashboardView
        return MaintenanceDashboardView
    
    def get_action_menu(self):
        """Retourne le menu des actions"""
        return self.get_menu_items()
