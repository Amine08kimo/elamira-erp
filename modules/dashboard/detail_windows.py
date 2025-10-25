# -*- coding: utf-8 -*-
"""
Fenêtres de détail pour le Dashboard
Affiche des listes complètes avec tableaux
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from core.ui.common_styles import ElAmiraStyles


class InvoicesDetailWindow(QDialog):
    """Fenêtre détaillée des factures"""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("📄 Liste des Factures")
        self.setMinimumSize(900, 600)
        self._setup_ui()
        self._load_data()
    
    def _setup_ui(self):
        """Configure l'interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("📄 Liste Complète des Factures")
        header.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {ElAmiraStyles.COLORS['primary']};")
        layout.addWidget(header)
        
        # Barre de recherche
        search_layout = QHBoxLayout()
        search_label = QLabel("🔍 Rechercher:")
        search_label.setStyleSheet("font-size: 13px; font-weight: 500;")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Numéro, client...")
        self.search_input.setStyleSheet(ElAmiraStyles.input_style())
        self.search_input.textChanged.connect(self._filter_data)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input, 1)
        layout.addLayout(search_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Numéro", "Client", "Date", "État", "Montant HT", "Montant TTC"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                gridline-color: #E0E0E0;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background: #F5F5F5;
                padding: 10px;
                border: none;
                font-weight: 600;
                font-size: 13px;
            }
        """)
        layout.addWidget(self.table, 1)
        
        # Footer avec statistiques
        stats_layout = QHBoxLayout()
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("font-size: 13px; font-weight: 600; color: #5F6368;")
        stats_layout.addWidget(self.stats_label)
        stats_layout.addStretch()
        
        close_btn = QPushButton("✖️ Fermer")
        close_btn.setStyleSheet(ElAmiraStyles.button_secondary())
        close_btn.clicked.connect(self.close)
        stats_layout.addWidget(close_btn)
        
        layout.addLayout(stats_layout)
        
        self.setStyleSheet("background: #F5F5F5;")
    
    def _load_data(self):
        """Charge les factures"""
        if not self.db_manager:
            return
        
        try:
            result = self.db_manager.execute_query("""
                SELECT name, partner_name, date_invoice, state, 
                       amount_untaxed, amount_total
                FROM account_invoice
                ORDER BY date_invoice DESC
            """)
            
            self.all_data = result or []
            self._populate_table(self.all_data)
            
        except Exception as e:
            print(f"Erreur chargement factures: {e}")
    
    def _populate_table(self, data):
        """Remplit le tableau"""
        self.table.setRowCount(len(data))
        
        states_labels = {
            'draft': '📝 Brouillon',
            'open': '⏳ En attente',
            'paid': '✅ Payée',
            'cancel': '❌ Annulée'
        }
        
        total = 0
        paid_count = 0
        
        for row_idx, row in enumerate(data):
            # Numéro
            self.table.setItem(row_idx, 0, QTableWidgetItem(row['name']))
            
            # Client
            self.table.setItem(row_idx, 1, QTableWidgetItem(row['partner_name'] or "N/A"))
            
            # Date
            date_str = str(row['date_invoice'])[:10] if row['date_invoice'] else "N/A"
            self.table.setItem(row_idx, 2, QTableWidgetItem(date_str))
            
            # État
            state = row['state']
            state_label = states_labels.get(state, state)
            self.table.setItem(row_idx, 3, QTableWidgetItem(state_label))
            
            # Montants
            amount_untaxed = row['amount_untaxed'] or 0
            amount_total = row['amount_total'] or 0
            
            self.table.setItem(row_idx, 4, QTableWidgetItem(f"{amount_untaxed:,.2f} DA"))
            self.table.setItem(row_idx, 5, QTableWidgetItem(f"{amount_total:,.2f} DA"))
            
            if state == 'paid':
                paid_count += 1
                total += amount_total
        
        # Stats
        self.stats_label.setText(
            f"Total: {len(data)} factures | Payées: {paid_count} | CA Total: {total:,.2f} DA"
        )
    
    def _filter_data(self):
        """Filtre les données selon la recherche"""
        search_text = self.search_input.text().lower()
        
        if not search_text:
            self._populate_table(self.all_data)
            return
        
        filtered = [
            row for row in self.all_data
            if search_text in (row['name'] or "").lower() or
               search_text in (row['partner_name'] or "").lower()
        ]
        
        self._populate_table(filtered)


class ClientsDetailWindow(QDialog):
    """Fenêtre détaillée des clients"""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("👤 Liste des Clients")
        self.setMinimumSize(800, 600)
        self._setup_ui()
        self._load_data()
    
    def _setup_ui(self):
        """Configure l'interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("👤 Liste Complète des Clients")
        header.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {ElAmiraStyles.COLORS['primary']};")
        layout.addWidget(header)
        
        # Barre de recherche
        search_layout = QHBoxLayout()
        search_label = QLabel("🔍 Rechercher:")
        search_label.setStyleSheet("font-size: 13px; font-weight: 500;")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nom, téléphone, ville...")
        self.search_input.setStyleSheet(ElAmiraStyles.input_style())
        self.search_input.textChanged.connect(self._filter_data)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input, 1)
        layout.addLayout(search_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Nom", "Téléphone", "Email", "Ville", "Adresse"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                gridline-color: #E0E0E0;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background: #F5F5F5;
                padding: 10px;
                border: none;
                font-weight: 600;
                font-size: 13px;
            }
        """)
        layout.addWidget(self.table, 1)
        
        # Footer
        footer_layout = QHBoxLayout()
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("font-size: 13px; font-weight: 600; color: #5F6368;")
        footer_layout.addWidget(self.stats_label)
        footer_layout.addStretch()
        
        close_btn = QPushButton("✖️ Fermer")
        close_btn.setStyleSheet(ElAmiraStyles.button_secondary())
        close_btn.clicked.connect(self.close)
        footer_layout.addWidget(close_btn)
        
        layout.addLayout(footer_layout)
        
        self.setStyleSheet("background: #F5F5F5;")
    
    def _load_data(self):
        """Charge les clients"""
        if not self.db_manager:
            return
        
        try:
            result = self.db_manager.execute_query("""
                SELECT name, phone, email, city, address
                FROM res_partner
                WHERE customer = 1
                ORDER BY name ASC
            """)
            
            self.all_data = result or []
            self._populate_table(self.all_data)
            
        except Exception as e:
            print(f"Erreur chargement clients: {e}")
    
    def _populate_table(self, data):
        """Remplit le tableau"""
        self.table.setRowCount(len(data))
        
        for row_idx, row in enumerate(data):
            self.table.setItem(row_idx, 0, QTableWidgetItem(row['name']))
            self.table.setItem(row_idx, 1, QTableWidgetItem(row['phone'] or "N/A"))
            self.table.setItem(row_idx, 2, QTableWidgetItem(row['email'] or "N/A"))
            self.table.setItem(row_idx, 3, QTableWidgetItem(row['city'] or "N/A"))
            self.table.setItem(row_idx, 4, QTableWidgetItem(row['address'] or "N/A"))
        
        self.stats_label.setText(f"Total: {len(data)} clients")
    
    def _filter_data(self):
        """Filtre les données"""
        search_text = self.search_input.text().lower()
        
        if not search_text:
            self._populate_table(self.all_data)
            return
        
        filtered = [
            row for row in self.all_data
            if search_text in (row['name'] or "").lower() or
               search_text in (row['phone'] or "").lower() or
               search_text in (row['city'] or "").lower()
        ]
        
        self._populate_table(filtered)


class ProductsDetailWindow(QDialog):
    """Fenêtre détaillée des produits"""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("📦 Liste des Produits")
        self.setMinimumSize(900, 600)
        self._setup_ui()
        self._load_data()
    
    def _setup_ui(self):
        """Configure l'interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("📦 Liste Complète des Produits")
        header.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {ElAmiraStyles.COLORS['primary']};")
        layout.addWidget(header)
        
        # Barre de recherche
        search_layout = QHBoxLayout()
        search_label = QLabel("🔍 Rechercher:")
        search_label.setStyleSheet("font-size: 13px; font-weight: 500;")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nom, code...")
        self.search_input.setStyleSheet(ElAmiraStyles.input_style())
        self.search_input.textChanged.connect(self._filter_data)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input, 1)
        layout.addLayout(search_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Code", "Nom", "Stock", "Min", "Prix Vente", "Prix Achat"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                gridline-color: #E0E0E0;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background: #F5F5F5;
                padding: 10px;
                border: none;
                font-weight: 600;
                font-size: 13px;
            }
        """)
        layout.addWidget(self.table, 1)
        
        # Footer
        footer_layout = QHBoxLayout()
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("font-size: 13px; font-weight: 600; color: #5F6368;")
        footer_layout.addWidget(self.stats_label)
        footer_layout.addStretch()
        
        close_btn = QPushButton("✖️ Fermer")
        close_btn.setStyleSheet(ElAmiraStyles.button_secondary())
        close_btn.clicked.connect(self.close)
        footer_layout.addWidget(close_btn)
        
        layout.addLayout(footer_layout)
        
        self.setStyleSheet("background: #F5F5F5;")
    
    def _load_data(self):
        """Charge les produits"""
        if not self.db_manager:
            return
        
        try:
            result = self.db_manager.execute_query("""
                SELECT code, name, qty_available, minimum_stock, 
                       list_price, standard_price
                FROM product_product
                WHERE active = 1
                ORDER BY name ASC
            """)
            
            self.all_data = result or []
            self._populate_table(self.all_data)
            
        except Exception as e:
            print(f"Erreur chargement produits: {e}")
    
    def _populate_table(self, data):
        """Remplit le tableau"""
        self.table.setRowCount(len(data))
        
        total_stock = 0
        low_stock = 0
        
        for row_idx, row in enumerate(data):
            code_item = QTableWidgetItem(row['code'] or "N/A")
            self.table.setItem(row_idx, 0, code_item)
            
            self.table.setItem(row_idx, 1, QTableWidgetItem(row['name']))
            
            qty = row['qty_available'] or 0
            min_stock = row['minimum_stock'] or 0
            total_stock += qty
            
            qty_item = QTableWidgetItem(str(qty))
            if qty < min_stock:
                qty_item.setForeground(Qt.GlobalColor.red)
                low_stock += 1
            self.table.setItem(row_idx, 2, qty_item)
            
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(min_stock)))
            
            list_price = row['list_price'] or 0
            standard_price = row['standard_price'] or 0
            
            self.table.setItem(row_idx, 4, QTableWidgetItem(f"{list_price:,.2f} DA"))
            self.table.setItem(row_idx, 5, QTableWidgetItem(f"{standard_price:,.2f} DA"))
        
        self.stats_label.setText(
            f"Total: {len(data)} produits | Stock: {total_stock} unités | ⚠️ Stock bas: {low_stock}"
        )
    
    def _filter_data(self):
        """Filtre les données"""
        search_text = self.search_input.text().lower()
        
        if not search_text:
            self._populate_table(self.all_data)
            return
        
        filtered = [
            row for row in self.all_data
            if search_text in (row['name'] or "").lower() or
               search_text in (row['code'] or "").lower()
        ]
        
        self._populate_table(filtered)
