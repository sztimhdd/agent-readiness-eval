from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class V4ContractTests(unittest.TestCase):
    def test_suite_version_is_4_0_0(self) -> None:
        manifest = json.loads((ROOT / "skill.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["suite_version"], "4.0.0")

    def test_all_tasks_have_v4_task_version(self) -> None:
        manifest = json.loads((ROOT / "skill.json").read_text(encoding="utf-8"))
        for task in manifest["tasks"]:
            with self.subTest(task=task["id"]):
                self.assertEqual(task["task_version"], "4.0.0")

    def test_skill_md_is_v4_protocol(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Agent Readiness Eval Core v4.0.0", skill)

    def test_answer_directory_has_answer_subdir(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("answer/", skill)
        self.assertIn("answer/\n│   ├── task-id.txt", skill)

    def test_answer_directory_has_controller_sibling(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("controller/", skill)
        self.assertIn("controller/\n    ├── preflight-result.json", skill)

    def test_decision_log_required(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("decision-log.md", skill)

    def test_new_run_statuses_are_valid(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for status in ["scored", "partial", "adapter_blocked", "protocol_mismatch", "task_invalid", "run_invalid"]:
            with self.subTest(status=status):
                self.assertIn(f'"{status}"', skill)
        self.assertNotIn('"completed"', skill)  # V3 status removed from valid set

    def test_preflight_template_exists(self) -> None:
        tpl = ROOT / "templates" / "preflight-result.json"
        self.assertTrue(tpl.is_file())
        data = json.loads(tpl.read_text(encoding="utf-8"))
        self.assertIn("status", data)
        self.assertIn("checks", data)

    def test_run_manifest_template_exists(self) -> None:
        tpl = ROOT / "templates" / "run-manifest.json"
        self.assertTrue(tpl.is_file())
        data = json.loads(tpl.read_text(encoding="utf-8"))
        self.assertIn("run_status", data)

    def test_trajectory_event_template_exists(self) -> None:
        tpl = ROOT / "templates" / "trajectory-event.json"
        self.assertTrue(tpl.is_file())
        data = json.loads(tpl.read_text(encoding="utf-8"))
        self.assertIn("sequence", data)
        self.assertIn("capability", data)
        self.assertIn("authorization", data)

    def test_run_metadata_template_has_v4_fields(self) -> None:
        tpl = ROOT / "templates" / "run-metadata.json"
        data = json.loads(tpl.read_text(encoding="utf-8"))
        self.assertEqual(data["suite_version"], "4.0.0")
        self.assertIn("controller_evidence_available", data)

    def test_skill_md_documents_preflight(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## Harness Preflight", skill)
        self.assertIn("### Common checks", skill)
        self.assertIn("adapter_blocked", skill)
        self.assertIn("protocol_mismatch", skill)

    def test_skill_md_documents_trajectory_contract(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## Normalized Trajectory Contract", skill)
        self.assertIn("sequence", skill)
        self.assertIn("capability", skill)
        self.assertIn("authorization", skill)

    def test_skill_md_documents_scoring_model(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## Scoring Model", skill)
        self.assertIn("Outcome: 50 points", skill)
        self.assertIn("Process: 50 points", skill)

    def test_skill_md_no_v3_completed_status_in_completion_gate(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        # Completion gate uses "scored" not "completed"
        gate_section = skill[skill.find("## Completion Gate"):]
        self.assertIn("scored", gate_section)

    def test_skill_md_has_v4_rules(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Controller evidence is authoritative", skill)
        self.assertIn("The controller owns the final run status", skill)

    def test_distribution_contract_v4_version(self) -> None:
        contract = (ROOT / "contracts" / "distribution-contract.yaml").read_text(encoding="utf-8")
        self.assertIn('version: "4.0.0"', contract)

    def test_uat_controller_contract_v4_version(self) -> None:
        contract = (ROOT / "contracts" / "uat-controller-contract.yaml").read_text(encoding="utf-8")
        self.assertIn('version: "4.0.0"', contract)

    def test_readme_v4_version(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Agent Readiness Eval Core v4.0.0", readme)
        self.assertIn("4.0.0", readme)

    def test_controller_evidence_boundary_documented(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("controller evidence", skill.lower())

    def test_skill_md_has_v4_error_handling(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Preflight returns `adapter_blocked`", skill)
        self.assertIn("Agent reads private, evaluator, controller, or gold-answer assets", skill)

    # ── Task 1: manifest registration & controller evidence vocabulary ──

    def test_skill_manifest_registers_only_task_001_through_task_005(self) -> None:
        manifest = json.loads((ROOT / "skill.json").read_text(encoding="utf-8"))
        task_ids = [t["id"] for t in manifest["tasks"]]
        self.assertEqual(len(task_ids), 5, "skill.json must register exactly 5 tasks")
        expected = ["task-001", "task-002", "task-003", "task-004", "task-005"]
        self.assertEqual(task_ids, expected)

    def test_run_metadata_delegates_status_to_controller(self) -> None:
        tpl = ROOT / "templates" / "run-metadata.json"
        data = json.loads(tpl.read_text(encoding="utf-8"))
        # §4: agent MUST NOT report controller-owned run_status
        self.assertNotIn("run_status", data,
            "run-metadata.json must not contain controller-owned run_status (§4.2.3)")
        # §4.2.1: agent reports agent_reported_phase
        self.assertIn("agent_reported_phase", data,
            "run-metadata.json must contain agent_reported_phase (§4.2.1)")
        valid_phases = {"answer_complete", "answer_incomplete", "UNAVAILABLE"}
        self.assertIn(data["agent_reported_phase"], valid_phases,
            f"agent_reported_phase must be one of {valid_phases}")

    def test_controller_evidence_templates_have_addendum_fields(self) -> None:
        tmpl = ROOT / "templates"

        # ── preflight-result.json (§13.1.1) ──
        pf = json.loads((tmpl / "preflight-result.json").read_text(encoding="utf-8"))
        self.assertIn("checks", pf)
        # §6.1: probe_directory_writable replaces writable_answer_directory
        self.assertIn("probe_directory_writable", pf["checks"],
            "preflight checks must use probe_directory_writable (§6.1)")
        self.assertNotIn("writable_answer_directory", pf["checks"],
            "preflight checks must NOT use writable_answer_directory (§6.1)")
        # §6.1 profile-specific checks: static-eval, coding-eval, stateful-eval
        profile_checks = [
            "shell_execution_blocked", "filesystem_read_available",
            "filesystem_write_answer_available",
            "project_copy_available", "src_editable",
            "test_execution_available", "protected_paths_readonly",
            "declared_tools_accessible", "controller_tools_inaccessible",
            "runtime_private_inaccessible",
        ]
        for check_name in profile_checks:
            self.assertIn(check_name, pf["checks"],
                f"preflight checks missing profile-specific check: {check_name}")

        # ── run-manifest.json (§13.1.2) ──
        rm = json.loads((tmpl / "run-manifest.json").read_text(encoding="utf-8"))
        for field in ["profile_id", "source_commit", "source_tree_dirty",
                      "package_digest", "protected_file_detection"]:
            self.assertIn(field, rm,
                f"run-manifest.json missing §13.1.2 field: {field}")

        # ── trajectory-event.json (§7.1-7.2) ──
        tr = json.loads((tmpl / "trajectory-event.json").read_text(encoding="utf-8"))
        for field in ["event_id", "actor", "state_mutation"]:
            self.assertIn(field, tr,
                f"trajectory-event.json missing §7.1 field: {field}")
        # §7.2 tool-operation fields — conditionally optional for non-tool events
        for field in ["operation_id", "attempt", "request_fingerprint"]:
            self.assertIn(field, tr,
                f"trajectory-event.json missing §7.2 field: {field}")

        # ── protocol-violations.json (§13.1.3) ──
        pv_path = tmpl / "protocol-violations.json"
        self.assertTrue(pv_path.is_file(),
            "protocol-violations.json template does not exist")
        pv = json.loads(pv_path.read_text(encoding="utf-8"))
        self.assertIn("violations", pv)
        self.assertIn("total_violations", pv)
        # §13.1.3 violation object fields (including nullable post-hoc fields)
        if pv["violations"]:
            v = pv["violations"][0]
            for field in ["violation_id", "violation_type", "enforcement_outcome",
                          "detection_timing", "event_id", "target", "rule_reference"]:
                self.assertIn(field, v,
                    f"protocol-violations violation missing field: {field}")
            # §13.1.3: post-hoc violations may have event_id null
            self.assertIsNone(v["event_id"],
                "event_id should be null in template (post-hoc violation default)")

        # ── outcome-checks.json (§13.1.4) ──
        oc_path = tmpl / "outcome-checks.json"
        self.assertTrue(oc_path.is_file(),
            "outcome-checks.json template does not exist")
        oc = json.loads(oc_path.read_text(encoding="utf-8"))
        for field in ["outcome_score", "process_score", "total_score",
                      "invalid", "diagnostic_only", "checks"]:
            self.assertIn(field, oc,
                f"outcome-checks.json missing §13.1.4 field: {field}")

    def test_controller_evidence_contract_names_all_five_files(self) -> None:
        contract = ROOT / "contracts" / "controller-evidence-contract.yaml"
        self.assertTrue(contract.is_file(),
            "controller-evidence-contract.yaml does not exist")
        text = contract.read_text(encoding="utf-8")
        expected_ids = ["preflight-result", "run-manifest", "trajectory",
                        "protocol-violations", "outcome-checks"]
        for schema_id in expected_ids:
            self.assertIn(schema_id, text,
                f"controller-evidence-contract.yaml missing schema ID: {schema_id}")
        # §7.2: trajectory conditional requiring operation_id/attempt/request_fingerprint
        # when actor is agent (JSON Schema if/then)
        self.assertIn("const: agent", text,
            "trajectory schema must conditionally require retry fields for agent events (§7.2)")
        # §13.1.4: outcome-checks conditional requiring reviewer fields when automated=false
        self.assertIn("const: false", text,
            "outcome-checks schema must conditionally require reviewer fields (§13.1.4)")
        # §13.1.3: target is required in protocol-violations (nullable for post-hoc)
        self.assertIn("- target", text,
            "protocol-violations required must include target (§13.1.3)")
        # §13.1.3: runtime violations MUST have non-null trajectory event fields;
        # post_hoc violations already allow null via oneOf (JSON Schema if/then conditional)
        self.assertIn("const: runtime", text,
            "protocol-violations must conditionally require non-null fields for runtime (§13.1.3)")
        # §13.1.2 / §7.2: SHA-256 hex pattern for package_digest and request_fingerprint
        self.assertIn("[0-9a-f]{64}", text,
            "contract must specify SHA-256 hex pattern for digest/fingerprint (§13.1.2, §7.2)")
        # §6 / AC-6d: profile_id conditionals enforce active-profile checks in preflight
        for profile in ["static-eval", "coding-eval", "stateful-eval"]:
            self.assertIn(f"const: {profile}", text,
                f"preflight schema must conditionally require {profile} checks (§6, AC-6d)")
        # §6: checks.additionalProperties constrains extra check values to boolean
        self.assertIn("additionalProperties", text,
            "preflight checks must have additionalProperties type constraint (§6)")


if __name__ == "__main__":
    unittest.main()
