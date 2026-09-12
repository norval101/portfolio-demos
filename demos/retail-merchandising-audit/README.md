# Retail Merchandising, Planogram & Store Execution Audit Sandbox

**Author:** Norval Mendez (Lead Systems Architect & Senior Software Developer)  
**Context:** Reference retail audit and field merchandising sandbox architecture modeled from retail operations and POS compliance platforms (`mechandizing-software` architecture).

---

## 🎯 Architecture Overview

This sandbox implements the core analytical engine used by field merchandisers, brand managers, and retail auditors to score store execution quality:

1. **Planogram (POG) Compliance Engine**:
   - Compares expected shelf layout blueprints against audited SKU facing counts.
   - Computes facing accuracy and sequence alignment.
2. **Share of Shelf (SoS) Analytics**:
   - Calculates brand shelf dominance against category competitors:
     $$\text{Share of Shelf} = \frac{\text{Target Brand Facings}}{\text{Total Category Facings}} \times 100\%$$
3. **Out-of-Stock (OOS) Alerting**:
   - Identifies missing high-velocity SKUs and flags immediate replenishment triggers.
4. **Composite Store Execution Score (SES)**:
   - Evaluates overall retail presentation using standard CPG industry metrics:
     $$SES = 0.30 \cdot POG + 0.30 \cdot \text{Availability} + 0.20 \cdot \text{POS Promo Visibility} + 0.20 \cdot \text{Facing Quality}$$
5. **Zero External Runtime Dependencies**:
   - Pure Python standard library with complete unit test suite.

---

## 🚀 Running the Tests
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```
