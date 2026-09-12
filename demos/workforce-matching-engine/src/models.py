"""
Domain models for Workforce Matching and Compliance Engine.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone


class QualificationStatus(str, Enum):
    RECOMMENDED = "RECOMMENDED"
    QUALIFIED_WITH_CONDITIONS = "QUALIFIED_WITH_CONDITIONS"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class CandidateProfile:
    id: str
    name: str
    noc_code: str
    years_experience: float
    skills: List[str]
    clb_level: int
    compliance_cleared: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class JobRequisition:
    id: str
    title: str
    target_noc: str
    min_experience_years: float
    required_skills: List[str]
    min_clb_level: int = 7
    compliance_required: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ScoreBreakdown:
    noc_score: float
    experience_score: float
    skills_score: float
    language_score: float
    composite_score: float


@dataclass(frozen=True)
class MatchResult:
    candidate_id: str
    requisition_id: str
    status: QualificationStatus
    scores: ScoreBreakdown
    reasons: List[str]
    is_compliant: bool
    audit_hash: str = ""
    evaluated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
