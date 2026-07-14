import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELEASED_ENVIRONMENT_TASKS = {"task-004", "task-005"}


class StagedEnvironmentContractTests(unittest.TestCase):
    def test_task_004_has_environment(self) -> None:
        task_dir = ROOT / "tasks" / "task-004"
        self.assertTrue((task_dir / "environment-contract.yaml").is_file(),
            "task-004 missing environment-contract.yaml")
        self.assertTrue((task_dir / "environment" / "base-project").is_dir(),
            "task-004 missing environment/base-project/")
        self.assertTrue((task_dir / "environment" / "base-project" / "tests").is_dir(),
            "task-004 missing environment/base-project/tests/")
        self.assertTrue((task_dir / "environment" / "base-project" / "src").is_dir(),
            "task-004 missing environment/base-project/src/")

    def test_task_005_has_environment(self) -> None:
        task_dir = ROOT / "tasks" / "task-005"
        self.assertTrue((task_dir / "environment" / "public" / "tool-contract.yaml").is_file(),
            "task-005 missing environment/public/tool-contract.yaml")
        self.assertTrue((task_dir / "environment" / "private").is_dir(),
            "task-005 missing environment/private/")
        self.assertTrue((task_dir / "environment" / "service" / "tool_api.py").is_file(),
            "task-005 missing environment/service/tool_api.py")

    def test_released_environment_tasks_do_not_use_inputs_dir(self) -> None:
        for task_id in RELEASED_ENVIRONMENT_TASKS:
            task_dir = ROOT / "tasks" / task_id
            with self.subTest(task=task_id):
                self.assertFalse((task_dir / "inputs").exists(),
                    f"{task_id} should not have inputs/ — uses environment instead")

    def test_build_agent_package_excludes_runtime_private(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "build-distribution.py"),
                 "--target", "agent", "--output", tmpdir],
                check=True, capture_output=True, text=True,
            )
            output_path = Path(tmpdir)
            all_files = [str(p.relative_to(output_path)) for p in output_path.rglob("*") if p.is_file()]

            task_005_private_re = re.compile(r"tasks/task-005/environment/(private|service)/")
            for fpath in all_files:
                self.assertIsNone(task_005_private_re.search(fpath),
                    f"Leaked task-005 runtime private in agent package: {fpath}")


if __name__ == "__main__":
    unittest.main()
