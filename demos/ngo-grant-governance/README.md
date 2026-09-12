# Philanthropic Grant Governance & Milestone Disbursement Sandbox

**Author:** Norval Mendez (Lead Systems Architect & Senior Software Developer)  
**Context:** Reference cross-border civil society & grant governance architecture modeled from regional philanthropic coalition platforms (`cariphil` architecture).

---

## 🎯 Architecture Overview

Managing international non-profit grants requires rigorous governance, role-segregated committee approvals, and tranche-based capital releases tied to verified social impact milestones.

This sandbox demonstrates the architectural principles behind `cariphil`:

1. **Multi-Party Grant Lifecycle**:
   - Donors pledge capital to specific program funds (e.g., Caribbean climate resilience, youth education).
   - Non-profits and community organizations submit milestone-based project proposals.
2. **Milestone Vetting & Tranche Disbursement**:
   - Capital is locked in escrow and only disbursed when field evidence / impact reports are submitted and formally approved by authorized committee members.
3. **Anti-Diversion Invariants**:
   - Prevents over-disbursement beyond authorized tranche limits.
   - Enforces sequential milestone satisfaction.
4. **Zero External Runtime Dependencies**:
   - Pure Python standard library with complete unit test suite.

---

## 🚀 Running the Tests
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```
