# -*- coding: utf-8 -*-
"""
Maintenance Views - Interface Maintenance Machines à Coudre
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QDialog, QFormLayout, QLineEdit, QTextEdit,
    QComboBox, QDateEdit, QDoubleSpinBox, QSpinBox, QMessageBox,
    QScrollArea, QCheckBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QFont
from .controller import MaintenanceController
from datetime import datetime, timedelta


def format_date(date_value):
    """Formate une date (string ou datetime) en DD/MM/YYYY"""
    if not date_value:
        return ""
    
    # Si c'est déjà une string, essayer de la parser
    if isinstance(date_value, str):
        try:
            # Format ISO avec T: 2025-10-20T12:30:00
            if 'T' in date_value:
                dt = datetime.fromisoformat(date_value)
                return dt.strftime("%d/%m/%Y")
            
            # Format avec espace et microsecondes: 2025-10-20 12:30:00.123456
            if ' ' in date_value:
                # Enlever les microsecondes si présentes
                date_str = date_value.split('.')[0]
                dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                return dt.strftime("%d/%m/%Y")
            
            # Format simple: 2025-10-20
            dt = datetime.strptime(date_value, "%Y-%m-%d")
            return dt.strftime("%d/%m/%Y")
        except:
            return date_value  # Retourner tel quel si échec
    
    # Si c'est un objet datetime
    if isinstance(date_value, datetime):
        return date_value.strftime("%d/%m/%Y")
    
    return str(date_value)


class MaintenanceDashboardView(QWidget):
    """Dashboard Maintenance - Vue d'ensemble"""
    
    def __init__(self, module, db_manager):
        super().__init__()
        self.module = module
        self.db_manager = db_manager
        self.controller = MaintenanceController(db_manager)
        self._setup_ui()
    
    def _setup_ui(self):
        """Configure l'interface dashboard"""
        self.setStyleSheet("background-color: #F5F5F5;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(24)
        
        # Header
        header = QHBoxLayout()
        
        title = QLabel("🔧 Dashboard Maintenance")
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: 700;
            color: #1A1A1A;
        """)
        header.addWidget(title)
        
        header.addStretch()
        
        # Barre de recherche
        search_container = QHBoxLayout()
        
        search_icon = QLabel("🔍")
        search_icon.setStyleSheet("font-size: 18px; padding: 5px;")
        search_container.addWidget(search_icon)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔎 Rechercher intervention (Client, ID, Machine...)")
        self.search_input.setMinimumWidth(300)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px 15px;
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                font-size: 13px;
                background: white;
            }
            QLineEdit:focus {
                border: 2px solid #6750A4;
                background: #FAFAFA;
            }
        """)
        self.search_input.textChanged.connect(self.search_interventions)
        search_container.addWidget(self.search_input)
        
        header.addLayout(search_container)
        header.addSpacing(20)
        
        # Bouton Imprimer Dashboard
        print_btn = QPushButton("🖨  Imprimer")
        print_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                background: #5F6368;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background: #4A4F54;
            }
        """)
        print_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        print_btn.clicked.connect(self.print_dashboard)
        header.addWidget(print_btn)
        
        # Bouton Nouvelle Intervention
        new_btn = QPushButton("➕  Nouvelle Intervention")
        new_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                background: #6750A4;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background: #5639A0;
            }
        """)
        new_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        new_btn.clicked.connect(self.create_intervention)
        header.addWidget(new_btn)
        
        layout.addLayout(header)
        
        # KPIs
        try:
            stats = self.controller.get_maintenance_stats()
            print(f"✓ Stats récupérées: {stats}")
        except Exception as e:
            print(f"✗ Erreur stats: {e}")
            stats = {
                'pending_interventions': 0,
                'monthly_interventions': 0,
                'active_contracts': 0,
                'low_stock_parts': 0,
                'monthly_revenue': 0.0
            }
        
        kpi_grid = QGridLayout()
        kpi_grid.setSpacing(20)
        
        self._add_kpi(kpi_grid, 0, 0, "En Cours", str(stats.get('pending_interventions', 0)), "#6750A4", "🛠️", self.show_interventions_pending)
        self._add_kpi(kpi_grid, 0, 1, "Ce Mois", str(stats.get('monthly_interventions', 0)), "#10B981", "📅", self.show_interventions_monthly)
        self._add_kpi(kpi_grid, 0, 2, "Contrats", str(stats.get('active_contracts', 0)), "#2563EB", "📋", self.show_contracts)
        self._add_kpi(kpi_grid, 0, 3, "Stock Bas", str(stats.get('low_stock_parts', 0)), "#F59E0B", "⚠️", self.show_low_stock)
        
        layout.addLayout(kpi_grid)
        
        # Calendrier interventions
        calendar_frame = self._create_calendar_section()
        layout.addWidget(calendar_frame)
        
        layout.addStretch()
    
    def _add_kpi(self, grid, row, col, label_text, value_text, color, emoji="", click_action=None):
        """Ajoute une carte KPI cliquable"""
        print(f"  Création KPI: {emoji} {label_text} = {value_text}")
        
        # Background color avec opacité
        bg_colors = {
            "#6750A4": "rgba(103, 80, 164, 0.08)",  # Violet clair
            "#10B981": "rgba(16, 185, 129, 0.08)",   # Vert clair
            "#2563EB": "rgba(37, 99, 235, 0.08)",    # Bleu clair
            "#F59E0B": "rgba(245, 158, 11, 0.08)"    # Orange clair
        }
        bg_color = bg_colors.get(color, "#FFFFFF")
        
        card = QPushButton()
        card.setObjectName("kpiCard")
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        card.setStyleSheet(f"""
            QPushButton#kpiCard {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {bg_color}, stop:1 #FFFFFF);
                border: 2px solid #E0E0E0;
                border-left: 5px solid {color};
                border-radius: 12px;
                padding: 20px;
                min-height: 120px;
                min-width: 180px;
                text-align: left;
            }}
            QPushButton#kpiCard:hover {{
                border: 2px solid {color};
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {color}, stop:1 {bg_color});
                transform: translateY(-2px);
            }}
            QPushButton#kpiCard:pressed {{
                background: {bg_color};
            }}
        """)
        
        # Connecter au clic
        if click_action:
            card.clicked.connect(click_action)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(8)
        
        # Header avec emoji
        header_layout = QHBoxLayout()
        
        # Emoji icône
        if emoji:
            emoji_label = QLabel(emoji)
            emoji_label.setStyleSheet("""
                font-size: 24px;
                background: transparent;
            """)
            header_layout.addWidget(emoji_label)
        
        # Label titre
        label = QLabel(label_text)
        label.setObjectName("kpiLabel")
        label.setStyleSheet(f"""
            QLabel#kpiLabel {{
                font-size: 11px;
                color: {color};
                font-weight: 700;
                background: transparent;
                letter-spacing: 0.5px;
            }}
        """)
        header_layout.addWidget(label)
        header_layout.addStretch()
        
        card_layout.addLayout(header_layout)
        
        # Valeur
        value = QLabel(value_text)
        value.setObjectName("kpiValue")
        value.setStyleSheet(f"""
            QLabel#kpiValue {{
                font-size: 32px;
                font-weight: 700;
                color: {color};
                background: transparent;
                padding: 8px 0px;
            }}
        """)
        card_layout.addWidget(value)
        
        card_layout.addStretch()
        grid.addWidget(card, row, col)
        
        print(f"    ✓ KPI ajouté: {emoji} visible")
    
    def _create_calendar_section(self):
        """Section calendrier des interventions"""
        frame = QFrame()
        frame.setObjectName("calendarFrame")
        frame.setStyleSheet("""
            QFrame#calendarFrame {
                background-color: #FFFFFF;
                border: 2px solid #E0E0E0;
                border-radius: 10px;
                padding: 24px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(20)
        
        # Header avec icône et titre
        header_layout = QHBoxLayout()
        
        icon_label = QLabel("📅")
        icon_label.setStyleSheet("font-size: 20px;")
        header_layout.addWidget(icon_label)
        
        title = QLabel("Interventions - Semaine")
        title.setStyleSheet("""
            font-size: 16px;
            font-weight: 700;
            color: #1A1A1A;
            background: transparent;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Filtres de date
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)
        
        filter_label = QLabel("📅 Filtrer:")
        filter_label.setStyleSheet("font-weight: 600; color: #1A1A1A;")
        filter_layout.addWidget(filter_label)
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems([
            "📅 Semaine",
            "📅 Mois",
            "📅 Année",
            "🔍 Entre dates",
            "🎯 Toutes"
        ])
        self.filter_combo.setStyleSheet("""
            QComboBox {
                padding: 8px 15px;
                border: 2px solid #E0E0E0;
                border-radius: 6px;
                font-size: 12px;
                min-width: 150px;
            }
            QComboBox:focus {
                border: 2px solid #6750A4;
            }
        """)
        self.filter_combo.currentIndexChanged.connect(self.filter_interventions)
        filter_layout.addWidget(self.filter_combo)
        
        # Dates personnalisées
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addDays(-30))
        self.date_from.setCalendarPopup(True)
        self.date_from.setDisplayFormat("dd/MM/yyyy")
        self.date_from.setVisible(False)
        self.date_from.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 2px solid #E0E0E0;
                border-radius: 6px;
            }
        """)
        filter_layout.addWidget(self.date_from)
        
        date_to_label = QLabel("→")
        date_to_label.setVisible(False)
        filter_layout.addWidget(date_to_label)
        self.date_to_label = date_to_label
        
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setCalendarPopup(True)
        self.date_to.setDisplayFormat("dd/MM/yyyy")
        self.date_to.setVisible(False)
        self.date_to.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 2px solid #E0E0E0;
                border-radius: 6px;
            }
        """)
        filter_layout.addWidget(self.date_to)
        
        # Bouton appliquer filtre dates
        self.apply_date_filter_btn = QPushButton("✅ Appliquer")
        self.apply_date_filter_btn.setVisible(False)
        self.apply_date_filter_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background: #6750A4;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #5639A0;
            }
        """)
        self.apply_date_filter_btn.clicked.connect(self.apply_date_filter)
        filter_layout.addWidget(self.apply_date_filter_btn)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Table interventions
        table = QTableWidget()
        table.setObjectName("interventionsTable")
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels([
            "ID", "Date", "Client", "Machine", "Type", "Tech.", "Statut"
        ])
        
        # Stocker pour recherche
        self.interventions_table = table
        self.all_interventions_data = []
        
        # Style de la table
        table.setStyleSheet("""
            QTableWidget#interventionsTable {
                background-color: #FAFAFA;
                border: 1px solid #E0E0E0;
                border-radius: 5px;
                gridline-color: #E0E0E0;
            }
            QTableWidget#interventionsTable::item {
                padding: 8px;
                border-bottom: 1px solid #F0F0F0;
            }
            QTableWidget#interventionsTable::item:selected {
                background-color: #E8F0FE;
                color: #1A1A1A;
            }
            QHeaderView::section {
                background-color: #F5F5F5;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #E0E0E0;
                font-weight: 700;
                color: #5F6368;
                text-transform: uppercase;
                font-size: 11px;
            }
        """)
        
        # Récupérer interventions semaine
        try:
            today = datetime.now()
            week_end = today + timedelta(days=7)
            interventions = self.controller.get_scheduled_interventions(today, week_end)
            print(f"✓ Interventions semaine: {len(interventions)}")
        except Exception as e:
            print(f"✗ Erreur interventions: {e}")
            interventions = []
        
        table.setRowCount(len(interventions))
        
        if len(interventions) == 0:
            # Message si aucune intervention
            table.setRowCount(1)
            no_data = QTableWidgetItem("Aucune intervention planifiée cette semaine")
            no_data.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setSpan(0, 0, 1, 7)
            table.setItem(0, 0, no_data)
        else:
            # Stocker pour recherche
            self.all_interventions_data = interventions
            
            for i, inter in enumerate(interventions):
                # ID
                id_item = QTableWidgetItem(f"#{inter.id}")
                id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                id_item.setForeground(QColor("#6750A4"))
                id_item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
                table.setItem(i, 0, id_item)
                
                # Date
                date_item = QTableWidgetItem(format_date(inter.date_scheduled))
                date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(i, 1, date_item)
                
                # Client
                table.setItem(i, 2, QTableWidgetItem(inter.partner_name or ""))
                
                # Machine
                table.setItem(i, 3, QTableWidgetItem(inter.machine_name or ""))
                
                # Type
                type_text = "⚙️ Préventive" if inter.intervention_type == "preventive" else "🔧 Corrective"
                table.setItem(i, 4, QTableWidgetItem(type_text))
                
                # Technicien
                table.setItem(i, 5, QTableWidgetItem(inter.technician_name or "Non assigné"))
                
                # Statut avec couleur et badge
                status_map = {
                    'scheduled': ('⏰ Planifiée', '#2563EB', '#E8F0FE'),
                    'in_progress': ('⏳ En cours', '#F59E0B', '#FEF3E8'),
                    'done': ('✅ Terminée', '#10B981', '#E8F5F0'),
                    'cancelled': ('❌ Annulée', '#DC2626', '#FCE8E6')
                }
                status_text, status_color, status_bg = status_map.get(inter.state, (inter.state, '#5F6368', '#F5F5F5'))
                status_item = QTableWidgetItem(status_text)
                status_item.setForeground(QColor(status_color))
                status_item.setBackground(QColor(status_bg))
                status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(i, 6, status_item)
        
        # Ajuster largeurs colonnes
        table.horizontalHeader().setStretchLastSection(True)
        table.setColumnWidth(0, 70)   # ID
        table.setColumnWidth(1, 100)  # Date
        table.setColumnWidth(2, 200)  # Client
        table.setColumnWidth(3, 180)  # Machine
        table.setColumnWidth(4, 130)  # Type
        table.setColumnWidth(5, 150)  # Technicien
        
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        table.setAlternatingRowColors(True)
        table.verticalHeader().setVisible(False)
        table.setMinimumHeight(200)
        
        layout.addWidget(table)
        
        return frame
    
    def create_intervention(self):
        """Créer une nouvelle intervention"""
        from modules.maintenance.dialogs import NewInterventionDialog
        
        dialog = NewInterventionDialog(self.controller, self)
        if dialog.exec():
            # Recharger les interventions
            self.load_dashboard_data()
            print("✅ Intervention créée et dashboard rechargé")
    
    def show_interventions_pending(self):
        """Afficher fenêtre interventions en cours"""
        dialog = InterventionsDetailDialog(self.controller, "pending", self)
        dialog.exec()
    
    def show_interventions_monthly(self):
        """Afficher fenêtre interventions du mois"""
        dialog = InterventionsDetailDialog(self.controller, "monthly", self)
        dialog.exec()
    
    def show_contracts(self):
        """Afficher fenêtre contrats"""
        dialog = ContractsDetailDialog(self.controller, self)
        dialog.exec()
    
    def show_low_stock(self):
        """Afficher fenêtre pièces stock bas"""
        dialog = LowStockDetailDialog(self.controller, self)
        dialog.exec()
    
    def search_interventions(self):
        """Rechercher interventions en temps réel"""
        search_text = self.search_input.text().lower().strip()
        
        if not search_text:
            # Réafficher toutes les interventions
            self._populate_table(self.all_interventions_data)
            return
        
        # Filtrer interventions
        filtered = []
        for inter in self.all_interventions_data:
            # Recherche par ID, client, machine
            if (search_text in str(inter.id).lower() or
                search_text in (inter.partner_name or "").lower() or
                search_text in (inter.machine_name or "").lower() or
                search_text in (inter.intervention_type or "").lower() or
                search_text in (inter.state or "").lower()):
                filtered.append(inter)
        
        self._populate_table(filtered)
        print(f"🔍 Recherche: '{search_text}' -> {len(filtered)} résultats")
    
    def _populate_table(self, interventions):
        """Remplit la table avec les interventions"""
        table = self.interventions_table
        table.setRowCount(len(interventions))
        
        if len(interventions) == 0:
            table.setRowCount(1)
            no_data = QTableWidgetItem("🔍 Aucun résultat trouvé")
            no_data.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setSpan(0, 0, 1, 7)
            table.setItem(0, 0, no_data)
            return
        
        for i, inter in enumerate(interventions):
            # ID
            id_item = QTableWidgetItem(f"#{inter.id}")
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            id_item.setForeground(QColor("#6750A4"))
            id_item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            table.setItem(i, 0, id_item)
            
            # Date
            date_item = QTableWidgetItem(format_date(inter.date_scheduled))
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(i, 1, date_item)
            
            # Client
            table.setItem(i, 2, QTableWidgetItem(inter.partner_name or ""))
            
            # Machine
            table.setItem(i, 3, QTableWidgetItem(inter.machine_name or ""))
            
            # Type
            type_text = "⚙️ Préventive" if inter.intervention_type == "preventive" else "🔧 Corrective"
            table.setItem(i, 4, QTableWidgetItem(type_text))
            
            # Technicien
            table.setItem(i, 5, QTableWidgetItem(inter.technician_name or "Non assigné"))
            
            # Statut avec couleur
            status_map = {
                'scheduled': ('⏰ Planifiée', '#2563EB', '#E8F0FE'),
                'in_progress': ('⏳ En cours', '#F59E0B', '#FEF3E8'),
                'done': ('✅ Terminée', '#10B981', '#E8F5F0'),
                'cancelled': ('❌ Annulée', '#DC2626', '#FCE8E6')
            }
            status_text, status_color, status_bg = status_map.get(inter.state, (inter.state, '#5F6368', '#F5F5F5'))
            status_item = QTableWidgetItem(status_text)
            status_item.setForeground(QColor(status_color))
            status_item.setBackground(QColor(status_bg))
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(i, 6, status_item)
    
    def print_dashboard(self):
        """Imprimer le dashboard en PDF"""
        from modules.maintenance.reports import MaintenanceReportGenerator
        
        generator = MaintenanceReportGenerator(self.controller)
        pdf_path = generator.generate_dashboard_report()
        
        if pdf_path:
            QMessageBox.information(self, "Impression", f"🖨 Rapport généré:\n{pdf_path}")
        else:
            QMessageBox.warning(self, "Erreur", "Impossible de générer le rapport")
    
    def filter_interventions(self):
        """Écouteur changement filtre"""
        filter_type = self.filter_combo.currentIndex()
        
        # Masquer/Afficher dates personnalisées
        if filter_type == 3:  # Entre dates
            self.date_from.setVisible(True)
            self.date_to_label.setVisible(True)
            self.date_to.setVisible(True)
            self.apply_date_filter_btn.setVisible(True)
        else:
            self.date_from.setVisible(False)
            self.date_to_label.setVisible(False)
            self.date_to.setVisible(False)
            self.apply_date_filter_btn.setVisible(False)
            # Appliquer filtre directement
            self.apply_filter()
    
    def apply_date_filter(self):
        """Applique le filtre de dates personnalisées"""
        self.apply_filter()
    
    def apply_filter(self):
        """Applique le filtre sélectionné"""
        filter_type = self.filter_combo.currentIndex()
        today = datetime.now()
        
        if filter_type == 0:  # Semaine
            start_date = today
            end_date = today + timedelta(days=7)
        elif filter_type == 1:  # Mois
            start_date = today.replace(day=1)
            end_date = (today.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        elif filter_type == 2:  # Année
            start_date = today.replace(month=1, day=1)
            end_date = today.replace(month=12, day=31)
        elif filter_type == 3:  # Entre dates
            start_date = self.date_from.date().toPyDate()
            start_date = datetime.combine(start_date, datetime.min.time())
            end_date = self.date_to.date().toPyDate()
            end_date = datetime.combine(end_date, datetime.max.time())
        else:  # Toutes
            # Afficher toutes
            self._populate_table(self.all_interventions_data)
            return
        
        # Filtrer interventions
        try:
            interventions = self.controller.get_scheduled_interventions(start_date, end_date)
            self._populate_table(interventions)
            print(f"✅ Filtre appliqué: {len(interventions)} interventions")
        except Exception as e:
            print(f"❌ Erreur filtre: {e}")
            self._populate_table([])
    
    def load_dashboard_data(self):
        """Recharge toutes les données du dashboard"""
        # Recharger la table
        try:
            today = datetime.now()
            week_end = today + timedelta(days=7)
            interventions = self.controller.get_scheduled_interventions(today, week_end)
            self.all_interventions_data = interventions
            self._populate_table(interventions)
            print(f"✅ Dashboard rechargé: {len(interventions)} interventions")
        except Exception as e:
            print(f"❌ Erreur rechargement: {e}")


class MaintenanceInterventionListView(QWidget):
    """Liste des interventions de maintenance"""
    
    def __init__(self, module, db_manager):
        super().__init__()
        self.module = module
        self.db_manager = db_manager
        self.controller = MaintenanceController(db_manager)
        self._setup_ui()
        self.load_interventions()
    
    def _setup_ui(self):
        """Configure l'interface"""
        self.setStyleSheet("background-color: #F5F5F5;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(20)
        
        # Header
        header = QHBoxLayout()
        
        title = QLabel("🛠️ Interventions de Maintenance")
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: 700;
            color: #1A1A1A;
        """)
        header.addWidget(title)
        
        header.addStretch()
        
        # Filtres
        self.state_filter = QComboBox()
        self.state_filter.addItems(["Tous", "Planifié", "En cours", "Terminé"])
        self.state_filter.currentTextChanged.connect(self.load_interventions)
        header.addWidget(self.state_filter)
        
        # Bouton Nouveau
        new_btn = QPushButton("+ Nouvelle Intervention")
        new_btn.setObjectName("primaryBtn")
        new_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        new_btn.clicked.connect(self.create_intervention)
        header.addWidget(new_btn)
        
        layout.addLayout(header)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "N°", "Date", "Client", "Machine", "Type", "Technicien", "Montant", "Statut"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.doubleClicked.connect(self.view_intervention)
        
        layout.addWidget(self.table)
    
    def load_interventions(self):
        """Charge les interventions"""
        state_map = {
            "Planifié": "scheduled",
            "En cours": "in_progress",
            "Terminé": "done"
        }
        state = state_map.get(self.state_filter.currentText())
        
        interventions = self.controller.get_all_interventions(state)
        
        self.table.setRowCount(len(interventions))
        for i, inter in enumerate(interventions):
            self.table.setItem(i, 0, QTableWidgetItem(str(inter.id)))
            self.table.setItem(i, 1, QTableWidgetItem(format_date(inter.date_scheduled)))
            self.table.setItem(i, 2, QTableWidgetItem(inter.partner_name or ""))
            self.table.setItem(i, 3, QTableWidgetItem(inter.machine_name or ""))
            self.table.setItem(i, 4, QTableWidgetItem(inter.intervention_type))
            self.table.setItem(i, 5, QTableWidgetItem(inter.technician_name))
            self.table.setItem(i, 6, QTableWidgetItem(f"{inter.total_cost:,.2f} DA"))
            self.table.setItem(i, 7, QTableWidgetItem(inter.state))
    
    def create_intervention(self):
        """Créer nouvelle intervention"""
        QMessageBox.information(self, "Info", "Dialogue création à implémenter")
    
    def view_intervention(self):
        """Voir détails intervention"""
        row = self.table.currentRow()
        if row >= 0:
            inter_id = int(self.table.item(row, 0).text())
            QMessageBox.information(self, "Info", f"Voir intervention #{inter_id}")


class MaintenanceContractListView(QWidget):
    """Liste des contrats de maintenance"""
    
    def __init__(self, module, db_manager):
        super().__init__()
        self.module = module
        self.db_manager = db_manager
        self.controller = MaintenanceController(db_manager)
        self._setup_ui()
        self.load_contracts()
    
    def _setup_ui(self):
        """Configure l'interface"""
        self.setStyleSheet("background-color: #F5F5F5;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(20)
        
        # Header
        header = QHBoxLayout()
        
        title = QLabel("📋 Contrats de Maintenance")
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: 700;
            color: #1A1A1A;
        """)
        header.addWidget(title)
        
        header.addStretch()
        
        # Bouton Nouveau
        new_btn = QPushButton("+ Nouveau Contrat")
        new_btn.setObjectName("primaryBtn")
        new_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        new_btn.clicked.connect(self.create_contract)
        header.addWidget(new_btn)
        
        layout.addLayout(header)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Référence", "Client", "Type", "Début", "Fin", "Montant", "Statut"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        layout.addWidget(self.table)
    
    def load_contracts(self):
        """Charge les contrats"""
        contracts = self.controller.get_all_contracts()
        
        self.table.setRowCount(len(contracts))
        for i, contract in enumerate(contracts):
            self.table.setItem(i, 0, QTableWidgetItem(contract.reference or ""))
            self.table.setItem(i, 1, QTableWidgetItem(contract.partner_name or ""))
            self.table.setItem(i, 2, QTableWidgetItem(contract.contract_type or ""))
            self.table.setItem(i, 3, QTableWidgetItem(format_date(contract.date_start)))
            self.table.setItem(i, 4, QTableWidgetItem(format_date(contract.date_end)))
            self.table.setItem(i, 5, QTableWidgetItem(f"{contract.total_amount:,.2f} DA"))
            self.table.setItem(i, 6, QTableWidgetItem(contract.state or ""))
    
    def create_contract(self):
        """Créer nouveau contrat"""
        QMessageBox.information(self, "Info", "Dialogue création contrat à implémenter")


class MachinePartListView(QWidget):
    """Liste des pièces de rechange"""
    
    def __init__(self, module, db_manager):
        super().__init__()
        self.module = module
        self.db_manager = db_manager
        self.controller = MaintenanceController(db_manager)
        self._setup_ui()
        self.load_parts()
    
    def _setup_ui(self):
        """Configure l'interface"""
        self.setStyleSheet("background-color: #F5F5F5;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(20)
        
        # Header
        header = QHBoxLayout()
        
        title = QLabel("🔩 Pièces de Rechange")
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: 700;
            color: #1A1A1A;
        """)
        header.addWidget(title)
        
        header.addStretch()
        
        # Alerte stock
        low_stock = self.controller.get_low_stock_parts()
        if low_stock:
            alert = QLabel(f"⚠️ {len(low_stock)} pièces en stock faible")
            alert.setStyleSheet("""
                background-color: #FEF7E0;
                color: #F9AB00;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 600;
            """)
            header.addWidget(alert)
        
        # Bouton Nouveau
        new_btn = QPushButton("+ Nouvelle Pièce")
        new_btn.setObjectName("primaryBtn")
        new_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        new_btn.clicked.connect(self.create_part)
        header.addWidget(new_btn)
        
        layout.addLayout(header)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Référence", "Nom", "Catégorie", "Stock", "Stock Min", "Prix Vente", "Fournisseur"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        layout.addWidget(self.table)
    
    def load_parts(self):
        """Charge les pièces"""
        parts = self.controller.get_all_parts()
        
        self.table.setRowCount(len(parts))
        for i, part in enumerate(parts):
            self.table.setItem(i, 0, QTableWidgetItem(part.reference or ""))
            self.table.setItem(i, 1, QTableWidgetItem(part.name))
            self.table.setItem(i, 2, QTableWidgetItem(part.category))
            
            # Stock avec couleur
            stock_item = QTableWidgetItem(str(part.quantity))
            if part.quantity <= part.min_quantity:
                stock_item.setBackground(QColor("#FCE8E6"))
                stock_item.setForeground(QColor("#D93025"))
            self.table.setItem(i, 3, stock_item)
            
            self.table.setItem(i, 4, QTableWidgetItem(str(part.min_quantity)))
            self.table.setItem(i, 5, QTableWidgetItem(f"{part.sale_price:,.2f} DA"))
            self.table.setItem(i, 6, QTableWidgetItem(part.supplier_name or ""))
    
    def create_part(self):
        """Créer nouvelle pièce"""
        QMessageBox.information(self, "Info", "Dialogue création pièce à implémenter")


# ============================================================================
# DIALOGUES DE DÉTAILS POUR KPIs CLIQUABLES
# ============================================================================

class InterventionsDetailDialog(QDialog):
    """Dialogue détails interventions"""
    
    def __init__(self, controller, filter_type, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.filter_type = filter_type
        self._setup_ui()
        self.load_data()
    
    def _setup_ui(self):
        """Configure l'interface"""
        self.setWindowTitle("Détails Interventions")
        self.setMinimumSize(900, 500)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Header
        if self.filter_type == "pending":
            title = QLabel("🛠️ Interventions En Cours")
        else:
            title = QLabel("📅 Interventions Ce Mois")
        
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #1A1A1A;
        """)
        layout.addWidget(title)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Date", "Client", "Machine", "Type", "Statut", "Coût"
        ])
        
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #FAFAFA;
                border: 1px solid #E0E0E0;
                gridline-color: #E0E0E0;
            }
            QHeaderView::section {
                background-color: #F5F5F5;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #E0E0E0;
                font-weight: 700;
                color: #5F6368;
            }
        """)
        
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.doubleClicked.connect(self.edit_intervention)
        
        layout.addWidget(self.table)
        
        # Boutons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        # Bouton Imprimer
        print_btn = QPushButton("🖨  Imprimer")
        print_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 20px;
                background: #6750A4;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #5639A0;
            }
        """)
        print_btn.clicked.connect(self.print_interventions)
        btn_layout.addWidget(print_btn)
        
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 20px;
                background: #E0E0E0;
                border: none;
                border-radius: 5px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #D0D0D0;
            }
        """)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
    
    def load_data(self):
        """Charge les données"""
        if self.filter_type == "pending":
            interventions = self.controller.get_all_interventions("in_progress")
            scheduled = self.controller.get_all_interventions("scheduled")
            interventions.extend(scheduled)
        else:
            interventions = self.controller.get_all_interventions()
        
        self.table.setRowCount(len(interventions))
        for i, inter in enumerate(interventions):
            self.table.setItem(i, 0, QTableWidgetItem(str(inter.id)))
            self.table.setItem(i, 1, QTableWidgetItem(format_date(inter.date_scheduled)))
            self.table.setItem(i, 2, QTableWidgetItem(inter.partner_name or ""))
            self.table.setItem(i, 3, QTableWidgetItem(inter.machine_name or ""))
            self.table.setItem(i, 4, QTableWidgetItem(inter.intervention_type or ""))
            self.table.setItem(i, 5, QTableWidgetItem(inter.state or ""))
            self.table.setItem(i, 6, QTableWidgetItem(f"{inter.total_cost:,.0f} DA"))
    
    def edit_intervention(self):
        """Éditer intervention (double-clic)"""
        row = self.table.currentRow()
        if row >= 0:
            inter_id = int(self.table.item(row, 0).text().replace('#', ''))
            QMessageBox.information(self, "Édition", f"Édition intervention #{inter_id}")
    
    def print_interventions(self):
        """Imprimer liste interventions"""
        from modules.maintenance.reports import MaintenanceReportGenerator
        
        generator = MaintenanceReportGenerator(self.controller)
        pdf_path = generator.generate_monthly_report()
        
        if pdf_path:
            QMessageBox.information(self, "Impression", f"🖨 Rapport généré:\n{pdf_path}")
        else:
            QMessageBox.warning(self, "Erreur", "Impossible de générer le rapport")


