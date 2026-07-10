#!/usr/bin/env python3
"""Task 005 Canonical Tool Service — Procurement Approval System.

Stdlib only (Python 3.10+). CLI entrypoint with per-run_id isolated state.

State: runtime-state/<run_id>/state.db (SQLite)
Audit: runtime-state/<run_id>/action-log.jsonl

Interface: python3 tool_api.py --run-id <id> <command> [args...]
Returns JSON to stdout. Errors to stderr.

Service records policy-read preconditions and enforces state machine
transitions. It does NOT encode expected final states or business decisions.
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

SERVICE_DIR = Path(__file__).resolve().parent
PRIVATE_DIR = SERVICE_DIR.parent / "private"
SCHEMA_PATH = PRIVATE_DIR / "schema.sql"
SEED_PATH = PRIVATE_DIR / "seed.sql"
RUNTIME_STATE_DIR = SERVICE_DIR / "runtime-state"

TERMINAL_STATES = {"approved", "rejected", "escalated"}

ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "pending": {"information_requested", "approved", "rejected", "escalated"},
    "information_requested": {"approved", "rejected", "escalated"},
}

MUTATING_TOOLS = {"request_information", "approve_request", "reject_request", "escalate_request"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _resolve_run_id(args_run_id: str | None) -> str:
    env_id = os.environ.get("AGENT_EVAL_RUN_ID", "")
    run_id = args_run_id or env_id
    if not run_id:
        print(json.dumps({"error": "No run_id provided. Use --run-id or set AGENT_EVAL_RUN_ID."}),
              file=sys.stderr)
        sys.exit(1)
    return run_id


def _db_path(run_id: str) -> Path:
    return RUNTIME_STATE_DIR / run_id / "state.db"


def _log_path(run_id: str) -> Path:
    return RUNTIME_STATE_DIR / run_id / "action-log.jsonl"


def _init_db(run_id: str) -> sqlite3.Connection:
    db_path = _db_path(run_id)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")

    # Check if already initialized by looking for the requests table
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='requests'"
    )
    if cur.fetchone() is None:
        _run_sql_file(conn, SCHEMA_PATH)
        _run_sql_file(conn, SEED_PATH)
        conn.commit()

    return conn


def _run_sql_file(conn: sqlite3.Connection, path: Path) -> None:
    sql = path.read_text(encoding="utf-8")
    conn.executescript(sql)


# ---------------------------------------------------------------------------
# Audit log
# ---------------------------------------------------------------------------

def _log_action(
    conn: sqlite3.Connection,
    run_id: str,
    tool: str,
    request_id: str | None,
    args_dict: dict,
    success: bool,
    error: str | None = None,
) -> None:
    """Write to action-log.jsonl and action_log table."""
    # Determine applicable policies and read status for mutating tools
    applicable_policy_ids: list[str] = []
    policy_ids_read_before: list[str] = []
    precondition_satisfied: bool | None = None

    if tool in MUTATING_TOOLS and request_id:
        applicable_policy_ids = _get_applicable_policy_ids(conn, request_id)
        policy_ids_read_before = _get_policies_read_this_session(conn, request_id)
        applicable_set = set(applicable_policy_ids)
        read_set = set(policy_ids_read_before)
        precondition_satisfied = applicable_set.issubset(read_set)

    # DB log
    conn.execute(
        """INSERT INTO action_log
           (timestamp, tool, request_id, args, success, error,
            applicable_policy_ids, policy_ids_read_before_action,
            policy_precondition_satisfied)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            _now_iso(),
            tool,
            request_id,
            json.dumps(args_dict),
            1 if success else 0,
            error,
            json.dumps(applicable_policy_ids) if applicable_policy_ids else None,
            json.dumps(policy_ids_read_before) if policy_ids_read_before else None,
            precondition_satisfied,
        ),
    )
    conn.commit()

    # JSONL log
    entry = {
        "timestamp": _now_iso(),
        "tool": tool,
        "request_id": request_id,
        "args": args_dict,
        "success": success,
    }
    if error:
        entry["error"] = error
    if applicable_policy_ids:
        entry["applicable_policy_ids"] = applicable_policy_ids
    if policy_ids_read_before:
        entry["policy_ids_read_before_action"] = policy_ids_read_before
    if precondition_satisfied is not None:
        entry["policy_precondition_satisfied"] = precondition_satisfied

    log_path = _log_path(run_id)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")


