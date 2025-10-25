# -*- coding: utf-8 -*-
"""
CRM Views V2 - ULTRA LISIBLE ET CLIQUABLE
Pipeline CRM Professionnel avec Design Moderne
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
    """Vue CRM V2 - Moderne, Lisible, Cliquable"""
    
    def __init__(self, module, db_manager):
        super().__init__()
        self.module = module
        self.db_manager = db_manager
        self.controller = CRMController(db_manager)
        self._setup_ui()
        self.load_leads()
    
    def _setup_ui(self):
        """Configure l'interface CRM ultra-lisible"""
        self.setStyleSheet("background-color: #F5F5F5;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(28)
        
        # ===== HEADER AVEC TITRE ET ACTIONS =====
        header_layout = QHBoxLayout()
        header_layout.setSpacing(20)
        
        # Titre GRAND avec icône
        title = QLabel("🎯 Pipeline CRM")
        title.setStyleSheet("""
            font-size: 32px;
            font-weight: 700;
            color: #1A1A1A;
            background-color: transparent;
            padding: 0px;
        """)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Recherche GRANDE
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍 Rechercher une opportunité...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                border: 2px solid #D0D0D0;
                border-radius: 8px;
                padding: 14px 18px;
                font-size: 16px;
                min-width: 350px;
                min-height: 24px;
            }
            QLineEdit:focus {
                border-color: #6750A4;
            }
        """)
        header_layout.addWidget(self.search_box)
        
        # Bouton Nouveau - GRAND et CLIQUABLE
        new_btn = QPushButton("+ Nouveau")
        new_btn.setObjectName("newBtn")
        new_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        new_btn.setStyleSheet("""
            QPushButton {
                background-color: #6750A4;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 16px 36px;
                font-size: 17px;
                font-weight: 700;
                min-height: 52px;
                min-width: 140px;
            }
            QPushButton:hover {
                background-color: #5746A6;
            }
            QPushButton:pressed {
                background-color: #4B3C96;
            }
        """)
        new_btn.clicked.connect(self.create_new_lead)
        header_layout.addWidget(new_btn)
        
        layout.addLayout(header_layout)
        
        # ===== STATISTIQUES - GRANDES ET LISIBLES =====
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        
        stats = self.controller.get_pipeline_stats()
        
        self._add_stat_card(
            stats_layout,
            "OPPORTUNITÉS",
            str(stats.get('total_leads', 0)),
            "#6750A4"
        )
        
        self._add_stat_card(
            stats_layout,
            "REVENU ATTENDU",
            f"{stats.get('expected_revenue', 0):,.0f} DA",
            "#1E8E3E"
        )
        
        self._add_stat_card(
            stats_layout,
            "TAUX CONVERSION",
            f"{stats.get('conversion_rate', 0):.1f}%",
            "#2563EB"
        )
        
        layout.addLayout(stats_layout)
        
        # ===== PIPELINE KANBAN =====
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        kanban_widget = QWidget()
        kanban_widget.setStyleSheet("background-color: transparent;")
        self.kanban_layout = QHBoxLayout(kanban_widget)
        self.kanban_layout.setSpacing(20)
        self.kanban_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        scroll.setWidget(kanban_widget)
        layout.addWidget(scroll)
    
    def _add_stat_card(self, parent_layout, label_text, value_text, color):
        """Carte statistique GRANDE et lisible"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #FFFFFF;
                border: 3px solid #E0E0E0;
                border-left: 6px solid {color};
                border-radius: 10px;
                padding: 24px 28px;
                min-height: 100px;
            }}
            QFrame:hover {{
                border-color: {color};
                background-color: #FAFAFA;
            }}
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(10)
        
        # Label
        label = QLabel(label_text)
        label.setStyleSheet("""
            font-size: 13px;
            color: #5F6368;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            background-color: transparent;
        """)
        card_layout.addWidget(label)
        
        # Valeur GRANDE
        value = QLabel(value_text)
        value.setStyleSheet(f"""
            font-size: 36px;
            font-weight: 700;
            color: {color};
            background-color: transparent;
        """)
        card_layout.addWidget(value)
        
        parent_layout.addWidget(card)
    
    def load_leads(self):
        """Charge les opportunités dans le pipeline"""
        # Effacer colonnes existantes
        while self.kanban_layout.count():
            item = self.kanban_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Charger étapes
        stages = self.controller.get_all_stages()
        
        for stage in stages:
            column = self._create_kanban_column(stage)
            self.kanban_layout.addWidget(column)
    
    def _create_kanban_column(self, stage):
        """Crée une colonne Kanban LISIBLE"""
        column = QFrame()
        column.setMinimumWidth(320)
        column.setMaximumWidth(400)
        column.setStyleSheet("""
            QFrame {
                background-color: #F9F9F9;
                border: 2px solid #E0E0E0;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        column_layout = QVBoxLayout(column)
        column_layout.setSpacing(16)
        
        # Header de colonne
        header_layout = QHBoxLayout()
        
        # Nom de l'étape GRAND
        stage_name = QLabel(stage['name'])
        stage_name.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #1A1A1A;
            background-color: transparent;
        """)
        header_layout.addWidget(stage_name)
        
        header_layout.addStretch()
        
        # Compteur
        leads = self.controller.get_leads_by_stage(stage['id'])
        count_label = QLabel(str(len(leads)))
        count_label.setStyleSheet("""
            background-color: #6750A4;
            color: white;
            font-size: 15px;
            font-weight: 700;
            padding: 6px 12px;
            border-radius: 16px;
            min-width: 32px;
        """)
        count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(count_label)
        
        column_layout.addLayout(header_layout)
        
        # Bouton Nouveau CLIQUABLE
        new_lead_btn = QPushButton("+ Nouveau")
        new_lead_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        new_lead_btn.setStyleSheet("""
            QPushButton {
                background-color: #E8F0FE;
                color: #6750A4;
                border: 2px dashed #6750A4;
                border-radius: 8px;
                padding: 14px;
                font-size: 15px;
                font-weight: 700;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #D2E3FC;
                border-style: solid;
            }
        """)
        new_lead_btn.clicked.connect(lambda: self.create_new_lead(stage['id']))
        column_layout.addWidget(new_lead_btn)
        
        # Cartes des opportunités
        if not leads:
            empty_label = QLabel("Aucune opportunité")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setStyleSheet("""
                color: #9AA0A6;
                font-size: 15px;
                font-style: italic;
                padding: 40px 20px;
                background-color: transparent;
            """)
            column_layout.addWidget(empty_label)
        else:
            for lead in leads:
                lead_card = self._create_lead_card(lead)
                column_layout.addWidget(lead_card)
        
        column_layout.addStretch()
        
        return column
    
    def _create_lead_card(self, lead):
        """Crée une carte opportunité LISIBLE et CLIQUABLE"""
        card = QFrame()
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 2px solid #D0D0D0;
                border-radius: 8px;
                padding: 18px;
            }
            QFrame:hover {
                border-color: #6750A4;
                background-color: #FAFAFA;
            }
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(12)
        
        # Nom du lead GRAND
        name_label = QLabel(lead.name)
        name_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 700;
            color: #1A1A1A;
            background-color: transparent;
        """)
        name_label.setWordWrap(True)
        card_layout.addWidget(name_label)
        
        # Client
        if lead.partner_name:
            client_label = QLabel(f"👤 {lead.partner_name}")
            client_label.setStyleSheet("""
                font-size: 14px;
                color: #5F6368;
                background-color: transparent;
            """)
            card_layout.addWidget(client_label)
        
        # Montant GRAND
        if lead.expected_revenue > 0:
            amount_label = QLabel(f"💰 {lead.expected_revenue:,.0f} DA")
            amount_label.setStyleSheet("""
                font-size: 17px;
                font-weight: 700;
                color: #1E8E3E;
                background-color: transparent;
                padding: 8px 0px;
            """)
            card_layout.addWidget(amount_label)
        
        # Probabilité
        if lead.probability > 0:
            prob_label = QLabel(f"📊 {lead.probability}% de probabilité")
            prob_label.setStyleSheet("""
                font-size: 13px;
                color: #2563EB;
                font-weight: 600;
                background-color: transparent;
            """)
            card_layout.addWidget(prob_label)
        
        # Boutons d'action
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(8)
        
        # Bouton Voir
        view_btn = QPushButton("👁 Voir")
        view_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        view_btn.setStyleSheet("""
            QPushButton {
                background-color: #6750A4;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 16px;
                font-size: 14px;
                font-weight: 600;
                min-height: 36px;
            }
            QPushButton:hover {
                background-color: #5746A6;
            }
        """)
        view_btn.clicked.connect(lambda: self.view_lead(lead))
        actions_layout.addWidget(view_btn)
        
        card_layout.addLayout(actions_layout)
        
        return card
    
    def create_new_lead(self, stage_id=None):
        """Ouvre le dialogue de création d'opportunité"""
        dialog = LeadDialog(self, stage_id)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            lead_data = dialog.get_lead_data()
            self.controller.create_lead(lead_data)
            self.load_leads()
            QMessageBox.information(self, "Succès", "Opportunité créée avec succès!")
    
    def view_lead(self, lead):
        """Affiche les détails de l'opportunité"""
        dialog = LeadDialog(self, lead=lead)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            lead_data = dialog.get_lead_data()
            self.controller.update_lead(lead.id, lead_data)
            self.load_leads()
            QMessageBox.information(self, "Succès", "Opportunité mise à jour!")


