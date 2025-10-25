# -*- coding: utf-8 -*-
"""
Settings Views - Vues des paramètres
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QLabel, QLineEdit, QFormLayout, QPushButton,
    QComboBox, QGroupBox, QTextEdit, QMessageBox,
    QFileDialog
)
from PyQt6.QtCore import Qt
from core.license_manager import LicenseManager


class SettingsView(QWidget):
    """Vue principale des paramètres"""
    
    def __init__(self, module, db_manager):
        super().__init__()
        self.module = module
        self.db_manager = db_manager
        self.license_manager = LicenseManager(db_manager)
        self._setup_ui()
        self._load_settings()
    
    def _setup_ui(self):
        """Configure l'interface style Odoo"""
        # Fond clair comme Odoo
        self.setStyleSheet("background-color: #F9FAFB;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)
        
        # Titre style Odoo - taille réduite
        title = QLabel("⚙️ Paramètres et Configuration")
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: 600;
            color: #202124;
            padding-bottom: 8px;
            background-color: transparent;
        """)
        layout.addWidget(title)
        
        # Onglets
        tabs = QTabWidget()
        
        # Onglet Général
        tabs.addTab(self._create_general_tab(), "🌍 Général")
        
        # Onglet Société (DZ)
        tabs.addTab(self._create_company_tab(), "🏢 Ma Société")
        
        # Onglet Licence
        tabs.addTab(self._create_license_tab(), "🔐 Licence")
        
        # Onglet Base de données
        tabs.addTab(self._create_database_tab(), "💾 Base de données")
        
        layout.addWidget(tabs)
    
    def _create_general_tab(self) -> QWidget:
        """Onglet paramètres généraux"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        
        # Langue
        lang_group = QGroupBox("🌐 Langue / اللغة")
        lang_layout = QFormLayout(lang_group)
        
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("Français", "fr")
        self.lang_combo.addItem("العربية (Arabe)", "ar")
        lang_layout.addRow("Langue de l'interface:", self.lang_combo)
        
        layout.addWidget(lang_group)
        
        # Apparence
        theme_group = QGroupBox("🎨 Apparence")
        theme_layout = QFormLayout(theme_group)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("Clair (Odoo)", "light")
        self.theme_combo.addItem("Sombre", "dark")
        theme_layout.addRow("Thème:", self.theme_combo)
        
        layout.addWidget(theme_group)
        
        layout.addStretch()
        
        # Boutons
        save_btn = QPushButton("💾 Enregistrer")
        save_btn.setObjectName("primaryBtn")
        save_btn.clicked.connect(self._save_general_settings)
        layout.addWidget(save_btn, alignment=Qt.AlignmentFlag.AlignRight)
        
        return widget
    
    def _create_company_tab(self) -> QWidget:
        """Onglet informations société (DZ)"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        
        info_label = QLabel(
            "ℹ️ Informations de votre société - Obligatoires pour la facturation DZ"
        )
        info_label.setStyleSheet("""
            background: #FEF3C7;
            padding: 10px;
            border-radius: 6px;
            color: #92400E;
        """)
        layout.addWidget(info_label)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Nom
        self.company_name_edit = QLineEdit()
        form_layout.addRow("Raison sociale *:", self.company_name_edit)
        
        # Nom arabe
        self.company_name_ar_edit = QLineEdit()
        form_layout.addRow("الاسم بالعربية:", self.company_name_ar_edit)
        
        # Adresse
        self.company_address_edit = QTextEdit()
        self.company_address_edit.setMaximumHeight(60)
        form_layout.addRow("Adresse:", self.company_address_edit)
        
        # Téléphone
        self.company_phone_edit = QLineEdit()
        form_layout.addRow("Téléphone:", self.company_phone_edit)
        
        # Email
        self.company_email_edit = QLineEdit()
        form_layout.addRow("Email:", self.company_email_edit)
        
        # === IDENTIFIANTS FISCAUX DZ ===
        fiscal_label = QLabel("📋 Identifiants Fiscaux (Obligatoires)")
        fiscal_label.setStyleSheet("font-weight: 600; margin-top: 15px;")
        form_layout.addRow(fiscal_label)
        
        # NIF
        self.company_nif_edit = QLineEdit()
        self.company_nif_edit.setPlaceholderText("Ex: 099900000000000")
        form_layout.addRow("NIF *:", self.company_nif_edit)
        
        # NIS
        self.company_nis_edit = QLineEdit()
        self.company_nis_edit.setPlaceholderText("Ex: 00000000000000")
        form_layout.addRow("NIS *:", self.company_nis_edit)
        
        # ART
        self.company_art_edit = QLineEdit()
        self.company_art_edit.setPlaceholderText("Ex: 00/00-0000000B00")
        form_layout.addRow("ART (RC) *:", self.company_art_edit)
        
        layout.addLayout(form_layout)
        
        layout.addStretch()
        
        # Boutons
        save_btn = QPushButton("💾 Enregistrer")
        save_btn.setObjectName("primaryBtn")
        save_btn.clicked.connect(self._save_company_settings)
        layout.addWidget(save_btn, alignment=Qt.AlignmentFlag.AlignRight)
        
        return widget
    
    def _create_license_tab(self) -> QWidget:
        """Onglet gestion de licence"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        
        # Statut actuel
        status_group = QGroupBox("📊 Statut de la Licence")
        status_layout = QVBoxLayout(status_group)
        
        self.license_status_label = QLabel("Vérification en cours...")
        self.license_status_label.setWordWrap(True)
        status_layout.addWidget(self.license_status_label)
        
        layout.addWidget(status_group)
        
        # Activation
        activation_group = QGroupBox("🔐 Activer une Licence")
        activation_layout = QFormLayout(activation_group)
        
        self.license_key_edit = QLineEdit()
        self.license_key_edit.setPlaceholderText("XXXX-XXXX-XXXX-XXXX")
        activation_layout.addRow("Clé de licence:", self.license_key_edit)
        
        self.license_company_edit = QLineEdit()
        activation_layout.addRow("Nom de société:", self.license_company_edit)
        
        self.license_email_edit = QLineEdit()
        activation_layout.addRow("Email:", self.license_email_edit)
        
        self.license_type_combo = QComboBox()
        self.license_type_combo.addItem("Licence Annuelle", "annual")
        self.license_type_combo.addItem("Licence à Vie", "lifetime")
        activation_layout.addRow("Type:", self.license_type_combo)
        
        activate_btn = QPushButton("✓ Activer la Licence")
        activate_btn.setObjectName("successBtn")
        activate_btn.clicked.connect(self._activate_license)
        activation_layout.addRow("", activate_btn)
        
        layout.addWidget(activation_group)
        
        # Générer une clé (pour test)
        generate_group = QGroupBox("🔧 Générer une Clé (Test)")
        generate_layout = QVBoxLayout(generate_group)
        
        generate_btn = QPushButton("🔑 Générer une Clé de Test")
        generate_btn.setObjectName("secondaryBtn")
        generate_btn.clicked.connect(self._generate_test_license)
        generate_layout.addWidget(generate_btn)
        
        layout.addWidget(generate_group)
        
        layout.addStretch()
        
        # Charger le statut
        self._update_license_status()
        
        return widget
    
    def _create_database_tab(self) -> QWidget:
        """Onglet gestion base de données"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        
        info_label = QLabel(
            "⚠️ Attention: Effectuez des sauvegardes régulières de votre base de données"
        )
        info_label.setStyleSheet("""
            background: #FEE2E2;
            padding: 10px;
            border-radius: 6px;
            color: #991B1B;
        """)
        layout.addWidget(info_label)
        
        # Sauvegarde
        backup_group = QGroupBox("💾 Sauvegarde")
        backup_layout = QVBoxLayout(backup_group)
        
        backup_btn = QPushButton("📥 Créer une Sauvegarde")
        backup_btn.setObjectName("primaryBtn")
        backup_btn.clicked.connect(self._backup_database)
        backup_layout.addWidget(backup_btn)
        
        layout.addWidget(backup_group)
        
        # Restauration
        restore_group = QGroupBox("♻ Restauration")
        restore_layout = QVBoxLayout(restore_group)
        
        restore_btn = QPushButton("📤 Restaurer depuis une Sauvegarde")
        restore_btn.setObjectName("secondaryBtn")
        restore_btn.clicked.connect(self._restore_database)
        restore_layout.addWidget(restore_btn)
        
        layout.addWidget(restore_group)
        
        layout.addStretch()
        
        return widget
    
    def _load_settings(self):
        """Charge les paramètres actuels"""
        # Charger les infos société
        company = self.db_manager.fetch_one("SELECT * FROM res_company LIMIT 1")
        
        if company:
            self.company_name_edit.setText(company.get('name', ''))
            self.company_name_ar_edit.setText(company.get('name_ar', ''))
            self.company_address_edit.setPlainText(company.get('address', ''))
            self.company_phone_edit.setText(company.get('phone', ''))
            self.company_email_edit.setText(company.get('email', ''))
            self.company_nif_edit.setText(company.get('nif', ''))
            self.company_nis_edit.setText(company.get('nis', ''))
            self.company_art_edit.setText(company.get('art', ''))
    
    def _save_general_settings(self):
        """Enregistre les paramètres généraux"""
        QMessageBox.information(
            self,
            "Paramètres",
            "Paramètres généraux enregistrés!\nRedémarrez l'application pour appliquer les changements."
        )
    
    def _save_company_settings(self):
        """Enregistre les informations de la société"""
        # Validation
        if not self.company_name_edit.text():
            QMessageBox.warning(self, "Validation", "Le nom de la société est obligatoire")
            return
        
        if not self.company_nif_edit.text():
            QMessageBox.warning(self, "Validation", "Le NIF est obligatoire")
            return
        
        # Vérifier si une société existe
        existing = self.db_manager.fetch_one("SELECT * FROM res_company LIMIT 1")
        
        try:
            if existing:
                # Mise à jour
                self.db_manager.execute_query("""
                    UPDATE res_company SET
                        name = ?, name_ar = ?, address = ?, phone = ?,
                        email = ?, nif = ?, nis = ?, art = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (
                    self.company_name_edit.text(),
                    self.company_name_ar_edit.text(),
                    self.company_address_edit.toPlainText(),
                    self.company_phone_edit.text(),
                    self.company_email_edit.text(),
                    self.company_nif_edit.text(),
                    self.company_nis_edit.text(),
                    self.company_art_edit.text(),
                    existing['id']
                ))
            else:
                # Création
                self.db_manager.execute_query("""
                    INSERT INTO res_company (
                        name, name_ar, address, phone, email, nif, nis, art
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    self.company_name_edit.text(),
                    self.company_name_ar_edit.text(),
                    self.company_address_edit.toPlainText(),
                    self.company_phone_edit.text(),
                    self.company_email_edit.text(),
                    self.company_nif_edit.text(),
                    self.company_nis_edit.text(),
                    self.company_art_edit.text()
                ))
            
            QMessageBox.information(
                self,
                "Succès",
                "Informations de la société enregistrées avec succès!"
            )
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur:\n{str(e)}")
    
    def _update_license_status(self):
        """Met à jour l'affichage du statut de licence"""
        status = self.license_manager.check_license()
        
        if status['is_valid']:
            text = f"""
✅ Licence Active

Type: {status['license_type'].upper()}
Société: {status['company_name']}
Expire le: {status['expiry_date'][:10]}
Jours restants: {status['days_left']}
            """
            self.license_status_label.setStyleSheet("color: #065F46;")
        else:
            text = f"""
⚠️ Aucune Licence Active

{status['message']}

Veuillez activer une licence pour bénéficier de toutes les fonctionnalités.
            """
            self.license_status_label.setStyleSheet("color: #991B1B;")
        
        self.license_status_label.setText(text)
    
    def _activate_license(self):
        """Active une licence"""
        key = self.license_key_edit.text()
        company = self.license_company_edit.text()
        email = self.license_email_edit.text()
        license_type = self.license_type_combo.currentData()
        
        if not key or not company or not email:
            QMessageBox.warning(
                self,
                "Validation",
                "Veuillez remplir tous les champs"
            )
            return
        
        result = self.license_manager.activate_license(
            key, company, email, license_type
        )
        
        if result['success']:
            QMessageBox.information(self, "Succès", result['message'])
            self._update_license_status()
        else:
            QMessageBox.warning(self, "Erreur", result['message'])
    
    def _generate_test_license(self):
        """Génère une clé de test"""
        import random
        import string
        
        # Générer une clé aléatoire pour test
        key_parts = []
        for _ in range(4):
            part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            key_parts.append(part)
        
        test_key = '-'.join(key_parts)
        
        self.license_key_edit.setText(test_key)
        self.license_company_edit.setText("Société Test")
        self.license_email_edit.setText("test@example.com")
        
        QMessageBox.information(
            self,
            "Clé de Test",
            f"Clé de test générée:\n{test_key}\n\nCliquez sur 'Activer' pour l'utiliser"
        )
    
    def _backup_database(self):
        """Crée une sauvegarde"""
        from datetime import datetime
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Sauvegarder la base de données",
            f"elamira_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db",
            "SQLite Database (*.db)"
        )
        
        if filename:
            if self.db_manager.backup_database(filename):
                QMessageBox.information(
                    self,
                    "Succès",
                    f"Sauvegarde créée avec succès:\n{filename}"
                )
            else:
                QMessageBox.critical(self, "Erreur", "Erreur lors de la sauvegarde")
    
    def _restore_database(self):
        """Restaure depuis une sauvegarde"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Restaurer la base de données",
            "",
            "SQLite Database (*.db)"
        )
        
        if filename:
            reply = QMessageBox.question(
                self,
                "Confirmation",
                "⚠️ ATTENTION: Cette opération va remplacer toutes les données actuelles!\n\n"
                "Êtes-vous sûr de vouloir continuer?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                if self.db_manager.restore_database(filename):
                    QMessageBox.information(
                        self,
                        "Succès",
                        "Base de données restaurée!\n\nRedémarrez l'application."
                    )
                else:
                    QMessageBox.critical(self, "Erreur", "Erreur lors de la restauration")
