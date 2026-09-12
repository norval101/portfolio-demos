# Cross-Border Manufacturing RFQ & Escrow State Machine Sandbox

**Author:** Norval Mendez (Lead Systems Architect & Senior Software Developer)  
**Context:** Reference B2B industrial marketplace sandbox architecture modeled from precision manufacturing and cross-border trade systems (`WindMade.ca` architecture).

---

## 🎯 Architecture Overview

This sandbox implements the core transaction pipeline for cross-border manufacturing between Canadian CNC/tooling shops and US industrial buyers:

1. **Machining Capacity Matching Engine**:
   - Matches buyer CAD RFQs against supplier machine profiles (e.g., 5-Axis CNC, Precision Stamping, EDM, Lathe Turning).
2. **Automated CUSMA / USMCA Certificate of Origin Generator**:
   - Classifies Harmonized System (HS) tariff codes (e.g., `8482.10`, `8207.30`) to determine preferential tariff eligibility under North American trade agreements.
3. **5-Day Post-Delivery Inspection Escrow State Machine**:
   - Manages state transitions:
     `DRAFT` $\to$ `QUOTED` $\to$ `ESCROW_FUNDED` $\to$ `IN_TRANSIT` $\to$ `DELIVERED_INSPECTION` $\to$ `FUNDS_RELEASED` (or `DISPUTED`).
   - Guarantees financial split invariant: 90% manufacturer payout / 10% platform fee.
4. **Zero External Runtime Dependencies**:
   - Pure Python standard library with complete unit test suite.

---

## 🚀 Running the Tests
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```
