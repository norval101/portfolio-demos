"""
Domain models for Retail Merchandising and Planogram Compliance Audit.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional


class SkuAvailabilityStatus(str, Enum):
    IN_STOCK = "IN_STOCK"
    LOW_STOCK = "LOW_STOCK"
    OUT_OF_STOCK = "OUT_OF_STOCK"


class PromotionPriceStatus(str, Enum):
    MATCHES = "MATCHES"
    DISCREPANCY = "DISCREPANCY"
    MISSING_TAG = "MISSING_TAG"


@dataclass(frozen=True)
class PlanogramSkuSpec:
    sku_id: str
    product_name: str
    brand: str
    expected_facings: int
    shelf_level: int
    is_core_sku: bool = True


@dataclass(frozen=True)
class AuditedSkuObservation:
    sku_id: str
    actual_facings: int
    availability: SkuAvailabilityStatus
    price_tag_status: PromotionPriceStatus
    product_facing_straight: bool = True


@dataclass(frozen=True)
class StoreAuditInput:
    store_id: str
    store_name: str
    auditor_id: str
    audit_date: str
    planogram_specs: List[PlanogramSkuSpec]
    observations: List[AuditedSkuObservation]
    competitor_facings: int
    pos_materials_displayed: bool


@dataclass(frozen=True)
class StoreAuditMetrics:
    planogram_compliance_pct: float
    shelf_availability_pct: float
    brand_share_of_shelf_pct: float
    pos_promo_visibility_pct: float
    facing_quality_pct: float
    store_execution_score: float
    out_of_stock_skus: List[str]
