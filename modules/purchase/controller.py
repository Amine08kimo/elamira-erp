# -*- coding: utf-8 -*-
"""
Purchase Controller - Logique métier pour les achats
"""

from typing import List, Optional, Dict
from datetime import datetime
from .models import PurchaseOrder, PurchaseOrderLine


class PurchaseController:
    """Contrôleur pour la gestion des achats fournisseurs"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def create_purchase_order(self, order: PurchaseOrder) -> int:
        """
        Crée une nouvelle commande d'achat
        
        Args:
            order: Objet PurchaseOrder à créer
            
        Returns:
            ID de la commande créée
        """
        # Générer le numéro de commande
        if not order.name:
            order.name = self.db.get_next_sequence('purchase.order')
        
        # Créer l'en-tête de commande
        cursor = self.db.execute_query("""
            INSERT INTO purchase_order (
                name, partner_id, supplier_invoice_ref,
                date_order, date_due, state,
                amount_untaxed, amount_tax, amount_total,
                notes, payment_term
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            order.name, order.partner_id, order.supplier_invoice_ref,
            order.date_order.isoformat() if order.date_order else None,
            order.date_due.isoformat() if order.date_due else None,
            order.state,
            order.amount_untaxed, order.amount_tax, order.amount_total,
            order.notes, order.payment_term
        ))
        
        order_id = cursor.lastrowid
        
        # Créer les lignes
        for line in order.lines:
            self.create_purchase_order_line(order_id, line)
        
        return order_id
    
    def create_purchase_order_line(self, order_id: int, line: PurchaseOrderLine):
        """Crée une ligne de commande d'achat"""
        line.calculate_amounts()
        
        self.db.execute_query("""
            INSERT INTO purchase_order_line (
                order_id, product_id, product_name, description,
                quantity, price_unit, tax_rate,
                subtotal, tax_amount, total
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            order_id, line.product_id, line.product_name, line.description,
            line.quantity, line.price_unit, line.tax_rate,
            line.subtotal, line.tax_amount, line.total
        ))
    
    def get_all_purchase_orders(self) -> List[PurchaseOrder]:
        """Récupère toutes les commandes d'achat"""
        rows = self.db.fetch_all("""
            SELECT po.*, p.name as partner_name
            FROM purchase_order po
            LEFT JOIN res_partner p ON po.partner_id = p.id
            ORDER BY po.date_order DESC
        """)
        
        orders = []
        for row in rows:
            order = self._row_to_purchase_order(row)
            order.lines = self.get_order_lines(order.id)
            orders.append(order)
        
        return orders
    
    def get_purchase_order_by_id(self, order_id: int) -> Optional[PurchaseOrder]:
        """Récupère une commande d'achat par ID"""
        row = self.db.fetch_one("""
            SELECT po.*, p.name as partner_name
            FROM purchase_order po
            LEFT JOIN res_partner p ON po.partner_id = p.id
            WHERE po.id = ?
        """, (order_id,))
        
        if not row:
            return None
        
        order = self._row_to_purchase_order(row)
        order.lines = self.get_order_lines(order_id)
        
        return order
    
    def get_order_lines(self, order_id: int) -> List[PurchaseOrderLine]:
        """Récupère les lignes d'une commande"""
        rows = self.db.fetch_all("""
            SELECT * FROM purchase_order_line
            WHERE order_id = ?
            ORDER BY id
        """, (order_id,))
        
        return [self._row_to_purchase_order_line(row) for row in rows]
    
    def update_purchase_order(self, order: PurchaseOrder) -> bool:
        """Met à jour une commande d'achat"""
        self.db.execute_query("""
            UPDATE purchase_order SET
                partner_id = ?,
                supplier_invoice_ref = ?,
                date_order = ?,
                date_due = ?,
                date_received = ?,
                state = ?,
                amount_untaxed = ?,
                amount_tax = ?,
                amount_total = ?,
                notes = ?,
                payment_term = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            order.partner_id, order.supplier_invoice_ref,
            order.date_order.isoformat() if order.date_order else None,
            order.date_due.isoformat() if order.date_due else None,
            order.date_received.isoformat() if order.date_received else None,
            order.state,
            order.amount_untaxed, order.amount_tax, order.amount_total,
            order.notes, order.payment_term,
            order.id
        ))
        
        return True
    
    def delete_purchase_order(self, order_id: int) -> bool:
        """Supprime une commande d'achat (seulement si brouillon)"""
        # Vérifier que c'est un brouillon
        order = self.get_purchase_order_by_id(order_id)
        if not order or order.state != 'draft':
            return False
        
        # Supprimer les lignes
        self.db.execute_query("""
            DELETE FROM purchase_order_line WHERE order_id = ?
        """, (order_id,))
        
        # Supprimer la commande
        self.db.execute_query("""
            DELETE FROM purchase_order WHERE id = ?
        """, (order_id,))
        
        return True
    
    def confirm_purchase_order(self, order_id: int) -> bool:
        """Confirme une commande d'achat"""
        self.db.execute_query("""
            UPDATE purchase_order SET
                state = 'confirmed',
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND state = 'draft'
        """, (order_id,))
        
        return True
    
    def receive_purchase_order(self, order_id: int) -> bool:
        """
        Marque une commande comme réceptionnée
        Met à jour le stock des produits
        """
        order = self.get_purchase_order_by_id(order_id)
        if not order or order.state not in ['confirmed']:
            return False
        
        # Mettre à jour le stock pour chaque ligne
        for line in order.lines:
            if line.product_id:
                self.db.execute_query("""
                    UPDATE product_product
                    SET qty_available = qty_available + ?
                    WHERE id = ?
                """, (line.quantity, line.product_id))
        
        # Mettre à jour le statut de la commande
        self.db.execute_query("""
            UPDATE purchase_order SET
                state = 'received',
                date_received = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (datetime.now().isoformat(), order_id))
        
        return True
    
    def get_purchase_stats(self) -> Dict:
        """Retourne des statistiques sur les achats"""
        stats = {}
        
        # Total des achats
        total = self.db.fetch_one("""
            SELECT 
                COUNT(*) as count,
                SUM(amount_total) as total_amount
            FROM purchase_order
            WHERE state != 'cancelled'
        """)
        
        stats['total_orders'] = total['count'] if total else 0
        stats['total_amount'] = total['total_amount'] if total and total['total_amount'] else 0
        
        # Achats du mois en cours
        month = self.db.fetch_one("""
            SELECT 
                COUNT(*) as count,
                SUM(amount_total) as total_amount
            FROM purchase_order
            WHERE state != 'cancelled'
            AND strftime('%Y-%m', date_order) = strftime('%Y-%m', 'now')
        """)
        
        stats['month_orders'] = month['count'] if month else 0
        stats['month_amount'] = month['total_amount'] if month and month['total_amount'] else 0
        
        # En attente de réception
        pending = self.db.fetch_one("""
            SELECT COUNT(*) as count
            FROM purchase_order
            WHERE state = 'confirmed'
        """)
        
        stats['pending_reception'] = pending['count'] if pending else 0
        
        return stats
    
    def _row_to_purchase_order(self, row: dict) -> PurchaseOrder:
        """Convertit une ligne DB en PurchaseOrder"""
        return PurchaseOrder(
            id=row['id'],
            name=row['name'],
            partner_id=row.get('partner_id'),
            partner_name=row.get('partner_name', ''),
            supplier_invoice_ref=row.get('supplier_invoice_ref', ''),
            date_order=datetime.fromisoformat(row['date_order']) if row.get('date_order') else None,
            date_due=datetime.fromisoformat(row['date_due']) if row.get('date_due') else None,
            date_received=datetime.fromisoformat(row['date_received']) if row.get('date_received') else None,
            state=row['state'],
            amount_untaxed=row.get('amount_untaxed', 0.0),
            amount_tax=row.get('amount_tax', 0.0),
            amount_total=row.get('amount_total', 0.0),
            notes=row.get('notes', ''),
            payment_term=row.get('payment_term', ''),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def _row_to_purchase_order_line(self, row: dict) -> PurchaseOrderLine:
        """Convertit une ligne DB en PurchaseOrderLine"""
        return PurchaseOrderLine(
            id=row['id'],
            order_id=row['order_id'],
            product_id=row.get('product_id'),
            product_name=row.get('product_name', ''),
            description=row.get('description', ''),
            quantity=row.get('quantity', 0.0),
            price_unit=row.get('price_unit', 0.0),
            tax_rate=row.get('tax_rate', 19.0),
            subtotal=row.get('subtotal', 0.0),
            tax_amount=row.get('tax_amount', 0.0),
            total=row.get('total', 0.0)
        )
