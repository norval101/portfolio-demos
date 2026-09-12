"""
Core Grant Governance Engine enforcing milestone approvals and tranche disbursement invariants.
"""

from datetime import datetime, timezone
from typing import Optional
from .models import (
    ProjectGrant,
    GrantMilestone,
    MilestoneStatus,
    GrantStatus
)


class GovernanceViolationError(Exception):
    """Raised when an operation violates grant disbursement or approval rules."""
    pass


class GrantGovernanceEngine:
    @staticmethod
    def submit_milestone_evidence(grant: ProjectGrant, milestone_id: str, evidence_url: str) -> None:
        milestone = GrantGovernanceEngine._find_milestone(grant, milestone_id)
        if milestone.status not in (MilestoneStatus.PENDING, MilestoneStatus.REJECTED):
            raise GovernanceViolationError(f"Cannot submit evidence for milestone in {milestone.status} status.")

        milestone.evidence_url = evidence_url
        milestone.status = MilestoneStatus.EVIDENCE_SUBMITTED

    @staticmethod
    def approve_milestone(grant: ProjectGrant, milestone_id: str, committee_officer: str) -> None:
        milestone = GrantGovernanceEngine._find_milestone(grant, milestone_id)
        if milestone.status != MilestoneStatus.EVIDENCE_SUBMITTED:
            raise GovernanceViolationError("Milestone cannot be approved without submitted field evidence.")

        milestone.approved_by = committee_officer
        milestone.status = MilestoneStatus.APPROVED

    @staticmethod
    def disburse_milestone_tranche(grant: ProjectGrant, milestone_id: str) -> float:
        if grant.status != GrantStatus.ACTIVE:
            raise GovernanceViolationError(f"Cannot disburse from grant in {grant.status} status.")

        milestone = GrantGovernanceEngine._find_milestone(grant, milestone_id)
        if milestone.status != MilestoneStatus.APPROVED:
            raise GovernanceViolationError(f"Milestone {milestone_id} is not APPROVED for disbursement.")

        amount = milestone.allocated_amount_usd
        if amount > grant.remaining_budget_usd:
            raise GovernanceViolationError("Tranche exceeds remaining grant authorized budget.")

        grant.disbursed_total_usd = round(grant.disbursed_total_usd + amount, 2)
        milestone.status = MilestoneStatus.DISBURSED
        milestone.disbursed_at = datetime.now(timezone.utc).isoformat()

        # If all milestones are disbursed, mark grant as COMPLETED
        if all(m.status == MilestoneStatus.DISBURSED for m in grant.milestones):
            grant.status = GrantStatus.COMPLETED

        return amount

    @staticmethod
    def _find_milestone(grant: ProjectGrant, milestone_id: str) -> GrantMilestone:
        for m in grant.milestones:
            if m.milestone_id == milestone_id:
                return m
        raise ValueError(f"Milestone {milestone_id} not found in grant {grant.grant_id}")
