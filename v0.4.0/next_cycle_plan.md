# TaskPilot v0.5.0 — Next Cycle Plan

**Created:** 2026-03-10
**Baseline:** v0.4.0 (overall_weighted_score: 0.97)

---

## Priorities (max 5)

### P1: Fix 14 vague exit criteria (target: >= 90% pass rate)
- **Type:** IMPROVEMENT
- **From:** exit_criteria_validator v0.4.0 results (64.10% pass rate)
- **Details:** Rewrite 14 failing criteria across PE, PM, QA, SDE, UX, DOC, RM, SEC skills.
  Add explicit thresholds, artifact names, or binary predicates.
- **KPI target:** exit_criteria_pass_rate >= 0.90
- **Effort:** Medium (each criterion needs rewriting with measurable verb)
- **Risk:** Low — criteria rewriting is mechanical, no architectural changes

### P2: Add SIM_012 (hallucination) and SIM_013 (tool_misuse)
- **Type:** IMPROVEMENT
- **From:** MAST coverage gap — 4/20 modes uncovered
- **Details:** Create scenarios for hallucination (agent produces factually incorrect output)
  and tool_misuse (agent invokes wrong skill or passes wrong parameters).
  These are canonical MAST modes with no scenario coverage.
- **KPI target:** mast_failure_coverage 0.80 -> 0.90 (18/20)
- **Effort:** Medium — need to design realistic failure injections
- **Risk:** Medium — hallucination detection is inherently harder to model

### P3: Runtime event chain validation (caused_by_event_id)
- **Type:** IMPROVEMENT
- **From:** PATTERN_037 added but not enforced
- **Details:** Add validation in simulation harness that every `gate_blocked` event has a
  non-null `caused_by_event_id` linking to the triggering failure. Verify chain completeness.
- **KPI target:** event_chain_traceability >= 0.95
- **Effort:** Low — add validation logic to existing harness
- **Risk:** Low — structural validation only

### P4: KPI range assertion in harness
- **Type:** BUG PREVENTION
- **From:** v0.4.0 Phase 4 discovered KPI values > 1.0 due to formula bugs
- **Details:** Add post-computation assertion that all KPI values are in [0.0, 1.0] range.
  Fail loudly if any KPI exceeds bounds, with descriptive error.
- **KPI target:** No KPI value outside [0.0, 1.0]
- **Effort:** Low — single validation function
- **Risk:** Low

### P5: Checkpoint-based scenario replay (PATTERN_039)
- **Type:** IMPROVEMENT
- **From:** Research log v0.4.0 — deferred LangGraph checkpoint replay pattern
- **Details:** Serialize orchestrator state at checkpointable nodes. For each scenario,
  specify `inject_at_state` and `expected_halt_at`. Harness loads checkpoint, injects
  failure, runs forward. Enables targeted regression testing as scenario count grows.
- **KPI target:** Simulation execution time < 50% of end-to-end for targeted tests
- **Effort:** High — requires checkpoint serialization infrastructure
- **Risk:** Medium — checkpoint format must be backward-compatible

---

## Hypotheses

1. **Fixing 14 vague criteria will improve skill_completion_rate** — currently at 1.0 because
   the metric counts skill presence, not criteria quality. After validator integration,
   skills with vague criteria should be counted as incomplete.
2. **Hallucination scenarios will require semantic validation** — unlike structural checks
   (assertion density, section headers), detecting factually incorrect output may need
   a reference artifact for comparison.
3. **KPI range assertions will prevent future formula bugs** — catching out-of-range
   values during Phase 4 TEST rather than during manual review saves debugging time.

## Research Backlog (from v0.4.0)

Papers 11-20 from the v0.4.0 research log should be processed:
- #11: Reward Hacking in RLHF (Anthropic) — informs SIM_010 refinement
- #14: Chain-of-Verification (CoVe) — informs artifact quality checking
- #16: Generative Agents (Park et al.) — agent memory architecture
- #18: Measuring Faithfulness in CoT Reasoning — verification gaming detection
- #19: AgentOps observability patterns — event bus improvements
