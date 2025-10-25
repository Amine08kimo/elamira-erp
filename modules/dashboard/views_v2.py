# -*- coding: utf-8 -*-
"""
Dashboard Views V2 - ULTRA LISIBLE
Textes GRANDS, Boutons CLIQUABLES, Design MODERNE
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QPushButton, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class DashboardView(QWidget):
    """Vue principale du tableau de bord - VERSION ULTRA LISIBLE"""
    
    def __init__(self, module, db_manager):
        super().__init__()
        self.module = module
        self.db_manager = db_manager
        self._setup_ui()
    
    def _setup_ui(self):
        """Configure l'interface du dashboard - Version professionnelle"""
        self.setStyleSheet("background-color: #F5F5F5;")
        
        # Scroll area pour contenu
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
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(32)
        
        # ===== HEADER AVEC TITRE ET ACTIONS =====
        header_layout = QHBoxLayout()
        header_layout.setSpacing(16)
        
        # Titre GRAND
        title = QLabel("📊 Tableau de Bord")
        title.setObjectName("pageTitle")
        title.setStyleSheet("""
            font-size: 32px;
            font-weight: 700;
            color: #1A1A1A;
            padding: 0px;
            background-color: transparent;
        """)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Bouton Actualiser - GRAND et CLIQUABLE
        refresh_btn = QPushButton("🔄 Actualiser")
        refresh_btn.setObjectName("primaryBtn")
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #6750A4;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 16px 32px;
                font-size: 16px;
                font-weight: 700;
                min-height: 48px;
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
        
        # ===== KPI CARDS - GRANDES ET LISIBLES =====
        kpi_grid = QGridLayout()
        kpi_grid.setSpacing(24)
        kpi_grid.setContentsMargins(0, 0, 0, 0)
        
        # Récupérer les vraies données
        stats = self._get_statistics()
        
        # 4 KPIs principales
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
        
        # ===== STATISTIQUES DÉTAILLÉES =====
        stats_frame = self._create_stats_section()
        layout.addWidget(stats_frame)
        
        # ===== ACTIONS RAPIDES =====
        actions_frame = self._create_quick_actions()
        layout.addWidget(actions_frame)
        
        # Spacer
        layout.addStretch()
    
    def _add_kpi_card(self, grid_layout, row, col, label_text, value_text, color, subtitle=""):
        """Crée une GRANDE carte KPI ultra-lisible"""
        card = QFrame()
        card.setObjectName("kpiCard")
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        card.setStyleSheet(f"""
            QFrame#kpiCard {{
                background-color: #FFFFFF;
                border: 3px solid #E0E0E0;
                border-left: 8px solid {color};
                border-radius: 12px;
                padding: 28px;
                min-height: 160px;
            }}
            QFrame#kpiCard:hover {{
                border-color: {color};
                border-left-color: {color};
                background-color: #FAFAFA;
                transform: translateY(-2px);
            }}
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(16)
        card_layout.setContentsMargins(0, 0, 0, 0)
        
        # Label - GRANDE taille
        label = QLabel(label_text)
        label.setStyleSheet("""
            font-size: 14px;
            color: #5F6368;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            background-color: transparent;
        """)
        card_layout.addWidget(label)
        
        # Valeur - TRÈS GRANDE
        value = QLabel(value_text)
        value.setStyleSheet(f"""
            font-size: 42px;
            font-weight: 700;
            color: {color};
            padding: 8px 0px;
            background-color: transparent;
        """)
        card_layout.addWidget(value)
        
        # Sous-titre
        if subtitle:
            sub = QLabel(subtitle)
            sub.setStyleSheet("""
                font-size: 14px;
                color: #9AA0A6;
                font-weight: 500;
                background-color: transparent;
            """)
            card_layout.addWidget(sub)
        
        card_layout.addStretch()
        
        grid_layout.addWidget(card, row, col)
    
    def _create_stats_section(self):
        """Section statistiques détaillées"""
        frame = QFrame()
        frame.setObjectName("card")
        frame.setStyleSheet("""
            QFrame#card {
                background-color: #FFFFFF;
                border: 2px solid #E0E0E0;
                border-radius: 12px;
                padding: 32px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(24)
        
        # Titre
        title = QLabel("📈 Statistiques de Vente")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: 700;
            color: #1A1A1A;
            padding-bottom: 12px;
            background-color: transparent;
        """)
        layout.addWidget(title)
        
        # Placeholder graphique
        chart_placeholder = QLabel("📊 Graphique des ventes\n(À implémenter avec matplotlib)")
        chart_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart_placeholder.setStyleSheet("""
            color: #9AA0A6;
            font-size: 18px;
            font-weight: 600;
            padding: 80px;
            background-color: #F9F9F9;
            border-radius: 8px;
            border: 2px dashed #D0D0D0;
        """)
        layout.addWidget(chart_placeholder)
        
        return frame
    
    def _create_quick_actions(self):
        """Section actions rapides"""
        frame = QFrame()
        frame.setObjectName("card")
        frame.setStyleSheet("""
            QFrame#card {
                background-color: #FFFFFF;
                border: 2px solid #E0E0E0;
                border-radius: 12px;
                padding: 32px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(24)
        
        # Titre
        title = QLabel("⚡ Actions Rapides")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: 700;
            color: #1A1A1A;
            padding-bottom: 12px;
            background-color: transparent;
        """)
        layout.addWidget(title)
        
        # Grid de boutons
        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(16)
        
        # Boutons d'action - GRANDS et CLIQUABLES
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
                    padding: 20px 28px;
                    font-size: 16px;
                    font-weight: 700;
                    min-height: 56px;
                    text-align: left;
                }}
                QPushButton:hover {{
                    background-color: {color};
                    opacity: 0.9;
                    transform: scale(1.02);
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
        """Récupère les statistiques réelles"""
        try:
            # CA total
            ca_result = self.db_manager.fetch_one("""
                SELECT COALESCE(SUM(amount_total), 0) as total
                FROM sale_order
                WHERE state != 'cancelled'
            """)
            ca = ca_result['total'] if ca_result else 0
            
            # Nombre de factures
            factures_result = self.db_manager.fetch_one("""
                SELECT COUNT(*) as count
                FROM sale_order
                WHERE state != 'cancelled'
            """)
            factures = factures_result['count'] if factures_result else 0
            
            # Nombre de clients
            clients_result = self.db_manager.fetch_one("""
                SELECT COUNT(*) as count
                FROM res_partner
                WHERE is_customer = 1 AND active = 1
            """)
            clients = clients_result['count'] if clients_result else 0
            
            # Nombre de produits
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
        """Actualise les données du dashboard"""
        print("🔄 Actualisation des données...")
        # Recharger les statistiques
        stats = self._get_statistics()
        print(f"✓ Stats: CA={stats['ca']} DA, Factures={stats['factures']}")
        # TODO: Mettre à jour les KPIs
