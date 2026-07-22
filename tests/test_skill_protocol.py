from __future__ import annotations

import unittest
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELEASED_TASK_IDS = ("task-001", "task-002", "task-003", "task-004", "task-005")


def _markdown_section(text: str, heading: str) -> str:
    marker = f"{heading}\n"
    start = text.find(marker)
    if start == -1:
        return ""

    body_start = start + len(marker)
    level = len(heading.split(" ", 1)[0])
    body = text[body_start:]
    next_heading = re.search(rf"\n#{{1,{level}}} ", body)
    if next_heading is None:
        return body
    return body[:next_heading.start()]


class SkillProtocolTests(unittest.TestCase):
    def test_harness_native_execution_documents_each_supported_harness(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        harness_section = _markdown_section(skill, "## Harness-Native Execution")
        self.assertIn("## Harness-Native Execution", skill)
        self.assertEqual(harness_section.count("\n### "), 4)
        for heading in ["### VitaClaw", "### OpenCode", "### Codex", "### Hermes"]:
            with self.subTest(heading=heading):
                self.assertIn(heading, harness_section)

    def test_vitaclaw_uses_skill_resource_tools_not_shell_path_guesses(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        section = _markdown_section(skill, "### VitaClaw")
        self.assertIn('read_skill_file(skill_id="agent-readiness-eval", path="tasks/<task-id>/task.md")', section)
        self.assertIn("Never use `exec`, `cat`, `find`, `list_dir`, or guessed filesystem paths to read Skill files", section)
        self.assertIn("Skill directory is a read-only mount", section)
        self.assertIn("answers go under the workspace root", section)

    def test_other_harnesses_have_literal_file_access_and_activation_guidance(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        expected_by_harness = {
            "### OpenCode": [
                "OpenCode uses the native `Read` tool",
                "restart OpenCode or start a fresh session",
            ],
            "### Codex": [
                "Codex uses workspace file tools pointed at the projection directory",
                "workspace-read fallback is a non-canonical install mode",
            ],
            "### Hermes": [
                "Hermes uses workspace tools after install",
                "`file://` limitation requires a pre-staged bundle",
            ],
        }
        for heading, phrases in expected_by_harness.items():
            section = _markdown_section(skill, heading)
            for phrase in phrases:
                with self.subTest(heading=heading, phrase=phrase):
                    self.assertIn(phrase, section)

    def test_output_paths_are_workspace_root_anchored(self) -> None:
        required_directory = "<workspace-root>/runs/<task-id>-<harness>-<model>-<run-id>/"
        flat_output_rule = "Do not write `final-answer.md`, `run-metadata.json`, or `task-id.txt` at the workspace root."
        preflight_rule = "If you cannot determine the workspace root, stop and report preflight failure."

        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(required_directory, skill)
        self.assertIn(flat_output_rule, skill)
        self.assertIn(preflight_rule, skill)
        self.assertIn("writing answers into the Skill directory will fail silently or corrupt the projection", skill)
        self.assertNotIn("under `runs/`", skill)
        self.assertNotIn("\nruns/<task-id>", skill)
        self.assertIn(required_directory, readme)

        for task_id in RELEASED_TASK_IDS:
            path = ROOT / "tasks" / task_id / "output-requirements.md"
            with self.subTest(task_id=task_id):
                text = path.read_text(encoding="utf-8")
                self.assertIn(required_directory, text)
                self.assertIn(flat_output_rule, text)
                self.assertNotIn("\nruns/<task-id>", text)

    def test_completion_gate_requires_reverification_before_scored_status(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        gate = _markdown_section(skill, "## Completion Gate")
        required_phrases = [
            "Re-read the task's `output-requirements.md` using the harness-native read tool",
            "Verify every required filename exists under `answer/`",
            "Verify every required Markdown heading exists literally",
            "Verify every JSON file parses without error",
            "Verify every required JSON key and value type exactly matches the declared schema",
            "Verify `run-metadata.json` contains every key from `templates/run-metadata.json`",
            "Verify `task-id.txt` contains exactly the correct task ID",
            "Verify `answer/decision-log.md` is present",
            "Set `agent_reported_phase` to `answer_incomplete` when any required item is missing or invalid",
            "Only report completion after all checks pass",
        ]
        self.assertIn("Before reporting completion:", gate)
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, gate)

    def test_error_handling_table_blocks_common_invalid_completion_paths(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        table = _markdown_section(skill, "## Error Handling")
        required_rows = [
            "| Skill directory is read-only | Write answers under workspace root, never inside the Skill directory |",
            "| Workspace root is unknown | Stop and report preflight failure; do not guess paths |",
            "| Output directory already exists | Append a new unique `run-id` |",
            "| A required artifact cannot be created | Set `agent_reported_phase` to `answer_incomplete`, document missing artifacts in `run-metadata.json` |",
            "| JSON output does not parse | Fix before attempting to mark completion |",
            "| Required Markdown heading is missing | Fix before attempting to mark completion |",
            "| Static task (001, 002, 003) attempted via `exec` or shell command | Stop; static tasks must use file tools only. Restart with correct task profile |",
            "| Preflight returns `adapter_blocked` | No model score produced; fix adapter before retry |",
        ]
        self.assertIn("| Condition | Action |", table)
        for row in required_rows:
            with self.subTest(row=row):
                self.assertIn(row, table)

    def test_tool_authorization_declares_task_profiles_without_global_allowed_tools(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        section = _markdown_section(skill, "## Tool Authorization")
        required_rows = [
            "| 001 — Reading and Delivery | `read_skill_file`, `write_file` | static-eval | No `exec` |",
            "| 002 — Multi-Source Investigation | `read_skill_file`, `write_file` | static-eval | No `exec` |",
            "| 003 — Policy-Constrained Decision | `read_skill_file`, `write_file` | static-eval | No `exec` |",
            "| 004 — Coding & Repair | file tools + code edit + restricted `exec` | coding-eval | `exec` restricted to `python3 -m unittest` and `python3 -m src.reconcile` |",
            "| 005 — Stateful Tool Use | file tools + `skill_run`/`run_skill_script` | stateful-eval | VitaClaw: controller sets `AGENT_EVAL_TASK005_TOOL_API`, then use `skill_run` on `scripts/task005_tool.py`. Other harnesses: use canonical tool names per `environment/public/tool-contract.yaml`. |",
        ]
        self.assertNotIn("allowed-tools: []", skill)
        self.assertIn("This Skill does not declare `allowed-tools`.", section)
        self.assertIn("The external controller binds the correct Profile per task per harness.", section)
        for row in required_rows:
            with self.subTest(row=row):
                self.assertIn(row, section)

    def test_controller_contract_records_profile_binding_boundary(self) -> None:
        contract = (ROOT / "contracts" / "uat-controller-contract.yaml").read_text(encoding="utf-8")
        required_phrases = [
            "profile_bindings:",
            "task-001: static-eval",
            "task-002: static-eval",
            "task-003: static-eval",
            "task-004: coding-eval",
            "task-005: stateful-eval",
            "static-eval: [filesystem.list, filesystem.read, filesystem.write_answer]",
            "coding-eval: [filesystem.read, filesystem.write_answer, code.edit, code.exec]",
            "stateful-eval: [filesystem.read, filesystem.write_answer, stateful.read, stateful.write]",
            "The controller binds Profiles; the Skill does not declare allowed-tools.",
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, contract)


if __name__ == "__main__":
    unittest.main()
