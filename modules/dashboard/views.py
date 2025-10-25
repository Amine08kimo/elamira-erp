# -*- coding: utf-8 -*-
"""
Dashboard Views - VERSION ÉQUILIBRÉE
Polices lisibles, Boxes généreuses, Design professionnel
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QPushButton, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class DashboardView(QWidget):
    """Vue Dashboard - Version équilibrée et professionnelle"""
    
    def __init__(self, module, db_manager):
        super().__init__()
        self.module = module
        self.db_manager = db_manager
        self._setup_ui()
    
    def _setup_ui(self):
        """Configure l'interface dashboard équilibrée"""
        self.setStyleSheet("background-color: #F5F5F5;")
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        content_widget = QWidget()
        scroll.setWidget(content_widget)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
        
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(28)
        
        # ===== HEADER =====
        header_layout = QHBoxLayout()
        header_layout.setSpacing(16)
        
        # Titre équilibré
        title = QLabel("📊 Tableau de Bord")
        title.setObjectName("pageTitle")
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: 700;
            color: #1A1A1A;
            padding: 0px;
            background-color: transparent;
        """)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Bouton Actualiser équilibré
        refresh_btn = QPushButton("🔄 Actualiser")
        refresh_btn.setObjectName("primaryBtn")
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #6750A4;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 15px;
                font-weight: 700;
                min-height: 38px;
            }
            QPushButton:hover {
                background-color: #5746A6;
            }
            QPushButton:pressed {
                background-color: #4B3C96;
            }
        """)
        refresh_btn.clicked.connect(self._refresh_data)
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        # ===== KPI CARDS - Boxes généreuses =====
        kpi_grid = QGridLayout()
        kpi_grid.setSpacing(20)
        kpi_grid.setContentsMargins(0, 0, 0, 0)
        
        # Statistiques
        stats = self._get_statistics()
        
        self._add_kpi_card(
            kpi_grid, 0, 0,
            "💰 CHIFFRE D'AFFAIRES",
            f"{stats['ca']:,.2f} DA",
            "#6750A4",
            "Ce mois"
        )
        
        self._add_kpi_card(
            kpi_grid, 0, 1,
            "📄 FACTURES",
            str(stats['factures']),
            "#10B981",
            "Total actif"
        )
        
        self._add_kpi_card(
            kpi_grid, 0, 2,
            "👥 CLIENTS",
            str(stats['clients']),
            "#2563EB",
            "Enregistrés"
        )
        
        self._add_kpi_card(
            kpi_grid, 0, 3,
            "📦 PRODUITS",
            str(stats['produits']),
            "#F59E0B",
            "En stock"
        )
        
        layout.addLayout(kpi_grid)
        
        # ===== STATISTIQUES =====
        stats_frame = self._create_stats_section()
        layout.addWidget(stats_frame)
        
        # ===== ACTIONS RAPIDES =====
        actions_frame = self._create_quick_actions()
        layout.addWidget(actions_frame)
        
        layout.addStretch()
    
    def _add_kpi_card(self, grid_layout, row, col, label_text, value_text, color, subtitle=""):
        """Carte KPI équilibrée - Box généreuse"""
        card = QFrame()
        card.setObjectName("kpiCard")
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        card.setStyleSheet(f"""
            QFrame#kpiCard {{
                background-color: #FFFFFF;
                border: 2px solid #E0E0E0;
                border-left: 5px solid {color};
                border-radius: 10px;
                padding: 28px;
                min-height: 150px;
                min-width: 220px;
            }}
            QFrame#kpiCard:hover {{
                border-color: {color};
                border-left-color: {color};
                background-color: #FAFAFA;
            }}
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(14)
        card_layout.setContentsMargins(0, 0, 0, 0)
        
        # Label
        label = QLabel(label_text)
        label.setStyleSheet("""
            font-size: 12px;
            color: #5F6368;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            background-color: transparent;
        """)
        card_layout.addWidget(label)
        
        # Valeur équilibrée
        value = QLabel(value_text)
        value.setStyleSheet(f"""
            font-size: 28px;
            font-weight: 700;
            color: {color};
            padding: 6px 0px;
            background-color: transparent;
        """)
        card_layout.addWidget(value)
        
        # Sous-titre
        if subtitle:
            sub = QLabel(subtitle)
            sub.setStyleSheet("""
                font-size: 13px;
                color: #9AA0A6;
                font-weight: 500;
                background-color: transparent;
            """)
            card_layout.addWidget(sub)
        
        card_layout.addStretch()
        
        grid_layout.addWidget(card, row, col)
    
    def _create_stats_section(self):
        """Section statistiques - Box généreuse"""
        frame = QFrame()
        frame.setObjectName("card")
        frame.setStyleSheet("""
            QFrame#card {
                background-color: #FFFFFF;
                border: 2px solid #E0E0E0;
                border-radius: 10px;
                padding: 28px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(20)
        
        # Titre
        title = QLabel("📈 Statistiques de Vente")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #1A1A1A;
            padding-bottom: 10px;
            background-color: transparent;
        """)
        layout.addWidget(title)
        
        # Placeholder
        chart_placeholder = QLabel("📊 Graphique des ventes\n(À implémenter avec matplotlib)")
        chart_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart_placeholder.setStyleSheet("""
            color: #9AA0A6;
            font-size: 16px;
            font-weight: 600;
            padding: 70px;
            background-color: #F9F9F9;
            border-radius: 8px;
            border: 2px dashed #D0D0D0;
        """)
        layout.addWidget(chart_placeholder)
        
        return frame
    
    def _create_quick_actions(self):
        """Actions rapides - Boutons avec icônes"""
        frame = QFrame()
        frame.setObjectName("card")
        frame.setStyleSheet("""
            QFrame#card {
                background-color: #FFFFFF;
                border: 2px solid #E0E0E0;
                border-radius: 10px;
                padding: 28px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(20)
        
        # Titre
        title = QLabel("⚡ Actions Rapides")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #1A1A1A;
            padding-bottom: 10px;
            background-color: transparent;
        """)
        layout.addWidget(title)
        
        # Grid de boutons
        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(14)
        
        actions = [
            ("📄 Nouvelle Facture", "#6750A4"),
            ("👤 Nouveau Client", "#10B981"),
            ("📦 Ajouter Produit", "#F59E0B"),
            ("📊 Voir Rapports", "#2563EB"),
        ]
        
        for idx, (text, color) in enumerate(actions):
            btn = QPushButton(text)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 16px 22px;
                    font-size: 14px;
                    font-weight: 700;
                    min-height: 48px;
                    text-align: left;
                }}
                QPushButton:hover {{
                    background-color: {color};
                    opacity: 0.9;
                }}
                QPushButton:pressed {{
                    transform: scale(0.98);
                }}
            """)
            row = idx // 2
            col = idx % 2
            buttons_layout.addWidget(btn, row, col)
        
        layout.addLayout(buttons_layout)
        
        return frame
    
    def _get_statistics(self):
        """Récupère les statistiques"""
        try:
            ca_result = self.db_manager.fetch_one("""
                SELECT COALESCE(SUM(amount_total), 0) as total
                FROM sale_order
                WHERE state != 'cancelled'
            """)
            ca = ca_result['total'] if ca_result else 0
            
            factures_result = self.db_manager.fetch_one("""
                SELECT COUNT(*) as count
                FROM sale_order
                WHERE state != 'cancelled'
            """)
            factures = factures_result['count'] if factures_result else 0
            
            clients_result = self.db_manager.fetch_one("""
                SELECT COUNT(*) as count
                FROM res_partner
                WHERE is_customer = 1 AND active = 1
            """)
            clients = clients_result['count'] if clients_result else 0
            
            produits_result = self.db_manager.fetch_one("""
                SELECT COUNT(*) as count
                FROM product_product
                WHERE active = 1
            """)
            produits = produits_result['count'] if produits_result else 0
            
            return {
                'ca': ca,
                'factures': factures,
                'clients': clients,
                'produits': produits
            }
        except Exception as e:
            print(f"Erreur statistiques: {e}")
            return {
                'ca': 0,
                'factures': 0,
                'clients': 0,
                'produits': 0
            }
    
    def _refresh_data(self):
        """Actualise les données"""
        print("🔄 Actualisation des données...")
        stats = self._get_statistics()
        print(f"✓ Stats: CA={stats['ca']} DA, Factures={stats['factures']}")