class ContractsDetailDialog(QDialog):
    """Dialogue détails contrats"""
    
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self._setup_ui()
        self.load_data()
    
    def _setup_ui(self):
        """Configure l'interface"""
        self.setWindowTitle("Contrats de Maintenance")
        self.setMinimumSize(900, 500)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Header
        title = QLabel("📋 Contrats Actifs")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #1A1A1A;
        """)
        layout.addWidget(title)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Réf", "Client", "Type", "Début", "Fin", "Montant", "Statut"
        ])
        
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #FAFAFA;
                border: 1px solid #E0E0E0;
                gridline-color: #E0E0E0;
            }
            QHeaderView::section {
                background-color: #F5F5F5;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #E0E0E0;
                font-weight: 700;
                color: #5F6368;
            }
        """)
        
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.doubleClicked.connect(self.edit_contract)
        
        layout.addWidget(self.table)
        
        # Boutons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 20px;
                background: #E0E0E0;
                border: none;
                border-radius: 5px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #D0D0D0;
            }
        """)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
    
    def load_data(self):
        """Charge les contrats"""
        contracts = self.controller.get_all_contracts()
        
        self.table.setRowCount(len(contracts))
        for i, contract in enumerate(contracts):
            self.table.setItem(i, 0, QTableWidgetItem(contract.reference or ""))
            self.table.setItem(i, 1, QTableWidgetItem(contract.partner_name or ""))
            self.table.setItem(i, 2, QTableWidgetItem(contract.contract_type or ""))
            self.table.setItem(i, 3, QTableWidgetItem(format_date(contract.date_start)))
            self.table.setItem(i, 4, QTableWidgetItem(format_date(contract.date_end)))
            self.table.setItem(i, 5, QTableWidgetItem(f"{contract.total_amount:,.0f} DA"))
            self.table.setItem(i, 6, QTableWidgetItem(contract.state or ""))
    
    def edit_contract(self):
        """Éditer contrat (double-clic)"""
        row = self.table.currentRow()
        if row >= 0:
            ref = self.table.item(row, 0).text()
            QMessageBox.information(self, "Édition", f"Édition contrat {ref}")


class LowStockDetailDialog(QDialog):
    """Dialogue pièces stock bas"""
    
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self._setup_ui()
        self.load_data()
    
    def _setup_ui(self):
        """Configure l'interface"""
        self.setWindowTitle("Pièces en Stock Bas")
        self.setMinimumSize(900, 500)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Header avec alerte
        header_layout = QHBoxLayout()
        
        title = QLabel("⚠️ Pièces en Alerte Stock")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #1A1A1A;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Réf", "Nom", "Catégorie", "Stock", "Min", "Prix", "Fournisseur"
        ])
        
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #FAFAFA;
                border: 1px solid #E0E0E0;
                gridline-color: #E0E0E0;
            }
            QHeaderView::section {
                background-color: #F5F5F5;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #E0E0E0;
                font-weight: 700;
                color: #5F6368;
            }
        """)
        
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.doubleClicked.connect(self.edit_part)
        
        layout.addWidget(self.table)
        
        # Boutons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        order_btn = QPushButton("Commander")
        order_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 20px;
                background: #F59E0B;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #D97706;
            }
        """)
        btn_layout.addWidget(order_btn)
        
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 20px;
                background: #E0E0E0;
                border: none;
                border-radius: 5px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #D0D0D0;
            }
        """)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
    
    def load_data(self):
        """Charge les pièces en stock bas"""
        parts = self.controller.get_low_stock_parts()
        
        self.table.setRowCount(len(parts))
        for i, part in enumerate(parts):
            self.table.setItem(i, 0, QTableWidgetItem(part.reference or ""))
            self.table.setItem(i, 1, QTableWidgetItem(part.name))
            self.table.setItem(i, 2, QTableWidgetItem(part.category or ""))
            
            # Stock en rouge
            stock_item = QTableWidgetItem(str(part.quantity))
            stock_item.setBackground(QColor("#FCE8E6"))
            stock_item.setForeground(QColor("#D93025"))
            self.table.setItem(i, 3, stock_item)
            
            self.table.setItem(i, 4, QTableWidgetItem(str(part.min_quantity)))
            self.table.setItem(i, 5, QTableWidgetItem(f"{part.purchase_price:,.0f} DA"))
            self.table.setItem(i, 6, QTableWidgetItem(part.supplier_name or ""))
    
    def edit_part(self):
        """Éditer pièce (double-clic)"""
        row = self.table.currentRow()
        if row >= 0:
            ref = self.table.item(row, 0).text()
            QMessageBox.information(self, "Édition", f"Édition pièce {ref}")
