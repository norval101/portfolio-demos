"""
Credit Underwriting Decision Engine evaluating DTI, credit tiers, and risk pricing.
"""

from typing import List
from .models import (
    LoanApplication,
    UnderwritingResult,
    UnderwritingDecision,
    RiskTier
)
from .amortization import AmortizationEngine


class LoanUnderwritingEngine:
    def evaluate(self, app: LoanApplication) -> UnderwritingResult:
        reasons: List[str] = []
        b = app.borrower

        # 1. Minimum Credit Score Filter
        if b.credit_score < 580:
            reasons.append(f"Credit score {b.credit_score} is below minimum underwriting cutoff (580).")
            return UnderwritingResult(
                decision=UnderwritingDecision.DECLINED,
                risk_tier=RiskTier.REJECTED,
                approved_amount=0.0,
                approved_annual_rate=0.0,
                monthly_payment=0.0,
                dti_ratio=0.0,
                reasons=reasons
            )

        # 2. Assign Risk Tier & Base Margin
        if b.credit_score >= 740:
            risk_tier = RiskTier.PRIME
            rate_spread = 0.00
        elif b.credit_score >= 670:
            risk_tier = RiskTier.NEAR_PRIME
            rate_spread = 0.025  # +2.5%
        else:
            risk_tier = RiskTier.SUBPRIME
            rate_spread = 0.055  # +5.5%

        effective_rate = round(app.requested_annual_rate + rate_spread, 4)

        # 3. Compute Preliminary Payment
        est_pmt = AmortizationEngine.calculate_pmt(
            app.requested_amount,
            effective_rate,
            app.term_months
        )

        # 4. Debt-to-Income (DTI) Analysis
        total_monthly_debt = b.monthly_debt_obligations + est_pmt
        if b.gross_monthly_income <= 0:
            dti = 100.0
        else:
            dti = round((total_monthly_debt / b.gross_monthly_income) * 100.0, 2)

        if dti > 50.0:
            reasons.append(f"Excessive Debt-to-Income ratio ({dti}% exceeds 50.0% hard cap).")
            return UnderwritingResult(
                decision=UnderwritingDecision.DECLINED,
                risk_tier=RiskTier.REJECTED,
                approved_amount=0.0,
                approved_annual_rate=effective_rate,
                monthly_payment=est_pmt,
                dti_ratio=dti,
                reasons=reasons
            )

        if dti > 42.0:
            decision = UnderwritingDecision.CONDITIONAL
            reasons.append(f"Elevated DTI ({dti}%): Requires proof of secondary liquid reserves or co-signer.")
        else:
            decision = UnderwritingDecision.APPROVED
            reasons.append("Underwriting parameters within standard credit policy bounds.")

        # 5. Employment Tenure Verification
        if b.employment_tenure_months < 6:
            decision = UnderwritingDecision.CONDITIONAL
            reasons.append(f"Employment tenure ({b.employment_tenure_months}m) < 6 months probationary minimum.")

        return UnderwritingResult(
            decision=decision,
            risk_tier=risk_tier,
            approved_amount=app.requested_amount,
            approved_annual_rate=effective_rate,
            monthly_payment=est_pmt,
            dti_ratio=dti,
            reasons=reasons
        )
