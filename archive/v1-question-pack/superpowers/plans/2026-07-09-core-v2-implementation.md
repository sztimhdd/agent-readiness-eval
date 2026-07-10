# Agent Readiness Eval Core v2.0 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan phase-by-phase.

**Goal:** Upgrade v1 question-pack to Agent Readiness Eval Core v2.0: six tasks across four-layer architecture, distribution builder, contract tests, archive, docs, and real OpenCode UAT.

**Architecture:** Four-layer separation (Agent-Visible / Controlled Runtime / Harness Adapter / Evaluator-Only). Distribution contract enforced by `scripts/build-distribution.py`. Tasks 001-003 are static file upgrades; tasks 004-006 introduce runnable environments.

**Tech Stack:** Python 3.10+ stdlib, SQLite3, YAML, JSON, Markdown.

## Global Constraints

- No push, no force-push, no credential changes
- All commits atomic, conventional format
- TDD: test before production code for every behavior change
- Distribution builder enforces evaluator-only exclusion from agent package
- Archive v1 before modifying any existing task content
- `dist/` directory gitignored
- Contract tests must pass after every phase
- LSP diagnostics clean on all changed files

---

## Phase 0: Preflight

**Status:** ✅ COMPLETE

- [x] Git status verified: main branch, 12 ahead of origin
- [x] `.gitignore` updated: added `.omo/`, `dist/`
- [x] `opencode.json` committed (project-level config, no secrets)
- [x] Baseline tests: 7/7 pass
- [x] Branch `core-v2-implementation` created

---

## Phase 1: Archive v1 + Rename + Core Infrastructure

### Task 1.1: Archive v1

**Files:**
- Create: `archive/v1-question-pack/` (copies of v1 assets)
- Create: git tag `v1.0-question-pack-pilot`

**Steps:**
- [ ] Create git tag `v1.0-question-pack-pilot` on current HEAD
- [ ] `mkdir -p archive/v1-question-pack/`
- [ ] Copy v1 skill.json, SKILL.md, README.md, tasks/ (snapshot), templates/, docs/ to archive/
- [ ] Create `archive/v1-question-pack/ARCHIVE-README.md` explaining this is read-only
- [ ] Commit: `chore: archive v1 question-pack and tag v1.0-question-pack-pilot`

### Task 1.2: Rename docs and test files

**Files:**
- Rename: `docs/PRD_v3.md` → `docs/PRD_core_v2.md`
- Rename: `docs/TDD_v3.md` → `docs/TDD_core_v2.md`
- Rename: `tests/test_v3_contract.py` → `tests/test_core_v2_contract.py`

**Steps:**
- [ ] `git mv docs/PRD_v3.md docs/PRD_core_v2.md`
- [ ] `git mv docs/TDD_v3.md docs/TDD_core_v2.md`
- [ ] `git mv tests/test_v3_contract.py tests/test_core_v2_contract.py`
- [ ] Update internal references in renamed files
- [ ] Commit: `refactor: rename v3→core_v2 (PRD, TDD, contract tests)`

### Task 1.3: Create distribution contract

**Files:**
- Create: `contracts/distribution-contract.yaml`

**Content:** Exact YAML from spec §2.5

**Steps:**
- [ ] `mkdir -p contracts/`
- [ ] Write `distribution-contract.yaml` per spec §2.5
- [ ] Commit: `feat: add distribution contract`

### Task 1.4: Create distribution builder

**Files:**
- Create: `scripts/build-distribution.py`

**Interface:**
```bash
python3 scripts/build-distribution.py --target agent --output dist/agent-package
python3 scripts/build-distribution.py --target runtime --task task-004 --output dist/runtime-task-004
python3 scripts/build-distribution.py --target evaluator --output dist/evaluator-package
```

**Requirements:**
- Reads `contracts/distribution-contract.yaml`
- Rejects unclassified files
- Outputs `package-manifest.json` with hashes
- Deterministic from same git revision
- Default-excludes: `archive/`, `runs/`, `.worktrees/`, `.superpowers/`, `__pycache__/`, `*.pyc`, `.DS_Store`

**Steps:**
- [ ] Write `scripts/build-distribution.py` (Python 3 stdlib only)
- [ ] Write failing contract test for distribution builder
- [ ] Implement builder
- [ ] Verify tests pass
- [ ] Commit: `feat: add distribution builder`

### Task 1.5: Update skill.json to v2 structure

**Files:**
- Modify: `skill.json`

**Change:** From bare string task IDs to structured task objects per spec §3.2

**Steps:**
- [ ] Rewrite `skill.json` with `suite_version: "2.0.0"` and structured task objects
- [ ] Commit: `feat: upgrade skill.json to v2 structured task catalog`

