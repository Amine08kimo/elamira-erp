#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Dialogues pour le module Maintenance
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, 
    QPushButton, QLineEdit, QTextEdit, QComboBox, QDateEdit,
    QDoubleSpinBox, QSpinBox, QMessageBox, QGroupBox, QScrollArea,
    QWidget, QCheckBox, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from datetime import datetime


class NewInterventionDialog(QDialog):
    """Dialogue création nouvelle intervention"""
    
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("➕ Nouvelle Intervention de Maintenance")
        self.setMinimumSize(900, 800)
        self.selected_client_id = None
        self.selected_client_name = ""
        self._setup_ui()
        self._load_data()
        self._generate_code()
    
    def _setup_ui(self):
        """Configure l'interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("🔧 Créer une Nouvelle Intervention")
        header.setStyleSheet("""
            font-size: 22px;
            font-weight: 700;
            color: #6750A4;
            padding-bottom: 10px;
        """)
        layout.addWidget(header)
        
        # Scroll area pour le formulaire
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(20)
        
        # ========== INFORMATIONS GÉNÉRALES ==========
        info_group = self._create_group("📋 Informations Générales")
        info_form = QFormLayout()
        info_form.setSpacing(15)
        
        # Code (auto-généré, lecture seule)
        self.code_input = QLineEdit()
        self.code_input.setReadOnly(True)
        self.code_input.setPlaceholderText("Généré automatiquement...")
        self.code_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #E0E0E0;
                border-radius: 6px;
                background: #F5F5F5;
                font-weight: 600;
                color: #6750A4;
            }
        """)
        info_form.addRow("🔖 Code Intervention:", self.code_input)
        
        # Titre/Nom
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Ex: Maintenance préventive JUKI DDL-8700")
        self._style_input(self.title_input)
        info_form.addRow("📝 Titre:", self.title_input)
        
        # Type intervention
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "⚙️ Maintenance Préventive",
            "🔧 Maintenance Corrective",
            "🔍 Diagnostic",
            "⚡ Dépannage Urgent",
            "🔄 Révision Complète",
            "🧰 Installation"
        ])
        self._style_combo(self.type_combo)
        info_form.addRow("🔧 Type:", self.type_combo)
        
        # Priorité
        self.priority_combo = QComboBox()
        self.priority_combo.addItems([
            "🔴 Urgent",
            "🟠 Élevée",
            "🟡 Normale",
            "🟢 Basse"
        ])
        self.priority_combo.setCurrentIndex(2)  # Normale par défaut
        self._style_combo(self.priority_combo)
        info_form.addRow("⚠️ Priorité:", self.priority_combo)
        
        info_group.setLayout(info_form)
        form_layout.addWidget(info_group)
        
        # ========== CLIENT & MACHINE ==========
        client_group = self._create_group("👤 Client & Machine")
        client_form = QFormLayout()
        client_form.setSpacing(15)
        
        # Client avec boutons
        client_layout = QHBoxLayout()
        
        self.client_input = QLineEdit()
        self.client_input.setReadOnly(True)
        self.client_input.setPlaceholderText("Aucun client sélectionné...")
        self._style_input(self.client_input)
        client_layout.addWidget(self.client_input)
        
        select_client_btn = QPushButton("🔍 Sélectionner")
        select_client_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 15px;
                background: #2563EB;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                min-width: 120px;
            }
            QPushButton:hover {
                background: #1D4ED8;
            }
        """)
        select_client_btn.clicked.connect(self.select_client)
        client_layout.addWidget(select_client_btn)
        
        new_client_btn = QPushButton("➕ Nouveau")
        new_client_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 15px;
                background: #10B981;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                min-width: 120px;
            }
            QPushButton:hover {
                background: #059669;
            }
        """)
        new_client_btn.clicked.connect(self.new_client)
        client_layout.addWidget(new_client_btn)
        
        client_form.addRow("👤 Client:", client_layout)
        
        # Machine
        self.machine_combo = QComboBox()
        self.machine_combo.setEditable(True)
        self.machine_combo.setPlaceholderText("Sélectionner ou saisir une machine...")
        self._style_combo(self.machine_combo)
        client_form.addRow("🏭 Machine:", self.machine_combo)
        
        # Numéro de série machine
        self.serial_input = QLineEdit()
        self.serial_input.setPlaceholderText("Ex: JUKI-2024-XYZ-001")
        self._style_input(self.serial_input)
        client_form.addRow("🔢 N° Série:", self.serial_input)
        
        client_group.setLayout(client_form)
        form_layout.addWidget(client_group)
        
        # ========== PLANIFICATION ==========
        planning_group = self._create_group("📅 Planification")
        planning_form = QFormLayout()
        planning_form.setSpacing(15)
        
        # Date planifiée
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("dd/MM/yyyy")
        self._style_date(self.date_input)
        planning_form.addRow("📅 Date Intervention:", self.date_input)
        
        # Durée estimée
        self.duration_input = QSpinBox()
        self.duration_input.setRange(1, 480)
        self.duration_input.setValue(60)
        self.duration_input.setSuffix(" min")
        self._style_spinbox(self.duration_input)
        planning_form.addRow("⏱️ Durée Estimée:", self.duration_input)
        
        # Technicien
        self.technician_combo = QComboBox()
        self.technician_combo.setEditable(True)
        self.technician_combo.setPlaceholderText("Assigner un technicien...")
        self._style_combo(self.technician_combo)
        planning_form.addRow("👨‍🔧 Technicien:", self.technician_combo)
        
        planning_group.setLayout(planning_form)
        form_layout.addWidget(planning_group)
        
        # ========== TARIFICATION ==========
        pricing_group = self._create_group("💰 Tarification")
        pricing_form = QFormLayout()
        pricing_form.setSpacing(15)
        
        # Prix service
        self.service_price_input = QDoubleSpinBox()
        self.service_price_input.setRange(0, 1000000)
        self.service_price_input.setValue(0)
        self.service_price_input.setDecimals(2)
        self.service_price_input.setSuffix(" DA")
        self._style_spinbox(self.service_price_input)
        pricing_form.addRow("💵 Prix Service:", self.service_price_input)
        
        # TVA
        self.tva_input = QDoubleSpinBox()
        self.tva_input.setRange(0, 100)
        self.tva_input.setValue(19)
        self.tva_input.setDecimals(2)
        self.tva_input.setSuffix(" %")
        self._style_spinbox(self.tva_input)
        pricing_form.addRow("📊 TVA:", self.tva_input)
        
        # Prix pièces
        self.parts_price_input = QDoubleSpinBox()
        self.parts_price_input.setRange(0, 1000000)
        self.parts_price_input.setValue(0)
        self.parts_price_input.setDecimals(2)
        self.parts_price_input.setSuffix(" DA")
        self._style_spinbox(self.parts_price_input)
        pricing_form.addRow("🔩 Prix Pièces:", self.parts_price_input)
        
        # Total calculé (lecture seule)
        self.total_label = QLabel("0.00 DA")
        self.total_label.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #10B981;
            padding: 10px;
            background: #E8F5F0;
            border-radius: 6px;
        """)
        pricing_form.addRow("💰 Total TTC:", self.total_label)
        
        # Connecter calcul auto
        self.service_price_input.valueChanged.connect(self._calculate_total)
        self.tva_input.valueChanged.connect(self._calculate_total)
        self.parts_price_input.valueChanged.connect(self._calculate_total)
        
        pricing_group.setLayout(pricing_form)
        form_layout.addWidget(pricing_group)
        
        # ========== DÉTAILS TECHNIQUES ==========
        details_group = self._create_group("🔍 Détails Techniques")
        details_layout = QVBoxLayout()
        
        # Description
        desc_label = QLabel("📝 Description Intervention:")
        desc_label.setStyleSheet("font-weight: 600; color: #1A1A1A;")
        details_layout.addWidget(desc_label)
        
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText(
            "Décrire l'intervention à réaliser:\n"
            "- Problème constaté\n"
            "- Actions à effectuer\n"
            "- Points à vérifier\n"
            "- Pièces à remplacer..."
        )
        self.description_input.setMinimumHeight(100)
        self._style_text(self.description_input)
        details_layout.addWidget(self.description_input)
        
        # Détails maintenance
        maint_label = QLabel("🔧 Détails Maintenance:")
        maint_label.setStyleSheet("font-weight: 600; color: #1A1A1A; margin-top: 15px;")
        details_layout.addWidget(maint_label)
        
        self.maintenance_details_input = QTextEdit()
        self.maintenance_details_input.setPlaceholderText(
            "Détails techniques de la maintenance:\n"
            "- Vérifications effectuées\n"
            "- Réglages réalisés\n"
            "- Pièces remplacées\n"
            "- Recommandations..."
        )
        self.maintenance_details_input.setMinimumHeight(100)
        self._style_text(self.maintenance_details_input)
        details_layout.addWidget(self.maintenance_details_input)
        
        # Notes
        notes_label = QLabel("📌 Notes Internes:")
        notes_label.setStyleSheet("font-weight: 600; color: #1A1A1A; margin-top: 15px;")
        details_layout.addWidget(notes_label)
        
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Notes internes (non visibles par le client)...")
        self.notes_input.setMinimumHeight(80)
        self._style_text(self.notes_input)
        details_layout.addWidget(self.notes_input)
        
        details_group.setLayout(details_layout)
        form_layout.addWidget(details_group)
        
        # ========== OPTIONS ==========
        options_group = self._create_group("⚙️ Options")
        options_layout = QVBoxLayout()
        
        self.send_email_check = QCheckBox("📧 Envoyer confirmation email au client")
        self.send_email_check.setChecked(True)
        self._style_checkbox(self.send_email_check)
        options_layout.addWidget(self.send_email_check)
        
        self.create_contract_check = QCheckBox("📋 Créer un contrat de maintenance associé")
        self._style_checkbox(self.create_contract_check)
        options_layout.addWidget(self.create_contract_check)
        
        self.urgent_check = QCheckBox("🚨 Marquer comme intervention urgente")
        self._style_checkbox(self.urgent_check)
        options_layout.addWidget(self.urgent_check)
        
        options_group.setLayout(options_layout)
        form_layout.addWidget(options_group)
        
        scroll.setWidget(form_widget)
        layout.addWidget(scroll)
        
        # ========== BOUTONS ACTION ==========
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        btn_layout.addStretch()
        
        # Aperçu PDF
        preview_btn = QPushButton("👁️  Aperçu PDF")
        preview_btn.setStyleSheet("""
            QPushButton {
                padding: 12px 25px;
                background: #2563EB;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #1D4ED8;
            }
        """)
        preview_btn.clicked.connect(self.preview_pdf)
        btn_layout.addWidget(preview_btn)
        
        # Annuler
        cancel_btn = QPushButton("❌ Annuler")
        cancel_btn.setStyleSheet("""
            QPushButton {
                padding: 12px 25px;
                background: #E0E0E0;
                color: #1A1A1A;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #D0D0D0;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        # Sauvegarder
        save_btn = QPushButton("✅ Créer l'Intervention")
        save_btn.setStyleSheet("""
            QPushButton {
                padding: 12px 30px;
                background: #10B981;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: 700;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #059669;
            }
        """)
        save_btn.clicked.connect(self.save_intervention)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
    
    def _create_group(self, title):
        """Crée un groupe avec style"""
        group = QGroupBox(title)
        group.setStyleSheet("""
            QGroupBox {
                font-size: 15px;
                font-weight: 700;
                color: #1A1A1A;
                border: 2px solid #E0E0E0;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 20px;
                background: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 5px 10px;
                background: white;
            }
        """)
        return group
    
    def _style_input(self, widget):
        """Style pour QLineEdit"""
        widget.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #E0E0E0;
                border-radius: 6px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #6750A4;
                background: #FAFAFA;
            }
        """)
    
    def _style_combo(self, widget):
        """Style pour QComboBox"""
        widget.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 2px solid #E0E0E0;
                border-radius: 6px;
                font-size: 13px;
            }
            QComboBox:focus {
                border: 2px solid #6750A4;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
        """)
    
    def _style_date(self, widget):
        """Style pour QDateEdit"""
        widget.setStyleSheet("""
            QDateEdit {
                padding: 10px;
                border: 2px solid #E0E0E0;
                border-radius: 6px;
                font-size: 13px;
            }
            QDateEdit:focus {
                border: 2px solid #6750A4;
            }
        """)
    
    def _style_spinbox(self, widget):
        """Style pour QSpinBox/QDoubleSpinBox"""
        widget.setStyleSheet("""
            QSpinBox, QDoubleSpinBox {
                padding: 10px;
                border: 2px solid #E0E0E0;
                border-radius: 6px;
                font-size: 13px;
            }
            QSpinBox:focus, QDoubleSpinBox:focus {
                border: 2px solid #6750A4;
            }
        """)
    
    def _style_text(self, widget):
        """Style pour QTextEdit"""
        widget.setStyleSheet("""
            QTextEdit {
                padding: 10px;
                border: 2px solid #E0E0E0;
                border-radius: 6px;
                font-size: 13px;
            }
            QTextEdit:focus {
                border: 2px solid #6750A4;
                background: #FAFAFA;
            }
        """)
    
    def _style_checkbox(self, widget):
        """Style pour QCheckBox"""
        widget.setStyleSheet("""
            QCheckBox {
                font-size: 13px;
                padding: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
        """)
    
    def _load_data(self):
        """Charge les données (clients, machines, techniciens)"""
        # Clients chargés depuis DB via dialogues
        
        # Machines (TODO: charger depuis DB)
        machines = [
            "JUKI DDL-8700",
            "JACK JK-5040",
            "BROTHER S-7300A",
            "SIRUBA 747F",
            "TYPICAL GC6160"
        ]
        self.machine_combo.addItems(machines)
        
        # Techniciens (TODO: charger depuis DB)
        technicians = [
            "Mohammed BENALI",
            "Karim MEZIANE",
            "Ahmed BOUDIAF",
            "Rachid HAMIDI"
        ]
        self.technician_combo.addItems(technicians)
    
    def _generate_code(self):
        """Génère le code intervention (MAINT-YYYY-NNN)"""
        year = datetime.now().year
        # TODO: Récupérer le dernier numéro depuis DB
        last_number = 1  # Temporaire
        code = f"MAINT-{year}-{last_number:03d}"
        self.code_input.setText(code)
    
    def _calculate_total(self):
        """Calcule le total TTC"""
        service = self.service_price_input.value()
        parts = self.parts_price_input.value()
        tva_rate = self.tva_input.value()
        
        subtotal = service + parts
        tva_amount = subtotal * (tva_rate / 100)
        total = subtotal + tva_amount
        
        self.total_label.setText(f"{total:,.2f} DA")
    
    def select_client(self):
        """Ouvre dialogue sélection client"""
        dialog = SelectClientDialog(self.controller, self)
        if dialog.exec():
            self.selected_client_id = dialog.selected_client_id
            self.selected_client_name = dialog.selected_client_name
            self.client_input.setText(self.selected_client_name)
            print(f"✅ Client sélectionné: {self.selected_client_name} (ID: {self.selected_client_id})")
    
    def new_client(self):
        """Ouvre dialogue nouveau client"""
        dialog = NewClientDialog(self.controller, self)
        if dialog.exec():
            # Client créé, le sélectionner automatiquement
            self.selected_client_id = dialog.created_client_id
            self.selected_client_name = dialog.created_client_name
            self.client_input.setText(self.selected_client_name)
            print(f"✅ Nouveau client créé: {self.selected_client_name}")
    
    def preview_pdf(self):
        """Aperçu du PDF"""
        from modules.maintenance.reports import MaintenanceReportGenerator
        import os
        import subprocess
        
        # Générer un PDF temporaire
        generator = MaintenanceReportGenerator(self.controller)
        
        # Créer un rapport de test avec les données du formulaire
        try:
            pdf_path = generator.generate_dashboard_report()
            
            if pdf_path and os.path.exists(pdf_path):
                # Ouvrir avec le viewer par défaut
                if os.name == 'nt':  # Windows
                    os.startfile(pdf_path)
                elif os.name == 'posix':  # Linux/Mac
                    subprocess.call(('xdg-open', pdf_path))
                
                QMessageBox.information(self, "Aperçu PDF", 
                    f"👁️ Aperçu ouvert:\n{pdf_path}")
            else:
                QMessageBox.warning(self, "Erreur", "Impossible de générer l'aperçu")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur aperçu: {str(e)}")
    
    def save_intervention(self):
        """Sauvegarde l'intervention"""
        # Validation
        if not self.title_input.text().strip():
            QMessageBox.warning(self, "Erreur", "❌ Veuillez saisir un titre")
            return
        
        if not self.selected_client_id:
            QMessageBox.warning(self, "Erreur", "❌ Veuillez sélectionner un client")
            return
        
        # Créer l'intervention
        # TODO: Sauvegarder en DB
        
        QMessageBox.information(self, "Succès", 
            f"✅ Intervention {self.code_input.text()} créée avec succès!")
        self.accept()


