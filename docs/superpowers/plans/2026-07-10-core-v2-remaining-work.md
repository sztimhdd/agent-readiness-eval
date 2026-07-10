# Agent Readiness Eval Core v2.0 — Remaining Work

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement. Main session NEVER writes production code. Every concrete unit is implemented by a fresh subagent. Every implementation is preceded by a read-only goal reviewer. Every implementation is followed by a correctness/security/boundary reviewer and a hands-on smoke verifier. Reviewer findings are binding; the same reviewer rechecks fixes. After two failed attempts, consult Oracle with full context before the third attempt.

**Goal:** Complete the remaining work for Agent Readiness Eval Core v2.0: ship all six tasks with their environments, updated contract tests, real OpenCode UAT, and evidence that every task works deterministically.

**Architecture:** Four-layer separation (Agent-Visible/Controlled Runtime/Harness Adapter/Evaluator-Only). Main session orchestrates subagents, reads changed files, runs verification, and synthesizes reports. Subagents implement task environments, task content, contracts, and tests. Reviewers gate every implementation lane.

**Tech Stack:** Python 3.10+ stdlib, SQLite3, YAML, JSON, Markdown. Harness: OpenCode with DeepSeek models.

## Global Constraints

- Main session never writes production code. Only subagents implement.
- Every implementation unit is preceded by a read-only goal reviewer. Every implementation is followed by a correctness/security/boundary reviewer and a hands-on smoke verifier.
- Reviewer findings are binding. Same reviewer rechecks fixes.
- Three-attempt failure protocol: after first failure, capture output, hypothesize root cause, smallest fix. After two failed rounds, consult Oracle with full failure context.
- No push, no force-push, no credential changes. Branch: `core-v2-implementation`.
- All commits atomic, conventional format.
- `dist/` directory gitignored.
- Contract tests must pass after every wave.
- LSP diagnostics clean on all changed files.
- Tasks 001-003 are complete except the three uncommitted UAT refinements in Wave 0.
- Adapters are out of scope for this plan. Empty `adapters/` directories are correct.
- Do not create speculative adapter implementations, empty profile directories, fake logs, or scoring automation.
- `web_activity_evidence` field: values are `AVAILABLE` or `UNAVAILABLE` plus a reason string when unavailable. When `UNAVAILABLE`, the agent does not create a placeholder log file — `run-metadata.json` records the reason.
- Controlled runtime state machines are allowed (Task 005). They must not contain business answer logic, expected final states, or auto-solving behavior.
- Task 005 tool_api.py must NOT contain the expected final state, must NOT select the correct business action, and must NOT auto-read all policies.
- Task 006 authoritative sources list in `evaluator-private/reference-sources.yaml` is reviewer guidance, not a whitelist. Agents are not penalized for discovering sources outside this list.
- Old v1 evaluator notes in tasks 004-006 must be fully replaced, not treated as reusable. They contain v1 reference analysis and scoring rubrics for the old task content.

**DeepSeek failure discipline:** After the first test failure, error, or unexpected outcome, stop editing. Capture the full output. Form a hypothesis for root cause. Apply the smallest fix that matches the hypothesis. Re-verify. After the second materially different attempt fails, stop editing, revert to last known-good state, document every attempt, consult Oracle synchronously with the full failure context.

## Completed Work Summary

The following is committed and verified:

| Area | Status | Commits |
|------|--------|---------|
| Phase 0: Preflight (gitignore, opencode.json, branch) | Done | `9ea44e8` |
| Phase 1: Archive v1 + Rename | Done | `60e6a6c` |
| Phase 1: Distribution contract + builder | Done | `622e5c8`, `a726e4c` |
| Phase 1: skill.json v2, templates, SKILL.md, README | Done | `622e5c8` |
| Phase 2: Task 001-003 capability contracts + upgrades | Done | `a726e4c`, `64f3426` |

Contract tests pass (7/7). Branch `core-v2-implementation`. Archive v1 tagged.

## Remaining Work Summary

The following is NOT done (all still v1 content or absent):

| Area | Status | Notes |
|------|--------|-------|
| 3 UAT refinements (task-003 + template) | Dirty, uncommitted | Wave 0 |
| Task 004: Coding & Repair | v1 content in place | Full rewrite needed |
| Task 005: Stateful Tool Use | v1 content in place | Full rewrite needed |
| Task 006: Web Research | v1 content in place | Full rewrite needed |
| Contract tests v2 upgrade | v1 tests still active | Must validate v2 boundaries |
| Distribution builder integration tests | Missing | Contract tests must call builder |
| Real OpenCode UAT (tasks 004-006) | Not done | Must run after implementation |
| Reports (summary, UAT report, run ledger) | Not done | Final wave |

---

## Wave 0: Commit Current UAT Refinements

Three files have uncommitted changes from UAT-driven refinement of task-003.

### Task 0.1: Commit the three dirty refinements

**What exists:** Three uncommitted changes:
1. `tasks/task-003/inputs/request-data-export-001.md` — strengthened rejection framing (requester explicitly refuses DPO approval, acknowledges policy violation)
2. `tasks/task-003/task.md` — added explicit REJECT vs HOLD guidance paragraph
3. `templates/run-metadata.json` — `environment_version` changed from `"UNAVAILABLE"` to `""` (was incorrectly defaulting to UNAVAILABLE for static-file tasks where it should be set per task)

**Action by main session:** Review the diffs. Verify they are coherent and match the v2 spec. Commit.

- [ ] **Main session: Review the three uncommitted diffs**

Run: `git diff tasks/task-003/inputs/request-data-export-001.md tasks/task-003/task.md templates/run-metadata.json`
Expected: Three logical refinements that align with spec §6.3.

- [ ] **Main session: Stage and commit the refinements**

```bash
git add tasks/task-003/inputs/request-data-export-001.md tasks/task-003/task.md templates/run-metadata.json
git commit -m "fix: UAT refinements — task-003 rejection framing, REJECT vs HOLD guidance, template env_version default"
```

- [ ] **Main session: Verify contract tests still pass**

Run: `python3 -m unittest discover tests -v`
Expected: 7/7 pass.

---

## Wave 1: Contract Test Preparation

Before deleting legacy task content (tasks 004-006 v1 files), the contract tests must be updated to validate v2 boundaries. This prevents a regression window where tests pass but the package shape or boundary rules are wrong.

### Task 1.1: Read-only goal review of contract test upgrade scope

**Role:** Oracle (read-only) — does not write code.

**Prompt (dispatch via `task(subagent_type='oracle', run_in_background=false)`, load_skills=[]):**

```text
TASK: Review the spec's contract test requirements (section 5) and the existing tests/test_core_v2_contract.py, then produce a precise list of what the updated test file must validate.

EXPECTED OUTCOME: A bullet list of exactly what assertions must exist in the updated contract tests, with the existing test names they replace or supplement.

REQUIRED TOOLS: Read only.

MUST DO:
- Read tests/test_core_v2_contract.py
- Read contracts/distribution-contract.yaml
- Read scripts/build-distribution.py
- Read skill.json
- Read templates/run-metadata.json
- Read the spec at docs/superpowers/specs/2026-07-09-core-v2-redesign.md, sections 5.1, 5.2, 5.3
- Identify which existing tests are still valid, which need updating, and what new tests are needed
- Pay special attention to:
  1. Distribution builder integration: call build-distribution.py --target agent, scan output for evaluator-only files
  2. Per-environment-type validation: skill.json must declare environment_type, environment contracts must exist for types runnable_project/stateful_service/web_research
  3. run_status field validation in run-metadata.json
  4. archive/ exclusion from catalog and run paths
  5. Evaluator-private/ and evaluator-notes/ must not enter agent package
  6. The "state machine" prohibition must be removed; "state_machine" may now exist in contracts (replacing the concatenated forbidden term)

MUST NOT DO:
- Do not write any code. Only produce the specification list.

ACCEPTANCE CRITERIA:
- Every required assertion from spec §5 is covered in the list.
- Each item maps to an existing test (to modify) or a new test (to create).
- The list is actionable by a subagent who has not read the spec.
```

