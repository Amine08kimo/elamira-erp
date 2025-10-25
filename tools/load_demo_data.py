# -*- coding: utf-8 -*-
"""
Script de Chargement de Données de Démonstration
Crée des clients, produits et factures de test pour l'application ElAmira ERP
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Ajouter le dossier parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import DatabaseManager


class DemoDataLoader:
    """Charge des données de démonstration dans la base de données"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def load_all(self):
        """Charge toutes les données de démo"""
        print("\n" + "="*60)
        print("CHARGEMENT DES DONNÉES DE DÉMONSTRATION")
        print("="*60 + "\n")
        
        self.load_partners()
        self.load_products()
        self.load_sale_orders()
        
        print("\n" + "="*60)
        print("✓ DONNÉES DE DÉMONSTRATION CHARGÉES AVEC SUCCÈS")
        print("="*60 + "\n")
    
    def load_partners(self):
        """Crée des clients et fournisseurs de démo"""
        print("→ Création des partenaires (clients/fournisseurs)...")
        
        partners = [
            # Clients
            {
                'name': 'SARL TECH SOLUTIONS',
                'name_ar': 'شركة تك سوليوشنز',
                'address': '123 Rue Didouche Mourad, Alger Centre',
                'address_ar': '123 شارع ديدوش مراد، الجزائر الوسطى',
                'phone': '023 45 67 89',
                'email': 'contact@techsolutions.dz',
                'nif': '099912345678901',
                'nis': '12345678901234',
                'art': '16/00-1234567B09',
                'is_customer': 1,
                'is_supplier': 0
            },
            {
                'name': 'EURL DIGITAL MARKETING',
                'name_ar': 'شركة التسويق الرقمي',
                'address': '45 Boulevard Zirout Youcef, Oran',
                'address_ar': '45 بوليفار زيروت يوسف، وهران',
                'phone': '041 23 45 67',
                'email': 'info@digitalmarketing.dz',
                'nif': '099923456789012',
                'nis': '23456789012345',
                'art': '31/00-2345678B09',
                'is_customer': 1,
                'is_supplier': 0
            },
            {
                'name': 'SPA INDUSTRIE ALIMENTAIRE',
                'name_ar': 'شركة الصناعات الغذائية',
                'address': '789 Route Nationale, Constantine',
                'address_ar': '789 الطريق الوطني، قسنطينة',
                'phone': '031 98 76 54',
                'email': 'contact@indusalimentaire.dz',
                'nif': '099934567890123',
                'nis': '34567890123456',
                'art': '25/00-3456789B09',
                'is_customer': 1,
                'is_supplier': 0
            },
            # Fournisseurs
            {
                'name': 'DISTRIBUTION MATÉRIEL INFORMATIQUE',
                'name_ar': 'توزيع المعدات الإعلامية',
                'address': '12 Zone Industrielle, Bab Ezzouar',
                'address_ar': '12 المنطقة الصناعية، باب الزوار',
                'phone': '021 55 66 77',
                'email': 'commercial@distmat.dz',
                'nif': '099945678901234',
                'nis': '45678901234567',
                'art': '16/00-4567890B09',
                'is_customer': 0,
                'is_supplier': 1
            },
            {
                'name': 'FOURNITURES BUREAU & PAPETERIE',
                'name_ar': 'مستلزمات المكتب والقرطاسية',
                'address': '56 Rue Larbi Ben Mhidi, Alger',
                'address_ar': '56 شارع العربي بن مهيدي، الجزائر',
                'phone': '023 88 99 00',
                'email': 'vente@fournitures.dz',
                'nif': '099956789012345',
                'nis': '56789012345678',
                'art': '16/00-5678901B09',
                'is_customer': 0,
                'is_supplier': 1
            }
        ]
        
        for partner in partners:
            self.db.execute_query("""
                INSERT OR IGNORE INTO res_partner (
                    name, name_ar, address, address_ar, phone, email,
                    nif, nis, art, is_customer, is_supplier, active
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            """, (
                partner['name'], partner['name_ar'],
                partner['address'], partner['address_ar'],
                partner['phone'], partner['email'],
                partner['nif'], partner['nis'], partner['art'],
                partner['is_customer'], partner['is_supplier']
            ))
        
        count = self.db.fetch_one("SELECT COUNT(*) as count FROM res_partner")
        print(f"  ✓ {count['count']} partenaires créés")
    
    def load_products(self):
        """Crée des produits de démo"""
        print("→ Création des produits...")
        
        products = [
            # Services
            {
                'name': 'Consultation Informatique (1 heure)',
                'name_ar': 'استشارة معلوماتية (ساعة واحدة)',
                'reference': 'SERV-CONS-001',
                'barcode': '',
                'description': 'Consultation technique et conseil en informatique',
                'description_ar': 'استشارة تقنية ومشورة في المعلوماتية',
                'sale_price': 3500.00,
                'cost_price': 0.00,
                'qty_available': 0,
                'tax_id': 1  # TVA 19%
            },
            {
                'name': 'Formation Logiciel ERP (journée)',
                'name_ar': 'تدريب برنامج ERP (يوم)',
                'reference': 'SERV-FORM-001',
                'barcode': '',
                'description': 'Formation complète sur le logiciel de gestion',
                'description_ar': 'تدريب كامل على برنامج الإدارة',
                'sale_price': 25000.00,
                'cost_price': 0.00,
                'qty_available': 0,
                'tax_id': 2  # TVA 9%
            },
            # Produits physiques
            {
                'name': 'Ordinateur Portable Dell Latitude',
                'name_ar': 'حاسوب محمول ديل لاتيتيود',
                'reference': 'PC-DELL-LAT-001',
                'barcode': '5397184439920',
                'description': 'i5, 8GB RAM, 256GB SSD',
                'description_ar': 'معالج i5، ذاكرة 8 جيجا، قرص SSD 256 جيجا',
                'sale_price': 85000.00,
                'cost_price': 68000.00,
                'qty_available': 15,
                'tax_id': 1  # TVA 19%
            },
            {
                'name': 'Imprimante HP LaserJet Pro',
                'name_ar': 'طابعة HP ليزر جيت برو',
                'reference': 'IMP-HP-LJ-001',
                'barcode': '0886112856816',
                'description': 'Impression laser noir et blanc, réseau',
                'description_ar': 'طباعة ليزر أبيض وأسود، شبكة',
                'sale_price': 32000.00,
                'cost_price': 25000.00,
                'qty_available': 8,
                'tax_id': 1  # TVA 19%
            },
            {
                'name': 'Pack Office 365 Business (1 an)',
                'name_ar': 'حزمة أوفيس 365 بيزنس (سنة)',
                'reference': 'SOFT-OFF-365',
                'barcode': '',
                'description': 'Licence Office 365 Business Standard',
                'description_ar': 'ترخيص أوفيس 365 بيزنس ستاندرد',
                'sale_price': 15000.00,
                'cost_price': 12000.00,
                'qty_available': 50,
                'tax_id': 2  # TVA 9%
            },
            {
                'name': 'Clavier + Souris Sans Fil Logitech',
                'name_ar': 'لوحة مفاتيح وماوس لوجيتك لاسلكي',
                'reference': 'ACC-LOG-KM-001',
                'barcode': '5099206052383',
                'description': 'Kit clavier et souris sans fil',
                'description_ar': 'طقم لوحة مفاتيح وماوس لاسلكي',
                'sale_price': 4500.00,
                'cost_price': 3200.00,
                'qty_available': 25,
                'tax_id': 1  # TVA 19%
            },
            {
                'name': 'Disque Dur Externe 1TB',
                'name_ar': 'قرص صلب خارجي 1 تيرابايت',
                'reference': 'STOCK-HDD-1TB',
                'barcode': '0718037855967',
                'description': 'Disque dur externe portable USB 3.0',
                'description_ar': 'قرص صلب خارجي محمول USB 3.0',
                'sale_price': 8500.00,
                'cost_price': 6800.00,
                'qty_available': 30,
                'tax_id': 1  # TVA 19%
            },
            {
                'name': 'Écran Dell 24 pouces Full HD',
                'name_ar': 'شاشة ديل 24 بوصة Full HD',
                'reference': 'MON-DELL-24-001',
                'barcode': '5397063966448',
                'description': 'Écran LED 24", résolution 1920x1080',
                'description_ar': 'شاشة LED 24"، دقة 1920x1080',
                'sale_price': 28000.00,
                'cost_price': 22000.00,
                'qty_available': 12,
                'tax_id': 1  # TVA 19%
            }
        ]
        
        for product in products:
            self.db.execute_query("""
                INSERT OR IGNORE INTO product_product (
                    name, name_ar, reference, barcode, description, description_ar,
                    sale_price, cost_price, qty_available, tax_id, active
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            """, (
                product['name'], product['name_ar'],
                product['reference'], product['barcode'],
                product['description'], product['description_ar'],
                product['sale_price'], product['cost_price'],
                product['qty_available'], product['tax_id']
            ))
        
        count = self.db.fetch_one("SELECT COUNT(*) as count FROM product_product")
        print(f"  ✓ {count['count']} produits créés")
    
    def load_sale_orders(self):
        """Crée des factures de vente de démo"""
        print("→ Création des factures de vente...")
        
        # Récupérer les clients
        customers = self.db.fetch_all(
            "SELECT id FROM res_partner WHERE is_customer = 1 LIMIT 3"
        )
        
        # Récupérer les produits
        products = self.db.fetch_all(
            "SELECT id, sale_price FROM product_product LIMIT 8"
        )
        
        if not customers or not products:
            print("  ⚠ Pas assez de données pour créer des factures")
            return
        
        # Créer 10 factures sur les 3 derniers mois
        base_date = datetime.now()
        
        for i in range(10):
            # Date aléatoire dans les 90 derniers jours
            days_ago = random.randint(0, 90)
            order_date = base_date - timedelta(days=days_ago)
            due_date = order_date + timedelta(days=30)
            
            # Client aléatoire
            customer = random.choice(customers)
            
            # Statut aléatoire
            states = ['draft', 'confirmed', 'done']
            weights = [0.2, 0.3, 0.5]  # Plus de "done"
            state = random.choices(states, weights=weights)[0]
            
            # Numéro de facture
            invoice_number = self.db.get_next_sequence('sale.order')
            
            # Calcul des montants
            num_lines = random.randint(1, 4)
            selected_products = random.sample(products, min(num_lines, len(products)))
            
            amount_untaxed = 0
            amount_tax = 0
            
            lines_data = []
            for product in selected_products:
                quantity = random.randint(1, 5)
                price_unit = product['sale_price']
                tax_rate = 19.0  # Simplification
                
                subtotal = quantity * price_unit
                tax_amount = subtotal * (tax_rate / 100)
                
                amount_untaxed += subtotal
                amount_tax += tax_amount
                
                lines_data.append({
                    'product_id': product['id'],
                    'quantity': quantity,
                    'price_unit': price_unit,
                    'tax_rate': tax_rate,
                    'subtotal': subtotal,
                    'tax_amount': tax_amount
                })
            
            amount_total = amount_untaxed + amount_tax
            
            # Créer la commande
            cursor = self.db.execute_query("""
                INSERT INTO sale_order (
                    name, partner_id, date_order, date_due, state,
                    amount_untaxed, amount_tax, amount_tap, amount_stamp, amount_total,
                    notes, payment_term
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                invoice_number, customer['id'],
                order_date.isoformat(), due_date.isoformat(),
                state,
                amount_untaxed, amount_tax, 0, 0, amount_total,
                'Facture de démonstration', 'Net 30 jours'
            ))
            
            order_id = cursor.lastrowid
            
            # Créer les lignes
            for line_data in lines_data:
                self.db.execute_query("""
                    INSERT INTO sale_order_line (
                        order_id, product_id, product_name, quantity, price_unit,
                        tax_rate, subtotal, tax_amount, total
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    order_id, line_data['product_id'], 'Produit',
                    line_data['quantity'], line_data['price_unit'],
                    line_data['tax_rate'], line_data['subtotal'],
                    line_data['tax_amount'],
                    line_data['subtotal'] + line_data['tax_amount']
                ))
        
        count = self.db.fetch_one("SELECT COUNT(*) as count FROM sale_order")
        print(f"  ✓ {count['count']} factures créées")


def main():
    """Fonction principale"""
    # Connexion à la base de données
    db_path = os.path.join('database', 'odoo_clone_dz.db')
    db_manager = DatabaseManager(db_path)
    
    # Charger les données
    loader = DemoDataLoader(db_manager)
    
    try:
        loader.load_all()
        print("\n✓ Redémarrez l'application pour voir les données")
    except Exception as e:
        print(f"\n✗ Erreur: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db_manager.close()


if __name__ == '__main__':
    main()
