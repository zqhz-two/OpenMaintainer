from __future__ import annotations

import argparse
import json

from .agents import generate_docs, review_pr, suggest_tests, triage_issue
from .github_tools import load_payload


def main() -> None:
    parser = argparse.ArgumentParser(prog="openmaintainer")
    sub = parser.add_subparsers(dest="command", required=True)

    for cmd in ["run-issue", "run-pr", "run-docs"]:
        p = sub.add_parser(cmd)
        p.add_argument("--input", required=True, help="JSON payload path")

    args = parser.parse_args()
    payload = load_payload(args.input)

    if args.command == "run-issue":
        result = triage_issue(payload)
    elif args.command == "run-pr":
        review = review_pr(payload)
        tests = suggest_tests(payload)
        result = {"review": review.model_dump(), "tests": tests.model_dump()}
    else:
        result = generate_docs(payload)

    if hasattr(result, "model_dump"):
        output = result.model_dump()
    else:
        output = result

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