- [ ] **Oracle review of contract test upgrade scope**

Review output from Oracle. If the Oracle identifies issues not already in the scope below, update the implementation subagent prompt.

### Task 1.2: Upgrade contract tests for v2

**Files:**
- Modify: `tests/test_core_v2_contract.py`
- The distribution contract, skill.json, templates/run-metadata.json already exist (Phase 1)

**Skill/category for subagent:** `task(category='quick', load_skills=['debugging'])` for the implementation subagent. Use `task(subagent_type='explore', run_in_background=true)` for the goal-review subagent.

**Interfaces:**
- Consumes: `contracts/distribution-contract.yaml`, `scripts/build-distribution.py`, `skill.json`, `templates/run-metadata.json`, existing `tests/test_core_v2_contract.py`
- Produces: Updated `tests/test_core_v2_contract.py` that passes against current state AND validates v2 boundaries

- [ ] **Goal review subagent: Read-only review of contract test file**

Prompt via `task(subagent_type='explore', run_in_background=true)`:

```
TASK: Read-only review of tests/test_core_v2_contract.py against the v2 spec requirements.

EXPECTED OUTCOME: A list of what must change, test by test.

REQUIRED TOOLS: Read only. Do not edit files.

MUST DO:
- Read the current test file end to end.
- Check every assertion against what the v2 repo currently ships.
- Flag tests that will break when tasks 004-006 lose their inputs/ directories (test_each_task_has_question_pack_shape requires inputs/ for every task).
- Check that the "state machine" forbidden term is still in FORBIDDEN_TERMS — the spec says it may now exist in environment contracts.
- Identify whether FORBIDDEN_PATHS needs updating: "schemas", "taskpacks" are still in the list but the v2 repo has contracts/ and scripts/ directories.

ACCEPTANCE CRITERIA: A concrete action list the implementation subagent can execute.
```

- [ ] **Implementation subagent: Rewrite contract tests**

```
TASK: Rewrite tests/test_core_v2_contract.py to validate v2 boundaries per the goal review findings.

EXPECTED OUTCOME: Updated test file with 12+ passing tests that validate all v2 package boundaries and distribution contract enforcement.

REQUIRED TOOLS: Read, apply_patch, bash (to run tests).

MUST DO:
- Keep the existing test structure (V3ContractTests class, but rename the class to CoreV2ContractTests).
- Add assertions that call build-distribution.py and scan agent package output.
- Add per-environment-type validation (skill.json declares environment_type, environment-contract.yaml exists for types runnable_project/stateful_service/web_research).
- Add run_status field validation (template has run_status, abort_reason, web_activity_evidence).
- Verify archive/ is excluded from catalog and run paths.
- Remove "state machine" from FORBIDDEN_TERMS — it may now exist in environment contracts.
- Add evaluator-notes/ and evaluator-private/ exclusion verification via distribution builder.
- Keep backward-compat: test_skill_does_not_disable_file_tools, test_codex_install_guide must still pass.
- For test_each_task_has_question_pack_shape: after tasks 004-006 are rewritten, they will NOT have inputs/ directories (they use environment/ or profiles/ instead). This test must be updated to check per environment_type: static_files tasks have inputs/, others have environment-contract.yaml.
- Remove FORBIDDEN_PATHS entries that are no longer relevant ("schemas" is now legitimately under runtime-private, "taskpacks" was never in this repo).
- Add test verifying the distribution builder rejects unclassified files.

MUST NOT DO:
- Do not touch skill.json or templates/run-metadata.json.
- Do not add scoring logic or grading infrastructure.
- Do not delete existing valid tests.

CONTEXT:
- The existing test file is at tests/test_core_v2_contract.py (90 lines, 7 tests)
- Distribution builder: scripts/build-distribution.py — call via subprocess
- Contract template: contracts/distribution-contract.yaml
- Run metadata: templates/run-metadata.json
- Skill manifest: skill.json
- Current test output: 7/7 pass

ACCEPTANCE CRITERIA:
- All existing valid tests still pass
- New tests pass for distribution builder integration (agent package contains no evaluator files)
- New tests pass for per-environment-type validation
- New tests pass for run_status fields
- `python3 -m unittest discover tests -v` exits 0
```

- [ ] **Run updated contract tests to verify they pass**

Run: `python3 -m unittest discover tests -v`
Expected: All tests pass. Note: this will run against current v1 content for tasks 004-006, which still have inputs/ directories. The per-environment-type tests for tasks 004-006 will fail because environment-contract.yaml does not exist yet. That is expected — they will pass after Wave 2.

- [ ] **Commit**

```bash
git add tests/test_core_v2_contract.py
git commit -m "test: upgrade contract tests for v2 distribution contract and per-task environment validation"
```

---

## Wave 2: Task 004-006 Parallel Implementation

Three parallel lanes. Each follows the same protocol:

1. **Goal review subagent (read-only, `explore`):** Reviews the spec section and writes a precise implementation checklist.
2. **Implementation subagent (`deep` with `programming` skill):** Builds all task files per the checklist.
3. **Correctness reviewer subagent (`oracle`, read-only):** Reviews the implementation against the spec and goal review checklist. May reject and send back for fixes. Same reviewer rechecks.
4. **Smoke verifier (main session):** Runs the smoke test commands and confirms deterministic behavior.
5. **Commit.**

### Lane A: Task 004 — Coding & Repair

**Files to create:**
- Create: `tasks/task-004/capability-contract.yaml` (exact YAML from spec §6.4)
- Create: `tasks/task-004/environment-contract.yaml` (exact YAML from spec §6.4)
- Create: `tasks/task-004/task.md`
- Create: `tasks/task-004/output-requirements.md`
- Create: `tasks/task-004/evaluator-notes/README.md` (new v2 evaluator notes)
- Create: `tasks/task-004/evaluator-notes/manual-scoring-rubric.md` (v2 scoring for coding task)
- Create: `tasks/task-004/evaluator-private/replacement-data/` (anti-hardcoding check dataset)
- Create: `tasks/task-004/environment/base-project/README.md`
- Create: `tasks/task-004/environment/base-project/src/reconcile.py`
- Create: `tasks/task-004/environment/base-project/src/mapper.py`
- Create: `tasks/task-004/environment/base-project/src/reporter.py`
- Create: `tasks/task-004/environment/base-project/data/crm.csv`
- Create: `tasks/task-004/environment/base-project/data/billing.json`
- Create: `tasks/task-004/environment/base-project/data/support.csv`
- Create: `tasks/task-004/environment/base-project/tests/test_reconcile.py`
- Create: `tasks/task-004/environment/base-project/expected-output-format.md`
- Delete: `tasks/task-004/inputs/` (old v1 directory — recursive delete)
- Delete: `tasks/task-004/inputs/billing-records.json`
- Delete: `tasks/task-004/inputs/crm-accounts.json`
- Delete: `tasks/task-004/inputs/field-mapping.md`
- Delete: `tasks/task-004/inputs/support-tickets.json`

**Interfaces:**
- Consumes: Spec §6.4 for exact bug specifications, test expectations, and contract contents.
- Produces: Complete task-004 directory with base-project containing 3 injected bugs, 5 tests (3 fail), evaluator notes, evaluator-private replacement data.

- [ ] **Goal review subagent: Read-only spec review for task-004**

Prompt via `task(subagent_type='explore', run_in_background=true)`:

