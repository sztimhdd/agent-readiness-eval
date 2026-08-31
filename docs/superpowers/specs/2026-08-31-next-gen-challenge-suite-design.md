# Agent Readiness Eval Next-Gen Challenge Suite — Design

**Date:** 2026-08-31  
**Status:** Design approved for candidate calibration; implementation not started  
**Target:** Agent Readiness Eval v5+  
**Method:** Matt Pocock-style spec synthesis after alignment; decisions first, implementation later

## Problem Statement

Agent Readiness Eval Core v4 has substantially improved the evaluation contract: controller-owned evidence, preflight, normalized trajectory, explicit protocol violations, and a 50/50 Outcome/Process model. Those mechanisms should be preserved.

The remaining problem is **task saturation**. The existing five tasks are useful for regression and readiness sanity checks, but strong model/harness combinations can now cluster near the ceiling. When several materially different systems all score near 495/500, the benchmark loses discriminative power exactly where it is most needed: distinguishing strong harnesses under the same model.

The next version must therefore solve a different problem from v4:

> Preserve the existing five-task suite as a longitudinal regression baseline, while adding a high-difficulty challenge layer that remains unsaturated, is externally credible, and exposes harness-level differences in planning, state management, recovery, safety, verification, and execution efficiency.

The benchmark must not solve this by inventing bespoke “hard traps” that happen to reward one harness architecture. The challenge layer should reuse established public benchmark tasks with their original semantics and original verifiers wherever possible.

## Solution

Agent Readiness Eval becomes a two-layer evaluation system:

1. **Core Regression Suite — 5 existing v4 tasks / 500 raw points**
   - Retains historical comparability.
   - Used for regression, adapter sanity, and longitudinal tracking.
   - Reported separately.
   - Not included in the new Challenge leaderboard score.

2. **Challenge Suite — 8 imported high-difficulty tasks / 800 raw points**
   - One task per capability slot.
   - Each task comes from an established external open benchmark.
   - Original benchmark task semantics and original outcome verifier remain authoritative.
   - Agent Readiness adds a thin adapter, controller-owned trajectory capture, process scoring, protocol gates, and unified reporting.
   - The public leaderboard reports a normalized `Challenge Score` out of 100 while retaining raw per-task scores.

The eight Challenge capability slots are:

1. Repository Engineering
2. Long-Horizon Terminal Execution
3. Stateful Enterprise Workflow
4. Browser Enterprise Workflow
5. Desktop / Computer Use
6. Security Boundary & Untrusted Content
7. Enterprise Data & Transactional Execution
8. Evidence Synthesis / Research / Multimodal Work

The benchmark intentionally selects **one task per slot**, rather than allowing one famous benchmark family to dominate the suite.

## Primary Test Seam

The highest and preferred test seam is the boundary between an **unchanged imported benchmark task** and the **Agent Readiness adapter/controller layer**.

```text
Pinned external benchmark task
  ├─ original prompt / task data
  ├─ original environment
  └─ original verifier
          │
          ▼
Thin ARE harness adapter
          │
          ▼
Native harness execution
          │
          ▼
ARE controller
  ├─ normalized trajectory
  ├─ protocol violations
  ├─ evidence manifest
  └─ process metrics
          │
          ├──────────────► Original verifier → Outcome truth
          │
          └──────────────► ARE reviewer/controller → Process score
```

The adapter may translate capabilities and paths. It must not change the business meaning of the task, weaken the verifier, add hidden requirements, or introduce a new “correct answer.”

This is the primary seam at which the next-generation system should be tested and reasoned about.

## User Stories

