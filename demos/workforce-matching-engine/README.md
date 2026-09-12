# Workforce Matching Engine & Compliance Audit Sandbox

**Author:** Norval Mendez (Lead Systems Architect & Senior Software Developer)  
**Context:** Reference sandbox architecture based on enterprise workforce matching pipelines (LMIAPro / WATSOF architecture).

---

## 🎯 Purpose & Scope

This sandbox provides a functional, production-ready reference implementation of a **Two-Sided Workforce Matching & Compliance Engine**. It demonstrates:

1. **Clean Domain Modeling & Separation of Concerns** (Domain Models, Service Layer, Audit Ledger, and API Presentation).
2. **Deterministic Weighted Scoring Algorithm** (evaluating NOC alignment, experience curves, skills overlap, and language benchmarks).
3. **Hard Regulatory Compliance Gating** (automatic disqualification on regulatory or visa compliance failures).
4. **Tamper-Evident Audit Logging** (SHA-256 cryptographic chaining of decision records for regulatory audits).
5. **Zero External Runtime Dependencies** (written with clean modern Python standard library; runnable anywhere with zero `pip install` friction).

---

## 📐 Scoring Formula

The matching engine computes a composite score $S \in [0, 100]$:

$$S = w_{noc} \cdot S_{noc} + w_{exp} \cdot S_{exp} + w_{skills} \cdot S_{skills} + w_{lang} \cdot S_{lang}$$

Default weights:
- **NOC / Title Alignment ($w_{noc} = 0.35$):** Full match = 100, Major group match = 60, Misaligned = 0.
- **Experience Curve ($w_{exp} = 0.25$):** Scaled asymptotically based on candidate years vs. required years.
- **Skills & Certifications ($w_{skills} = 0.25$):** Jaccard set similarity across required and preferred skill tags.
- **Language Benchmarks ($w_{lang} = 0.15$):** Canadian Language Benchmark (CLB) comparison.

### Qualification Thresholds:
- **`RECOMMENDED`**: Score $\ge 80\%$ and all compliance gates passed.
- **`QUALIFIED_WITH_CONDITIONS`**: $60\% \le \text{Score} < 80\%$ and all compliance gates passed.
- **`REJECTED`**: Score $< 60\%$ or failure of any mandatory compliance gate.

---

## 🚀 Running the Sandbox & Tests

### 1. Run Unit Tests (100% Pass Rate)
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### 2. Start the REST API Service
```bash
python -m src.api
# Server listens on http://localhost:8080
```

### 3. Sample Health Check Request
```bash
curl http://localhost:8080/health
```

### 4. Sample Candidate Evaluation Request
```bash
curl -X POST http://localhost:8080/api/v1/match \
  -H "Content-Type: application/json" \
  -d '{
    "candidate": {
      "id": "cand-001",
      "name": "Alex Mercer",
      "noc_code": "21232",
      "years_experience": 5.5,
      "skills": ["Python", "Docker", "AWS", "MySQL", "REST APIs"],
      "clb_level": 8,
      "compliance_cleared": true
    },
    "requisition": {
      "id": "req-900",
      "title": "Software Systems Engineer",
      "target_noc": "21232",
      "min_experience_years": 4.0,
      "required_skills": ["Python", "REST APIs", "SQL"],
      "min_clb_level": 7,
      "compliance_required": true
    }
  }'
```

---

## 🏛️ Architecture & OpenAPI Specification
- An OpenAPI 3.0 specification is available at `openapi.yaml`.
- All decisions produce an immutable `AuditRecord` with a unique hash preventing post-hoc alterations of vetting records.