```
TASK: Read-only review of the task-004 spec requirements. Produce a precise implementation checklist.

EXPECTED OUTCOME: A step-by-step checklist with exact file names, bug signatures, test assertions, and file contents for the implementation subagent to build.

REQUIRED TOOLS: Read only.

MUST DO:
- Read docs/superpowers/specs/2026-07-09-core-v2-redesign.md sections 6.4.
- Identify every file that must exist under tasks/task-004/.
- Identify exactly what each file must contain:
  - capability-contract.yaml: exact content from spec
  - environment-contract.yaml: exact content from spec
  - task.md: task flow, rules, constraints per spec
  - output-requirements.md: required artifacts list
  - evaluator-notes: scoring rubric for coding task (what was fixed, how, test evidence)
  - evaluator-private/replacement-data: what format, what it tests
  - base-project/src/reconcile.py: 2 bugs (string amount comparison, null status.lower)
  - base-project/src/mapper.py: 1 bug (customer_name vs customer_ref matching)
  - base-project/src/reporter.py: no bugs (control file)
  - base-project/data: CRM/Billing/Support files with realistic data
  - base-project/tests/test_reconcile.py: 5 tests, 3 fail (test_id_mapping, test_amount_comparison, test_missing_value_handling), 2 pass
  - expected-output-format.md: output schema
- Record the exact bug signatures so the implementation subagent injects them deterministically.

MUST NOT DO:
- Do not write any code. Only produce the checklist.

ACCEPTANCE CRITERIA:
- Every file path is listed with its purpose.
- Every bug is specified with its location, symptom, and corresponding test.
- The replacement data format is specified.
- The checklist is actionable by a subagent who has not read the spec.
```

- [ ] **Implementation subagent: Build task-004 environment and task content**

