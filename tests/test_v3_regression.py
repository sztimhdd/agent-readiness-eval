from __future__ import annotations

import hashlib
import json
import os
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALL_TASKS = sorted(
    d for d in (ROOT / "tasks").iterdir()
    if d.is_dir() and d.name.startswith("task-")
)


class V3RegressionTests(unittest.TestCase):
    """Verify V3 historical evidence is preserved unchanged."""

    def test_v3_task_directories_still_exist(self) -> None:
        on_disk = {d.name for d in ALL_TASKS}
        for task_id in ["task-001", "task-002", "task-003", "task-004", "task-005", "task-006"]:
            self.assertIn(task_id, on_disk)

    def test_v3_output_requirements_still_present(self) -> None:
        """V3 output-requirements.md files still exist (V4 adds new ones alongside)"""
        for task_dir in ALL_TASKS:
            if task_dir.name == "task-006":
                continue
            req = task_dir / "output-requirements.md"
            self.assertTrue(req.is_file(), f"{task_dir.name}: missing output-requirements.md")

    def test_v3_environment_tasks_still_have_environment(self) -> None:
        for task_id in ["task-004", "task-005"]:
            task_dir = ROOT / "tasks" / task_id
            self.assertTrue((task_dir / "environment-contract.yaml").is_file(),
                f"{task_id}: missing environment-contract.yaml")
            self.assertTrue((task_dir / "environment").is_dir(),
                f"{task_id}: missing environment/")

    def test_task_006_still_backlog_only(self) -> None:
        task_dir = ROOT / "tasks" / "task-006"
        self.assertTrue((task_dir / "task.md").is_file(),
            "task-006 task.md still exists")
        self.assertTrue((task_dir / "evaluator-notes").is_dir(),
            "task-006 evaluator-notes still exists")

    def test_v3_evaluator_notes_untouched(self) -> None:
        """V3 evaluator-only assets not modified"""
        for task_id in ["task-002", "task-003", "task-004", "task-005"]:
            notes_dir = ROOT / "tasks" / task_id / "evaluator-notes"
            self.assertTrue(notes_dir.is_dir(),
                f"{task_id}: evaluator-notes removed")

    def test_skill_md_preserves_v3_harness_instructions(self) -> None:
        """V3 harness execution instructions are preserved in V4"""
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("### VitaClaw", skill)
        self.assertIn("### OpenCode", skill)
        self.assertIn("### Codex", skill)
        self.assertIn("### Hermes", skill)
        self.assertIn("Never use `exec`, `cat`, `find`, `list_dir`", skill)

    def test_skill_md_preserves_tool_authorization_tables(self) -> None:
        """Task capability tables from V3 are preserved in V4"""
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("This Skill does not declare `allowed-tools`.", skill)
        self.assertIn("The external controller binds the correct Profile per task per harness.", skill)

    def test_v3_contract_tests_still_run(self) -> None:
        """test_core_v2_contract.py still exists (V3 structural checks preserved)"""
        self.assertTrue((ROOT / "tests" / "test_core_v2_contract.py").is_file())

    def test_archive_v1_preserved(self) -> None:
        """v1-question-pack still exists"""
        self.assertTrue((ROOT / "archive" / "v1-question-pack").is_dir())

    def test_v3_answer_dir_format_documented(self) -> None:
        """V4 SKILL.md documents V3 as historical evidence"""
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("V3 Historical Evidence", readme)

    def test_v4_not_backward_compatible_with_v3(self) -> None:
        """V4 does not add V3 compatibility shims"""
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("V3 compat", skill.lower())
        self.assertNotIn("backward compat", skill.lower())

    @unittest.skipUnless(
        os.environ.get("AGENT_EVAL_V3_RELEASE_CHECKOUT"),
        "release-management V3 checkout unavailable",
    )
    def test_v3_manifest_hashes_match_release_checkout(self) -> None:
        checkout = Path(os.environ["AGENT_EVAL_V3_RELEASE_CHECKOUT"])
        manifest_path = ROOT / "docs" / "v3-evidence" / "v3.0.0-package-manifest.json"
        self.assertTrue(manifest_path.is_file(),
            f"Frozen manifest missing: {manifest_path}")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        files = manifest["files"]
        self.assertIsInstance(files, list)

        for entry in files:
            path = entry["path"]
            expected_sha = entry["sha256"]
            file_path = checkout / path
            self.assertTrue(file_path.is_file(),
                f"Missing in checkout: {path}")
            actual_sha = hashlib.sha256(file_path.read_bytes()).hexdigest()
            self.assertEqual(actual_sha, expected_sha,
                f"SHA-256 mismatch for {path}")


if __name__ == "__main__":
    unittest.main()
