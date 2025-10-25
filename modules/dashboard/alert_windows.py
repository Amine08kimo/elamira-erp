# -*- coding: utf-8 -*-
"""
Fenêtres d'alertes avancées pour le Dashboard
Affiche tableaux détaillés avec actions possibles
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from core.ui.common_styles import ElAmiraStyles


class LowStockAlertWindow(QDialog):
    """Fenêtre alerte stock minimum avec actions"""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("📉 Alerte Stock Minimum")
        self.setMinimumSize(900, 600)
        self._setup_ui()
        self._load_data()
    
    def _setup_ui(self):
        """Configure l'interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header avec icône alerte
        header_layout = QHBoxLayout()
        header = QLabel("⚠️ Produits en Stock Minimum")
        header.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {ElAmiraStyles.COLORS['warning']};")
        header_layout.addWidget(header)
        header_layout.addStretch()
        
        # Badge nombre alertes
        self.badge_label = QLabel("0")
        self.badge_label.setStyleSheet(f"""
            background: {ElAmiraStyles.COLORS['danger']};
            color: white;
            padding: 5px 12px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: bold;
        """)
        header_layout.addWidget(self.badge_label)
        
        layout.addLayout(header_layout)
        
        # Message d'alerte
        alert_msg = QLabel(
            "⚠️ Les produits suivants sont en dessous du stock minimum.\n"
            "Action recommandée : Réapprovisionner rapidement."
        )
        alert_msg.setStyleSheet("""
            background: #FEF3C7;
            color: #92400E;
            padding: 12px;
            border-left: 4px solid #F59E0B;
            border-radius: 6px;
            font-size: 13px;
        """)
        layout.addWidget(alert_msg)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Code", "Produit", "Stock Actuel", "Stock Min", "Manquant", 
            "Prix Achat", "Coût Réappro"
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
            QTableWidget::item:selected {
                background: #FEF3C7;
            }
        """)
        layout.addWidget(self.table, 1)
        
        # Footer avec stats et actions
        footer_layout = QHBoxLayout()
        
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("font-size: 13px; font-weight: 600; color: #5F6368;")
        footer_layout.addWidget(self.stats_label)
        
        footer_layout.addStretch()
        
        # Boutons d'action
        reappro_btn = QPushButton("📦 Créer Bon de Commande")
        reappro_btn.setStyleSheet(ElAmiraStyles.button_primary())
        reappro_btn.clicked.connect(self._create_purchase_order)
        footer_layout.addWidget(reappro_btn)
        
        export_btn = QPushButton("📄 Exporter Liste")
        export_btn.setStyleSheet(ElAmiraStyles.button_secondary())
        export_btn.clicked.connect(self._export_list)
        footer_layout.addWidget(export_btn)
        
        close_btn = QPushButton("✖️ Fermer")
        close_btn.setStyleSheet(ElAmiraStyles.button_neutral())
        close_btn.clicked.connect(self.close)
        footer_layout.addWidget(close_btn)
        
        layout.addLayout(footer_layout)
        
        self.setStyleSheet("background: #F5F5F5;")
    
    def _load_data(self):
        """Charge les produits en stock bas"""
        if not self.db_manager:
            return
        
        try:
            result = self.db_manager.execute_query("""
                SELECT code, name, qty_available, minimum_stock, standard_price
                FROM product_product
                WHERE qty_available < minimum_stock AND active = 1
                ORDER BY (minimum_stock - qty_available) DESC
            """)
            
            if not result:
                # Message si tout est OK
                self.table.setRowCount(1)
                item = QTableWidgetItem("✅ Tous les stocks sont au niveau optimal !")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setForeground(QColor(16, 185, 129))  # Vert
                font = item.font()
                font.setPointSize(14)
                font.setBold(True)
                item.setFont(font)
                self.table.setItem(0, 0, item)
                self.table.setSpan(0, 0, 1, 7)
                self.badge_label.setText("0")
                self.badge_label.setStyleSheet(f"""
                    background: {ElAmiraStyles.COLORS['success']};
                    color: white;
                    padding: 5px 12px;
                    border-radius: 12px;
                    font-size: 14px;
                    font-weight: bold;
                """)
                self.stats_label.setText("Aucune alerte stock")
                return
            
            self._populate_table(result)
            
        except Exception as e:
            print(f"Erreur chargement stock bas: {e}")
    
    def _populate_table(self, data):
        """Remplit le tableau"""
        self.table.setRowCount(len(data))
        
        total_missing = 0
        total_cost = 0
        
        for row_idx, row in enumerate(data):
            code = row['code'] or "N/A"
            name = row['name']
            qty = row['qty_available'] or 0
            min_stock = row['minimum_stock'] or 0
            price = row['standard_price'] or 0
            
            missing = max(0, min_stock - qty)
            cost = missing * price
            
            total_missing += missing
            total_cost += cost
            
            # Code
            self.table.setItem(row_idx, 0, QTableWidgetItem(code))
            
            # Nom
            name_item = QTableWidgetItem(name)
            name_item.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            self.table.setItem(row_idx, 1, name_item)
            
            # Stock actuel (ROUGE)
            qty_item = QTableWidgetItem(str(qty))
            qty_item.setForeground(QColor(220, 38, 38))  # Rouge
            qty_item.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            qty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_idx, 2, qty_item)
            
            # Stock min
            min_item = QTableWidgetItem(str(min_stock))
            min_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_idx, 3, min_item)
            
            # Manquant
            missing_item = QTableWidgetItem(str(missing))
            missing_item.setForeground(QColor(245, 158, 11))  # Orange
            missing_item.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            missing_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_idx, 4, missing_item)
            
            # Prix achat
            self.table.setItem(row_idx, 5, QTableWidgetItem(f"{price:,.2f} DA"))
            
            # Coût réappro
            cost_item = QTableWidgetItem(f"{cost:,.2f} DA")
            cost_item.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            self.table.setItem(row_idx, 6, cost_item)
        
        # Stats
        self.badge_label.setText(str(len(data)))
        self.stats_label.setText(
            f"⚠️ {len(data)} produits | "
            f"📦 {total_missing} unités manquantes | "
            f"💰 Coût réappro: {total_cost:,.2f} DA"
        )
    
    def _create_purchase_order(self):
        """Crée un bon de commande (placeholder)"""
        QMessageBox.information(self, "Bon de Commande",
            "📦 Fonctionnalité en développement\n\n"
            "Cette action ouvrira le module Achats avec un bon\n"
            "de commande pré-rempli pour tous les produits en stock bas.")
    
    def _export_list(self):
        """Exporte la liste (placeholder)"""
        QMessageBox.information(self, "Export",
            "📄 Fonctionnalité en développement\n\n"
            "Cette action exportera la liste en Excel/PDF.")


class MaintenanceAlertWindow(QDialog):
    """Fenêtre alerte maintenances planifiées"""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("🔧 Maintenances Planifiées")
        self.setMinimumSize(1000, 600)
        self._setup_ui()
        self._load_data()
    
    def _setup_ui(self):
        """Configure l'interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        header = QLabel("🔧 Planning Maintenances")
        header.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {ElAmiraStyles.COLORS['primary']};")
        header_layout.addWidget(header)
        header_layout.addStretch()
        
        self.badge_label = QLabel("0")
        self.badge_label.setStyleSheet(f"""
            background: {ElAmiraStyles.COLORS['secondary']};
            color: white;
            padding: 5px 12px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: bold;
        """)
        header_layout.addWidget(self.badge_label)
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Date", "Machine", "Type", "Client", "Technicien", "État", "Priorité"
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
        
        calendar_btn = QPushButton("📅 Voir Calendrier")
        calendar_btn.setStyleSheet(ElAmiraStyles.button_primary())
        calendar_btn.clicked.connect(self._show_calendar)
        footer_layout.addWidget(calendar_btn)
        
        close_btn = QPushButton("✖️ Fermer")
        close_btn.setStyleSheet(ElAmiraStyles.button_secondary())
        close_btn.clicked.connect(self.close)
        footer_layout.addWidget(close_btn)
        
        layout.addLayout(footer_layout)
        
        self.setStyleSheet("background: #F5F5F5;")
    
    def _load_data(self):
        """Charge les maintenances"""
        if not self.db_manager:
            return
        
        try:
            result = self.db_manager.execute_query("""
                SELECT date_scheduled, machine_name, intervention_type,
                       partner_name, technician_name, state, priority
                FROM maintenance_intervention
                WHERE state IN ('scheduled', 'in_progress')
                ORDER BY date_scheduled ASC
                LIMIT 50
            """)
            
            if not result:
                self.table.setRowCount(1)
                item = QTableWidgetItem("✅ Aucune maintenance planifiée")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setForeground(QColor(16, 185, 129))
                font = item.font()
                font.setPointSize(14)
                font.setBold(True)
                item.setFont(font)
                self.table.setItem(0, 0, item)
                self.table.setSpan(0, 0, 1, 7)
                self.badge_label.setText("0")
                self.stats_label.setText("Aucune maintenance")
                return
            
            self._populate_table(result)
            
        except Exception as e:
            print(f"Erreur chargement maintenances: {e}")
    
    def _populate_table(self, data):
        """Remplit le tableau"""
        self.table.setRowCount(len(data))
        
        state_labels = {
            'scheduled': ('📅 Planifiée', ElAmiraStyles.COLORS['secondary']),
            'in_progress': ('⚙️ En cours', ElAmiraStyles.COLORS['warning']),
        }
        
        priority_labels = {
            'high': ('🔴 Haute', ElAmiraStyles.COLORS['danger']),
            'normal': ('🟡 Normale', ElAmiraStyles.COLORS['warning']),
            'low': ('🟢 Basse', ElAmiraStyles.COLORS['success']),
        }
        
        for row_idx, row in enumerate(data):
            # Date
            date_str = str(row['date_scheduled'])[:10] if row['date_scheduled'] else "N/A"
            date_item = QTableWidgetItem(date_str)
            date_item.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            self.table.setItem(row_idx, 0, date_item)
            
            # Machine
            self.table.setItem(row_idx, 1, QTableWidgetItem(row['machine_name'] or "N/A"))
            
            # Type
            intervention_type = row['intervention_type'] or "N/A"
            type_labels = {
                'preventive': '🛡️ Préventive',
                'corrective': '🔧 Corrective',
                'emergency': '🚨 Urgence'
            }
            type_label = type_labels.get(intervention_type, intervention_type)
            self.table.setItem(row_idx, 2, QTableWidgetItem(type_label))
            
            # Client
            self.table.setItem(row_idx, 3, QTableWidgetItem(row['partner_name'] or "N/A"))
            
            # Technicien
            self.table.setItem(row_idx, 4, QTableWidgetItem(row['technician_name'] or "Non assigné"))
            
            # État
            state = row['state']
            state_label, state_color = state_labels.get(state, (state, '#5F6368'))
            state_item = QTableWidgetItem(state_label)
            state_item.setForeground(QColor(state_color))
            state_item.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            self.table.setItem(row_idx, 5, state_item)
            
            # Priorité
            priority = row['priority'] or 'normal'
            priority_label, priority_color = priority_labels.get(priority, ('Normal', '#5F6368'))
            priority_item = QTableWidgetItem(priority_label)
            priority_item.setForeground(QColor(priority_color))
            priority_item.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            self.table.setItem(row_idx, 6, priority_item)
        
        # Stats
        self.badge_label.setText(str(len(data)))
        self.stats_label.setText(f"🔧 {len(data)} maintenances planifiées")
    
    def _show_calendar(self):
        """Affiche calendrier (placeholder)"""
        QMessageBox.information(self, "Calendrier",
            "📅 Fonctionnalité en développement\n\n"
            "Cette action ouvrira une vue calendrier des maintenances.")


