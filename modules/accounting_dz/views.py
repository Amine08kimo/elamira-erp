# -*- coding: utf-8 -*-
"""
Accounting Views - Vues pour la comptabilité DZ
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QPushButton,
    QLabel, QDialog, QFormLayout, QDateEdit, QDoubleSpinBox,
    QTextEdit, QMessageBox, QGroupBox
)
from PyQt6.QtCore import Qt, QDate
from .controller import AccountingController
from .models import G12Declaration
from datetime import datetime


class AccountingMainView(QWidget):
    """Vue principale du module comptabilité avec onglets"""
    
    def __init__(self, module, db_manager):
        super().__init__()
        self.module = module
        self.db_manager = db_manager
        self.controller = AccountingController(db_manager)
        self._setup_ui()
    
    def _setup_ui(self):
        """Configure l'interface avec onglets style Odoo"""
        # Fond clair Odoo
        self.setStyleSheet("background-color: #F9FAFB;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Titre
        title = QLabel("Comptabilité & Finance")
        title.setStyleSheet("font-size: 20px; font-weight: 600;")
        layout.addWidget(title)
        
        # Onglets
        tabs = QTabWidget()
        
        # Onglet PCN
        pcn_view = PCNChartView(self.controller)
        tabs.addTab(pcn_view, "📊 Plan Comptable")
        
        # Onglet Écritures
        moves_view = AccountMoveListView(self.controller)
        tabs.addTab(moves_view, "📝 Écritures")
        
        # Onglet G12
        g12_view = G12DeclarationView(self.controller, self.db_manager)
        tabs.addTab(g12_view, "📋 Déclaration G12")
        
        layout.addWidget(tabs)


class PCNChartView(QWidget):
    """Vue du Plan Comptable National"""
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._setup_ui()
        self.load_accounts()
    
    def _setup_ui(self):
        """Configure l'interface"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Info
        info_label = QLabel("Plan Comptable National Algérien")
        info_label.setStyleSheet("font-weight: 600; font-size: 14px;")
        layout.addWidget(info_label)
        
        # Tableau
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Code", "Nom (FR)", "Nom (AR)", "Type"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)
    
    def load_accounts(self):
        """Charge les comptes PCN"""
        accounts = self.controller.get_all_pcn_accounts()
        
        self.table.setRowCount(len(accounts))
        
        for row_idx, account in enumerate(accounts):
            self.table.setItem(row_idx, 0, QTableWidgetItem(account['code']))
            self.table.setItem(row_idx, 1, QTableWidgetItem(account['name_fr']))
            self.table.setItem(row_idx, 2, QTableWidgetItem(account.get('name_ar', '')))
            self.table.setItem(row_idx, 3, QTableWidgetItem(account['account_type']))


class AccountMoveListView(QWidget):
    """Liste des pièces comptables"""
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._setup_ui()
        self.load_moves()
    
    def _setup_ui(self):
        """Configure l'interface"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        header_layout.addStretch()
        
        new_btn = QPushButton("+ Nouvelle Écriture")
        new_btn.setObjectName("primaryBtn")
        header_layout.addWidget(new_btn)
        
        layout.addLayout(header_layout)
        
        # Tableau
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Numéro", "Date", "Référence", "Total", "État"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)
    
    def load_moves(self):
        """Charge les pièces comptables"""
        moves = self.controller.get_all_moves()
        
        self.table.setRowCount(len(moves))
        
        for row_idx, move in enumerate(moves):
            self.table.setItem(row_idx, 0, QTableWidgetItem(move.name))
            
            date_str = move.date.strftime("%d/%m/%Y") if move.date else ""
            self.table.setItem(row_idx, 1, QTableWidgetItem(date_str))
            
            self.table.setItem(row_idx, 2, QTableWidgetItem(move.ref))
            
            total_item = QTableWidgetItem(f"{move.amount_total:,.2f} DA")
            total_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_idx, 3, total_item)
            
            state_map = {
                'draft': '📝 Brouillon',
                'posted': '✅ Comptabilisée',
                'cancelled': '❌ Annulée'
            }
            self.table.setItem(row_idx, 4, QTableWidgetItem(state_map.get(move.state, move.state)))