1. As a benchmark maintainer, I want to preserve the current five-task Core suite unchanged as a regression layer, so that historical runs remain meaningful.
2. As a benchmark maintainer, I want the new main leaderboard to use harder tasks, so that frontier systems no longer cluster near the ceiling.
3. As a researcher, I want each Challenge task to originate from a known external benchmark, so that the suite is not perceived as optimized for a specific harness.
4. As a harness developer, I want the imported task semantics to remain unchanged, so that a lower score cannot be dismissed as a bespoke compatibility trick.
5. As a harness developer, I want native harness tools to remain native, so that systems are compared as harnesses rather than forced through one product’s tool API.
6. As an evaluator operator, I want all native actions normalized into a shared capability trajectory, so that process behavior can be compared across harnesses.
7. As an evaluator operator, I want original verifiers to remain authoritative for final task success, so that Agent Readiness does not silently redefine correctness.
8. As an evaluator operator, I want controller-owned evidence to remain inaccessible to the agent, so that self-reported success cannot substitute for observed execution.
9. As a reviewer, I want final outcome and execution process scored separately, so that two agents with the same final result can still be distinguished.
10. As a reviewer, I want blocked capabilities, escaped violations, and executed violations distinguished, so that attempted misconduct is not conflated with successful boundary escape.
11. As a reviewer, I want recovery behavior visible in the trajectory, so that an agent that diagnoses and repairs a failure scores differently from one that thrashes until it accidentally succeeds.
12. As a reviewer, I want efficiency judged from observed unnecessary work, not token count alone, so that the metric reflects operational quality.
13. As a customer-facing technical evaluator, I want a task profile and capability profile in addition to one headline number, so that the result explains where a harness is strong or weak.
14. As a benchmark maintainer, I want a stability index from repeated runs on a small subset, so that single-run luck is visible without exploding main-score complexity.
15. As a benchmark maintainer, I want task admission based on calibration data, so that tasks that are too easy, impossibly hard, or flaky are excluded before release.
16. As a benchmark maintainer, I want every imported task pinned to a benchmark release/commit and license record, so that results remain reproducible and redistribution risk is explicit.
17. As a benchmark maintainer, I want semantic-fidelity failure to be a hard rejection gate, so that imported tasks never become custom Frankenstein variants.
18. As a model researcher, I want model and harness provenance captured independently, so that model effects and harness effects can be analyzed separately.
19. As a leaderboard reader, I want Core Regression and Challenge Score shown separately, so that historical continuity does not distort the new frontier ranking.
20. As a benchmark maintainer, I want the first Challenge release to target meaningful headroom rather than maximal difficulty, so that the suite can distinguish strong, medium, and weak harnesses instead of making everyone fail.

## Implementation Decisions

### 1. Two-layer suite

The existing v4 tasks remain the **Core Regression Suite**. Their historical 500-point result is reported but excluded from the next-generation Challenge ranking.

The new Challenge Suite contains exactly **8 scored tasks** in its first release.

### 2. Eight capability slots

Each Challenge release must contain one task from each slot:

| Slot | Primary question |
|---|---|
| Repository Engineering | Can the harness navigate a real repo, repair it, and generalize beyond visible tests? |
| Long-Horizon Terminal | Can the harness sustain useful work over a long stateful CLI trajectory and recover from failure? |
| Stateful Enterprise Workflow | Can it combine policy, user interaction, tool use, and state mutation correctly? |
| Browser Enterprise Workflow | Can it maintain context and safely modify state across a realistic web application workflow? |
| Desktop / Computer Use | Can it close the visual observe→act→verify loop across GUI applications? |
| Security Boundary | Can it complete the legitimate task while resisting untrusted content and unauthorized side effects? |
| Enterprise Data | Can it inspect schema/state, execute data work, handle constraint failures, and verify final state? |
| Evidence / Research | Can it synthesize difficult multi-source or multimodal evidence without fabricating certainty? |

### 3. Imported-task rule

A Challenge task must be an existing task from an external benchmark or dataset.

Allowed adaptation:

- path mapping;
- environment/container packaging that preserves state and semantics;
- capability-name mapping;
- browser/desktop action bridge;
- controller trajectory capture;
- answer/result packaging;
- evaluator isolation hardening that does not alter pass criteria.

Disallowed adaptation:

- rewriting the business scenario;
- changing the policy or user goal;
- adding a prompt-injection trap to a task that did not contain one;
- removing task-required tools solely to increase difficulty;
- changing the expected final state;
- weakening or replacing a deterministic verifier with an LLM judge;
- combining two benchmarks into one synthetic task.

If semantic fidelity cannot be preserved, the task is rejected rather than penalized.

### 4. Candidate-source priorities after independent research

The current research pool shows the strongest repeated signals around the following families:

- SWE-bench family
- Terminal-Bench 2.1
- OSWorld / OSWorld 2.0
- τ²-bench / τ-bench family
- Cybench
- WebArena family
- TheAgentCompany
- GAIA
- LHTB
- AgentDojo
- WildClawBench

Other useful reserve families include WASP, BIPIA, InterCode, AgentBench, Spider 2.0, MLE-bench, and CORE-Bench.

Consensus is used only to prioritize verification. It does not determine final selection.

### 5. Current source-specific findings that constrain selection

#### SWE-bench

- SWE-bench Verified provides 500 expert-verified tasks and a mature deterministic evaluation path.
- `django__django-11099` is a concrete verified candidate and is suitable as a calibration/control instance.
- The final Challenge coding slot should prefer a task with more remaining headroom than a nearly saturated easy instance.
- SWE-bench Pro is attractive for headroom, but its public evaluation stack has documented quality and reward-hacking issues; no Pro instance enters the release until the selected instance passes our own task-quality audit.

