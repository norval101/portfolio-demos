# PropTech Association Compliance & Multi-Touch Lead Attribution Sandbox

**Author:** Norval Mendez (Lead Systems Architect & Senior Software Developer)  
**Context:** Reference PropTech and real estate operating system architecture modeled from association compliance hubs and performance lead funnels (`propOSFlow` and `realtor-lead` architecture).

---

## 🎯 Architecture Overview

This sandbox implements the core regulatory and marketing engines of a modern real estate operating system:

1. **Role-Based Tenant & Member Governance (`propOSFlow`)**:
   - Hierarchical access boundaries: `PLATFORM_ADMIN`, `ASSOCIATION_ADMIN` (RAJ), `BROKER_ADMIN`, and `REALTOR_MEMBER`.
   - Automated regulatory compliance gating: verifies active broker licenses, mandatory Continuing Professional Development (CPD) hours, and ethical clearance before permitting transaction access.
2. **Multi-Touch Marketing Lead Attribution Engine (`realtor-lead`)**:
   - Ingests cross-channel campaign touchpoints (Google Ads, Meta Pixel, LinkedIn Insight Tag, TikTok).
   - Computes multi-touch attribution credit using deterministic linear weighting and time-decay models.
3. **Geographic & Specialty Lead Routing**:
   - Dispatches validated buyer/seller leads exclusively to actively compliant realtors registered within target geographic territories.
4. **Zero External Runtime Dependencies**:
   - Pure Python standard library with complete unit test suite.

---

## 🚀 Running the Tests
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```
