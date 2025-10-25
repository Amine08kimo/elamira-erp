#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Diagnostic complet de l'application"""

import sys
import os

print("=" * 60)
print("DIAGNOSTIC ELAMIRA ERP")
print("=" * 60)

# Test 1: Imports de base
print("\n1. Tests imports de base...")
try:
    from PyQt6.QtWidgets import QApplication, QWidget
    print("   ✓ PyQt6 OK")
except Exception as e:
    print(f"   ✗ PyQt6 ERROR: {e}")
    sys.exit(1)

# Test 2: Import DB
print("\n2. Test Database Manager...")
try:
    from core.database import DatabaseManager
    print("   ✓ DatabaseManager OK")
except Exception as e:
    print(f"   ✗ DatabaseManager ERROR: {e}")
    sys.exit(1)

# Test 3: Common Styles
print("\n3. Test Common Styles...")
try:
    from core.ui.common_styles import ElAmiraStyles, ElAmiraDialog
    print("   ✓ ElAmiraStyles OK")
    print(f"   - Primary color: {ElAmiraStyles.COLORS['primary']}")
except Exception as e:
    print(f"   ✗ ElAmiraStyles ERROR: {e}")
    import traceback
    traceback.print_exc()

# Test 4: ModernDashboard
print("\n4. Test ModernDashboard...")
try:
    from modules.dashboard.modern_dashboard import ModernDashboard
    print("   ✓ ModernDashboard import OK")
except Exception as e:
    print(f"   ✗ ModernDashboard ERROR: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Dashboard Module
print("\n5. Test Dashboard Module...")
try:
    from modules.dashboard.dashboard_module import DashboardModule
    print("   ✓ DashboardModule import OK")
    
    # Test instanciation
    db = DatabaseManager("elamira.db")
    module = DashboardModule(db)
    print("   ✓ DashboardModule instanciation OK")
    
    # Test get_main_view_class
    view_class = module.get_main_view_class()
    print(f"   ✓ Vue principale: {view_class.__name__}")
    
except Exception as e:
    print(f"   ✗ DashboardModule ERROR: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Création vue dashboard
print("\n6. Test création vue dashboard...")
try:
    app = QApplication([])
    db = DatabaseManager("elamira.db")
    module = DashboardModule(db)
    view_class = module.get_main_view_class()
    
    # Tenter de créer la vue
    view = view_class(module, db)
    print("   ✓ Vue dashboard créée avec succès!")
    print(f"   - Type: {type(view).__name__}")
    
except Exception as e:
    print(f"   ✗ Création vue ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("DIAGNOSTIC TERMINE")
print("=" * 60)
