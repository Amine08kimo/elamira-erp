#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Styles communs pour tous les modules ElAmira ERP
Style moderne inspiré du module Maintenance
"""


class ElAmiraStyles:
    """Styles réutilisables pour l'ERP"""
    
    # ========== COULEURS ==========
    COLORS = {
        # Primaires
        'primary': '#6750A4',        # Violet principal
        'secondary': '#2563EB',      # Bleu
        'success': '#10B981',        # Vert
        'warning': '#F59E0B',        # Orange
        'danger': '#DC2626',         # Rouge
        
        # Neutres
        'gray_dark': '#1A1A1A',
        'gray': '#5F6368',
        'gray_light': '#E0E0E0',
        'gray_lighter': '#F5F5F5',
        'white': '#FFFFFF',
        
        # Backgrounds
        'bg_hover': '#FAFAFA',
        'bg_selected': '#E8F0FE',
        
        # Statuts
        'status_blue': '#2563EB',
        'status_green': '#10B981',
        'status_orange': '#F59E0B',
        'status_red': '#DC2626',
        
        # KPIs
        'kpi_violet': '#6750A4',
        'kpi_green': '#10B981',
        'kpi_blue': '#2563EB',
        'kpi_orange': '#F59E0B',
    }
    
    # ========== DIALOGUES ==========
    @staticmethod
    def dialog_header(title_color='primary'):
        """Style pour header de dialogue"""
        color = ElAmiraStyles.COLORS.get(title_color, ElAmiraStyles.COLORS['primary'])
        return f"""
            font-size: 20px;
            font-weight: 700;
            color: {color};
            padding-bottom: 10px;
        """
    
    @staticmethod
    def dialog_large_header(title_color='primary'):
        """Style pour grand header"""
        color = ElAmiraStyles.COLORS.get(title_color, ElAmiraStyles.COLORS['primary'])
        return f"""
            font-size: 22px;
            font-weight: 700;
            color: {color};
            padding-bottom: 10px;
        """
    
    # ========== INPUTS ==========
    @staticmethod
    def input_style(focus_color='primary'):
        """Style pour QLineEdit"""
        color = ElAmiraStyles.COLORS.get(focus_color, ElAmiraStyles.COLORS['primary'])
        return f"""
            QLineEdit {{
                padding: 10px;
                border: 2px solid {ElAmiraStyles.COLORS['gray_light']};
                border-radius: 6px;
                font-size: 13px;
                background: white;
            }}
            QLineEdit:focus {{
                border: 2px solid {color};
                background: {ElAmiraStyles.COLORS['bg_hover']};
            }}
            QLineEdit:read-only {{
                background: {ElAmiraStyles.COLORS['gray_lighter']};
                color: {ElAmiraStyles.COLORS['gray']};
            }}
        """
    
    @staticmethod
    def text_edit_style(focus_color='primary'):
        """Style pour QTextEdit"""
        color = ElAmiraStyles.COLORS.get(focus_color, ElAmiraStyles.COLORS['primary'])
        return f"""
            QTextEdit {{
                padding: 10px;
                border: 2px solid {ElAmiraStyles.COLORS['gray_light']};
                border-radius: 6px;
                font-size: 13px;
                background: white;
            }}
            QTextEdit:focus {{
                border: 2px solid {color};
                background: {ElAmiraStyles.COLORS['bg_hover']};
            }}
        """
    
    @staticmethod
    def combo_style(focus_color='primary'):
        """Style pour QComboBox"""
        color = ElAmiraStyles.COLORS.get(focus_color, ElAmiraStyles.COLORS['primary'])
        return f"""
            QComboBox {{
                padding: 10px;
                border: 2px solid {ElAmiraStyles.COLORS['gray_light']};
                border-radius: 6px;
                font-size: 13px;
                background: white;
            }}
            QComboBox:focus {{
                border: 2px solid {color};
            }}
            QComboBox::drop-down {{
                border: none;
                padding-right: 10px;
            }}
        """
    
    @staticmethod
    def date_style(focus_color='primary'):
        """Style pour QDateEdit"""
        color = ElAmiraStyles.COLORS.get(focus_color, ElAmiraStyles.COLORS['primary'])
        return f"""
            QDateEdit {{
                padding: 10px;
                border: 2px solid {ElAmiraStyles.COLORS['gray_light']};
                border-radius: 6px;
                font-size: 13px;
                background: white;
            }}
            QDateEdit:focus {{
                border: 2px solid {color};
            }}
        """
    
    @staticmethod
    def spinbox_style(focus_color='primary'):
        """Style pour QSpinBox/QDoubleSpinBox"""
        color = ElAmiraStyles.COLORS.get(focus_color, ElAmiraStyles.COLORS['primary'])
        return f"""
            QSpinBox, QDoubleSpinBox {{
                padding: 10px;
                border: 2px solid {ElAmiraStyles.COLORS['gray_light']};
                border-radius: 6px;
                font-size: 13px;
                background: white;
            }}
            QSpinBox:focus, QDoubleSpinBox:focus {{
                border: 2px solid {color};
            }}
        """
    
    # ========== BOUTONS ==========
    @staticmethod
    def button_primary():
        """Bouton principal (violet)"""
        return f"""
            QPushButton {{
                padding: 10px 20px;
                background: {ElAmiraStyles.COLORS['primary']};
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background: #5639A0;
            }}
            QPushButton:pressed {{
                background: #4A2E8C;
            }}
        """
    
    @staticmethod
    def button_secondary():
        """Bouton secondaire (bleu)"""
        return f"""
            QPushButton {{
                padding: 10px 20px;
                background: {ElAmiraStyles.COLORS['secondary']};
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background: #1D4ED8;
            }}
            QPushButton:pressed {{
                background: #1E40AF;
            }}
        """
    
    @staticmethod
    def button_success():
        """Bouton succès (vert)"""
        return f"""
            QPushButton {{
                padding: 10px 20px;
                background: {ElAmiraStyles.COLORS['success']};
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background: #059669;
            }}
            QPushButton:pressed {{
                background: #047857;
            }}
        """
    
    @staticmethod
    def button_danger():
        """Bouton danger (rouge)"""
        return f"""
            QPushButton {{
                padding: 10px 20px;
                background: {ElAmiraStyles.COLORS['danger']};
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background: #B91C1C;
            }}
            QPushButton:pressed {{
                background: #991B1B;
            }}
        """
    
    @staticmethod
    def button_neutral():
        """Bouton neutre (gris)"""
        return f"""
            QPushButton {{
                padding: 10px 20px;
                background: {ElAmiraStyles.COLORS['gray_light']};
                color: {ElAmiraStyles.COLORS['gray_dark']};
                border: none;
                border-radius: 6px;
                font-weight: 600;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background: #D0D0D0;
            }}
            QPushButton:pressed {{
                background: #C0C0C0;
            }}
        """
    
    # ========== TABLES ==========
    @staticmethod
    def table_style():
        """Style pour QTableWidget"""
        return f"""
            QTableWidget {{
                background: white;
                border: 2px solid {ElAmiraStyles.COLORS['gray_light']};
                border-radius: 6px;
                gridline-color: {ElAmiraStyles.COLORS['gray_light']};
            }}
            QHeaderView::section {{
                background: {ElAmiraStyles.COLORS['gray_lighter']};
                padding: 10px;
                border: none;
                border-bottom: 2px solid {ElAmiraStyles.COLORS['gray_light']};
                font-weight: 700;
                color: {ElAmiraStyles.COLORS['gray']};
                font-size: 12px;
            }}
            QTableWidget::item {{
                padding: 8px;
            }}
            QTableWidget::item:selected {{
                background: {ElAmiraStyles.COLORS['bg_selected']};
                color: {ElAmiraStyles.COLORS['gray_dark']};
            }}
            QTableWidget::item:hover {{
                background: {ElAmiraStyles.COLORS['bg_hover']};
            }}
        """
    
    # ========== GROUPBOX ==========
    @staticmethod
    def groupbox_style():
        """Style pour QGroupBox"""
        return f"""
            QGroupBox {{
                font-size: 15px;
                font-weight: 700;
                color: {ElAmiraStyles.COLORS['gray_dark']};
                border: 2px solid {ElAmiraStyles.COLORS['gray_light']};
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 20px;
                background: white;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 5px 10px;
                background: white;
            }}
        """
    
    # ========== KPI CARDS ==========
    @staticmethod
    def kpi_card_style(color_key='kpi_violet'):
        """Style pour KPI card (QPushButton)"""
        color = ElAmiraStyles.COLORS.get(color_key, ElAmiraStyles.COLORS['kpi_violet'])
        bg_color = f"rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.08)"
        
        return f"""
            QPushButton#kpiCard {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {bg_color}, stop:1 #FFFFFF);
                border: 2px solid {ElAmiraStyles.COLORS['gray_light']};
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
        """
    
    # ========== BADGES STATUT ==========
    @staticmethod
    def get_status_colors(status):
        """Retourne les couleurs pour un statut"""
        status_map = {
            'planned': ('status_blue', '#E8F0FE'),
            'in_progress': ('status_orange', '#FEF3E8'),
            'done': ('status_green', '#E8F5F0'),
            'cancelled': ('status_red', '#FCE8E6'),
        }
        
        if status.lower() in ['planned', 'scheduled', 'planifiée', 'planifié']:
            color_key, bg = status_map['planned']
        elif status.lower() in ['in_progress', 'en cours', 'in progress']:
            color_key, bg = status_map['in_progress']
        elif status.lower() in ['done', 'terminée', 'terminé', 'completed']:
            color_key, bg = status_map['done']
        elif status.lower() in ['cancelled', 'annulée', 'annulé']:
            color_key, bg = status_map['cancelled']
        else:
            color_key, bg = 'gray', ElAmiraStyles.COLORS['gray_lighter']
        
        return ElAmiraStyles.COLORS[color_key], bg
    
    # ========== CHECKBOX ==========
    @staticmethod
    def checkbox_style():
        """Style pour QCheckBox"""
        return """
            QCheckBox {
                font-size: 13px;
                padding: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
        """
    
    # ========== SEARCH BAR ==========
    @staticmethod
    def search_bar_style():
        """Style pour barre de recherche"""
        return f"""
            QLineEdit {{
                padding: 10px 15px;
                border: 2px solid {ElAmiraStyles.COLORS['gray_light']};
                border-radius: 8px;
                font-size: 13px;
                background: white;
                min-width: 300px;
            }}
            QLineEdit:focus {{
                border: 2px solid {ElAmiraStyles.COLORS['primary']};
                background: {ElAmiraStyles.COLORS['bg_hover']};
            }}
        """


