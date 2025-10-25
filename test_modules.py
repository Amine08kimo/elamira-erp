#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test de chargement des modules
"""

import os
import sys

print("=" * 60)
print("  TEST DES MODULES")
print("=" * 60)
print()

# Vérifier les dossiers de modules
modules_path = "modules"
modules_found = []

if os.path.exists(modules_path):
    for item in os.listdir(modules_path):
        module_dir = os.path.join(modules_path, item)
        if os.path.isdir(module_dir) and not item.startswith('_'):
            init_file = os.path.join(module_dir, '__init__.py')
            if os.path.exists(init_file):
                modules_found.append(item)
                print(f"✓ {item}")
            else:
                print(f"⚠ {item} (pas de __init__.py)")

print()
print(f"Total: {len(modules_found)} modules trouvés")
print()

# Vérifier module Maintenance
if 'maintenance' in modules_found:
    print("✅ Module Maintenance présent!")
    
    # Vérifier fichiers
    maint_files = [
        'modules/maintenance/__init__.py',
        'modules/maintenance/maintenance_module.py',
        'modules/maintenance/models.py',
        'modules/maintenance/controller.py',
        'modules/maintenance/views.py'
    ]
    
    print("\nFichiers Maintenance:")
    for f in maint_files:
        if os.path.exists(f):
            print(f"  ✓ {os.path.basename(f)}")
        else:
            print(f"  ✗ {os.path.basename(f)} MANQUANT")
else:
    print("❌ Module Maintenance MANQUANT!")
    print("\nLe dossier modules/maintenance/ n'existe pas.")
    print("Il faut le créer avec tous les fichiers.")

print()
print("=" * 60)
