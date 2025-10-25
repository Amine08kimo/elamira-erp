# -*- coding: utf-8 -*-
"""
Stock Views - Vues pour le module Stock
Vue Kanban et Liste des produits
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QPushButton, QLineEdit, QTableWidget,
    QTableWidgetItem, QHeaderView, QScrollArea, QDialog,
    QFormLayout, QTextEdit, QDoubleSpinBox, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from .controller import StockController
from .models import Product


class ProductKanbanView(QWidget):
    """Vue Kanban des produits (cartes)"""
    
    def __init__(self, module, db_manager):
        super().__init__()
        self.module = module
        self.db_manager = db_manager
        self.controller = StockController(db_manager)
        self._setup_ui()
        self.load_products()
    
    def _setup_ui(self):
        """Configure l'interface style Odoo"""
        # Fond clair Odoo
        self.setStyleSheet("background-color: #F9FAFB;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        # Barre de recherche
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍 Rechercher un produit...")
        self.search_box.setFixedWidth(300)
        self.search_box.textChanged.connect(self.search_products)
        header_layout.addWidget(self.search_box)
        
        header_layout.addStretch()
        
        # Boutons vue
        list_view_btn = QPushButton("📋 Liste")
        list_view_btn.setObjectName("secondaryBtn")
        header_layout.addWidget(list_view_btn)
        
        kanban_view_btn = QPushButton("📦 Cartes")
        kanban_view_btn.setObjectName("primaryBtn")
        header_layout.addWidget(kanban_view_btn)
        
        # Bouton Nouveau
        new_btn = QPushButton("+ Nouveau Produit")
        new_btn.setObjectName("primaryBtn")
        new_btn.clicked.connect(self.create_new_product)
        header_layout.addWidget(new_btn)
        
        layout.addLayout(header_layout)
        
        # Zone scrollable pour les cartes
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        # Container pour les cartes
        self.cards_container = QWidget()
        self.cards_layout = QGridLayout(self.cards_container)
        self.cards_layout.setSpacing(20)
        
        scroll.setWidget(self.cards_container)
        layout.addWidget(scroll)
    
    def load_products(self):
        """Charge les produits en mode Kanban"""
        products = self.controller.get_all_products()
        
        # Effacer les cartes existantes
        for i in reversed(range(self.cards_layout.count())):
            self.cards_layout.itemAt(i).widget().setParent(None)
        
        # Créer les cartes (4 par ligne)
        for idx, product in enumerate(products):
            row = idx // 4
            col = idx % 4
            card = self._create_product_card(product)
            self.cards_layout.addWidget(card, row, col)
    
    def _create_product_card(self, product: Product) -> QFrame:
        """Crée une carte produit"""
        card = QFrame()
        card.setObjectName("card")
        card.setFixedSize(250, 300)
        card.setStyleSheet("""
            QFrame#card {
                background: white;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
            }
            QFrame#card:hover {
                border-color: #667eea;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(10)
        
        # Image produit (placeholder)
        img_label = QLabel()
        img_label.setFixedSize(230, 150)
        img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img_label.setStyleSheet("""
            QLabel {
                background: #F3F4F6;
                border-radius: 8px;
                color: #9CA3AF;
                font-size: 48px;
            }
        """)
        img_label.setText("📦")
        layout.addWidget(img_label)
        
        # Nom du produit
        name_label = QLabel(product.name)
        name_label.setStyleSheet("font-weight: 600; font-size: 14px;")
        name_label.setWordWrap(True)
        name_label.setMaximumHeight(40)
        layout.addWidget(name_label)
        
        # Référence
        ref_label = QLabel(f"Réf: {product.reference or 'N/A'}")
        ref_label.setStyleSheet("color: #6B7280; font-size: 12px;")
        layout.addWidget(ref_label)
        
        # Prix et stock
        info_layout = QHBoxLayout()
        
        price_label = QLabel(f"{product.sale_price:,.2f} DA")
        price_label.setStyleSheet("color: #667eea; font-weight: 600;")
        info_layout.addWidget(price_label)
        
        info_layout.addStretch()
        
        # Indicateur de stock
        stock_badge = QLabel(f"📊 {product.qty_available:.0f}")
        if product.qty_available > 10:
            stock_badge.setStyleSheet("""
                background: #D1FAE5; 
                color: #065F46; 
                padding: 4px 8px; 
                border-radius: 12px;
                font-size: 11px;
                font-weight: 600;
            """)
        elif product.qty_available > 0:
            stock_badge.setStyleSheet("""
                background: #FEF3C7; 
                color: #92400E; 
                padding: 4px 8px; 
                border-radius: 12px;
                font-size: 11px;
                font-weight: 600;
            """)
        else:
            stock_badge.setStyleSheet("""
                background: #FEE2E2; 
                color: #991B1B; 
                padding: 4px 8px; 
                border-radius: 12px;
                font-size: 11px;
                font-weight: 600;
            """)
        info_layout.addWidget(stock_badge)
        
        layout.addLayout(info_layout)
        
        # Rendre la carte cliquable
        card.mousePressEvent = lambda e: self.edit_product(product)
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        
        return card
    
    def search_products(self, query: str):
        """Recherche des produits"""
        if query:
            products = self.controller.search_products(query)
        else:
            products = self.controller.get_all_products()
        
        # Recharger les cartes avec les résultats
        for i in reversed(range(self.cards_layout.count())):
            self.cards_layout.itemAt(i).widget().setParent(None)
        
        for idx, product in enumerate(products):
            row = idx // 4
            col = idx % 4
            card = self._create_product_card(product)
            self.cards_layout.addWidget(card, row, col)
    
    def create_new_product(self):
        """Ouvre le formulaire de création"""
        dialog = ProductFormDialog(self.db_manager, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_products()
    
    def edit_product(self, product):
        """Ouvre le formulaire d'édition"""
        dialog = ProductFormDialog(self.db_manager, product=product, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_products()


class ProductFormDialog(QDialog):
    """Formulaire de création/édition de produit"""
    
    def __init__(self, db_manager, product=None, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.controller = StockController(db_manager)
        self.product = product if product else Product()
        
        self.setWindowTitle("Produit")
        self.setMinimumSize(600, 500)
        self._setup_ui()
        
        if product:
            self._load_product_data()
    
    def _setup_ui(self):
        """Configure l'interface"""
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Nom
        self.name_edit = QLineEdit()
        form_layout.addRow("Nom *:", self.name_edit)
        
        # Nom arabe
        self.name_ar_edit = QLineEdit()
        form_layout.addRow("الاسم:", self.name_ar_edit)
        
        # Référence
        self.reference_edit = QLineEdit()
        form_layout.addRow("Référence:", self.reference_edit)
        
        # Code-barres
        self.barcode_edit = QLineEdit()
        form_layout.addRow("Code-barres:", self.barcode_edit)
        
        # Prix de vente
        self.sale_price_spin = QDoubleSpinBox()
        self.sale_price_spin.setMaximum(999999999.99)
        self.sale_price_spin.setDecimals(2)
        self.sale_price_spin.setSuffix(" DA")
        form_layout.addRow("Prix de vente *:", self.sale_price_spin)
        
        # Prix de revient
        self.cost_price_spin = QDoubleSpinBox()
        self.cost_price_spin.setMaximum(999999999.99)
        self.cost_price_spin.setDecimals(2)
        self.cost_price_spin.setSuffix(" DA")
        form_layout.addRow("Prix de revient:", self.cost_price_spin)
        
        # Quantité initiale
        self.qty_spin = QDoubleSpinBox()
        self.qty_spin.setMaximum(999999999.99)
        self.qty_spin.setDecimals(2)
        form_layout.addRow("Quantité en stock:", self.qty_spin)
        
        # TVA
        self.tax_combo = QComboBox()
        self.tax_combo.addItem("TVA 0%", 0)
        self.tax_combo.addItem("TVA 9%", 9)
        self.tax_combo.addItem("TVA 19%", 19)
        form_layout.addRow("TVA:", self.tax_combo)
        
        # Description
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        form_layout.addRow("Description:", self.description_edit)
        
        layout.addLayout(form_layout)
        
        # Boutons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.setObjectName("secondaryBtn")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("💾 Enregistrer")
        save_btn.setObjectName("primaryBtn")
        save_btn.clicked.connect(self.save_product)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)
    
    def _load_product_data(self):
        """Charge les données du produit"""
        self.name_edit.setText(self.product.name)
        self.name_ar_edit.setText(self.product.name_ar)
        self.reference_edit.setText(self.product.reference)
        self.barcode_edit.setText(self.product.barcode)
        self.sale_price_spin.setValue(self.product.sale_price)
        self.cost_price_spin.setValue(self.product.cost_price)
        self.qty_spin.setValue(self.product.qty_available)
        self.description_edit.setPlainText(self.product.description)
    
    def save_product(self):
        """Enregistre le produit"""
        from PyQt6.QtWidgets import QMessageBox
        
        # Validation
        if not self.name_edit.text():
            QMessageBox.warning(self, "Validation", "Le nom est obligatoire")
            return
        
        # Construire l'objet
        product = Product()
        product.name = self.name_edit.text()
        product.name_ar = self.name_ar_edit.text()
        product.reference = self.reference_edit.text()
        product.barcode = self.barcode_edit.text()
        product.sale_price = self.sale_price_spin.value()
        product.cost_price = self.cost_price_spin.value()
        product.qty_available = self.qty_spin.value()
        product.description = self.description_edit.toPlainText()
        
        try:
            if self.product.id:
                # Mise à jour
                product.id = self.product.id
                self.controller.update_product(product)
                QMessageBox.information(self, "Succès", "Produit mis à jour")
            else:
                # Création
                self.controller.create_product(product)
                QMessageBox.information(self, "Succès", "Produit créé")
            
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur:\n{str(e)}")