def _get_applicable_policy_ids(conn: sqlite3.Connection, request_id: str) -> list[str]:
    rows = conn.execute(
        "SELECT policy_id FROM request_policies WHERE request_id = ?",
        (request_id,),
    ).fetchall()
    return sorted(r["policy_id"] for r in rows)


def _get_policies_read_this_session(
    conn: sqlite3.Connection, request_id: str
) -> list[str]:
    """Return policy IDs that have been read this session via get_policy.

    A policy read once applies to all requests governed by it for the
    remainder of the run.
    """
    rows = conn.execute(
        "SELECT DISTINCT args FROM action_log WHERE tool = 'get_policy' AND success = 1"
    ).fetchall()
    read_ids: set[str] = set()
    for r in rows:
        try:
            args = json.loads(r["args"])
            pid = args.get("policy_id", "")
            if pid:
                read_ids.add(pid)
        except (json.JSONDecodeError, TypeError):
            pass
    return sorted(read_ids)


# ---------------------------------------------------------------------------
# State machine helper
# ---------------------------------------------------------------------------

def _check_transition(conn: sqlite3.Connection, request_id: str, target: str) -> None:
    """Raise ValueError if transition is invalid."""
    row = conn.execute(
        "SELECT status FROM requests WHERE id = ?", (request_id,)
    ).fetchone()
    if row is None:
        raise ValueError(f"Request '{request_id}' not found")

    current = row["status"]
    if current in TERMINAL_STATES:
        raise ValueError(
            f"Request '{request_id}' is in terminal state '{current}'. "
            f"No further operations allowed."
        )

    allowed = ALLOWED_TRANSITIONS.get(current, set())
    if target not in allowed:
        raise ValueError(
            f"Cannot transition '{request_id}' from '{current}' to '{target}'. "
            f"Allowed transitions: {sorted(allowed)}"
        )


# ---------------------------------------------------------------------------
# Read tools (no state modification)
# ---------------------------------------------------------------------------

def cmd_list_requests(conn: sqlite3.Connection) -> dict:
    rows = conn.execute(
        "SELECT id, title, submitter, amount, department, status FROM requests"
    ).fetchall()
    return {
        "requests": [
            {
                "request_id": r["id"],
                "title": r["title"],
                "submitter": r["submitter"],
                "amount": r["amount"],
                "department": r["department"],
                "status": r["status"],
            }
            for r in rows
        ]
    }


def cmd_get_request(conn: sqlite3.Connection, request_id: str) -> dict:
    row = conn.execute(
        "SELECT * FROM requests WHERE id = ?", (request_id,)
    ).fetchone()
    if row is None:
        return {"error": f"Request '{request_id}' not found"}

    # Get approval chain
    approvals = conn.execute(
        "SELECT approver, approved FROM approval_chain WHERE request_id = ?",
        (request_id,),
    ).fetchall()

    # Get applicable policies
    policy_ids = _get_applicable_policy_ids(conn, request_id)

    return {
        "request_id": row["id"],
        "title": row["title"],
        "submitter": row["submitter"],
        "amount": row["amount"],
        "department": row["department"],
        "description": row["description"],
        "existing_approvals": json.loads(row["existing_approvals"]),
        "status": row["status"],
        "approval_chain": [
            {"approver": a["approver"], "approved": bool(a["approved"])}
            for a in approvals
        ],
        "applicable_policy_ids": policy_ids,
    }


def cmd_list_policies(conn: sqlite3.Connection) -> dict:
    rows = conn.execute("SELECT id, title FROM policies").fetchall()
    return {
        "policies": [
            {"policy_id": r["id"], "title": r["title"]} for r in rows
        ]
    }


def cmd_get_policy(conn: sqlite3.Connection, policy_id: str) -> dict:
    row = conn.execute(
        "SELECT * FROM policies WHERE id = ?", (policy_id,)
    ).fetchone()
    if row is None:
        return {"error": f"Policy '{policy_id}' not found"}
    return {
        "policy_id": row["id"],
        "title": row["title"],
        "full_text": row["full_text"],
    }