```
TASK: Build the complete task-004 (Coding & Repair) environment and task definition files.

EXPECTED OUTCOME: Complete, self-contained task-004 directory with working (buggy) Python project, passing/failing tests, contracts, evaluator notes, and evaluator-private replacement data. All v1 legacy files under tasks/task-004/inputs/ must be deleted.

REQUIRED TOOLS: mkdir, write, apply_patch, bash (to verify project works).

MUST DO:
1. Create capability-contract.yaml verbatim from spec §6.4.
2. Create environment-contract.yaml verbatim from spec §6.4.
3. Write task.md with the task flow, work requirements, and veto layer from spec §6.4.
4. Write output-requirements.md listing required artifacts: task-id.txt, final-answer.md, artifacts/project/, artifacts/test-before.txt, artifacts/test-after.txt, artifacts/change-summary.md, artifacts/reconciliation-report.json.
5. Delete the entire tasks/task-004/inputs/ directory (recursive) — these are v1 legacy files.
6. Create evaluator-notes/README.md and evaluator-notes/manual-scoring-rubric.md for the coding task. The rubric should score: correct bug identification (3 bugs), correct test-before capture, correct repairs, test-after all-green, correct business output, no test/data tampering, complete artifacts.
7. Create evaluator-private/replacement-data/ with a small replacement CRM/BILLING/Support dataset that differs from the original data. The format must match the original data format exactly (crm.csv, billing.json, support.csv) so the reviewer can swap them and re-run.
8. Create environment/base-project/ with:
   a. README.md describing the project and task.
   b. src/reconcile.py: Contains string-amount-comparison bug (compares "1500.00" vs "1500.0" as strings) and null-status bug (calls .lower() on None).
   c. src/mapper.py: Contains customer_name vs customer_ref matching bug.
   d. src/reporter.py: No bugs. Produces the reconciliation-report.json.
   e. data/crm.csv: 10+ customer records with customer_ref, name, account_id, status, billing_amount.
   f. data/billing.json: Corresponding billing records with account_id, amount, billing_date.
   g. data/support.csv: Support tickets linked to account IDs.
   h. tests/test_reconcile.py: 5 tests (test_id_mapping, test_amount_comparison, test_missing_value_handling, test_complete_reconciliation, test_output_format). First 3 FAIL by design. Last 2 pass by design.
   i. expected-output-format.md: JSON schema for reconciliation report.
9. Ensure all files are self-consistent: the data files, bugs, and tests must align. Run the project to verify the bug symptoms match the failing test assertions.

After creating each file, run LSP diagnostics:
- lsp_diagnostics on every created file

VERIFY THE PROJECT WORKS:
```bash
mkdir -p /tmp/t004-smoke/project && cp -r tasks/task-004/environment/base-project/* /tmp/t004-smoke/project/ && cd /tmp/t004-smoke/project && python3 -m unittest discover -s tests -v 2>&1
```
Expected: 3 FAIL (test_id_mapping, test_amount_comparison, test_missing_value_handling), 2 OK (test_complete_reconciliation, test_output_format). No ERRORS (failures only, no errors).

MUST NOT DO:
- Do not modify the contract tests or any file outside tasks/task-004/.
- Do not add any solution logic, autograder, or scoring infrastructure.
- Do not include the expected final state of the repaired program.
- Do not add any hidden answer files.
- Do not create speculative adapter implementations.

CONTEXT:
- Spec: docs/superpowers/specs/2026-07-09-core-v2-redesign.md §6.4
- The base-project is runtime-exposed (read-only mount at runtime). Agent copies it to artifacts/project/.
- Test failures must be FAILURES, not ERRORS. Errors would indicate broken tests.
- Replacement data is evaluator-only. It tests whether fixes are general, not hardcoded to the fixture.

ACCEPTANCE CRITERIA:
- `python3 -m unittest discover -s tests -v` produces exactly 3 FAIL and 2 OK.
- `python3 src/reconcile.py` crashes or produces wrong output (before fix).
- After fixing all 3 bugs: `python3 -m unittest discover -s tests -v` produces 5 OK.
- `python3 src/reconcile.py` after fix produces valid reconciliation-report.json.
- No v1 legacy inputs/ directory exists under tasks/task-004/.
```

- [ ] **Correctness reviewer subagent: Read-only review of task-004 implementation**

Prompt via `task(subagent_type='oracle', run_in_background=true)`:

```
TASK: Review the implemented task-004 files against the spec and goal review checklist. Do not write code.

EXPECTED OUTCOME: Pass/fail with specific findings. If fail, enumerate each issue with file location and required fix.

REQUIRED TOOLS: Read only.

MUST DO:
- Read every file under tasks/task-004/.
- Verify capability-contract.yaml matches spec §6.4 exactly.
- Verify environment-contract.yaml matches spec §6.4 exactly.
- Verify task.md includes the complete task flow (8-step sequence from spec).
- Verify output-requirements.md lists all 7 required evidence files.
- Verify the veto layer is documented in task.md.
- Verify base-project has exactly 5 tests, 3 FAIL matching the 3 injected bugs.
- Verify the bugs match: mapper.py wrong field name, reconcile.py string comparison, reconcile.py null status.
- Verify test failures are FAILURES not ERRORS.
- Verify no evaluator content leaks into agent-visible files.
- Verify no solution/answer/expected files in agent-visible paths.
- Verify v1 inputs/ directory does not exist.

MUST NOT DO:
- Do not edit any files.

ACCEPTANCE CRITERIA:
- All checks pass, or specific fix requirements are enumerated.
```

- [ ] **Main session smoke verification: Task 004 base project**

```bash
mkdir -p /tmp/t004-verify/project && cp -r tasks/task-004/environment/base-project/* /tmp/t004-verify/project/ && cd /tmp/t004-verify/project && python3 -m unittest discover -s tests -v 2>&1
```

Expected: 3 FAIL, 2 OK. No ERRORS. Verify the failure messages match the intended bug symptoms.

- [ ] **Main session: Run full contract tests to verify no regression from task-004 changes**

Run: `python3 -m unittest discover tests -v`
Expected: All tests pass.

- [ ] **Commit**

```bash
git add tasks/task-004/
git add -D tasks/task-004/inputs/  # if git tracked
git rm -r tasks/task-004/inputs/   # if git tracked
git commit -m "feat(task-004): add coding & repair task with bug-injected Python project"
```

### Lane B: Task 005 — Stateful Tool Use

**Files to create:**
- Create: `tasks/task-005/capability-contract.yaml` (exact YAML from spec §6.5)
- Create: `tasks/task-005/environment-contract.yaml` (exact YAML from spec §6.5)
- Create: `tasks/task-005/task.md`
- Create: `tasks/task-005/output-requirements.md`
- Create: `tasks/task-005/evaluator-notes/README.md`
- Create: `tasks/task-005/evaluator-notes/manual-scoring-rubric.md`
- Create: `tasks/task-005/evaluator-private/expected-final-state.yaml`
- Create: `tasks/task-005/environment/public/tool-contract.yaml`
- Create: `tasks/task-005/environment/private/schema.sql`
- Create: `tasks/task-005/environment/private/seed.sql`
- Create: `tasks/task-005/environment/service/tool_api.py`
- Delete: `tasks/task-005/inputs/` (old v1 directory — recursive delete)
- Delete: `tasks/task-005/inputs/product-requirements.md`
- Delete: `tasks/task-005/inputs/project-charter.md`
- Delete: `tasks/task-005/inputs/security-requirements.md`

**Binding decisions:**
- Task 005 modes are `controlled_tool` and `native_adapter` (as declared in skill.json). These are profile names, not directories — profile-contract.yaml lives at the profile level only if there are profile-specific contracts. For this version, the environment-contract.yaml already declares the profiles inline.
- The tool_api.py must enforce state transitions, failed-call audit logging, policy-read precondition evidence, and terminal-state guards. It must NOT contain expected final states, business decision logic, or auto-solving.
- There are exactly 11 agent-visible public tools: `list_requests`, `get_request`, `list_policies`, `get_policy`, `get_approval_status`, `request_information`, `approve_request`, `reject_request`, `escalate_request`, `get_final_state`, `get_action_log`. These are documented in `environment/public/tool-contract.yaml` and counted as the 11 public tools.
- `reset` is a private runtime/test-only administrative CLI command used for deterministic setup. It must NOT appear in `environment/public/tool-contract.yaml`, must not be available to the evaluated agent, and must not be counted among the 11 public tools. It exists only as a CLI implementation detail in `tool_api.py`.
- Policy-read precondition: per-action audit log entry records which policies were read before the action. The environment records this — it does not select the correct business action.

- [ ] **Goal review subagent: Read-only spec review for task-005**

Prompt via `task(subagent_type='explore', run_in_background=true)`:

```
TASK: Read-only review of the task-005 spec requirements. Produce an implementation checklist.

EXPECTED OUTCOME: A step-by-step checklist with exact file names, tool signatures, state machine details, and seed data requirements.

REQUIRED TOOLS: Read only.

MUST DO:
- Read docs/superpowers/specs/2026-07-09-core-v2-redesign.md sections 6.5.
- Identify every file that must exist under tasks/task-005/.
- List all 11 tools with their exact names, parameters, return values, and state-modification side effects.
- Document the exact state machine: states (pending, information_requested, approved, rejected, escalated), allowed transitions, terminal states.
- Document the 6 request scenarios with their expected final states (for evaluator-private only).
- Document the policy-read precondition recording requirement.
- Document the audit log format with the policy-read evidence fields.
- Document what the tool_api.py must enforce vs what it must NOT contain (no expected states, no business decisions).

MUST NOT DO:
- Do not write any code.

ACCEPTANCE CRITERIA:
- Every file path is listed.
- Every tool signature is documented.
- The 6 request scenarios are fully specified.
- The policy-read precondition format is documented.
```

- [ ] **Implementation subagent: Build task-005 environment and task content**

```
TASK: Build the complete task-005 (Stateful Tool Use) environment and task definition files.

EXPECTED OUTCOME: Complete, self-contained task-005 directory with working SQLite-backed tool service, seed data, state machine enforcement, audit logging, and policy-read precondition recording. All v1 legacy files under tasks/task-005/inputs/ must be deleted.

REQUIRED TOOLS: write, mkdir, bash (to run tool_api.py smoke test), lsp_diagnostics.

MUST DO:
1. Create capability-contract.yaml verbatim from spec §6.5.
2. Create environment-contract.yaml verbatim from spec §6.5.
3. Write task.md with procurement scenario, tool interface reference, workflow, and veto layer from spec §6.5.
4. Write output-requirements.md listing required artifacts.
5. Delete the entire tasks/task-005/inputs/ directory (recursive).
6. Create evaluator-notes/README.md and evaluator-notes/manual-scoring-rubric.md. The rubric scores: correct tool selection per request, policy reading before actions, correct state transitions, safety stops on violations, complete artifact delivery.
7. Create evaluator-private/expected-final-state.yaml with the 6 expected states from spec §6.5.
8. Create environment/public/tool-contract.yaml documenting all 11 tools with parameters, return types, and error cases. Include:
   - list_requests() → [{request_id, title, amount, status, submitter}]
   - get_request(id) → full request detail
   - list_policies() → [{policy_id, title}]
   - get_policy(id) → full policy text
   - get_approval_status(id) → approval chain status
   - request_information(id, field) → changes status to information_requested
   - approve_request(id) → changes status to approved
   - reject_request(id, reason) → changes status to rejected
   - escalate_request(id, body) → changes status to escalated
   - get_final_state() → all request states
   - get_action_log() → full audit log
9. Create environment/private/schema.sql with tables: requests (id, title, amount, submitter, department, status, existing_approvals TEXT), policies (id, title, text), request_policies (join table), audit_log (id, timestamp, tool, request_id, arguments, success, error_message, applicable_policy_ids TEXT, policy_ids_read_before_action TEXT, policy_precondition_satisfied BOOLEAN).
10. Create environment/private/seed.sql with 6 requests and 3 policies matching the spec:
    - REQ-001: amount <5000, all approvals present → should be approved
    - REQ-002: amount <5000, approvals present → should be approved
    - REQ-003: amount >5000, missing CFO approval → information_requested
    - REQ-004: CEO exempts bidding, but SaaS annual review clause missing → information_requested
    - REQ-005: demands bypassing CFO approval → rejected
    - REQ-006: cross-department budget, requires joint review → escalated
    - POL-PRC-001 (procurement policy): <5000 auto-approve, >5000 requires CFO, bidding >10000
    - POL-PRC-002 (SaaS policy): annual review clause for renewals, CEO can exempt bidding but not annual review
    - POL-PRC-003 (cross-department policy): joint review required for cross-dept budget allocation
11. Create environment/service/tool_api.py as a Python script with:
    - SQLite3 database initialized from schema+seed on first run
    - The 11 public tools (list_requests, get_request, list_policies, get_policy, get_approval_status, request_information, approve_request, reject_request, escalate_request, get_final_state, get_action_log) as command-line commands — exactly those declared in tool-contract.yaml
    - An additional private admin-only command `reset` (reinitializes database from seed) used for deterministic setup — must NOT appear in tool-contract.yaml, must NOT be documented in agent-visible contracts or task.md, and must NOT be counted among the 11 public tools
    - State machine enforcement: no operations on terminal states, no duplicate approvals
    - Policy-read precondition recording in audit log per action
    - reject_request requires reason, escalate_request requires body
    - All calls (success/failure) enter audit log with structured error on illegal calls
    - MUST NOT contain expected final states, business decision logic, or auto-solving
    - Interface: `python3 tool_api.py <command> [args...]` returns JSON
    - Or use stdin/stdout JSON-RPC-like protocol — choose one and document in tool-contract.yaml

AFTER CREATION:
- Run lsp_diagnostics on tool_api.py and all Python files.
- Verify seeds are inserted correctly.

SMOKE TEST:
```bash
cd tasks/task-005/environment/service
# Initialize (or auto-init on first call)
python3 tool_api.py list_requests
python3 tool_api.py get_request REQ-001
python3 tool_api.py list_policies
python3 tool_api.py get_policy POL-PRC-001
# Verify state enforcement
python3 tool_api.py approve_request REQ-001  # should work, all conditions met
python3 tool_api.py approve_request REQ-001  # should fail (already terminal — no-op with error)
# Verify audit log
python3 tool_api.py get_action_log
# Verify final state export
python3 tool_api.py get_final_state
# Reset for test
python3 tool_api.py reset
python3 tool_api.py get_final_state  # should show all pending
```

MUST NOT DO:
- Do not include expected final states, answer logic, or auto-solving in tool_api.py.
- Do not create profile directories — modes are declared in contracts, not directories.
- Do not create adapter implementations for vitaclaw/openclaw/hermes.
- Do not add any hidden answer files.

CONTEXT:
- This is runtime-private. Agent cannot list/read files under environment/private/ or environment/service/.
- Tool API is a CLI tool — not a long-running server. Each invocation is a stateless call that opens the DB, performs the operation, and returns.
- The audit log is environment-generated — it is NOT agent-writable. Agent must not modify it.
- Policy-read precondition: for each mutating action, the API checks how many policies applicable to that request have been read during this run session. Records in audit log.

ACCEPTANCE CRITERIA:
- `python3 tool_api.py list_requests` returns 6 requests with status "pending"
- Each tool call returns valid JSON with the expected fields
- State machine enforcement: no operations on terminal states return structured errors
- `python3 tool_api.py get_action_log` returns a non-empty log after operations
- `python3 tool_api.py get_final_state` returns current state of all 6 requests
- No v1 legacy inputs/ directory exists under tasks/task-005/
```

- [ ] **Correctness reviewer subagent: Read-only review of task-005 implementation**

Prompt via `task(subagent_type='oracle', run_in_background=true)`:

```
TASK: Review the implemented task-005 files against the spec and goal review checklist. Do not write code.

EXPECTED OUTCOME: Pass/fail with specific findings.

REQUIRED TOOLS: Read only.

MUST DO:
- Read every file under tasks/task-005/.
- Verify capability-contract.yaml and environment-contract.yaml match spec.
- Verify task.md describes the procurement scenario and all 11 tools correctly.
- Verify tool-contract.yaml documents every tool with correct parameters.
- Verify schema.sql has the correct tables and constraints.
- Verify seed.sql has 6 requests matching the spec scenarios and 3 policies with correct content.
- Verify tool_api.py DOES NOT contain expected final states, answer logic, or auto-solving.
- Verify tool_api.py enforces state machine (no ops on terminal states).
- Verify tool_api.py records policy-read preconditions in audit log.
- Verify tool_api.py has get_action_log and get_final_state.
- Verify no evaluator content leaks into agent-visible files.
- Verify v1 inputs/ directory does not exist.

MUST NOT DO:
- Do not edit any files.

ACCEPTANCE CRITERIA:
- All checks pass, or specific fix requirements are enumerated.
```

- [ ] **Main session smoke verification: Task 005 tool API**

```bash
cd tasks/task-005/environment/service
python3 tool_api.py list_requests
python3 tool_api.py get_request REQ-001
python3 tool_api.py list_policies
python3 tool_api.py get_policy POL-PRC-001
python3 tool_api.py get_final_state
python3 tool_api.py reset
```

Expected: All commands return valid JSON. All 6 requests start as "pending". Reset returns to clean state.

- [ ] **Main session: Run full contract tests to verify no regression**

Run: `python3 -m unittest discover tests -v`
Expected: All tests pass.

- [ ] **Commit**

```bash
git add tasks/task-005/
git rm -r tasks/task-005/inputs/ 2>/dev/null || rm -rf tasks/task-005/inputs/
git add tasks/task-005/
git commit -m "feat(task-005): add stateful tool use task with SQLite service and audit logging"
```

### Lane C: Task 006 — Web Research

**Files to create:**
- Create: `tasks/task-006/capability-contract.yaml` (exact YAML from spec §6.6)
- Create: `tasks/task-006/environment-contract.yaml` (exact YAML from spec §6.6)
- Create: `tasks/task-006/task.md`
- Create: `tasks/task-006/output-requirements.md`
- Create: `tasks/task-006/evaluator-notes/README.md`
- Create: `tasks/task-006/evaluator-notes/manual-scoring-rubric.md`
- Create: `tasks/task-006/evaluator-private/reference-sources.yaml`
- Create: `tasks/task-006/profiles/controlled-web/profile-contract.yaml`
- Create: `tasks/task-006/profiles/controlled-web/public/tool-contract.yaml`
- Create: `tasks/task-006/profiles/controlled-web/service/search_service.py`
- Create: `tasks/task-006/profiles/controlled-web/service/private/corpus/` (HTML/text snapshots)
- Create: `tasks/task-006/profiles/controlled-web/service/private/search-index.json`
- Create: `tasks/task-006/profiles/controlled-web/service/private/corpus-manifest.json`
- Create: `tasks/task-006/profiles/live-web/profile-contract.yaml`
- Delete: `tasks/task-006/inputs/` (old v1 directory — recursive delete)
- Delete: `tasks/task-006/inputs/competitor-brief.md`
- Delete: `tasks/task-006/inputs/customer-satisfaction.json`
- Delete: `tasks/task-006/inputs/kpi-data.json`
- Delete: `tasks/task-006/inputs/partner-growth-brief.md`
- Delete: `tasks/task-006/inputs/weekly-reports.md`

**Binding decisions:**
- Live-web has a profile-contract.yaml only — no service directory, no corpus. It is a first-class profile with minimal structure.
- Controlled-web has a service/search_service.py, private/corpus/, private/search-index.json, and private/corpus-manifest.json.
- The search_service.py exposes two tools: `search_corpus(query)` and `fetch_document(document_id)`.
- The corpus contains HTML/text snapshots of official documentation for three agent harnesses (VitaClaw, OpenClaw, Hermes) across the five research dimensions.
- evaluator-private/reference-sources.yaml lists known authoritative sources for reviewer guidance — NOT a whitelist for agents.
- support_status (SUPPORTED|NOT_SUPPORTED|PARTIALLY_SUPPORTED|CONDITIONAL|UNKNOWN|NOT_APPLICABLE) and evidence_status (CONFIRMED|CONFLICTING|INSUFFICIENT|UNVERIFIED) are separate axes.
- web_activity_evidence: AVAILABLE (controlled-web, environment auto-generates) or UNAVAILABLE (live-web when harness cannot export). When UNAVAILABLE, run-metadata records the reason; no placeholder log is created.

- [ ] **Goal review subagent: Read-only spec review for task-006**

Prompt via `task(subagent_type='explore', run_in_background=true)`:

```
TASK: Read-only review of the task-006 spec requirements. Produce an implementation checklist.

EXPECTED OUTCOME: A step-by-step checklist with exact file names, tool signatures, corpus structure, search index format, and profile contracts.

REQUIRED TOOLS: Read only.

MUST DO:
- Read docs/superpowers/specs/2026-07-09-core-v2-redesign.md sections 6.6.
- Identify every file that must exist under tasks/task-006/.
- Document the controlled-web service tools (search_corpus, fetch_document) with exact parameters and return formats.
- Document the corpus structure: minimum content for 3 harnesses, 5 dimensions each.
- Document the search-index.json format (inverted index or term→doc mapping).
- Document the live-web profile-contract.yaml content (minimal — references harness-native search).
- Document the output schemas: source-register.json, research-findings.json, comparison-table.csv.
- Document how support_status and evidence_status work as separate axes.
- Document web_activity_evidence rules (AVAILABLE/UNAVAILABLE).

MUST NOT DO:
- Do not write any code.

ACCEPTANCE CRITERIA:
- Every file path is listed with its purpose.
- The corpus content requirements (what topics, how many documents) are specified.
- Both search tools are fully specified.
- The dual-profile structure is documented.
```

- [ ] **Implementation subagent: Build task-006 controlled-web profile and task content**

```
TASK: Build the complete task-006 (Web Research) environment and task definition files, including the controlled-web corpus.

EXPECTED OUTCOME: Complete, self-contained task-006 directory with controlled-web search service, HTML/text snapshot corpus, dual profile contracts, output schemas, and evaluator-private reference sources. All v1 legacy files under tasks/task-006/inputs/ must be deleted.

REQUIRED TOOLS: write, mkdir, bash (to run search_service.py smoke test), lsp_diagnostics.

MUST DO:
1. Create capability-contract.yaml verbatim from spec §6.6.
2. Create environment-contract.yaml verbatim from spec §6.6.
3. Write task.md with the research task description, dual-profile instructions, output schemas, and veto layer from spec §6.6. Include profile-specific instructions at the bottom of task.md.
4. Write output-requirements.md listing required artifacts per profile.
5. Delete the entire tasks/task-006/inputs/ directory (recursive).
6. Create evaluator-notes/README.md and evaluator-notes/manual-scoring-rubric.md. The rubric scores: source discovery, authority assessment, multi-source cross-referencing, claim verification accuracy, uncertainty labeling, structured output completeness.
7. Create evaluator-private/reference-sources.yaml with known authoritative source URLs for each harness-dimension pair. This is reviewer guidance only — not a whitelist.

8. Create profiles/controlled-web/:
   a. profile-contract.yaml declaring corpus_version, search_index_version, network_required: false, reset_strategy: static_corpus.
   b. public/tool-contract.yaml declaring search_corpus(query: string) → [{doc_id, title, snippet, score}] and fetch_document(doc_id: string) → {doc_id, title, content, url, source, retrieved_at}.
   c. service/search_service.py: Python stdlib search service. Loads search-index.json into memory at startup. search_corpus does basic term matching on the index (word tokenization, lowercase, term frequency scoring). fetch_document reads the corpus file for the given doc_id. Both return JSON via stdout. Interface: `python3 search_service.py search_corpus "query terms"` and `python3 search_service.py fetch_document DOC-001`.
   d. service/private/corpus/: HTML/text snapshot files. One per document. At minimum, cover 3 harnesses × 5 dimensions with 1-2 documents each (15-30 documents). Documents can be synthesized Markdown or text files that resemble official documentation covers:
      - Skill Installation (VitaClaw, OpenClaw, Hermes)
      - Tool Invocation (VitaClaw, OpenClaw, Hermes)
      - Sandbox (VitaClaw, OpenClaw, Hermes)
      - Licensing (VitaClaw, OpenClaw, Hermes)
      - Offline Deployment (VitaClaw, OpenClaw, Hermes)
   e. service/private/search-index.json: JSON object mapping terms → [{doc_id, score}]. Generate from the corpus files by tokenizing and computing simple TF scores.
   f. service/private/corpus-manifest.json: JSON object with document count, last_updated, and list of {doc_id, title, source, dimension}.

9. Create profiles/live-web/profile-contract.yaml with network_required: true, determinism: non_deterministic_by_nature, freshness_requirement: sources_must_be_retrieved_during_run.

AFTER CREATION:
- Run lsp_diagnostics on search_service.py.
- Verify search service responds.

SMOKE TEST:
```bash
cd tasks/task-006/profiles/controlled-web/service
python3 search_service.py search_corpus "VitaClaw"
# Expected: List of doc_ids with titles and snippets mentioning VitaClaw
python3 search_service.py fetch_document DOC-001
# Expected: Full document content
python3 search_service.py search_corpus "sandbox Docker"
# Expected: Documents about sandboxing (may include OpenClaw, Hermes)
```

MUST NOT DO:
- Do not create real web scraping or live internet access code.
- Do not create adapter implementations.
- Do not add expected answers, solution logic, or autograding.
- Do not create a search service for the live-web profile (live-web uses harness-native search only).
- Do not use external data or network calls during corpus building — synthesize representative documentation snapshots.

CONTEXT:
- The corpus is runtime-private. Agent cannot list/read files under profiles/controlled-web/service/private/.
- Agent tools: search_corpus and fetch_document only.
- The corpus content is representative synthetic documentation, not real web pages. Content should be realistic enough for the research task but does not need to reflect actual current documentation (evaluators have reference sources for ground truth).
- Live-web profile has minimal structure — profile-contract.yaml only. No service, no corpus.
- The output schemas (source-register.json with source_id/url/title/retrieved_at/authority_tier, research-findings.json with claim_id/harness/dimension/support_status/evidence_status/source_ids) must match the spec exactly.

ACCEPTANCE CRITERIA:
- search_corpus returns matching documents for all 5 dimensions across the 3 harnesses.
- fetch_document returns full document content.
- Controlled-web profile contract references the search service.
- Live-web profile contract references harness-native search.
- No v1 legacy inputs/ directory exists under tasks/task-006/.
- Corpus covers all 5 research dimensions for all 3 harnesses (minimum 15 documents).
```

- [ ] **Correctness reviewer subagent: Read-only review of task-006 implementation**

Prompt via `task(subagent_type='oracle', run_in_background=true)`:

```
TASK: Review the implemented task-006 files against the spec and goal review checklist. Do not write code.

EXPECTED OUTCOME: Pass/fail with specific findings.

REQUIRED TOOLS: Read only.

MUST DO:
- Read every file under tasks/task-006/.
- Verify capability-contract.yaml and environment-contract.yaml match spec.
- Verify task.md includes the research dimensions, dual-profile instructions, and output schemas.
- Verify controlled-web profile-contract.yaml and tool-contract.yaml match spec.
- Verify live-web profile-contract.yaml exists and is minimal.
- Verify search_service.py has search_corpus and fetch_document.
- Verify the corpus covers all 5 dimensions for all 3 harnesses.
- Verify search-index.json and corpus-manifest.json exist and are valid JSON.
- Verify evaluator-private/reference-sources.yaml exists.
- Verify output schemas match spec (source-register.json, research-findings.json, comparison-table.csv).
- Verify no evaluator content leaks into agent-visible files.
- Verify v1 inputs/ directory does not exist.

MUST NOT DO:
- Do not edit any files.

ACCEPTANCE CRITERIA:
- All checks pass, or specific fix requirements are enumerated.
```

- [ ] **Main session smoke verification: Task 006 search service**

```bash
cd tasks/task-006/profiles/controlled-web/service
python3 search_service.py search_corpus "VitaClaw skill installation"
python3 search_service.py search_corpus "OpenClaw sandbox"
python3 search_service.py search_corpus "Hermes licensing"
python3 search_service.py fetch_document DOC-001
```

Expected: Each command returns valid JSON. Search returns relevant documents. Fetch returns full content.

- [ ] **Main session: Run full contract tests to verify no regression**

Run: `python3 -m unittest discover tests -v`
Expected: All tests pass.

- [ ] **Commit**

```bash
git add tasks/task-006/
git rm -r tasks/task-006/inputs/ 2>/dev/null || rm -rf tasks/task-006/inputs/
git add tasks/task-006/
git commit -m "feat(task-006): add web research task with controlled-web corpus and dual profiles"
```

---

## Wave 3: Evaluator and Distribution Alignment

After all three lanes are committed, align the evaluator assets and distribution contract.

### Task 3.1: Update evaluator-notes for tasks 002-003

**Files:**
- Modify: `tasks/task-002/evaluator-notes/manual-scoring-rubric.md`
- Modify: `tasks/task-002/evaluator-notes/reference-analysis.md`
- Modify: `tasks/task-003/evaluator-notes/manual-scoring-rubric.md`
- Modify: `tasks/task-003/evaluator-notes/reference-analysis.md`

**Note:** Tasks 002-003 had their capability contracts and task.md updated but their evaluator notes may still reference v1 scoring criteria, decision frameworks, or reference analysis. These must be brought in line with the v2 spec. Task 001 has no evaluator-notes directory — it only gained a capability contract, which does not change evaluator material.

- [ ] **Main session: Check whether evaluator-notes for tasks 002-003 need updating**

Read `tasks/task-002/evaluator-notes/`, `tasks/task-003/evaluator-notes/`. If evaluator notes reference v1 content that has changed (e.g., task-003 evaluator notes still reference the old compliance-report.json instead of approval-decision.json), update them.

- [ ] **If needed: Implementation subagent for evaluator note updates**

```
TASK: Update evaluator notes for tasks 002-003 to align with v2 spec.

EXPECTED OUTCOME: Evaluator notes reference v2 decision frameworks, output formats, and scoring criteria.

REQUIRED TOOLS: Read, apply_patch.

MUST DO:
- Update task-002 evaluator notes: scoring rubric should reference confirmed facts + reasonable inferences + unknowns per spec §6.2.
- Update task-003 evaluator notes: scoring rubric should reference APPROVE/HOLD/REJECT/ESCALATE decisions, the veto layer from spec §6.3, and the new approval-decision.json schema. Remove references to compliance-report.json.

MUST NOT DO:
- Do not add hidden answers or solution logic.
- Do not modify agent-visible files (task.md, inputs/, output-requirements.md).

CONTEXT:
- The v1 evaluator notes still exist from the archive process and may have been copied forward.
- The v2 spec changes task-003 output from compliance-report.json to approval-decision.json.
- Task 001 has no evaluator-notes directory — it only gained a capability contract, which does not change evaluator material.
```

- [ ] **Commit evaluator note updates**

```bash
git add tasks/task-002/evaluator-notes/ tasks/task-003/evaluator-notes/
git commit -m "docs: update evaluator notes for v2 task content"
```

### Task 3.2: Verify distribution builder produces correct packages

- [ ] **Main session: Build all distribution targets and verify**

```bash
mkdir -p /tmp/arev2-dist-test
python3 scripts/build-distribution.py --target agent --output /tmp/arev2-dist-test/agent
python3 scripts/build-distribution.py --target runtime --task task-004 --output /tmp/arev2-dist-test/runtime-004
python3 scripts/build-distribution.py --target runtime --task task-005 --output /tmp/arev2-dist-test/runtime-005
python3 scripts/build-distribution.py --target runtime --task task-006 --output /tmp/arev2-dist-test/runtime-006
python3 scripts/build-distribution.py --target evaluator --output /tmp/arev2-dist-test/evaluator
```

Verify:
- Agent package: no evaluator-notes/, no evaluator-private/, no service/, no private/
- Agent package: has all 6 task.md, all 6 capability-contract.yaml, all inputs for 001-003
- Agent package: task-004 has no inputs/ directory, has environment-contract.yaml
- Runtime-004 package: has base-project/
- Runtime-005 package: has service/, private/
- Runtime-006 package: has profiles/controlled-web/service/
- Evaluator package: has evaluator-notes/ for tasks 002-006 (task 001 has no evaluator-notes directory)
- All packages have package-manifest.json

- [ ] **If distribution builder fails on any target, fix it**

```
TASK: Fix scripts/build-distribution.py to correctly classify all files in the new task-004/005/006 structures.

EXPECTED OUTCOME: All distribution targets produce correct packages per the distribution contract.

REQUIRED TOOLS: Read, apply_patch, bash.

MUST DO:
- Identify why the builder is missing or misclassifying files in the new task directories.
- Update distribution-contract.yaml patterns or the builder Python code as needed.
- Re-verify all targets produce correct output.

MUST NOT DO:
- Do not change the distribution contract's intent — only fix pattern matching.

CONTEXT:
- Distribution contract: contracts/distribution-contract.yaml
- Builder: scripts/build-distribution.py
- The builder uses glob patterns from the distribution contract.
```

- [ ] **Commit distribution fixes (if any)**

```bash
git add contracts/distribution-contract.yaml scripts/build-distribution.py
git commit -m "fix: distribution builder correctly classifies new task environment files"
```

---

## Wave 4: Deterministic Verification

### Task 4.1: Full contract test suite

- [ ] **Main session: Run complete contract tests**

```bash
python3 -m unittest discover tests -v
```

Expected: All tests pass. If any fail, determine whether the test needs updating or the implementation needs fixing. File the appropriate fix.

### Task 4.2: Task-004 deterministic verification

- [ ] **Main session: Fresh copy of base-project, verify 3 FAIL 2 OK**

```bash
mkdir -p /tmp/arev2-t004/project && cp -r tasks/task-004/environment/base-project/* /tmp/arev2-t004/project/ && cd /tmp/arev2-t004/project && python3 -m unittest discover -s tests -v 2>&1
```

Record the output as evidence. Expected: 3 FAIL, 2 OK, 0 ERRORS.

- [ ] **Main session: Verify that fixing all 3 bugs produces 5 OK**

Manually fix the bugs in /tmp/arev2-t004/project/src/:
1. Fix mapper.py: change `customer_name` match to `customer_ref` match
2. Fix reconcile.py: convert amounts to float before comparison (not string)
3. Fix reconcile.py: add null check before `.lower()`

```bash
cd /tmp/arev2-t004/project && python3 -m unittest discover -s tests -v 2>&1
```

Expected: 5 OK.

```bash
cd /tmp/arev2-t004/project && python3 src/reconcile.py
```

Expected: Generates reconciliation-report.json with valid content.

- [ ] **Main session: After verification, clean up temp files**

```bash
rm -rf /tmp/arev2-t004
```

### Task 4.3: Task-005 deterministic verification

- [ ] **Main session: Verify task-005 tools and state machine**

```bash
cd tasks/task-005/environment/service
python3 tool_api.py list_requests
python3 tool_api.py get_final_state
```

Record the output. Expected: 6 requests, all status "pending".

- [ ] **Main session: Verify reset determinism**

```bash
python3 tool_api.py approve_request REQ-001
python3 tool_api.py get_final_state  # REQ-001 is now approved
python3 tool_api.py reset
python3 tool_api.py get_final_state  # All pending again
```

Expected: Reset restores all requests to pending state.

### Task 4.4: Task-006 deterministic verification

- [ ] **Main session: Verify controlled-web search produces consistent results**

```bash
cd tasks/task-006/profiles/controlled-web/service
python3 search_service.py search_corpus "VitaClaw" > /tmp/t006-r1.json
python3 search_service.py search_corpus "VitaClaw" > /tmp/t006-r2.json
diff /tmp/t006-r1.json /tmp/t006-r2.json
```

Expected: No diff (same query, same corpus, deterministic).

```bash
python3 search_service.py fetch_document DOC-001
```

Expected: Returns full document content.

### Task 4.5: Clean temp files

- [ ] **Main session: Remove all temp files**

```bash
rm -rf /tmp/arev2-* /tmp/t004-* /tmp/t006-* /tmp/t004-smoke
```

---

## Wave 5: Real OpenCode UAT

Run each task through OpenCode with DeepSeek models. Record results in a UAT ledger.

### Task 5.1: Build agent package for UAT

- [ ] **Main session: Build clean agent package**

```bash
mkdir -p /tmp/arev2-uat
python3 scripts/build-distribution.py --target agent --output /tmp/arev2-uat/skill
```

- [ ] **Main session: Verify agent package isolation**

```bash
# Check no evaluator content leaked
rtk rg -l "evaluator" /tmp/arev2-uat/skill/ 2>/dev/null | head -5
# Expected: only capability-contract.yaml references (which have "evaluator" in their excluded paths section maybe)
# Better: list all top-level files
ls -R /tmp/arev2-uat/skill/
```

Expected: No evaluator-notes/, no evaluator-private/, no environment/private/, no environment/service/, no profiles/*/service/ directories.

