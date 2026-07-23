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
                # Status appears in lifecycle table, error handling, completion gate, etc.
                # Now documented as backtick-quoted Markdown (`status`) rather than JSON-quoted.
                self.assertIn(f"`{status}`", skill)
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

    # ── Task 2: profiles, lifecycle, target precedence, violation semantics ──

    def test_readme_run_status_points_to_controller(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        # §4.2.3: run_status is controller-owned, not in answer/run-metadata.json
        self.assertNotIn("run-metadata.json records a `run_status`", readme,
            "README must not claim answer/run-metadata.json records run_status (§4.2.3)")
        self.assertIn("controller/run-manifest.json", readme,
            "README must point run_status to controller/run-manifest.json (§4.2.3)")

    def test_skill_md_does_not_assign_run_status_to_agent(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        # §4.2.3: agent MUST NOT set run_status
        required_flow_section = skill[skill.find("## Required Flow"):skill.find("## Completion Gate")]
        self.assertNotIn('Set `run_status` to:', required_flow_section,
            "SKILL.md Required Flow must not instruct agent to set run_status (§4.2.3)")
        self.assertIn("agent_reported_phase", required_flow_section,
            "SKILL.md Required Flow must instruct agent to report agent_reported_phase instead (§4.2.1)")

    def test_lifecycle_distinguishes_preflight_blocked_from_ready(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        # AC-3a: preflight adapter_blocked/protocol_mismatch have NO answer/ dir
        self.assertIn("create NO", skill,
            "SKILL.md must state preflight-blocked runs create NO answer/ directory (AC-3a)")
        # AC-5d: preflight-blocked = 2 controller files only
        preflight_blocked_2 = "2: preflight-result + run-manifest"
        self.assertIn(preflight_blocked_2, skill,
            "SKILL.md lifecycle must state preflight-blocked writes only 2 controller files (AC-5d)")

    def test_violation_status_mapping_table_exists(self) -> None:
        guide = (ROOT / "docs" / "OFFLINE-SCORING-GUIDE.md").read_text(encoding="utf-8")
        # §8.1: violation-to-status mapping documented in scoring guide
        for term in ["unauthorized_read", "evidence_fabrication", "prohibited_exec",
                     "boundary_escape", "evidence_tamper", "protected_file_modification"]:
            self.assertIn(term, guide.lower(),
                f"OFFLINE-SCORING-GUIDE.md missing violation type: {term} (§8.1)")
        # §8.1: prohibited_exec = process cap 20 (not task_invalid)
        self.assertIn("process cap", guide.lower(),
            "OFFLINE-SCORING-GUIDE.md must document process cap for prohibited_exec (§8.1)")
        # §8.1: boundary_escape split by target
        self.assertIn("task_invalid", guide.lower(),
            "OFFLINE-SCORING-GUIDE.md must document boundary_escape→task_invalid when reaching protected content (§8.1)")
        # AC-8b: SQLite bypass = run_invalid
        self.assertIn("sqlite", guide.lower(),
            "OFFLINE-SCORING-GUIDE.md must document SQLite bypass→run_invalid (AC-8b)")

    def test_material_trajectory_loss_rules_documented(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        # §9.2.1: zero trajectory events = protocol_mismatch
        self.assertIn("protocol_mismatch", skill.lower())
        # §9.2.3: decision-log SHALL NOT substitute for trajectory
        self.assertIn("not substitute", skill.lower(),
            "SKILL.md must state decision-log does not substitute for trajectory (§9.2.3)")
        # §9.2.4: partial-but-sufficient trajectory = deduction, not mismatch
        self.assertIn("deduction", skill.lower(),
            "SKILL.md must document partial trajectory = deductions, not protocol_mismatch (§9.2.4)")

    def test_uat_contract_uses_normalized_capability_vocabulary(self) -> None:
        contract = (ROOT / "contracts" / "uat-controller-contract.yaml").read_text(encoding="utf-8")
        # §10.1: static-eval normalized capabilities
        self.assertIn("filesystem.list", contract,
            "uat-controller-contract.yaml missing filesystem.list for static-eval (§10.1)")
        self.assertIn("filesystem.read", contract,
            "uat-controller-contract.yaml missing filesystem.read for static-eval (§10.1)")
        self.assertIn("filesystem.write_answer", contract,
            "uat-controller-contract.yaml missing filesystem.write_answer for static-eval (§10.1)")
        # §10.3: coding-eval must include code.exec
        self.assertIn("code.exec", contract,
            "uat-controller-contract.yaml coding-eval missing code.exec (§10.3)")
        self.assertIn("code.edit", contract,
            "uat-controller-contract.yaml coding-eval missing code.edit (§10.3)")
        # §10.4: stateful-eval must include stateful.read and stateful.write
        self.assertIn("stateful.read", contract,
            "uat-controller-contract.yaml stateful-eval missing stateful.read (§10.4)")
        self.assertIn("stateful.write", contract,
            "uat-controller-contract.yaml stateful-eval missing stateful.write (§10.4)")

    def test_uat_contract_declares_stateful_tool_boundary(self) -> None:
        contract = (ROOT / "contracts" / "uat-controller-contract.yaml").read_text(encoding="utf-8")
        # §10.4 / AC-10d: exactly 9 public agent tools named
        public_tools = [
            "list_requests", "get_request", "list_policies", "get_policy",
            "get_approval_status", "request_information", "approve_request",
            "reject_request", "escalate_request",
        ]
        for tool in public_tools:
            self.assertIn(tool, contract,
                f"uat-controller-contract.yaml missing public tool: {tool} (§10.4)")
        # §10.4: 3 admin-only tools named
        admin_tools = ["get_final_state", "get_action_log", "reset"]
        for tool in admin_tools:
            self.assertIn(tool, contract,
                f"uat-controller-contract.yaml missing admin tool: {tool} (§10.4)")
        self.assertIn("admin", contract.lower(),
            "uat-controller-contract.yaml must declare admin tool boundary (§10.4)")

    def test_profile_contract_declares_read_only_shell_fallback(self) -> None:
        contract = (ROOT / "contracts" / "uat-controller-contract.yaml").read_text(encoding="utf-8")
        # §10.2: read_only_shell_fallback is non-canonical, diagnostic-only
        self.assertIn("read_only_shell_fallback", contract,
            "uat-controller-contract.yaml missing read_only_shell_fallback profile (§10.2)")
        self.assertIn("shell.exec.read_only", contract,
            "uat-controller-contract.yaml missing shell.exec.read_only capability (§10.2)")
        self.assertIn("diagnostic_only", contract,
            "uat-controller-contract.yaml must declare fallback diagnostic-only (§10.2)")

    def test_trajectory_contract_has_target_precedence(self) -> None:
        contract_path = ROOT / "contracts" / "trajectory-contract.yaml"
        self.assertTrue(contract_path.is_file(),
            "trajectory-contract.yaml does not exist (§7, §10)")
        text = contract_path.read_text(encoding="utf-8")
        # target-class precedence: editable_workspace for answer/artifacts/project/**
        self.assertIn("editable_workspace", text,
            "trajectory-contract.yaml missing editable_workspace target class")
        self.assertIn("answer/artifacts/project", text,
            "trajectory-contract.yaml must map answer/artifacts/project/** to editable_workspace")
        # answer_directory for other answer/**
        self.assertIn("answer_directory", text,
            "trajectory-contract.yaml missing answer_directory target class")
        # gold_answer precedes evaluator_only in precedence (§7)
        self.assertIn("gold_answer", text)
        self.assertIn("evaluator_only", text)
        ga_pos = text.find("gold_answer")
        eo_pos = text.find("evaluator_only")
        self.assertLess(ga_pos, eo_pos,
            "gold_answer must precede evaluator_only in target-class precedence")

    def test_violation_dimensions_are_orthogonal(self) -> None:
        contract = (ROOT / "contracts" / "controller-evidence-contract.yaml").read_text(encoding="utf-8")
        # §8.1: violation_type, enforcement_outcome, detection_timing are independent dimensions
        for dim in ["violation_type", "enforcement_outcome", "detection_timing"]:
            self.assertIn(dim, contract,
                f"controller-evidence-contract.yaml must declare {dim} as independent dimension (§8.1)")
        # AC-8c: evidence_fabrication maps to executed enforcement and post_hoc detection
        self.assertIn("evidence_fabrication", contract)
        self.assertIn("executed", contract,
            "evidence_fabrication must map to enforcement_outcome: executed (AC-8c)")
        self.assertIn("post_hoc", contract,
            "evidence_fabrication must map to detection_timing: post_hoc (AC-8c)")

    def test_docs_distinguish_partial_from_invalid(self) -> None:
        guide = (ROOT / "docs" / "OFFLINE-SCORING-GUIDE.md").read_text(encoding="utf-8")
        # §5.2.1: invalid outcome scores are JSON null (not 0)
        self.assertIn("null", guide.lower(),
            "OFFLINE-SCORING-GUIDE.md must state invalid outcome scores are null (§5.2.1)")
        # §5.2.2-5.2.3: partial is diagnostic-only, never a passing grade
        self.assertIn("partial", guide.lower(),
            "OFFLINE-SCORING-GUIDE.md must define partial status (§5.2)")
        self.assertIn("diagnostic", guide.lower(),
            "OFFLINE-SCORING-GUIDE.md must mention diagnostic-only treatment for partial (§5.2.3)")


    # ── Task 4: deterministic task content at evaluator boundary ──

    def test_task001_update_log_is_severity_authority(self) -> None:
        # §12.1.2: ticket-update-log.md > data.json for severity
        contract = (ROOT / "tasks/task-001/capability-contract.yaml").read_text(encoding="utf-8")
        self.assertIn("source_authority_resolution", contract)
        # §12.1.4: source_authority_resolution capability in contract
        task = (ROOT / "tasks/task-001/task.md").read_text(encoding="utf-8")
        self.assertIn("ticket-update-log.md", task)
        self.assertIn("severity-policy.md", task)
        # Evaluator notes exist and document source authority
        ref_path = ROOT / "tasks/task-001/evaluator-notes/reference-analysis.md"
        self.assertTrue(ref_path.is_file(),
            "task-001 evaluator-notes/reference-analysis.md does not exist")
        ref = ref_path.read_text(encoding="utf-8")
        self.assertIn("ticket-update-log.md", ref.lower())
        self.assertIn("source", ref.lower())
        rubric_path = ROOT / "tasks/task-001/evaluator-notes/manual-scoring-rubric.md"
        self.assertTrue(rubric_path.is_file(),
            "task-001 evaluator-notes/manual-scoring-rubric.md does not exist")

    def test_task002_has_exactly_six_relevant_and_two_distractor_files(self) -> None:
        # §12.2.1: exactly 8 files, 6 relevant + 2 distractors at file level
        inputs_dir = ROOT / "tasks/task-002/inputs"
        files = sorted([f.name for f in inputs_dir.iterdir()])
        self.assertEqual(len(files), 8, f"task-002 must have exactly 8 input files, got {len(files)}")
        expected = [
            "customer-email.txt", "deployment-log.md", "error-log-extract.txt",
            "sprint-planning-notes.md", "system-metrics.txt", "team-notes.md",
            "tickets.json", "vendor-advisory.txt",
        ]
        self.assertEqual(files, expected)
        ref = (ROOT / "tasks/task-002/evaluator-notes/reference-analysis.md").read_text(encoding="utf-8")
        self.assertIn("6 relevant", ref.lower())
        self.assertIn("2 distractor", ref.lower())
        # Each input file is named in the reference analysis
        for f_name in expected:
            self.assertIn(f_name, ref, f"reference-analysis.md missing file: {f_name}")

    def test_task002_preserves_unresolved_eight_vs_twelve_conflict(self) -> None:
        # §12.2.4: 09:15 is authoritative incident start
        deploy = (ROOT / "tasks/task-002/inputs/deployment-log.md").read_text(encoding="utf-8")
        self.assertIn("09:15 UTC", deploy,
            "deployment-log.md must record deploy at 09:15 UTC (§12.2.4)")
        ref = (ROOT / "tasks/task-002/evaluator-notes/reference-analysis.md").read_text(encoding="utf-8")
        # §12.2.5: unresolved 8-vs-12 conflict for Pilot Bank A
        self.assertIn("Pilot Bank A", ref,
            "reference-analysis.md must document Pilot Bank A conflict (§12.2.5)")
        self.assertIn("8", ref)
        self.assertIn("12", ref)
        # 09:15 is authoritative incident start per metrics precedence
        self.assertIn("09:15", ref,
            "reference-analysis.md must use 09:15 as authoritative start (§12.2.4)")

    def test_task003_policy_and_matrix_have_one_canonical_decision(self) -> None:
        # §12.3.1: >= 12 months
        procurement = (ROOT / "tasks/task-003/inputs/policy-procurement.md").read_text(encoding="utf-8")
        self.assertIn(">= 12 months", procurement,
            "policy-procurement.md must have >= 12 months clause (§12.3.1)")
        # §12.3.2: joint Legal + DPO review
        data_pol = (ROOT / "tasks/task-003/inputs/policy-data.md").read_text(encoding="utf-8")
        self.assertIn("Legal", data_pol,
            "policy-data.md must reference Legal in exemption (§12.3.2)")
        self.assertIn("DPO", data_pol,
            "policy-data.md must reference DPO in exemption (§12.3.2)")
        self.assertIn("joint", data_pol.lower(),
            "policy-data.md must have joint review clause (§12.3.2)")
        # §12.3.3: DAT-2025-008 = ESCALATE with Legal+DPO joint review rationale
        matrix_text = (ROOT / "tasks/task-003/evaluator-notes/decision-matrix.yaml").read_text(encoding="utf-8")
        self.assertIn("DAT-2025-008", matrix_text)
        self.assertIn("ESCALATE", matrix_text)
        self.assertIn("Legal", matrix_text)
        self.assertIn("DPO", matrix_text)
        # §12.3.4: one canonical decision per request — task.md must state this
        task_md = (ROOT / "tasks/task-003/task.md").read_text(encoding="utf-8")
        self.assertIn("ONE decision", task_md,
            "task-003 task.md must state ONE canonical decision per request (§12.3.4)")


if __name__ == "__main__":
    unittest.main()