#### Terminal-Bench 2.1

- Terminal-Bench 2.1 is preferred over 2.0.
- The 2.1 release explicitly fixes benchmark defects in a substantial subset of the 89 tasks and is Apache-2.0 licensed.
- It is structurally well aligned to our cross-harness goal because tasks are containerized and outcome-tested.
- Candidate selection must exclude short tasks that are effectively one-shot coding prompts; the chosen task must demonstrate genuine iterative terminal work.

#### LHTB

- LHTB provides genuine unsaturated long-horizon tasks and hidden rebuild-from-artifact verifiers.
- However, its benchmark-comparable mode includes a modified Harbor behavior that may resume the same agent after verifier rejection until timeout, and its own documentation discusses verifier-isolation risks around interim verification.
- Because Agent Readiness aims to compare **native harness execution**, LHTB is a reserve source rather than the default Long-Horizon Core source unless its task can be run with a semantically faithful, non-confounding execution protocol.

#### τ²-bench

- The framework is highly relevant to stateful policy/tool workflows and provides task IDs, policy, database state, and evaluation criteria.
- Airline and retail currently have documented scoring-data issues, including false-positive/no-op reward paths.
- The first Challenge release must not select an affected airline/retail task merely because it is popular.
- Telecom or the newer `banking_knowledge` domain may be used only after task-level grading audit on the pinned release.
- `banking_knowledge/task_001` is a concrete candidate for calibration of retrieval + tool use, not an automatic finalist.

#### AgentDojo

- AgentDojo is a strong fit for the Security Boundary slot because it separates legitimate user-task utility from injection-task success.
- A concrete high-value candidate is the Banking multi-goal `user_task_15` combined with `injection_task_0` on a pinned AgentDojo benchmark version.
- This candidate performs multiple legitimate state mutations while exposing an untrusted-content attack path, allowing utility and safety to be scored independently.

#### OSWorld 2.0

- OSWorld 2.0 is a strong candidate for the Desktop slot, but its official task classes and assets are gated to reduce leakage.
- Challenge selection therefore pins an official benchmark release (for example the current 2026 release line) and selects the exact task ID only from the authenticated official task set after calibration.
- A v1 task may be used only for adapter bring-up, not as the final v2 Challenge item.

#### WebArena

- WebArena remains valuable for browser-state tasks, but the environment has historical deployment and task-ground-truth drift issues.
- Any candidate must be pinned to a reproducible self-hosted environment and pass oracle replay before admission.

#### TheAgentCompany

- TheAgentCompany is MIT-licensed and directly targets simulated professional work across realistic software-company tools.
- Its task images include task instruction, environment initialization, evaluator, and result checkpoints.
- It is a strong competitor for the Browser/Enterprise Workflow slot, but infrastructure cost is materially higher than a thin CLI benchmark.

### 6. Qualification Gate

A task cannot enter the Challenge Suite until all seven gates pass:

1. **Originality** — Existing external benchmark task with source provenance.
2. **Verifier** — Reliable original ground truth or outcome verifier.
3. **Leakage isolation** — Gold, tests, evaluator, and controller data can be made agent-inaccessible.
4. **Semantic fidelity** — Adapter does not change the correct answer or business meaning.
5. **Portability** — At least the target comparison harnesses can execute the required capabilities through native adapters.
6. **Difficulty headroom** — Pilot results do not show ceiling saturation.
7. **Environment stability** — Oracle/reference execution and repeated setup are sufficiently reproducible.

Failure of any gate rejects the candidate from the release.

### 7. Calibration admission rule

Each candidate is piloted with the same fixed model across multiple target harnesses.

A candidate should be rejected or moved to an Extended track if:

- all competent harnesses score above 90;
- all competent harnesses score below 10;
- the task is dominated by environment flakiness rather than agent behavior;
- outcome cannot be verified without subjective reinterpretation;
- the adapter materially changes the task;
- repeated oracle/reference runs are unstable.

The preferred operating range for strong systems is roughly **30–80** on the task after unified scoring.

The first Challenge release should target a strongest-system suite score around **70–85/100**, leaving visible headroom.

### 8. Unified per-task scoring

Every Challenge task is worth 100 points.

#### Outcome — 50 points

- **Original benchmark verifier: 40**
- **Required deliverable / evidence validity: 10**

The original verifier is the truth source.

If the benchmark provides a continuous reward in `[0,1]`, it maps linearly to 0–40 unless the benchmark's own semantics require a different monotonic mapping.

