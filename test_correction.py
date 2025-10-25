#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test des corrections
"""

print("=" * 60)
print("  TEST DES CORRECTIONS")
print("=" * 60)
print()

# Test 1: Module Maintenance
print("[1] Test module Maintenance...")
try:
    from modules.maintenance.maintenance_module import MaintenanceModule
    from core.database import DatabaseManager
    
    db = DatabaseManager(":memory:")
    module = MaintenanceModule(db)
    
    # Vérifier toutes les méthodes
    assert hasattr(module, 'get_name'), "get_name manquante"
    assert hasattr(module, 'get_name_ar'), "get_name_ar manquante"
    assert hasattr(module, 'get_icon'), "get_icon manquante"
    assert hasattr(module, 'get_main_view_class'), "get_main_view_class manquante"
    assert hasattr(module, 'get_action_menu'), "get_action_menu manquante"
    
    assert module.get_name() == "Maintenance"
    assert module.get_icon() == "🔧"
    
    print("  ✓ Module Maintenance OK")
    
except Exception as e:
    print(f"  ✗ Erreur: {e}")

print()

# Test 2: Thème CSS
print("[2] Test thème CSS...")
import os
theme_path = "core/assets/themes/odoo_theme.qss"

if os.path.exists(theme_path):
    with open(theme_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Vérifier corrections
    checks = [
        ("QWidget#sidebar" in content, "Style sidebar"),
        ("QWidget#header" in content, "Style header"),
        ("QStackedWidget" in content, "Style QStackedWidget"),
        ("background-color: #F5F5F5" in content, "Fond gris clair"),
    ]
    
    for check, desc in checks:
        if check:
            print(f"  ✓ {desc}")
        else:
            print(f"  ✗ {desc} manquant")
else:
    print("  ✗ Fichier thème introuvable")

print()
print("=" * 60)
print("  ✅ TESTS TERMINÉS")
print("=" * 60)
print()
print("Relancer : python main.py")
print()
