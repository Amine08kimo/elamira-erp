#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Chargement Données Démo - Module Maintenance
"""

import sys
import os
from datetime import datetime, timedelta

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import DatabaseManager

def load_maintenance_demo_data():
    """Charge les données de démonstration pour le module Maintenance"""
    
    print("=" * 60)
    print("  CHARGEMENT DONNÉES MAINTENANCE")
    print("=" * 60)
    print()
    
    # Connexion base de données
    db = DatabaseManager("database/odoo_clone_dz.db")
    
    # === 1. PIÈCES DE RECHANGE ===
    print("[1] Création pièces de rechange...")
    
    parts_data = [
        # Aiguilles
        {
            'name': 'Aiguille DB×1 #14',
            'name_ar': 'إبرة DB×1 #14',
            'reference': 'AIL-DB1-14',
            'category': 'accessory',
            'part_type': 'Aiguille',
            'compatible_machines': 'JUKI DDL-8700, BROTHER S-7300A',
            'brand': 'SCHMETZ',
            'quantity': 150,
            'min_quantity': 50,
            'purchase_price': 60.0,
            'sale_price': 80.0,
            'tax_rate': 19.0,
            'specifications': 'Aiguille industrielle standard pour tissus moyens',
            'supplier_name': 'SCHMETZ ALGÉRIE'
        },
        {
            'name': 'Aiguille DB×5 #16 (Cuir)',
            'name_ar': 'إبرة DB×5 #16 (جلد)',
            'reference': 'AIL-DB5-16',
            'category': 'accessory',
            'part_type': 'Aiguille',
            'compatible_machines': 'CONSEW 206RB, PFAFF 483',
            'brand': 'SCHMETZ',
            'quantity': 80,
            'min_quantity': 30,
            'purchase_price': 100.0,
            'sale_price': 120.0,
            'tax_rate': 19.0,
            'specifications': 'Aiguille pour cuir et tissus épais',
            'supplier_name': 'SCHMETZ ALGÉRIE'
        },
        # Canettes
        {
            'name': 'Canette Métal Standard',
            'name_ar': 'بكرة معدنية قياسية',
            'reference': 'CAN-STD-001',
            'category': 'accessory',
            'part_type': 'Canette',
            'compatible_machines': 'Toutes machines industrielles',
            'brand': 'GENERIC',
            'quantity': 200,
            'min_quantity': 100,
            'purchase_price': 40.0,
            'sale_price': 50.0,
            'tax_rate': 19.0,
            'specifications': 'Canette métallique universelle',
            'supplier_name': 'FOURNITURES GÉNÉRALES'
        },
        # Moteurs
        {
            'name': 'Servomoteur 550W',
            'name_ar': 'محرك سيرفو 550 واط',
            'reference': 'MOT-SERVO-550',
            'category': 'motor',
            'part_type': 'Moteur',
            'compatible_machines': 'JUKI DDL-8700, BROTHER S-7300A',
            'brand': 'EFKA',
            'quantity': 5,
            'min_quantity': 3,
            'purchase_price': 28000.0,
            'sale_price': 35000.0,
            'tax_rate': 19.0,
            'specifications': 'Moteur servomoteur économie énergie 550W',
            'supplier_name': 'EFKA ALGÉRIE'
        },
        {
            'name': 'Servomoteur 750W',
            'name_ar': 'محرك سيرفو 750 واط',
            'reference': 'MOT-SERVO-750',
            'category': 'motor',
            'part_type': 'Moteur',
            'compatible_machines': 'JACK JK-58420, TYPICAL GC6150H',
            'brand': 'EFKA',
            'quantity': 2,
            'min_quantity': 3,
            'purchase_price': 36000.0,
            'sale_price': 45000.0,
            'tax_rate': 19.0,
            'specifications': 'Moteur servomoteur haute puissance 750W',
            'supplier_name': 'EFKA ALGÉRIE'
        },
        # Courroies
        {
            'name': 'Courroie A-35',
            'name_ar': 'سير A-35',
            'reference': 'COU-A35-001',
            'category': 'mechanical',
            'part_type': 'Courroie',
            'compatible_machines': 'JUKI, BROTHER, JACK',
            'brand': 'GATES',
            'quantity': 25,
            'min_quantity': 15,
            'purchase_price': 800.0,
            'sale_price': 1200.0,
            'tax_rate': 19.0,
            'specifications': 'Courroie trapézoïdale type A longueur 35',
            'supplier_name': 'GATES ALGÉRIE'
        },
        # Pieds presseurs
        {
            'name': 'Pied Presseur Standard',
            'name_ar': 'قدم الضغط القياسية',
            'reference': 'PIE-STD-001',
            'category': 'accessory',
            'part_type': 'Pied Presseur',
            'compatible_machines': 'Toutes piqueuses plates',
            'brand': 'GENERIC',
            'quantity': 40,
            'min_quantity': 20,
            'purchase_price': 600.0,
            'sale_price': 800.0,
            'tax_rate': 19.0,
            'specifications': 'Pied presseur universel',
            'supplier_name': 'FOURNITURES GÉNÉRALES'
        },
        {
            'name': 'Pied Fermeture Éclair',
            'name_ar': 'قدم السحاب',
            'reference': 'PIE-ZIP-001',
            'category': 'accessory',
            'part_type': 'Pied Presseur',
            'compatible_machines': 'Toutes piqueuses plates',
            'brand': 'JUKI',
            'quantity': 15,
            'min_quantity': 10,
            'purchase_price': 1000.0,
            'sale_price': 1200.0,
            'tax_rate': 19.0,
            'specifications': 'Pied spécial pose fermeture éclair',
            'supplier_name': 'JUKI ALGÉRIE'
        },
    ]
    
    for part_data in parts_data:
        try:
            db.execute_query("""
                INSERT INTO machine_part (
                    name, name_ar, reference, category, part_type,
                    compatible_machines, brand, quantity, min_quantity,
                    purchase_price, sale_price, tax_rate,
                    specifications, supplier_name,
                    active, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                part_data['name'],
                part_data['name_ar'],
                part_data['reference'],
                part_data['category'],
                part_data['part_type'],
                part_data['compatible_machines'],
                part_data['brand'],
                part_data['quantity'],
                part_data['min_quantity'],
                part_data['purchase_price'],
                part_data['sale_price'],
                part_data['tax_rate'],
                part_data['specifications'],
                part_data['supplier_name'],
                1,
                datetime.now()
            ))
            print(f"  ✓ {part_data['name']}")
        except Exception as e:
            if "UNIQUE constraint" in str(e):
                print(f"  - {part_data['name']} (déjà existant)")
            else:
                print(f"  ✗ Erreur: {e}")
    
    print()
    
    # === 2. CONTRATS MAINTENANCE ===
    print("[2] Création contrats maintenance...")
    
    contracts_data = [
        {
            'name': 'Contrat ATELIER DE COUTURE MODERNE - Bronze',
            'reference': 'MAINT00001',
            'partner_id': 1,
            'partner_name': 'ATELIER DE COUTURE MODERNE',
            'contract_type': 'annual',
            'state': 'active',
            'date_start': datetime.now(),
            'date_end': datetime.now() + timedelta(days=365),
            'frequency': 'monthly',
            'monthly_cost': 15000.0,
            'total_amount': 180000.0,
            'preventive_maintenance': 1,
            'corrective_maintenance': 0,
            'parts_included': 0,
            'priority_support': 0,
            'interventions_max': 12,
            'description': 'Contrat Bronze - 1 visite préventive/mois',
            'terms': 'Main d\'œuvre -20%, Pièces prix normal'
        },
        {
            'name': 'Contrat USINE TEXTILE SETIF - Silver',
            'reference': 'MAINT00002',
            'partner_id': 2,
            'partner_name': 'USINE TEXTILE SETIF',
            'contract_type': 'annual',
            'state': 'active',
            'date_start': datetime.now(),
            'date_end': datetime.now() + timedelta(days=365),
            'frequency': 'biweekly',
            'monthly_cost': 25000.0,
            'total_amount': 300000.0,
            'preventive_maintenance': 1,
            'corrective_maintenance': 1,
            'parts_included': 0,
            'priority_support': 1,
            'interventions_max': 24,
            'description': 'Contrat Silver - 2 visites préventives/mois + corrective illimité',
            'terms': 'Main d\'œuvre gratuite, Pièces -30%, Support 24/7'
        },
        {
            'name': 'Contrat CONFECTION EL BARAKA - Gold',
            'reference': 'MAINT00003',
            'partner_id': 3,
            'partner_name': 'CONFECTION EL BARAKA',
            'contract_type': 'annual',
            'state': 'active',
            'date_start': datetime.now() - timedelta(days=30),
            'date_end': datetime.now() + timedelta(days=335),
            'frequency': 'weekly',
            'monthly_cost': 45000.0,
            'total_amount': 540000.0,
            'preventive_maintenance': 1,
            'corrective_maintenance': 1,
            'parts_included': 1,
            'priority_support': 1,
            'interventions_max': 999,
            'description': 'Contrat Gold - 4 visites/mois, tout inclus',
            'terms': 'Tout gratuit sauf moteurs, Intervention sous 4h, Machine remplacement'
        },
    ]
    
    for contract_data in contracts_data:
        try:
            db.execute_query("""
                INSERT INTO maintenance_contract (
                    name, reference, partner_id, partner_name,
                    contract_type, state, date_start, date_end,
                    frequency, monthly_cost, total_amount,
                    preventive_maintenance, corrective_maintenance,
                    parts_included, priority_support,
                    interventions_max, description, terms,
                    created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                contract_data['name'],
                contract_data['reference'],
                contract_data['partner_id'],
                contract_data['partner_name'],
                contract_data['contract_type'],
                contract_data['state'],
                contract_data['date_start'],
                contract_data['date_end'],
                contract_data['frequency'],
                contract_data['monthly_cost'],
                contract_data['total_amount'],
                contract_data['preventive_maintenance'],
                contract_data['corrective_maintenance'],
                contract_data['parts_included'],
                contract_data['priority_support'],
                contract_data['interventions_max'],
                contract_data['description'],
                contract_data['terms'],
                datetime.now()
            ))
            print(f"  ✓ {contract_data['reference']}")
        except Exception as e:
            if "UNIQUE constraint" in str(e):
                print(f"  - {contract_data['reference']} (déjà existant)")
            else:
                print(f"  ✗ Erreur: {e}")
    
    print()
    
    # === 3. INTERVENTIONS ===
    print("[3] Création interventions...")
    
    interventions_data = [
        {
            'name': 'Maintenance Préventive JUKI DDL-8700',
            'intervention_type': 'preventive',
            'state': 'scheduled',
            'priority': 'normal',
            'machine_id': 1,
            'machine_name': 'JUKI DDL-8700',
            'machine_serial': 'JUKI-001',
            'partner_id': 1,
            'partner_name': 'ATELIER DE COUTURE MODERNE',
            'partner_phone': '0555123456',
            'date_scheduled': datetime.now() + timedelta(days=2),
            'description': 'Maintenance préventive mensuelle',
            'technician_name': 'Mohammed BENALI',
            'labor_cost': 5500.0,
            'parts_cost': 0.0,
            'total_cost': 5500.0,
            'duration_hours': 2.0,
            'under_warranty': 0,
            'contract_id': 1
        },
        {
            'name': 'Réparation Moteur BROTHER S-7300A',
            'intervention_type': 'corrective',
            'state': 'in_progress',
            'priority': 'high',
            'machine_id': 2,
            'machine_name': 'BROTHER S-7300A',
            'machine_serial': 'BROTHER-002',
            'partner_id': 2,
            'partner_name': 'USINE TEXTILE SETIF',
            'partner_phone': '0666234567',
            'date_scheduled': datetime.now(),
            'description': 'Bruit anormal moteur - Diagnostic en cours',
            'work_done': 'Remplacement courroie, vérification alignement',
            'technician_name': 'Karim MEZIANE',
            'labor_cost': 0.0,
            'parts_cost': 1200.0,
            'total_cost': 1200.0,
            'duration_hours': 1.5,
            'under_warranty': 0,
            'contract_id': 2
        },
        {
            'name': 'Révision Complète PEGASUS M732',
            'intervention_type': 'preventive',
            'state': 'done',
            'priority': 'normal',
            'machine_id': 3,
            'machine_name': 'PEGASUS M732',
            'machine_serial': 'PEGASUS-003',
            'partner_id': 3,
            'partner_name': 'CONFECTION EL BARAKA',
            'partner_phone': '0777345678',
            'date_scheduled': datetime.now() - timedelta(days=5),
            'date_start': datetime.now() - timedelta(days=5),
            'date_end': datetime.now() - timedelta(days=5),
            'description': 'Révision complète annuelle',
            'work_done': 'Nettoyage, graissage, réglages, tests complets',
            'recommendations': 'Prochaine révision dans 6 mois',
            'technician_name': 'Ahmed SAIDI',
            'labor_cost': 0.0,
            'parts_cost': 0.0,
            'total_cost': 0.0,
            'duration_hours': 3.0,
            'under_warranty': 0,
            'contract_id': 3
        },
        {
            'name': 'Maintenance Préventive JACK JK-58420',
            'intervention_type': 'preventive',
            'state': 'scheduled',
            'priority': 'normal',
            'machine_id': 5,
            'machine_name': 'JACK JK-58420',
            'machine_serial': 'JACK-005',
            'partner_id': 2,
            'partner_name': 'USINE TEXTILE SETIF',
            'partner_phone': '0666234567',
            'date_scheduled': datetime.now() + timedelta(days=5),
            'description': 'Maintenance préventive bihebdomadaire',
            'technician_name': 'Karim MEZIANE',
            'labor_cost': 0.0,
            'parts_cost': 0.0,
            'total_cost': 0.0,
            'duration_hours': 1.5,
            'under_warranty': 0,
            'contract_id': 2
        },
    ]
    
    for inter_data in interventions_data:
        try:
            db.execute_query("""
                INSERT INTO maintenance_intervention (
                    name, intervention_type, state, priority,
                    machine_id, machine_name, machine_serial,
                    partner_id, partner_name, partner_phone,
                    date_scheduled, date_start, date_end,
                    description, work_done, recommendations,
                    technician_name, parts_used,
                    labor_cost, parts_cost, total_cost,
                    duration_hours, contract_id, under_warranty,
                    created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                inter_data['name'],
                inter_data['intervention_type'],
                inter_data['state'],
                inter_data['priority'],
                inter_data['machine_id'],
                inter_data['machine_name'],
                inter_data['machine_serial'],
                inter_data['partner_id'],
                inter_data['partner_name'],
                inter_data['partner_phone'],
                inter_data['date_scheduled'],
                inter_data.get('date_start'),
                inter_data.get('date_end'),
                inter_data['description'],
                inter_data.get('work_done'),
                inter_data.get('recommendations'),
                inter_data['technician_name'],
                None,
                inter_data['labor_cost'],
                inter_data['parts_cost'],
                inter_data['total_cost'],
                inter_data['duration_hours'],
                inter_data['contract_id'],
                inter_data['under_warranty'],
                datetime.now()
            ))
            print(f"  ✓ {inter_data['name']}")
        except Exception as e:
            print(f"  ✗ Erreur: {e}")
    
    print()
    print("=" * 60)
    print("  ✅ DONNÉES MAINTENANCE CHARGÉES")
    print("=" * 60)
    print()
    print("DONNÉES CRÉÉES :")
    print(f"  ✅ {len(parts_data)} Pièces de rechange")
    print(f"  ✅ {len(contracts_data)} Contrats maintenance")
    print(f"  ✅ {len(interventions_data)} Interventions")
    print()
    print("KPIs ATTENDUS :")
    print("  🛠️ EN COURS : 2 interventions")
    print("  📅 CE MOIS : 4 interventions")
    print("  📋 CONTRATS : 3 actifs")
    print("  ⚠️ STOCK BAS : 1 pièce (Servomoteur 750W)")
    print()
    print("Relancer : python main.py")
    print()
    
    db.close()

if __name__ == "__main__":
    load_maintenance_demo_data()