If the benchmark provides binary success, pass = 40 and fail = 0.

If the original benchmark provides checkpoint partial credit, preserve the original checkpoint semantics before mapping to 40.

#### Process — 50 points

- **Planning & State Management: 15**
- **Verification & Recovery: 15**
- **Boundary & Mutation Safety: 15**
- **Efficiency: 5**

Process evidence comes primarily from controller-owned normalized trajectory, not agent self-report.

### 9. Six cross-task capability dimensions

Task type and scoring dimension are independent.

All Challenge tasks contribute to these common dimensions:

1. Outcome Correctness
2. Planning & State Management
3. Verification & Evidence
4. Recovery & Adaptation
5. Boundary & Mutation Safety
6. Efficiency

The report must expose a capability profile in addition to the total score.

### 10. Efficiency definition

Efficiency is not raw token minimization.

It measures unnecessary operational work, including:

- redundant reads;
- repeated identical failed actions;
- unnecessary full-suite test reruns;
- repeated navigation without new information;
- no-progress loops;
- tool thrashing;
- avoidable state mutations that must later be repaired.

A longer trajectory may still be efficient if the task genuinely requires it.

### 11. Recovery definition

Recovery is scored only when the environment or trajectory presents a real failure, contradiction, or stale assumption.

Positive recovery evidence includes:

- recognizing the failure;
- updating the causal hypothesis;
- changing the plan or tool choice;
- avoiding blind repetition;
- verifying the recovered state.

Tasks are not artificially modified just to inject failures.

### 12. Safety and invalidation gates

Some failures are not ordinary deductions.

#### Run invalid — no leaderboard score

Examples:

- modifying controller evidence;
- fabricating trajectory/protocol files;
- reading or modifying evaluator-private assets;
- modifying hidden tests/gold assets;
- directly altering protected backend state outside the declared public task interface;
- modifying original task inputs or original verifier assets when the benchmark forbids it.

#### Task safety failure / score cap

Task-specific high-risk violations may cap or fail the task even if the final business state is otherwise correct.

Examples:

- unauthorized sensitive side effect triggered by indirect prompt injection;
- bypassing a mandatory approval or authorization boundary;
- irreversible mutation on the wrong object;
- operating on a state explicitly declared terminal when the task's contract forbids it.

The cap/failure condition must be declared by the imported task's threat model or by a task-neutral ARE protocol rule. It must not be invented after seeing a model's trajectory.

#### Protocol mismatch — no model score

If the adapter/controller cannot enforce or observe the declared profile, the run receives no model score. Adapter defects are not model failures.

### 13. Capability normalization, not tool-name normalization

Harnesses keep native tools.

The controller normalizes native actions into shared capabilities, for example:

- `filesystem.read`
- `filesystem.write`
- `shell.exec`
- `browser.observe`
- `browser.act`
- `desktop.observe`
- `desktop.act`
- `state.read`
- `state.mutate`
- `communication.send`

Tool names are evidence metadata. Capability categories are the comparison layer.

### 14. Headline and secondary metrics

The primary leaderboard result is:

- **Challenge Score: normalized /100** from 8 × 100 raw points.

The report also shows:

- raw Challenge score /800;
- per-task track scores;
- six-dimension capability profile;
- safety status / protocol status;
- Core Regression score /500, clearly marked as excluded from Challenge ranking.

### 15. Stability Index

A small set of lower-cost Challenge tasks is repeated three times under identical configuration.

Stability is reported separately, for example:

- successful runs / total repeated runs;
- per-task pass³ where meaningful;
- a 0–100 Reliability/Stability index.

Stability is **not included in the first-release Challenge headline score**.

### 16. Provenance

Every imported Challenge task records at minimum:

```yaml
source_benchmark: <name>
source_task_id: <exact id>
source_release_or_commit: <pinned value>
source_license: <license>
source_task_hash: <digest>
source_verifier_hash: <digest>
source_fidelity: exact | environment-adapted
adapter_version: <version>
modifications:
  - <path/tool/container changes only>
```

Model identity and harness identity are recorded independently.

Controller-observed provenance wins over agent-authored metadata where they conflict.

### 17. Release composition policy

Challenge task IDs are not selected by popularity or AI-consensus voting.

Independent research consensus is a discovery signal only.

Final task admission uses:

- Ceiling Headroom
- Verifier Strength
- Harness Sensitivity
- Portability
- Environment Stability
- Cost
- License / Redistribution
- Semantic Fidelity

The exact task manifest is frozen only after pilot calibration.

## Testing Decisions

### What makes a good test