### Task 1.6: Update templates

**Files:**
- Modify: `templates/run-metadata.json`

**Changes:** Add `suite_version`, `task_version`, `environment_version`, `adapter_contract_version`, `run_id`, `run_status`, `abort_reason`, `web_activity_evidence`

**Steps:**
- [ ] Update `templates/run-metadata.json`
- [ ] Update contract tests for new fields
- [ ] Commit: `feat: add v2 run-metadata fields`

### Task 1.7: Update SKILL.md and README

**Files:**
- Modify: `SKILL.md`
- Modify: `README.md`

**Changes:** v2 trigger, run-id, aborted/partial/completed rules, task catalog

**Steps:**
- [ ] Rewrite `SKILL.md` per spec §2.6 (run_status, run_id uniqueness)
- [ ] Update `README.md` with v2 task catalog
- [ ] Commit: `docs: update SKILL.md and README for v2`

---

## Phase 2: Task 001–003 Upgrades

### Task 2.1: Task 001 — Baseline (static)

**Files:**
- Create: `tasks/task-001/capability-contract.yaml`
- Modify: `tasks/task-001/task.md` (remove causal implication between T-1003/T-1005)

**Steps:**
- [ ] Write `capability-contract.yaml` per spec §6.1
- [ ] Edit `task.md` to remove language implying same root cause
- [ ] Commit: `feat(task-001): add capability contract, remove causal implication`

### Task 2.2: Task 002 — Investigation (static)

**Files:**
- Create: `tasks/task-002/capability-contract.yaml`
- Modify: `tasks/task-002/inputs/deployment-log.md` (spread RCA evidence)

**Steps:**
- [ ] Write `capability-contract.yaml` per spec §6.2
- [ ] Rewrite `deployment-log.md` — spread root cause across entries, no single file gives complete RCA
- [ ] Commit: `feat(task-002): add capability contract, decompose deployment log evidence`

### Task 2.3: Task 003 — Policy Decision (static)

**Files:**
- Create: `tasks/task-003/capability-contract.yaml`
- Modify: `tasks/task-003/task.md` (APPROVE/HOLD/REJECT/ESCALATE)
- Modify: `tasks/task-003/output-requirements.md` (`approval-decision.json` schema)
- Modify: `tasks/task-003/inputs/` (4 requests covering 4 branches, DAT-2025-008=ESCALATE)
- Modify: `tasks/task-003/evaluator-notes/` (updated target decisions)

**Steps:**
- [ ] Write `capability-contract.yaml` per spec §6.3
- [ ] Rewrite task.md with four-decision semantics and role boundary
- [ ] Update output-requirements.md to `approval-decision.json` schema
- [ ] Update request inputs (4 requests → 4 branches)
- [ ] Update evaluator notes with new target decisions
- [ ] Commit: `feat(task-003): upgrade to APPROVE/HOLD/REJECT/ESCALATE decision model`

---

## Phase 3: Task 004 — Coding & Repair

### Task 3.1: Task 004 environment and task definition

**Files:**
- Create: `tasks/task-004/capability-contract.yaml`
- Create: `tasks/task-004/environment-contract.yaml`
- Create: `tasks/task-004/task.md`
- Create: `tasks/task-004/output-requirements.md`
- Create: `tasks/task-004/evaluator-notes/README.md`
- Create: `tasks/task-004/evaluator-private/replacement-data/`
- Create/Dir: `tasks/task-004/environment/base-project/`

**Environment structure:**
```
environment/base-project/
├── README.md
├── src/
│   ├── reconcile.py    # main (1 bug: string amount compare)
│   ├── mapper.py       # field mapping (1 bug: wrong field match)
│   └── reporter.py     # report gen (no bugs)
├── data/
│   ├── crm.csv
│   ├── billing.json
│   └── support.csv
├── tests/
│   └── test_reconcile.py  # 5 tests, 3 FAIL
└── expected-output-format.md
```

**3 injected bugs:**
1. `mapper.py`: matches `customer_name` not `customer_ref` → `account_id`
2. `reconcile.py`: string compare `"1500.00" != "1500.0"` flags false discrepancy
3. `reconcile.py`: `status.lower()` on null throws AttributeError

**Steps:**
- [ ] Write `capability-contract.yaml` and `environment-contract.yaml` per spec §6.4
- [ ] Write `task.md` and `output-requirements.md`
- [ ] Create base project with injected bugs
- [ ] Create evaluator notes and replacement data
- [ ] Create evaluator-private replacement data (anti-hardcoding)
- [ ] Commit: `feat(task-004): add coding & repair task with bug-injected Python project`

---

## Phase 4: Task 005 — Stateful Tool Use

### Task 4.1: Task 005 service and task definition

