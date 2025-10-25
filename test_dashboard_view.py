#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test création Dashboard Maintenance
"""

import sys
from PyQt6.QtWidgets import QApplication
from core.database import DatabaseManager
from modules.maintenance.maintenance_module import MaintenanceModule
from modules.maintenance.views import MaintenanceDashboardView

print("=" * 60)
print("  TEST DASHBOARD VIEW")
print("=" * 60)
print()

# Créer application Qt
app = QApplication(sys.argv)

# Connexion DB
db = DatabaseManager("database/odoo_clone_dz.db")

# Créer module
module = MaintenanceModule(db)

print("[1] Création Dashboard View...")
try:
    dashboard = MaintenanceDashboardView(module, db)
    print("  ✓ Dashboard créé")
    print(f"  ✓ Visible: {dashboard.isVisible()}")
    print(f"  ✓ Largeur: {dashboard.width()}")
    print(f"  ✓ Hauteur: {dashboard.height()}")
    
    # Afficher brièvement
    dashboard.show()
    print("  ✓ Dashboard affiché")
    
    # Traiter les événements
    app.processEvents()
    
    print("\n  Appuyez sur Ctrl+C pour fermer...")
    sys.exit(app.exec())
    
except Exception as e:
    print(f"  ✗ Erreur: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
