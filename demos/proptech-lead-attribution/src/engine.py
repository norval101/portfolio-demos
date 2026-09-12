"""
PropTech Compliance Evaluation, Lead Routing, and Multi-Touch Attribution Engine.
"""

from typing import List, Dict, Optional
from collections import defaultdict
from .models import (
    RealtorComplianceRecord,
    BuyerSellerLead,
    LeadAttributionReport,
    UserRoleLevel
)


class PropTechGovernanceEngine:
    @staticmethod
    def resolve_dashboard_route(role: UserRoleLevel) -> str:
        """Determines role-segregated UI dashboard entrypoints."""
        routes = {
            UserRoleLevel.PLATFORM_ADMIN: "/admin/dashboard/overview",
            UserRoleLevel.ASSOCIATION_ADMIN: "/raj/dashboard/realtors",
            UserRoleLevel.BROKER_ADMIN: "/broker/dashboard/compliance",
            UserRoleLevel.REALTOR_MEMBER: "/realtor/dashboard/home"
        }
        return routes.get(role, "/user/dashboard")

    @staticmethod
    def calculate_linear_attribution(lead: BuyerSellerLead) -> Dict[str, float]:
        """Calculates linear multi-touch attribution across all recorded campaign touchpoints."""
        if not lead.touchpoints:
            return {"ORGANIC_DIRECT": 100.0}

        total_touches = len(lead.touchpoints)
        weight_per_touch = 100.0 / total_touches

        attribution: Dict[str, float] = defaultdict(float)
        for touch in lead.touchpoints:
            attribution[touch.channel.value] += weight_per_touch

        # Round values nicely
        return {ch: round(score, 2) for ch, score in attribution.items()}

    @classmethod
    def route_lead_to_compliant_realtor(
        cls,
        lead: BuyerSellerLead,
        realtors: List[RealtorComplianceRecord]
    ) -> LeadAttributionReport:
        channel_credits = cls.calculate_linear_attribution(lead)

        # Filter candidate realtors who match territory and pass all regulatory compliance gates
        eligible = [
            r for r in realtors
            if r.territory.lower() == lead.target_territory.lower() and r.is_fully_compliant
        ]

        assigned_id = eligible[0].realtor_id if eligible else None

        return LeadAttributionReport(
            lead_id=lead.lead_id,
            assigned_realtor_id=assigned_id,
            channel_credits=channel_credits,
            attribution_model="LINEAR_MULTI_TOUCH"
        )