def cmd_get_approval_status(conn: sqlite3.Connection, request_id: str) -> dict:
    row = conn.execute(
        "SELECT id, status FROM requests WHERE id = ?", (request_id,)
    ).fetchone()
    if row is None:
        return {"error": f"Request '{request_id}' not found"}

    approvals = conn.execute(
        "SELECT approver, approved FROM approval_chain WHERE request_id = ?",
        (request_id,),
    ).fetchall()

    return {
        "request_id": row["id"],
        "status": row["status"],
        "approval_chain": [
            {"approver": a["approver"], "approved": bool(a["approved"])}
            for a in approvals
        ],
    }


def cmd_get_final_state(conn: sqlite3.Connection) -> dict:
    rows = conn.execute("SELECT id, status FROM requests").fetchall()
    return {
        "final_state": [
            {"request_id": r["id"], "status": r["status"]} for r in rows
        ]
    }


def cmd_get_action_log(conn: sqlite3.Connection, run_id: str) -> dict:
    log_path = _log_path(run_id)
    entries: list[dict] = []
    if log_path.exists():
        for line in log_path.read_text(encoding="utf-8").strip().split("\n"):
            if line.strip():
                entries.append(json.loads(line))
    return {"action_log": entries}


# ---------------------------------------------------------------------------
# Mutating tools
# ---------------------------------------------------------------------------

def cmd_request_information(
    conn: sqlite3.Connection, run_id: str, request_id: str, field: str
) -> dict:
    _check_transition(conn, request_id, "information_requested")
    conn.execute(
        "UPDATE requests SET status = 'information_requested' WHERE id = ?",
        (request_id,),
    )
    conn.commit()
    return {
        "request_id": request_id,
        "action": "information_requested",
        "field": field,
        "status": "information_requested",
        "message": f"Information requested for field '{field}'. Request status set to information_requested.",
    }


def cmd_approve_request(
    conn: sqlite3.Connection, run_id: str, request_id: str
) -> dict:
    _check_transition(conn, request_id, "approved")
    conn.execute(
        "UPDATE requests SET status = 'approved' WHERE id = ?",
        (request_id,),
    )
    conn.commit()
    return {
        "request_id": request_id,
        "action": "approved",
        "status": "approved",
        "message": f"Request '{request_id}' has been approved.",
    }


def cmd_reject_request(
    conn: sqlite3.Connection, run_id: str, request_id: str, reason: str
) -> dict:
    if not reason or not reason.strip():
        raise ValueError("reject_request requires a non-empty reason")
    _check_transition(conn, request_id, "rejected")
    conn.execute(
        "UPDATE requests SET status = 'rejected' WHERE id = ?",
        (request_id,),
    )
    conn.commit()
    return {
        "request_id": request_id,
        "action": "rejected",
        "reason": reason,
        "status": "rejected",
        "message": f"Request '{request_id}' has been rejected. Reason: {reason}",
    }


def cmd_escalate_request(
    conn: sqlite3.Connection, run_id: str, request_id: str, body: str
) -> dict:
    if not body or not body.strip():
        raise ValueError("escalate_request requires a non-empty escalation body")
    _check_transition(conn, request_id, "escalated")
    conn.execute(
        "UPDATE requests SET status = 'escalated' WHERE id = ?",
        (request_id,),
    )
    conn.commit()
    return {
        "request_id": request_id,
        "action": "escalated",
        "escalation_body": body,
        "status": "escalated",
        "message": f"Request '{request_id}' has been escalated to {body}.",
    }


# ---------------------------------------------------------------------------
# Admin command (NOT agent-visible)
# ---------------------------------------------------------------------------

def cmd_reset(conn: sqlite3.Connection) -> dict:
    """Reinitialize database from seed. Private admin command."""
    conn.execute("DELETE FROM action_log")
    conn.execute("DELETE FROM approval_chain")
    conn.execute("DELETE FROM request_policies")
    conn.execute("DELETE FROM requests")
    conn.execute("DELETE FROM policies")
    _run_sql_file(conn, SEED_PATH)
    conn.commit()
    return {"reset": "ok", "message": "Database reinitialized from seed."}


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

