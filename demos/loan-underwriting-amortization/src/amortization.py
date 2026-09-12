"""
Precision Amortization Engine using actuarial PMT formulation.
"""

from typing import List
from .models import AmortizationScheduleRow


class AmortizationEngine:
    @staticmethod
    def calculate_pmt(principal: float, annual_rate: float, term_months: int) -> float:
        if principal <= 0 or term_months <= 0:
            return 0.0

        if annual_rate == 0:
            return round(principal / term_months, 2)

        monthly_rate = annual_rate / 12.0
        # PMT formula: P * (r * (1 + r)^n) / ((1 + r)^n - 1)
        factor = (1.0 + monthly_rate) ** term_months
        pmt = principal * (monthly_rate * factor) / (factor - 1.0)
        return round(pmt, 2)

    @classmethod
    def generate_schedule(
        cls,
        principal: float,
        annual_rate: float,
        term_months: int
    ) -> List[AmortizationScheduleRow]:
        if principal <= 0 or term_months <= 0:
            return []

        monthly_rate = annual_rate / 12.0
        pmt = cls.calculate_pmt(principal, annual_rate, term_months)
        schedule: List[AmortizationScheduleRow] = []

        balance = float(principal)

        for period in range(1, term_months + 1):
            interest = round(balance * monthly_rate, 2)

            if period == term_months:
                # Final installment resolves any residual fractional penny rounding
                principal_portion = round(balance, 2)
                payment = round(principal_portion + interest, 2)
                balance = 0.0
            else:
                principal_portion = round(pmt - interest, 2)
                # Safeguard against negative principal if interest exceeds PMT (edge case)
                principal_portion = min(principal_portion, balance)
                balance = round(balance - principal_portion, 2)
                payment = pmt

            schedule.append(AmortizationScheduleRow(
                period=period,
                payment_amount=payment,
                principal_portion=principal_portion,
                interest_portion=interest,
                remaining_balance=max(0.0, balance)
            ))

        return schedule
