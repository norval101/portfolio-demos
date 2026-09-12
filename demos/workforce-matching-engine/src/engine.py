"""
Core Workforce Matching Engine with weighted scoring and regulatory rules gating.
"""

from dataclasses import dataclass
from typing import List, Optional, Set
from .models import (
    CandidateProfile,
    JobRequisition,
    MatchResult,
    ScoreBreakdown,
    QualificationStatus
)
from .audit import ComplianceAuditLedger


@dataclass(frozen=True)
class ScoringWeights:
    noc: float = 0.35
    experience: float = 0.25
    skills: float = 0.25
    language: float = 0.15

    def __post_init__(self):
        total = self.noc + self.experience + self.skills + self.language
        if round(total, 4) != 1.0:
            raise ValueError(f"Scoring weights must sum to 1.0, got {total}")


class WorkforceMatchingEngine:
    def __init__(
        self,
        weights: Optional[ScoringWeights] = None,
        audit_ledger: Optional[ComplianceAuditLedger] = None
    ):
        self.weights = weights or ScoringWeights()
        self.audit_ledger = audit_ledger or ComplianceAuditLedger()

    def evaluate(
        self,
        candidate: CandidateProfile,
        requisition: JobRequisition
    ) -> MatchResult:
        reasons: List[str] = []

        # 1. Mandatory Regulatory Compliance Gate
        if requisition.compliance_required and not candidate.compliance_cleared:
            reasons.append("Disqualified: Candidate failed mandatory regulatory compliance clearance.")
            scores = ScoreBreakdown(0.0, 0.0, 0.0, 0.0, 0.0)
            audit_entry = self.audit_ledger.record_decision(
                candidate_id=candidate.id,
                requisition_id=requisition.id,
                status=QualificationStatus.REJECTED.value,
                composite_score=0.0,
                payload_snapshot={"reasons": reasons, "compliance_failure": True}
            )
            return MatchResult(
                candidate_id=candidate.id,
                requisition_id=requisition.id,
                status=QualificationStatus.REJECTED,
                scores=scores,
                reasons=reasons,
                is_compliant=False,
                audit_hash=audit_entry.current_hash
            )

        # 2. NOC Alignment Score
        noc_score = self._compute_noc_score(candidate.noc_code, requisition.target_noc, reasons)

        # 3. Experience Alignment Score
        exp_score = self._compute_experience_score(
            candidate.years_experience,
            requisition.min_experience_years,
            reasons
        )

        # 4. Skills & Certifications Overlap Score
        skills_score = self._compute_skills_score(
            candidate.skills,
            requisition.required_skills,
            reasons
        )

        # 5. Language Benchmark Score
        lang_score = self._compute_language_score(
            candidate.clb_level,
            requisition.min_clb_level,
            reasons
        )

        # Composite Weighted Score
        composite = (
            (noc_score * self.weights.noc) +
            (exp_score * self.weights.experience) +
            (skills_score * self.weights.skills) +
            (lang_score * self.weights.language)
        )
        composite = round(min(max(composite, 0.0), 100.0), 2)

        scores = ScoreBreakdown(
            noc_score=round(noc_score, 2),
            experience_score=round(exp_score, 2),
            skills_score=round(skills_score, 2),
            language_score=round(lang_score, 2),
            composite_score=composite
        )

        # Determine Qualification Status
        if composite >= 80.0 and exp_score >= 80.0:
            status = QualificationStatus.RECOMMENDED
            reasons.append("Meets and exceeds core benchmark qualifications.")
        elif composite >= 60.0:
            status = QualificationStatus.QUALIFIED_WITH_CONDITIONS
            reasons.append("Conditionally qualified; secondary interview or bridging assessment required.")
        else:
            status = QualificationStatus.REJECTED
            reasons.append("Below required composite matching threshold.")

        # Record into tamper-evident audit ledger
        audit_entry = self.audit_ledger.record_decision(
            candidate_id=candidate.id,
            requisition_id=requisition.id,
            status=status.value,
            composite_score=composite,
            payload_snapshot={
                "scores": {
                    "noc": scores.noc_score,
                    "experience": scores.experience_score,
                    "skills": scores.skills_score,
                    "language": scores.language_score,
                    "composite": scores.composite_score
                },
                "reasons": reasons
            }
        )

        return MatchResult(
            candidate_id=candidate.id,
            requisition_id=requisition.id,
            status=status,
            scores=scores,
            reasons=reasons,
            is_compliant=True,
            audit_hash=audit_entry.current_hash
        )

    def _compute_noc_score(self, cand_noc: str, target_noc: str, reasons: List[str]) -> float:
        clean_cand = str(cand_noc).strip()
        clean_target = str(target_noc).strip()

        if clean_cand == clean_target:
            return 100.0
        # Major unit group match (first 4 digits)
        if len(clean_cand) >= 4 and len(clean_target) >= 4 and clean_cand[:4] == clean_target[:4]:
            reasons.append(f"Minor NOC divergence: candidate NOC {clean_cand} shares unit group with {clean_target}.")
            return 80.0
        # Broad occupational group match (first 2 digits)
        if len(clean_cand) >= 2 and len(clean_target) >= 2 and clean_cand[:2] == clean_target[:2]:
            reasons.append(f"Broad NOC group match: {clean_cand} vs {clean_target}.")
            return 50.0

        reasons.append(f"NOC misalignment: {clean_cand} does not match {clean_target}.")
        return 0.0

    def _compute_experience_score(self, candidate_years: float, required_years: float, reasons: List[str]) -> float:
        if required_years <= 0:
            return 100.0
        ratio = candidate_years / required_years
        if ratio >= 1.0:
            # Exceeding experience caps at 100 with modest bonus factor
            bonus = min((ratio - 1.0) * 5.0, 10.0)
            return min(100.0, 95.0 + bonus)
        elif ratio >= 0.75:
            reasons.append(f"Candidate experience ({candidate_years}y) is slightly under required ({required_years}y).")
            return 75.0 * ratio
        else:
            reasons.append(f"Insufficient experience: {candidate_years}y provided, {required_years}y required.")
            return max(0.0, 50.0 * ratio)

    def _compute_skills_score(self, candidate_skills: List[str], required_skills: List[str], reasons: List[str]) -> float:
        if not required_skills:
            return 100.0

        cand_set: Set[str] = {s.strip().lower() for s in candidate_skills}
        req_set: Set[str] = {s.strip().lower() for s in required_skills}

        matched = cand_set.intersection(req_set)
        match_count = len(matched)
        req_count = len(req_set)

        missing = req_set - cand_set
        if missing:
            reasons.append(f"Missing required skills: {', '.join(sorted(missing))}.")

        return (match_count / req_count) * 100.0

    def _compute_language_score(self, candidate_clb: int, min_clb: int, reasons: List[str]) -> float:
        if min_clb <= 0:
            return 100.0

        if candidate_clb >= min_clb:
            bonus = min((candidate_clb - min_clb) * 5.0, 10.0)
            return min(100.0, 95.0 + bonus)
        else:
            deficit = min_clb - candidate_clb
            reasons.append(f"CLB level {candidate_clb} below minimum target {min_clb}.")
            return max(0.0, 100.0 - (deficit * 25.0))
