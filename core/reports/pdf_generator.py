# -*- coding: utf-8 -*-
"""
PDF Generator - Génération de documents PDF professionnels
Utilise ReportLab pour créer des factures conformes DGI
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph,
    Spacer, Image, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import os


class InvoicePDFGenerator:
    """Générateur de factures PDF style professionnel"""
    
    def __init__(self, output_path="invoices"):
        self.output_path = output_path
        os.makedirs(output_path, exist_ok=True)
        
        # Styles
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configure les styles personnalisés"""
        # Titre principal
        self.styles.add(ParagraphStyle(
            name='InvoiceTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#6750A4'),
            spaceAfter=12,
            alignment=TA_CENTER
        ))
        
        # Sous-titre
        self.styles.add(ParagraphStyle(
            name='InvoiceSubtitle',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.grey,
            alignment=TA_CENTER
        ))
        
        # Texte normal
        self.styles.add(ParagraphStyle(
            name='InvoiceNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            leading=14
        ))
        
        # Petit texte
        self.styles.add(ParagraphStyle(
            name='InvoiceSmall',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.grey
        ))
    
    def generate_invoice_pdf(self, invoice_data, company_data, filename=None):
        """
        Génère un PDF de facture
        
        Args:
            invoice_data: dict avec les données de la facture
            company_data: dict avec les données de la société
            filename: nom du fichier (optionnel)
        
        Returns:
            Chemin du fichier PDF créé
        """
        if not filename:
            filename = f"facture_{invoice_data['number']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        filepath = os.path.join(self.output_path, filename)
        
        # Créer le document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Contenu
        story = []
        
        # En-tête société
        story.extend(self._create_header(company_data))
        story.append(Spacer(1, 0.5*cm))
        
        # Titre FACTURE
        story.append(Paragraph("FACTURE", self.styles['InvoiceTitle']))
        story.append(Paragraph(
            f"N° {invoice_data['number']}", 
            self.styles['InvoiceSubtitle']
        ))
        story.append(Spacer(1, 1*cm))
        
        # Informations client et facture
        story.extend(self._create_invoice_info(invoice_data))
        story.append(Spacer(1, 1*cm))
        
        # Lignes de facture
        story.extend(self._create_invoice_lines(invoice_data['lines']))
        story.append(Spacer(1, 1*cm))
        
        # Totaux
        story.extend(self._create_totals(invoice_data))
        story.append(Spacer(1, 1*cm))
        
        # Pied de page
        story.extend(self._create_footer(company_data))
        
        # Construire le PDF
        doc.build(story)
        
        return filepath
    
    def _create_header(self, company_data):
        """Crée l'en-tête avec les infos de la société"""
        elements = []
        
        # Table avec logo et infos société
        data = [[
            [
                Paragraph(f"<b>{company_data.get('name', '')}</b>", self.styles['InvoiceNormal']),
                Paragraph(company_data.get('address', ''), self.styles['InvoiceSmall']),
                Paragraph(f"Tél: {company_data.get('phone', '')}", self.styles['InvoiceSmall']),
                Paragraph(f"Email: {company_data.get('email', '')}", self.styles['InvoiceSmall']),
            ],
            [
                Paragraph(f"<b>NIF:</b> {company_data.get('nif', '')}", self.styles['InvoiceSmall']),
                Paragraph(f"<b>NIS:</b> {company_data.get('nis', '')}", self.styles['InvoiceSmall']),
                Paragraph(f"<b>ART:</b> {company_data.get('art', '')}", self.styles['InvoiceSmall']),
            ]
        ]]
        
        table = Table(data, colWidths=[10*cm, 7*cm])
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#6750A4')),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _create_invoice_info(self, invoice_data):
        """Crée le bloc informations client et facture"""
        elements = []
        
        customer = invoice_data.get('customer', {})
        
        data = [
            [
                [
                    Paragraph("<b>CLIENT:</b>", self.styles['InvoiceNormal']),
                    Paragraph(customer.get('name', ''), self.styles['InvoiceNormal']),
                    Paragraph(customer.get('address', ''), self.styles['InvoiceSmall']),
                    Paragraph(f"NIF: {customer.get('nif', '')}", self.styles['InvoiceSmall']),
                    Paragraph(f"NIS: {customer.get('nis', '')}", self.styles['InvoiceSmall']),
                    Paragraph(f"ART: {customer.get('art', '')}", self.styles['InvoiceSmall']),
                ],
                [
                    Paragraph(f"<b>Date:</b> {invoice_data.get('date', '')}", self.styles['InvoiceNormal']),
                    Paragraph(f"<b>Échéance:</b> {invoice_data.get('due_date', '')}", self.styles['InvoiceNormal']),
                    Paragraph(f"<b>Mode de paiement:</b> {invoice_data.get('payment_term', 'Net 30')}", self.styles['InvoiceSmall']),
                ]
            ]
        ]
        
        table = Table(data, colWidths=[10*cm, 7*cm])
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOX', (0, 0), (-1, -1), 1, colors.lightgrey),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F9FAFB')),
            ('PADDING', (0, 0), (-1, -1), 10),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _create_invoice_lines(self, lines):
        """Crée le tableau des lignes de facture"""
        elements = []
        
        # En-tête du tableau
        data = [[
            Paragraph("<b>Désignation</b>", self.styles['InvoiceSmall']),
            Paragraph("<b>Qté</b>", self.styles['InvoiceSmall']),
            Paragraph("<b>Prix U.</b>", self.styles['InvoiceSmall']),
            Paragraph("<b>TVA</b>", self.styles['InvoiceSmall']),
            Paragraph("<b>Total HT</b>", self.styles['InvoiceSmall']),
        ]]
        
        # Lignes
        for line in lines:
            data.append([
                Paragraph(line.get('product_name', ''), self.styles['InvoiceSmall']),
                Paragraph(str(line.get('quantity', 0)), self.styles['InvoiceSmall']),
                Paragraph(f"{line.get('price_unit', 0):,.2f} DA", self.styles['InvoiceSmall']),
                Paragraph(f"{line.get('tax_rate', 0)}%", self.styles['InvoiceSmall']),
                Paragraph(f"{line.get('subtotal', 0):,.2f} DA", self.styles['InvoiceSmall']),
            ])
        
        table = Table(data, colWidths=[7*cm, 2*cm, 3*cm, 2*cm, 3*cm])
        table.setStyle(TableStyle([
            # En-tête
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6750A4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (1, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Lignes
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('PADDING', (0, 0), (-1, -1), 8),
            
            # Lignes alternées
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _create_totals(self, invoice_data):
        """Crée le tableau des totaux"""
        elements = []
        
        data = []
        
        # Total HT
        data.append([
            Paragraph("<b>Total HT:</b>", self.styles['InvoiceNormal']),
            Paragraph(f"{invoice_data.get('amount_untaxed', 0):,.2f} DA", self.styles['InvoiceNormal'])
        ])
        
        # TVA
        data.append([
            Paragraph("TVA:", self.styles['InvoiceNormal']),
            Paragraph(f"{invoice_data.get('amount_tax', 0):,.2f} DA", self.styles['InvoiceNormal'])
        ])
        
        # TAP si applicable
        if invoice_data.get('amount_tap', 0) > 0:
            data.append([
                Paragraph("TAP (2%):", self.styles['InvoiceNormal']),
                Paragraph(f"{invoice_data['amount_tap']:,.2f} DA", self.styles['InvoiceNormal'])
            ])
        
        # Timbre fiscal
        if invoice_data.get('amount_stamp', 0) > 0:
            data.append([
                Paragraph("Timbre Fiscal:", self.styles['InvoiceNormal']),
                Paragraph(f"{invoice_data['amount_stamp']:,.2f} DA", self.styles['InvoiceNormal'])
            ])
        
        # Total TTC
        data.append([
            Paragraph("<b>TOTAL TTC:</b>", self.styles['InvoiceTitle']),
            Paragraph(
                f"<b>{invoice_data.get('amount_total', 0):,.2f} DA</b>", 
                self.styles['InvoiceTitle']
            )
        ])
        
        table = Table(data, colWidths=[10*cm, 7*cm])
        table.setStyle(TableStyle([
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#6750A4')),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(table)
        
        return elements
    
    def _create_footer(self, company_data):
        """Crée le pied de page"""
        elements = []
        
        footer_text = f"""
        <para align=center fontSize=8 textColor=grey>
        {company_data.get('name', '')} - {company_data.get('address', '')}<br/>
        Tél: {company_data.get('phone', '')} - Email: {company_data.get('email', '')}<br/>
        NIF: {company_data.get('nif', '')} | NIS: {company_data.get('nis', '')} | ART: {company_data.get('art', '')}<br/>
        <br/>
        <i>Facture générée par ElAmira ERP - Conforme DGI Algérie 🇩🇿</i>
        </para>
        """
        
        elements.append(Spacer(1, 1*cm))
        elements.append(Paragraph(footer_text, self.styles['InvoiceSmall']))
        
        return elements


class G12PDFGenerator:
    """Générateur de déclarations G12 en PDF"""
    
    def __init__(self, output_path="g12"):
        self.output_path = output_path
        os.makedirs(output_path, exist_ok=True)
    
    def generate_g12_pdf(self, g12_data, company_data, filename=None):
        """Génère un PDF de déclaration G12"""
        # TODO: Implémenter la génération G12
        # Format officiel DGI avec tous les tableaux réglementaires
        pass


# Test
if __name__ == '__main__':
    # Test de génération
    generator = InvoicePDFGenerator()
    
    # Données de test
    invoice_data = {
        'number': 'FAC-00001',
        'date': '17/10/2024',
        'due_date': '16/11/2024',
        'payment_term': 'Net 30 jours',
        'customer': {
            'name': 'SARL TECH SOLUTIONS',
            'address': '123 Rue Didouche Mourad, Alger',
            'nif': '099912345678901',
            'nis': '12345678901234',
            'art': '16/00-1234567B09'
        },
        'lines': [
            {
                'product_name': 'Ordinateur Portable Dell',
                'quantity': 2,
                'price_unit': 85000,
                'tax_rate': 19,
                'subtotal': 170000
            },
            {
                'product_name': 'Imprimante HP LaserJet',
                'quantity': 1,
                'price_unit': 32000,
                'tax_rate': 19,
                'subtotal': 32000
            }
        ],
        'amount_untaxed': 202000,
        'amount_tax': 38380,
        'amount_tap': 0,
        'amount_stamp': 25,
        'amount_total': 240405
    }
    
    company_data = {
        'name': 'ElAmira SARL',
        'address': '1 Rue de la Liberté, Alger 16000',
        'phone': '023 45 67 89',
        'email': 'contact@elamira.dz',
        'nif': '099900000000000',
        'nis': '00000000000000',
        'art': '16/00-0000000B09'
    }
    
    pdf_path = generator.generate_invoice_pdf(invoice_data, company_data)
    print(f"✓ PDF généré : {pdf_path}")
