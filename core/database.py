# -*- coding: utf-8 -*-
"""
Gestionnaire de Base de Données SQLite - Singleton
Gère toutes les connexions et opérations sur la base de données
Inclut les tables spécifiques au marché algérien (PCN, NIF/NIS/ART, etc.)
"""

import sqlite3
import os
from typing import Any, List, Dict, Optional, Tuple
from datetime import datetime
from pathlib import Path


class DatabaseManager:
    """
    Gestionnaire singleton de la base de données SQLite.
    Assure une connexion unique et thread-safe.
    """
    
    _instance = None
    _connection = None
    _db_path = None
    
    def __new__(cls, db_path: str = None):
        """Implémentation du pattern Singleton"""
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, db_path: str = None):
        """
        Initialise la connexion à la base de données
        
        Args:
            db_path: Chemin vers le fichier de base de données
        """
        if db_path and not self._connection:
            self._db_path = db_path
            self._connect()
            self._initialize_database()
    
    def _connect(self):
        """Établit la connexion à la base de données"""
        try:
            # Créer le dossier si nécessaire
            db_dir = os.path.dirname(self._db_path)
            if db_dir:  # Seulement si un chemin existe
                os.makedirs(db_dir, exist_ok=True)
            
            self._connection = sqlite3.connect(
                self._db_path,
                check_same_thread=False  # Pour utilisation multi-thread
            )
            self._connection.row_factory = sqlite3.Row  # Retourner des dictionnaires
            print(f"✓ Connexion établie à la base de données: {self._db_path}")
        except Exception as e:
            print(f"✗ Erreur de connexion à la base de données: {e}")
            raise
    
    def _initialize_database(self):
        """
        Crée toutes les tables de base nécessaires au système.
        Inclut les spécificités algériennes (PCN, taxes DZ, etc.)
        """
        
        # Table des utilisateurs
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS res_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT,
                is_admin BOOLEAN DEFAULT 0,
                active BOOLEAN DEFAULT 1,
                lang TEXT DEFAULT 'fr_FR',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table de la société (informations fiscales DZ)
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS res_company (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                name_ar TEXT,
                address TEXT,
                address_ar TEXT,
                phone TEXT,
                email TEXT,
                nif TEXT,  -- Numéro d'Identification Fiscale (DZ)
                nis TEXT,  -- Numéro d'Identification Statistique (DZ)
                art TEXT,  -- Article du Registre du Commerce (DZ)
                logo BLOB,
                currency TEXT DEFAULT 'DA',
                tax_regime TEXT DEFAULT 'normal',  -- normal, simplifié, forfaitaire
                fiscal_year_start TEXT DEFAULT '01-01',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table des modules installés
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS ir_module_module (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                display_name TEXT NOT NULL,
                state TEXT DEFAULT 'uninstalled',  -- uninstalled, installed, to_upgrade
                version TEXT,
                author TEXT,
                icon_path TEXT,
                installed_at TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table du Plan Comptable National (PCN) Algérien
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS pcn_account (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                name_fr TEXT NOT NULL,
                name_ar TEXT,
                account_type TEXT NOT NULL,  -- Actif, Passif, Capitaux, Charges, Produits
                parent_id INTEGER,
                level INTEGER DEFAULT 1,
                is_view BOOLEAN DEFAULT 0,  -- Compte de regroupement
                active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (parent_id) REFERENCES pcn_account (id)
            )
        """)
        
        # Table des taxes (TVA, TAP, etc.) - Conformité DZ
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS account_tax (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                name_ar TEXT,
                tax_type TEXT NOT NULL,  -- tva, tap, timbre
                rate REAL NOT NULL,  -- Taux en pourcentage (ex: 19.0 pour 19%)
                amount REAL DEFAULT 0,  -- Montant fixe (pour timbre fiscal)
                scope TEXT DEFAULT 'sale',  -- sale, purchase, both
                pcn_account_id INTEGER,  -- Compte PCN associé
                active BOOLEAN DEFAULT 1,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (pcn_account_id) REFERENCES pcn_account (id)
            )
        """)
        
        # Table des séquences (pour numérotation automatique)
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS ir_sequence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                code TEXT UNIQUE NOT NULL,
                prefix TEXT,
                suffix TEXT,
                padding INTEGER DEFAULT 5,
                next_number INTEGER DEFAULT 1,
                active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table des licences
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS system_license (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                license_key TEXT UNIQUE NOT NULL,
                license_type TEXT NOT NULL,  -- annual, lifetime
                company_name TEXT NOT NULL,
                email TEXT NOT NULL,
                activation_date TIMESTAMP,
                expiry_date TIMESTAMP,
                is_active BOOLEAN DEFAULT 0,
                hardware_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # ===== TABLES MÉTIERS =====
        
        # Table des partenaires (clients/fournisseurs)
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS res_partner (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                name_ar TEXT,
                is_company BOOLEAN DEFAULT 1,
                parent_id INTEGER,
                phone TEXT,
                mobile TEXT,
                email TEXT,
                address TEXT,
                address_ar TEXT,
                city TEXT,
                city_ar TEXT,
                zip_code TEXT,
                country TEXT DEFAULT 'DZ',
                nif TEXT,
                nis TEXT,
                art TEXT,
                customer BOOLEAN DEFAULT 1,
                supplier BOOLEAN DEFAULT 0,
                employee BOOLEAN DEFAULT 0,
                active BOOLEAN DEFAULT 1,
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (parent_id) REFERENCES res_partner (id)
            )
        """)
        
        # Table des produits
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS product_product (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                name_ar TEXT,
                code TEXT UNIQUE,
                barcode TEXT,
                category TEXT DEFAULT 'product',
                product_type TEXT DEFAULT 'product',  -- product, service, consumable
                list_price REAL DEFAULT 0.0,
                standard_price REAL DEFAULT 0.0,
                qty_available INTEGER DEFAULT 0,
                minimum_stock INTEGER DEFAULT 5,
                uom TEXT DEFAULT 'Unit',
                description TEXT,
                description_ar TEXT,
                image_url TEXT,
                active BOOLEAN DEFAULT 1,
                can_be_sold BOOLEAN DEFAULT 1,
                can_be_purchased BOOLEAN DEFAULT 1,
                tax_id INTEGER,
                supplier_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (tax_id) REFERENCES account_tax (id),
                FOREIGN KEY (supplier_id) REFERENCES res_partner (id)
            )
        """)
        
        # Table des factures
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS account_invoice (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                partner_id INTEGER NOT NULL,
                partner_name TEXT,
                date_invoice TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_due TIMESTAMP,
                invoice_type TEXT DEFAULT 'out_invoice',  -- out_invoice, in_invoice
                state TEXT DEFAULT 'draft',  -- draft, open, paid, cancel
                amount_untaxed REAL DEFAULT 0.0,
                amount_tax REAL DEFAULT 0.0,
                amount_total REAL DEFAULT 0.0,
                residual REAL DEFAULT 0.0,
                payment_term TEXT,
                reference TEXT,
                comment TEXT,
                user_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (partner_id) REFERENCES res_partner (id),
                FOREIGN KEY (user_id) REFERENCES res_users (id)
            )
        """)
        
        # Table des lignes de facture
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS account_invoice_line (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id INTEGER NOT NULL,
                product_id INTEGER,
                product_name TEXT NOT NULL,
                description TEXT,
                quantity REAL DEFAULT 1.0,
                uom TEXT DEFAULT 'Unit',
                price_unit REAL DEFAULT 0.0,
                discount REAL DEFAULT 0.0,
                tax_id INTEGER,
                price_subtotal REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (invoice_id) REFERENCES account_invoice (id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES product_product (id),
                FOREIGN KEY (tax_id) REFERENCES account_tax (id)
            )
        """)
        
        # Table des interventions de maintenance
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS maintenance_intervention (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                intervention_type TEXT DEFAULT 'preventive',
                state TEXT DEFAULT 'draft',  -- draft, scheduled, in_progress, done, cancel
                priority TEXT DEFAULT 'normal',
                machine_id INTEGER,
                machine_name TEXT,
                machine_serial TEXT,
                partner_id INTEGER,
                partner_name TEXT,
                partner_phone TEXT,
                date_scheduled TIMESTAMP,
                date_start TIMESTAMP,
                date_end TIMESTAMP,
                date_next TIMESTAMP,
                description TEXT,
                work_done TEXT,
                recommendations TEXT,
                technician_id INTEGER,
                technician_name TEXT,
                parts_used TEXT,
                labor_cost REAL DEFAULT 0.0,
                parts_cost REAL DEFAULT 0.0,
                total_cost REAL DEFAULT 0.0,
                duration_hours REAL DEFAULT 0.0,
                contract_id INTEGER,
                under_warranty INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP,
                FOREIGN KEY (partner_id) REFERENCES res_partner (id),
                FOREIGN KEY (machine_id) REFERENCES product_product (id)
            )
        """)
        
        # Insérer des données de base si la base est vide
        self._insert_default_data()
        
        print("✓ Base de données initialisée avec succès")
    
    def _insert_default_data(self):
        """Insère les données par défaut (PCN, taxes standards, séquences)"""
        
        # Vérifier si des données existent déjà
        result = self.fetch_one("SELECT COUNT(*) as count FROM pcn_account")
        if result and result['count'] > 0:
            return  # Données déjà présentes
        
        # Comptes PCN de base (Structure simplifiée du PCN Algérien)
        pcn_accounts = [
            # Classe 1 - Comptes de Capitaux
            ('10', 'Capital', 'رأس المال', 'Capitaux', 1),
            ('11', 'Réserves', 'الاحتياطيات', 'Capitaux', 1),
            ('12', 'Résultat', 'النتيجة', 'Capitaux', 1),
            
            # Classe 2 - Comptes d'Immobilisations
            ('20', 'Immobilisations incorporelles', 'الأصول غير المادية', 'Actif', 1),
            ('21', 'Immobilisations corporelles', 'الأصول المادية', 'Actif', 1),
            
            # Classe 3 - Comptes de Stocks
            ('30', 'Stocks de marchandises', 'مخزون البضائع', 'Actif', 1),
            ('31', 'Stocks de matières premières', 'مخزون المواد الأولية', 'Actif', 1),
            
            # Classe 4 - Comptes de Tiers
            ('40', 'Fournisseurs', 'الموردون', 'Passif', 1),
            ('41', 'Clients', 'الزبائن', 'Actif', 1),
            ('42', 'Personnel', 'الموظفون', 'Passif', 1),
            ('44', 'État et collectivités', 'الدولة', 'Passif', 1),
            ('445', 'TVA Collectée', 'الرسم على القيمة المضافة المحصلة', 'Passif', 2),
            ('4456', 'TVA Déductible', 'الرسم على القيمة المضافة القابلة للخصم', 'Actif', 2),
            
            # Classe 5 - Comptes Financiers
            ('50', 'Banques', 'البنوك', 'Actif', 1),
            ('53', 'Caisse', 'الصندوق', 'Actif', 1),
            
            # Classe 6 - Comptes de Charges
            ('60', 'Achats consommés', 'المشتريات المستهلكة', 'Charges', 1),
            ('61', 'Services extérieurs', 'الخدمات الخارجية', 'Charges', 1),
            ('63', 'Charges de personnel', 'أعباء الموظفين', 'Charges', 1),
            ('64', 'Impôts et taxes', 'الضرائب والرسوم', 'Charges', 1),
            
            # Classe 7 - Comptes de Produits
            ('70', 'Ventes de marchandises', 'مبيعات البضائع', 'Produits', 1),
            ('71', 'Production vendue', 'الإنتاج المباع', 'Produits', 1),
        ]
        
        for code, name_fr, name_ar, account_type, level in pcn_accounts:
            self.execute_query("""
                INSERT OR IGNORE INTO pcn_account (code, name_fr, name_ar, account_type, level)
                VALUES (?, ?, ?, ?, ?)
            """, (code, name_fr, name_ar, account_type, level))
        
        # Taxes standards algériennes
        taxes = [
            ('TVA 19%', 'الرسم على القيمة المضافة 19%', 'tva', 19.0, 0, 'both', None),
            ('TVA 9%', 'الرسم على القيمة المضافة 9%', 'tva', 9.0, 0, 'both', None),
            ('TVA 0%', 'الرسم على القيمة المضافة 0%', 'tva', 0.0, 0, 'both', None),
            ('TAP 2%', 'الرسم على النشاط المهني 2%', 'tap', 2.0, 0, 'sale', None),
            ('Timbre Fiscal', 'الطابع الجبائي', 'timbre', 0.0, 25.0, 'both', None),  # 25 DA fixe
        ]
        
        for name, name_ar, tax_type, rate, amount, scope, pcn_account_id in taxes:
            self.execute_query("""
                INSERT OR IGNORE INTO account_tax (name, name_ar, tax_type, rate, amount, scope, pcn_account_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, name_ar, tax_type, rate, amount, scope, pcn_account_id))
        
        # Séquences par défaut
        sequences = [
            ('Factures de Vente', 'sale.order', 'INV', '', 5),
            ('Factures d\'Achat', 'purchase.order', 'BILL', '', 5),
            ('Bons de Livraison', 'stock.picking', 'BL', '', 5),
            ('Pièces Comptables', 'account.move', 'PC', '', 5),
        ]
        
        for name, code, prefix, suffix, padding in sequences:
            self.execute_query("""
                INSERT OR IGNORE INTO ir_sequence (name, code, prefix, suffix, padding)
                VALUES (?, ?, ?, ?, ?)
            """, (name, code, prefix, suffix, padding))
        
        # Créer un utilisateur admin par défaut
        self.execute_query("""
            INSERT OR IGNORE INTO res_users (login, password, name, email, is_admin)
            VALUES (?, ?, ?, ?, ?)
        """, ('admin', 'admin', 'Administrateur', 'admin@elamira.dz', 1))
        
        print("✓ Données par défaut insérées")
    
    def execute_query(self, query: str, params: Tuple = None) -> Optional[sqlite3.Cursor]:
        """
        Exécute une requête SQL (INSERT, UPDATE, DELETE, CREATE, etc.)
        
        Args:
            query: La requête SQL à exécuter
            params: Paramètres de la requête (tuple)
            
        Returns:
            Le curseur après exécution
        """
        try:
            cursor = self._connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self._connection.commit()
            return cursor
        except Exception as e:
            print(f"✗ Erreur d'exécution de la requête: {e}")
            print(f"  Requête: {query}")
            print(f"  Paramètres: {params}")
            self._connection.rollback()
            raise
    
    def fetch_all(self, query: str, params: Tuple = None) -> List[Dict[str, Any]]:
        """
        Exécute une requête SELECT et retourne tous les résultats
        
        Args:
            query: La requête SELECT
            params: Paramètres de la requête
            
        Returns:
            Liste de dictionnaires représentant les lignes
        """
        try:
            cursor = self._connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"✗ Erreur de lecture: {e}")
            print(f"  Requête: {query}")
            return []
    
    def fetch_one(self, query: str, params: Tuple = None) -> Optional[Dict[str, Any]]:
        """
        Exécute une requête SELECT et retourne un seul résultat
        
        Args:
            query: La requête SELECT
            params: Paramètres de la requête
            
        Returns:
            Un dictionnaire ou None
        """
        try:
            cursor = self._connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"✗ Erreur de lecture: {e}")
            return None
    
    def get_next_sequence(self, sequence_code: str) -> str:
        """
        Génère le prochain numéro de séquence
        
        Args:
            sequence_code: Code de la séquence
            
        Returns:
            Le numéro formaté (ex: INV00001)
        """
        seq = self.fetch_one(
            "SELECT * FROM ir_sequence WHERE code = ?",
            (sequence_code,)
        )
        
        if not seq:
            return "ERR00000"
        
        # Formater le numéro
        number = str(seq['next_number']).zfill(seq['padding'])
        full_number = f"{seq['prefix']}{number}{seq['suffix']}"
        
        # Incrémenter pour la prochaine fois
        self.execute_query(
            "UPDATE ir_sequence SET next_number = next_number + 1 WHERE code = ?",
            (sequence_code,)
        )
        
        return full_number
    
    def backup_database(self, backup_path: str) -> bool:
        """
        Crée une sauvegarde de la base de données
        
        Args:
            backup_path: Chemin du fichier de sauvegarde
            
        Returns:
            True si succès, False sinon
        """
        try:
            import shutil
            shutil.copy2(self._db_path, backup_path)
            print(f"✓ Sauvegarde créée: {backup_path}")
            return True
        except Exception as e:
            print(f"✗ Erreur de sauvegarde: {e}")
            return False
    
    def restore_database(self, backup_path: str) -> bool:
        """
        Restaure la base de données depuis une sauvegarde
        
        Args:
            backup_path: Chemin du fichier de sauvegarde
            
        Returns:
            True si succès, False sinon
        """
        try:
            import shutil
            self._connection.close()
            shutil.copy2(backup_path, self._db_path)
            self._connect()
            print(f"✓ Base de données restaurée depuis: {backup_path}")
            return True
        except Exception as e:
            print(f"✗ Erreur de restauration: {e}")
            return False
    
    def close(self):
        """Ferme la connexion à la base de données"""
        if self._connection:
            self._connection.close()
            print("✓ Connexion à la base de données fermée")
