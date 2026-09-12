"""
Unit tests for NGO Grant Governance and Milestone Disbursement Engine.
"""

import unittest
from src.models import (
    ProjectGrant,
    GrantMilestone,
    MilestoneStatus,
    GrantStatus
)
from src.governance_engine import (
    GrantGovernanceEngine,
    GovernanceViolationError
)


class TestGrantGovernanceEngine(unittest.TestCase):
    def setUp(self):
        m1 = GrantMilestone("M1", "Baseline Community Needs Assessment", 15000.0)
        m2 = GrantMilestone("M2", "Water Filtration Infrastructure Build", 35000.0)
        self.grant = ProjectGrant(
            grant_id="GRANT-CARIB-2026-01",
            program_name="Clean Water Resilience Initiative",
            recipient_ngo="Caribbean Alliance for Community Development",
            total_budget_usd=50000.0,
            milestones=[m1, m2]
        )

    def test_milestone_disbursement_lifecycle(self):
        # 1. Submit evidence
        GrantGovernanceEngine.submit_milestone_evidence(
            self.grant, "M1", "https://evidence.cariphil.org/reports/m1_assessment.pdf"
        )
        self.assertEqual(self.grant.milestones[0].status, MilestoneStatus.EVIDENCE_SUBMITTED)

        # 2. Approve milestone
        GrantGovernanceEngine.approve_milestone(
            self.grant, "M1", "Dr. Marcus Vance (Executive Board)"
        )
        self.assertEqual(self.grant.milestones[0].status, MilestoneStatus.APPROVED)

        # 3. Disburse tranche
        disbursed = GrantGovernanceEngine.disburse_milestone_tranche(self.grant, "M1")
        self.assertEqual(disbursed, 15000.0)
        self.assertEqual(self.grant.disbursed_total_usd, 15000.0)
        self.assertEqual(self.grant.remaining_budget_usd, 35000.0)
        self.assertEqual(self.grant.status, GrantStatus.ACTIVE)

    def test_unapproved_milestone_cannot_be_disbursed(self):
        # M2 is PENDING, attempting disbursement must throw error
        with self.assertRaises(GovernanceViolationError):
            GrantGovernanceEngine.disburse_milestone_tranche(self.grant, "M2")

    def test_full_grant_completion_status(self):
        # Process M1
        GrantGovernanceEngine.submit_milestone_evidence(self.grant, "M1", "url1")
        GrantGovernanceEngine.approve_milestone(self.grant, "M1", "Board")
        GrantGovernanceEngine.disburse_milestone_tranche(self.grant, "M1")

        # Process M2
        GrantGovernanceEngine.submit_milestone_evidence(self.grant, "M2", "url2")
        GrantGovernanceEngine.approve_milestone(self.grant, "M2", "Board")
        GrantGovernanceEngine.disburse_milestone_tranche(self.grant, "M2")

        # Entire grant should transition to COMPLETED
        self.assertEqual(self.grant.status, GrantStatus.COMPLETED)
        self.assertEqual(self.grant.remaining_budget_usd, 0.0)


if __name__ == "__main__":
    unittest.main()
