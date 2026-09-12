"""
Cryptographic Audit Ledger for Regulatory Compliance.
Maintains a verifiable SHA-256 chained ledger of candidate evaluations.
"""

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any


@dataclass
class AuditEntry:
    index: int
    timestamp: str
    candidate_id: str
    requisition_id: str
    status: str
    composite_score: float
    previous_hash: str
    current_hash: str
    payload_snapshot: Dict[str, Any] = field(default_factory=dict)


class ComplianceAuditLedger:
    def __init__(self):
        self._chain: List[AuditEntry] = []
        self._genesis_created = False
        self._init_genesis()

    @staticmethod
    def _compute_hash(index: int, prev_hash: str, candidate_id: str, requisition_id: str, status: str, composite_score: float, payload_str: str) -> str:
        hasher = hashlib.sha256()
        envelope = f"{index}:{prev_hash}:{candidate_id}:{requisition_id}:{status}:{composite_score:.2f}:{payload_str}"
        hasher.update(envelope.encode("utf-8"))
        return hasher.hexdigest()

    def _init_genesis(self):
        genesis_hash = self._compute_hash(
            0,
            "0" * 64,
            "SYSTEM",
            "SYSTEM",
            "GENESIS",
            100.0,
            "GENESIS_PAYLOAD"
        )
        genesis = AuditEntry(
            index=0,
            timestamp=datetime.now(timezone.utc).isoformat(),
            candidate_id="SYSTEM",
            requisition_id="SYSTEM",
            status="GENESIS",
            composite_score=100.0,
            previous_hash="0" * 64,
            current_hash=genesis_hash,
            payload_snapshot={"note": "Genesis block for regulatory compliance audit ledger"}
        )
        self._chain.append(genesis)
        self._genesis_created = True

    def record_decision(
        self,
        candidate_id: str,
        requisition_id: str,
        status: str,
        composite_score: float,
        payload_snapshot: Optional[Dict[str, Any]] = None
    ) -> AuditEntry:
        prev_entry = self._chain[-1]
        next_index = prev_entry.index + 1
        snapshot = payload_snapshot or {}
        payload_serialized = json.dumps(snapshot, sort_keys=True)

        current_hash = self._compute_hash(
            next_index,
            prev_entry.current_hash,
            candidate_id,
            requisition_id,
            status,
            composite_score,
            payload_serialized
        )

        entry = AuditEntry(
            index=next_index,
            timestamp=datetime.now(timezone.utc).isoformat(),
            candidate_id=candidate_id,
            requisition_id=requisition_id,
            status=status,
            composite_score=composite_score,
            previous_hash=prev_entry.current_hash,
            current_hash=current_hash,
            payload_snapshot=snapshot
        )
        self._chain.append(entry)
        return entry

    def verify_integrity(self) -> bool:
        if len(self._chain) <= 1:
            return True

        for i in range(1, len(self._chain)):
            curr = self._chain[i]
            prev = self._chain[i - 1]

            if curr.previous_hash != prev.current_hash:
                return False

            payload_serialized = json.dumps(curr.payload_snapshot, sort_keys=True)
            recomputed = self._compute_hash(
                curr.index,
                curr.previous_hash,
                curr.candidate_id,
                curr.requisition_id,
                curr.status,
                curr.composite_score,
                payload_serialized
            )
            if recomputed != curr.current_hash:
                return False

        return True

    def get_entry_by_index(self, index: int) -> Optional[AuditEntry]:
        if 0 <= index < len(self._chain):
            return self._chain[index]
        return None

    @property
    def length(self) -> int:
        return len(self._chain)
