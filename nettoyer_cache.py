#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nettoyage du cache Python
"""

import os
import shutil

print("=" * 60)
print("  NETTOYAGE CACHE PYTHON")
print("=" * 60)
print()

count = 0

# Parcourir tous les dossiers
for root, dirs, files in os.walk('.'):
    # Supprimer __pycache__
    if '__pycache__' in dirs:
        pycache_path = os.path.join(root, '__pycache__')
        try:
            shutil.rmtree(pycache_path)
            print(f"✓ Supprimé: {pycache_path}")
            count += 1
        except Exception as e:
            print(f"✗ Erreur: {pycache_path} - {e}")
    
    # Supprimer fichiers .pyc
    for file in files:
        if file.endswith('.pyc'):
            pyc_path = os.path.join(root, file)
            try:
                os.remove(pyc_path)
                print(f"✓ Supprimé: {pyc_path}")
                count += 1
            except Exception as e:
                print(f"✗ Erreur: {pyc_path} - {e}")

print()
print("=" * 60)
print(f"  ✅ {count} fichiers/dossiers supprimés")
print("=" * 60)
print()
print("Vous pouvez maintenant relancer : python main.py")
print()
