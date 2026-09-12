"""
Unit tests for Workforce Matching Engine.
"""

import unittest
from src.models import (
    CandidateProfile,
    JobRequisition,
    QualificationStatus
)
from src.engine import WorkforceMatchingEngine, ScoringWeights
from src.audit import ComplianceAuditLedger


class TestWorkforceMatchingEngine(unittest.TestCase):
    def setUp(self):
        self.ledger = ComplianceAuditLedger()
        self.engine = WorkforceMatchingEngine(audit_ledger=self.ledger)

    def test_ideal_candidate_recommended(self):
        candidate = CandidateProfile(
            id="cand-001",
            name="John Developer",
            noc_code="21232",
            years_experience=6.0,
            skills=["Python", "SQL", "Docker", "RESTful APIs", "AWS"],
            clb_level=8,
            compliance_cleared=True
        )
        requisition = JobRequisition(
            id="req-101",
            title="Senior Software Engineer",
            target_noc="21232",
            min_experience_years=5.0,
            required_skills=["Python", "SQL", "RESTful APIs"],
            min_clb_level=7,
            compliance_required=True
        )

        result = self.engine.evaluate(candidate, requisition)
        self.assertEqual(result.status, QualificationStatus.RECOMMENDED)
        self.assertTrue(result.is_compliant)
        self.assertGreaterEqual(result.scores.composite_score, 90.0)
        self.assertIn("Meets and exceeds core benchmark qualifications.", result.reasons)
        self.assertTrue(len(result.audit_hash) == 64)

    def test_compliance_failure_instant_rejection(self):
        candidate = CandidateProfile(
            id="cand-002",
            name="Non Compliant Applicant",
            noc_code="21232",
            years_experience=10.0,
            skills=["Python", "SQL"],
            clb_level=9,
            compliance_cleared=False  # Regulatory clearance failed
        )
        requisition = JobRequisition(
            id="req-102",
            title="Senior Lead",
            target_noc="21232",
            min_experience_years=5.0,
            required_skills=["Python"],
            min_clb_level=7,
            compliance_required=True
        )

        result = self.engine.evaluate(candidate, requisition)
        self.assertEqual(result.status, QualificationStatus.REJECTED)
        self.assertFalse(result.is_compliant)
        self.assertEqual(result.scores.composite_score, 0.0)
        self.assertTrue(any("failed mandatory regulatory compliance" in r for r in result.reasons))

    def test_minor_noc_unit_group_partial_score(self):
        candidate = CandidateProfile(
            id="cand-003",
            name="Adjacent Field Analyst",
            noc_code="21231",  # 2123 unit group
            years_experience=5.0,
            skills=["Python", "SQL"],
            clb_level=7,
            compliance_cleared=True
        )
        requisition = JobRequisition(
            id="req-103",
            title="Software Developer",
            target_noc="21232",  # 2123 unit group
            min_experience_years=4.0,
            required_skills=["Python", "SQL"],
            min_clb_level=7
        )

        result = self.engine.evaluate(candidate, requisition)
        self.assertEqual(result.scores.noc_score, 80.0)
        self.assertIn(result.status, [QualificationStatus.RECOMMENDED, QualificationStatus.QUALIFIED_WITH_CONDITIONS])

    def test_low_experience_conditional_qualification(self):
        candidate = CandidateProfile(
            id="cand-004",
            name="Junior Dev",
            noc_code="21232",
            years_experience=2.0,
            skills=["Python", "Docker"],
            clb_level=7,
            compliance_cleared=True
        )
        requisition = JobRequisition(
            id="req-104",
            title="Mid-Level Engineer",
            target_noc="21232",
            min_experience_years=4.0,
            required_skills=["Python", "Docker", "Kubernetes"],
            min_clb_level=7
        )

        result = self.engine.evaluate(candidate, requisition)
        self.assertNotEqual(result.status, QualificationStatus.RECOMMENDED)
        self.assertIn("Insufficient experience", " ".join(result.reasons))

    def test_invalid_weights_raise_error(self):
        with self.assertRaises(ValueError):
            ScoringWeights(noc=0.5, experience=0.5, skills=0.5, language=0.5)


if __name__ == "__main__":
    unittest.main()