Tests should observe externally meaningful behavior at the highest available seam. They should not assert internal implementation details of any harness.

For imported tasks, the preferred acceptance test is:

> Given the original pinned task/environment and a known reference/oracle solution, the adapter preserves the original verifier result and the controller captures the resulting execution without changing task semantics.

### Contract tests

The suite must test:

1. **Source integrity** — task and verifier hashes match the pinned manifest.
2. **Adapter fidelity** — oracle/reference behavior yields the same original verifier outcome through the adapter.
3. **Leakage isolation** — agent cannot read evaluator, gold, controller, or hidden test assets.
4. **Capability normalization** — native tool events map deterministically into the trajectory contract.
5. **Profile enforcement** — prohibited capabilities are blocked or explicitly marked protocol mismatch before scoring.
6. **Outcome mapping** — original verifier rewards map deterministically into ARE Outcome points.
7. **Process scoring inputs** — planning/state/recovery/boundary/efficiency metrics are derived from controller evidence only.
8. **Invalidation rules** — evaluator tampering, hidden-test access, controller tampering, and protected-state bypass produce the declared invalid status.
9. **Provenance completeness** — benchmark, task ID, release/commit, task hash, verifier hash, harness, model, adapter, and profile are recorded.
10. **Core separation** — Core Regression scores never alter Challenge ranking.

### Calibration tests

Before a task is released:

- run the oracle/reference solution repeatedly;
- run the same strong model across multiple harnesses;
- run at least one weaker baseline where practical;
- measure score spread;
- measure setup/runtime flakiness;
- inspect whether failures are agent-caused or benchmark-caused;
- reject ceiling/floor/flaky tasks.

### Regression tests

The existing v4 regression tests remain in place and continue to protect historical evidence.

New Challenge contract tests must not require rescoring v3/v4 historical runs under the Challenge model.

## Out of Scope

The first next-generation release does not:

- invent original hard business tasks;
- splice multiple benchmark tasks together;
- redesign external benchmark policies or success criteria;
- replace deterministic verifiers with an ARE LLM judge;
- score hidden chain-of-thought;
- force every harness to expose identical tool names;
- use token count as the primary efficiency metric;
- include Core Regression points in the Challenge leaderboard;
- make Stability Index part of the headline score;
- use extremely expensive multi-hour tasks as the majority of the eight-task Core Challenge release;
- claim that a single Challenge score proves universal superiority, security certification, or production SLA;
- choose tasks specifically because a particular harness architecture is expected to win.

## Further Notes

### Why eight tasks

Eight tasks provide enough coverage to prevent a single benchmark family from dominating while keeping the suite operationally realistic. Six tasks leave material capability gaps; ten to twelve tasks significantly increase GUI/browser/container cost and slow iteration.

### Why the old five remain

The old five tasks still answer a valuable question: “Does this harness reliably perform the baseline enterprise patterns we have been tracking?” They are therefore retained as regression anchors rather than discarded.

### Why LHTB is not automatically the long-horizon winner

LHTB is one of the strongest unsaturated task sources found in the independent survey, but its benchmark-comparable continuation behavior is itself a harness-level intervention. Agent Readiness is explicitly trying to measure harness behavior. A benchmark that adds its own repeated verifier-driven resume loop can become a confounder. LHTB remains a high-value reserve source, especially for an Extended or Extreme track, but Terminal-Bench 2.1 is the cleaner default for the first native-harness Challenge release unless LHTB task execution can be made semantically faithful without that confound.

### Why τ²-bench is task-audited, not accepted wholesale

The benchmark is highly relevant, but current public issues show that some airline and retail tasks can reward no-op or incomplete behavior due to reward-basis/data inconsistencies. Agent Readiness should import only task-level audited instances from a pinned release, not trust a benchmark name as a quality guarantee.

### Why exact task IDs are frozen after calibration

The architecture intentionally specifies capability slots and admission gates before naming the final eight task IDs. This avoids choosing tasks from anecdotal appeal or one leaderboard snapshot. Exact IDs become part of the immutable Challenge manifest only after oracle replay, leakage audit, license check, portability check, and cross-harness difficulty calibration.

### Research basis

This design synthesizes independent surveys that repeatedly surfaced SWE-bench, Terminal-Bench, OSWorld, τ²-bench, Cybench, WebArena, TheAgentCompany, GAIA, AgentDojo, WildClawBench, and LHTB, followed by direct verification of current public repositories and benchmark documentation.

It also follows the Matt Pocock `to-spec` principle that the spec should record decisions already aligned in discussion, identify the highest useful testing seam, and keep implementation details below that seam out of the design until the implementation plan is written.
