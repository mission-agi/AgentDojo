# Cycle Plan — v0.4.0

## Date: 2026-03-10
## Predecessor: v0.3.0 (promoted, overall_weighted_score 0.96)
## Branch: feature/v0.4.0-simulation-hardening-mast-expansion

## Priority List (5 items)

### P1: [FIX-NOW] BUG-005 — Structured Outcome Validation
**Problem:** `_is_failure_detected()` uses naive string matching (`"should detect" in expected_outcomes`) instead of structured assertions against failure taxonomy.
**Solution:** Refactor simulation harness to validate outcomes against FailureMode enum and structured outcome schema. Each scenario declares `expected_detections` (already present in v0.3.0 scenarios) — harness validates detector role, skill, and finding classification match.
**KPI Target:** artifact_correctness ≥ 0.97, defect_detection measurement accuracy improved
**Bug:** BUG-005

### P2: [FIX-NOW] BUG-006 — ExitCriteria Validator
**Problem:** Skill exit criteria can be vague ("reviewed by X", "meets quality bar"). No validation at registration time.
**Solution:** Add `exit_criteria_validator.py` that parses all skill YAML files and enforces:
- Each criterion must be a binary assertion (contains measurable verb: "exists", "passes", "≥", "==", "contains", "zero")
- Each criterion must have a `verification_method` (manual_checklist, automated_test, artifact_exists, metric_threshold)
- Reject criteria with vague words: "reviewed", "quality bar", "sufficient", "appropriate"
**KPI Target:** skill_completion_rate → 1.00
**Bug:** BUG-006

### P3: [IMPROVE] MAST Coverage 10/14 → 12/14
**Problem:** 4 remaining uncovered MAST failure modes. Most relevant for TaskPilot: reward_hacking (skill gaming its own exit criteria) and verification_gaming (producing artifacts that pass checks but are low quality).
**Solution:** Add SIM_010 (reward_hacking) and SIM_011 (verification_gaming) scenarios.
- SIM_010: Skill claims 100% test coverage by writing trivial assertion-free tests
- SIM_011: SDE produces design doc that passes word-count checks but lacks actual trade-off analysis
**KPI Target:** mast_failure_coverage ≥ 0.86

### P4: [IMPROVE] Runtime Dependency Enforcement
**Problem:** `depends_on/produces` fields exist in YAML but no runtime check validates artifact existence before skill activation.
**Solution:** Add `dependency_checker.py` that reads skill manifests and validates all `depends_on` artifacts exist before dispatching a skill. Integrated into simulation harness as pre-execution check.
**KPI Target:** orchestration_reliability ≥ 0.98

### P5: [IMPROVE] Keyword Memory Search
**Problem:** Memory system supports only filter-by-field queries. Cannot search "what did we learn about protocol extraction" across cycles.
**Solution:** Add `memory_search.py` with BM25-style keyword search over training_log.jsonl `rationale` and `notes` fields. No external dependencies.
**KPI Target:** New KPI: memory_query_relevance ≥ 0.80

## Items NOT Addressed This Cycle
- Semantic/vector search (deferred — BM25 keyword search is sufficient first step)
- Event emission integration with Claude Code hooks (not needed for simulation)
- Loop tracking automation (lower priority than simulation correctness)
- Remaining 2 MAST modes after this cycle (M13 capability_overshoot, M14 misaligned_sub_goals — for v0.5.0)
