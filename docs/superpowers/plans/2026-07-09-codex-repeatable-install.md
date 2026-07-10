# Codex Repeatable Skill Installation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the question pack safely installable in Codex and document a repeatable, leakage-free evaluation procedure without adding a packaged runtime.

**Architecture:** Keep this repository as the authoring source. Codex receives a manually constructed projection containing only runtime-visible files; evaluator notes remain in the source repository but are never copied. The guide records immutable run parameters and requires new answer directories for each repeat.

**Tech Stack:** Markdown, JSON, Python standard-library unittest, Codex local Skills directory.

## Global Constraints

- Do not add packaged execution, grading, orchestration, result-packaging, or token-estimation code.
- Do not expose `evaluator-notes/` in the Codex-installed projection.
- Do not commit unrelated existing untracked files.
- Keep `runs/` local and gitignored.

---

### Task 1: Guard the Codex-facing Skill contract

**Files:**
- Modify: `tests/test_v3_contract.py`
- Modify: `SKILL.md`

**Interfaces:**
- Consumes: `SKILL.md` front matter and task protocol.
- Produces: a contract test that rejects an empty `allowed-tools` declaration and a protocol that names an explicit task invocation.

- [ ] **Step 1: Add a failing contract test**

Append this test to `V3ContractTests`:

```python
    def test_skill_does_not_disable_the_file_tools_required_by_tasks(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("allowed-tools: []", skill)
        self.assertIn("评测 task-001", skill)
```

- [ ] **Step 2: Run the test and verify it fails**

Run: `python3 -m unittest tests.test_v3_contract.V3ContractTests.test_skill_does_not_disable_the_file_tools_required_by_tasks`

Expected: failure because `SKILL.md` declares `allowed-tools: []` and does not contain the explicit invocation.

- [ ] **Step 3: Make the minimal protocol change**

Delete the `allowed-tools: []` front-matter line. Change the Trigger section to say that users invoke a named task, for example `评测 task-001`; retain a backwards-compatible default to task-001 only when no task is named.

- [ ] **Step 4: Run the focused and complete contract suites**

Run: `python3 -m unittest tests.test_v3_contract.V3ContractTests.test_skill_does_not_disable_the_file_tools_required_by_tasks && python3 -m unittest discover tests`

Expected: focused test passes and the complete suite has no failures.

### Task 2: Document the safe, repeatable Codex procedure

**Files:**
- Create: `docs/INSTALL-CODEX.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: the task protocol, `skill.json`, `templates/run-metadata.json`, and the local Codex Skills directory.
- Produces: exact manual projection commands, a run-record checklist, and a README link.

- [ ] **Step 1: Write a failing documentation-presence test**

Append this test to `V3ContractTests`:

```python
    def test_codex_install_guide_documents_the_leakage_free_projection(self) -> None:
        guide = (ROOT / "docs" / "INSTALL-CODEX.md").read_text(encoding="utf-8")
        self.assertIn("~/.codex/skills/agent-readiness-eval", guide)
        self.assertIn("evaluator-notes", guide)
        self.assertIn("three", guide)
```

- [ ] **Step 2: Run the test and verify it fails**

Run: `python3 -m unittest tests.test_v3_contract.V3ContractTests.test_codex_install_guide_documents_the_leakage_free_projection`

Expected: error because `docs/INSTALL-CODEX.md` does not exist.

- [ ] **Step 3: Add the guide and README reference**

The guide must: create a fresh temporary projection; copy only `SKILL.md`, `skill.json`, the metadata template, and the three agent-visible elements of each task; never copy `evaluator-notes`; replace the installed skill only after the projection is complete; state restart/new-task verification; and define a run ledger with source revision, install timestamp, Codex version, model/provider, task, run ID, and tool/sandbox policy. It must specify at least three independent runs per model/task comparison cell.

Add `INSTALL-CODEX.md` to the README package shape and installation-doc list.

- [ ] **Step 4: Run documentation and complete contract tests**

Run: `python3 -m unittest tests.test_v3_contract.V3ContractTests.test_codex_install_guide_documents_the_leakage_free_projection && python3 -m unittest discover tests`

Expected: focused test passes and the complete suite has no failures.

### Task 3: Verify the installed projection and initial evaluation

**Files:**
- Verify: `~/.codex/skills/agent-readiness-eval/`
- Verify: a fresh local `runs/task-001-<harness>-<model>-<run-id>/` directory

**Interfaces:**
- Consumes: the guide's projection procedure and Codex's installed-skill discovery.
- Produces: evidence that no evaluator-only content is installed and a valid Task 001 answer directory.

- [ ] **Step 1: Build the projection with the documented commands**

Run every command in the guide from the repository root. Before replacement, verify with:

```bash
find ~/.codex/skills/agent-readiness-eval -path '*/evaluator-notes/*' -print
```

Expected: no output.

- [ ] **Step 2: Start a fresh Codex task and invoke Task 001**

Use: `评测 task-001`.

Expected: Codex reads only task-001 agent-visible inputs and writes a newly named answer directory.

- [ ] **Step 3: Validate the answer-directory contract**

Run the existing task-001 file/JSON checks against the new directory and run `python3 -m unittest discover tests` in the source repository.

Expected: all required files exist; artifact and metadata parse as JSON; task ID is exact; unknown observability fields remain `UNAVAILABLE`; contract suite passes.
