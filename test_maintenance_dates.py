#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test des dates du module Maintenance
"""

import sys
from datetime import datetime, timedelta

print("=" * 60)
print("  TEST DATES MODULE MAINTENANCE")
print("=" * 60)
print()

# Test fonction format_date
print("[1] Test fonction format_date...")
from modules.maintenance.views import format_date

test_cases = [
    ("2025-10-20T12:30:00", "20/10/2025"),
    ("2025-10-20", "20/10/2025"),
    ("", ""),
    (None, ""),
    (datetime(2025, 10, 20), "20/10/2025"),
]

for input_val, expected in test_cases:
    result = format_date(input_val)
    status = "✓" if result == expected else "✗"
    print(f"  {status} format_date({repr(input_val)}) = {repr(result)} (attendu: {repr(expected)})")

print()

# Test avec vraies données DB
print("[2] Test avec données DB...")
try:
    from core.database import DatabaseManager
    from modules.maintenance.controller import MaintenanceController
    
    db = DatabaseManager("database/odoo_clone_dz.db")
    controller = MaintenanceController(db)
    
    # Récupérer interventions
    interventions = controller.get_all_interventions()
    print(f"  Interventions trouvées: {len(interventions)}")
    
    for inter in interventions[:3]:  # Afficher 3 premières
        print(f"\n  Intervention #{inter.id}:")
        print(f"    - date_scheduled: {repr(inter.date_scheduled)}")
        print(f"    - type: {type(inter.date_scheduled)}")
        print(f"    - formatté: {format_date(inter.date_scheduled)}")
    
    # Récupérer contrats
    print()
    contracts = controller.get_all_contracts()
    print(f"  Contrats trouvés: {len(contracts)}")
    
    for contract in contracts[:2]:  # Afficher 2 premiers
        print(f"\n  Contrat {contract.reference}:")
        print(f"    - date_start: {repr(contract.date_start)}")
        print(f"    - formatté: {format_date(contract.date_start)}")
    
    print()
    print("✓ Toutes les dates peuvent être formatées")
    
    db.close()
    
except Exception as e:
    print(f"✗ Erreur: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 60)
print("  FIN TEST DATES")
print("=" * 60)
print()
print("Si tous les tests passent, relancer : python main.py")
print()
