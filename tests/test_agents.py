from openmaintainer.agents import review_pr, triage_issue


def test_issue_triage_priority():
    result = triage_issue({"title": "Security bug", "body": "复现: ..."})
    assert result.priority == "p0"
    assert result.issue_type == "bug"


def test_pr_review_blocks_failed_ci():
    result = review_pr({"changed_files": ["src/auth/x.py"], "ci_status": "failed"})
    assert result.merge_recommendation == "request_changes"
    assert result.risk_level in {"medium", "high"}