**Files:**
- Create: `tasks/task-005/capability-contract.yaml`
- Create: `tasks/task-005/environment-contract.yaml`
- Create: `tasks/task-005/task.md`
- Create: `tasks/task-005/output-requirements.md`
- Create: `tasks/task-005/evaluator-notes/README.md`
- Create: `tasks/task-005/evaluator-private/expected-final-state.yaml`
- Create: `tasks/task-005/environment/public/tool-contract.yaml`
- Create: `tasks/task-005/environment/private/schema.sql`
- Create: `tasks/task-005/environment/private/seed.sql`
- Create: `tasks/task-005/environment/service/tool_api.py`

**Tool API:** Python 3 stdlib SQLite3. 12 tools: list_requests, get_request, list_policies, get_policy, get_approval_status, request_information, approve_request, reject_request, escalate_request, get_final_state, get_action_log, reset (for testing).

**State machine:** pending → {information_requested, approved, rejected, escalated}. Terminal: approved, rejected, escalated.

**6 request scenarios** per spec §6.5: REQ-001→approved, REQ-002→approved, REQ-003→information_requested, REQ-004→information_requested, REQ-005→rejected, REQ-006→escalated.

**Steps:**
- [ ] Write all contracts and task definition files
- [ ] Write `schema.sql` and `seed.sql`
- [ ] Write `tool_api.py` with full state machine and policy precondition enforcement
- [ ] Write evaluator-private `expected-final-state.yaml`
- [ ] Commit: `feat(task-005): add stateful tool use task with SQLite service`

---

## Phase 5: Task 006 — Web Research

### Task 5.1: Task 006 controlled web profile

**Files:**
- Create: `tasks/task-006/capability-contract.yaml`
- Create: `tasks/task-006/environment-contract.yaml`
- Create: `tasks/task-006/task.md`
- Create: `tasks/task-006/output-requirements.md`
- Create: `tasks/task-006/evaluator-notes/README.md`
- Create: `tasks/task-006/evaluator-private/reference-sources.yaml`
- Create: `tasks/task-006/profiles/controlled-web/profile-contract.yaml`
- Create: `tasks/task-006/profiles/controlled-web/public/tool-contract.yaml`
- Create: `tasks/task-006/profiles/controlled-web/service/search_service.py`
- Create: `tasks/task-006/profiles/controlled-web/service/private/corpus/` (HTML snapshots)
- Create: `tasks/task-006/profiles/controlled-web/service/private/search-index.json`
- Create: `tasks/task-006/profiles/controlled-web/service/private/corpus-manifest.json`
- Create: `tasks/task-006/profiles/live-web/profile-contract.yaml`

**Controlled web service:** `search_corpus(query)` → doc IDs + snippets; `fetch_document(doc_id)` → full text. Agent cannot read corpus directly.

**Output:** `final-answer.md`, `artifacts/source-register.json`, `artifacts/research-findings.json`, `artifacts/comparison-table.csv`, web activity log.

**Steps:**
- [ ] Write all contracts and task definition files
- [ ] Build controlled web corpus (3 harnesses × official docs snapshots)
- [ ] Write search service with `search_corpus` and `fetch_document`
- [ ] Write evaluator-private reference sources
- [ ] Commit: `feat(task-006): add web research task with controlled-web profile`

---

## Phase 6: Contract Tests Update

### Task 6.1: Upgrade contract tests

**Files:**
- Modify: `tests/test_core_v2_contract.py` (renamed in Phase 1)

**Changes per spec §5:**
- Remove blanket prohibition on packaged execution support
- Add per-environment-type validation rules
- Verify `skill.json` declares environment type per task
- Verify environment contracts exist for tasks 004-006
- Verify `evaluator-notes/` and `evaluator-private/` excluded from agent package via distribution builder
- Verify `archive/` excluded from catalog and run paths
- Add `run_status` field validation
- Verify actual Agent Package contains zero evaluator-only files

**Steps:**
- [ ] Rewrite contract tests for v2
- [ ] Run tests, verify all pass
- [ ] Test distribution builder integration (build agent package, verify no evaluator leaks)
- [ ] Commit: `test: upgrade contract tests for v2 distribution contract`

---

## Phase 7: Verification

### Task 7.1: Run all contract tests

```bash
python3 -m unittest discover tests -v
```

- [ ] All 7+ tests pass

### Task 7.2: Verify distribution builder

```bash
python3 scripts/build-distribution.py --target agent --output dist/agent-package
python3 scripts/build-distribution.py --target runtime --task task-004 --output dist/runtime-task-004
python3 scripts/build-distribution.py --target runtime --task task-005 --output dist/runtime-task-005
python3 scripts/build-distribution.py --target runtime --task task-006 --output dist/runtime-task-006
python3 scripts/build-distribution.py --target evaluator --output dist/evaluator-package
```

