"""
Unit tests for Merchandising Audit & Planogram Compliance Engine.
"""

import unittest
from src.models import (
    PlanogramSkuSpec,
    AuditedSkuObservation,
    StoreAuditInput,
    SkuAvailabilityStatus,
    PromotionPriceStatus
)
from src.audit_engine import MerchandisingAuditEngine


class TestMerchandisingAuditEngine(unittest.TestCase):
    def setUp(self):
        self.engine = MerchandisingAuditEngine()

    def test_perfect_store_execution_score(self):
        specs = [
            PlanogramSkuSpec("SKU-1", "Organic Juice 1L", "PureFresh", expected_facings=3, shelf_level=2),
            PlanogramSkuSpec("SKU-2", "Apple Cider 750ml", "PureFresh", expected_facings=2, shelf_level=2)
        ]
        observations = [
            AuditedSkuObservation("SKU-1", actual_facings=3, availability=SkuAvailabilityStatus.IN_STOCK, price_tag_status=PromotionPriceStatus.MATCHES),
            AuditedSkuObservation("SKU-2", actual_facings=2, availability=SkuAvailabilityStatus.IN_STOCK, price_tag_status=PromotionPriceStatus.MATCHES)
        ]
        audit = StoreAuditInput(
            store_id="STR-501",
            store_name="Metro Downtown",
            auditor_id="AUD-09",
            audit_date="2026-09-12",
            planogram_specs=specs,
            observations=observations,
            competitor_facings=5,  # 5 brand vs 5 competitor = 50% Share of Shelf
            pos_materials_displayed=True
        )

        metrics = self.engine.evaluate(audit)
        self.assertEqual(metrics.planogram_compliance_pct, 100.0)
        self.assertEqual(metrics.shelf_availability_pct, 100.0)
        self.assertEqual(metrics.brand_share_of_shelf_pct, 50.0)
        self.assertEqual(metrics.store_execution_score, 100.0)
        self.assertEqual(len(metrics.out_of_stock_skus), 0)

    def test_out_of_stock_penalizes_score(self):
        specs = [
            PlanogramSkuSpec("SKU-1", "Almond Milk", "NutriDiet", expected_facings=4, shelf_level=1),
            PlanogramSkuSpec("SKU-2", "Oat Milk", "NutriDiet", expected_facings=3, shelf_level=1),
            PlanogramSkuSpec("SKU-3", "Soy Milk", "NutriDiet", expected_facings=2, shelf_level=1)
        ]
        observations = [
            AuditedSkuObservation("SKU-1", actual_facings=4, availability=SkuAvailabilityStatus.IN_STOCK, price_tag_status=PromotionPriceStatus.MATCHES),
            AuditedSkuObservation("SKU-2", actual_facings=0, availability=SkuAvailabilityStatus.OUT_OF_STOCK, price_tag_status=PromotionPriceStatus.DISCREPANCY),
            AuditedSkuObservation("SKU-3", actual_facings=2, availability=SkuAvailabilityStatus.IN_STOCK, price_tag_status=PromotionPriceStatus.MATCHES)
        ]
        audit = StoreAuditInput(
            store_id="STR-702",
            store_name="WholeFoods Market",
            auditor_id="AUD-12",
            audit_date="2026-09-12",
            planogram_specs=specs,
            observations=observations,
            competitor_facings=14,
            pos_materials_displayed=False
        )

        metrics = self.engine.evaluate(audit)
        self.assertIn("SKU-2", metrics.out_of_stock_skus)
        self.assertAlmostEqual(metrics.planogram_compliance_pct, 66.67, places=1)
        self.assertAlmostEqual(metrics.shelf_availability_pct, 66.67, places=1)
        self.assertLess(metrics.store_execution_score, 80.0)


if __name__ == "__main__":
    unittest.main()
