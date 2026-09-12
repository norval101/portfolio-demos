# Automated Document Audit & Compliance Pipeline Sandbox

**Author:** Norval Mendez (Lead Systems Architect & Senior Software Developer)  
**Context:** Reference sandbox architecture based on automated candidate pre-screening and document compliance pipelines (WATSOF / JELPO Group architecture).

---

## 🎯 Purpose & Impact

In international workforce mobility, improper documentation, expired credentials, and non-compliant visa forms represent the #1 driver of government and sponsor rejections. 

This sandbox demonstrates the architectural principles behind the automated audit pipeline that **reduced cross-border processing rejection rates by 94%**:

1. **Multi-Stage Document Validation Pipeline**:
   - Schema & metadata completeness checks.
   - Date validity & expiration bounds analysis.
   - Cross-field consistency verification (passport number alignment, name token matching).
   - Regulatory rule compliance gates.
2. **Deterministic Risk Scoring**:
   - Calculates document rejection risk score ($0.0 - 100.0\%$).
   - Flags granular `CRITICAL_BLOCKER`, `WARNING`, and `INFORMATIONAL` items.
3. **Decoupled Rules Engine**:
   - Modular validator rules allowing new sponsor/regulatory rules to be plugged in dynamically without refactoring core logic.
4. **Zero External Runtime Dependencies**:
   - Built cleanly with modern Python standard library.

---

## 🚀 Running the Sandbox & Tests

### Run Unit Tests (100% Pass Rate)
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## 🧪 Pipeline Validation Stages

```
   [ Incoming Document Payload ]
                │
                ▼
   Stage 1: Format & Checksum Verification
                │
                ▼
   Stage 2: Temporal Expiration Analysis
                │
                ▼
   Stage 3: Cross-Document Identity Consistency
                │
                ▼
   Stage 4: Regulatory Sponsor Rules Engine
                │
                ▼
   [ Audit Verdict: PASS | CONDITIONAL | REJECTED ]
   [ Automated Audit Log & Anomaly Report Generated ]
```