- [ ] Agent package contains zero evaluator-notes/evaluator-private/runtime-private files
- [ ] Runtime packages contain correct environment assets
- [ ] Evaluator package contains scoring materials

### Task 7.3: Task 004 smoke test

```bash
cp -r tasks/task-004/environment/base-project /tmp/t004-test/project
cd /tmp/t004-test/project
python3 -m unittest discover -s tests -v  # → 3 FAIL (RED)
# Fix bugs
python3 -m unittest discover -s tests -v  # → 5 PASS (GREEN)
python3 src/reconcile.py                  # → generates output
```

- [ ] Tests fail before fix (RED)
- [ ] Tests pass after fix (GREEN)
- [ ] Business output generated

### Task 7.4: Task 005 smoke test

```bash
cd tasks/task-005/environment/service
python3 tool_api.py init
python3 tool_api.py list_requests
# Execute all 6 scenarios
python3 tool_api.py get_final_state
python3 tool_api.py get_action_log
```

- [ ] All 6 requests achieve expected final states
- [ ] Action log records all operations

### Task 7.5: Task 006 controlled web smoke test

```bash
cd tasks/task-006/profiles/controlled-web/service
python3 search_service.py search_corpus "VitaClaw skill installation"
python3 search_service.py fetch_document <doc_id>
```

- [ ] Search returns relevant documents
- [ ] fetch_document returns full content

### Task 7.6: Dist clean check

```bash
git status  # must be clean (or only intentionally uncommitted artifacts)
```

---

## Phase 8: Real OpenCode UAT

### Task 8.1: Build agent package for UAT

- [ ] `python3 scripts/build-distribution.py --target agent --output /tmp/arev2-uat/skill`

### Task 8.2: Verify agent package isolation

- [ ] No `evaluator-notes/` in package
- [ ] No `evaluator-private/` in package
- [ ] No `runtime-private/` directories
- [ ] All 6 task directories present

### Task 8.3: DeepSeek Pro smoke UAT

Run each task with unique run-id. Record results.

- [ ] task-001 (baseline delivery)
- [ ] task-004 (coding & repair)
- [ ] task-005 controlled_tool (stateful tool use)
- [ ] task-006 controlled_web (web research)

### Task 8.4: DeepSeek Flash smoke UAT

- [ ] task-001
- [ ] task-004

### Task 8.5: Record UAT results

- [ ] Git revision, OpenCode version, model/provider per run
- [ ] Run status, artifacts produced
- [ ] Blockers documented if any

---

## Phase 9: Reporting

### Task 9.1: Generate reports

**Files:**
- Create: `docs/core-v2-implementation-summary.md`
- Create: `docs/core-v2-uat-report.md`
- Create: `docs/core-v2-run-ledger.md`
- Create: `docs/core-v2-blockers.md` (if any)

**Steps:**
- [ ] Write implementation summary
- [ ] Write UAT report
- [ ] Write run ledger
- [ ] Write blockers doc if applicable
- [ ] Commit: `docs: add v2 implementation summary, UAT report, run ledger`

---

## Commit Plan (Atomic)

| # | Message | Files |
|---|---------|-------|
| 1 | `chore: add .omo/ and dist/ to .gitignore` | .gitignore |
| 2 | `chore: archive v1 question-pack and tag v1.0-question-pack-pilot` | archive/, tag |
| 3 | `refactor: rename v3→core_v2 (PRD, TDD, contract tests)` | docs/, tests/ |
| 4 | `feat: add distribution contract` | contracts/ |
| 5 | `feat: add distribution builder` | scripts/ |
| 6 | `feat: upgrade skill.json to v2 structured task catalog` | skill.json |
| 7 | `feat: add v2 run-metadata fields` | templates/ |
| 8 | `docs: update SKILL.md and README for v2` | SKILL.md, README.md |
| 9 | `feat(task-001): add capability contract, remove causal implication` | tasks/task-001/ |
| 10 | `feat(task-002): add capability contract, decompose deployment log evidence` | tasks/task-002/ |
| 11 | `feat(task-003): upgrade to APPROVE/HOLD/REJECT/ESCALATE decision model` | tasks/task-003/ |
| 12 | `feat(task-004): add coding & repair task with bug-injected Python project` | tasks/task-004/ |
| 13 | `feat(task-005): add stateful tool use task with SQLite service` | tasks/task-005/ |
| 14 | `feat(task-006): add web research task with controlled-web profile` | tasks/task-006/ |
| 15 | `test: upgrade contract tests for v2 distribution contract` | tests/ |
| 16 | `docs: add v2 implementation summary, UAT report, run ledger` | docs/ |
