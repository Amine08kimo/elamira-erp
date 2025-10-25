# -*- coding: utf-8 -*-
"""
Accounting Controller - Logique comptable DZ
"""

from typing import List, Optional
from datetime import datetime
from .models import AccountMove, AccountMoveLine, G12Declaration


class AccountingController:
    """Contrôleur pour la comptabilité"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    # === PLAN COMPTABLE NATIONAL ===
    
    def get_all_pcn_accounts(self) -> List[dict]:
        """Récupère tous les comptes PCN"""
        return self.db.fetch_all("""
            SELECT * FROM pcn_account 
            WHERE active = 1
            ORDER BY code
        """)
    
    def get_pcn_account_by_code(self, code: str) -> Optional[dict]:
        """Récupère un compte PCN par son code"""
        return self.db.fetch_one(
            "SELECT * FROM pcn_account WHERE code = ?",
            (code,)
        )
    
    # === ÉCRITURES COMPTABLES ===
    
    def create_account_move(self, move: AccountMove) -> int:
        """
        Crée une pièce comptable
        
        Args:
            move: Objet AccountMove
            
        Returns:
            ID de la pièce créée
        """
        # Générer le numéro si nécessaire
        if not move.name:
            move.name = self.db.get_next_sequence('account.move')
        
        # Insérer la pièce
        cursor = self.db.execute_query("""
            INSERT INTO account_move (
                name, ref, date, journal_id, state, amount_total, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            move.name, move.ref,
            move.date.isoformat() if move.date else datetime.now().isoformat(),
            move.journal_id, move.state, move.amount_total, move.notes
        ))
        
        move_id = cursor.lastrowid
        
        # Insérer les lignes
        for line in move.line_ids:
            self._create_move_line(move_id, line)
        
        return move_id
    
    def _create_move_line(self, move_id: int, line: AccountMoveLine):
        """Crée une ligne d'écriture"""
        self.db.execute_query("""
            INSERT INTO account_move_line (
                move_id, name, pcn_account_id, debit, credit, partner_id
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            move_id, line.name, line.pcn_account_id,
            line.debit, line.credit, line.partner_id
        ))
    
    def get_all_moves(self) -> List[AccountMove]:
        """Récupère toutes les pièces comptables"""
        rows = self.db.fetch_all("""
            SELECT * FROM account_move 
            ORDER BY date DESC, id DESC
        """)
        
        moves = []
        for row in rows:
            move = self._row_to_account_move(row)
            move.line_ids = self._get_move_lines(move.id)
            moves.append(move)
        
        return moves
    
    def _get_move_lines(self, move_id: int) -> List[AccountMoveLine]:
        """Récupère les lignes d'une pièce"""
        rows = self.db.fetch_all("""
            SELECT * FROM account_move_line 
            WHERE move_id = ? 
            ORDER BY id
        """, (move_id,))
        
        return [self._row_to_move_line(row) for row in rows]
    
    def _row_to_account_move(self, row: dict) -> AccountMove:
        """Convertit une ligne DB en AccountMove"""
        return AccountMove(
            id=row['id'],
            name=row['name'],
            ref=row.get('ref', ''),
            date=datetime.fromisoformat(row['date']) if row['date'] else None,
            journal_id=row['journal_id'],
            state=row['state'],
            amount_total=row.get('amount_total', 0.0),
            notes=row.get('notes', ''),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def _row_to_move_line(self, row: dict) -> AccountMoveLine:
        """Convertit une ligne DB en AccountMoveLine"""
        return AccountMoveLine(
            id=row['id'],
            move_id=row['move_id'],
            name=row['name'],
            pcn_account_id=row['pcn_account_id'],
            debit=row['debit'],
            credit=row['credit'],
            partner_id=row.get('partner_id')
        )
    
    # === DÉCLARATION G12 ===
    
    def create_g12_declaration(self, declaration: G12Declaration) -> int:
        """
        Crée une déclaration G12
        
        Args:
            declaration: Objet G12Declaration
            
        Returns:
            ID de la déclaration créée
        """
        # Calculer les totaux
        declaration.calculate_totals()
        
        # Générer le nom
        if not declaration.name:
            period = declaration.period_start.strftime("%m/%Y")
            declaration.name = f"G12-{period}"
        
        # Insérer
        cursor = self.db.execute_query("""
            INSERT INTO g12_declaration (
                name, period_start, period_end, state,
                ca_ht, ca_exonere, ca_total,
                tva_19_base, tva_19_amount, tva_9_base, tva_9_amount,
                tva_collectee_total, tva_deductible_immobilisations,
                tva_deductible_biens, tva_deductible_services,
                tva_deductible_total, tva_due, tva_credit_report,
                tva_a_payer, tap_base, tap_rate, tap_amount
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            declaration.name,
            declaration.period_start.isoformat(),
            declaration.period_end.isoformat(),
            declaration.state,
            declaration.ca_ht, declaration.ca_exonere, declaration.ca_total,
            declaration.tva_19_base, declaration.tva_19_amount,
            declaration.tva_9_base, declaration.tva_9_amount,
            declaration.tva_collectee_total,
            declaration.tva_deductible_immobilisations,
            declaration.tva_deductible_biens,
            declaration.tva_deductible_services,
            declaration.tva_deductible_total,
            declaration.tva_due, declaration.tva_credit_report,
            declaration.tva_a_payer,
            declaration.tap_base, declaration.tap_rate, declaration.tap_amount
        ))
        
        return cursor.lastrowid
    
    def get_all_g12_declarations(self) -> List[G12Declaration]:
        """Récupère toutes les déclarations G12"""
        rows = self.db.fetch_all("""
            SELECT * FROM g12_declaration 
            ORDER BY period_start DESC
        """)
        
        return [self._row_to_g12(row) for row in rows]
    
    def _row_to_g12(self, row: dict) -> G12Declaration:
        """Convertit une ligne DB en G12Declaration"""
        return G12Declaration(
            id=row['id'],
            name=row['name'],
            period_start=datetime.fromisoformat(row['period_start']),
            period_end=datetime.fromisoformat(row['period_end']),
            state=row['state'],
            ca_ht=row['ca_ht'],
            ca_exonere=row.get('ca_exonere', 0.0),
            ca_total=row['ca_total'],
            tva_19_base=row['tva_19_base'],
            tva_19_amount=row['tva_19_amount'],
            tva_9_base=row.get('tva_9_base', 0.0),
            tva_9_amount=row.get('tva_9_amount', 0.0),
            tva_collectee_total=row['tva_collectee_total'],
            tva_deductible_immobilisations=row.get('tva_deductible_immobilisations', 0.0),
            tva_deductible_biens=row.get('tva_deductible_biens', 0.0),
            tva_deductible_services=row.get('tva_deductible_services', 0.0),
            tva_deductible_total=row['tva_deductible_total'],
            tva_due=row['tva_due'],
            tva_credit_report=row.get('tva_credit_report', 0.0),
            tva_a_payer=row['tva_a_payer'],
            tap_base=row.get('tap_base', 0.0),
            tap_rate=row.get('tap_rate', 2.0),
            tap_amount=row.get('tap_amount', 0.0),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def generate_g12_from_sales(self, period_start: datetime, period_end: datetime) -> G12Declaration:
        """
        Génère automatiquement une déclaration G12 à partir des factures de vente
        
        Args:
            period_start: Début de période
            period_end: Fin de période
            
        Returns:
            Objet G12Declaration pré-rempli
        """
        declaration = G12Declaration()
        declaration.period_start = period_start
        declaration.period_end = period_end
        
        # Récupérer les factures de la période
        sales = self.db.fetch_all("""
            SELECT 
                SUM(amount_untaxed) as total_ht,
                SUM(amount_tax) as total_tva,
                SUM(amount_tap) as total_tap
            FROM sale_order
            WHERE date_order BETWEEN ? AND ?
            AND state IN ('confirmed', 'done')
        """, (period_start.isoformat(), period_end.isoformat()))
        
        if sales and sales[0]['total_ht']:
            declaration.ca_ht = sales[0]['total_ht']
            declaration.tva_19_base = sales[0]['total_ht']  # Simplification
            declaration.tap_base = sales[0]['total_ht']
        
        # Calculer les totaux
        declaration.calculate_totals()
        
        return declaration
