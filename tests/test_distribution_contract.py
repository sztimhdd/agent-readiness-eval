from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _declared_task_ids() -> set[str]:
    manifest = json.loads((ROOT / "skill.json").read_text(encoding="utf-8"))
    return {task["id"] for task in manifest["tasks"]}


def _build_package(target: str, output: Path, task_id: str | None = None) -> dict[str, str | list[dict[str, str]]]:
    command = [
        sys.executable,
        str(ROOT / "scripts" / "build-distribution.py"),
        "--target",
        target,
        "--output",
        str(output),
    ]
    if task_id is not None:
        command.extend(["--task", task_id])
    subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads((output / "package-manifest.json").read_text(encoding="utf-8"))


def _manifest_paths(manifest: dict[str, str | list[dict[str, str]]]) -> list[str]:
    files = manifest["files"]
    if not isinstance(files, list):
        return []
    return [entry["path"] for entry in files]


class DistributionContractTests(unittest.TestCase):
    def test_packages_only_include_manifest_declared_task_paths(self) -> None:
        declared = _declared_task_ids()
        build_targets = [("agent", None), ("evaluator", None), ("runtime", "task-004"), ("runtime", "task-005")]
        with tempfile.TemporaryDirectory() as tmpdir:
            for target, task_id in build_targets:
                with self.subTest(target=target, task_id=task_id):
                    manifest = _build_package(target, Path(tmpdir) / f"{target}-{task_id or 'all'}", task_id)
                    for path in _manifest_paths(manifest):
                        if path.startswith("tasks/"):
                            self.assertIn(path.split("/", 2)[1], declared)
                        self.assertFalse(path.startswith("tasks/task-006/"), path)

    def test_package_manifest_records_canonical_package_digest(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            first = _build_package("agent", Path(tmpdir) / "first")
            second = _build_package("agent", Path(tmpdir) / "second")

        self.assertIn("source_commit", first)
        self.assertNotEqual(first["source_commit"], "")
        self.assertNotIn("file_set_sha256", first)
        self.assertIn("package_digest", first)
        self.assertEqual(first["package_digest"], second["package_digest"])

        files = first["files"]
        if not isinstance(files, list):
            self.fail("package manifest files must be a list")
        expected = hashlib.sha256(
            "".join(sorted(f"{entry['path']}:{entry['sha256']}" for entry in files)).encode("utf-8"),
        ).hexdigest()
        self.assertEqual(first["package_digest"], expected)

    def test_agent_package_includes_task005_vitaclaw_adapter(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest = _build_package("agent", Path(tmpdir) / "agent")
        self.assertIn("scripts/task005_tool.py", _manifest_paths(manifest))

    def test_agent_task005_adapter_runs_against_runtime_package(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            _build_package("agent", tmp / "agent")
            _build_package("runtime", tmp / "runtime", "task-005")

            tool_api = tmp / "runtime" / "tasks" / "task-005" / "environment" / "service" / "tool_api.py"
            result = subprocess.run(
                [
                    sys.executable,
                    str(tmp / "agent" / "scripts" / "task005_tool.py"),
                    json.dumps({"operation": "get_request", "run_id": "contract-smoke", "request_id": "REQ-001"}),
                ],
                check=False,
                capture_output=True,
                env={"AGENT_EVAL_TASK005_TOOL_API": str(tool_api)},
                text=True,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["request_id"], "REQ-001")

    def test_task005_runtime_package_excludes_generated_runtime_state(self) -> None:
        runtime_state_root = ROOT / "tasks" / "task-005" / "environment" / "service" / "runtime-state"
        pre_existed = runtime_state_root.exists()

        try:
            runtime_state_root.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(prefix="contract-leak-check-", dir=runtime_state_root) as state_tmp:
                state_dir = Path(state_tmp)
                (state_dir / "state.db").write_text("generated", encoding="utf-8")

                with tempfile.TemporaryDirectory() as tmpdir:
                    manifest = _build_package("runtime", Path(tmpdir) / "runtime", "task-005")

            for path in _manifest_paths(manifest):
                self.assertNotIn("/runtime-state/", path)
        finally:
            if not pre_existed:
                import shutil
                shutil.rmtree(runtime_state_root, ignore_errors=True)

    def test_runtime_state_fixture_cleaned_after_distribution_test(self) -> None:
        runtime_state_root = ROOT / "tasks" / "task-005" / "environment" / "service" / "runtime-state"
        pre_existed = runtime_state_root.exists()

        self.test_task005_runtime_package_excludes_generated_runtime_state()

        if not pre_existed:
            self.assertFalse(runtime_state_root.exists(),
                f"{runtime_state_root} was not cleaned after test_task005_runtime_package_excludes_generated_runtime_state")
        else:
            self.assertTrue(runtime_state_root.exists(),
                f"{runtime_state_root} was removed but pre-existed before the test")


if __name__ == "__main__":
    unittest.main()