class SelectClientDialog(QDialog):
    """Dialogue sélection client depuis DB"""
    
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.selected_client_id = None
        self.selected_client_name = ""
        self.setWindowTitle("🔍 Sélectionner un Client")
        self.setMinimumSize(700, 500)
        self._setup_ui()
        self._load_clients()
    
    def _setup_ui(self):
        """Configure l'interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("👤 Sélectionner un Client")
        header.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #2563EB;
        """)
        layout.addWidget(header)
        
        # Recherche
        search_layout = QHBoxLayout()
        search_label = QLabel("🔍 Rechercher:")
        search_label.setStyleSheet("font-weight: 600;")
        search_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nom du client...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #E0E0E0;
                border-radius: 6px;
            }
            QLineEdit:focus {
                border: 2px solid #2563EB;
            }
        """)
        self.search_input.textChanged.connect(self._filter_clients)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Table clients
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Téléphone", "Ville"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 2px solid #E0E0E0;
                border-radius: 6px;
            }
            QHeaderView::section {
                background: #F5F5F5;
                padding: 10px;
                border: none;
                font-weight: 700;
                color: #1A1A1A;
            }
            QTableWidget::item:selected {
                background: #E8F0FE;
                color: #1A1A1A;
            }
        """)
        self.table.doubleClicked.connect(self._select_and_close)
        layout.addWidget(self.table)
        
        # Boutons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("❌ Annuler")
        cancel_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                background: #E0E0E0;
                border: none;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #D0D0D0;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        select_btn = QPushButton("✅ Sélectionner")
        select_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 25px;
                background: #2563EB;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 700;
            }
            QPushButton:hover {
                background: #1D4ED8;
            }
        """)
        select_btn.clicked.connect(self._select_client)
        btn_layout.addWidget(select_btn)
        
        layout.addLayout(btn_layout)
    
    def _load_clients(self):
        """Charge la liste des clients depuis DB"""
        # TODO: Charger depuis vraie DB
        # Pour l'instant, clients d'exemple
        self.all_clients = [
            {"id": 1, "name": "ATELIER DE COUTURE MODERNE", "phone": "0550123456", "city": "Alger"},
            {"id": 2, "name": "USINE TEXTILE SETIF", "phone": "0551234567", "city": "Sétif"},
            {"id": 3, "name": "CONFECTION AL-BARAKA", "phone": "0552345678", "city": "Oran"},
            {"id": 4, "name": "MAISON DE LA COUTURE", "phone": "0553456789", "city": "Constantine"},
        ]
        self._populate_table(self.all_clients)
    
    def _populate_table(self, clients):
        """Remplit la table avec les clients"""
        self.table.setRowCount(len(clients))
        for i, client in enumerate(clients):
            self.table.setItem(i, 0, QTableWidgetItem(str(client["id"])))
            self.table.setItem(i, 1, QTableWidgetItem(client["name"]))
            self.table.setItem(i, 2, QTableWidgetItem(client["phone"]))
            self.table.setItem(i, 3, QTableWidgetItem(client["city"]))
        
        # Masquer colonne ID
        self.table.setColumnHidden(0, True)
    
    def _filter_clients(self):
        """Filtre les clients par recherche"""
        search_text = self.search_input.text().lower()
        if not search_text:
            self._populate_table(self.all_clients)
            return
        
        filtered = [
            c for c in self.all_clients
            if search_text in c["name"].lower() or
               search_text in c["phone"] or
               search_text in c["city"].lower()
        ]
        self._populate_table(filtered)
    
    def _select_client(self):
        """Sélectionne le client"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Erreur", "❌ Veuillez sélectionner un client")
            return
        
        self.selected_client_id = int(self.table.item(row, 0).text())
        self.selected_client_name = self.table.item(row, 1).text()
        self.accept()
    
    def _select_and_close(self):
        """Double-clic pour sélectionner"""
        self._select_client()


