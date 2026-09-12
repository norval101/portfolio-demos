"""
Unit tests for PropTech Compliance, Route Dispatching, and Lead Attribution Engine.
"""

import unittest
from src.models import (
    UserRoleLevel,
    MarketingChannel,
    RealtorComplianceRecord,
    LeadTouchpoint,
    BuyerSellerLead
)
from src.engine import PropTechGovernanceEngine


class TestPropTechGovernanceEngine(unittest.TestCase):
    def test_role_based_routing(self):
        self.assertEqual(
            PropTechGovernanceEngine.resolve_dashboard_route(UserRoleLevel.ASSOCIATION_ADMIN),
            "/raj/dashboard/realtors"
        )
        self.assertEqual(
            PropTechGovernanceEngine.resolve_dashboard_route(UserRoleLevel.REALTOR_MEMBER),
            "/realtor/dashboard/home"
        )

    def test_multi_touch_linear_attribution_split(self):
        lead = BuyerSellerLead(
            lead_id="LEAD-881",
            contact_name="Daniel Craig",
            target_territory="Windsor-Essex",
            estimated_budget=750000.0,
            touchpoints=[
                LeadTouchpoint(MarketingChannel.GOOGLE_SEARCH, "camp-g-1", "2026-09-01T10:00:00Z"),
                LeadTouchpoint(MarketingChannel.META_INSTAGRAM, "camp-m-2", "2026-09-05T14:30:00Z"),
                LeadTouchpoint(MarketingChannel.LINKEDIN, "camp-li-3", "2026-09-08T09:15:00Z"),
                LeadTouchpoint(MarketingChannel.GOOGLE_SEARCH, "camp-g-retarget", "2026-09-10T11:00:00Z")
            ]
        )

        credits = PropTechGovernanceEngine.calculate_linear_attribution(lead)
        # 4 total touchpoints: Google has 2 (50%), Meta has 1 (25%), LinkedIn has 1 (25%)
        self.assertAlmostEqual(credits["GOOGLE_SEARCH"], 50.0, places=1)
        self.assertAlmostEqual(credits["META_INSTAGRAM"], 25.0, places=1)
        self.assertAlmostEqual(credits["LINKEDIN"], 25.0, places=1)

    def test_lead_routing_enforces_compliance_and_territory(self):
        compliant_realtor = RealtorComplianceRecord(
            realtor_id="REALTOR-01",
            legal_name="Sarah Jenkins",
            brokerage_id="BRK-01",
            territory="Windsor-Essex",
            license_active=True,
            cpd_hours_completed=15.0,  # >= 12 required
            active_disciplinary_sanctions=0
        )

        non_compliant_realtor = RealtorComplianceRecord(
            realtor_id="REALTOR-02",
            legal_name="John Defaulter",
            brokerage_id="BRK-01",
            territory="Windsor-Essex",
            license_active=True,
            cpd_hours_completed=4.0,  # < 12 required, non-compliant!
            active_disciplinary_sanctions=0
        )

        wrong_territory_realtor = RealtorComplianceRecord(
            realtor_id="REALTOR-03",
            legal_name="Mark Calgary",
            brokerage_id="BRK-02",
            territory="Calgary-NW",
            license_active=True,
            cpd_hours_completed=14.0,
            active_disciplinary_sanctions=0
        )

        lead = BuyerSellerLead(
            lead_id="LEAD-900",
            contact_name="Evelyn Rose",
            target_territory="Windsor-Essex",
            estimated_budget=600000.0,
            touchpoints=[]
        )

        report = PropTechGovernanceEngine.route_lead_to_compliant_realtor(
            lead,
            [non_compliant_realtor, wrong_territory_realtor, compliant_realtor]
        )

        # Must route exclusively to the compliant realtor in Windsor-Essex
        self.assertEqual(report.assigned_realtor_id, "REALTOR-01")


if __name__ == "__main__":
    unittest.main()