### Task 5.2: OpenCode UAT runs (using subagents)

Each UAT run uses a subagent with the `skill` tool loading the agent-readiness-eval skill.

UAT BLOCKED: Real OpenCode UAT requires the skill to be installed in a harness and triggered with `评测`. This cannot be fully automated within this plan's scope. Record that UAT is BLOCKED until the skill is installed in a real harness (OpenCode, Codex, or other).

**What can be verified without a harness:**
- All files are syntactically correct (Python, YAML, JSON, CSV)
- All smoke tests pass (task-004 base project, task-005 tool API, task-006 search service)
- All contract tests pass
- Distribution builder produces correct packages

- [ ] **Main session: Record UAT blocker in run ledger**

Document: "Real OpenCode UAT blocked — requires skill installation in a harness. All structural, deterministic, and contract-based verification is complete and passing."

### Task 5.3: Build all distribution targets

- [ ] **Main session: Build and verify all targets one final time**

```bash
python3 scripts/build-distribution.py --target agent --output /tmp/arev2-final/agent 2>&1
python3 scripts/build-distribution.py --target runtime --task task-004 --output /tmp/arev2-final/runtime-004 2>&1
python3 scripts/build-distribution.py --target runtime --task task-005 --output /tmp/arev2-final/runtime-005 2>&1
python3 scripts/build-distribution.py --target runtime --task task-006 --output /tmp/arev2-final/runtime-006 2>&1
python3 scripts/build-distribution.py --target evaluator --output /tmp/arev2-final/evaluator 2>&1
```

