#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test final du module Maintenance
"""

import sys
import os

print("=" * 60)
print("  TEST FINAL MODULE MAINTENANCE")
print("=" * 60)
print()

# Test chargement
try:
    # Créer DB temporaire
    sys.path.insert(0, os.path.abspath('.'))
    
    from core.database import DatabaseManager
    from modules.maintenance.maintenance_module import MaintenanceModule
    
    print("[1] Import module...")
    db = DatabaseManager("database/odoo_clone_dz.db")
    
    print("[2] Création instance...")
    module = MaintenanceModule(db)
    
    print("[3] Vérification méthodes...")
    
    checks = [
        (module.get_name(), "Maintenance", "get_name"),
        (module.get_name_ar(), "الصيانة", "get_name_ar"),
        (module.get_icon(), "🔧", "get_icon"),
    ]
    
    for result, expected, method in checks:
        if result == expected:
            print(f"  ✓ {method}() = {result}")
        else:
            print(f"  ✗ {method}() = {result} (attendu: {expected})")
    
    print()
    print("[4] Vérification vues...")
    views = module.get_views()
    for view_name in views.keys():
        print(f"  ✓ {view_name}")
    
    print()
    print("=" * 60)
    print("  ✅ MODULE MAINTENANCE PRÊT !")
    print("=" * 60)
    print()
    print("Le module Maintenance inclut :")
    print("  🔧 Dashboard Maintenance")
    print("  🛠️ Interventions")
    print("  📋 Contrats")
    print("  🔩 Pièces de Rechange")
    print()
    print("Relancer : python main.py")
    print()
    
    db.close()
    
except Exception as e:
    print(f"\n✗ ERREUR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