class LeadDialog(QDialog):
    """Dialogue de création/édition d'opportunité - LISIBLE"""
    
    def __init__(self, parent=None, stage_id=None, lead=None):
        super().__init__(parent)
        self.stage_id = stage_id
        self.lead = lead
        self.controller = parent.controller
        self._setup_ui()
        if lead:
            self._fill_data()
    
    def _setup_ui(self):
        """Configure le dialogue"""
        self.setWindowTitle("✨ Nouvelle Opportunité" if not self.lead else "✏ Modifier Opportunité")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Formulaire
        form = QFormLayout()
        form.setSpacing(16)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Champs GRANDS
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ex: Vente machines à coudre")
        self.name_input.setStyleSheet("font-size: 15px; padding: 12px;")
        form.addRow("📋 Nom:", self.name_input)
        
        self.partner_combo = QComboBox()
        self.partner_combo.setStyleSheet("font-size: 15px; padding: 10px;")
        self._load_partners()
        form.addRow("👤 Client:", self.partner_combo)
        
        self.revenue_input = QDoubleSpinBox()
        self.revenue_input.setMaximum(999999999)
        self.revenue_input.setSuffix(" DA")
        self.revenue_input.setStyleSheet("font-size: 15px; padding: 12px;")
        form.addRow("💰 Montant:", self.revenue_input)
        
        self.probability_input = QDoubleSpinBox()
        self.probability_input.setMaximum(100)
        self.probability_input.setSuffix(" %")
        self.probability_input.setValue(50)
        self.probability_input.setStyleSheet("font-size: 15px; padding: 12px;")
        form.addRow("📊 Probabilité:", self.probability_input)
        
        self.stage_combo = QComboBox()
        self.stage_combo.setStyleSheet("font-size: 15px; padding: 10px;")
        self._load_stages()
        form.addRow("📍 Étape:", self.stage_combo)
        
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Notes et commentaires...")
        self.notes_input.setMaximumHeight(120)
        self.notes_input.setStyleSheet("font-size: 15px; padding: 12px;")
        form.addRow("📝 Notes:", self.notes_input)
        
        layout.addLayout(form)
        
        # Boutons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #F5F5F5;
                border: 2px solid #D0D0D0;
                border-radius: 6px;
                padding: 12px 24px;
                font-size: 15px;
                font-weight: 600;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("💾 Enregistrer")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #6750A4;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 28px;
                font-size: 15px;
                font-weight: 700;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #5746A6;
            }
        """)
        save_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)
    
    def _load_partners(self):
        """Charge les clients"""
        partners = self.controller.db_manager.fetch_all("""
            SELECT id, name FROM res_partner
            WHERE is_customer = 1 AND active = 1
            ORDER BY name
        """)
        
        self.partner_combo.addItem("-- Sélectionner un client --", None)
        for partner in partners:
            self.partner_combo.addItem(partner['name'], partner['id'])
    
    def _load_stages(self):
        """Charge les étapes"""
        stages = self.controller.get_all_stages()
        
        for idx, stage in enumerate(stages):
            self.stage_combo.addItem(stage['name'], stage['id'])
            if self.stage_id and stage['id'] == self.stage_id:
                self.stage_combo.setCurrentIndex(idx)
    
    def _fill_data(self):
        """Remplit les données si édition"""
        if not self.lead:
            return
        
        self.name_input.setText(self.lead.name)
        self.revenue_input.setValue(self.lead.expected_revenue)
        self.probability_input.setValue(self.lead.probability)
        self.notes_input.setPlainText(self.lead.notes or "")
        
        # Sélectionner client
        for i in range(self.partner_combo.count()):
            if self.partner_combo.itemData(i) == self.lead.partner_id:
                self.partner_combo.setCurrentIndex(i)
                break
        
        # Sélectionner étape
        for i in range(self.stage_combo.count()):
            if self.stage_combo.itemData(i) == self.lead.stage_id:
                self.stage_combo.setCurrentIndex(i)
                break
    
    def get_lead_data(self):
        """Récupère les données du formulaire"""
        return {
            'name': self.name_input.text(),
            'partner_id': self.partner_combo.currentData(),
            'expected_revenue': self.revenue_input.value(),
            'probability': self.probability_input.value(),
            'stage_id': self.stage_combo.currentData(),
            'notes': self.notes_input.toPlainText()
        }
