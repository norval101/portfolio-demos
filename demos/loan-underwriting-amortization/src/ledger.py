"""
Double-Entry General Ledger accounting engine enforcing Debit == Credit invariant.
"""

from typing import List, Dict
from datetime import datetime, timezone
import uuid
from .models import JournalEntry, LedgerEntryLine


class LedgerBalanceError(Exception):
    """Raised when a Journal Entry violates the fundamental accounting equation."""
    pass


class DoubleEntryLedger:
    def __init__(self):
        self._journal: List[JournalEntry] = []
        self._account_balances: Dict[str, float] = {}

    def post(self, description: str, lines: List[LedgerEntryLine]) -> JournalEntry:
        if not lines:
            raise ValueError("Journal entry must contain at least two entry lines.")

        total_debit = round(sum(line.debit for line in lines), 2)
        total_credit = round(sum(line.credit for line in lines), 2)

        if total_debit != total_credit:
            raise LedgerBalanceError(
                f"Ledger out of balance! Debits: {total_debit:.2f} != Credits: {total_credit:.2f}"
            )

        entry = JournalEntry(
            entry_id=str(uuid.uuid4())[:8],
            description=description,
            timestamp=datetime.now(timezone.utc).isoformat(),
            lines=lines
        )

        for line in lines:
            curr = self._account_balances.get(line.account_id, 0.0)
            # Net balance effect: Debits increase Asset/Expense; Credits increase Liability/Equity/Revenue
            # For general balance mapping, we track net balance (Debit - Credit)
            self._account_balances[line.account_id] = round(curr + line.debit - line.credit, 2)

        self._journal.append(entry)
        return entry

    def record_loan_disbursement(self, loan_id: str, principal: float) -> JournalEntry:
        """
        Record loan origination:
        Debit:  1100 - Loans Receivable (Asset increases)
        Credit: 1010 - Operating Cash / Bank (Asset decreases)
        """
        lines = [
            LedgerEntryLine("1100", f"Loans Receivable (Loan {loan_id})", debit=principal, credit=0.0),
            LedgerEntryLine("1010", "Operating Cash Account", debit=0.0, credit=principal)
        ]
        return self.post(f"Loan Disbursement for {loan_id}", lines)

    def record_repayment(self, loan_id: str, principal_paid: float, interest_paid: float) -> JournalEntry:
        """
        Record borrower installment:
        Debit:  1010 - Operating Cash (Asset increases by total payment)
        Credit: 1100 - Loans Receivable (Asset decreases by principal portion)
        Credit: 4010 - Interest Income (Revenue increases by interest portion)
        """
        total = round(principal_paid + interest_paid, 2)
        lines = [
            LedgerEntryLine("1010", "Operating Cash Account", debit=total, credit=0.0),
            LedgerEntryLine("1100", f"Loans Receivable (Loan {loan_id})", debit=0.0, credit=principal_paid),
            LedgerEntryLine("4010", "Interest Income", debit=0.0, credit=interest_paid)
        ]
        return self.post(f"Repayment Installment for {loan_id}", lines)

    def get_account_balance(self, account_id: str) -> float:
        return self._account_balances.get(account_id, 0.0)

    @property
    def total_entries(self) -> int:
        return len(self._journal)
