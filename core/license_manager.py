# -*- coding: utf-8 -*-
"""
Gestionnaire de Licences
Gère les licences annuelles et à vie de l'application
"""

import hashlib
import uuid
import json
from datetime import datetime, timedelta
from typing import Optional, Dict


class LicenseManager:
    """
    Gestionnaire de licences pour l'application ElAmira ERP.
    Supporte les licences annuelles et à vie.
    """
    
    def __init__(self, db_manager):
        """
        Initialise le gestionnaire de licences
        
        Args:
            db_manager: Instance du DatabaseManager
        """
        self.db_manager = db_manager
        self._hardware_id = self._get_hardware_id()
    
    def _get_hardware_id(self) -> str:
        """
        Génère un identifiant unique basé sur le matériel
        
        Returns:
            Hash SHA256 du matériel
        """
        try:
            import platform
            
            # Récupérer des informations système
            machine = platform.machine()
            processor = platform.processor()
            system = platform.system()
            node = platform.node()
            
            # Créer une chaîne unique
            hardware_string = f"{machine}-{processor}-{system}-{node}"
            
            # Hasher la chaîne
            return hashlib.sha256(hardware_string.encode()).hexdigest()
        except Exception as e:
            print(f"⚠ Erreur lors de la génération du hardware ID: {e}")
            # Fallback sur un UUID
            return str(uuid.uuid4())
    
    def generate_license_key(self, company_name: str, email: str, license_type: str) -> str:
        """
        Génère une clé de licence unique
        
        Args:
            company_name: Nom de la société
            email: Email de contact
            license_type: Type de licence ('annual' ou 'lifetime')
            
        Returns:
            Clé de licence formatée
        """
        # Créer une chaîne à partir des informations
        data_string = f"{company_name}-{email}-{license_type}-{datetime.now().isoformat()}"
        
        # Générer un hash
        hash_obj = hashlib.sha256(data_string.encode())
        hash_hex = hash_obj.hexdigest().upper()
        
        # Formater en groupes de 4 caractères (ex: XXXX-XXXX-XXXX-XXXX)
        key_parts = [hash_hex[i:i+4] for i in range(0, 16, 4)]
        license_key = '-'.join(key_parts)
        
        return license_key
    
    def activate_license(self, license_key: str, company_name: str, 
                        email: str, license_type: str) -> Dict:
        """
        Active une licence
        
        Args:
            license_key: Clé de licence
            company_name: Nom de la société
            email: Email
            license_type: Type de licence ('annual' ou 'lifetime')
            
        Returns:
            Dictionnaire avec le statut de l'activation
        """
        try:
            # Vérifier si la licence existe déjà
            existing = self.db_manager.fetch_one(
                "SELECT * FROM system_license WHERE license_key = ?",
                (license_key,)
            )
            
            if existing and existing['is_active']:
                return {
                    'success': False,
                    'message': 'Cette licence est déjà activée'
                }
            
            # Calculer la date d'expiration
            activation_date = datetime.now()
            if license_type == 'annual':
                expiry_date = activation_date + timedelta(days=365)
            else:  # lifetime
                expiry_date = activation_date + timedelta(days=365*100)  # 100 ans
            
            # Insérer ou mettre à jour la licence
            if existing:
                self.db_manager.execute_query("""
                    UPDATE system_license 
                    SET is_active = 1,
                        activation_date = ?,
                        expiry_date = ?,
                        hardware_id = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE license_key = ?
                """, (
                    activation_date.isoformat(),
                    expiry_date.isoformat(),
                    self._hardware_id,
                    license_key
                ))
            else:
                self.db_manager.execute_query("""
                    INSERT INTO system_license 
                    (license_key, license_type, company_name, email, 
                     activation_date, expiry_date, is_active, hardware_id)
                    VALUES (?, ?, ?, ?, ?, ?, 1, ?)
                """, (
                    license_key,
                    license_type,
                    company_name,
                    email,
                    activation_date.isoformat(),
                    expiry_date.isoformat(),
                    self._hardware_id
                ))
            
            return {
                'success': True,
                'message': f'Licence activée avec succès jusqu\'au {expiry_date.strftime("%d/%m/%Y")}',
                'expiry_date': expiry_date.isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de l\'activation: {str(e)}'
            }
    
    def check_license(self) -> Dict:
        """
        Vérifie si une licence valide est active
        
        Returns:
            Dictionnaire avec le statut de la licence
        """
        try:
            # Récupérer toutes les licences actives
            licenses = self.db_manager.fetch_all("""
                SELECT * FROM system_license 
                WHERE is_active = 1
                ORDER BY activation_date DESC
            """)
            
            if not licenses:
                return {
                    'is_valid': False,
                    'message': 'Aucune licence active',
                    'trial_days_left': 30  # 30 jours d'essai
                }
            
            # Vérifier la première licence active
            license_data = licenses[0]
            
            # Vérifier l'expiration
            expiry_date = datetime.fromisoformat(license_data['expiry_date'])
            now = datetime.now()
            
            if expiry_date < now:
                return {
                    'is_valid': False,
                    'message': 'Licence expirée',
                    'expired_since': (now - expiry_date).days
                }
            
            # Licence valide
            days_left = (expiry_date - now).days
            
            return {
                'is_valid': True,
                'license_type': license_data['license_type'],
                'company_name': license_data['company_name'],
                'expiry_date': license_data['expiry_date'],
                'days_left': days_left,
                'message': f'Licence valide - {days_left} jours restants'
            }
            
        except Exception as e:
            print(f"✗ Erreur lors de la vérification de la licence: {e}")
            return {
                'is_valid': False,
                'message': f'Erreur: {str(e)}'
            }
    
    def deactivate_license(self, license_key: str) -> bool:
        """
        Désactive une licence
        
        Args:
            license_key: Clé de licence à désactiver
            
        Returns:
            True si succès
        """
        try:
            self.db_manager.execute_query("""
                UPDATE system_license 
                SET is_active = 0, updated_at = CURRENT_TIMESTAMP
                WHERE license_key = ?
            """, (license_key,))
            
            print(f"✓ Licence {license_key} désactivée")
            return True
        except Exception as e:
            print(f"✗ Erreur lors de la désactivation: {e}")
            return False
    
    def get_all_licenses(self) -> list:
        """
        Récupère toutes les licences enregistrées
        
        Returns:
            Liste des licences
        """
        return self.db_manager.fetch_all("""
            SELECT * FROM system_license 
            ORDER BY created_at DESC
        """)
    
    def export_license_info(self) -> str:
        """
        Exporte les informations de licence pour le support
        
        Returns:
            JSON des informations de licence
        """
        license_status = self.check_license()
        system_info = {
            'hardware_id': self._hardware_id,
            'license_status': license_status,
            'timestamp': datetime.now().isoformat()
        }
        
        return json.dumps(system_info, indent=2, ensure_ascii=False)
