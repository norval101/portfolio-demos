"""
Unit tests for Precision Amortization Engine.
"""

import unittest
from src.amortization import AmortizationEngine


class TestAmortizationEngine(unittest.TestCase):
    def test_pmt_calculation_standard_loan(self):
        # $10,000 at 6.0% annual interest over 12 months
        pmt = AmortizationEngine.calculate_pmt(10000.0, 0.06, 12)
        # Expected formula PMT: ~ $860.66
        self.assertAlmostEqual(pmt, 860.66, places=2)

    def test_zero_interest_loan(self):
        pmt = AmortizationEngine.calculate_pmt(1200.0, 0.0, 12)
        self.assertEqual(pmt, 100.0)

    def test_schedule_sums_to_exact_principal(self):
        principal = 25000.0
        term_months = 36
        rate = 0.075

        schedule = AmortizationEngine.generate_schedule(principal, rate, term_months)
        self.assertEqual(len(schedule), term_months)

        total_principal_paid = sum(row.principal_portion for row in schedule)
        self.assertAlmostEqual(total_principal_paid, principal, places=2)

        # Final remaining balance must be zero
        self.assertEqual(schedule[-1].remaining_balance, 0.0)

    def test_interest_declines_monotonically(self):
        schedule = AmortizationEngine.generate_schedule(15000.0, 0.09, 24)
        for i in range(1, len(schedule)):
            self.assertLessEqual(schedule[i].interest_portion, schedule[i - 1].interest_portion)


if __name__ == "__main__":
    unittest.main()
