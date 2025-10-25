#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test des statistiques Maintenance
"""

from core.database import DatabaseManager
from modules.maintenance.controller import MaintenanceController

print("=" * 60)
print("  TEST STATISTIQUES MAINTENANCE")
print("=" * 60)
print()

db = DatabaseManager("database/odoo_clone_dz.db")
controller = MaintenanceController(db)

print("[1] Test get_maintenance_stats()...")
stats = controller.get_maintenance_stats()

print(f"\nRésultats :")
print(f"  pending_interventions: {stats['pending_interventions']}")
print(f"  monthly_interventions: {stats['monthly_interventions']}")
print(f"  active_contracts: {stats['active_contracts']}")
print(f"  low_stock_parts: {stats['low_stock_parts']}")
print(f"  monthly_revenue: {stats['monthly_revenue']}")

print()
print("[2] Vérification données brutes...")

# Interventions en cours
result = db.fetch_one("SELECT COUNT(*) as count FROM maintenance_intervention WHERE state IN ('scheduled', 'in_progress')")
print(f"  Interventions en cours (DB): {result['count'] if result else 0}")

# Interventions ce mois
result = db.fetch_one("""
    SELECT COUNT(*) as count FROM maintenance_intervention
    WHERE strftime('%Y-%m', date_scheduled) = strftime('%Y-%m', 'now')
""")
print(f"  Interventions ce mois (DB): {result['count'] if result else 0}")

# Contrats actifs
result = db.fetch_one("SELECT COUNT(*) as count FROM maintenance_contract WHERE state = 'active'")
print(f"  Contrats actifs (DB): {result['count'] if result else 0}")

# Pièces stock bas
result = db.fetch_one("SELECT COUNT(*) as count FROM machine_part WHERE quantity <= min_quantity")
print(f"  Pièces stock bas (DB): {result['count'] if result else 0}")

print()
print("[3] Liste des interventions...")
interventions = controller.get_all_interventions()
print(f"  Total interventions: {len(interventions)}")
for inter in interventions:
    print(f"    - #{inter.id}: {inter.name} - État: {inter.state}")

print()
print("[4] Liste des contrats...")
contracts = controller.get_all_contracts()
print(f"  Total contrats: {len(contracts)}")
for contract in contracts:
    print(f"    - {contract.reference}: {contract.partner_name} - État: {contract.state}")

print()
print("[5] Liste des pièces...")
parts = controller.get_all_parts()
print(f"  Total pièces: {len(parts)}")
low_stock = controller.get_low_stock_parts()
print(f"  Pièces en stock bas: {len(low_stock)}")
for part in low_stock:
    print(f"    - {part.name}: Stock {part.quantity}/{part.min_quantity}")

print()
print("=" * 60)
print("  FIN TEST")
print("=" * 60)

db.close()
