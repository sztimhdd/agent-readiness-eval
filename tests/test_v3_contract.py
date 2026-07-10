from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALL_TASKS = sorted(
    d for d in (ROOT / "tasks").iterdir()
    if d.is_dir() and d.name.startswith("task-")
)
FORBIDDEN_PATHS = ["run" + "ner", "sco" + "rer", "schemas", "scripts", "task", "taskpacks", ".vitaclaw_eval" + "_runs"]
FORBIDDEN_TERMS = [
    "Local" + "Executor",
    "run_readiness" + "_eval",
    "eval" + "_v0.py",
    "ver" + "ifier.py",
    "judge" + "_output",
    "evi" + "dence bun" + "dle",
    "state" + " machine",
]


class V3ContractTests(unittest.TestCase):
    def test_package_has_only_portable_v3_top_level_shape(self) -> None:
        existing = {path.name for path in ROOT.iterdir()}
        self.assertTrue({"SKILL.md", "README.md", "skill.json", "tasks", "templates", "docs", "tests"}.issubset(existing))
        for forbidden in FORBIDDEN_PATHS:
            self.assertFalse((ROOT / forbidden).exists(), forbidden)

    def test_each_task_has_question_pack_shape_without_hidden_answer_code(self) -> None:
        for task_dir in ALL_TASKS:
            with self.subTest(task=task_dir.name):
                self.assertTrue((task_dir / "task.md").is_file(),
                    f"{task_dir.name}: missing task.md")
                self.assertTrue((task_dir / "inputs").is_dir(),
                    f"{task_dir.name}: missing inputs/")
                self.assertTrue((task_dir / "output-requirements.md").is_file(),
                    f"{task_dir.name}: missing output-requirements.md")
                forbidden_names = {"ver" + "ifier.py", "solution.py", "answer.json", "ground_truth.json"}
                actual_names = {path.name for path in task_dir.rglob("*")}
                overlap = forbidden_names & actual_names
                self.assertTrue(len(overlap) == 0,
                    f"{task_dir.name}: forbidden files found: {overlap}")

    def test_skill_json_tasks_match_on_disk_directories(self) -> None:
        manifest = json.loads((ROOT / "skill.json").read_text(encoding="utf-8"))
        declared = set(manifest.get("tasks", []))
        on_disk = {d.name for d in ALL_TASKS}
        missing_from_manifest = on_disk - declared
        extra_in_manifest = declared - on_disk
        self.assertTrue(len(missing_from_manifest) == 0,
            f"Tasks on disk not in skill.json: {missing_from_manifest}")
        self.assertTrue(len(extra_in_manifest) == 0,
            f"Tasks in skill.json not on disk: {extra_in_manifest}")

    def test_metadata_template_uses_unavailable_for_unknown_observability(self) -> None:
        metadata = json.loads((ROOT / "templates" / "run-metadata.json").read_text(encoding="utf-8"))
        self.assertEqual(metadata["input_tokens"], "UNAVAILABLE")
        self.assertEqual(metadata["output_tokens"], "UNAVAILABLE")
        self.assertEqual(metadata["total_tokens"], "UNAVAILABLE")
        self.assertEqual(metadata["tool_calls"], "UNAVAILABLE")

    def test_active_docs_do_not_reference_legacy_execution_architecture(self) -> None:
        checked_files = [ROOT / "SKILL.md", ROOT / "README.md", ROOT / "skill.json"] + sorted((ROOT / "docs").glob("*.md"))
        combined = "\n".join(path.read_text(encoding="utf-8") for path in checked_files)
        for term in FORBIDDEN_TERMS:
            self.assertNotIn(term, combined, term)

    def test_skill_does_not_disable_the_file_tools_required_by_tasks(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("allowed-tools: []", skill)
        self.assertIn("评测 task-001", skill)

    def test_codex_install_guide_documents_the_leakage_free_projection(self) -> None:
        guide = (ROOT / "docs" / "INSTALL-CODEX.md").read_text(encoding="utf-8")
        self.assertIn("~/.codex/skills/agent-readiness-eval", guide)
        self.assertIn("evaluator-notes", guide)
        self.assertIn("three", guide)


if __name__ == "__main__":
    unittest.main()
