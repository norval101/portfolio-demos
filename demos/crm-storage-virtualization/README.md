# CRM Virtual Storage & Cloud Object Proxy Sandbox

**Author:** Norval Mendez (Lead Systems Architect & Senior Software Developer)  
**Context:** Reference enterprise storage virtualization architecture modeled from high-scale CRM asset management systems (`client-crm` architecture).

---

## 🎯 Architecture Overview

In multi-tenant CRM platforms, transitioning from local disk storage to cloud object storage (e.g., AWS S3) across legacy controllers (46+ endpoints handling invoices, estimates, receipts, customer contracts) presents major risks of regression and downtime.

This sandbox demonstrates the architectural solution implemented in `client-crm`:

1. **Storage Driver Abstraction Layer**:
   - Decouples client controllers from underlying filesystem mechanics via a unified `VirtualStorageManager`.
   - Supports pluggable backends: `LocalStorageDriver` and `CloudS3StorageDriver`.
2. **Transparent Read / Fallback Mechanism**:
   - Attempts reads from Cloud S3; if an asset hasn't yet migrated, seamlessly falls back to local disk without throwing 404 errors.
3. **Zero-Downtime Migration Engine**:
   - Batches local files, transfers them to the cloud object store, verifies cryptographic SHA-256 checksums, and updates metadata pointers.
4. **Zero External Runtime Dependencies**:
   - Pure Python standard library with complete unit test suite.

---

## 🚀 Running the Tests
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```
