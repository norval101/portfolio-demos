"""
Domain models for NGO Grant Governance and Milestone Disbursement.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from datetime import datetime, timezone


class MilestoneStatus(str, Enum):
    PENDING = "PENDING"
    EVIDENCE_SUBMITTED = "EVIDENCE_SUBMITTED"
    APPROVED = "APPROVED"
    DISBURSED = "DISBURSED"
    REJECTED = "REJECTED"


class GrantStatus(str, Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    FROZEN = "FROZEN"


@dataclass
class GrantMilestone:
    milestone_id: str
    title: str
    allocated_amount_usd: float
    status: MilestoneStatus = MilestoneStatus.PENDING
    evidence_url: Optional[str] = None
    approved_by: Optional[str] = None
    disbursed_at: Optional[str] = None


@dataclass
class ProjectGrant:
    grant_id: str
    program_name: str
    recipient_ngo: str
    total_budget_usd: float
    milestones: List[GrantMilestone]
    status: GrantStatus = GrantStatus.ACTIVE
    disbursed_total_usd: float = 0.0

    @property
    def remaining_budget_usd(self) -> float:
        return round(self.total_budget_usd - self.disbursed_total_usd, 2)
