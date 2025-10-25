#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Générateur de rapports PDF pour le module Maintenance
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from datetime import datetime
import os


class MaintenanceReportGenerator:
    """Générateur de rapports maintenance en PDF"""
    
    def __init__(self, controller):
        self.controller = controller
        self.output_dir = "reports/maintenance"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _get_header_footer(self, canvas_obj, doc):
        """En-tête et pied de page"""
        canvas_obj.saveState()
        
        # En-tête
        canvas_obj.setFont('Helvetica-Bold', 16)
        canvas_obj.setFillColor(colors.HexColor('#6750A4'))
        canvas_obj.drawString(2*cm, A4[1] - 2*cm, "🪡 ElAmira ERP")
        
        canvas_obj.setFont('Helvetica', 10)
        canvas_obj.setFillColor(colors.black)
        canvas_obj.drawString(2*cm, A4[1] - 2.5*cm, "Module Maintenance - Gestion d'Interventions")
        
        # Ligne de séparation
        canvas_obj.setStrokeColor(colors.HexColor('#6750A4'))
        canvas_obj.setLineWidth(2)
        canvas_obj.line(2*cm, A4[1] - 3*cm, A4[0] - 2*cm, A4[1] - 3*cm)
        
        # Pied de page
        canvas_obj.setFont('Helvetica', 8)
        canvas_obj.setFillColor(colors.grey)
        canvas_obj.drawString(2*cm, 1.5*cm, f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
        canvas_obj.drawRightString(A4[0] - 2*cm, 1.5*cm, f"Page {doc.page}")
        
        canvas_obj.restoreState()
    
    def generate_dashboard_report(self):
        """Génère le rapport Dashboard"""
        filename = f"dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Créer PDF
        doc = SimpleDocTemplate(filepath, pagesize=A4,
                                topMargin=4*cm, bottomMargin=2.5*cm)
        
        story = []
        styles = getSampleStyleSheet()
        
        # Titre
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#6750A4'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        story.append(Paragraph("📊 Dashboard Maintenance", title_style))
        story.append(Spacer(1, 0.5*cm))
        
        # KPIs
        stats = self.controller.get_maintenance_stats()
        
        kpi_data = [
            ['Indicateur', 'Valeur'],
            ['🛠️ Interventions En Cours', str(stats['pending_interventions'])],
            ['📅 Interventions Ce Mois', str(stats['monthly_interventions'])],
            ['📋 Contrats Actifs', str(stats['active_contracts'])],
            ['⚠️ Pièces Stock Bas', str(stats['low_stock_parts'])],
        ]
        
        kpi_table = Table(kpi_data, colWidths=[12*cm, 4*cm])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6750A4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        story.append(kpi_table)
        story.append(Spacer(1, 1*cm))
        
        # Interventions de la semaine
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2563EB'),
            spaceAfter=15,
            fontName='Helvetica-Bold'
        )
        story.append(Paragraph("📅 Interventions de la Semaine", subtitle_style))
        
        today = datetime.now()
        from datetime import timedelta
        week_end = today + timedelta(days=7)
        interventions = self.controller.get_scheduled_interventions(today, week_end)
        
        if interventions:
            inter_data = [['ID', 'Date', 'Client', 'Machine', 'Type', 'Statut']]
            for inter in interventions:
                from modules.maintenance.views import format_date
                inter_data.append([
                    f"#{inter.id}",
                    format_date(inter.date_scheduled),
                    inter.partner_name or "",
                    inter.machine_name or "",
                    "Préventive" if inter.intervention_type == "preventive" else "Corrective",
                    inter.state or ""
                ])
            
            inter_table = Table(inter_data, colWidths=[1.5*cm, 2.5*cm, 4*cm, 4*cm, 2.5*cm, 2*cm])
            inter_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            story.append(inter_table)
        else:
            story.append(Paragraph("Aucune intervention planifiée cette semaine", styles['Normal']))
        
        # Générer PDF
        doc.build(story, onFirstPage=self._get_header_footer, 
                  onLaterPages=self._get_header_footer)
        
        print(f"✓ Rapport généré: {filepath}")
        return filepath
    
    def generate_intervention_report(self, intervention_id):
        """Génère le rapport d'une intervention"""
        filename = f"intervention_{intervention_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Créer PDF
        doc = SimpleDocTemplate(filepath, pagesize=A4,
                                topMargin=4*cm, bottomMargin=2.5*cm)
        
        story = []
        styles = getSampleStyleSheet()
        
        # Titre
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor('#6750A4'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        story.append(Paragraph(f"🔧 Fiche Intervention #{intervention_id}", title_style))
        story.append(Spacer(1, 0.5*cm))
        
        # Récupérer intervention
        interventions = self.controller.get_all_interventions()
        intervention = next((i for i in interventions if i.id == intervention_id), None)
        
        if not intervention:
            story.append(Paragraph("Intervention non trouvée", styles['Normal']))
        else:
            from modules.maintenance.views import format_date
            
            # Informations générales
            info_data = [
                ['Champ', 'Valeur'],
                ['Client', intervention.partner_name or "N/A"],
                ['Machine', intervention.machine_name or "N/A"],
                ['Type', "Préventive" if intervention.intervention_type == "preventive" else "Corrective"],
                ['Date Planifiée', format_date(intervention.date_scheduled)],
                ['Technicien', intervention.technician_name or "Non assigné"],
                ['Statut', intervention.state or "N/A"],
                ['Description', intervention.name or "N/A"],
                ['Coût Total', f"{intervention.total_cost:,.2f} DA"],
            ]
            
            info_table = Table(info_data, colWidths=[5*cm, 11*cm])
            info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6750A4')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            
            story.append(info_table)
        
        # Générer PDF
        doc.build(story, onFirstPage=self._get_header_footer,
                  onLaterPages=self._get_header_footer)
        
        print(f"✓ Rapport intervention généré: {filepath}")
        return filepath
    
    def generate_monthly_report(self):
        """Génère le rapport mensuel"""
        filename = f"rapport_mensuel_{datetime.now().strftime('%Y%m')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=A4,
                                topMargin=4*cm, bottomMargin=2.5*cm)
        
        story = []
        styles = getSampleStyleSheet()
        
        # Titre
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#6750A4'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        story.append(Paragraph(f"📊 Rapport Mensuel - {datetime.now().strftime('%B %Y')}", title_style))
        story.append(Spacer(1, 0.5*cm))
        
        # Statistiques
        stats = self.controller.get_maintenance_stats()
        
        stats_data = [
            ['Indicateur', 'Valeur', 'Tendance'],
            ['Interventions Réalisées', str(stats['monthly_interventions']), '📈 +12%'],
            ['Contrats Actifs', str(stats['active_contracts']), '➡️ Stable'],
            ['Revenus Générés', f"{stats['monthly_revenue']:,.0f} DA", '📈 +8%'],
            ['Pièces Consommées', '24', '➡️ Normal'],
        ]
        
        stats_table = Table(stats_data, colWidths=[8*cm, 4*cm, 4*cm])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10B981')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        story.append(stats_table)
        story.append(Spacer(1, 1*cm))
        
        # Liste interventions du mois
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2563EB'),
            spaceAfter=15,
            fontName='Helvetica-Bold'
        )
        story.append(Paragraph("📋 Interventions du Mois", subtitle_style))
        
        interventions = self.controller.get_all_interventions()
        
        if interventions:
            from modules.maintenance.views import format_date
            
            inter_data = [['ID', 'Client', 'Machine', 'Type', 'Date', 'Statut']]
            for inter in interventions[:10]:  # Limiter à 10
                inter_data.append([
                    f"#{inter.id}",
                    inter.partner_name or "",
                    inter.machine_name or "",
                    "Prév." if inter.intervention_type == "preventive" else "Corr.",
                    format_date(inter.date_scheduled),
                    inter.state or ""
                ])
            
            inter_table = Table(inter_data, colWidths=[1.5*cm, 4*cm, 4*cm, 2*cm, 2.5*cm, 2.5*cm])
            inter_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            story.append(inter_table)
        
        # Générer PDF
        doc.build(story, onFirstPage=self._get_header_footer,
                  onLaterPages=self._get_header_footer)
        
        print(f"✓ Rapport mensuel généré: {filepath}")
        return filepath
    
    def generate_contract_report(self, contract_ref):
        """Génère le rapport d'un contrat"""
        filename = f"contrat_{contract_ref}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=A4,
                                topMargin=4*cm, bottomMargin=2.5*cm)
        
        story = []
        styles = getSampleStyleSheet()
        
        # Titre
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor('#2563EB'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        story.append(Paragraph(f"📋 Contrat de Maintenance {contract_ref}", title_style))
        story.append(Spacer(1, 0.5*cm))
        
        # Récupérer contrat
        contracts = self.controller.get_all_contracts()
        contract = next((c for c in contracts if c.reference == contract_ref), None)
        
        if contract:
            from modules.maintenance.views import format_date
            
            contract_data = [
                ['Champ', 'Valeur'],
                ['Référence', contract.reference or "N/A"],
                ['Client', contract.partner_name or "N/A"],
                ['Type', contract.contract_type or "N/A"],
                ['Date Début', format_date(contract.date_start)],
                ['Date Fin', format_date(contract.date_end)],
                ['Montant Total', f"{contract.total_amount:,.2f} DA"],
                ['Statut', contract.state or "N/A"],
            ]
            
            contract_table = Table(contract_data, colWidths=[5*cm, 11*cm])
            contract_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            
            story.append(contract_table)
        
        doc.build(story, onFirstPage=self._get_header_footer,
                  onLaterPages=self._get_header_footer)
        
        print(f"✓ Rapport contrat généré: {filepath}")
        return filepath
