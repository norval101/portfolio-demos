"""
Unit tests for Compliance Audit Ledger.
"""

import unittest
from src.audit import ComplianceAuditLedger, AuditEntry


class TestComplianceAuditLedger(unittest.TestCase):
    def setUp(self):
        self.ledger = ComplianceAuditLedger()

    def test_genesis_block_creation(self):
        self.assertEqual(self.ledger.length, 1)
        genesis = self.ledger.get_entry_by_index(0)
        self.assertIsNotNone(genesis)
        self.assertEqual(genesis.index, 0)
        self.assertEqual(genesis.status, "GENESIS")
        self.assertTrue(self.ledger.verify_integrity())

    def test_record_multiple_decisions_and_verify_chain(self):
        entry1 = self.ledger.record_decision(
            candidate_id="cand-1",
            requisition_id="req-1",
            status="RECOMMENDED",
            composite_score=88.5,
            payload_snapshot={"notes": "All checks passed"}
        )
        self.assertEqual(entry1.index, 1)

        entry2 = self.ledger.record_decision(
            candidate_id="cand-2",
            requisition_id="req-1",
            status="REJECTED",
            composite_score=42.0,
            payload_snapshot={"notes": "Low experience"}
        )
        self.assertEqual(entry2.index, 2)
        self.assertEqual(self.ledger.length, 3)

        self.assertTrue(self.ledger.verify_integrity())

    def test_tamper_detection(self):
        self.ledger.record_decision("c1", "r1", "RECOMMENDED", 90.0)
        self.ledger.record_decision("c2", "r1", "REJECTED", 30.0)

        # Integrity passes initially
        self.assertTrue(self.ledger.verify_integrity())

        # Simulate tampering with a historical record
        entry = self.ledger.get_entry_by_index(1)
        entry.composite_score = 99.9  # Unauthorized modification!

        # Integrity verification must catch this tamper
        self.assertFalse(self.ledger.verify_integrity())


if __name__ == "__main__":
    unittest.main()
