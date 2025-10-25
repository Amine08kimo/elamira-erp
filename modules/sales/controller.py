# -*- coding: utf-8 -*-
"""
Sales Controller - Logique métier pour les ventes
"""

from typing import List, Optional
from datetime import datetime
from .models import SaleOrder, SaleOrderLine, Partner


class SalesController:
    """Contrôleur pour la gestion des ventes"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    # === GESTION DES PARTENAIRES ===
    
    def create_partner(self, partner: Partner) -> int:
        """
        Crée un nouveau partenaire
        
        Args:
            partner: Objet Partner à créer
            
        Returns:
            ID du partenaire créé
        """
        cursor = self.db.execute_query("""
            INSERT INTO res_partner (
                name, name_ar, address, address_ar, phone, email,
                nif, nis, art, is_customer, is_supplier, active
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            partner.name, partner.name_ar, partner.address, partner.address_ar,
            partner.phone, partner.email, partner.nif, partner.nis, partner.art,
            partner.is_customer, partner.is_supplier, partner.active
        ))
        
        return cursor.lastrowid
    
    def get_all_partners(self, is_customer: bool = True) -> List[Partner]:
        """Récupère tous les partenaires"""
        rows = self.db.fetch_all("""
            SELECT * FROM res_partner 
            WHERE is_customer = ? AND active = 1
            ORDER BY name
        """, (is_customer,))
        
        return [self._row_to_partner(row) for row in rows]
    
    def get_partner(self, partner_id: int) -> Optional[Partner]:
        """Récupère un partenaire par ID"""
        row = self.db.fetch_one(
            "SELECT * FROM res_partner WHERE id = ?",
            (partner_id,)
        )
        
        return self._row_to_partner(row) if row else None
    
    def _row_to_partner(self, row: dict) -> Partner:
        """Convertit une ligne DB en objet Partner"""
        return Partner(
            id=row['id'],
            name=row['name'],
            name_ar=row.get('name_ar', ''),
            address=row.get('address', ''),
            address_ar=row.get('address_ar', ''),
            phone=row.get('phone', ''),
            email=row.get('email', ''),
            nif=row.get('nif', ''),
            nis=row.get('nis', ''),
            art=row.get('art', ''),
            is_customer=bool(row['is_customer']),
            is_supplier=bool(row.get('is_supplier', 0)),
            active=bool(row['active']),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    # === GESTION DES COMMANDES ===
    
    def create_sale_order(self, order: SaleOrder) -> int:
        """
        Crée une nouvelle commande de vente
        
        Args:
            order: Objet SaleOrder à créer
            
        Returns:
            ID de la commande créée
        """
        # Calculer les totaux
        order.calculate_totals()
        
        # Générer le numéro de facture
        if not order.name:
            order.name = self.db.get_next_sequence('sale.order')
        
        # Insérer la commande
        cursor = self.db.execute_query("""
            INSERT INTO sale_order (
                name, partner_id, date_order, date_due, state,
                amount_untaxed, amount_tax, amount_tap, amount_stamp, amount_total,
                notes, payment_term
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            order.name, order.partner_id,
            order.date_order.isoformat() if order.date_order else datetime.now().isoformat(),
            order.date_due.isoformat() if order.date_due else None,
            order.state,
            order.amount_untaxed, order.amount_tax, order.amount_tap,
            order.amount_stamp, order.amount_total,
            order.notes, order.payment_term
        ))
        
        order_id = cursor.lastrowid
        
        # Insérer les lignes
        for line in order.order_lines:
            self._create_order_line(order_id, line)
        
        return order_id
    
    def _create_order_line(self, order_id: int, line: SaleOrderLine):
        """Crée une ligne de commande"""
        line.calculate_amounts()
        
        self.db.execute_query("""
            INSERT INTO sale_order_line (
                order_id, product_id, product_name, description,
                quantity, price_unit, tax_id, tax_rate, discount,
                subtotal, tax_amount, total
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            order_id, line.product_id, line.product_name, line.description,
            line.quantity, line.price_unit, line.tax_id, line.tax_rate,
            line.discount, line.subtotal, line.tax_amount, line.total
        ))
    
    def get_all_orders(self, state: str = None) -> List[SaleOrder]:
        """
        Récupère toutes les commandes
        
        Args:
            state: Filtrer par état (optionnel)
        """
        if state:
            query = "SELECT * FROM sale_order WHERE state = ? ORDER BY date_order DESC"
            rows = self.db.fetch_all(query, (state,))
        else:
            rows = self.db.fetch_all(
                "SELECT * FROM sale_order ORDER BY date_order DESC"
            )
        
        orders = []
        for row in rows:
            order = self._row_to_sale_order(row)
            # Charger les lignes
            order.order_lines = self._get_order_lines(order.id)
            orders.append(order)
        
        return orders
    
    def get_sale_order(self, order_id: int) -> Optional[SaleOrder]:
        """Récupère une commande par ID"""
        row = self.db.fetch_one(
            "SELECT * FROM sale_order WHERE id = ?",
            (order_id,)
        )
        
        if not row:
            return None
        
        order = self._row_to_sale_order(row)
        order.order_lines = self._get_order_lines(order_id)
        
        return order
    
    def _get_order_lines(self, order_id: int) -> List[SaleOrderLine]:
        """Récupère les lignes d'une commande"""
        rows = self.db.fetch_all(
            "SELECT * FROM sale_order_line WHERE order_id = ? ORDER BY id",
            (order_id,)
        )
        
        return [self._row_to_order_line(row) for row in rows]
    
    def _row_to_sale_order(self, row: dict) -> SaleOrder:
        """Convertit une ligne DB en objet SaleOrder"""
        return SaleOrder(
            id=row['id'],
            name=row['name'],
            partner_id=row['partner_id'],
            date_order=datetime.fromisoformat(row['date_order']) if row['date_order'] else None,
            date_due=datetime.fromisoformat(row['date_due']) if row.get('date_due') else None,
            state=row['state'],
            amount_untaxed=row['amount_untaxed'],
            amount_tax=row['amount_tax'],
            amount_tap=row.get('amount_tap', 0.0),
            amount_stamp=row.get('amount_stamp', 0.0),
            amount_total=row['amount_total'],
            notes=row.get('notes', ''),
            payment_term=row.get('payment_term', ''),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def _row_to_order_line(self, row: dict) -> SaleOrderLine:
        """Convertit une ligne DB en objet SaleOrderLine"""
        return SaleOrderLine(
            id=row['id'],
            order_id=row['order_id'],
            product_id=row['product_id'],
            product_name=row['product_name'],
            description=row.get('description', ''),
            quantity=row['quantity'],
            price_unit=row['price_unit'],
            tax_id=row.get('tax_id'),
            tax_rate=row.get('tax_rate', 0.0),
            discount=row.get('discount', 0.0),
            subtotal=row['subtotal'],
            tax_amount=row['tax_amount'],
            total=row['total']
        )
    
    def confirm_order(self, order_id: int) -> bool:
        """Confirme une commande"""
        self.db.execute_query("""
            UPDATE sale_order 
            SET state = 'confirmed', updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (order_id,))
        
        return True
    
    def cancel_order(self, order_id: int) -> bool:
        """Annule une commande"""
        self.db.execute_query("""
            UPDATE sale_order 
            SET state = 'cancelled', updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (order_id,))
        
        return True
