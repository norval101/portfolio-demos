"""
Domain models for Cross-Border RFQ and Escrow State Machine.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional
from datetime import datetime, timezone


class EscrowState(str, Enum):
    DRAFT = "DRAFT"
    QUOTED = "QUOTED"
    ESCROW_FUNDED = "ESCROW_FUNDED"
    IN_MANUFACTURE = "IN_MANUFACTURE"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED_INSPECTION = "DELIVERED_INSPECTION"
    FUNDS_RELEASED = "FUNDS_RELEASED"
    DISPUTED = "DISPUTED"
    REFUNDED = "REFUNDED"


class MachineCapability(str, Enum):
    FIVE_AXIS_CNC = "FIVE_AXIS_CNC"
    PRECISION_STAMPING = "PRECISION_STAMPING"
    WIRE_EDM = "WIRE_EDM"
    CNC_LATHE = "CNC_LATHE"
    TOOL_AND_DIE = "TOOL_AND_DIE"


@dataclass(frozen=True)
class CadRfq:
    rfq_id: str
    buyer_company: str
    buyer_country: str  # e.g. "USA"
    part_name: str
    cad_filename: str
    material: str
    required_tolerance_mm: float
    required_capability: MachineCapability
    quantity: int
    hs_tariff_code: str  # e.g. "8482.10"
    target_budget_usd: float


@dataclass(frozen=True)
class ManufacturerProfile:
    mfg_id: str
    company_name: str
    country: str  # e.g. "CAN"
    capabilities: List[MachineCapability]
    min_tolerance_mm: float
    cusma_registered: bool = True


@dataclass(frozen=True)
class CusmaCertificate:
    cert_id: str
    rfq_id: str
    exporter_mfg_id: str
    importer_company: str
    hs_code: str
    origin_criterion: str
    is_eligible: bool
    generated_at: str


@dataclass
class EscrowOrder:
    order_id: str
    rfq_id: str
    buyer_company: str
    mfg_id: str
    total_amount_usd: float
    state: EscrowState
    manufacturer_payout: float = 0.0
    platform_fee: float = 0.0
    inspection_days_remaining: int = 5
    tracking_number: Optional[str] = None
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