```bash
rm -rf /tmp/arev2-final
```

---

## Wave 6: Reports

### Task 6.1: Write implementation summary

**Files:**
- Create: `docs/core-v2-implementation-summary.md`

**Content:** Summary of all changes per task, architecture layers created, design decisions.

- [ ] **Implementation subagent: Write implementation summary**

```
TASK: Write docs/core-v2-implementation-summary.md — a concise summary of what was built.

EXPECTED OUTCOME: A Markdown document covering what was implemented per task, what changed from v1, and key architecture decisions.

REQUIRED TOOLS: Read, write.

MUST DO:
- Read the current state of key files (SKILL.md, README.md, contracts/, tasks/ tree).
- Summarize for each task what changed from v1.
- Document the distribution contract and builder.
- Document the archive structure.
- Keep it concise (2-3 pages max).

MUST NOT DO:
- Do not include implementation dates or author names.
- Do not include speculative future work.
- Do not include UAT results (separate report).

ACCEPTANCE CRITERIA:
- All 6 tasks are covered.
- Architecture layers are documented.
- Distribution contract and builder are documented.
- Changes from v1 are summarized.
```

### Task 6.2: Write UAT report

**Files:**
- Create: `docs/core-v2-uat-report.md`

**Content:** What was tested, what was verified, what is blocked.

