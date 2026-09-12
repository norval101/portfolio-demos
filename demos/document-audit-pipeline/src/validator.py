"""
Core Document Audit and Anomaly Detection Rules Engine.
"""

from datetime import datetime, date, timezone
from typing import List, Tuple, Set, Optional
import re

from .models import (
    DocumentPayload,
    AnomalyFlag,
    AnomalySeverity,
    AuditReport,
    AuditVerdict
)


class DocumentAuditPipeline:
    def __init__(self, reference_date: Optional[date] = None):
        # Allow injecting reference date for deterministic test execution
        self.ref_date = reference_date or date.today()

    def audit(self, doc: DocumentPayload) -> AuditReport:
        anomalies: List[AnomalyFlag] = []

        # Stage 1: Checksum & Identifier Integrity
        self._check_file_integrity(doc, anomalies)

        # Stage 2: Temporal Boundaries & Validity
        self._check_temporal_validity(doc, anomalies)

        # Stage 3: Cross-Field Identity Consistency
        self._check_identity_consistency(doc, anomalies)

        # Stage 4: Document Type Specific Constraints
        self._check_type_specific_rules(doc, anomalies)

        # Compute Risk Score & Final Verdict
        verdict, risk_score = self._compute_verdict_and_risk(anomalies)

        return AuditReport(
            document_id=doc.document_id,
            candidate_id=doc.candidate_id,
            verdict=verdict,
            risk_score=risk_score,
            anomalies=anomalies
        )

    def _check_file_integrity(self, doc: DocumentPayload, anomalies: List[AnomalyFlag]):
        if not doc.file_sha256 or len(doc.file_sha256) != 64 or not re.match(r"^[0-9a-fA-F]{64}$", doc.file_sha256):
            anomalies.append(AnomalyFlag(
                code="ERR_INTEGRITY_CHECKSUM_INVALID",
                severity=AnomalySeverity.BLOCKER,
                message="Corrupted or invalid SHA-256 document checksum.",
                field_name="file_sha256"
            ))

    def _check_temporal_validity(self, doc: DocumentPayload, anomalies: List[AnomalyFlag]):
        # Parse Dates
        try:
            issue_dt = datetime.strptime(doc.issue_date, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            anomalies.append(AnomalyFlag(
                code="ERR_DATE_ISSUE_FORMAT",
                severity=AnomalySeverity.BLOCKER,
                message="Issue date is missing or not in YYYY-MM-DD format.",
                field_name="issue_date"
            ))
            issue_dt = None

        try:
            expiry_dt = datetime.strptime(doc.expiry_date, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            anomalies.append(AnomalyFlag(
                code="ERR_DATE_EXPIRY_FORMAT",
                severity=AnomalySeverity.BLOCKER,
                message="Expiry date is missing or not in YYYY-MM-DD format.",
                field_name="expiry_date"
            ))
            expiry_dt = None

        if issue_dt and expiry_dt:
            if expiry_dt <= issue_dt:
                anomalies.append(AnomalyFlag(
                    code="ERR_EXPIRY_BEFORE_ISSUE",
                    severity=AnomalySeverity.BLOCKER,
                    message="Document expiration date cannot be earlier than or equal to issue date.",
                    field_name="expiry_date"
                ))

            if expiry_dt < self.ref_date:
                anomalies.append(AnomalyFlag(
                    code="ERR_DOCUMENT_EXPIRED",
                    severity=AnomalySeverity.BLOCKER,
                    message=f"Document expired on {expiry_dt} (reference date: {self.ref_date}).",
                    field_name="expiry_date"
                ))
            else:
                days_left = (expiry_dt - self.ref_date).days
                # Regulatory rule: international travel requires >= 6 months (180 days) passport validity
                if doc.document_type == "PASSPORT" and days_left < 180:
                    anomalies.append(AnomalyFlag(
                        code="WARN_PASSPORT_EXPIRING_SOON",
                        severity=AnomalySeverity.WARNING,
                        message=f"Passport has only {days_left} days of validity remaining (< 180 day 6-month rule).",
                        field_name="expiry_date"
                    ))

    def _check_identity_consistency(self, doc: DocumentPayload, anomalies: List[AnomalyFlag]):
        # Normalize and compare names token-wise
        legal_tokens = set(re.findall(r"\w+", doc.candidate_legal_name.lower()))
        extracted_tokens = set(re.findall(r"\w+", doc.extracted_name.lower()))

        if not legal_tokens or not extracted_tokens:
            anomalies.append(AnomalyFlag(
                code="ERR_NAME_EMPTY",
                severity=AnomalySeverity.BLOCKER,
                message="Legal name or extracted document name is empty.",
                field_name="extracted_name"
            ))
            return

        intersection = legal_tokens.intersection(extracted_tokens)
        similarity = len(intersection) / max(len(legal_tokens), len(extracted_tokens))

        if similarity < 0.6:
            anomalies.append(AnomalyFlag(
                code="ERR_NAME_MISMATCH",
                severity=AnomalySeverity.BLOCKER,
                message=f"Document name '{doc.extracted_name}' does not align with legal candidate name '{doc.candidate_legal_name}'.",
                field_name="extracted_name"
            ))
        elif similarity < 1.0:
            anomalies.append(AnomalyFlag(
                code="WARN_NAME_PARTIAL_MATCH",
                severity=AnomalySeverity.WARNING,
                message=f"Minor name discrepancy detected: '{doc.extracted_name}' vs '{doc.candidate_legal_name}'.",
                field_name="extracted_name"
            ))

    def _check_type_specific_rules(self, doc: DocumentPayload, anomalies: List[AnomalyFlag]):
        if doc.document_type == "POLICE_RECORD":
            # Police clearances typically must be issued within 6 months
            try:
                issue_dt = datetime.strptime(doc.issue_date, "%Y-%m-%d").date()
                age_days = (self.ref_date - issue_dt).days
                if age_days > 180:
                    anomalies.append(AnomalyFlag(
                        code="ERR_POLICE_RECORD_STALE",
                        severity=AnomalySeverity.BLOCKER,
                        message=f"Police clearance was issued {age_days} days ago (> 180 days maximum limit).",
                        field_name="issue_date"
                    ))
            except (ValueError, TypeError):
                pass

    def _compute_verdict_and_risk(self, anomalies: List[AnomalyFlag]) -> Tuple[AuditVerdict, float]:
        blockers = [a for a in anomalies if a.severity == AnomalySeverity.BLOCKER]
        warnings = [a for a in anomalies if a.severity == AnomalySeverity.WARNING]

        if blockers:
            risk = 90.0 + min(len(blockers) * 2.5, 10.0)
            return AuditVerdict.REJECTED, min(100.0, risk)
        elif warnings:
            risk = 25.0 + (len(warnings) * 15.0)
            return AuditVerdict.NEEDS_REVIEW, min(75.0, risk)
        else:
            return AuditVerdict.PASSED, 0.0
