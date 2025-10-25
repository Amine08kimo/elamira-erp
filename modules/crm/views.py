# -*- coding: utf-8 -*-
"""
CRM Views - Vues du module CRM
Vue Kanban du pipeline de ventes
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QScrollArea, QFrame,
    QGridLayout, QDialog, QFormLayout, QTextEdit,
    QDoubleSpinBox, QComboBox, QDateEdit, QMessageBox
)
from PyQt6.QtCore import Qt, QDate
from .controller import CRMController
from .models import Lead


class CRMLeadListView(QWidget):
    """Vue principale du CRM avec pipeline Kanban"""
    
    def __init__(self, module, db_manager):
        super().__init__()
        self.module = module
        self.db_manager = db_manager
        self.controller = CRMController(db_manager)
        self._setup_ui()
        self.load_leads()
    
    def _setup_ui(self):
        """Configure l'interface style Odoo"""
        # Fond clair
        self.setStyleSheet("background-color: #F9FAFB;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        # Titre
        title = QLabel("🎯 Pipeline CRM")
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: 600;
            color: #202124;
            background-color: transparent;
        """)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Recherche
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍 Rechercher une opportunité...")
        self.search_box.setFixedWidth(300)
        header_layout.addWidget(self.search_box)
        
        # Bouton Nouveau
        new_btn = QPushButton("+ Nouvelle Opportunité")
        new_btn.setObjectName("primaryBtn")
        new_btn.clicked.connect(self.create_new_lead)
        header_layout.addWidget(new_btn)
        
        layout.addLayout(header_layout)
        
        # Stats rapides
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)
        
        stats = self.controller.get_pipeline_stats()
        
        self._add_stat_card(stats_layout, "Opportunités", str(stats.get('total_leads', 0)), "#6750A4")
        self._add_stat_card(stats_layout, "Revenu Attendu", f"{stats.get('expected_revenue', 0):,.0f} DA", "#1E8E3E")
        self._add_stat_card(stats_layout, "Taux Conversion", f"{stats.get('conversion_rate', 0):.1f}%", "#2563EB")
        
        layout.addLayout(stats_layout)
        
        # Zone Kanban avec scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        kanban_widget = QWidget()
        self.kanban_layout = QHBoxLayout(kanban_widget)
        self.kanban_layout.setSpacing(16)
        self.kanban_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        scroll.setWidget(kanban_widget)
        layout.addWidget(scroll)
    
    def _add_stat_card(self, parent_layout, label_text, value_text, color):
        """Ajoute une mini carte de statistique"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #FFFFFF;
                border: 1px solid #DADCE0;
                border-left: 4px solid {color};
                border-radius: 8px;
                padding: 16px;
            }}
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(4)
        
        label = QLabel(label_text)
        label.setStyleSheet("""
            font-size: 11px;
            color: #5F6368;
            font-weight: 600;
            text-transform: uppercase;
        """)
        card_layout.addWidget(label)
        
        value = QLabel(value_text)
        value.setStyleSheet(f"""
            font-size: 24px;
            font-weight: 700;
            color: {color};
        """)
        card_layout.addWidget(value)
        
        parent_layout.addWidget(card)
    
    def load_leads(self):
        """Charge les opportunités dans le pipeline Kanban"""
        # Effacer les colonnes existantes
        while self.kanban_layout.count():
            item = self.kanban_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Charger les étapes
        stages = self.controller.get_all_stages()
        
        for stage in stages:
            # Créer une colonne par étape
            column = self._create_kanban_column(stage)
            self.kanban_layout.addWidget(column)
    
    def _create_kanban_column(self, stage):
        """Crée une colonne Kanban pour une étape"""
        column = QFrame()
        column.setStyleSheet("""
            QFrame {
                background-color: #F9FAFB;
                border: 1px solid #DADCE0;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        column.setMinimumWidth(280)
        column.setMaximumWidth(320)
        
        layout = QVBoxLayout(column)
        layout.setSpacing(12)
        
        # Header de la colonne
        header = QLabel(f"{stage.name}")
        header.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #202124;
            padding: 8px;
            background-color: #E8F0FE;
            border-radius: 4px;
        """)
        layout.addWidget(header)
        
        # Leads de cette étape
        leads = self.controller.get_leads_by_stage(stage.id)
        
        if not leads:
            empty_label = QLabel("Aucune opportunité")
            empty_label.setStyleSheet("color: #9AA0A6; font-style: italic; padding: 20px;")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(empty_label)
        else:
            for lead in leads:
                card = self._create_lead_card(lead)
                layout.addWidget(card)
        
        layout.addStretch()
        
        return column
    
    def _create_lead_card(self, lead):
        """Crée une carte pour une opportunité"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #DADCE0;
                border-radius: 6px;
                padding: 12px;
            }
            QFrame:hover {
                border-color: #6750A4;
                background-color: #FAFBFC;
            }
        """)
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(8)
        
        # Nom de l'opportunité
        name_label = QLabel(lead.name)
        name_label.setStyleSheet("""
            font-size: 13px;
            font-weight: 600;
            color: #202124;
        """)
        name_label.setWordWrap(True)
        layout.addWidget(name_label)
        
        # Client
        if lead.partner_name:
            partner_label = QLabel(f"👤 {lead.partner_name}")
            partner_label.setStyleSheet("font-size: 12px; color: #5F6368;")
            layout.addWidget(partner_label)
        
        # Montant
        amount_label = QLabel(f"💰 {lead.expected_revenue:,.0f} DA")
        amount_label.setStyleSheet("font-size: 13px; color: #1E8E3E; font-weight: 600;")
        layout.addWidget(amount_label)
        
        # Probabilité
        prob_label = QLabel(f"📊 {lead.probability:.0f}%")
        prob_label.setStyleSheet("font-size: 11px; color: #6750A4;")
        layout.addWidget(prob_label)
        
        # Priorité
        priority_colors = {
            'low': '#9AA0A6',
            'medium': '#F9AB00',
            'high': '#D93025'
        }
        priority_label = QLabel(f"⚠️ {lead.priority.capitalize()}")
        priority_label.setStyleSheet(f"font-size: 11px; color: {priority_colors.get(lead.priority, '#9AA0A6')};")
        layout.addWidget(priority_label)
        
        # Clic pour éditer
        card.mousePressEvent = lambda e: self.edit_lead(lead)
        
        return card
    
    def create_new_lead(self):
        """Ouvre le formulaire de création"""
        dialog = LeadFormDialog(self.db_manager, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_leads()
    
    def edit_lead(self, lead):
        """Ouvre le formulaire d'édition"""
        dialog = LeadFormDialog(self.db_manager, lead=lead, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_leads()


class LeadFormDialog(QDialog):
    """Formulaire de création/édition d'opportunité"""
    
    def __init__(self, db_manager, lead=None, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.controller = CRMController(db_manager)
        self.lead = lead if lead else Lead()
        
        self.setWindowTitle("Opportunité CRM")
        self.setMinimumSize(600, 500)
        self._setup_ui()
        
        if lead:
            self._load_lead_data()
    
    def _setup_ui(self):
        """Configure l'interface"""
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Nom de l'opportunité
        self.name_edit = QLineEdit()
        form_layout.addRow("Nom de l'opportunité *:", self.name_edit)
        
        # Client
        self.partner_combo = QComboBox()
        self._load_partners()
        form_layout.addRow("Client:", self.partner_combo)
        
        # Contact
        self.contact_edit = QLineEdit()
        form_layout.addRow("Personne de contact:", self.contact_edit)
        
        # Email
        self.email_edit = QLineEdit()
        form_layout.addRow("Email:", self.email_edit)
        
        # Téléphone
        self.phone_edit = QLineEdit()
        form_layout.addRow("Téléphone:", self.phone_edit)
        
        # Revenu attendu
        self.revenue_spin = QDoubleSpinBox()
        self.revenue_spin.setMaximum(999999999.99)
        self.revenue_spin.setDecimals(2)
        self.revenue_spin.setSuffix(" DA")
        form_layout.addRow("Revenu attendu:", self.revenue_spin)
        
        # Probabilité
        self.probability_spin = QDoubleSpinBox()
        self.probability_spin.setMaximum(100)
        self.probability_spin.setSuffix(" %")
        form_layout.addRow("Probabilité:", self.probability_spin)
        
        # Priorité
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Low", "Medium", "High"])
        self.priority_combo.setCurrentIndex(1)
        form_layout.addRow("Priorité:", self.priority_combo)
        
        # Date limite
        self.deadline_edit = QDateEdit()
        self.deadline_edit.setCalendarPopup(True)
        self.deadline_edit.setDate(QDate.currentDate().addDays(30))
        form_layout.addRow("Date limite:", self.deadline_edit)
        
        # Description
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        form_layout.addRow("Description:", self.description_edit)
        
        layout.addLayout(form_layout)
        
        # Boutons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.setObjectName("secondaryBtn")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("💾 Enregistrer")
        save_btn.setObjectName("primaryBtn")
        save_btn.clicked.connect(self.save_lead)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)
    
    def _load_partners(self):
        """Charge la liste des clients"""
        self.partner_combo.addItem("-- Aucun --", None)
        
        partners = self.db_manager.fetch_all("""
            SELECT id, name FROM res_partner
            WHERE is_customer = 1 AND active = 1
            ORDER BY name
        """)
        
        for partner in partners:
            self.partner_combo.addItem(partner['name'], partner['id'])
    
    def _load_lead_data(self):
        """Charge les données du lead"""
        self.name_edit.setText(self.lead.name)
        
        # Sélectionner le partenaire
        if self.lead.partner_id:
            index = self.partner_combo.findData(self.lead.partner_id)
            if index >= 0:
                self.partner_combo.setCurrentIndex(index)
        
        self.contact_edit.setText(self.lead.contact_name)
        self.email_edit.setText(self.lead.email)
        self.phone_edit.setText(self.lead.phone)
        self.revenue_spin.setValue(self.lead.expected_revenue)
        self.probability_spin.setValue(self.lead.probability)
        
        # Priorité
        priority_index = {"low": 0, "medium": 1, "high": 2}.get(self.lead.priority, 1)
        self.priority_combo.setCurrentIndex(priority_index)
        
        # Date
        if self.lead.date_deadline:
            qdate = QDate(
                self.lead.date_deadline.year,
                self.lead.date_deadline.month,
                self.lead.date_deadline.day
            )
            self.deadline_edit.setDate(qdate)
        
        self.description_edit.setPlainText(self.lead.description)
    
    def save_lead(self):
        """Enregistre l'opportunité"""
        # Validation
        if not self.name_edit.text():
            QMessageBox.warning(self, "Validation", "Le nom de l'opportunité est obligatoire")
            return
        
        # Construire l'objet
        lead = Lead()
        lead.name = self.name_edit.text()
        lead.partner_id = self.partner_combo.currentData()
        lead.contact_name = self.contact_edit.text()
        lead.email = self.email_edit.text()
        lead.phone = self.phone_edit.text()
        lead.expected_revenue = self.revenue_spin.value()
        lead.probability = self.probability_spin.value()
        lead.priority = ["low", "medium", "high"][self.priority_combo.currentIndex()]
        
        # Date
        qdate = self.deadline_edit.date()
        from datetime import datetime
        lead.date_deadline = datetime(qdate.year(), qdate.month(), qdate.day())
        
        lead.description = self.description_edit.toPlainText()
        
        try:
            if self.lead.id:
                # Mise à jour
                lead.id = self.lead.id
                self.controller.update_lead(lead)
                QMessageBox.information(self, "Succès", "Opportunité mise à jour")
            else:
                # Création
                self.controller.create_lead(lead)
                QMessageBox.information(self, "Succès", "Opportunité créée")
            
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur:\n{str(e)}")
