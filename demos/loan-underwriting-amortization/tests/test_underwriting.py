"""
Unit tests for Loan Underwriting Engine.
"""

import unittest
from src.models import (
    BorrowerFinancials,
    LoanApplication,
    UnderwritingDecision,
    RiskTier
)
from src.underwriting import LoanUnderwritingEngine


class TestLoanUnderwritingEngine(unittest.TestCase):
    def setUp(self):
        self.engine = LoanUnderwritingEngine()

    def test_prime_borrower_approved(self):
        borrower = BorrowerFinancials(
            borrower_id="b-100",
            legal_name="Alice Smith",
            credit_score=780,
            gross_monthly_income=9500.0,
            monthly_debt_obligations=1200.0,
            employment_tenure_months=36
        )
        app = LoanApplication(
            application_id="app-1",
            borrower=borrower,
            requested_amount=20000.0,
            term_months=36,
            requested_annual_rate=0.065
        )

        result = self.engine.evaluate(app)
        self.assertEqual(result.decision, UnderwritingDecision.APPROVED)
        self.assertEqual(result.risk_tier, RiskTier.PRIME)
        self.assertEqual(result.approved_annual_rate, 0.065)  # 0% spread
        self.assertLess(result.dti_ratio, 30.0)

    def test_low_credit_score_declined(self):
        borrower = BorrowerFinancials(
            borrower_id="b-101",
            legal_name="Bob LowScore",
            credit_score=520,  # Below 580 minimum
            gross_monthly_income=5000.0,
            monthly_debt_obligations=500.0,
            employment_tenure_months=24
        )
        app = LoanApplication(
            application_id="app-2",
            borrower=borrower,
            requested_amount=5000.0,
            term_months=12,
            requested_annual_rate=0.08
        )

        result = self.engine.evaluate(app)
        self.assertEqual(result.decision, UnderwritingDecision.DECLINED)
        self.assertEqual(result.risk_tier, RiskTier.REJECTED)
        self.assertTrue(any("below minimum underwriting cutoff" in r for r in result.reasons))

    def test_excessive_dti_declined(self):
        borrower = BorrowerFinancials(
            borrower_id="b-102",
            legal_name="Charlie Overleveraged",
            credit_score=710,
            gross_monthly_income=4000.0,
            monthly_debt_obligations=2200.0,  # High prior debt
            employment_tenure_months=48
        )
        app = LoanApplication(
            application_id="app-3",
            borrower=borrower,
            requested_amount=30000.0,  # Generates high PMT pushing DTI > 50%
            term_months=24,
            requested_annual_rate=0.075
        )

        result = self.engine.evaluate(app)
        self.assertEqual(result.decision, UnderwritingDecision.DECLINED)
        self.assertGreater(result.dti_ratio, 50.0)


if __name__ == "__main__":
    unittest.main()