class G12DeclarationView(QWidget):
    """Vue pour la déclaration G12 (spécifique DZ)"""
    
    def __init__(self, controller, db_manager):
        super().__init__()
        self.controller = controller
        self.db_manager = db_manager
        self._setup_ui()
        self.load_declarations()
    
    def _setup_ui(self):
        """Configure l'interface"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Info header
        info_box = QLabel(
            "📋 Déclaration G12 - Déclaration mensuelle/trimestrielle de TVA et TAP\n"
            "Conforme aux normes de la DGI (Direction Générale des Impôts)"
        )
        info_box.setStyleSheet("""
            QLabel {
                background: #EEF2FF;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #667eea;
                color: #1E40AF;
            }
        """)
        layout.addWidget(info_box)
        
        # Boutons d'action
        actions_layout = QHBoxLayout()
        actions_layout.addStretch()
        
        generate_btn = QPushButton("🔄 Générer depuis factures")
        generate_btn.setObjectName("secondaryBtn")
        generate_btn.clicked.connect(self.generate_from_sales)
        actions_layout.addWidget(generate_btn)
        
        new_btn = QPushButton("+ Nouvelle Déclaration")
        new_btn.setObjectName("primaryBtn")
        new_btn.clicked.connect(self.create_new_declaration)
        actions_layout.addWidget(new_btn)
        
        layout.addLayout(actions_layout)
        
        # Liste des déclarations
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Numéro", "Période", "CA HT", "TVA à payer", "TAP", "État"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.doubleClicked.connect(self.view_declaration)
        layout.addWidget(self.table)
    
    def load_declarations(self):
        """Charge les déclarations G12"""
        declarations = self.controller.get_all_g12_declarations()
        
        self.table.setRowCount(len(declarations))
        
        for row_idx, decl in enumerate(declarations):
            self.table.setItem(row_idx, 0, QTableWidgetItem(decl.name))
            
            period = f"{decl.period_start.strftime('%d/%m/%Y')} - {decl.period_end.strftime('%d/%m/%Y')}"
            self.table.setItem(row_idx, 1, QTableWidgetItem(period))
            
            ca_item = QTableWidgetItem(f"{decl.ca_ht:,.2f} DA")
            ca_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_idx, 2, ca_item)
            
            tva_item = QTableWidgetItem(f"{decl.tva_a_payer:,.2f} DA")
            tva_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_idx, 3, tva_item)
            
            tap_item = QTableWidgetItem(f"{decl.tap_amount:,.2f} DA")
            tap_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_idx, 4, tap_item)
            
            state_map = {'draft': '📝 Brouillon', 'submitted': '✅ Soumise'}
            self.table.setItem(row_idx, 5, QTableWidgetItem(state_map.get(decl.state, decl.state)))
            
            # Stocker l'ID dans la ligne
            self.table.item(row_idx, 0).setData(Qt.ItemDataRole.UserRole, decl.id)
    
    def create_new_declaration(self):
        """Ouvre le formulaire de création"""
        dialog = G12FormDialog(self.controller, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_declarations()
    
    def generate_from_sales(self):
        """Génère une déclaration depuis les factures"""
        dialog = G12GenerateDialog(self.controller, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_declarations()
    
    def view_declaration(self, index):
        """Affiche les détails d'une déclaration"""
        row = index.row()
        decl_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        # TODO: Ouvrir un dialog avec les détails


