# -*- coding: utf-8 -*-
"""
Report Generator - Génération de rapports
Supporte PDF (conforme DZ), Excel, CSV
"""

import os
from typing import Dict, List, Any
from datetime import datetime


class ReportGenerator:
    """
    Générateur de rapports multi-formats
    Spécialisé pour les documents conformes DZ (factures, G12, etc.)
    """
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.templates_path = os.path.join('reports', 'templates')
    
    def to_pdf(self, data: Dict[str, Any], template_name: str, output_path: str) -> bool:
        """
        Génère un PDF à partir d'un template HTML
        
        Args:
            data: Dictionnaire de données à injecter dans le template
            template_name: Nom du fichier template (ex: 'invoice_dz_template.html')
            output_path: Chemin du fichier PDF de sortie
            
        Returns:
            True si succès, False sinon
        """
        try:
            # Charger le template HTML
            template_path = os.path.join(self.templates_path, template_name)
            
            if not os.path.exists(template_path):
                print(f"✗ Template introuvable: {template_path}")
                return False
            
            with open(template_path, 'r', encoding='utf-8') as f:
                html_template = f.read()
            
            # Remplacer les variables dans le template
            html_content = self._render_template(html_template, data)
            
            # Générer le PDF avec weasyprint
            try:
                from weasyprint import HTML, CSS
                
                HTML(string=html_content).write_pdf(
                    output_path,
                    stylesheets=[CSS(string=self._get_pdf_css())]
                )
                
                print(f"✓ PDF généré: {output_path}")
                return True
                
            except ImportError:
                print("⚠ weasyprint non installé. Installation: pip install weasyprint")
                # Fallback: sauvegarder en HTML
                html_output = output_path.replace('.pdf', '.html')
                with open(html_output, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print(f"→ Sauvegardé en HTML: {html_output}")
                return False
                
        except Exception as e:
            print(f"✗ Erreur génération PDF: {e}")
            return False
    
    def _render_template(self, template: str, data: Dict[str, Any]) -> str:
        """
        Remplace les variables {{ variable }} dans le template
        
        Args:
            template: Contenu HTML du template
            data: Dictionnaire des données
            
        Returns:
            HTML rendu
        """
        result = template
        
        # Remplacer les variables simples
        for key, value in data.items():
            placeholder = f"{{{{{key}}}}}"
            result = result.replace(placeholder, str(value))
        
        # Traiter les boucles {% for item in items %}
        # (Version simplifiée, pour production utiliser Jinja2)
        
        return result
    
    def _get_pdf_css(self) -> str:
        """
        Retourne le CSS pour les PDFs
        
        Returns:
            CSS en string
        """
        return """
        @page {
            size: A4;
            margin: 2cm;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            font-size: 10pt;
            color: #333;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 20px;
        }
        
        .company-info {
            margin-bottom: 20px;
        }
        
        .invoice-title {
            font-size: 24pt;
            font-weight: bold;
            color: #667eea;
            margin: 20px 0;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        
        th {
            background: #f3f4f6;
            padding: 10px;
            text-align: left;
            border-bottom: 2px solid #667eea;
            font-weight: 600;
        }
        
        td {
            padding: 8px 10px;
            border-bottom: 1px solid #e5e7eb;
        }
        
        .text-right {
            text-align: right;
        }
        
        .totals {
            margin-top: 30px;
            float: right;
            width: 40%;
        }
        
        .totals table {
            border: none;
        }
        
        .totals td {
            border: none;
        }
        
        .total-line {
            font-weight: bold;
            font-size: 12pt;
            background: #f3f4f6;
        }
        
        .footer {
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
            font-size: 9pt;
            color: #6b7280;
        }
        """
    
    def generate_invoice_pdf(self, order_id: int, output_path: str) -> bool:
        """
        Génère une facture PDF conforme DZ
        
        Args:
            order_id: ID de la commande
            output_path: Chemin de sortie
            
        Returns:
            True si succès
        """
        # Récupérer les données de la facture
        order = self.db_manager.fetch_one(
            "SELECT * FROM sale_order WHERE id = ?",
            (order_id,)
        )
        
        if not order:
            print(f"✗ Commande {order_id} introuvable")
            return False
        
        # Récupérer le partenaire
        partner = self.db_manager.fetch_one(
            "SELECT * FROM res_partner WHERE id = ?",
            (order['partner_id'],)
        )
        
        # Récupérer les lignes
        lines = self.db_manager.fetch_all(
            "SELECT * FROM sale_order_line WHERE order_id = ?",
            (order_id,)
        )
        
        # Récupérer les infos société
        company = self.db_manager.fetch_one("SELECT * FROM res_company LIMIT 1")
        
        # Construire les données pour le template
        data = {
            'invoice_number': order['name'],
            'invoice_date': order['date_order'][:10] if order['date_order'] else '',
            'due_date': order['date_due'][:10] if order.get('date_due') else '',
            
            # Société
            'company_name': company['name'] if company else 'Société',
            'company_address': company.get('address', '') if company else '',
            'company_phone': company.get('phone', '') if company else '',
            'company_nif': company.get('nif', '') if company else '',
            'company_nis': company.get('nis', '') if company else '',
            'company_art': company.get('art', '') if company else '',
            
            # Client
            'customer_name': partner['name'] if partner else '',
            'customer_address': partner.get('address', '') if partner else '',
            'customer_nif': partner.get('nif', '') if partner else '',
            'customer_nis': partner.get('nis', '') if partner else '',
            'customer_art': partner.get('art', '') if partner else '',
            
            # Totaux
            'amount_untaxed': f"{order['amount_untaxed']:,.2f}",
            'amount_tax': f"{order['amount_tax']:,.2f}",
            'amount_tap': f"{order.get('amount_tap', 0):,.2f}",
            'amount_stamp': f"{order.get('amount_stamp', 0):,.2f}",
            'amount_total': f"{order['amount_total']:,.2f}",
            
            # Lignes (HTML)
            'lines_html': self._generate_lines_html(lines)
        }
        
        # Générer le PDF
        return self.to_pdf(data, 'invoice_dz_template.html', output_path)
    
    def _generate_lines_html(self, lines: List[Dict]) -> str:
        """Génère le HTML des lignes de facture"""
        html = ""
        for line in lines:
            html += f"""
            <tr>
                <td>{line['product_name']}</td>
                <td class="text-right">{line['quantity']:.2f}</td>
                <td class="text-right">{line['price_unit']:,.2f} DA</td>
                <td class="text-right">{line.get('tax_rate', 0):.0f}%</td>
                <td class="text-right">{line['subtotal']:,.2f} DA</td>
            </tr>
            """
        return html
    
    def to_excel(self, data: List[Dict], output_path: str, sheet_name: str = 'Data') -> bool:
        """
        Exporte des données vers Excel
        
        Args:
            data: Liste de dictionnaires
            output_path: Chemin du fichier Excel
            sheet_name: Nom de la feuille
            
        Returns:
            True si succès
        """
        try:
            import pandas as pd
            
            df = pd.DataFrame(data)
            df.to_excel(output_path, sheet_name=sheet_name, index=False)
            
            print(f"✓ Excel généré: {output_path}")
            return True
            
        except ImportError:
            print("⚠ pandas non installé. Installation: pip install pandas openpyxl")
            return False
        except Exception as e:
            print(f"✗ Erreur génération Excel: {e}")
            return False
    
    def to_csv(self, data: List[Dict], output_path: str) -> bool:
        """
        Exporte des données vers CSV
        
        Args:
            data: Liste de dictionnaires
            output_path: Chemin du fichier CSV
            
        Returns:
            True si succès
        """
        try:
            import pandas as pd
            
            df = pd.DataFrame(data)
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            
            print(f"✓ CSV généré: {output_path}")
            return True
            
        except ImportError:
            print("⚠ pandas non installé. Installation: pip install pandas")
            return False
        except Exception as e:
            print(f"✗ Erreur génération CSV: {e}")
            return False
    
    def generate_g12_pdf(self, declaration_id: int, output_path: str) -> bool:
        """
        Génère un PDF de déclaration G12 (format DGI)
        
        Args:
            declaration_id: ID de la déclaration
            output_path: Chemin de sortie
            
        Returns:
            True si succès
        """
        # Récupérer la déclaration
        decl = self.db_manager.fetch_one(
            "SELECT * FROM g12_declaration WHERE id = ?",
            (declaration_id,)
        )
        
        if not decl:
            print(f"✗ Déclaration {declaration_id} introuvable")
            return False
        
        # Récupérer les infos société
        company = self.db_manager.fetch_one("SELECT * FROM res_company LIMIT 1")
        
        # Construire les données
        data = {
            'declaration_number': decl['name'],
            'period_start': decl['period_start'][:10],
            'period_end': decl['period_end'][:10],
            
            # Société
            'company_name': company['name'] if company else '',
            'company_nif': company.get('nif', '') if company else '',
            'company_nis': company.get('nis', '') if company else '',
            'company_art': company.get('art', '') if company else '',
            
            # CA
            'ca_ht': f"{decl['ca_ht']:,.2f}",
            'ca_exonere': f"{decl.get('ca_exonere', 0):,.2f}",
            'ca_total': f"{decl['ca_total']:,.2f}",
            
            # TVA Collectée
            'tva_19_base': f"{decl['tva_19_base']:,.2f}",
            'tva_19_amount': f"{decl['tva_19_amount']:,.2f}",
            'tva_9_base': f"{decl.get('tva_9_base', 0):,.2f}",
            'tva_9_amount': f"{decl.get('tva_9_amount', 0):,.2f}",
            'tva_collectee_total': f"{decl['tva_collectee_total']:,.2f}",
            
            # TVA Déductible
            'tva_ded_immo': f"{decl.get('tva_deductible_immobilisations', 0):,.2f}",
            'tva_ded_biens': f"{decl.get('tva_deductible_biens', 0):,.2f}",
            'tva_ded_services': f"{decl.get('tva_deductible_services', 0):,.2f}",
            'tva_deductible_total': f"{decl['tva_deductible_total']:,.2f}",
            
            # TVA Due
            'tva_due': f"{decl['tva_due']:,.2f}",
            'tva_credit': f"{decl.get('tva_credit_report', 0):,.2f}",
            'tva_a_payer': f"{decl['tva_a_payer']:,.2f}",
            
            # TAP
            'tap_base': f"{decl.get('tap_base', 0):,.2f}",
            'tap_rate': f"{decl.get('tap_rate', 2):.1f}",
            'tap_amount': f"{decl.get('tap_amount', 0):,.2f}",
        }
        
        # Générer le PDF
        return self.to_pdf(data, 'g12_template.html', output_path)
