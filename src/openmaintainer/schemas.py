from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Literal


@dataclass
class IssueTriageResult:
    issue_type: Literal["bug", "feature", "question", "docs", "other"]
    priority: Literal["p0", "p1", "p2", "p3"]
    missing_information: list[str] = field(default_factory=list)
    recommendation: str = ""

    def model_dump(self) -> dict:
        return asdict(self)


@dataclass
class PRReviewResult:
    summary: str
    risk_level: Literal["low", "medium", "high"]
    blocking_issues: list[str] = field(default_factory=list)
    merge_recommendation: Literal["approve", "request_changes", "comment"] = "comment"

    def model_dump(self) -> dict:
        return asdict(self)


@dataclass
class TestSuggestionResult:
    unit_tests: list[str] = field(default_factory=list)
    integration_tests: list[str] = field(default_factory=list)
    regression_tests: list[str] = field(default_factory=list)

    def model_dump(self) -> dict:
        return asdict(self)


@dataclass
class DocsResult:
    readme_updates: list[str] = field(default_factory=list)
    changelog_entries: list[str] = field(default_factory=list)

    def model_dump(self) -> dict:
        return asdict(self)
