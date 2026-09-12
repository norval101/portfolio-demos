"""
Retail Merchandising Audit & Store Execution Scoring Engine.
"""

from typing import List, Dict, Set
from .models import (
    StoreAuditInput,
    StoreAuditMetrics,
    PlanogramSkuSpec,
    AuditedSkuObservation,
    SkuAvailabilityStatus,
    PromotionPriceStatus
)


class MerchandisingAuditEngine:
    # Component weights for composite Store Execution Score (SES)
    WEIGHT_POG = 0.30
    WEIGHT_AVAILABILITY = 0.30
    WEIGHT_POS = 0.20
    WEIGHT_FACING = 0.20

    def evaluate(self, audit: StoreAuditInput) -> StoreAuditMetrics:
        spec_map: Dict[str, PlanogramSkuSpec] = {s.sku_id: s for s in audit.planogram_specs}
        obs_map: Dict[str, AuditedSkuObservation] = {o.sku_id: o for o in audit.observations}

        total_skus = len(audit.planogram_specs)
        if total_skus == 0:
            return StoreAuditMetrics(100.0, 100.0, 0.0, 100.0, 100.0, 100.0, [])

        pog_compliant_count = 0
        in_stock_count = 0
        facing_straight_count = 0
        promo_price_matches_count = 0
        total_brand_facings = 0
        oos_skus: List[str] = []

        for spec in audit.planogram_specs:
            obs = obs_map.get(spec.sku_id)

            if obs is not None:
                total_brand_facings += obs.actual_facings

                # 1. POG compliance: actual facings must equal or exceed expected facings
                if obs.actual_facings >= spec.expected_facings:
                    pog_compliant_count += 1

                # 2. Shelf Availability
                if obs.availability == SkuAvailabilityStatus.IN_STOCK:
                    in_stock_count += 1
                elif obs.availability == SkuAvailabilityStatus.OUT_OF_STOCK:
                    oos_skus.append(spec.sku_id)

                # 3. Facing Quality
                if obs.product_facing_straight:
                    facing_straight_count += 1

                # 4. Promotion / POS pricing tag match
                if obs.price_tag_status == PromotionPriceStatus.MATCHES:
                    promo_price_matches_count += 1
            else:
                # Missing from observation implies missing from shelf
                oos_skus.append(spec.sku_id)

        # Percentages
        pog_pct = round((pog_compliant_count / total_skus) * 100.0, 2)
        avail_pct = round((in_stock_count / total_skus) * 100.0, 2)
        facing_pct = round((facing_straight_count / total_skus) * 100.0, 2)

        # POS Visibility Score (combines materials presence and price tag accuracy)
        promo_price_pct = (promo_price_matches_count / total_skus) * 100.0
        pos_display_factor = 100.0 if audit.pos_materials_displayed else 50.0
        pos_visibility_pct = round((0.6 * promo_price_pct) + (0.4 * pos_display_factor), 2)

        # Brand Share of Shelf (SoS)
        total_category_facings = total_brand_facings + max(0, audit.competitor_facings)
        if total_category_facings > 0:
            sos_pct = round((total_brand_facings / total_category_facings) * 100.0, 2)
        else:
            sos_pct = 0.0

        # Composite Store Execution Score
        ses = (
            (self.WEIGHT_POG * pog_pct) +
            (self.WEIGHT_AVAILABILITY * avail_pct) +
            (self.WEIGHT_POS * pos_visibility_pct) +
            (self.WEIGHT_FACING * facing_pct)
        )
        ses = round(min(100.0, max(0.0, ses)), 2)

        return StoreAuditMetrics(
            planogram_compliance_pct=pog_pct,
            shelf_availability_pct=avail_pct,
            brand_share_of_shelf_pct=sos_pct,
            pos_promo_visibility_pct=pos_visibility_pct,
            facing_quality_pct=facing_pct,
            store_execution_score=ses,
            out_of_stock_skus=oos_skus
        )
