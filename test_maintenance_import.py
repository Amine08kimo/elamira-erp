#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test des imports du module Maintenance
"""

print("=" * 60)
print("  TEST IMPORTS MODULE MAINTENANCE")
print("=" * 60)
print()

# Test 1 : Import module
print("[1] Test import MaintenanceModule...")
try:
    from modules.maintenance.maintenance_module import MaintenanceModule
    print("  ✓ MaintenanceModule importé")
except Exception as e:
    print(f"  ✗ Erreur: {e}")
    import traceback
    traceback.print_exc()

print()

# Test 2 : Import controller
print("[2] Test import MaintenanceController...")
try:
    from modules.maintenance.controller import MaintenanceController
    print("  ✓ MaintenanceController importé")
except Exception as e:
    print(f"  ✗ Erreur: {e}")
    import traceback
    traceback.print_exc()

print()

# Test 3 : Import vues
print("[3] Test import vues...")
try:
    from modules.maintenance.views import MaintenanceDashboardView
    print("  ✓ MaintenanceDashboardView importée")
except Exception as e:
    print(f"  ✗ Erreur MaintenanceDashboardView: {e}")
    import traceback
    traceback.print_exc()

try:
    from modules.maintenance.views import MaintenanceInterventionListView
    print("  ✓ MaintenanceInterventionListView importée")
except Exception as e:
    print(f"  ✗ Erreur MaintenanceInterventionListView: {e}")

try:
    from modules.maintenance.views import MaintenanceContractListView
    print("  ✓ MaintenanceContractListView importée")
except Exception as e:
    print(f"  ✗ Erreur MaintenanceContractListView: {e}")

try:
    from modules.maintenance.views import MachinePartListView
    print("  ✓ MachinePartListView importée")
except Exception as e:
    print(f"  ✗ Erreur MachinePartListView: {e}")

print()

# Test 4 : Créer instance
print("[4] Test création instance module...")
try:
    from core.database import DatabaseManager
    
    db = DatabaseManager("database/odoo_clone_dz.db")
    module = MaintenanceModule(db)
    
    print("  ✓ Instance créée")
    
    # Test méthodes
    print(f"  ✓ Nom: {module.get_name()}")
    print(f"  ✓ Icône: {module.get_icon()}")
    
    # Test get_main_view_class
    view_class = module.get_main_view_class()
    print(f"  ✓ get_main_view_class(): {view_class.__name__}")
    
    # Test get_views
    views = module.get_views()
    print(f"  ✓ get_views(): {len(views)} vues")
    for name, cls in views.items():
        print(f"    - {name}: {cls.__name__}")
    
    db.close()
    
except Exception as e:
    print(f"  ✗ Erreur: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 60)
print("  FIN TEST")
print("=" * 60)
