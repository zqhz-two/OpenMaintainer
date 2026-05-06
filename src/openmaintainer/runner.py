from __future__ import annotations

import argparse
import json
from pathlib import Path

from .agents import generate_docs, review_pr, suggest_tests, triage_issue
from .github_tools import load_payload


def _render_markdown(command: str, output: dict) -> str:
    if command == "run-issue":
        return (
            f"### Issue Triage\n"
            f"- type: `{output['issue_type']}`\n"
            f"- priority: `{output['priority']}`\n"
            f"- missing: {', '.join(output['missing_information']) or 'none'}\n"
            f"- recommendation: {output['recommendation']}\n"
        )
    if command == "run-pr":
        review = output["review"]
        tests = output["tests"]
        return (
            "### PR Review\n"
            f"- risk: `{review['risk_level']}`\n"
            f"- summary: {review['summary']}\n"
            f"- merge: `{review['merge_recommendation']}`\n\n"
            "### Test Suggestions\n"
            + "\n".join([f"- {item}" for item in tests["unit_tests"] + tests["integration_tests"] + tests["regression_tests"]])
        )
    return "### Docs Draft\n" + "\n".join([f"- {item}" for item in output["readme_updates"] + output["changelog_entries"]])


def main() -> None:
    parser = argparse.ArgumentParser(prog="openmaintainer")
    sub = parser.add_subparsers(dest="command", required=True)

    for cmd in ["run-issue", "run-pr", "run-docs"]:
        command_parser = sub.add_parser(cmd)
        command_parser.add_argument("--input", required=True, help="JSON payload path")
        command_parser.add_argument("--format", choices=["json", "markdown"], default="json")
        command_parser.add_argument("--output", help="output file path")

    args = parser.parse_args()
    payload = load_payload(args.input)

    if args.command == "run-issue":
        result = triage_issue(payload).model_dump()
    elif args.command == "run-pr":
        result = {
            "review": review_pr(payload).model_dump(),
            "tests": suggest_tests(payload).model_dump(),
        }
    else:
        result = generate_docs(payload).model_dump()

    rendered = json.dumps(result, ensure_ascii=False, indent=2) if args.format == "json" else _render_markdown(args.command, result)

    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
