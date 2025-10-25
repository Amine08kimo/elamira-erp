# -*- coding: utf-8 -*-
"""
Script de Chargement de Données Démo - Machines à Coudre
Génère des données réalistes pour vente et maintenance de machines à coudre
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import DatabaseManager
from datetime import datetime, timedelta
import random


def load_sewing_machines_demo():
    """Charge les données de démonstration pour machines à coudre"""
    
    db_path = os.path.join('database', 'odoo_clone_dz.db')
    db = DatabaseManager(db_path)
    
    print("\n" + "="*70)
    print("CHARGEMENT DONNÉES DÉMO - MACHINES À COUDRE")
    print("="*70 + "\n")
    
    # 1. Clients spécialisés machines à coudre
    print("→ Création des clients...")
    clients = [
        {
            'name': 'ATELIER DE COUTURE MODERNE',
            'name_ar': 'ورشة الخياطة العصرية',
            'address': '15 Rue Larbi Ben M\'hidi, Alger Centre',
            'phone': '023 45 12 34',
            'email': 'contact@couture-moderne.dz',
            'nif': '099912345670001',
            'nis': '12345670000001',
            'art': '16/00-1234501B09'
        },
        {
            'name': 'USINE TEXTILE SETIF',
            'name_ar': 'مصنع المنسوجات سطيف',
            'address': 'Zone Industrielle Ain El Kebira, Sétif',
            'phone': '036 78 90 12',
            'email': 'production@textile-setif.dz',
            'nif': '099912345670002',
            'nis': '12345670000002',
            'art': '19/00-1234502B09'
        },
        {
            'name': 'CONFECTION EL BARAKA',
            'name_ar': 'خياطة البركة',
            'address': '89 Boulevard Mohamed V, Oran',
            'phone': '041 23 45 67',
            'email': 'info@elbaraka-confection.dz',
            'nif': '099912345670003',
            'nis': '12345670000003',
            'art': '31/00-1234503B09'
        },
        {
            'name': 'MAISON DE HAUTE COUTURE',
            'name_ar': 'دار الأزياء الراقية',
            'address': '12 Rue Didouche Mourad, Alger',
            'phone': '023 67 89 01',
            'email': 'contact@haute-couture.dz',
            'nif': '099912345670004',
            'nis': '12345670000004',
            'art': '16/00-1234504B09'
        },
        {
            'name': 'ÉCOLE DE FORMATION PROFESSIONNELLE',
            'name_ar': 'مدرسة التكوين المهني',
            'address': 'Cité 1000 Logements, Constantine',
            'phone': '031 45 67 89',
            'email': 'formation@cfpa-constantine.dz',
            'nif': '099912345670005',
            'nis': '12345670000005',
            'art': '25/00-1234505B09'
        }
    ]
    
    for client in clients:
        db.execute_query("""
            INSERT OR IGNORE INTO res_partner (
                name, name_ar, address, phone, email,
                nif, nis, art, is_customer, is_supplier, active
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, 0, 1)
        """, (
            client['name'], client['name_ar'], client['address'],
            client['phone'], client['email'],
            client['nif'], client['nis'], client['art']
        ))
    
    print(f"  ✓ {len(clients)} clients créés")
    
    # 2. Machines à coudre professionnelles
    print("\n→ Création des machines à coudre...")
    
    machines = [
        {
            'name': 'Machine à Coudre Industrielle JUKI DDL-8700',
            'name_ar': 'آلة الخياطة الصناعية جوكي DDL-8700',
            'ref': 'MAC-JUKI-8700',
            'description': 'Machine piqueuse plate industrielle à grande vitesse. Moteur direct drive, coupe-fil automatique. Idéale pour couture de vêtements, jeans, cuir léger.',
            'category': 'Machine Industrielle',
            'sale_price': 185000.00,
            'cost_price': 145000.00,
            'qty': 12,
            'tax_rate': 19.0,
            'image_url': 'images/juki-ddl-8700.jpg'
        },
        {
            'name': 'Machine à Coudre BROTHER S-7300A Piqueuse Plate',
            'name_ar': 'آلة الخياطة براذر S-7300A',
            'ref': 'MAC-BROTHER-S7300',
            'description': 'Piqueuse plate électronique avec écran tactile. 7000 points/min, coupe-fil, releveur de pied automatique. Parfaite pour production textile.',
            'category': 'Machine Industrielle',
            'sale_price': 295000.00,
            'cost_price': 235000.00,
            'qty': 8,
            'tax_rate': 19.0,
            'image_url': 'images/brother-s7300a.jpg'
        },
        {
            'name': 'Surjeteuse 4 Fils PEGASUS M732',
            'name_ar': 'آلة الأوفرلوك بيجاسوس M732',
            'ref': 'MAC-PEGASUS-M732',
            'description': 'Surjeteuse industrielle 4 fils. Couture extensible, finition parfaite. Vitesse 7000 pts/min. Pour jersey, tricot, tissus élastiques.',
            'category': 'Surjeteuse',
            'sale_price': 165000.00,
            'cost_price': 128000.00,
            'qty': 15,
            'tax_rate': 19.0,
            'image_url': 'images/pegasus-m732.jpg'
        },
        {
            'name': 'Machine Point Invisible SUNSTAR KM-250AK',
            'name_ar': 'آلة الغرزة الخفية صن ستار KM-250AK',
            'ref': 'MAC-SUNSTAR-250',
            'description': 'Point invisible ourlet pantalon, jupe, robe. Semi-automatique, réglage facile. Rendu professionnel invisible.',
            'category': 'Machine Spéciale',
            'sale_price': 125000.00,
            'cost_price': 98000.00,
            'qty': 10,
            'tax_rate': 19.0,
            'image_url': 'images/sunstar-km250.jpg'
        },
        {
            'name': 'Machine Boutonnière BROTHER BH-790',
            'name_ar': 'آلة عمل الأزرار براذر BH-790',
            'ref': 'MAC-BROTHER-BH790',
            'description': 'Boutonnière automatique électronique. Programme multi-tailles (10-40mm). Production rapide chemises, vestes, pantalons.',
            'category': 'Machine Spéciale',
            'sale_price': 215000.00,
            'cost_price': 168000.00,
            'qty': 6,
            'tax_rate': 19.0,
            'image_url': 'images/brother-bh790.jpg'
        },
        {
            'name': 'Machine Triple Entraînement JUKI DU-1181N',
            'name_ar': 'آلة الجر الثلاثي جوكي DU-1181N',
            'ref': 'MAC-JUKI-1181',
            'description': 'Triple entraînement pour cuir, vinyle, skaï. Puissante, précise. Sellerie, maroquinerie, ameublement.',
            'category': 'Machine Industrielle',
            'sale_price': 275000.00,
            'cost_price': 215000.00,
            'qty': 5,
            'tax_rate': 19.0,
            'image_url': 'images/juki-du1181.jpg'
        },
        {
            'name': 'Recouvreuse 3 Aiguilles KANSAI DFB-1412P',
            'name_ar': 'آلة الفلاتلوك كانساي DFB-1412P',
            'ref': 'MAC-KANSAI-1412',
            'description': 'Recouvreuse plate 3 aiguilles. Finition col T-shirt, bord manche. Vitesse 6500 pts/min. Qualité professionnelle.',
            'category': 'Recouvreuse',
            'sale_price': 195000.00,
            'cost_price': 152000.00,
            'qty': 9,
            'tax_rate': 19.0,
            'image_url': 'images/kansai-dfb1412.jpg'
        },
        {
            'name': 'Machine Point Noué BROTHER KE-430F',
            'name_ar': 'آلة نقطة الربط براذر KE-430F',
            'ref': 'MAC-BROTHER-KE430',
            'description': 'Point de consolidation automatique. Fixation boutonnière, poche, passant. Programmable, rapide.',
            'category': 'Machine Spéciale',
            'sale_price': 245000.00,
            'cost_price': 192000.00,
            'qty': 7,
            'tax_rate': 19.0,
            'image_url': 'images/brother-ke430.jpg'
        },
        {
            'name': 'Machine Familiale Électronique SINGER Quantum 9960',
            'name_ar': 'آلة الخياطة المنزلية سينجر 9960',
            'ref': 'MAC-SINGER-9960',
            'description': 'Machine électronique 600 points. Écran LCD, enfilage automatique. Idéale particuliers, retouches, créations.',
            'category': 'Machine Familiale',
            'sale_price': 45000.00,
            'cost_price': 32000.00,
            'qty': 25,
            'tax_rate': 19.0,
            'image_url': 'images/singer-9960.jpg'
        },
        {
            'name': 'Machine Familiale JANOME Memory Craft 6700P',
            'name_ar': 'آلة الخياطة جانومي 6700P',
            'ref': 'MAC-JANOME-6700',
            'description': 'Machine électronique 165 points, broderie. Mémoire motifs, USB. Pour créateurs, retoucheurs.',
            'category': 'Machine Familiale',
            'sale_price': 85000.00,
            'cost_price': 62000.00,
            'qty': 18,
            'tax_rate': 19.0,
            'image_url': 'images/janome-6700.jpg'
        },
        {
            'name': 'Table de Coupe Professionnelle GERBER 180cm',
            'name_ar': 'طاولة القطع المهنية جيربر 180سم',
            'ref': 'ACC-TABLE-180',
            'description': 'Table de coupe professionnelle 180x90cm. Surface auto-cicatrisante, règle graduée. Indispensable atelier.',
            'category': 'Accessoire',
            'sale_price': 35000.00,
            'cost_price': 22000.00,
            'qty': 30,
            'tax_rate': 19.0,
            'image_url': 'images/table-coupe.jpg'
        },
        {
            'name': 'Fer à Repasser Professionnel ROTONDI 2.5L',
            'name_ar': 'مكواة احترافية روتوندي 2.5 لتر',
            'ref': 'ACC-FER-ROTONDI',
            'description': 'Fer vapeur industriel 2.5L, pompe intégrée. Semelle inox, réglage température. Finition professionnelle.',
            'category': 'Accessoire',
            'sale_price': 28000.00,
            'cost_price': 18000.00,
            'qty': 20,
            'tax_rate': 19.0,
            'image_url': 'images/fer-rotondi.jpg'
        }
    ]
    
    for machine in machines:
        db.execute_query("""
            INSERT OR IGNORE INTO product_product (
                name, name_ar, ref, description, category,
                sale_price, cost_price, qty_available,
                tax_rate, image_url, type, active
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'product', 1)
        """, (
            machine['name'], machine['name_ar'], machine['ref'],
            machine['description'], machine['category'],
            machine['sale_price'], machine['cost_price'], machine['qty'],
            machine['tax_rate'], machine['image_url']
        ))
    
    print(f"  ✓ {len(machines)} machines à coudre créées")
    
    # 3. Services de maintenance
    print("\n→ Création des services...")
    
    services = [
        {
            'name': 'Maintenance Préventive Machine Industrielle',
            'name_ar': 'صيانة وقائية للآلة الصناعية',
            'ref': 'SRV-MAINT-IND',
            'description': 'Révision complète: nettoyage, graissage, réglages tensions, synchronisation. Garantie 3 mois.',
            'category': 'Service Maintenance',
            'sale_price': 8500.00,
            'cost_price': 4500.00,
            'tax_rate': 19.0,
        },
        {
            'name': 'Réparation Carte Électronique',
            'name_ar': 'إصلاح اللوحة الإلكترونية',
            'ref': 'SRV-REPARE-ELEC',
            'description': 'Diagnostic et réparation carte électronique, écran tactile. Pièces d\'origine. Délai 48-72h.',
            'category': 'Service Réparation',
            'sale_price': 15000.00,
            'cost_price': 8000.00,
            'tax_rate': 19.0,
        },
        {
            'name': 'Remplacement Courroie & Moteur',
            'name_ar': 'استبدال الحزام والمحرك',
            'ref': 'SRV-MOTEUR',
            'description': 'Changement courroie, moteur, poulies. Test complet. Pièces neuves garanties.',
            'category': 'Service Réparation',
            'sale_price': 12000.00,
            'cost_price': 6500.00,
            'tax_rate': 19.0,
        },
        {
            'name': 'Formation Utilisation Machine Industrielle',
            'name_ar': 'تدريب على استخدام الآلة الصناعية',
            'ref': 'SRV-FORMATION',
            'description': 'Formation 2 jours: utilisation, entretien, dépannage de base. Sur site client. Support inclus.',
            'category': 'Service Formation',
            'sale_price': 25000.00,
            'cost_price': 12000.00,
            'tax_rate': 19.0,
        },
        {
            'name': 'Installation & Mise en Service',
            'name_ar': 'التركيب والتشغيل',
            'ref': 'SRV-INSTALL',
            'description': 'Installation complète machine, raccordement, réglages optimaux, formation opérateur.',
            'category': 'Service Installation',
            'sale_price': 6000.00,
            'cost_price': 2500.00,
            'tax_rate': 19.0,
        }
    ]
    
    for service in services:
        db.execute_query("""
            INSERT OR IGNORE INTO product_product (
                name, name_ar, ref, description, category,
                sale_price, cost_price, tax_rate, type, active
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'service', 1)
        """, (
            service['name'], service['name_ar'], service['ref'],
            service['description'], service['category'],
            service['sale_price'], service['cost_price'], service['tax_rate']
        ))
    
    print(f"  ✓ {len(services)} services créés")
    
    # 4. Factures démo
    print("\n→ Création des factures démo...")
    
    # Récupérer IDs
    clients_db = db.fetch_all("SELECT id FROM res_partner WHERE is_customer = 1 ORDER BY id DESC LIMIT 5")
    products_db = db.fetch_all("SELECT id, sale_price, tax_rate FROM product_product WHERE active = 1")
    
    if not clients_db or not products_db:
        print("  ⚠ Pas de clients ou produits pour créer les factures")
        return
    
    # Créer 15 factures réalistes
    today = datetime.now()
    document_types = ['invoice', 'proforma', 'order', 'delivery']
    
    for i in range(15):
        client = random.choice(clients_db)
        doc_type = random.choice(document_types)
        
        # Numérotation selon type
        prefixes = {
            'invoice': 'FAC',
            'proforma': 'PRO',
            'order': 'BC',
            'delivery': 'BL'
        }
        prefix = prefixes[doc_type]
        doc_number = f"{prefix}-{2025}{(i+1):05d}"
        
        date_order = today - timedelta(days=random.randint(0, 90))
        state = random.choice(['draft', 'confirmed', 'done'])
        
        # Créer la facture
        cursor = db.execute_query("""
            INSERT INTO sale_order (
                name, partner_id, document_type, date_order, state,
                amount_untaxed, amount_tax, amount_total
            ) VALUES (?, ?, ?, ?, ?, 0, 0, 0)
        """, (doc_number, client['id'], doc_type, date_order.isoformat(), state))
        
        order_id = cursor.lastrowid
        
        # Ajouter 2-4 lignes
        num_lines = random.randint(2, 4)
        total_ht = 0
        total_tax = 0
        
        for _ in range(num_lines):
            product = random.choice(products_db)
            qty = random.randint(1, 3)
            price = product['sale_price']
            tax_rate = product['tax_rate']
            
            subtotal = qty * price
            tax_amount = subtotal * (tax_rate / 100)
            total = subtotal + tax_amount
            
            total_ht += subtotal
            total_tax += tax_amount
            
            db.execute_query("""
                INSERT INTO sale_order_line (
                    order_id, product_id, quantity, price_unit,
                    tax_rate, subtotal, tax_amount, total
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (order_id, product['id'], qty, price, tax_rate, subtotal, tax_amount, total))
        
        # Mettre à jour les totaux
        total_ttc = total_ht + total_tax
        db.execute_query("""
            UPDATE sale_order
            SET amount_untaxed = ?, amount_tax = ?, amount_total = ?
            WHERE id = ?
        """, (total_ht, total_tax, total_ttc, order_id))
    
    print(f"  ✓ 15 documents créés (Factures, Proforma, BC, BL)")
    
    print("\n" + "="*70)
    print("✓ DONNÉES DÉMO MACHINES À COUDRE CHARGÉES AVEC SUCCÈS")
    print("="*70)
    print("\nStatistiques:")
    print(f"  • {len(clients)} clients spécialisés")
    print(f"  • {len(machines)} machines à coudre")
    print(f"  • {len(services)} services maintenance")
    print(f"  • 15 documents de vente")
    print("\n")


if __name__ == '__main__':
    load_sewing_machines_demo()
