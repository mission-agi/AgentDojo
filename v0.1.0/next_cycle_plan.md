# Next Cycle Plan (v0.2.0)

## Predecessor: v0.1.0 (baseline)
## Planned improvements: up to 5

---

## Priority 1: [FIX] BUG-001 — Event emission hooks not integrated
- **Source:** TASKPILOT-KNOWN-BUGS-AND-IMPROVEMENTS.md
- **Why now:** Highest-severity unfixed bug. Without event hooks, training_log.jsonl must be manually populated. Blocks automated KPI tracking.
- **Expected KPI impact:** skill_completion_rate +0.10, orchestration_reliability +0.05
- **Approach:** Implement hook triggers in orchestrator/SKILL.md that emit JSONL events to .project/events.jsonl on skill start, completion, failure. Wire into simulation harness for automated tracking.

## Priority 2: [FIX] BUG-002 — Loop tracking not automated
- **Source:** TASKPILOT-KNOWN-BUGS-AND-IMPROVEMENTS.md
- **Why now:** Second-highest bug. Loop detection is critical for orchestration_reliability (currently 0.60). Manual tracking misses loops during long runs.
- **Expected KPI impact:** orchestration_reliability +0.10, human_intervention_rate -0.10
- **Approach:** Add loop counter to orchestrator state schema. Auto-append to loops.md on each iteration. Add loop limit enforcement to simulation harness.

## Priority 3: [IMPROVE] Enhance simulation harness for Build/Quality phase detection
- **Source:** v0.1.0 KPI results — defect_detection_rate 0.56 (target 0.85), scenarios 2 & 4 failed
- **Why now:** Largest KPI gap. Current mock detection is too simplistic for Build/Quality phases where failures occur during code execution.
- **Expected KPI impact:** defect_detection_rate +0.20, defect_escape_rate -0.20, overall_weighted_score +0.10
- **Approach:** Add phase-specific detection models to simulation harness. Model Build phase failures (compilation errors, test failures, dependency conflicts) and Quality phase failures (coverage gaps, security vulnerabilities, performance regressions) with distinct detection probability distributions.

## Priority 4: [FIX] BUG-003 — Skill manifest lacks dependency metadata
- **Source:** TASKPILOT-KNOWN-BUGS-AND-IMPROVEMENTS.md
- **Why now:** Blocking automated prerequisite chain validation. Skills currently cannot declare what they depend on or produce.
- **Expected KPI impact:** skill_completion_rate +0.08
- **Approach:** Add YAML frontmatter to each skill .md file with depends_on and produces fields. Update skill-manifest.json to reference YAML skill definitions. Add dependency validation to simulation harness.

## Priority 5: [IMPROVE] Add 5 new simulation scenarios targeting weak KPIs
- **Source:** v0.1.0 simulation results — only 5 scenarios, 2 failed, 1 partial
- **Why now:** Need broader scenario coverage to improve measurement confidence. Current scenarios don't adequately test Build/Quality phase failures.
- **Expected KPI impact:** test_coverage +0.15, overall measurement confidence improvement
- **Approach:** Create scenarios for: (6) dependency version conflict in Build, (7) test flakiness cascade, (8) cross-domain artifact mismatch, (9) gate approval timeout, (10) parallel skill resource contention.

---

## Research backlog for v0.2.0
Papers to study (from v0.1.0 backlog):
1. "Scalable Multi-Agent RL with Agent-Specific Global State" — for state management patterns
2. "Dynamic Task Allocation in MAS" — for skill selection optimization
3. "AgentVerse: Facilitating Multi-Agent Collaboration" — for collaboration primitives

Production systems to study:
- Semantic Kernel (Microsoft) — planner patterns, skill chaining
- DSPy — optimization-based prompt engineering for skills

## Hypotheses to test
- H1: Adding phase-specific detection models will raise defect_detection_rate above 0.75
- H2: Automated loop tracking will reduce human_intervention_rate below 0.30
- H3: Dependency metadata in skills will improve skill_completion_rate above 0.70

## Success criteria for v0.2.0 promotion
- overall_weighted_score >= 0.65 (up from 0.58 baseline)
- defect_detection_rate >= 0.70 (up from 0.56)
- orchestration_reliability >= 0.75 (up from 0.60)
- No regressions on artifact_correctness (must stay >= 0.80)