class G12FormDialog(QDialog):
    """Formulaire de déclaration G12"""
    
    def __init__(self, controller, declaration=None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.declaration = declaration if declaration else G12Declaration()
        
        self.setWindowTitle("Déclaration G12")
        self.setMinimumSize(700, 800)
        self._setup_ui()
    
    def _setup_ui(self):
        """Configure l'interface"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Période
        period_group = QGroupBox("📅 Période de Déclaration")
        period_layout = QFormLayout(period_group)
        
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate().addMonths(-1))
        period_layout.addRow("Date de début:", self.start_date_edit)
        
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(QDate.currentDate())
        period_layout.addRow("Date de fin:", self.end_date_edit)
        
        layout.addWidget(period_group)
        
        # Chiffre d'affaires
        ca_group = QGroupBox("💰 Chiffre d'Affaires")
        ca_layout = QFormLayout(ca_group)
        
        self.ca_ht_spin = QDoubleSpinBox()
        self.ca_ht_spin.setMaximum(999999999999.99)
        self.ca_ht_spin.setDecimals(2)
        self.ca_ht_spin.setSuffix(" DA")
        ca_layout.addRow("CA HT:", self.ca_ht_spin)
        
        self.ca_exonere_spin = QDoubleSpinBox()
        self.ca_exonere_spin.setMaximum(999999999999.99)
        self.ca_exonere_spin.setDecimals(2)
        self.ca_exonere_spin.setSuffix(" DA")
        ca_layout.addRow("CA Exonéré:", self.ca_exonere_spin)
        
        layout.addWidget(ca_group)
        
        # TVA Collectée
        tva_col_group = QGroupBox("📊 TVA Collectée")
        tva_col_layout = QFormLayout(tva_col_group)
        
        self.tva_19_base_spin = QDoubleSpinBox()
        self.tva_19_base_spin.setMaximum(999999999999.99)
        self.tva_19_base_spin.setDecimals(2)
        self.tva_19_base_spin.setSuffix(" DA")
        tva_col_layout.addRow("Base TVA 19%:", self.tva_19_base_spin)
        
        self.tva_9_base_spin = QDoubleSpinBox()
        self.tva_9_base_spin.setMaximum(999999999999.99)
        self.tva_9_base_spin.setDecimals(2)
        self.tva_9_base_spin.setSuffix(" DA")
        tva_col_layout.addRow("Base TVA 9%:", self.tva_9_base_spin)
        
        layout.addWidget(tva_col_group)
        
        # TVA Déductible
        tva_ded_group = QGroupBox("📉 TVA Déductible")
        tva_ded_layout = QFormLayout(tva_ded_group)
        
        self.tva_ded_immo_spin = QDoubleSpinBox()
        self.tva_ded_immo_spin.setMaximum(999999999999.99)
        self.tva_ded_immo_spin.setDecimals(2)
        self.tva_ded_immo_spin.setSuffix(" DA")
        tva_ded_layout.addRow("Sur Immobilisations:", self.tva_ded_immo_spin)
        
        self.tva_ded_biens_spin = QDoubleSpinBox()
        self.tva_ded_biens_spin.setMaximum(999999999999.99)
        self.tva_ded_biens_spin.setDecimals(2)
        self.tva_ded_biens_spin.setSuffix(" DA")
        tva_ded_layout.addRow("Sur Biens:", self.tva_ded_biens_spin)
        
        self.tva_ded_services_spin = QDoubleSpinBox()
        self.tva_ded_services_spin.setMaximum(999999999999.99)
        self.tva_ded_services_spin.setDecimals(2)
        self.tva_ded_services_spin.setSuffix(" DA")
        tva_ded_layout.addRow("Sur Services:", self.tva_ded_services_spin)
        
        layout.addWidget(tva_ded_group)
        
        # Boutons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        calc_btn = QPushButton("🧮 Calculer")
        calc_btn.setObjectName("secondaryBtn")
        calc_btn.clicked.connect(self.calculate_preview)
        buttons_layout.addWidget(calc_btn)
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.setObjectName("secondaryBtn")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("💾 Enregistrer")
        save_btn.setObjectName("primaryBtn")
        save_btn.clicked.connect(self.save_declaration)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)
    
    def calculate_preview(self):
        """Calcule et affiche un aperçu"""
        decl = self._build_declaration()
        decl.calculate_totals()
        
        msg = f"""
RÉCAPITULATIF G12

Chiffre d'Affaires Total: {decl.ca_total:,.2f} DA

TVA Collectée: {decl.tva_collectee_total:,.2f} DA
TVA Déductible: {decl.tva_deductible_total:,.2f} DA
TVA Due: {decl.tva_due:,.2f} DA

TVA à Payer: {decl.tva_a_payer:,.2f} DA

TAP ({decl.tap_rate}%): {decl.tap_amount:,.2f} DA
        """
        
        QMessageBox.information(self, "Calcul G12", msg)
    
    def _build_declaration(self) -> G12Declaration:
        """Construit l'objet déclaration depuis le formulaire"""
        decl = G12Declaration()
        
        start = self.start_date_edit.date()
        decl.period_start = datetime(start.year(), start.month(), start.day())
        
        end = self.end_date_edit.date()
        decl.period_end = datetime(end.year(), end.month(), end.day())
        
        decl.ca_ht = self.ca_ht_spin.value()
        decl.ca_exonere = self.ca_exonere_spin.value()
        decl.tva_19_base = self.tva_19_base_spin.value()
        decl.tva_9_base = self.tva_9_base_spin.value()
        decl.tva_deductible_immobilisations = self.tva_ded_immo_spin.value()
        decl.tva_deductible_biens = self.tva_ded_biens_spin.value()
        decl.tva_deductible_services = self.tva_ded_services_spin.value()
        
        return decl
    
    def save_declaration(self):
        """Enregistre la déclaration"""
        try:
            decl = self._build_declaration()
            decl_id = self.controller.create_g12_declaration(decl)
            
            QMessageBox.information(
                self,
                "Succès",
                f"Déclaration G12 créée avec succès!\nNuméro: {decl.name}"
            )
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur:\n{str(e)}")


class G12GenerateDialog(QDialog):
    """Dialog pour générer automatiquement une G12"""
    
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        
        self.setWindowTitle("Générer G12 depuis les factures")
        self.setMinimumSize(400, 200)
        self._setup_ui()
    
    def _setup_ui(self):
        """Configure l'interface"""
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate().addMonths(-1))
        form_layout.addRow("Date de début:", self.start_date_edit)
        
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(QDate.currentDate())
        form_layout.addRow("Date de fin:", self.end_date_edit)
        
        layout.addLayout(form_layout)
        
        # Boutons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        generate_btn = QPushButton("🔄 Générer")
        generate_btn.setObjectName("primaryBtn")
        generate_btn.clicked.connect(self.generate)
        buttons_layout.addWidget(generate_btn)
        
        layout.addLayout(buttons_layout)
    
    def generate(self):
        """Génère la déclaration"""
        start = self.start_date_edit.date()
        period_start = datetime(start.year(), start.month(), start.day())
        
        end = self.end_date_edit.date()
        period_end = datetime(end.year(), end.month(), end.day())
        
        try:
            decl = self.controller.generate_g12_from_sales(period_start, period_end)
            decl_id = self.controller.create_g12_declaration(decl)
            
            QMessageBox.information(
                self,
                "Succès",
                f"Déclaration G12 générée!\n\nCA HT: {decl.ca_ht:,.2f} DA\nTVA à payer: {decl.tva_a_payer:,.2f} DA"
            )
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur:\n{str(e)}")