class ElAmiraDialog:
    """Classe utilitaire pour créer des dialogues stylisés"""
    
    @staticmethod
    def apply_input_style(widget, focus_color='primary'):
        """Applique le style à un input"""
        widget.setStyleSheet(ElAmiraStyles.input_style(focus_color))
    
    @staticmethod
    def apply_combo_style(widget, focus_color='primary'):
        """Applique le style à un combo"""
        widget.setStyleSheet(ElAmiraStyles.combo_style(focus_color))
    
    @staticmethod
    def apply_text_style(widget, focus_color='primary'):
        """Applique le style à un text edit"""
        widget.setStyleSheet(ElAmiraStyles.text_edit_style(focus_color))
    
    @staticmethod
    def apply_date_style(widget, focus_color='primary'):
        """Applique le style à un date edit"""
        widget.setStyleSheet(ElAmiraStyles.date_style(focus_color))
    
    @staticmethod
    def apply_spinbox_style(widget, focus_color='primary'):
        """Applique le style à un spinbox"""
        widget.setStyleSheet(ElAmiraStyles.spinbox_style(focus_color))
    
    @staticmethod
    def create_header(text, color='primary'):
        """Crée un header stylisé"""
        from PyQt6.QtWidgets import QLabel
        header = QLabel(text)
        color_value = ElAmiraStyles.COLORS.get(color, ElAmiraStyles.COLORS['primary'])
        header.setStyleSheet(f"""
            font-size: 20px;
            font-weight: 700;
            color: {color_value};
            padding-bottom: 10px;
        """)
        return header
    
    @staticmethod
    def create_button(text, button_type='primary'):
        """Crée un bouton stylisé"""
        from PyQt6.QtWidgets import QPushButton
        button = QPushButton(text)
        
        styles = {
            'primary': ElAmiraStyles.button_primary(),
            'secondary': ElAmiraStyles.button_secondary(),
            'success': ElAmiraStyles.button_success(),
            'danger': ElAmiraStyles.button_danger(),
            'neutral': ElAmiraStyles.button_neutral(),
        }
        
        button.setStyleSheet(styles.get(button_type, styles['primary']))
        return button
