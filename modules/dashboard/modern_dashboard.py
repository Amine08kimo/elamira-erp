#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Dashboard Moderne Unifié - Style Maintenance
Hérite du système de styles communs
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QScrollArea, QMessageBox, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QCursor
from datetime import datetime, timedelta
from core.ui.common_styles import ElAmiraStyles, ElAmiraDialog


class ModernDashboard(QWidget):
    """Dashboard moderne avec style unifié"""
    
    def __init__(self, module, db_manager):
        super().__init__()
        self.module = module
        self.db_manager = db_manager
        self.main_window = None  # Sera défini par le parent
        
        try:
            self._setup_ui()
            self._load_data()
            self._setup_notifications()
        except Exception as e:
            print(f"Erreur initialisation dashboard: {e}")
            import traceback
            traceback.print_exc()
            self._show_error_message(str(e))
    
    def _setup_ui(self):
        """Configure l'interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # ========== HEADER ==========
        header_layout = QHBoxLayout()
        
        title = QLabel("📊 Tableau de Bord")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: 700;
            color: #1A1A1A;
        """)
        header_layout.addWidget(title)
        
        # Date/Heure en temps réel
        self.datetime_label = QLabel()
        self.datetime_label.setStyleSheet("""
            font-size: 14px;
            color: #5F6368;
            font-weight: 600;
        """)
        self.update_datetime()
        header_layout.addWidget(self.datetime_label)
        
        header_layout.addStretch()
        
        # Bouton Actualiser
        refresh_btn = ElAmiraDialog.create_button("🔄 Actualiser", 'primary')
        refresh_btn.clicked.connect(self._load_data)
        header_layout.addWidget(refresh_btn)
        
        # Bouton Notifications
        self.notif_btn = QPushButton("🔔 Notifications")
        self.notif_btn.setStyleSheet(ElAmiraStyles.button_secondary())
        self.notif_btn.clicked.connect(self.show_notifications)
        header_layout.addWidget(self.notif_btn)
        
        layout.addLayout(header_layout)
        
        # ========== KPI CARDS (Style Maintenance) ==========
        kpi_title = QLabel("📈 Indicateurs Clés")
        kpi_title.setStyleSheet("""
            font-size: 16px;
            font-weight: 700;
            color: #1A1A1A;
            margin-top: 10px;
        """)
        layout.addWidget(kpi_title)
        
        kpi_grid = QGridLayout()
        kpi_grid.setSpacing(15)
        
        # KPI Cards (4 principaux)
        self.kpi_cards = {}
        
        # 1. Chiffre d'Affaires
        ca_card = self._create_kpi_card(
            "💰", "CHIFFRE D'AFFAIRES", "0.00 DA", "Ce mois", 
            'kpi_violet', 'sales'
        )
        kpi_grid.addWidget(ca_card, 0, 0)
        self.kpi_cards['ca'] = ca_card
        
        # 2. Factures
        factures_card = self._create_kpi_card(
            "📄", "FACTURES", "0", "Total actif",
            'kpi_green', 'invoices'
        )
        kpi_grid.addWidget(factures_card, 0, 1)
        self.kpi_cards['factures'] = factures_card
        
        # 3. Clients
        clients_card = self._create_kpi_card(
            "👤", "CLIENTS", "0", "Enregistrés",
            'kpi_blue', 'clients'
        )
        kpi_grid.addWidget(clients_card, 0, 2)
        self.kpi_cards['clients'] = clients_card
        
        # 4. Produits
        produits_card = self._create_kpi_card(
            "📦", "PRODUITS", "0", "En stock",
            'kpi_orange', 'products'
        )
        kpi_grid.addWidget(produits_card, 0, 3)
        self.kpi_cards['produits'] = produits_card
        
        layout.addLayout(kpi_grid)
        
        # ========== SECTION ALERTES ==========
        alerts_title = QLabel("⚠️ Alertes & Notifications")
        alerts_title.setStyleSheet("""
            font-size: 16px;
            font-weight: 700;
            color: #1A1A1A;
            margin-top: 20px;
        """)
        layout.addWidget(alerts_title)
        
        alerts_layout = QHBoxLayout()
        alerts_layout.setSpacing(15)
        
        # Alerte Stock Minimum
        self.stock_alert_card = self._create_alert_card(
            "📉", "Stock Minimum", "0 produits", 
            ElAmiraStyles.COLORS['warning']
        )
        self.stock_alert_card.clicked.connect(self.show_low_stock)
        alerts_layout.addWidget(self.stock_alert_card)
        
        # Alerte Maintenances
        self.maint_alert_card = self._create_alert_card(
            "🔧", "Maintenances", "0 à venir",
            ElAmiraStyles.COLORS['secondary']
        )
        self.maint_alert_card.clicked.connect(self.show_maintenance_schedule)
        alerts_layout.addWidget(self.maint_alert_card)
        
        # Alerte Factures Impayées
        self.unpaid_alert_card = self._create_alert_card(
            "💳", "Factures Impayées", "0.00 DA",
            ElAmiraStyles.COLORS['danger']
        )
        self.unpaid_alert_card.clicked.connect(self.show_unpaid_invoices)
        alerts_layout.addWidget(self.unpaid_alert_card)
        
        layout.addLayout(alerts_layout)
        
        # ========== SECTION GRAPHIQUES ==========
        charts_title = QLabel("📊 Statistiques & Graphiques")
        charts_title.setStyleSheet("""
            font-size: 16px;
            font-weight: 700;
            color: #1A1A1A;
            margin-top: 20px;
        """)
        layout.addWidget(charts_title)
        
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(15)
        
        # Graphique Ventes
        sales_chart = self._create_chart_card(
            "📈", "Ventes Mensuelles", "sales_chart"
        )
        sales_chart.clicked.connect(self.show_sales_chart)
        charts_layout.addWidget(sales_chart)
        
        # Graphique Top Produits
        products_chart = self._create_chart_card(
            "🏆", "Top Produits", "products_chart"
        )
        products_chart.clicked.connect(self.show_products_chart)
        charts_layout.addWidget(products_chart)
        
        # Graphique CA
        revenue_chart = self._create_chart_card(
            "💰", "Évolution CA", "revenue_chart"
        )
        revenue_chart.clicked.connect(self.show_revenue_chart)
        charts_layout.addWidget(revenue_chart)
        
        layout.addLayout(charts_layout)
        
        # ========== ACCÈS RAPIDES MODULES ==========
        modules_title = QLabel("🚀 Accès Rapides")
        modules_title.setStyleSheet("""
            font-size: 16px;
            font-weight: 700;
            color: #1A1A1A;
            margin-top: 20px;
        """)
        layout.addWidget(modules_title)
        
        modules_layout = QGridLayout()
        modules_layout.setSpacing(15)
        
        # Boutons modules
        modules = [
            ("💰", "Nouvelle Vente", "sales", "success"),
            ("📦", "Nouveau Produit", "stock", "primary"),
            ("👤", "Nouveau Client", "crm", "secondary"),
            ("🛒", "Nouvel Achat", "purchase", "secondary"),
            ("🔧", "Nouvelle Maintenance", "maintenance", "primary"),
            ("📄", "Nouvelle Facture", "accounting", "success"),
        ]
        
        row, col = 0, 0
        for emoji, label, module, color in modules:
            btn = self._create_module_button(emoji, label, module, color)
            modules_layout.addWidget(btn, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        layout.addLayout(modules_layout)
        
        layout.addStretch()
    
    def _create_kpi_card(self, emoji, title, value, subtitle, color_key, data_key):
        """Crée une KPI card cliquable avec hover effects"""
        card = QPushButton()
        card.setObjectName("kpiCard")
        card.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        # Style avec animation hover
        color = ElAmiraStyles.COLORS.get(color_key, ElAmiraStyles.COLORS['kpi_violet'])
        bg_color = f"rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.08)"
        
        card.setStyleSheet(f"""
            QPushButton#kpiCard {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {bg_color}, stop:1 #FFFFFF);
                border: 2px solid #E0E0E0;
                border-radius: 12px;
                padding: 15px;
                text-align: left;
                min-height: 140px;
                min-width: 200px;
            }}
            QPushButton#kpiCard:hover {{
                border: 2px solid {color};
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {color}, stop:1 {bg_color});
                transform: translateY(-4px);
                box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            }}
            QPushButton#kpiCard:pressed {{
                background: {bg_color};
                transform: translateY(0px);
            }}
        """)
        
        card.setMinimumHeight(140)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        
        # Layout interne
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(8)
        
        # Emoji + Title
        header_layout = QHBoxLayout()
        emoji_label = QLabel(emoji)
        emoji_label.setStyleSheet("font-size: 24px;")
        header_layout.addWidget(emoji_label)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            font-size: 11px;
            font-weight: 700;
            color: {ElAmiraStyles.COLORS[color_key]};
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        card_layout.addLayout(header_layout)
        
        # Valeur
        value_label = QLabel(value)
        value_label.setObjectName(f"value_{data_key}")
        value_label.setStyleSheet("""
            font-size: 32px;
            font-weight: 700;
            color: #1A1A1A;
        """)
        card_layout.addWidget(value_label)
        
        # Sous-titre
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("""
            font-size: 12px;
            color: #5F6368;
        """)
        card_layout.addWidget(subtitle_label)
        
        card_layout.addStretch()
        
        # Connecter clic
        card.clicked.connect(lambda: self.on_kpi_click(data_key))
        
        return card
    
    def _create_alert_card(self, emoji, title, value, color):
        """Crée une carte d'alerte cliquable avec hover effects"""
        card = QPushButton()
        card.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        card.setMinimumHeight(100)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        
        # Couleur de fond avec transparence
        bg_color = f"rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.1)"
        bg_hover = f"rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.2)"
        
        card.setStyleSheet(f"""
            QPushButton {{
                background: {bg_color};
                border: 2px solid {ElAmiraStyles.COLORS['gray_light']};
                border-left: 5px solid {color};
                border-radius: 10px;
                padding: 15px;
                text-align: left;
                min-width: 180px;
            }}
            QPushButton:hover {{
                border: 2px solid {color};
                border-left: 5px solid {color};
                background: {bg_hover};
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }}
            QPushButton:pressed {{
                background: {bg_color};
                transform: translateY(0px);
            }}
        """)
        
        layout = QVBoxLayout(card)
        
        # Emoji
        emoji_label = QLabel(emoji)
        emoji_label.setStyleSheet("font-size: 28px;")
        layout.addWidget(emoji_label)
        
        # Titre
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            font-size: 14px;
            font-weight: 700;
            color: {color};
        """)
        layout.addWidget(title_label)
        
        # Valeur
        value_label = QLabel(value)
        value_label.setObjectName(f"alert_value_{title.lower().replace(' ', '_')}")
        value_label.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #1A1A1A;
        """)
        layout.addWidget(value_label)
        
        return card
    
    def _create_chart_card(self, emoji, title, chart_key):
        """Crée une carte graphique cliquable"""
        card = QPushButton()
        card.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        card.setMinimumHeight(120)
        card.setStyleSheet(f"""
            QPushButton {{
                background: white;
                border: 2px solid {ElAmiraStyles.COLORS['gray_light']};
                border-radius: 10px;
                padding: 20px;
            }}
            QPushButton:hover {{
                border: 2px solid {ElAmiraStyles.COLORS['primary']};
                background: {ElAmiraStyles.COLORS['bg_hover']};
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Emoji
        emoji_label = QLabel(emoji)
        emoji_label.setStyleSheet("font-size: 36px;")
        emoji_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(emoji_label)
        
        # Titre
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 14px;
            font-weight: 700;
            color: #1A1A1A;
            margin-top: 10px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Label "Cliquer pour voir"
        info_label = QLabel("Cliquer pour afficher")
        info_label.setStyleSheet("""
            font-size: 11px;
            color: #5F6368;
            margin-top: 5px;
        """)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)
        
        return card
    
    def _create_module_button(self, emoji, label, module, color):
        """Crée un bouton d'accès rapide module"""
        btn = ElAmiraDialog.create_button(f"{emoji} {label}", color)
        btn.setMinimumHeight(50)
        btn.clicked.connect(lambda: self.open_module(module))
        return btn
    
    def _setup_notifications(self):
        """Configure le système de notifications"""
        # Timer pour mise à jour temps réel
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)  # Chaque seconde
        
        # Timer pour vérification alertes
        self.alert_timer = QTimer()
        self.alert_timer.timeout.connect(self._check_alerts)
        self.alert_timer.start(60000)  # Chaque minute
    
    def update_datetime(self):
        """Met à jour date/heure"""
        now = datetime.now()
        try:
            self.datetime_label.setText(now.strftime("📅 %d/%m/%Y  🕐 %H:%M:%S"))
        except (UnicodeEncodeError, UnicodeDecodeError):
            # Fallback sans emojis si problème d'encodage
            self.datetime_label.setText(now.strftime("%d/%m/%Y  %H:%M:%S"))
    
    def _load_data(self):
        """Charge les données du dashboard"""
        print("🔄 Chargement données dashboard...")
        
        try:
            # Charger vraies données depuis DB
            if self.db_manager:
                # KPI: Chiffre d'affaires
                ca_result = self.db_manager.execute_query(
                    "SELECT SUM(amount_total) as total FROM account_invoice WHERE state = 'paid'"
                )
                ca = ca_result[0]['total'] if ca_result and ca_result[0]['total'] else 0
                self._update_kpi_value('ca', f"{ca:,.2f} DA")
                
                # KPI: Nombre de factures
                factures = self.db_manager.execute_query(
                    "SELECT COUNT(*) as count FROM account_invoice"
                )
                nb_factures = factures[0]['count'] if factures else 0
                self._update_kpi_value('factures', str(nb_factures))
                
                # KPI: Nombre de clients
                clients = self.db_manager.execute_query(
                    "SELECT COUNT(*) as count FROM res_partner WHERE is_company = 1"
                )
                nb_clients = clients[0]['count'] if clients else 0
                self._update_kpi_value('clients', str(nb_clients))
                
                # KPI: Nombre de produits
                produits = self.db_manager.execute_query(
                    "SELECT COUNT(*) as count FROM product_product WHERE active = 1"
                )
                nb_produits = produits[0]['count'] if produits else 0
                self._update_kpi_value('produits', str(nb_produits))
                
                # Alertes: Stock minimum
                stock_low = self.db_manager.execute_query(
                    "SELECT COUNT(*) as count FROM product_product WHERE qty_available < minimum_stock AND active = 1"
                )
                nb_stock_low = stock_low[0]['count'] if stock_low else 0
                self._update_alert('stock', f"{nb_stock_low} produits")
                
                # Alertes: Maintenances à venir
                maint = self.db_manager.execute_query(
                    "SELECT COUNT(*) as count FROM maintenance_intervention WHERE state = 'scheduled'"
                )
                nb_maint = maint[0]['count'] if maint else 0
                self._update_alert('maintenances', f"{nb_maint} à venir")
                
                # Alertes: Factures impayées
                unpaid = self.db_manager.execute_query(
                    "SELECT SUM(amount_total) as total FROM account_invoice WHERE state = 'open'"
                )
                montant_unpaid = unpaid[0]['total'] if unpaid and unpaid[0]['total'] else 0
                self._update_alert('factures_impayées', f"{montant_unpaid:,.2f} DA")
                
            else:
                # Données d'exemple si pas de DB
                self._update_kpi_value('ca', "2,353,225.00 DA")
                self._update_kpi_value('factures', "11")
                self._update_kpi_value('clients', "13")
                self._update_kpi_value('produits', "8")
                
                self._update_alert('stock', "2 produits")
                self._update_alert('maintenances', "3 à venir")
                self._update_alert('factures_impayées', "150,000 DA")
                
        except Exception as e:
            print(f"⚠️ Erreur chargement données: {e}")
            # Fallback sur données exemple
            self._update_kpi_value('ca', "0.00 DA")
            self._update_kpi_value('factures', "0")
            self._update_kpi_value('clients', "0")
            self._update_kpi_value('produits', "0")
        
        print("✅ Données chargées")
    
    def _update_kpi_value(self, key, value):
        """Met à jour valeur KPI"""
        card = self.kpi_cards.get(key)
        if card:
            value_label = card.findChild(QLabel, f"value_{key}")
            if value_label:
                value_label.setText(value)
    
    def _update_alert(self, key, value):
        """Met à jour valeur alerte"""
        alert_label_name = f"alert_value_{key}"
        # Trouver le label dans les cards d'alerte
        for card in [self.stock_alert_card, self.maint_alert_card, self.unpaid_alert_card]:
            label = card.findChild(QLabel, alert_label_name)
            if label:
                label.setText(value)
                break
    
    def _check_alerts(self):
        """Vérifie et affiche les alertes"""
        # TODO: Implémenter vérifications réelles
        pass
    
    # ========== ÉVÉNEMENTS CLIC ==========
    
    def on_kpi_click(self, data_key):
        """Gère clic sur KPI card"""
        print(f"🖱️ Clic KPI: {data_key}")
        
        actions = {
            'sales': self.show_sales_detail,
            'invoices': self.show_invoices_detail,
            'clients': self.show_clients_detail,
            'products': self.show_products_detail,
        }
        
        action = actions.get(data_key)
        if action:
            action()
    
    def show_sales_detail(self):
        """Affiche détails ventes"""
        try:
            if not self.db_manager:
                QMessageBox.information(self, "Ventes", "📊 Aucune donnée disponible")
                return
            
            # Récupérer stats ventes
            result = self.db_manager.execute_query("""
                SELECT 
                    SUM(amount_total) as total,
                    COUNT(*) as count,
                    AVG(amount_total) as average
                FROM account_invoice 
                WHERE state = 'paid'
            """)
            
            if result and result[0]:
                total = result[0]['total'] or 0
                count = result[0]['count'] or 0
                average = result[0]['average'] or 0
                
                msg = f"""📊 STATISTIQUES VENTES
                
💰 Chiffre d'Affaires Total: {total:,.2f} DA
📄 Nombre de Factures Payées: {count}
📈 Montant Moyen par Vente: {average:,.2f} DA

Pour voir la liste complète, accédez au module Ventes."""
            else:
                msg = "📊 Aucune vente enregistrée"
                
            QMessageBox.information(self, "Détails Ventes", msg)
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur chargement données: {e}")
    
    def show_invoices_detail(self):
        """Affiche détails factures"""
        try:
            from modules.dashboard.detail_windows import InvoicesDetailWindow
            window = InvoicesDetailWindow(self.db_manager, self)
            window.exec()
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur ouverture fenêtre: {e}")
    
    def show_clients_detail(self):
        """Affiche détails clients"""
        try:
            from modules.dashboard.detail_windows import ClientsDetailWindow
            window = ClientsDetailWindow(self.db_manager, self)
            window.exec()
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur ouverture fenêtre: {e}")
    
    def show_products_detail(self):
        """Affiche détails produits"""
        try:
            from modules.dashboard.detail_windows import ProductsDetailWindow
            window = ProductsDetailWindow(self.db_manager, self)
            window.exec()
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur ouverture fenêtre: {e}")
    
    def show_low_stock(self):
        """Affiche produits stock bas"""
        try:
            from modules.dashboard.alert_windows import LowStockAlertWindow
            window = LowStockAlertWindow(self.db_manager, self)
            window.exec()
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur ouverture fenêtre: {e}")
    
    def show_maintenance_schedule(self):
        """Affiche planning maintenances"""
        try:
            from modules.dashboard.alert_windows import MaintenanceAlertWindow
            window = MaintenanceAlertWindow(self.db_manager, self)
            window.exec()
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur ouverture fenêtre: {e}")
    
    def show_unpaid_invoices(self):
        """Affiche factures impayées"""
        try:
            from modules.dashboard.alert_windows import UnpaidInvoicesAlertWindow
            window = UnpaidInvoicesAlertWindow(self.db_manager, self)
            window.exec()
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur ouverture fenêtre: {e}")
    
    def show_sales_chart(self):
        """Affiche graphique ventes"""
        try:
            from modules.dashboard.chart_widgets import SalesChartWindow
            window = SalesChartWindow(self.db_manager, self)
            window.exec()
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur ouverture graphique: {e}")
    
    def show_products_chart(self):
        """Affiche graphique top produits"""
        try:
            from modules.dashboard.chart_widgets import ProductsChartWindow
            window = ProductsChartWindow(self.db_manager, self)
            window.exec()
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur ouverture graphique: {e}")
    
    def show_revenue_chart(self):
        """Affiche graphique CA"""
        try:
            from modules.dashboard.chart_widgets import CAEvolutionChartWindow
            window = CAEvolutionChartWindow(self.db_manager, self)
            window.exec()
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur ouverture graphique: {e}")
    
    def show_notifications(self):
        """Affiche panneau notifications"""
        QMessageBox.information(self, "Notifications",
            "🔔 Centre de notifications:\n\n"
            "• 2 produits en stock bas\n"
            "• 3 maintenances à venir\n"
            "• 2 factures impayées")
    
    def open_module(self, module):
        """Ouvre un module"""
        print(f"🚀 Ouverture module: {module}")
        # TODO: Connecter à la navigation principale
        QMessageBox.information(self, "Module", 
            f"Ouverture module {module.upper()}\n(À implémenter)")
    
    def _show_error_message(self, error_msg):
        """Affiche un message d'erreur dans le widget"""
        # Créer un simple layout si nécessaire
        if not self.layout():
            error_layout = QVBoxLayout(self)
        else:
            error_layout = self.layout()
        
        error_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        error_label = QLabel(f"❌ Erreur de chargement du dashboard\n\n{error_msg}")
        error_label.setStyleSheet("""
            font-size: 16px;
            color: #DC2626;
            padding: 20px;
            background: #FEE2E2;
            border: 2px solid #DC2626;
            border-radius: 10px;
        """)
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_layout.addWidget(error_label)