COMMANDS: dict[str, dict] = {
    "list_requests":       {"mutating": False, "args": 0, "fn": lambda conn, rid: cmd_list_requests(conn)},
    "get_request":         {"mutating": False, "args": 1, "fn": lambda conn, rid, a1: cmd_get_request(conn, a1)},
    "list_policies":       {"mutating": False, "args": 0, "fn": lambda conn, rid: cmd_list_policies(conn)},
    "get_policy":          {"mutating": False, "args": 1, "fn": lambda conn, rid, a1: cmd_get_policy(conn, a1)},
    "get_approval_status": {"mutating": False, "args": 1, "fn": lambda conn, rid, a1: cmd_get_approval_status(conn, a1)},
    "get_final_state":     {"mutating": False, "args": 0, "fn": lambda conn, rid: cmd_get_final_state(conn)},
    "get_action_log":      {"mutating": False, "args": 0, "fn": lambda conn, rid: cmd_get_action_log(conn, rid)},
    "request_information": {"mutating": True,  "args": 2, "fn": lambda conn, rid, a1, a2: cmd_request_information(conn, rid, a1, a2)},
    "approve_request":     {"mutating": True,  "args": 1, "fn": lambda conn, rid, a1: cmd_approve_request(conn, rid, a1)},
    "reject_request":      {"mutating": True,  "args": 2, "fn": lambda conn, rid, a1, a2: cmd_reject_request(conn, rid, a1, a2)},
    "escalate_request":    {"mutating": True,  "args": 2, "fn": lambda conn, rid, a1, a2: cmd_escalate_request(conn, rid, a1, a2)},
    "reset":               {"mutating": True,  "args": 0, "fn": lambda conn, rid: cmd_reset(conn)},
}


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="tool_api.py",
        description="Task 005 Canonical Tool Service",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--run-id", default=None, help="Run identifier (or set AGENT_EVAL_RUN_ID)")
    parser.add_argument("command", nargs="?", help="Tool command")
    parser.add_argument("args", nargs="*", help="Positional arguments for the command")

    parsed = parser.parse_args()

    if not parsed.command:
        parser.print_help()
        sys.exit(1)

    command = parsed.command
    if command not in COMMANDS:
        print(json.dumps({"error": f"Unknown command: '{command}'"}), file=sys.stderr)
        sys.exit(1)

    run_id = _resolve_run_id(parsed.run_id)
    cmd_def = COMMANDS[command]
    expected_args = cmd_def["args"]

    if len(parsed.args) != expected_args:
        print(json.dumps({
            "error": f"'{command}' expects {expected_args} argument(s), got {len(parsed.args)}"
        }), file=sys.stderr)
        sys.exit(1)

    conn = _init_db(run_id)
    tool_args: dict = {}
    request_id: str | None = None

    if command == "reset":
        # reset applies to all requests; no per-request ID
        pass
    elif command in ("list_requests", "list_policies", "get_final_state", "get_action_log"):
        pass
    elif command == "get_policy":
        tool_args = {"policy_id": parsed.args[0]}
    else:
        # Commands that take a request_id as first arg
        request_id = parsed.args[0]
        tool_args = {"request_id": request_id}
        if command == "request_information":
            tool_args["field"] = parsed.args[1]
        elif command == "reject_request":
            tool_args["reason"] = parsed.args[1]
        elif command == "escalate_request":
            tool_args["body"] = parsed.args[1]

    success = True
    error_msg: str | None = None
    result: dict | None = None

    try:
        if command == "reset":
            result = cmd_reset(conn)
        elif command == "get_request":
            result = cmd_get_request(conn, parsed.args[0])
        elif command == "get_policy":
            result = cmd_get_policy(conn, parsed.args[0])
        elif command == "get_approval_status":
            result = cmd_get_approval_status(conn, parsed.args[0])
        elif command == "list_requests":
            result = cmd_list_requests(conn)
        elif command == "list_policies":
            result = cmd_list_policies(conn)
        elif command == "get_final_state":
            result = cmd_get_final_state(conn)
        elif command == "get_action_log":
            result = cmd_get_action_log(conn, run_id)
        elif command == "request_information":
            result = cmd_request_information(conn, run_id, parsed.args[0], parsed.args[1])
        elif command == "approve_request":
            result = cmd_approve_request(conn, run_id, parsed.args[0])
        elif command == "reject_request":
            result = cmd_reject_request(conn, run_id, parsed.args[0], parsed.args[1])
        elif command == "escalate_request":
            result = cmd_escalate_request(conn, run_id, parsed.args[0], parsed.args[1])
    except ValueError as exc:
        success = False
        error_msg = str(exc)
        result = {"error": error_msg}

    # Log action (include reset in action log for audit trail)
    _log_action(conn, run_id, command, request_id, tool_args, success, error_msg)
    conn.close()

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
