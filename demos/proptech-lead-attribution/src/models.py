"""
Domain models for PropTech Compliance and Lead Attribution.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional
from datetime import datetime, timezone


class UserRoleLevel(str, Enum):
    PLATFORM_ADMIN = "PLATFORM_ADMIN"
    ASSOCIATION_ADMIN = "ASSOCIATION_ADMIN"
    BROKER_ADMIN = "BROKER_ADMIN"
    REALTOR_MEMBER = "REALTOR_MEMBER"


class MarketingChannel(str, Enum):
    GOOGLE_SEARCH = "GOOGLE_SEARCH"
    META_INSTAGRAM = "META_INSTAGRAM"
    LINKEDIN = "LINKEDIN"
    TIKTOK = "TIKTOK"
    ORGANIC_DIRECT = "ORGANIC_DIRECT"


@dataclass(frozen=True)
class RealtorComplianceRecord:
    realtor_id: str
    legal_name: str
    brokerage_id: str
    territory: str  # e.g. "Windsor-Essex", "Calgary-NW"
    license_active: bool
    cpd_hours_completed: float
    cpd_hours_required: float = 12.0
    active_disciplinary_sanctions: int = 0

    @property
    def is_fully_compliant(self) -> bool:
        return (
            self.license_active and
            self.cpd_hours_completed >= self.cpd_hours_required and
            self.active_disciplinary_sanctions == 0
        )


@dataclass(frozen=True)
class LeadTouchpoint:
    channel: MarketingChannel
    campaign_id: str
    timestamp: str


@dataclass(frozen=True)
class BuyerSellerLead:
    lead_id: str
    contact_name: str
    target_territory: str
    estimated_budget: float
    touchpoints: List[LeadTouchpoint]


@dataclass(frozen=True)
class LeadAttributionReport:
    lead_id: str
    assigned_realtor_id: Optional[str]
    channel_credits: Dict[str, float]  # Percentage credit attributed to each marketing channel
    attribution_model: str = "LINEAR_MULTI_TOUCH"
