from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
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

    def test_task_has_question_pack_shape_without_hidden_answer_code(self) -> None:
        task = ROOT / "tasks" / "task-001"
        self.assertTrue((task / "task.md").is_file())
        self.assertTrue((task / "inputs" / "data.json").is_file())
        self.assertTrue((task / "output-requirements.md").is_file())
        forbidden_names = {"ver" + "ifier.py", "solution.py", "answer.json", "ground_truth.json"}
        actual_names = {path.name for path in task.rglob("*")}
        self.assertTrue(forbidden_names.isdisjoint(actual_names))

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


if __name__ == "__main__":
    unittest.main()
