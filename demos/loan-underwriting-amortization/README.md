# Loan Underwriting, Amortization & Double-Entry Ledger Sandbox

**Author:** Norval Mendez (Lead Systems Architect & Senior Software Developer)  
**Context:** Reference FinTech sandbox architecture modeled from enterprise banking and credit lending systems (`loan-managment-software` architecture).

---

## 🎯 Architecture Overview

This sandbox implements the core mathematical and accounting engines required for commercial and consumer lending platforms:

1. **Credit Underwriting & Risk Decision Engine**:
   - Debt-to-Income (DTI) and Debt-Service Coverage Ratio (DSCR) evaluation.
   - Dynamic risk-tier scoring (Prime, Near-Prime, Subprime, Rejected).
   - Maximum loan amount calculation and risk-adjusted pricing.
2. **Precision Amortization Engine**:
   - Monthly payment calculation ($PMT$) using annuity actuarial formulas.
   - Periodic principal and interest splitting.
   - Complete amortization schedule generation with rounding invariance guarantees.
3. **Double-Entry General Ledger Engine**:
   - Strict accounting invariant: $\sum \text{Debits} \equiv \sum \text{Credits}$ for every financial transaction.
   - Automated journal entry creation for loan origination, fund disbursement, and borrower repayment distributions.
4. **Zero External Runtime Dependencies**:
   - Pure Python standard library with complete unit test coverage.

---

## 📐 Actuarial & Underwriting Formulas

### 1. Monthly Amortization Payment Formula ($PMT$)
$$PMT = P \times \frac{r(1+r)^n}{(1+r)^n - 1}$$
Where:
- $P$ = Principal loan amount
- $r$ = Periodic monthly interest rate ($\frac{\text{Annual Rate}}{12}$)
- $n$ = Total number of monthly installments

### 2. Debt-to-Income (DTI) Ratio
$$DTI = \frac{\text{Existing Monthly Debt} + PMT}{\text{Gross Monthly Income}} \times 100\%$$
- **Prime Tier:** $DTI \le 36\%$
- **Approved Tier:** $36\% < DTI \le 45\%$
- **Disqualified:** $DTI > 45\%$

---

## 🚀 Running the Tests
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```