- [ ] **Implementation subagent: Write UAT report**

```
TASK: Write docs/core-v2-uat-report.md — a record of what was verified and what remains blocked for UAT.

EXPECTED OUTCOME: A Markdown document covering all smoke tests, contract tests, deterministic verification, and known UAT blockers.

REQUIRED TOOLS: Read, write.

MUST DO:
- Document every smoke test that was run and its result.
- Document contract test results.
- Document deterministic verification (task-004 3/5 fail, task-005 reset, task-006 search determinism).
- Document UAT blocker: real harness installation not yet done.
- Use tables for test results.

MUST NOT DO:
- Do not fabricate UAT results that were not actually run.
- Do not claim completion for blocked items.

ACCEPTANCE CRITERIA:
- Every verification step from Waves 0-5 is recorded.
- BLOCKED items are clearly marked.
- Results are factual, not aspirational.
```

### Task 6.3: Write run ledger

**Files:**
- Create: `docs/core-v2-run-ledger.md`

**Content:** Git revision, branch, and immutable record of what was delivered.

- [ ] **Main session: Write run ledger**

```bash
echo "# Core v2.0 Run Ledger" > docs/core-v2-run-ledger.md
echo "" >> docs/core-v2-run-ledger.md
echo "**Branch:** \`$(git rev-parse --abbrev-ref HEAD)\`" >> docs/core-v2-run-ledger.md
echo "**Revision:** \`$(git rev-parse HEAD)\`" >> docs/core-v2-run-ledger.md
echo "**Date:** $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> docs/core-v2-run-ledger.md
echo "" >> docs/core-v2-run-ledger.md
echo "## Commit Log" >> docs/core-v2-run-ledger.md
echo "" >> docs/core-v2-run-ledger.md
git log --oneline --no-decorate >> docs/core-v2-run-ledger.md
echo "" >> docs/core-v2-run-ledger.md
echo "## Files" >> docs/core-v2-run-ledger.md
echo "" >> docs/core-v2-run-ledger.md
echo '```' >> docs/core-v2-run-ledger.md
git ls-files >> docs/core-v2-run-ledger.md
echo '```' >> docs/core-v2-run-ledger.md
```

### Task 6.4: Commit reports

- [ ] **Commit**

```bash
git add docs/core-v2-implementation-summary.md docs/core-v2-uat-report.md docs/core-v2-run-ledger.md
git commit -m "docs: add v2 implementation summary, UAT report, and run ledger"
```

---

## Wave 7: Final Clean Check

### Task 7.1: Verify git status

- [ ] **Main session: Check git status is clean**

```bash
git status
```

Expected: Clean working tree (or only intentionally uncommitted artifacts like /tmp files).

### Task 7.2: Verify branch is up to date

- [ ] **Main session: Check branch log**

```bash
git log --oneline -20
```

Expected: All commits from Waves 0-6 present. No merge commits unless intentional.

### Task 7.3: Final smoke test pass

- [ ] **Main session: Run complete test suite one final time**

```bash
python3 -m unittest discover tests -v 2>&1
```

Expected: All tests pass.

### Task 7.4: Final distribution build

- [ ] **Main session: Build and verify all targets one final time**

```bash
python3 scripts/build-distribution.py --target agent --output /tmp/arev2-final-check/agent 2>&1
python3 scripts/build-distribution.py --target evaluator --output /tmp/arev2-final-check/evaluator 2>&1
```

Verify: agent package has no evaluator files. Evaluator package has evaluator-notes for tasks 002-006 (task 001 has no evaluator-notes directory).

```bash
rm -rf /tmp/arev2-final-check
```

---

## Commit Plan (Remaining)

| # | Message | Files |
|---|---------|-------|
| 1 | `fix: UAT refinements — task-003 rejection framing, REJECT vs HOLD guidance, template env_version default` | tasks/task-003/inputs/, tasks/task-003/task.md, templates/run-metadata.json |
| 2 | `test: upgrade contract tests for v2 distribution contract and per-task environment validation` | tests/test_core_v2_contract.py |
| 3 | `feat(task-004): add coding & repair task with bug-injected Python project` | tasks/task-004/ (new), - tasks/task-004/inputs/ (deleted) |
| 4 | `feat(task-005): add stateful tool use task with SQLite service and audit logging` | tasks/task-005/ (new), - tasks/task-005/inputs/ (deleted) |
| 5 | `feat(task-006): add web research task with controlled-web corpus and dual profiles` | tasks/task-006/ (new), - tasks/task-006/inputs/ (deleted) |
| 6 | `docs: update evaluator notes for v2 task content` | tasks/*/evaluator-notes/ |
| 7 | `fix: distribution builder correctly classifies new task environment files` (if needed) | contracts/, scripts/ |
| 8 | `docs: add v2 implementation summary, UAT report, and run ledger` | docs/ |
