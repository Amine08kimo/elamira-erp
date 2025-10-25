# -*- coding: utf-8 -*-
"""
Purchase Views - Vues du module Achats
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QHeaderView, QDialog, QFormLayout, QComboBox,
    QDoubleSpinBox, QTextEdit, QDateEdit, QSpinBox,
    QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
from .controller import PurchaseController
from .models import PurchaseOrder, PurchaseOrderLine


class PurchaseOrderListView(QWidget):
    """Vue liste des commandes d'achat"""
    
    def __init__(self, module, db_manager):
        super().__init__()
        self.module = module
        self.db_manager = db_manager
        self.controller = PurchaseController(db_manager)
        self._setup_ui()
        self.load_purchase_orders()
    
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
        title = QLabel("🛒 Achats Fournisseurs")
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
        self.search_box.setPlaceholderText("🔍 Rechercher...")
        self.search_box.setFixedWidth(300)
        self.search_box.textChanged.connect(self.search_orders)
        header_layout.addWidget(self.search_box)
        
        # Boutons
        refresh_btn = QPushButton("🔄 Actualiser")
        refresh_btn.setObjectName("secondaryBtn")
        refresh_btn.clicked.connect(self.load_purchase_orders)
        header_layout.addWidget(refresh_btn)
        
        new_btn = QPushButton("+ Nouvelle Commande")
        new_btn.setObjectName("primaryBtn")
        new_btn.clicked.connect(self.create_new_order)
        header_layout.addWidget(new_btn)
        
        layout.addLayout(header_layout)
        
        # Stats rapides
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)
        
        stats = self.controller.get_purchase_stats()
        
        self._add_stat_card(stats_layout, "Total Commandes", str(stats.get('total_orders', 0)), "#6750A4")
        self._add_stat_card(stats_layout, "Montant Total", f"{stats.get('total_amount', 0):,.0f} DA", "#1E8E3E")
        self._add_stat_card(stats_layout, "Ce Mois", f"{stats.get('month_amount', 0):,.0f} DA", "#2563EB")
        self._add_stat_card(stats_layout, "En Attente", str(stats.get('pending_reception', 0)), "#F9AB00")
        
        layout.addLayout(stats_layout)
        
        # Table des commandes
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "N°", "Fournisseur", "Réf. Facture", "Date", 
            "Montant HT", "TVA", "Total TTC", "Statut"
        ])
        
        # Configurer l'apparence du tableau
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.doubleClicked.connect(self.edit_selected_order)
        
        layout.addWidget(self.table)
        
        # Boutons d'action
        actions_layout = QHBoxLayout()
        actions_layout.addStretch()
        
        confirm_btn = QPushButton("✓ Confirmer")
        confirm_btn.setObjectName("successBtn")
        confirm_btn.clicked.connect(self.confirm_selected_order)
        actions_layout.addWidget(confirm_btn)
        
        receive_btn = QPushButton("📦 Réceptionner")
        receive_btn.setObjectName("primaryBtn")
        receive_btn.clicked.connect(self.receive_selected_order)
        actions_layout.addWidget(receive_btn)
        
        delete_btn = QPushButton("🗑️ Supprimer")
        delete_btn.setObjectName("dangerBtn")
        delete_btn.clicked.connect(self.delete_selected_order)
        actions_layout.addWidget(delete_btn)
        
        layout.addLayout(actions_layout)
    
    def _add_stat_card(self, parent_layout, label_text, value_text, color):
        """Ajoute une carte de statistique"""
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
            font-size: 20px;
            font-weight: 700;
            color: {color};
        """)
        card_layout.addWidget(value)
        
        parent_layout.addWidget(card)
    
    def load_purchase_orders(self):
        """Charge toutes les commandes"""
        self.table.setRowCount(0)
        orders = self.controller.get_all_purchase_orders()
        
        for order in orders:
            self._add_order_to_table(order)
        
        # Recharger les stats
        stats = self.controller.get_purchase_stats()
        # Mettre à jour les cartes de stats si nécessaire
    
    def _add_order_to_table(self, order: PurchaseOrder):
        """Ajoute une commande au tableau"""
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        # N°
        item = QTableWidgetItem(order.name)
        item.setData(Qt.ItemDataRole.UserRole, order.id)
        self.table.setItem(row, 0, item)
        
        # Fournisseur
        self.table.setItem(row, 1, QTableWidgetItem(order.partner_name))
        
        # Référence facture
        self.table.setItem(row, 2, QTableWidgetItem(order.supplier_invoice_ref))
        
        # Date
        date_str = order.date_order.strftime("%d/%m/%Y") if order.date_order else ""
        self.table.setItem(row, 3, QTableWidgetItem(date_str))
        
        # Montant HT
        self.table.setItem(row, 4, QTableWidgetItem(f"{order.amount_untaxed:,.2f}"))
        
        # TVA
        self.table.setItem(row, 5, QTableWidgetItem(f"{order.amount_tax:,.2f}"))
        
        # Total TTC
        self.table.setItem(row, 6, QTableWidgetItem(f"{order.amount_total:,.2f}"))
        
        # Statut avec couleur
        status_item = QTableWidgetItem(order.get_state_label())
        status_colors = {
            'draft': QColor(156, 163, 175),  # Gris
            'confirmed': QColor(37, 99, 235),  # Bleu
            'received': QColor(22, 163, 74),  # Vert
            'paid': QColor(34, 197, 94),  # Vert clair
            'cancelled': QColor(220, 38, 38)  # Rouge
        }
        if order.state in status_colors:
            status_item.setForeground(status_colors[order.state])
        self.table.setItem(row, 7, status_item)
    
    def search_orders(self):
        """Filtre les commandes par recherche"""
        search_text = self.search_box.text().lower()
        
        for row in range(self.table.rowCount()):
            show_row = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            self.table.setRowHidden(row, not show_row)
    
    def create_new_order(self):
        """Ouvre le formulaire de création"""
        dialog = PurchaseOrderFormDialog(self.db_manager, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_purchase_orders()
    
    def edit_selected_order(self):
        """Édite la commande sélectionnée"""
        selected = self.table.currentRow()
        if selected < 0:
            return
        
        order_id = self.table.item(selected, 0).data(Qt.ItemDataRole.UserRole)
        order = self.controller.get_purchase_order_by_id(order_id)
        
        if order:
            dialog = PurchaseOrderFormDialog(self.db_manager, order=order, parent=self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.load_purchase_orders()
    
    def confirm_selected_order(self):
        """Confirme la commande sélectionnée"""
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Sélection", "Veuillez sélectionner une commande")
            return
        
        order_id = self.table.item(selected, 0).data(Qt.ItemDataRole.UserRole)
        
        reply = QMessageBox.question(
            self, "Confirmation",
            "Confirmer cette commande d'achat?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.controller.confirm_purchase_order(order_id):
                QMessageBox.information(self, "Succès", "Commande confirmée")
                self.load_purchase_orders()
            else:
                QMessageBox.warning(self, "Erreur", "Impossible de confirmer cette commande")
    
    def receive_selected_order(self):
        """Réceptionne la commande (met à jour le stock)"""
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Sélection", "Veuillez sélectionner une commande")
            return
        
        order_id = self.table.item(selected, 0).data(Qt.ItemDataRole.UserRole)
        
        reply = QMessageBox.question(
            self, "Réception",
            "Réceptionner cette commande?\n\nLe stock des produits sera mis à jour.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.controller.receive_purchase_order(order_id):
                QMessageBox.information(self, "Succès", "Commande réceptionnée\nStock mis à jour")
                self.load_purchase_orders()
            else:
                QMessageBox.warning(self, "Erreur", "Impossible de réceptionner cette commande")
    
    def delete_selected_order(self):
        """Supprime la commande sélectionnée"""
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Sélection", "Veuillez sélectionner une commande")
            return
        
        order_id = self.table.item(selected, 0).data(Qt.ItemDataRole.UserRole)
        
        reply = QMessageBox.question(
            self, "Suppression",
            "Supprimer cette commande?\n\n(Seulement les brouillons peuvent être supprimés)",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.controller.delete_purchase_order(order_id):
                QMessageBox.information(self, "Succès", "Commande supprimée")
                self.load_purchase_orders()
            else:
                QMessageBox.warning(self, "Erreur", "Impossible de supprimer (pas un brouillon)")


class PurchaseOrderFormDialog(QDialog):
    """Formulaire de création/édition de commande d'achat"""
    
    def __init__(self, db_manager, order=None, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.controller = PurchaseController(db_manager)
        self.order = order if order else PurchaseOrder()
        self.lines = []
        
        self.setWindowTitle("Commande d'Achat Fournisseur")
        self.setMinimumSize(900, 600)
        self._setup_ui()
        
        if order and order.id:
            self._load_order_data()
    
    def _setup_ui(self):
        """Configure l'interface"""
        layout = QVBoxLayout(self)
        
        # Formulaire en-tête
        form_layout = QFormLayout()
        
        # Fournisseur
        self.supplier_combo = QComboBox()
        self._load_suppliers()
        form_layout.addRow("Fournisseur *:", self.supplier_combo)
        
        # Référence facture fournisseur
        self.supplier_ref_edit = QLineEdit()
        form_layout.addRow("N° Facture Fournisseur:", self.supplier_ref_edit)
        
        # Dates
        dates_layout = QHBoxLayout()
        
        self.date_order_edit = QDateEdit()
        self.date_order_edit.setCalendarPopup(True)
        self.date_order_edit.setDate(QDate.currentDate())
        dates_layout.addWidget(QLabel("Date Commande:"))
        dates_layout.addWidget(self.date_order_edit)
        
        self.date_due_edit = QDateEdit()
        self.date_due_edit.setCalendarPopup(True)
        self.date_due_edit.setDate(QDate.currentDate().addDays(30))
        dates_layout.addWidget(QLabel("Date Échéance:"))
        dates_layout.addWidget(self.date_due_edit)
        
        form_layout.addRow("", dates_layout)
        
        layout.addLayout(form_layout)
        
        # Section lignes
        lines_label = QLabel("Lignes de Commande")
        lines_label.setStyleSheet("font-size: 14px; font-weight: 600; margin-top: 10px;")
        layout.addWidget(lines_label)
        
        # Bouton ajouter ligne
        add_line_btn = QPushButton("+ Ajouter une Ligne")
        add_line_btn.clicked.connect(self._add_line)
        layout.addWidget(add_line_btn)
        
        # Table des lignes
        self.lines_table = QTableWidget()
        self.lines_table.setColumnCount(7)
        self.lines_table.setHorizontalHeaderLabels([
            "Produit", "Description", "Quantité", "Prix Unit.", "TVA %", "Total HT", "Actions"
        ])
        self.lines_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.lines_table)
        
        # Totaux
        totals_frame = QFrame()
        totals_frame.setStyleSheet("""
            QFrame {
                background-color: #F9FAFB;
                border: 1px solid #DADCE0;
                border-radius: 8px;
                padding: 16px;
            }
        """)
        totals_layout = QFormLayout(totals_frame)
        
        self.total_ht_label = QLabel("0.00 DA")
        self.total_ht_label.setStyleSheet("font-size: 14px; font-weight: 600;")
        totals_layout.addRow("Total HT:", self.total_ht_label)
        
        self.total_tva_label = QLabel("0.00 DA")
        self.total_tva_label.setStyleSheet("font-size: 14px; font-weight: 600;")
        totals_layout.addRow("TVA Déductible:", self.total_tva_label)
        
        self.total_ttc_label = QLabel("0.00 DA")
        self.total_ttc_label.setStyleSheet("font-size: 16px; font-weight: 700; color: #1E8E3E;")
        totals_layout.addRow("Total TTC:", self.total_ttc_label)
        
        layout.addWidget(totals_frame)
        
        # Notes
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(80)
        self.notes_edit.setPlaceholderText("Notes internes...")
        layout.addWidget(QLabel("Notes:"))
        layout.addWidget(self.notes_edit)
        
        # Boutons
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
    
    def _load_suppliers(self):
        """Charge la liste des fournisseurs"""
        self.supplier_combo.addItem("-- Sélectionner un fournisseur --", None)
        
        suppliers = self.db_manager.fetch_all("""
            SELECT id, name FROM res_partner
            WHERE is_supplier = 1 AND active = 1
            ORDER BY name
        """)
        
        for supplier in suppliers:
            self.supplier_combo.addItem(supplier['name'], supplier['id'])
    
    def _load_order_data(self):
        """Charge les données de la commande"""
        if self.order.partner_id:
            index = self.supplier_combo.findData(self.order.partner_id)
            if index >= 0:
                self.supplier_combo.setCurrentIndex(index)
        
        self.supplier_ref_edit.setText(self.order.supplier_invoice_ref)
        
        if self.order.date_order:
            qdate = QDate(self.order.date_order.year, self.order.date_order.month, self.order.date_order.day)
            self.date_order_edit.setDate(qdate)
        
        if self.order.date_due:
            qdate = QDate(self.order.date_due.year, self.order.date_due.month, self.order.date_due.day)
            self.date_due_edit.setDate(qdate)
        
        self.notes_edit.setPlainText(self.order.notes)
        
        # Charger les lignes
        for line in self.order.lines:
            self.lines.append(line)
            self._add_line_to_table(line)
        
        self._update_totals()
    
    def _add_line(self):
        """Ajoute une ligne vide"""
        line = PurchaseOrderLine()
        self.lines.append(line)
        self._add_line_to_table(line)
    
    def _add_line_to_table(self, line):
        """Ajoute une ligne au tableau"""
        row = self.lines_table.rowCount()
        self.lines_table.insertRow(row)
        
        # Produit (ComboBox)
        product_combo = QComboBox()
        product_combo.addItem("-- Produit --", None)
        products = self.db_manager.fetch_all("""
            SELECT id, name, cost_price FROM product_product WHERE active = 1 ORDER BY name
        """)
        for product in products:
            product_combo.addItem(product['name'], product['id'])
        
        if line.product_id:
            index = product_combo.findData(line.product_id)
            if index >= 0:
                product_combo.setCurrentIndex(index)
        
        product_combo.currentIndexChanged.connect(lambda: self._on_product_changed(row))
        self.lines_table.setCellWidget(row, 0, product_combo)
        
        # Description
        desc_edit = QLineEdit(line.description)
        desc_edit.textChanged.connect(lambda: self._update_totals())
        self.lines_table.setCellWidget(row, 1, desc_edit)
        
        # Quantité
        qty_spin = QDoubleSpinBox()
        qty_spin.setValue(line.quantity)
        qty_spin.setMinimum(0.01)
        qty_spin.setMaximum(999999)
        qty_spin.valueChanged.connect(lambda: self._update_totals())
        self.lines_table.setCellWidget(row, 2, qty_spin)
        
        # Prix unitaire
        price_spin = QDoubleSpinBox()
        price_spin.setValue(line.price_unit)
        price_spin.setMinimum(0)
        price_spin.setMaximum(999999999)
        price_spin.setDecimals(2)
        price_spin.valueChanged.connect(lambda: self._update_totals())
        self.lines_table.setCellWidget(row, 3, price_spin)
        
        # TVA
        tax_combo = QComboBox()
        tax_combo.addItem("0%", 0)
        tax_combo.addItem("9%", 9)
        tax_combo.addItem("19%", 19)
        
        if line.tax_rate == 9:
            tax_combo.setCurrentIndex(1)
        elif line.tax_rate == 19:
            tax_combo.setCurrentIndex(2)
        
        tax_combo.currentIndexChanged.connect(lambda: self._update_totals())
        self.lines_table.setCellWidget(row, 4, tax_combo)
        
        # Total HT
        total_item = QTableWidgetItem(f"{line.subtotal:.2f}")
        total_item.setFlags(total_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.lines_table.setItem(row, 5, total_item)
        
        # Bouton supprimer
        delete_btn = QPushButton("🗑️")
        delete_btn.clicked.connect(lambda: self._remove_line(row))
        self.lines_table.setCellWidget(row, 6, delete_btn)
    
    def _on_product_changed(self, row):
        """Quand un produit est sélectionné"""
        product_combo = self.lines_table.cellWidget(row, 0)
        product_id = product_combo.currentData()
        
        if product_id:
            product = self.db_manager.fetch_one("""
                SELECT name, cost_price FROM product_product WHERE id = ?
            """, (product_id,))
            
            if product:
                # Mettre à jour le prix
                price_spin = self.lines_table.cellWidget(row, 3)
                price_spin.setValue(product['cost_price'])
        
        self._update_totals()
    
    def _remove_line(self, row):
        """Supprime une ligne"""
        if row < len(self.lines):
            del self.lines[row]
        self.lines_table.removeRow(row)
        self._update_totals()
    
    def _update_totals(self):
        """Met à jour les totaux"""
        total_ht = 0
        total_tva = 0
        
        for row in range(self.lines_table.rowCount()):
            qty_spin = self.lines_table.cellWidget(row, 2)
            price_spin = self.lines_table.cellWidget(row, 3)
            tax_combo = self.lines_table.cellWidget(row, 4)
            
            if qty_spin and price_spin and tax_combo:
                qty = qty_spin.value()
                price = price_spin.value()
                tax_rate = tax_combo.currentData()
                
                subtotal = qty * price
                tax_amount = subtotal * (tax_rate / 100)
                
                total_ht += subtotal
                total_tva += tax_amount
                
                # Mettre à jour la colonne Total HT
                total_item = QTableWidgetItem(f"{subtotal:.2f}")
                total_item.setFlags(total_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.lines_table.setItem(row, 5, total_item)
        
        total_ttc = total_ht + total_tva
        
        self.total_ht_label.setText(f"{total_ht:,.2f} DA")
        self.total_tva_label.setText(f"{total_tva:,.2f} DA")
        self.total_ttc_label.setText(f"{total_ttc:,.2f} DA")
    
    def save_order(self):
        """Enregistre la commande"""
        # Validation
        if not self.supplier_combo.currentData():
            QMessageBox.warning(self, "Validation", "Veuillez sélectionner un fournisseur")
            return
        
        if self.lines_table.rowCount() == 0:
            QMessageBox.warning(self, "Validation", "Veuillez ajouter au moins une ligne")
            return
        
        # Construire l'objet
        order = PurchaseOrder()
        order.partner_id = self.supplier_combo.currentData()
        order.supplier_invoice_ref = self.supplier_ref_edit.text()
        
        # Dates
        qdate = self.date_order_edit.date()
        from datetime import datetime
        order.date_order = datetime(qdate.year(), qdate.month(), qdate.day())
        
        qdate_due = self.date_due_edit.date()
        order.date_due = datetime(qdate_due.year(), qdate_due.month(), qdate_due.day())
        
        order.notes = self.notes_edit.toPlainText()
        order.state = 'draft'
        
        # Lignes
        order.lines = []
        for row in range(self.lines_table.rowCount()):
            line = PurchaseOrderLine()
            
            product_combo = self.lines_table.cellWidget(row, 0)
            line.product_id = product_combo.currentData()
            line.product_name = product_combo.currentText()
            
            desc_edit = self.lines_table.cellWidget(row, 1)
            line.description = desc_edit.text()
            
            qty_spin = self.lines_table.cellWidget(row, 2)
            line.quantity = qty_spin.value()
            
            price_spin = self.lines_table.cellWidget(row, 3)
            line.price_unit = price_spin.value()
            
            tax_combo = self.lines_table.cellWidget(row, 4)
            line.tax_rate = tax_combo.currentData()
            
            line.calculate_amounts()
            order.lines.append(line)
        
        order.calculate_totals()
        
        try:
            if self.order.id:
                # Mise à jour
                order.id = self.order.id
                self.controller.update_purchase_order(order)
                QMessageBox.information(self, "Succès", "Commande mise à jour")
            else:
                # Création
                self.controller.create_purchase_order(order)
                QMessageBox.information(self, "Succès", "Commande créée")
            
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'enregistrement:\n{str(e)}")
