"""Staged environment contract tests for tasks 004-006.

These tests will FAIL against the current repo state because tasks 004-006
still have v1 `inputs/` directories and lack v2 environment scaffolding.

=== ACTIVATION PLAN ===

When tasks 004-006 are migrated to v2 environments (environment/ dirs,
profile dirs, removal of inputs/), activate these tests by:

1. Rename this file to `test_staged_environment.py` (adds `test_` prefix
   so unittest discovers it).
2. Run `python3 -m unittest discover tests -v` to confirm all pass.
3. Commit alongside the task 004-006 implementation commits.

Do NOT commit this file. Do NOT use skip/expectedFailure to mask failures.
The tests are paired with their implementation — both ship together.
"""

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NON_STATIC_TASKS = {"task-004", "task-005", "task-006"}


class StagedEnvironmentContractTests(unittest.TestCase):
    """Tests that will activate when tasks 004-006 receive v2 environments.

    Currently commented out — uncomment and move to CoreV2ContractTests
    when the environment migrations land.
    """

    # =========================================================================
    # Uncomment and activate when task-004 environment lands
    # =========================================================================

    def test_task_004_has_environment(self) -> None:
        """Verify task-004 has environment scaffolding."""
        task_dir = ROOT / "tasks" / "task-004"
        self.assertTrue((task_dir / "environment-contract.yaml").is_file(),
            "task-004 missing environment-contract.yaml")
        self.assertTrue((task_dir / "environment" / "base-project").is_dir(),
            "task-004 missing environment/base-project/")

    # =========================================================================
    # Uncomment and activate when task-005 environment lands
    # =========================================================================

    def test_task_005_has_environment(self) -> None:
        """Verify task-005 has full stateful service environment."""
        task_dir = ROOT / "tasks" / "task-005"
        self.assertTrue((task_dir / "environment" / "public" / "tool-contract.yaml").is_file(),
            "task-005 missing environment/public/tool-contract.yaml")
        self.assertTrue((task_dir / "environment" / "private").is_dir(),
            "task-005 missing environment/private/")
        self.assertTrue((task_dir / "environment" / "service" / "tool_api.py").is_file(),
            "task-005 missing environment/service/tool_api.py")

    # =========================================================================
    # Uncomment and activate when task-006 profiles land
    # =========================================================================

    def test_task_006_has_profiles(self) -> None:
        """Verify task-006 has controlled-web and live-web profiles."""
        task_dir = ROOT / "tasks" / "task-006"
        self.assertTrue((task_dir / "profiles" / "controlled-web").is_dir(),
            "task-006 missing profiles/controlled-web/")
        self.assertTrue((task_dir / "profiles" / "live-web").is_dir(),
            "task-006 missing profiles/live-web/")

    # =========================================================================
    # Uncomment when ALL non-static tasks have migrated away from inputs/
    # =========================================================================

    def test_non_static_tasks_no_inputs_dir(self) -> None:
        """Verify tasks 004-006 do NOT use legacy inputs/ directories."""
        for task_id in NON_STATIC_TASKS:
            task_dir = ROOT / "tasks" / task_id
            with self.subTest(task=task_id):
                self.assertFalse((task_dir / "inputs").exists(),
                    f"{task_id} should not have inputs/ — uses environment instead")

    # =========================================================================
    # Uncomment when task-005 service/private exists on disk
    # =========================================================================

    def test_build_agent_package_excludes_runtime_private(self) -> None:
        """Agent package must exclude task-005 service/private directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "build-distribution.py"),
                 "--target", "agent", "--output", tmpdir],
                check=True, capture_output=True, text=True,
            )
            output_path = Path(tmpdir)
            all_files = [str(p.relative_to(output_path)) for p in output_path.rglob("*") if p.is_file()]

            # task-005 environment/private and environment/service must not leak
            task_005_private_re = re.compile(r"tasks/task-005/environment/(private|service)/")
            for fpath in all_files:
                self.assertIsNone(task_005_private_re.search(fpath),
                    f"Leaked task-005 runtime private in agent package: {fpath}")

            # task-006 profiles/*/service must not leak
            profile_service_re = re.compile(r"tasks/task-006/profiles/[^/]+/service/")
            for fpath in all_files:
                self.assertIsNone(profile_service_re.search(fpath),
                    f"Leaked task-006 profile service in agent package: {fpath}")


if __name__ == "__main__":
    unittest.main()
