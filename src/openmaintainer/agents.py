from __future__ import annotations

from .schemas import DocsResult, IssueTriageResult, PRReviewResult, TestSuggestionResult
def review_pr(payload: dict) -> PRReviewResult:
    changed_files = payload.get("changed_files", [])
    ci_status = payload.get("ci_status", "unknown")
    risk_level = "low"
    if len(risky) >= 2:
        risk_level = "high"
    elif risky:
        risk_level = "medium"
def suggest_tests(payload: dict) -> TestSuggestionResult:
    changed_files = payload.get("changed_files", [])
def generate_docs(payload: dict) -> DocsResult:
    features = payload.get("features", [])
    fixes = payload.get("fixes", [])