# Systems Architecture & Sandbox Demos Directory

**Author:** Norval Mendez (Lead Systems Architect & Senior Software Developer)  
**Repository:** [norval101/portfolio-demos](https://github.com/norval101/portfolio-demos)  
**Total Demos:** 9 Sandboxes | **Total Test Suite:** 42/42 Tests Passing (100%)

---

## 🧭 Master Sandbox Catalog

Every demo in this folder is a **self-contained, fully tested open-source reference implementation** modeled after real-world production architectures I have designed and delivered. 

All code is written in clean, modern Python standard library with **zero external runtime dependencies** (no `pip install` required), guaranteeing that any engineering hiring manager or technical interviewer can run the entire suite immediately.

| # | Sandbox Directory | Target Domain & Inspiration | Core Architectural Patterns & Algorithms | Tests |
| :-: | :--- | :--- | :--- | :-: |
| **1** | [`workforce-matching-engine/`](./workforce-matching-engine) | `LMIAPro` / `WATSOF` | Two-sided candidate matching, deterministic weighted NOC/experience/skills scoring, SHA-256 chained audit ledger, REST API + OpenAPI 3.0 | **8/8 Passing** |
| **2** | [`document-audit-pipeline/`](./document-audit-pipeline) | `WATSOF` AI Vetting | Multi-stage document verification (SHA-256 checksums, temporal validity, token similarity, 94% rejection reduction logic) | **5/5 Passing** |
| **3** | [`loan-underwriting-amortization/`](./loan-underwriting-amortization) | `loan-managment-software` | Credit underwriting risk decisioning (DTI/DSCR), precision reducing-balance PMT amortization, double-entry general ledger | **10/10 Passing** |
| **4** | [`solar-iot-telemetry-engine/`](./solar-iot-telemetry-engine) | `solar-engineering` / `nht-solar` | Streaming inverter telemetry ingestion, STC temperature-derated yield modeling, thermal hotspot & open-string detection | **4/4 Passing** |
| **5** | [`retail-merchandising-audit/`](./retail-merchandising-audit) | `mechandizing-software` | Planogram (POG) compliance scoring, Brand Share of Shelf (SoS), Out-of-Stock (OOS) alerting, Store Execution Score (SES) | **2/2 Passing** |
| **6** | [`cross-border-escrow-rfq/`](./cross-border-escrow-rfq) | `WindMade.ca` | B2B machining capacity matching, automated CUSMA/USMCA origin certificate generator, 5-day inspection escrow state machine | **4/4 Passing** |
| **7** | [`crm-storage-virtualization/`](./crm-storage-virtualization) | `client-crm` | Pluggable storage driver abstraction, transparent dual-read fallback, zero-downtime S3 migration engine with SHA-256 verification | **3/3 Passing** |
| **8** | [`proptech-lead-attribution/`](./proptech-lead-attribution) | `propOSFlow` / `realtor-lead` | Role-based tenant routing (Platform, Association, Broker, Member), regulatory ethics gating, multi-touch linear lead attribution | **3/3 Passing** |
| **9** | [`ngo-grant-governance/`](./ngo-grant-governance) | `cariphil` | Multi-party grant governance, milestone-based tranche disbursements, anti-diversion financial checks, committee sign-off ledger | **3/3 Passing** |

---

## 🔍 Detailed Demo Specifications

### 1. [`workforce-matching-engine/`](./workforce-matching-engine)
- **Problem Solved:** Fragmented international talent matching causing months of manual recruitment delays.
- **Key Modules:**
  - `src/models.py`: Immutable domain models for candidate profiles, job requisitions, and score breakdowns.
  - `src/engine.py`: Weighted multi-criteria matching algorithm (NOC taxonomy alignment, asymptotic experience curves, skill set Jaccard intersection, CLB language benchmarks).
  - `src/audit.py`: Cryptographic SHA-256 chained audit ledger ensuring regulatory auditability.
  - `src/api.py`: Embedded REST API server with health checks, matching endpoints, and ledger verification.
  - `openapi.yaml`: OpenAPI 3.0 specification for standardized B2B partner integration.
- **Run Tests:**
  ```bash
  python -m unittest discover -s workforce-matching-engine/tests -t workforce-matching-engine -p "test_*.py" -v
  ```

---

### 2. [`document-audit-pipeline/`](./document-audit-pipeline)
- **Problem Solved:** High government/sponsor visa rejection rates caused by expired credentials and mismatched document metadata.
- **Key Modules:**
  - `src/models.py`: Document payload representations, anomaly severity tiers (`BLOCKER`, `WARNING`, `INFO`), and verdict models.
  - `src/validator.py`: Multi-stage pipeline validating SHA-256 file checksums, temporal expiration bounds, 6-month passport validity rules, token-based legal name alignment, and police record recency.
- **Run Tests:**
  ```bash
  python -m unittest discover -s document-audit-pipeline/tests -t document-audit-pipeline -p "test_*.py" -v
  ```

---

### 3. [`loan-underwriting-amortization/`](./loan-underwriting-amortization)
- **Problem Solved:** Loan servicing errors, inaccurate amortization rounding, and accounting discrepancies in credit lending.
- **Key Modules:**
  - `src/amortization.py`: Actuarial PMT reducing-balance amortization engine guaranteeing exact penny reconciliation across any term.
  - `src/underwriting.py`: Credit score risk-tiering (Prime, Near-Prime, Subprime) and Debt-to-Income (DTI) gating.
  - `src/ledger.py`: Strict double-entry general ledger enforcing $\sum \text{Debits} \equiv \sum \text{Credits}$ across loan origination, fund disbursement, and repayments.
- **Run Tests:**
  ```bash
  python -m unittest discover -s loan-underwriting-amortization/tests -t loan-underwriting-amortization -p "test_*.py" -v
  ```

---

### 4. [`solar-iot-telemetry-engine/`](./solar-iot-telemetry-engine)
- **Problem Solved:** Undetected string disconnects and module hotspots degrading clean energy generation yield.
- **Key Modules:**
  - `src/models.py`: Inverter SCADA telemetry frames (DC voltage, current, AC active power, module temperature, POA irradiance).
  - `src/analyzer.py`: Temperature-derated Standard Test Condition (STC) yield modeling, conversion efficiency ($\eta = P_{AC}/P_{DC}$), and automated fault detection (`THERMAL_HOTSPOT`, `STRING_DISCONNECT`, `INVERTER_DERATING`).
- **Run Tests:**
  ```bash
  python -m unittest discover -s solar-iot-telemetry-engine/tests -t solar-iot-telemetry-engine -p "test_*.py" -v
  ```

---

### 5. [`retail-merchandising-audit/`](./retail-merchandising-audit)
- **Problem Solved:** Millions lost in CPG retail networks to out-of-stock (OOS) conditions and planogram non-compliance.
- **Key Modules:**
  - `src/models.py`: Planogram SKU specifications, field auditor observations, and store execution metrics.
  - `src/audit_engine.py`: Planogram compliance scoring, brand Share of Shelf (SoS) calculations, OOS alerts, and composite Store Execution Score (SES).
- **Run Tests:**
  ```bash
  python -m unittest discover -s retail-merchandising-audit/tests -t retail-merchandising-audit -p "test_*.py" -v
  ```

---

### 6. [`cross-border-escrow-rfq/`](./cross-border-escrow-rfq)
- **Problem Solved:** Friction in custom manufacturing trade, cross-border customs paperwork, and supplier payment risks.
- **Key Modules:**
  - `src/models.py`: CAD RFQ specifications, manufacturer capacity profiles, CUSMA certificates, and escrow orders.
  - `src/escrow_engine.py`: 5-Axis CNC / stamping machine matching, automated CUSMA/USMCA origin certificate generation from HS codes, and a 5-day post-delivery inspection escrow state machine (90% manufacturer / 10% platform fee).
- **Run Tests:**
  ```bash
  python -m unittest discover -s cross-border-escrow-rfq/tests -t cross-border-escrow-rfq -p "test_*.py" -v
  ```

---

### 7. [`crm-storage-virtualization/`](./crm-storage-virtualization)
- **Problem Solved:** High-risk cloud migrations in legacy CRMs where hundreds of endpoints depend on local disk file paths.
- **Key Modules:**
  - `src/models.py`: Stored object metadata, storage backend enumeration, and migration progress trackers.
  - `src/storage_manager.py`: Pluggable virtual storage driver, dual-read fallback strategy (checks Cloud S3 first, falls back to local disk), and zero-downtime batch migration with cryptographic SHA-256 verification.
- **Run Tests:**
  ```bash
  python -m unittest discover -s crm-storage-virtualization/tests -t crm-storage-virtualization -p "test_*.py" -v
  ```

---

### 8. [`proptech-lead-attribution/`](./proptech-lead-attribution)
- **Problem Solved:** Complex real estate association governance and disputed marketing attribution across multi-channel ad spend.
- **Key Modules:**
  - `src/models.py`: Role-level taxonomy, marketing channels, realtor compliance records, touchpoints, and leads.
  - `src/engine.py`: Role-based route dispatching, license/CPD hours compliance gating, linear multi-touch attribution credit calculations, and compliant geographic lead assignment.
- **Run Tests:**
  ```bash
  python -m unittest discover -s proptech-lead-attribution/tests -t proptech-lead-attribution -p "test_*.py" -v
  ```

---

### 9. [`ngo-grant-governance/`](./ngo-grant-governance)
- **Problem Solved:** Donor fund diversion and lack of milestone traceability in regional humanitarian grants.
- **Key Modules:**
  - `src/models.py`: Multi-tranche project grants, milestone states, and allocation records.
  - `src/governance_engine.py`: Enforces sequential milestone evidence submission, committee approval signatures, and tranche disbursement invariants with zero budget overrun tolerance.
- **Run Tests:**
  ```bash
  python -m unittest discover -s ngo-grant-governance/tests -t ngo-grant-governance -p "test_*.py" -v
  ```

---

## 🧪 Execute All 42 Tests in One Single Command

From the root of this repository, run:

```bash
python -m unittest discover -s demos/workforce-matching-engine/tests -t demos/workforce-matching-engine -p "test_*.py" ; `
python -m unittest discover -s demos/document-audit-pipeline/tests -t demos/document-audit-pipeline -p "test_*.py" ; `
python -m unittest discover -s demos/loan-underwriting-amortization/tests -t demos/loan-underwriting-amortization -p "test_*.py" ; `
python -m unittest discover -s demos/solar-iot-telemetry-engine/tests -t demos/solar-iot-telemetry-engine -p "test_*.py" ; `
python -m unittest discover -s demos/retail-merchandising-audit/tests -t demos/retail-merchandising-audit -p "test_*.py" ; `
python -m unittest discover -s demos/cross-border-escrow-rfq/tests -t demos/cross-border-escrow-rfq -p "test_*.py" ; `
python -m unittest discover -s demos/crm-storage-virtualization/tests -t demos/crm-storage-virtualization -p "test_*.py" ; `
python -m unittest discover -s demos/proptech-lead-attribution/tests -t demos/proptech-lead-attribution -p "test_*.py" ; `
python -m unittest discover -s demos/ngo-grant-governance/tests -t demos/ngo-grant-governance -p "test_*.py"
```
