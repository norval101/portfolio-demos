"""
Unit tests for Document Audit Pipeline.
"""

import unittest
from datetime import date
from src.models import DocumentPayload, AnomalySeverity, AuditVerdict
from src.validator import DocumentAuditPipeline


class TestDocumentAuditPipeline(unittest.TestCase):
    def setUp(self):
        # Anchor reference date to 2026-09-01 for deterministic evaluations
        self.ref_date = date(2026, 9, 1)
        self.pipeline = DocumentAuditPipeline(reference_date=self.ref_date)
        self.valid_sha = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

    def test_valid_passport_passes(self):
        doc = DocumentPayload(
            document_id="doc-100",
            candidate_id="cand-001",
            document_type="PASSPORT",
            candidate_legal_name="Norval Kemo Mendez",
            extracted_name="Norval Kemo Mendez",
            issue_date="2024-01-15",
            expiry_date="2029-01-15",
            issuing_country="CAN",
            file_sha256=self.valid_sha
        )

        report = self.pipeline.audit(doc)
        self.assertEqual(report.verdict, AuditVerdict.PASSED)
        self.assertEqual(report.risk_score, 0.0)
        self.assertEqual(len(report.anomalies), 0)

    def test_expired_document_rejected(self):
        doc = DocumentPayload(
            document_id="doc-101",
            candidate_id="cand-002",
            document_type="PASSPORT",
            candidate_legal_name="John Doe",
            extracted_name="John Doe",
            issue_date="2015-01-01",
            expiry_date="2025-01-01",  # Expired relative to 2026-09-01
            issuing_country="USA",
            file_sha256=self.valid_sha
        )

        report = self.pipeline.audit(doc)
        self.assertEqual(report.verdict, AuditVerdict.REJECTED)
        self.assertGreaterEqual(report.risk_score, 90.0)
        self.assertTrue(any(a.code == "ERR_DOCUMENT_EXPIRED" for a in report.anomalies))

    def test_passport_validity_under_6_months_warning(self):
        # Expiry is 60 days from ref_date (less than 180 days)
        doc = DocumentPayload(
            document_id="doc-102",
            candidate_id="cand-003",
            document_type="PASSPORT",
            candidate_legal_name="Jane Smith",
            extracted_name="Jane Smith",
            issue_date="2020-01-01",
            expiry_date="2026-10-30",
            issuing_country="CAN",
            file_sha256=self.valid_sha
        )

        report = self.pipeline.audit(doc)
        self.assertEqual(report.verdict, AuditVerdict.NEEDS_REVIEW)
        self.assertTrue(any(a.code == "WARN_PASSPORT_EXPIRING_SOON" for a in report.anomalies))

    def test_name_mismatch_blocks(self):
        doc = DocumentPayload(
            document_id="doc-103",
            candidate_id="cand-004",
            document_type="PASSPORT",
            candidate_legal_name="Robert Michael Vance",
            extracted_name="Carlos Eduardo Sanchez",
            issue_date="2024-01-01",
            expiry_date="2029-01-01",
            issuing_country="CAN",
            file_sha256=self.valid_sha
        )

        report = self.pipeline.audit(doc)
        self.assertEqual(report.verdict, AuditVerdict.REJECTED)
        self.assertTrue(any(a.code == "ERR_NAME_MISMATCH" for a in report.anomalies))

    def test_stale_police_record_blocked(self):
        # Issued 250 days prior to ref_date (exceeds 180 day validity)
        doc = DocumentPayload(
            document_id="doc-104",
            candidate_id="cand-005",
            document_type="POLICE_RECORD",
            candidate_legal_name="Sarah Connor",
            extracted_name="Sarah Connor",
            issue_date="2025-12-01",
            expiry_date="2027-12-01",
            issuing_country="JAM",
            file_sha256=self.valid_sha
        )

        report = self.pipeline.audit(doc)
        self.assertEqual(report.verdict, AuditVerdict.REJECTED)
        self.assertTrue(any(a.code == "ERR_POLICE_RECORD_STALE" for a in report.anomalies))


if __name__ == "__main__":
    unittest.main()
