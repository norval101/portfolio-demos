"""
Unit tests for Double-Entry Accounting Ledger.
"""

import unittest
from src.ledger import DoubleEntryLedger, LedgerBalanceError
from src.models import LedgerEntryLine


class TestDoubleEntryLedger(unittest.TestCase):
    def setUp(self):
        self.ledger = DoubleEntryLedger()

    def test_balanced_entry_succeeds(self):
        lines = [
            LedgerEntryLine("1010", "Cash", debit=1000.0, credit=0.0),
            LedgerEntryLine("3010", "Capital", debit=0.0, credit=1000.0)
        ]
        entry = self.ledger.post("Initial Capital Contribution", lines)
        self.assertIsNotNone(entry.entry_id)
        self.assertEqual(self.ledger.total_entries, 1)
        self.assertEqual(self.ledger.get_account_balance("1010"), 1000.0)
        self.assertEqual(self.ledger.get_account_balance("3010"), -1000.0)

    def test_unbalanced_entry_raises_ledger_balance_error(self):
        lines = [
            LedgerEntryLine("1010", "Cash", debit=1000.0, credit=0.0),
            LedgerEntryLine("3010", "Capital", debit=0.0, credit=999.00)  # Off by $1.00
        ]
        with self.assertRaises(LedgerBalanceError):
            self.ledger.post("Unbalanced Attempt", lines)

    def test_loan_disbursement_and_repayment_cycle(self):
        # 1. Originate loan of $5,000
        self.ledger.record_loan_disbursement("LN-001", 5000.0)
        self.assertEqual(self.ledger.get_account_balance("1100"), 5000.0)  # Loans Receivable
        self.assertEqual(self.ledger.get_account_balance("1010"), -5000.0) # Cash outflow

        # 2. Record borrower payment of $500 ($450 principal + $50 interest)
        self.ledger.record_repayment("LN-001", principal_paid=450.0, interest_paid=50.0)

        # Loans Receivable decreases to $4,550
        self.assertEqual(self.ledger.get_account_balance("1100"), 4550.0)
        # Cash net is now -5000 + 500 = -4500
        self.assertEqual(self.ledger.get_account_balance("1010"), -4500.0)
        # Interest income credited by 50
        self.assertEqual(self.ledger.get_account_balance("4010"), -50.0)


if __name__ == "__main__":
    unittest.main()