class NewClientDialog(QDialog):
    """Dialogue création nouveau client"""
    
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.created_client_id = None
        self.created_client_name = ""
        self.setWindowTitle("➕ Nouveau Client")
        self.setMinimumSize(600, 500)
        self._setup_ui()
    
    def _setup_ui(self):
        """Configure l'interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("👤 Créer un Nouveau Client")
        header.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #10B981;
        """)
        layout.addWidget(header)
        
        # Formulaire
        form = QFormLayout()
        form.setSpacing(15)
        
        # Nom
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ex: ATELIER DE COUTURE MODERNE")
        self._style_input(self.name_input)
        form.addRow("📝 Nom Complet:", self.name_input)
        
        # Téléphone
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Ex: 0550123456")
        self._style_input(self.phone_input)
        form.addRow("📞 Téléphone:", self.phone_input)
        
        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Ex: contact@atelier.dz")
        self._style_input(self.email_input)
        form.addRow("📧 Email:", self.email_input)
        
        # Adresse
        self.address_input = QTextEdit()
        self.address_input.setPlaceholderText("Adresse complète...")
        self.address_input.setMaximumHeight(80)
        self._style_text(self.address_input)
        form.addRow("📍 Adresse:", self.address_input)
        
        # Ville
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Ex: Alger")
        self._style_input(self.city_input)
        form.addRow("🏙️ Ville:", self.city_input)
        
        # Code postal
        self.zip_input = QLineEdit()
        self.zip_input.setPlaceholderText("Ex: 16000")
        self._style_input(self.zip_input)
        form.addRow("📮 Code Postal:", self.zip_input)
        
        # Type client
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "Professionnel",
            "Particulier",
            "Entreprise",
            "Usine"
        ])
        self._style_combo(self.type_combo)
        form.addRow("🏭 Type:", self.type_combo)
        
        # Notes
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Notes sur le client...")
        self.notes_input.setMaximumHeight(80)
        self._style_text(self.notes_input)
        form.addRow("📋 Notes:", self.notes_input)
        
        layout.addLayout(form)
        layout.addStretch()
        
        # Boutons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("❌ Annuler")
        cancel_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                background: #E0E0E0;
                border: none;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #D0D0D0;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("✅ Créer le Client")
        save_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 25px;
                background: #10B981;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 700;
            }
            QPushButton:hover {
                background: #059669;
            }
        """)
        save_btn.clicked.connect(self._save_client)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
    
    def _style_input(self, widget):
        """Style input"""
        widget.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #E0E0E0;
                border-radius: 6px;
            }
            QLineEdit:focus {
                border: 2px solid #10B981;
            }
        """)
    
    def _style_text(self, widget):
        """Style text"""
        widget.setStyleSheet("""
            QTextEdit {
                padding: 10px;
                border: 2px solid #E0E0E0;
                border-radius: 6px;
            }
            QTextEdit:focus {
                border: 2px solid #10B981;
            }
        """)
    
    def _style_combo(self, widget):
        """Style combo"""
        widget.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 2px solid #E0E0E0;
                border-radius: 6px;
            }
            QComboBox:focus {
                border: 2px solid #10B981;
            }
        """)
    
    def _save_client(self):
        """Sauvegarde le nouveau client"""
        # Validation
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Erreur", "❌ Veuillez saisir un nom")
            return
        
        if not self.phone_input.text().strip():
            QMessageBox.warning(self, "Erreur", "❌ Veuillez saisir un téléphone")
            return
        
        # TODO: Sauvegarder en DB
        # Pour l'instant, générer un ID temporaire
        self.created_client_id = 999  # Temporaire
        self.created_client_name = self.name_input.text().strip()
        
        QMessageBox.information(self, "Succès", 
            f"✅ Client '{self.created_client_name}' créé avec succès!")
        self.accept()
