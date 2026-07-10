-- Task 005 Stateful Tool Use — Database Schema
-- Runtime-private; agent never sees this file.

CREATE TABLE IF NOT EXISTS requests (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    submitter TEXT NOT NULL,
    amount REAL NOT NULL,
    department TEXT NOT NULL,
    description TEXT NOT NULL,
    existing_approvals TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending'
);

CREATE TABLE IF NOT EXISTS policies (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    full_text TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS request_policies (
    request_id TEXT NOT NULL,
    policy_id TEXT NOT NULL,
    PRIMARY KEY (request_id, policy_id),
    FOREIGN KEY (request_id) REFERENCES requests(id),
    FOREIGN KEY (policy_id) REFERENCES policies(id)
);

CREATE TABLE IF NOT EXISTS approval_chain (
    request_id TEXT NOT NULL,
    approver TEXT NOT NULL,
    approved INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (request_id, approver),
    FOREIGN KEY (request_id) REFERENCES requests(id)
);

CREATE TABLE IF NOT EXISTS action_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    tool TEXT NOT NULL,
    request_id TEXT,
    args TEXT NOT NULL,
    success INTEGER NOT NULL,
    error TEXT,
    applicable_policy_ids TEXT,
    policy_ids_read_before_action TEXT,
    policy_precondition_satisfied INTEGER
);
