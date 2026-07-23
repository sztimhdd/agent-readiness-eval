#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


TOOL_API = Path(
    os.environ.get(
        "AGENT_EVAL_TASK005_TOOL_API",
        Path(__file__).resolve().parents[1] / "tasks" / "task-005" / "environment" / "service" / "tool_api.py",
    ),
)
ARG_NAMES = {
    "list_requests": [],
    "get_request": ["request_id"],
    "list_policies": [],
    "get_policy": ["policy_id"],
    "get_approval_status": ["request_id"],
    "request_information": ["request_id", "field"],
    "approve_request": ["request_id"],
    "reject_request": ["request_id", "reason"],
    "escalate_request": ["request_id", "body"],
}


def _read_request():
    raw = sys.argv[1] if len(sys.argv) >= 2 else sys.stdin.read()
    try:
        request = json.loads(raw)
    except json.JSONDecodeError:
        print(json.dumps({"error": "invalid JSON input"}))
        sys.exit(1)
    if not isinstance(request, dict):
        print(json.dumps({"error": "input must be a JSON object"}))
        sys.exit(1)
    return request


def main() -> None:
    request = _read_request()
    operation = request.get("operation")
    if not isinstance(operation, str) or not operation:
        print(json.dumps({"error": "missing operation"}))
        sys.exit(1)
    if operation not in ARG_NAMES:
        print(json.dumps({"error": f"unknown operation: {operation}"}))
        sys.exit(1)

    run_id = request.get("run_id", "default")
    if not isinstance(run_id, str) or not run_id:
        print(json.dumps({"error": "run_id must be a non-empty string"}))
        sys.exit(1)

    args = []
    for name in ARG_NAMES[operation]:
        value = request.get(name)
        if not isinstance(value, str) or not value:
            print(json.dumps({"error": f"{name} must be a non-empty string"}))
            sys.exit(1)
        args.append(value)

    result = subprocess.run(
        [sys.executable, str(TOOL_API), "--run-id", run_id, operation, *args],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="")
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
