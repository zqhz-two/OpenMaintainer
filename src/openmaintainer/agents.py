from __future__ import annotations

from .schemas import DocsResult, IssueTriageResult, PRReviewResult, TestSuggestionResult


def triage_issue(payload: dict) -> IssueTriageResult:
    title = (payload.get("title") or "").lower()
    body = (payload.get("body") or "").lower()

    issue_type = "question"
    if any(k in title + body for k in ["bug", "error", "crash", "exception"]):
        issue_type = "bug"
    elif any(k in title + body for k in ["feature", "enhancement", "proposal"]):
        issue_type = "feature"

    priority = "p2"
    if "security" in title + body or "data loss" in title + body:
        priority = "p0"
    elif "production" in title + body or "blocking" in title + body:
        priority = "p1"

    missing = []
    if "reproduce" not in body and "复现" not in body:
        missing.append("缺少复现步骤")
    if "expected" not in body and "期望" not in body:
        missing.append("缺少期望行为说明")

    recommendation = "请维护者先补充标签并确认影响范围。"
    return IssueTriageResult(
        issue_type=issue_type,
        priority=priority,
        missing_information=missing,
        recommendation=recommendation,
    )


def review_pr(payload: dict) -> PRReviewResult:
    changed_files = payload.get("changed_files", [])
    ci_status = payload.get("ci_status", "unknown")
    risky = [f for f in changed_files if "auth" in f or "permission" in f or "db" in f]

    risk_level = "low"
    if len(risky) >= 2:
        risk_level = "high"
    elif risky:
        risk_level = "medium"

    blocking = []
    if ci_status != "success":
        blocking.append("CI 未通过，请先修复失败任务")

    merge_recommendation = "approve" if not blocking else "request_changes"
    return PRReviewResult(
        summary=f"变更文件数: {len(changed_files)}，高风险文件数: {len(risky)}。",
        risk_level=risk_level,
        blocking_issues=blocking,
        merge_recommendation=merge_recommendation,
    )


def suggest_tests(payload: dict) -> TestSuggestionResult:
    changed_files = payload.get("changed_files", [])
    unit_tests = [f"为 {f} 增加关键函数单元测试" for f in changed_files[:5]]
    integration_tests = ["验证主流程 API / CLI 在典型输入下可运行"]
    regression_tests = ["针对本次修复场景补充回归测试，防止问题重现"]
    return TestSuggestionResult(
        unit_tests=unit_tests,
        integration_tests=integration_tests,
        regression_tests=regression_tests,
    )


def generate_docs(payload: dict) -> DocsResult:
    features = payload.get("features", [])
    fixes = payload.get("fixes", [])
    readme = [f"新增功能：{item}" for item in features]
    changelog = [f"feat: {item}" for item in features] + [f"fix: {item}" for item in fixes]
    return DocsResult(readme_updates=readme, changelog_entries=changelog)
