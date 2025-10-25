# -*- coding: utf-8 -*-
"""
Sales Views - Vues pour le module Ventes
Interface style Odoo
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableView, QPushButton,
    QLineEdit, QLabel, QDialog, QFormLayout, QComboBox,
    QDateEdit, QTextEdit, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QSpinBox, QDoubleSpinBox
)
from PyQt6.QtCore import Qt, QDate, QAbstractTableModel, QModelIndex
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from .controller import SalesController
from .models import SaleOrder, SaleOrderLine
from datetime import datetime


class SaleOrderListView(QWidget):
    """Vue liste des commandes de vente (style Odoo)"""
    
    def __init__(self, module, db_manager):
        super().__init__()
        self.module = module
        self.db_manager = db_manager
        self.controller = SalesController(db_manager)
        self._setup_ui()
        self.load_orders()
    
    def _setup_ui(self):
        """Configure l'interface style Odoo"""
        # Fond clair Odoo
        self.setStyleSheet("background-color: #F9FAFB;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Header avec boutons d'action
        header_layout = QHBoxLayout()
        
        # Barre de recherche
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍 Rechercher une facture...")
        self.search_box.setFixedWidth(300)
        header_layout.addWidget(self.search_box)
        
        header_layout.addStretch()
        
        # Bouton Nouveau
        new_btn = QPushButton("+ Nouvelle Facture")
        new_btn.setObjectName("primaryBtn")
        new_btn.clicked.connect(self.create_new_order)
        header_layout.addWidget(new_btn)
        
        layout.addLayout(header_layout)
        
        # Tableau des commandes
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Numéro", "Client", "Date", "Total HT", "Total TTC", "État", "Actions"
        ])
        
        # Configurer le tableau
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.table)
    
    def load_orders(self):
        """Charge les commandes depuis la base de données"""
        orders = self.controller.get_all_orders()
        
        self.table.setRowCount(len(orders))
        
        for row_idx, order in enumerate(orders):
            # Numéro
            self.table.setItem(row_idx, 0, QTableWidgetItem(order.name))
            
            # Client
            partner = self.controller.get_partner(order.partner_id)
            partner_name = partner.name if partner else f"ID: {order.partner_id}"
            self.table.setItem(row_idx, 1, QTableWidgetItem(partner_name))
            
            # Date
            date_str = order.date_order.strftime("%d/%m/%Y") if order.date_order else ""
            self.table.setItem(row_idx, 2, QTableWidgetItem(date_str))
            
            # Total HT
            ht_item = QTableWidgetItem(f"{order.amount_untaxed:,.2f} DA")
            ht_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_idx, 3, ht_item)
            
            # Total TTC
            ttc_item = QTableWidgetItem(f"{order.amount_total:,.2f} DA")
            ttc_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_idx, 4, ttc_item)
            
            # État
            state_map = {
                'draft': '📝 Brouillon',
                'confirmed': '✅ Confirmée',
                'done': '✓ Terminée',
                'cancelled': '❌ Annulée'
            }
            self.table.setItem(row_idx, 5, QTableWidgetItem(state_map.get(order.state, order.state)))
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 0, 5, 0)
            
            view_btn = QPushButton("👁")
            view_btn.setToolTip("Voir")
            view_btn.setFixedWidth(30)
            view_btn.clicked.connect(lambda checked, o=order: self.view_order(o))
            actions_layout.addWidget(view_btn)
            
            self.table.setCellWidget(row_idx, 6, actions_widget)
    
    def create_new_order(self):
        """Ouvre le formulaire de création"""
        dialog = SaleOrderFormDialog(self.db_manager, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_orders()  # Recharger la liste
    
    def view_order(self, order):
        """Affiche les détails d'une commande"""
        dialog = SaleOrderFormDialog(self.db_manager, order=order, parent=self)
        dialog.exec()


class SaleOrderFormDialog(QDialog):
    """Formulaire de création/édition d'une commande de vente"""
    
    def __init__(self, db_manager, order=None, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.controller = SalesController(db_manager)
        self.order = order if order else SaleOrder()
        self.order_lines = self.order.order_lines if order else []
        
        self.setWindowTitle("Facture de Vente")
        self.setMinimumSize(900, 700)
        self._setup_ui()
        
        if order:
            self._load_order_data()
    
    def _setup_ui(self):
        """Configure l'interface du formulaire"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # === EN-TÊTE ===
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Client
        self.customer_combo = QComboBox()
        partners = self.controller.get_all_partners(is_customer=True)
        for partner in partners:
            self.customer_combo.addItem(f"{partner.name} (NIF: {partner.nif})", partner.id)
        form_layout.addRow("Client *:", self.customer_combo)
        
        # Date
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        form_layout.addRow("Date:", self.date_edit)
        
        # Date d'échéance
        self.due_date_edit = QDateEdit()
        self.due_date_edit.setCalendarPopup(True)
        self.due_date_edit.setDate(QDate.currentDate().addDays(30))
        form_layout.addRow("Date d'échéance:", self.due_date_edit)
        
        layout.addLayout(form_layout)
        
        # === LIGNES DE COMMANDE ===
        lines_label = QLabel("Lignes de la facture:")
        lines_label.setStyleSheet("font-weight: 600; font-size: 14px;")
        layout.addWidget(lines_label)
        
        # Tableau des lignes
        self.lines_table = QTableWidget()
        self.lines_table.setColumnCount(7)
        self.lines_table.setHorizontalHeaderLabels([
            "Produit", "Description", "Qté", "Prix Unit. (DA)", "TVA %", "Total HT", ""
        ])
        self.lines_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.lines_table.setMinimumHeight(250)
        layout.addWidget(self.lines_table)
        
        # Bouton Ajouter ligne
        add_line_btn = QPushButton("+ Ajouter une ligne")
        add_line_btn.setObjectName("secondaryBtn")
        add_line_btn.clicked.connect(self.add_line)
        layout.addWidget(add_line_btn)
        
        # === TOTAUX ===
        totals_frame = QWidget()
        totals_frame.setStyleSheet("""
            QWidget {
                background: #F9FAFB;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        totals_layout = QFormLayout(totals_frame)
        
        self.total_ht_label = QLabel("0.00 DA")
        self.total_ht_label.setStyleSheet("font-weight: 600;")
        totals_layout.addRow("Total HT:", self.total_ht_label)
        
        self.total_tva_label = QLabel("0.00 DA")
        totals_layout.addRow("Total TVA:", self.total_tva_label)
        
        self.total_ttc_label = QLabel("0.00 DA")
        self.total_ttc_label.setStyleSheet("font-size: 18px; font-weight: 700; color: #667eea;")
        totals_layout.addRow("Total TTC:", self.total_ttc_label)
        
        layout.addWidget(totals_frame)
        
        # === NOTES ===
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Notes et conditions de paiement...")
        self.notes_edit.setMaximumHeight(80)
        layout.addWidget(QLabel("Notes:"))
        layout.addWidget(self.notes_edit)
        
        # === BOUTONS D'ACTION ===
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.setObjectName("secondaryBtn")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("💾 Enregistrer")
        save_btn.setObjectName("primaryBtn")
        save_btn.clicked.connect(self.save_order)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)
    
    def add_line(self):
        """Ajoute une ligne vide au tableau"""
        row = self.lines_table.rowCount()
        self.lines_table.insertRow(row)
        
        # Produit
        product_edit = QLineEdit()
        product_edit.setPlaceholderText("Nom du produit")
        self.lines_table.setCellWidget(row, 0, product_edit)
        
        # Description
        desc_edit = QLineEdit()
        self.lines_table.setCellWidget(row, 1, desc_edit)
        
        # Quantité
        qty_spin = QDoubleSpinBox()
        qty_spin.setMinimum(0.01)
        qty_spin.setValue(1.0)
        qty_spin.valueChanged.connect(self.calculate_totals)
        self.lines_table.setCellWidget(row, 2, qty_spin)
        
        # Prix unitaire
        price_spin = QDoubleSpinBox()
        price_spin.setMaximum(999999999.99)
        price_spin.setDecimals(2)
        price_spin.valueChanged.connect(self.calculate_totals)
        self.lines_table.setCellWidget(row, 3, price_spin)
        
        # TVA
        tax_combo = QComboBox()
        tax_combo.addItem("0%", 0.0)
        tax_combo.addItem("9%", 9.0)
        tax_combo.addItem("19%", 19.0)
        tax_combo.currentIndexChanged.connect(self.calculate_totals)
        self.lines_table.setCellWidget(row, 4, tax_combo)
        
        # Total HT (calculé)
        self.lines_table.setItem(row, 5, QTableWidgetItem("0.00 DA"))
        
        # Bouton Supprimer
        del_btn = QPushButton("🗑")
        del_btn.setFixedWidth(30)
        del_btn.clicked.connect(lambda: self.remove_line(row))
        self.lines_table.setCellWidget(row, 6, del_btn)
        
        self.calculate_totals()
    
    def remove_line(self, row):
        """Supprime une ligne"""
        self.lines_table.removeRow(row)
        self.calculate_totals()
    
    def calculate_totals(self):
        """Calcule et met à jour les totaux"""
        total_ht = 0.0
        total_tva = 0.0
        
        for row in range(self.lines_table.rowCount()):
            qty_widget = self.lines_table.cellWidget(row, 2)
            price_widget = self.lines_table.cellWidget(row, 3)
            tax_widget = self.lines_table.cellWidget(row, 4)
            
            if qty_widget and price_widget and tax_widget:
                qty = qty_widget.value()
                price = price_widget.value()
                tax_rate = tax_widget.currentData()
                
                line_ht = qty * price
                line_tva = line_ht * (tax_rate / 100)
                
                total_ht += line_ht
                total_tva += line_tva
                
                # Mettre à jour le total de la ligne
                total_item = self.lines_table.item(row, 5)
                if total_item:
                    total_item.setText(f"{line_ht:,.2f} DA")
        
        total_ttc = total_ht + total_tva
        
        self.total_ht_label.setText(f"{total_ht:,.2f} DA")
        self.total_tva_label.setText(f"{total_tva:,.2f} DA")
        self.total_ttc_label.setText(f"{total_ttc:,.2f} DA")
    
    def _load_order_data(self):
        """Charge les données d'une commande existante"""
        # Charger le client
        for i in range(self.customer_combo.count()):
            if self.customer_combo.itemData(i) == self.order.partner_id:
                self.customer_combo.setCurrentIndex(i)
                break
        
        # Charger les dates
        if self.order.date_order:
            self.date_edit.setDate(QDate(
                self.order.date_order.year,
                self.order.date_order.month,
                self.order.date_order.day
            ))
        
        # Charger les lignes
        for line in self.order.order_lines:
            row = self.lines_table.rowCount()
            self.lines_table.insertRow(row)
            
            # Créer les widgets et les peupler
            # (code similaire à add_line mais avec les valeurs)
            self.lines_table.setItem(row, 0, QTableWidgetItem(line.product_name))
        
        # Charger les notes
        self.notes_edit.setPlainText(self.order.notes)
        
        self.calculate_totals()
    
    def save_order(self):
        """Enregistre la commande"""
        # Valider
        if self.customer_combo.currentIndex() == -1:
            QMessageBox.warning(self, "Validation", "Veuillez sélectionner un client")
            return
        
        if self.lines_table.rowCount() == 0:
            QMessageBox.warning(self, "Validation", "Veuillez ajouter au moins une ligne")
            return
        
        # Construire l'objet SaleOrder
        order = SaleOrder()
        order.partner_id = self.customer_combo.currentData()
        
        date = self.date_edit.date()
        order.date_order = datetime(date.year(), date.month(), date.day())
        
        due_date = self.due_date_edit.date()
        order.date_due = datetime(due_date.year(), due_date.month(), due_date.day())
        
        order.notes = self.notes_edit.toPlainText()
        order.state = 'draft'
        
        # Construire les lignes
        for row in range(self.lines_table.rowCount()):
            product_widget = self.lines_table.cellWidget(row, 0)
            desc_widget = self.lines_table.cellWidget(row, 1)
            qty_widget = self.lines_table.cellWidget(row, 2)
            price_widget = self.lines_table.cellWidget(row, 3)
            tax_widget = self.lines_table.cellWidget(row, 4)
            
            if qty_widget and price_widget:
                line = SaleOrderLine()
                line.product_name = product_widget.text() if hasattr(product_widget, 'text') else ""
                line.description = desc_widget.text() if hasattr(desc_widget, 'text') else ""
                line.quantity = qty_widget.value()
                line.price_unit = price_widget.value()
                line.tax_rate = tax_widget.currentData() if tax_widget else 0.0
                
                order.order_lines.append(line)
        
        # Enregistrer
        try:
            order_id = self.controller.create_sale_order(order)
            QMessageBox.information(
                self,
                "Succès",
                f"Facture créée avec succès!\nNuméro: {order.name}"
            )
            self.accept()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erreur",
                f"Erreur lors de l'enregistrement:\n{str(e)}"
            )
