"""
Domain models for Loan Underwriting, Amortization, and Double-Entry Ledger.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from datetime import datetime, timezone


class RiskTier(str, Enum):
    PRIME = "PRIME"
    NEAR_PRIME = "NEAR_PRIME"
    SUBPRIME = "SUBPRIME"
    REJECTED = "REJECTED"


class UnderwritingDecision(str, Enum):
    APPROVED = "APPROVED"
    CONDITIONAL = "CONDITIONAL"
    DECLINED = "DECLINED"


class AccountType(str, Enum):
    ASSET = "ASSET"          # e.g., Cash, Loans Receivable
    LIABILITY = "LIABILITY"  # e.g., Customer Deposits, Borrowings
    EQUITY = "EQUITY"        # Capital
    REVENUE = "REVENUE"      # Interest Income, Fee Income
    EXPENSE = "EXPENSE"      # Default Provisions, Processing Costs


@dataclass(frozen=True)
class BorrowerFinancials:
    borrower_id: str
    legal_name: str
    credit_score: int
    gross_monthly_income: float
    monthly_debt_obligations: float
    employment_tenure_months: int


@dataclass(frozen=True)
class LoanApplication:
    application_id: str
    borrower: BorrowerFinancials
    requested_amount: float
    term_months: int
    requested_annual_rate: float  # e.g., 0.085 for 8.5%


@dataclass(frozen=True)
class UnderwritingResult:
    decision: UnderwritingDecision
    risk_tier: RiskTier
    approved_amount: float
    approved_annual_rate: float
    monthly_payment: float
    dti_ratio: float
    reasons: List[str]


@dataclass(frozen=True)
class AmortizationScheduleRow:
    period: int
    payment_amount: float
    principal_portion: float
    interest_portion: float
    remaining_balance: float


@dataclass(frozen=True)
class LedgerEntryLine:
    account_id: str
    account_name: str
    debit: float
    credit: float


@dataclass(frozen=True)
class JournalEntry:
    entry_id: str
    description: str
    timestamp: str
    lines: List[LedgerEntryLine]
