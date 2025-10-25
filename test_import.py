#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test imports"""

try:
    print("Test 1: Import common_styles...")
    from core.ui.common_styles import ElAmiraStyles, ElAmiraDialog
    print("✅ ElAmiraStyles OK")
    
    print("\nTest 2: Import ModernDashboard...")
    from modules.dashboard.modern_dashboard import ModernDashboard
    print("✅ ModernDashboard OK")
    
    print("\nTest 3: Vérifier COLORS...")
    print(f"  Primary: {ElAmiraStyles.COLORS['primary']}")
    print(f"  Success: {ElAmiraStyles.COLORS['success']}")
    
    print("\n🎉 TOUS LES IMPORTS FONCTIONNENT !")
    
except Exception as e:
    print(f"\n❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()
