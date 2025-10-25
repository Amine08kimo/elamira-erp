#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Ajoute des données de test dans la base de données"""

from core.database import DatabaseManager
from datetime import datetime, timedelta
import random

db = DatabaseManager("elamira.db")

print("=" * 60)
print("AJOUT DONNÉES DE TEST")
print("=" * 60)

# 1. Clients
print("\n1. Ajout clients...")
clients = [
    ("Atelier de Couture El Baraka", "ورشة الخياطة البركة", "0551234567", "15 Rue Didouche Mourad, Alger"),
    ("Confection Moderne Sarl", "مصنع الخياطة الحديثة", "0661234568", "Zone Industrielle, Rouiba"),
    ("Boutique Rym", "محل ريم", "0771234569", "Centre Ville, Oran"),
    ("Usine Textile Constantine", "مصنع النسيج قسنطينة", "0551234570", "Route Nationale 3, Constantine"),
    ("Couture Express", "خياطة سريعة", "0661234571", "Hai Essalem, Annaba"),
]

for name, name_ar, phone, address in clients:
    db.execute_query("""
        INSERT INTO res_partner (name, name_ar, phone, address, customer, supplier)
        VALUES (?, ?, ?, ?, 1, 0)
    """, (name, name_ar, phone, address))
print(f"✅ {len(clients)} clients ajoutés")

# 2. Produits (Machines à coudre)
print("\n2. Ajout produits...")
produits = [
    ("JUKI DDL-8700", "جوكي DDL-8700", "JUKI-001", 45000, 35000, 3, 5),
    ("JACK JK-58420", "جاك JK-58420", "JACK-001", 42000, 32000, 2, 5),
    ("BROTHER S-7300A", "براذر S-7300A", "BROTHER-001", 55000, 42000, 4, 5),
    ("SINGER 20U", "سينجر 20U", "SINGER-001", 38000, 28000, 5, 5),
    ("SIRUBA L818F", "سيروبا L818F", "SIRUBA-001", 48000, 38000, 1, 5),
    ("Fil Polyester Rouge", "خيط بوليستر أحمر", "FIL-R-001", 450, 300, 8, 10),
    ("Aiguilles JUKI Taille 14", "إبر جوكي مقاس 14", "AIGUILLE-14", 1200, 800, 15, 20),
    ("Bobines Canette Métal", "بكرات معدنية", "BOB-001", 800, 500, 25, 15),
]

for name, name_ar, code, list_price, standard_price, qty, min_stock in produits:
    db.execute_query("""
        INSERT INTO product_product (name, name_ar, code, list_price, standard_price, qty_available, minimum_stock, active)
        VALUES (?, ?, ?, ?, ?, ?, ?, 1)
    """, (name, name_ar, code, list_price, standard_price, qty, min_stock))
print(f"✅ {len(produits)} produits ajoutés")

# 3. Factures
print("\n3. Ajout factures...")
partners = db.execute_query("SELECT id, name FROM res_partner WHERE customer = 1")
factures_data = []

for i in range(15):
    partner = random.choice(partners)
    date_invoice = datetime.now() - timedelta(days=random.randint(1, 90))
    states = ['draft', 'open', 'paid', 'paid', 'paid']  # Plus de factures payées
    state = random.choice(states)
    
    amount_untaxed = random.randint(30000, 200000)
    amount_tax = amount_untaxed * 0.19
    amount_total = amount_untaxed + amount_tax
    
    name = f"INV/2025/{str(i+1).zfill(4)}"
    
    db.execute_query("""
        INSERT INTO account_invoice (
            name, partner_id, partner_name, date_invoice, state,
            amount_untaxed, amount_tax, amount_total
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, partner['id'], partner['name'], date_invoice, state, 
          amount_untaxed, amount_tax, amount_total))
    
    factures_data.append((name, state, amount_total))

print(f"✅ {len(factures_data)} factures ajoutées")

# 4. Maintenances
print("\n4. Ajout maintenances...")
machines = db.execute_query("SELECT id, name FROM product_product WHERE code LIKE 'J%' OR code LIKE 'BROTHER%' OR code LIKE 'SINGER%'")

for i in range(8):
    machine = random.choice(machines) if machines else {'id': 1, 'name': 'Machine Test'}
    partner = random.choice(partners)
    
    date_scheduled = datetime.now() + timedelta(days=random.randint(1, 30))
    states = ['draft', 'scheduled', 'scheduled', 'in_progress']  # Plus de maintenances planifiées
    state = random.choice(states)
    
    name = f"MAINT-2025-{str(i+1).zfill(3)}"
    types = ['preventive', 'corrective']
    intervention_type = random.choice(types)
    
    db.execute_query("""
        INSERT INTO maintenance_intervention (
            name, machine_id, machine_name, partner_id, partner_name,
            date_scheduled, state, intervention_type, description
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, machine['id'], machine['name'], partner['id'], partner['name'],
          date_scheduled, state, intervention_type, 
          f"Maintenance {intervention_type} de {machine['name']}"))

print(f"✅ 8 maintenances ajoutées")

# 5. Statistiques finales
print("\n" + "=" * 60)
print("STATISTIQUES")
print("=" * 60)

stats = {
    "Clients": db.execute_query("SELECT COUNT(*) as count FROM res_partner WHERE customer = 1")[0]['count'],
    "Produits": db.execute_query("SELECT COUNT(*) as count FROM product_product")[0]['count'],
    "Factures": db.execute_query("SELECT COUNT(*) as count FROM account_invoice")[0]['count'],
    "Maintenances": db.execute_query("SELECT COUNT(*) as count FROM maintenance_intervention")[0]['count'],
}

for key, value in stats.items():
    print(f"  {key}: {value}")

# CA Total
ca = db.execute_query("SELECT SUM(amount_total) as total FROM account_invoice WHERE state = 'paid'")[0]['total'] or 0
print(f"  CA Total: {ca:,.2f} DA")

# Stock bas
stock_low = db.execute_query("SELECT COUNT(*) as count FROM product_product WHERE qty_available < minimum_stock")[0]['count']
print(f"  Produits stock bas: {stock_low}")

# Factures impayées
unpaid = db.execute_query("SELECT COUNT(*) as count FROM account_invoice WHERE state = 'open'")[0]['count']
print(f"  Factures impayées: {unpaid}")

print("\n✅ DONNÉES DE TEST AJOUTÉES AVEC SUCCÈS !")
print("\nRelancez l'application pour voir les données dans le dashboard.")