class UnpaidInvoicesAlertWindow(QDialog):
    """Fenêtre alerte factures impayées"""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("💳 Factures Impayées")
        self.setMinimumSize(1000, 600)
        self._setup_ui()
        self._load_data()
    
    def _setup_ui(self):
        """Configure l'interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        header = QLabel("💳 Factures Impayées")
        header.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {ElAmiraStyles.COLORS['danger']};")
        header_layout.addWidget(header)
        header_layout.addStretch()
        
        self.badge_label = QLabel("0")
        self.badge_label.setStyleSheet(f"""
            background: {ElAmiraStyles.COLORS['danger']};
            color: white;
            padding: 5px 12px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: bold;
        """)
        header_layout.addWidget(self.badge_label)
        
        layout.addLayout(header_layout)
        
        # Message d'alerte
        alert_msg = QLabel(
            "⚠️ Factures en attente de paiement. Action recommandée : Relancer les clients."
        )
        alert_msg.setStyleSheet("""
            background: #FEE2E2;
            color: #7F1D1D;
            padding: 12px;
            border-left: 4px solid #DC2626;
            border-radius: 6px;
            font-size: 13px;
        """)
        layout.addWidget(alert_msg)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Numéro", "Client", "Date", "Montant", "Jours Retard", "Actions"
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
        
        relance_btn = QPushButton("📧 Relancer Tous")
        relance_btn.setStyleSheet(ElAmiraStyles.button_danger())
        relance_btn.clicked.connect(self._send_reminders)
        footer_layout.addWidget(relance_btn)
        
        close_btn = QPushButton("✖️ Fermer")
        close_btn.setStyleSheet(ElAmiraStyles.button_secondary())
        close_btn.clicked.connect(self.close)
        footer_layout.addWidget(close_btn)
        
        layout.addLayout(footer_layout)
        
        self.setStyleSheet("background: #F5F5F5;")
    
    def _load_data(self):
        """Charge les factures impayées"""
        if not self.db_manager:
            return
        
        try:
            result = self.db_manager.execute_query("""
                SELECT name, partner_name, date_invoice, amount_total,
                       julianday('now') - julianday(date_invoice) as days_late
                FROM account_invoice
                WHERE state = 'open'
                ORDER BY date_invoice ASC
            """)
            
            if not result:
                self.table.setRowCount(1)
                item = QTableWidgetItem("✅ Toutes les factures sont payées !")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setForeground(QColor(16, 185, 129))
                font = item.font()
                font.setPointSize(14)
                font.setBold(True)
                item.setFont(font)
                self.table.setItem(0, 0, item)
                self.table.setSpan(0, 0, 1, 6)
                self.badge_label.setText("0")
                self.badge_label.setStyleSheet(f"""
                    background: {ElAmiraStyles.COLORS['success']};
                    color: white;
                    padding: 5px 12px;
                    border-radius: 12px;
                    font-size: 14px;
                    font-weight: bold;
                """)
                self.stats_label.setText("Aucune facture impayée")
                return
            
            self._populate_table(result)
            
        except Exception as e:
            print(f"Erreur chargement factures impayées: {e}")
    
    def _populate_table(self, data):
        """Remplit le tableau"""
        self.table.setRowCount(len(data))
        
        total_unpaid = 0
        
        for row_idx, row in enumerate(data):
            name = row['name']
            partner = row['partner_name'] or "N/A"
            date = str(row['date_invoice'])[:10] if row['date_invoice'] else "N/A"
            amount = row['amount_total'] or 0
            days_late = int(row['days_late']) if row['days_late'] else 0
            
            total_unpaid += amount
            
            # Numéro
            self.table.setItem(row_idx, 0, QTableWidgetItem(name))
            
            # Client
            client_item = QTableWidgetItem(partner)
            client_item.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            self.table.setItem(row_idx, 1, client_item)
            
            # Date
            self.table.setItem(row_idx, 2, QTableWidgetItem(date))
            
            # Montant
            amount_item = QTableWidgetItem(f"{amount:,.2f} DA")
            amount_item.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            amount_item.setForeground(QColor(220, 38, 38))
            self.table.setItem(row_idx, 3, amount_item)
            
            # Jours retard
            days_item = QTableWidgetItem(f"{days_late} jours")
            if days_late > 30:
                days_item.setForeground(QColor(220, 38, 38))  # Rouge
            elif days_late > 15:
                days_item.setForeground(QColor(245, 158, 11))  # Orange
            days_item.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            days_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_idx, 4, days_item)
            
            # Actions (placeholder)
            self.table.setItem(row_idx, 5, QTableWidgetItem("📧 📞 📄"))
        
        # Stats
        self.badge_label.setText(str(len(data)))
        self.stats_label.setText(
            f"💳 {len(data)} factures impayées | "
            f"💰 Total: {total_unpaid:,.2f} DA"
        )
    
    def _send_reminders(self):
        """Envoie des relances (placeholder)"""
        QMessageBox.information(self, "Relances",
            "📧 Fonctionnalité en développement\n\n"
            "Cette action enverra des emails de relance\n"
            "à tous les clients avec factures impayées.")
