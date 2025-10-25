# -*- coding: utf-8 -*-
"""
Fenêtre Principale de l'Application
Interface de type Odoo avec menu latéral, barre de recherche et zone de contenu
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QListWidget, QListWidgetItem, QStackedWidget, QLabel,
    QLineEdit, QPushButton, QToolButton, QMenu, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QTranslator, QLocale, QSize
from PyQt6.QtGui import QIcon, QAction, QPixmap
import os


class MainWindow(QMainWindow):
    """
    Fenêtre principale de l'application ElAmira ERP.
    Reproduit l'interface utilisateur d'Odoo avec une barre latérale pour les modules.
    """
    
    # Signal émis lors du changement de langue
    language_changed = pyqtSignal(str)
    
    def __init__(self, db_manager, license_manager):
        """
        Initialise la fenêtre principale
        
        Args:
            db_manager: Instance du DatabaseManager
            license_manager: Instance du LicenseManager
        """
        super().__init__()
        
        self.db_manager = db_manager
        self.license_manager = license_manager
        self.modules = []
        self.current_language = 'fr'  # Français par défaut
        
        # Vérifier la licence au démarrage
        self._check_license_status()
        
        # Configuration de la fenêtre
        self.setWindowTitle("ElAmira ERP - Gestion d'Entreprise")
        self.setMinimumSize(1280, 720)
        
        # Créer l'interface
        self._setup_ui()
        
        # Charger le thème CSS
        self._load_theme()
    
    def _check_license_status(self):
        """Vérifie le statut de la licence et affiche un avertissement si nécessaire"""
        license_status = self.license_manager.check_license()
        
        if not license_status['is_valid']:
            # Mode démo/essai
            trial_days = license_status.get('trial_days_left', 0)
            QMessageBox.warning(
                self,
                "Licence Inactive",
                f"Aucune licence active détectée.\n\n"
                f"Vous disposez de {trial_days} jours d'essai.\n"
                f"Veuillez activer votre licence dans les Paramètres."
            )
    
    def _setup_ui(self):
        """Configure l'interface utilisateur principale"""
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal (horizontal)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # === SIDEBAR GAUCHE (Menu des Applications) ===
        self._create_sidebar(main_layout)
        
        # === ZONE PRINCIPALE (Droite) ===
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        
        # Barre supérieure (header)
        self._create_header(right_layout)
        
        # Zone de contenu (QStackedWidget pour les vues des modules)
        self.content_stack = QStackedWidget()
        right_layout.addWidget(self.content_stack)
        
        # Ajouter le panneau droit au layout principal
        main_layout.addWidget(right_panel, stretch=1)
    
    def _create_sidebar(self, parent_layout):
        """
        Crée la barre latérale gauche avec les icônes des modules
        
        Args:
            parent_layout: Layout parent où ajouter la sidebar
        """
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(80)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 10, 0, 10)
        sidebar_layout.setSpacing(5)
        
        # Logo en haut
        logo_label = QLabel()
        logo_label.setObjectName("appLogo")
        logo_label.setFixedSize(60, 60)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("""
            QLabel#appLogo {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #714B67, stop:1 #8B5A83);
                border-radius: 12px;
                color: white;
                font-size: 26px;
                font-weight: bold;
                border: 2px solid rgba(255,255,255,0.1);
            }
        """)
        logo_label.setText("🏢")
        sidebar_layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        # Séparateur
        separator = QLabel()
        separator.setFixedHeight(1)
        separator.setStyleSheet("background: #E0E0E0;")
        sidebar_layout.addWidget(separator)
        
        # Liste des modules (icônes seulement)
        self.module_list = QListWidget()
        self.module_list.setObjectName("moduleList")
        self.module_list.setIconSize(QSize(48, 48))
        self.module_list.setSpacing(5)
        self.module_list.currentRowChanged.connect(self._on_module_changed)
        
        sidebar_layout.addWidget(self.module_list, stretch=1)
        
        # Bouton Paramètres en bas
        settings_btn = QPushButton()
        settings_btn.setObjectName("settingsBtn")
        settings_btn.setFixedSize(50, 50)
        settings_btn.setToolTip("Paramètres")
        settings_btn.setText("⚙")
        settings_btn.setStyleSheet("""
            QPushButton#settingsBtn {
                font-size: 24px;
                border: none;
                background: transparent;
                border-radius: 8px;
            }
            QPushButton#settingsBtn:hover {
                background: #F0F0F0;
            }
        """)
        sidebar_layout.addWidget(settings_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        parent_layout.addWidget(sidebar)
    
    def _create_header(self, parent_layout):
        """
        Crée la barre supérieure (header) avec recherche et menu utilisateur
        
        Args:
            parent_layout: Layout parent où ajouter le header
        """
        header = QWidget()
        header.setObjectName("header")
        header.setFixedHeight(60)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 10, 20, 10)
        
        # Fil d'Ariane (Breadcrumb)
        self.breadcrumb_label = QLabel("Tableau de Bord")
        self.breadcrumb_label.setObjectName("breadcrumb")
        self.breadcrumb_label.setStyleSheet("""
            QLabel#breadcrumb {
                font-size: 18px;
                font-weight: bold;
                color: #2C3E50;
            }
        """)
        header_layout.addWidget(self.breadcrumb_label)
        
        header_layout.addStretch()
        
        # Barre de recherche globale
        self.search_box = QLineEdit()
        self.search_box.setObjectName("globalSearch")
        self.search_box.setPlaceholderText("Rechercher...")
        self.search_box.setFixedWidth(300)
        self.search_box.setStyleSheet("""
            QLineEdit#globalSearch {
                padding: 8px 15px;
                border: 1px solid #DDD;
                border-radius: 20px;
                background: #F8F8F8;
                font-size: 14px;
            }
            QLineEdit#globalSearch:focus {
                border: 1px solid #667eea;
                background: white;
            }
        """)
        header_layout.addWidget(self.search_box)
        
        # Bouton Nouveau
        new_btn = QPushButton("+ Nouveau")
        new_btn.setObjectName("newBtn")
        new_btn.setStyleSheet("""
            QPushButton#newBtn {
                padding: 8px 20px;
                background: #667eea;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton#newBtn:hover {
                background: #5568d3;
            }
            QPushButton#newBtn:pressed {
                background: #4a5bc4;
            }
        """)
        header_layout.addWidget(new_btn)
        
        # Menu utilisateur
        user_menu_btn = QToolButton()
        user_menu_btn.setText("👤 Admin")
        user_menu_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        user_menu_btn.setStyleSheet("""
            QToolButton {
                padding: 8px 15px;
                border: 1px solid #DDD;
                border-radius: 5px;
                background: white;
                font-size: 14px;
            }
            QToolButton:hover {
                background: #F0F0F0;
            }
        """)
        
        # Créer le menu utilisateur
        user_menu = QMenu()
        user_menu.addAction("Mon Profil")
        user_menu.addAction("Paramètres")
        user_menu.addSeparator()
        
        # Action de changement de langue
        lang_menu = user_menu.addMenu("🌐 Langue / اللغة")
        
        fr_action = QAction("Français", self)
        fr_action.triggered.connect(lambda: self.switch_language('fr'))
        lang_menu.addAction(fr_action)
        
        ar_action = QAction("العربية", self)
        ar_action.triggered.connect(lambda: self.switch_language('ar'))
        lang_menu.addAction(ar_action)
        
        user_menu.addSeparator()
        
        # Action déconnexion
        logout_action = QAction("Déconnexion", self)
        logout_action.triggered.connect(self.close)
        user_menu.addAction(logout_action)
        
        user_menu_btn.setMenu(user_menu)
        header_layout.addWidget(user_menu_btn)
        
        parent_layout.addWidget(header)
    
    def load_modules(self, module_loader):
        """
        Charge les modules dans l'interface
        Filtre selon la licence active
        
        Args:
            module_loader: Instance du ModuleLoader avec les modules chargés
        """
        # Vérifier la licence pour filtrer les modules
        license_status = self.license_manager.check_license()
        is_licensed = license_status['is_valid']
        
        # Modules de base gratuits (toujours visibles)
        free_modules = ['Tableau de Bord', 'Paramètres']
        
        self.modules = []
        
        # Vider la liste actuelle
        self.module_list.clear()
        
        # Icônes emoji par défaut pour chaque module
        module_icons = {
            'Tableau de Bord': '📊',
            'Ventes': '💰',
            'Stock': '📦',
            'Comptabilité': '📚',
            'Paramètres': '⚙️',
            'CRM': '👥',
            'Achats': '🛒',
            'Maintenance': '🔧'
        }
        
        # Ajouter chaque module à la liste et au stack
        for module in module_loader.loaded_modules:
            module_name = module.get_name()
            
            # Filtrer selon licence (modules gratuits toujours visibles)
            if not is_licensed and module_name not in free_modules:
                continue  # Ignorer ce module si pas de licence
            
            self.modules.append(module)
            
            # Créer l'item de liste avec icône emoji
            item = QListWidgetItem()
            
            # Icône par défaut selon le module
            emoji_icon = module_icons.get(module_name, '📋')
            
            # Essayer de charger l'icône fichier, sinon utiliser emoji
            icon_path = module.get_icon()
            if os.path.exists(icon_path):
                item.setIcon(QIcon(icon_path))
            else:
                # Utiliser l'emoji comme texte de l'item
                item.setText(emoji_icon)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Tooltip avec le nom du module
            tooltip_text = module.get_name()
            if self.current_language == 'ar':
                tooltip_text += f"\n{module.get_name_ar()}"
            item.setToolTip(tooltip_text)
            
            # Style personnalisé pour chaque item
            item.setSizeHint(QSize(60, 60))
            
            self.module_list.addItem(item)
            
            # Créer et ajouter la vue du module au stack
            try:
                view_class = module.get_main_view_class()
                view_instance = view_class(module, self.db_manager)
                self.content_stack.addWidget(view_instance)
            except Exception as e:
                print(f"✗ Erreur lors de la création de la vue pour {module.get_name()}: {e}")
                # Ajouter une vue par défaut en cas d'erreur
                error_widget = QLabel(f"Erreur de chargement du module {module.get_name()}")
                error_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.content_stack.addWidget(error_widget)
        
        # Afficher message si modules restreints
        if not is_licensed and len(self.modules) < len(module_loader.loaded_modules):
            print(f"⚠ Mode démo: {len(self.modules)}/{len(module_loader.loaded_modules)} modules actifs")
            print(f"  Activez une licence pour accéder à tous les modules")
        
        # Sélectionner le premier module par défaut
        if self.modules:
            self.module_list.setCurrentRow(0)
    
    def _on_module_changed(self, index):
        """
        Callback appelé quand l'utilisateur change de module
        
        Args:
            index: Index du module sélectionné
        """
        if 0 <= index < len(self.modules):
            module = self.modules[index]
            
            # Changer le contenu affiché
            self.content_stack.setCurrentIndex(index)
            
            # Mettre à jour le breadcrumb
            if self.current_language == 'ar':
                self.breadcrumb_label.setText(module.get_name_ar())
            else:
                self.breadcrumb_label.setText(module.get_name())
    
    def switch_language(self, lang_code: str):
        """
        Change la langue de l'interface
        
        Args:
            lang_code: Code de la langue ('fr' ou 'ar')
        """
        self.current_language = lang_code
        
        # Changer la direction du layout pour l'arabe
        if lang_code == 'ar':
            self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
            QMessageBox.information(
                self,
                "تغيير اللغة",
                "تم تغيير اللغة إلى العربية\nقد تحتاج إلى إعادة تشغيل التطبيق"
            )
        else:
            self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
            QMessageBox.information(
                self,
                "Changement de langue",
                "La langue a été changée en français\nVous devrez peut-être redémarrer l'application"
            )
        
        # Émettre le signal de changement de langue
        self.language_changed.emit(lang_code)
        
        # Mettre à jour l'affichage
        self._update_ui_language()
    
    def _update_ui_language(self):
        """Met à jour les textes de l'interface selon la langue actuelle"""
        if self.current_language == 'ar':
            self.search_box.setPlaceholderText("بحث...")
            self.setWindowTitle("إلعميرة - نظام إدارة المؤسسة")
        else:
            self.search_box.setPlaceholderText("Rechercher...")
            self.setWindowTitle("ElAmira ERP - Gestion d'Entreprise")
        
        # Mettre à jour le breadcrumb
        current_index = self.module_list.currentRow()
        if 0 <= current_index < len(self.modules):
            self._on_module_changed(current_index)
    
    def _load_theme(self):
        """Charge le thème CSS principal (style Odoo)"""
        theme_path = os.path.join('core', 'assets', 'themes', 'odoo_theme.qss')
        
        if os.path.exists(theme_path):
            try:
                with open(theme_path, 'r', encoding='utf-8') as f:
                    stylesheet = f.read()
                    self.setStyleSheet(stylesheet)
                print("✓ Thème chargé avec succès")
            except Exception as e:
                print(f"✗ Erreur de chargement du thème: {e}")
        else:
            # Appliquer un style par défaut minimal
            self.setStyleSheet("""
                QMainWindow {
                    background: #F5F5F5;
                }
                QWidget#sidebar {
                    background: white;
                    border-right: 1px solid #E0E0E0;
                }
                QWidget#header {
                    background: white;
                    border-bottom: 1px solid #E0E0E0;
                }
                QListWidget#moduleList {
                    background: transparent;
                    border: none;
                }
                QListWidget#moduleList::item {
                    padding: 10px;
                    border-radius: 8px;
                    margin: 5px;
                }
                QListWidget#moduleList::item:selected {
                    background: #667eea;
                }
                QListWidget#moduleList::item:hover {
                    background: #F0F0F0;
                }
            """)
    
    def closeEvent(self, event):
        """Override pour gérer la fermeture de l'application"""
        reply = QMessageBox.question(
            self,
            'Quitter',
            'Êtes-vous sûr de vouloir quitter ElAmira ERP ?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Fermer la connexion à la base de données
            self.db_manager.close()
            event.accept()
        else:
            event.ignore()
