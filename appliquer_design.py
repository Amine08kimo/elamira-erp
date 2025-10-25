#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour appliquer le design équilibré
"""

import shutil
import os

print("=" * 60)
print("  APPLICATION DU DESIGN ÉQUILIBRÉ")
print("=" * 60)
print()

# Chemins
source_theme = "core/assets/themes/odoo_theme_balanced.qss"
dest_theme = "core/assets/themes/odoo_theme.qss"

source_dash = "modules/dashboard/views_balanced.py"
dest_dash = "modules/dashboard/views.py"

# Copier thème
if os.path.exists(source_theme):
    shutil.copy(source_theme, dest_theme)
    print("✓ Thème équilibré appliqué")
else:
    print("✗ Fichier thème équilibré introuvable")

# Copier dashboard
if os.path.exists(source_dash):
    shutil.copy(source_dash, dest_dash)
    print("✓ Dashboard équilibré appliqué")
else:
    print("⚠ Fichier dashboard équilibré introuvable")

print()
print("=" * 60)
print("  ✅ DESIGN APPLIQUÉ AVEC SUCCÈS!")
print("=" * 60)
print()
print("Prochaine étape : python main.py")
print()
