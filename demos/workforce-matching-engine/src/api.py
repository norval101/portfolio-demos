"""
Lightweight REST API service for Workforce Matching Engine.
Runnable with standard library Python without external dependencies.
"""

import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any

from .models import CandidateProfile, JobRequisition
from .engine import WorkforceMatchingEngine
from .audit import ComplianceAuditLedger

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

_ENGINE = WorkforceMatchingEngine()


class WorkforceAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: Dict[str, Any]):
        response_bytes = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(response_bytes)

    def do_OPTIONS(self):
        self._send_json(200, {"status": "ok"})

    def do_GET(self):
        if self.path in ("/health", "/healthz"):
            self._send_json(200, {
                "status": "healthy",
                "service": "workforce-matching-engine",
                "version": "1.0.0",
                "audit_ledger_length": _ENGINE.audit_ledger.length,
                "audit_integrity": _ENGINE.audit_ledger.verify_integrity()
            })
        elif self.path == "/api/v1/audit/integrity":
            is_valid = _ENGINE.audit_ledger.verify_integrity()
            self._send_json(200, {
                "audit_chain_valid": is_valid,
                "total_records": _ENGINE.audit_ledger.length
            })
        else:
            self._send_json(404, {"error": "Not Found", "path": self.path})

    def do_POST(self):
        if self.path == "/api/v1/match":
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length).decode("utf-8")
                payload = json.loads(body)

                cand_data = payload.get("candidate", {})
                req_data = payload.get("requisition", {})

                candidate = CandidateProfile(
                    id=cand_data.get("id", "cand-anon"),
                    name=cand_data.get("name", "Unnamed Candidate"),
                    noc_code=cand_data.get("noc_code", ""),
                    years_experience=float(cand_data.get("years_experience", 0)),
                    skills=cand_data.get("skills", []),
                    clb_level=int(cand_data.get("clb_level", 4)),
                    compliance_cleared=bool(cand_data.get("compliance_cleared", True))
                )

                requisition = JobRequisition(
                    id=req_data.get("id", "req-anon"),
                    title=req_data.get("title", "Job Position"),
                    target_noc=req_data.get("target_noc", ""),
                    min_experience_years=float(req_data.get("min_experience_years", 0)),
                    required_skills=req_data.get("required_skills", []),
                    min_clb_level=int(req_data.get("min_clb_level", 7)),
                    compliance_required=bool(req_data.get("compliance_required", True))
                )

                result = _ENGINE.evaluate(candidate, requisition)

                self._send_json(200, {
                    "candidate_id": result.candidate_id,
                    "requisition_id": result.requisition_id,
                    "status": result.status.value,
                    "scores": {
                        "noc": result.scores.noc_score,
                        "experience": result.scores.experience_score,
                        "skills": result.scores.skills_score,
                        "language": result.scores.language_score,
                        "composite": result.scores.composite_score
                    },
                    "reasons": result.reasons,
                    "is_compliant": result.is_compliant,
                    "audit_hash": result.audit_hash,
                    "evaluated_at": result.evaluated_at
                })

            except json.JSONDecodeError:
                self._send_json(400, {"error": "Invalid JSON payload"})
            except Exception as e:
                logging.exception("Error processing matching request")
                self._send_json(500, {"error": str(e)})
        else:
            self._send_json(404, {"error": "Endpoint not found"})


def run_server(port: int = 8080):
    server = HTTPServer(("0.0.0.0", port), WorkforceAPIHandler)
    logging.info("Workforce Matching API server started at http://localhost:%d", port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        logging.info("Server stopped.")


if __name__ == "__main__":
    run_server()
