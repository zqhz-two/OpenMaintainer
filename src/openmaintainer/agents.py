from __future__ import annotations

from .schemas import DocsResult, IssueTriageResult, PRReviewResult, TestSuggestionResult


BUG_KEYWORDS = ("bug", "error", "crash", "exception", "fail")
FEATURE_KEYWORDS = ("feature", "enhancement", "proposal", "request")
CRITICAL_KEYWORDS = ("security", "data loss", "泄露", "丢失")
HIGH_KEYWORDS = ("production", "blocking", "线上", "阻塞")
RISKY_PATH_HINTS = ("auth", "permission", "db", "migration", "payment")


def _contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    return any(keyword in text for keyword in keywords)


def triage_issue(payload: dict) -> IssueTriageResult:
    title = (payload.get("title") or "").lower()
    body = (payload.get("body") or "").lower()
    merged = f"{title}\n{body}"

    issue_type = "question"
    if _contains_any(merged, BUG_KEYWORDS):
        issue_type = "bug"
    elif _contains_any(merged, FEATURE_KEYWORDS):
        issue_type = "feature"

    priority = "p2"
    if _contains_any(merged, CRITICAL_KEYWORDS):
        priority = "p0"
    elif _contains_any(merged, HIGH_KEYWORDS):
        priority = "p1"

    missing_information = []
    if "reproduce" not in merged and "复现" not in merged:
        missing_information.append("缺少复现步骤")
    if "expected" not in merged and "期望" not in merged:
        missing_information.append("缺少期望行为说明")

    recommendation = "请维护者补充标签、确认影响范围，并按优先级进入迭代。"
    return IssueTriageResult(issue_type, priority, missing_information, recommendation)


def review_pr(payload: dict) -> PRReviewResult:
    changed_files = payload.get("changed_files", [])
    ci_status = payload.get("ci_status", "unknown")
    risky = [f for f in changed_files if _contains_any(f.lower(), RISKY_PATH_HINTS)]

    risk_level = "low"
    if len(risky) >= 2:
        risk_level = "high"
    elif risky:
        risk_level = "medium"

    blocking_issues = []
    if ci_status != "success":
        blocking_issues.append("CI 未通过，请先修复失败任务")

    recommendation = "approve" if not blocking_issues else "request_changes"
    return PRReviewResult(
        summary=f"变更文件数: {len(changed_files)}，高风险文件数: {len(risky)}。",
        risk_level=risk_level,
        blocking_issues=blocking_issues,
        merge_recommendation=recommendation,
    )


def suggest_tests(payload: dict) -> TestSuggestionResult:
    changed_files = payload.get("changed_files", [])
    unit_tests = [f"为 {file} 增加关键函数单元测试" for file in changed_files[:5]]
    if not unit_tests:
        unit_tests = ["补充核心模块的最小单元测试（空变更保护）"]

    integration_tests = ["验证主流程 API / CLI 在典型输入下可运行"]
    regression_tests = ["针对本次修复场景补充回归测试，防止问题重现"]
    return TestSuggestionResult(unit_tests, integration_tests, regression_tests)


def generate_docs(payload: dict) -> DocsResult:
    features = payload.get("features", [])
    fixes = payload.get("fixes", [])
    readme_updates = [f"新增功能：{item}" for item in features]
    changelog_entries = [f"feat: {item}" for item in features] + [f"fix: {item}" for item in fixes]
    return DocsResult(readme_updates, changelog_entries)
