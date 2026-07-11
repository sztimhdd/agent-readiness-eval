from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALL_TASKS = sorted(
    d for d in (ROOT / "tasks").iterdir()
    if d.is_dir() and d.name.startswith("task-")
)
NON_STATIC = {"task-004", "task-005", "task-006"}
# Tasks that exist on disk but are excluded from the current release
EXCLUDED_FROM_RELEASE: set[str] = {"task-006"}
FORBIDDEN_PATHS = ["run" + "ner", "sco" + "rer", "schemas", "task", "taskpacks", ".vitaclaw_eval" + "_runs"]
FORBIDDEN_TERMS = [
    "Local" + "Executor",
    "run_readiness" + "_eval",
    "eval" + "_v0.py",
    "ver" + "ifier.py",
    "judge" + "_output",
    "evi" + "dence bun" + "dle",
]


class CoreV2ContractTests(unittest.TestCase):
    def test_package_has_only_portable_v3_top_level_shape(self) -> None:
        existing = {path.name for path in ROOT.iterdir()}
        self.assertTrue({"SKILL.md", "README.md", "skill.json", "tasks", "templates", "docs", "tests", "contracts", "archive", "scripts"}.issubset(existing))
        for forbidden in FORBIDDEN_PATHS:
            self.assertFalse((ROOT / forbidden).exists(), forbidden)

    def test_each_task_has_question_pack_shape_without_hidden_answer_code(self) -> None:
        for task_dir in ALL_TASKS:
            with self.subTest(task=task_dir.name):
                self.assertTrue((task_dir / "task.md").is_file(),
                    f"{task_dir.name}: missing task.md")
                if task_dir.name not in NON_STATIC:
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
        tasks = manifest.get("tasks", [])
        # v2 tasks are structured objects with "id" field
        if tasks and isinstance(tasks[0], dict):
            declared = {t["id"] for t in tasks}
        else:
            declared = set(tasks)
        on_disk = {d.name for d in ALL_TASKS}
        # Exclude tasks intentionally held back from this release
        on_disk -= EXCLUDED_FROM_RELEASE
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
        self.assertIn("run_status", metadata)
        self.assertIn("web_activity_evidence", metadata)

    def test_active_docs_do_not_reference_legacy_execution_architecture(self) -> None:
        checked_files = [ROOT / "SKILL.md", ROOT / "README.md", ROOT / "skill.json"] + sorted((ROOT / "docs").glob("*.md"))
        combined = "\n".join(path.read_text(encoding="utf-8") for path in checked_files)
        for term in FORBIDDEN_TERMS:
            self.assertNotIn(term, combined, term)

    def test_skill_does_not_disable_the_file_tools_required_by_tasks(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("allowed-tools: []", skill)
        self.assertIn("评测 task-001", skill)
        self.assertIn("<run-id>", skill)

    def test_codex_install_guide_documents_the_leakage_free_projection(self) -> None:
        guide = (ROOT / "docs" / "INSTALL-CODEX.md").read_text(encoding="utf-8")
        self.assertIn("~/.codex/skills/agent-readiness-eval", guide)
        self.assertIn("evaluator-notes", guide)
        self.assertIn("three", guide)


    def test_skill_json_has_structured_tasks(self) -> None:
        manifest = json.loads((ROOT / "skill.json").read_text(encoding="utf-8"))
        tasks = manifest.get("tasks", [])
        self.assertTrue(len(tasks) > 0, "skill.json must have at least one task")
        for t in tasks:
            with self.subTest(task=t.get("id", "unknown")):
                self.assertIn("id", t)
                self.assertIn("task_version", t)
                self.assertIn("environment_type", t)

    def test_agent_package_excludes_leaked_sensitive_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "build-distribution.py"),
                 "--target", "agent", "--output", tmpdir],
                check=True, capture_output=True, text=True,
            )
            output_path = Path(tmpdir)
            all_files = [str(p.relative_to(output_path)) for p in output_path.rglob("*") if p.is_file()]
            forbidden_patterns = [
                "evaluator-notes/",
                "evaluator-private/",
                "environment/private/",
                "environment/service/",
            ]
            for fpath in all_files:
                for forbidden in forbidden_patterns:
                    self.assertNotIn(forbidden, fpath,
                        f"Leaked path in agent package: {fpath} contains {forbidden}")
            # profiles/*/service/ — profile dir with a service/ subdir
            profile_service_re = re.compile(r"profiles/[^/]+/service/")
            for fpath in all_files:
                self.assertIsNone(profile_service_re.search(fpath),
                    f"Leaked profile service in agent package: {fpath}")


if __name__ == "__main__":
    unittest.main()
