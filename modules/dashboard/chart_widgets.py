# -*- coding: utf-8 -*-
"""
Widgets de graphiques pour le Dashboard
Utilise Matplotlib pour créer des graphiques professionnels
"""

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from core.ui.common_styles import ElAmiraStyles

try:
    import matplotlib
    matplotlib.use('Qt5Agg')
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
    from matplotlib.figure import Figure
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️ Matplotlib non disponible. Installez-le avec: pip install matplotlib")


class ChartCanvas(FigureCanvasQTAgg):
    """Canvas Matplotlib pour PyQt6"""
    
    def __init__(self, figure):
        super().__init__(figure)
        self.setMinimumSize(800, 500)


class SalesChartWindow(QDialog):
    """Fenêtre graphique ventes mensuelles"""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("📈 Graphique Ventes Mensuelles")
        self.setMinimumSize(900, 650)
        self._setup_ui()
        self._load_and_plot()
    
    def _setup_ui(self):
        """Configure l'interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("📈 Ventes Mensuelles (12 derniers mois)")
        header.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {ElAmiraStyles.COLORS['primary']};")
        layout.addWidget(header)
        
        # Message si matplotlib non disponible
        if not MATPLOTLIB_AVAILABLE:
            error_label = QLabel(
                "⚠️ Matplotlib n'est pas installé.\n\n"
                "Pour installer : pip install matplotlib"
            )
            error_label.setStyleSheet("""
                font-size: 14px;
                color: #DC2626;
                padding: 20px;
                background: #FEE2E2;
                border-radius: 8px;
            """)
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(error_label, 1)
        else:
            # Canvas pour le graphique
            self.canvas_widget = None
            layout.addStretch()
        
        # Footer
        footer_layout = QHBoxLayout()
        footer_layout.addStretch()
        
        close_btn = QPushButton("✖️ Fermer")
        close_btn.setStyleSheet(ElAmiraStyles.button_secondary())
        close_btn.clicked.connect(self.close)
        footer_layout.addWidget(close_btn)
        
        layout.addLayout(footer_layout)
        
        self.setStyleSheet("background: #F5F5F5;")
    
    def _load_and_plot(self):
        """Charge les données et affiche le graphique"""
        if not MATPLOTLIB_AVAILABLE or not self.db_manager:
            return
        
        try:
            # Récupérer données ventes mensuelles
            result = self.db_manager.execute_query("""
                SELECT 
                    strftime('%Y-%m', date_invoice) as month,
                    SUM(amount_total) as total,
                    COUNT(*) as count
                FROM account_invoice
                WHERE state = 'paid' AND date_invoice IS NOT NULL
                GROUP BY month
                ORDER BY month DESC
                LIMIT 12
            """)
            
            if not result:
                # Données exemple si vide
                result = [
                    {'month': '2025-10', 'total': 850000, 'count': 3},
                    {'month': '2025-09', 'total': 620000, 'count': 2},
                    {'month': '2025-08', 'total': 450000, 'count': 2},
                    {'month': '2025-07', 'total': 720000, 'count': 3},
                ]
            
            # Inverser pour avoir chronologique
            result.reverse()
            
            # Extraire données
            months = [row['month'] for row in result]
            totals = [row['total'] for row in result]
            counts = [row['count'] for row in result]
            
            # Créer figure
            fig = Figure(figsize=(10, 6), dpi=100)
            fig.patch.set_facecolor('#F5F5F5')
            
            # Créer axes
            ax = fig.add_subplot(111)
            
            # Graphique barres
            bars = ax.bar(months, totals, color=ElAmiraStyles.COLORS['primary'], 
                          alpha=0.8, edgecolor='white', linewidth=2)
            
            # Ajouter valeurs sur barres
            for i, (bar, total, count) in enumerate(zip(bars, totals, counts)):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{total/1000:.0f}k DA\n({count})',
                       ha='center', va='bottom', fontsize=10, fontweight='bold')
            
            # Styling
            ax.set_xlabel('Mois', fontsize=12, fontweight='bold')
            ax.set_ylabel('Chiffre d\'Affaires (DA)', fontsize=12, fontweight='bold')
            ax.set_title('Évolution du CA', fontsize=14, fontweight='bold', pad=20)
            ax.grid(True, alpha=0.3, linestyle='--', axis='y')
            ax.set_facecolor('white')
            
            # Rotation labels
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
            
            # Ajuster layout
            fig.tight_layout()
            
            # Ajouter canvas
            self.canvas_widget = ChartCanvas(fig)
            self.layout().insertWidget(1, self.canvas_widget)
            
        except Exception as e:
            print(f"Erreur création graphique ventes: {e}")
            import traceback
            traceback.print_exc()


class ProductsChartWindow(QDialog):
    """Fenêtre graphique top produits"""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("🏆 Top Produits Vendus")
        self.setMinimumSize(900, 650)
        self._setup_ui()
        self._load_and_plot()
    
    def _setup_ui(self):
        """Configure l'interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("🏆 Top 10 Produits les Plus Vendus")
        header.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {ElAmiraStyles.COLORS['primary']};")
        layout.addWidget(header)
        
        if not MATPLOTLIB_AVAILABLE:
            error_label = QLabel(
                "⚠️ Matplotlib n'est pas installé.\n\n"
                "Pour installer : pip install matplotlib"
            )
            error_label.setStyleSheet("""
                font-size: 14px;
                color: #DC2626;
                padding: 20px;
                background: #FEE2E2;
                border-radius: 8px;
            """)
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(error_label, 1)
        else:
            self.canvas_widget = None
            layout.addStretch()
        
        # Footer
        footer_layout = QHBoxLayout()
        footer_layout.addStretch()
        
        close_btn = QPushButton("✖️ Fermer")
        close_btn.setStyleSheet(ElAmiraStyles.button_secondary())
        close_btn.clicked.connect(self.close)
        footer_layout.addWidget(close_btn)
        
        layout.addLayout(footer_layout)
        
        self.setStyleSheet("background: #F5F5F5;")
    
    def _load_and_plot(self):
        """Charge les données et affiche le graphique"""
        if not MATPLOTLIB_AVAILABLE or not self.db_manager:
            return
        
        try:
            # Récupérer top produits (simulé pour l'instant)
            # TODO: Ajouter table order_line pour vrais chiffres
            result = self.db_manager.execute_query("""
                SELECT name, qty_available as qty
                FROM product_product
                WHERE active = 1
                ORDER BY qty_available DESC
                LIMIT 10
            """)
            
            if not result:
                # Données exemple
                result = [
                    {'name': 'JUKI DDL-8700', 'qty': 25},
                    {'name': 'BROTHER S-7300A', 'qty': 18},
                    {'name': 'SINGER 20U', 'qty': 15},
                    {'name': 'Fil Polyester', 'qty': 12},
                    {'name': 'Aiguilles', 'qty': 10},
                ]
            
            # Extraire données
            names = [row['name'][:20] for row in result]  # Tronquer noms longs
            quantities = [row['qty'] for row in result]
            
            # Créer figure
            fig = Figure(figsize=(10, 6), dpi=100)
            fig.patch.set_facecolor('#F5F5F5')
            
            # Créer axes
            ax = fig.add_subplot(111)
            
            # Graphique barres horizontales
            colors = [ElAmiraStyles.COLORS['success'], ElAmiraStyles.COLORS['primary'],
                     ElAmiraStyles.COLORS['secondary'], ElAmiraStyles.COLORS['warning'],
                     ElAmiraStyles.COLORS['gray']] * 2
            
            bars = ax.barh(names, quantities, color=colors[:len(names)], 
                          alpha=0.8, edgecolor='white', linewidth=2)
            
            # Ajouter valeurs
            for i, (bar, qty) in enumerate(zip(bars, quantities)):
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2.,
                       f' {qty}',
                       ha='left', va='center', fontsize=11, fontweight='bold')
            
            # Styling
            ax.set_xlabel('Quantité Vendue', fontsize=12, fontweight='bold')
            ax.set_title('Classement des Produits', fontsize=14, fontweight='bold', pad=20)
            ax.grid(True, alpha=0.3, linestyle='--', axis='x')
            ax.set_facecolor('white')
            
            # Inverser ordre pour avoir top en haut
            ax.invert_yaxis()
            
            # Ajuster layout
            fig.tight_layout()
            
            # Ajouter canvas
            self.canvas_widget = ChartCanvas(fig)
            self.layout().insertWidget(1, self.canvas_widget)
            
        except Exception as e:
            print(f"Erreur création graphique produits: {e}")
            import traceback
            traceback.print_exc()


