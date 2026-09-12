"""
Domain models for Document Audit and Compliance Pipeline.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone


class AnomalySeverity(str, Enum):
    BLOCKER = "BLOCKER"
    WARNING = "WARNING"
    INFO = "INFO"


class AuditVerdict(str, Enum):
    PASSED = "PASSED"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class DocumentPayload:
    document_id: str
    candidate_id: str
    document_type: str  # e.g., "PASSPORT", "POLICE_RECORD", "MEDICAL_CLEARANCE", "DS_2019"
    candidate_legal_name: str
    extracted_name: str
    issue_date: str     # YYYY-MM-DD
    expiry_date: str    # YYYY-MM-DD
    issuing_country: str
    file_sha256: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AnomalyFlag:
    code: str
    severity: AnomalySeverity
    message: str
    field_name: Optional[str] = None


@dataclass(frozen=True)
class AuditReport:
    document_id: str
    candidate_id: str
    verdict: AuditVerdict
    risk_score: float  # 0.0 to 100.0%
    anomalies: List[AnomalyFlag]
    audit_timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
