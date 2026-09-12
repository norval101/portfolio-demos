"""
Unit tests for Cross-Border Manufacturing RFQ and Escrow Engine.
"""

import unittest
from src.models import (
    CadRfq,
    ManufacturerProfile,
    MachineCapability,
    EscrowState
)
from src.escrow_engine import (
    CrossBorderManufacturingEngine,
    InvalidStateTransitionError
)


class TestCrossBorderManufacturingEngine(unittest.TestCase):
    def setUp(self):
        self.rfq = CadRfq(
            rfq_id="RFQ-101",
            buyer_company="Detroit Precision Auto Corp",
            buyer_country="USA",
            part_name="Transmission Planetary Pinion Housing",
            cad_filename="pinion_housing_v4.step",
            material="AISI 4140 Alloy Steel",
            required_tolerance_mm=0.008,  # 8 microns
            required_capability=MachineCapability.FIVE_AXIS_CNC,
            quantity=500,
            hs_tariff_code="8482.10",
            target_budget_usd=45000.0
        )

        self.mfg_capable = ManufacturerProfile(
            mfg_id="MFG-WSR-01",
            company_name="Windsor High-Precision Tooling Ltd",
            country="CAN",
            capabilities=[MachineCapability.FIVE_AXIS_CNC, MachineCapability.WIRE_EDM],
            min_tolerance_mm=0.005,  # 5 microns (exceeds required precision)
            cusma_registered=True
        )

        self.mfg_incapable = ManufacturerProfile(
            mfg_id="MFG-WSR-02",
            company_name="Standard Stamping Shop",
            country="CAN",
            capabilities=[MachineCapability.PRECISION_STAMPING],
            min_tolerance_mm=0.05,
            cusma_registered=True
        )

    def test_capacity_matching_filters_properly(self):
        matches = CrossBorderManufacturingEngine.match_manufacturers(
            self.rfq,
            [self.mfg_capable, self.mfg_incapable]
        )
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].mfg_id, "MFG-WSR-01")

    def test_cusma_certificate_generation(self):
        cert = CrossBorderManufacturingEngine.generate_cusma_certificate(self.rfq, self.mfg_capable)
        self.assertTrue(cert.is_eligible)
        self.assertIn("Criterion B", cert.origin_criterion)
        self.assertEqual(cert.hs_code, "8482.10")

    def test_full_escrow_lifecycle_and_payout_split(self):
        order = CrossBorderManufacturingEngine.create_order(self.rfq, self.mfg_capable.mfg_id, 45000.0)
        self.assertEqual(order.state, EscrowState.QUOTED)

        # 1. Fund
        CrossBorderManufacturingEngine.fund_escrow(order)
        self.assertEqual(order.state, EscrowState.ESCROW_FUNDED)

        # 2. Manufacture
        CrossBorderManufacturingEngine.start_manufacturing(order)
        self.assertEqual(order.state, EscrowState.IN_MANUFACTURE)

        # 3. Ship
        CrossBorderManufacturingEngine.dispatch_shipment(order, "CN-FREIGHT-883921")
        self.assertEqual(order.state, EscrowState.IN_TRANSIT)
        self.assertEqual(order.tracking_number, "CN-FREIGHT-883921")

        # 4. Deliver
        CrossBorderManufacturingEngine.confirm_delivery(order)
        self.assertEqual(order.state, EscrowState.DELIVERED_INSPECTION)

        # 5. Release Escrow
        CrossBorderManufacturingEngine.release_escrow(order)
        self.assertEqual(order.state, EscrowState.FUNDS_RELEASED)
        # 90% to manufacturer ($40,500), 10% platform fee ($4,500)
        self.assertAlmostEqual(order.manufacturer_payout, 40500.0, places=2)
        self.assertAlmostEqual(order.platform_fee, 4500.0, places=2)

    def test_invalid_transition_raises_error(self):
        order = CrossBorderManufacturingEngine.create_order(self.rfq, self.mfg_capable.mfg_id, 10000.0)
        # Cannot release escrow directly from QUOTED without funding and delivery
        with self.assertRaises(InvalidStateTransitionError):
            CrossBorderManufacturingEngine.release_escrow(order)


if __name__ == "__main__":
    unittest.main()
