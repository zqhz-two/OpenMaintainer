from __future__ import annotations

import argparse
import json
from .agents import generate_docs, review_pr, suggest_tests, triage_issue
from .github_tools import load_payload
def main() -> None:
    parser = argparse.ArgumentParser(prog="openmaintainer")
    sub = parser.add_subparsers(dest="command", required=True)

    for cmd in ["run-issue", "run-pr", "run-docs"]:
    args = parser.parse_args()
    payload = load_payload(args.input)

    if args.command == "run-issue":
if __name__ == "__main__":
    main()
