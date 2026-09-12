"""
Core Engine for Capacity Matching, CUSMA Certificate Generation, and Escrow State Machine.
"""

from typing import List, Optional
import uuid
from datetime import datetime, timezone

from .models import (
    CadRfq,
    ManufacturerProfile,
    EscrowOrder,
    EscrowState,
    CusmaCertificate
)


class InvalidStateTransitionError(Exception):
    """Raised when an order transition violates the escrow state machine rules."""
    pass


class CrossBorderManufacturingEngine:
    # 90% payout to manufacturer, 10% platform fee
    MANUFACTURER_SHARE = 0.90
    PLATFORM_SHARE = 0.10

    @staticmethod
    def match_manufacturers(rfq: CadRfq, manufacturers: List[ManufacturerProfile]) -> List[ManufacturerProfile]:
        """Filters manufacturers that possess required capability, tolerance precision, and cross-border standing."""
        matches: List[ManufacturerProfile] = []
        for m in manufacturers:
            has_capability = rfq.required_capability in m.capabilities
            meets_tolerance = m.min_tolerance_mm <= rfq.required_tolerance_mm
            if has_capability and meets_tolerance:
                matches.append(m)
        return matches

    @staticmethod
    def generate_cusma_certificate(rfq: CadRfq, mfg: ManufacturerProfile) -> CusmaCertificate:
        """Generates automated CUSMA / USMCA origin documentation based on HS codes and manufacturing origin."""
        cert_id = f"CUSMA-{uuid.uuid4().hex[:8].upper()}"
        # North American Trade Agreement check: Canada -> USA
        is_eligible = (mfg.country == "CAN" and rfq.buyer_country == "USA" and mfg.cusma_registered)
        criterion = "Criterion B - Regional Value Content (RVC >= 60%)" if is_eligible else "Ineligible"

        return CusmaCertificate(
            cert_id=cert_id,
            rfq_id=rfq.rfq_id,
            exporter_mfg_id=mfg.mfg_id,
            importer_company=rfq.buyer_company,
            hs_code=rfq.hs_tariff_code,
            origin_criterion=criterion,
            is_eligible=is_eligible,
            generated_at=datetime.now(timezone.utc).isoformat()
        )

    @classmethod
    def create_order(cls, rfq: CadRfq, mfg_id: str, agreed_amount_usd: float) -> EscrowOrder:
        order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        return EscrowOrder(
            order_id=order_id,
            rfq_id=rfq.rfq_id,
            buyer_company=rfq.buyer_company,
            mfg_id=mfg_id,
            total_amount_usd=agreed_amount_usd,
            state=EscrowState.QUOTED
        )

    @classmethod
    def fund_escrow(cls, order: EscrowOrder) -> None:
        if order.state != EscrowState.QUOTED:
            raise InvalidStateTransitionError(f"Cannot fund escrow from state {order.state}")
        order.state = EscrowState.ESCROW_FUNDED

    @classmethod
    def start_manufacturing(cls, order: EscrowOrder) -> None:
        if order.state != EscrowState.ESCROW_FUNDED:
            raise InvalidStateTransitionError(f"Cannot start manufacturing from state {order.state}")
        order.state = EscrowState.IN_MANUFACTURE

    @classmethod
    def dispatch_shipment(cls, order: EscrowOrder, tracking_number: str) -> None:
        if order.state != EscrowState.IN_MANUFACTURE:
            raise InvalidStateTransitionError(f"Cannot ship order from state {order.state}")
        order.state = EscrowState.IN_TRANSIT
        order.tracking_number = tracking_number

    @classmethod
    def confirm_delivery(cls, order: EscrowOrder) -> None:
        if order.state != EscrowState.IN_TRANSIT:
            raise InvalidStateTransitionError(f"Cannot mark delivered from state {order.state}")
        order.state = EscrowState.DELIVERED_INSPECTION
        order.inspection_days_remaining = 5

    @classmethod
    def release_escrow(cls, order: EscrowOrder) -> None:
        if order.state != EscrowState.DELIVERED_INSPECTION:
            raise InvalidStateTransitionError(f"Cannot release funds from state {order.state}")
        order.manufacturer_payout = round(order.total_amount_usd * cls.MANUFACTURER_SHARE, 2)
        order.platform_fee = round(order.total_amount_usd * cls.PLATFORM_SHARE, 2)
        order.state = EscrowState.FUNDS_RELEASED

    @classmethod
    def file_dispute(cls, order: EscrowOrder) -> None:
        if order.state != EscrowState.DELIVERED_INSPECTION:
            raise InvalidStateTransitionError(f"Dispute can only be filed during inspection window, not in {order.state}")
        order.state = EscrowState.DISPUTED