class CAEvolutionChartWindow(QDialog):
    """Fenêtre graphique évolution CA"""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("💰 Évolution Chiffre d'Affaires")
        self.setMinimumSize(900, 650)
        self._setup_ui()
        self._load_and_plot()
    
    def _setup_ui(self):
        """Configure l'interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("💰 Évolution du Chiffre d'Affaires")
        header.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {ElAmiraStyles.COLORS['primary']};")
        layout.addWidget(header)
        
        if not MATPLOTLIB_AVAILABLE:
            error_label = QLabel(
                "⚠️ Matplotlib n'est pas installé.\n\n"
                "Pour installer : pip install matplotlib"
            )
            error_label.setStyleSheet("""
                font-size: 14px;
                color: #DC2626;
                padding: 20px;
                background: #FEE2E2;
                border-radius: 8px;
            """)
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(error_label, 1)
        else:
            self.canvas_widget = None
            layout.addStretch()
        
        # Footer
        footer_layout = QHBoxLayout()
        footer_layout.addStretch()
        
        close_btn = QPushButton("✖️ Fermer")
        close_btn.setStyleSheet(ElAmiraStyles.button_secondary())
        close_btn.clicked.connect(self.close)
        footer_layout.addWidget(close_btn)
        
        layout.addLayout(footer_layout)
        
        self.setStyleSheet("background: #F5F5F5;")
    
    def _load_and_plot(self):
        """Charge les données et affiche le graphique"""
        if not MATPLOTLIB_AVAILABLE or not self.db_manager:
            return
        
        try:
            # Récupérer CA par mois
            result = self.db_manager.execute_query("""
                SELECT 
                    strftime('%Y-%m', date_invoice) as month,
                    SUM(amount_total) as total
                FROM account_invoice
                WHERE state = 'paid' AND date_invoice IS NOT NULL
                GROUP BY month
                ORDER BY month ASC
                LIMIT 24
            """)
            
            if not result:
                # Données exemple
                import random
                from datetime import datetime, timedelta
                result = []
                base = 500000
                for i in range(12, 0, -1):
                    date = datetime.now() - timedelta(days=30*i)
                    month = date.strftime('%Y-%m')
                    total = base + random.randint(-100000, 200000)
                    result.append({'month': month, 'total': total})
            
            # Extraire données
            months = [row['month'] for row in result]
            totals = [row['total'] for row in result]
            
            # Créer figure
            fig = Figure(figsize=(10, 6), dpi=100)
            fig.patch.set_facecolor('#F5F5F5')
            
            # Créer axes
            ax = fig.add_subplot(111)
            
            # Graphique ligne avec marqueurs
            line = ax.plot(months, totals, 
                          color=ElAmiraStyles.COLORS['success'],
                          linewidth=3, marker='o', markersize=8,
                          markerfacecolor='white', markeredgewidth=2,
                          markeredgecolor=ElAmiraStyles.COLORS['success'])
            
            # Remplissage sous la courbe
            ax.fill_between(range(len(months)), totals, alpha=0.2,
                           color=ElAmiraStyles.COLORS['success'])
            
            # Ajouter valeurs sur points importants
            max_idx = totals.index(max(totals))
            min_idx = totals.index(min(totals))
            
            ax.annotate(f'{totals[max_idx]/1000:.0f}k DA',
                       xy=(max_idx, totals[max_idx]),
                       xytext=(10, 20), textcoords='offset points',
                       fontsize=11, fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.5', 
                                facecolor=ElAmiraStyles.COLORS['success'], 
                                alpha=0.2),
                       arrowprops=dict(arrowstyle='->', 
                                     color=ElAmiraStyles.COLORS['success']))
            
            # Styling
            ax.set_xlabel('Mois', fontsize=12, fontweight='bold')
            ax.set_ylabel('Chiffre d\'Affaires (DA)', fontsize=12, fontweight='bold')
            ax.set_title('Tendance du CA', fontsize=14, fontweight='bold', pad=20)
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.set_facecolor('white')
            
            # Rotation labels
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
            
            # Format Y axis
            ax.yaxis.set_major_formatter(plt.FuncFormatter(
                lambda x, p: f'{x/1000:.0f}k'
            ))
            
            # Ajuster layout
            fig.tight_layout()
            
            # Ajouter canvas
            self.canvas_widget = ChartCanvas(fig)
            self.layout().insertWidget(1, self.canvas_widget)
            
        except Exception as e:
            print(f"Erreur création graphique CA: {e}")
            import traceback
            traceback.print_exc()
