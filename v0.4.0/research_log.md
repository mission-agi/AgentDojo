# TaskPilot v0.4.0 — Research Log

**Date:** 2026-03-10
**Cycle:** v0.4.0
**Focus:** Simulation hardening, MAST expansion, structured validation

---

## Frameworks Studied

| Framework | Version | Key Takeaway |
|-----------|---------|-------------|
| CrewAI | 0.102+ (2025) | `output_pydantic` schema validation for task outputs; `guardrail` callable on task completion; structured memory with `kickoff_for_each` batch processing |
| LangGraph | 0.3+ (2025) | Compile-time state schema validation; `MemorySaver` checkpoint replay; conditional edge routing with typed state |
| AutoGen | 0.4+ (2025) | Composable termination conditions (`MaxMessageTermination`, `TextMentionTermination`); nested chats for scoped conversations; `SelectorGroupChat` for dynamic role dispatch |
| MetaGPT | 0.8+ (2025) | `cause_by` message routing for event chain tracing; JSON schema validation for intermediate artifacts; SOP-driven role workflows |
| DSPy | 2.5+ (2025) | `dspy.Assert` (hard) and `dspy.Suggest` (soft) inline assertions; typed predictors with Pydantic enforcement; metric-driven optimization |

## Top 10 Papers

| # | Title | Year | Relevance |
|---|-------|------|-----------|
| 1 | Why Do Multi-Agent LLM Systems Fail? (MAST taxonomy) | 2025 | Defines 14 failure modes; directly provides MAST taxonomy for SIM_010 (reward_hacking) and SIM_011 (verification_gaming) |
| 2 | AgentBench: Evaluating LLMs as Agents | 2023 | Structured success metrics per environment; failure categorization methodology |
| 3 | MetaGPT: Meta Programming for Multi-Agent Framework | 2023 | SOP-driven roles; `cause_by` message routing; structured artifact validation |
| 4 | AutoGen: Enabling Next-Gen LLM Applications | 2023 | Composable termination conditions; nested chats for challenge resolution |
| 5 | DSPy: Compiling Declarative LM Calls into Self-Improving Pipelines | 2023 | Assert/Suggest predicates; typed signatures; metric-driven compilation |
| 6 | DSPy Assertions: Computational Constraints for Self-Refining LM Pipelines | 2024 | 35.7% quality improvement with assertions; maps to exit criteria enforcement |
| 7 | Voyager: Open-Ended Embodied Agent with LLMs | 2023 | Skill library with verification functions; self-verification pattern |
| 8 | CAMEL: Communicative Agents for Mind Exploration | 2023 | Role-playing protocol; inception prompting; role specialization benefits |
| 9 | Reflexion: Language Agents with Verbal Reinforcement Learning | 2023 | Episodic memory for cycle-over-cycle learning; 22% improvement on coding tasks |
| 10 | TaskBench: Benchmarking LLMs for Task Automation | 2023 | Task graph correctness metrics (node F1, edge F1); orchestration graph validation |

## Next 10 Backlog

| # | Title / Topic | Year | Why Process Next |
|---|--------------|------|-----------------|
| 11 | Reward Hacking in RLHF (Anthropic) | 2024 | Catalogues reward gaming strategies; informs SIM_010 |
| 12 | Language Agent Tree Search (LATS) | 2023 | Backtracking for agent failures; alternative to linear phase-gate |
| 13 | AgentVerse | 2023 | Parallel multi-agent simulation with collaboration primitives |
| 14 | Chain-of-Verification (CoVe) | 2023 | Verification-plan pipeline; informs artifact quality checking |
| 15 | Scalable Multi-Agent RL with Agent-Specific Global State | 2024 | State management for large agent counts |
| 16 | Generative Agents (Park et al.) | 2023 | Agent memory architecture; informs memory search design |
| 17 | ToolLLM | 2023 | Tool selection evaluation; informs skill dispatch quality |
| 18 | Measuring Faithfulness in Chain-of-Thought Reasoning | 2024 | Detecting unfaithful reasoning; relevant to verification gaming |
| 19 | AgentOps: Observability for AI Agent Systems | 2024-2025 | Production observability patterns; informs event bus |
| 20 | SmartPlay: Benchmark for LLMs as Intelligent Agents | 2023 | Multi-dimensional scoring rubrics |

---

## Adopted Patterns (v0.4.0)

### PATTERN_035: Pydantic-Style Schema Validation for Simulation Outcomes
- **Source:** CrewAI `output_pydantic` + MetaGPT JSON schema validation
- **Applies to:** simulation_harness.py `_is_failure_detected()`
- **Implementation:** Replace `expected_outcomes` strings with structured `expected_detections` schema (detector, skill, finding_type, severity). Validator matches on role+skill+finding_type instead of substring.
- **Addresses:** BUG-005
- **Expected KPI impact:** artifact_correctness 0.95 -> 0.97

### PATTERN_036: Assert/Suggest Binary Exit Criteria Predicates
- **Source:** DSPy `dspy.Assert` and `dspy.Suggest`
- **Applies to:** exit_criteria_validator.py (new)
- **Implementation:** 14 measurable patterns (regex) + 7 vague word patterns. Each criterion must contain a quantitative, artifact, or process assertion. Vague words rejected.
- **Addresses:** BUG-006
- **Expected KPI impact:** skill_completion_rate 0.98 -> 1.00

### PATTERN_037: cause_by Event Chain Tracing
- **Source:** MetaGPT `cause_by` message routing
- **Applies to:** event_bus.yaml, orchestration_graph.yaml
- **Implementation:** Added `caused_by_event_id` field to event emissions. Enables root-cause tracing: skill_failed -> challenge_raised -> gate_blocked chain.
- **Expected KPI impact:** Enables event_chain_traceability metric

### PATTERN_038: Composable Termination Conditions
- **Source:** AutoGen `MaxMessageTermination`, `TextMentionTermination`
- **Applies to:** dependency_checker.py gate conditions
- **Implementation:** Gate conditions modeled as composable predicates (AllConditionsMet, MetricThreshold, ArtifactExists).
- **Expected KPI impact:** orchestration_reliability maintained at 1.0

### PATTERN_040: Guardrail Callable Pattern
- **Source:** CrewAI task `guardrail` parameter
- **Applies to:** exit_criteria_validator.py integration at BUILD exit
- **Implementation:** EXIT_CRITERIA_VALIDATION state runs validator after BUILD, blocks TEST entry if pass rate < 90%.
- **Expected KPI impact:** Prevents malformed artifacts from reaching TEST

### PATTERN_041: Reward Hacking Detection (SIM_010)
- **Source:** MAST paper M11 + Anthropic reward hacking research
- **Applies to:** scenarios.yaml SIM_010
- **Implementation:** Scenario injects 50 assertion-free tests gaming 95% coverage. QA must detect assertion density = 0.
- **Expected KPI impact:** mast_failure_coverage 10/14 -> 11/14

### PATTERN_042: Verification Gaming Detection (SIM_011)
- **Source:** MAST paper M13
- **Applies to:** scenarios.yaml SIM_011
- **Implementation:** Scenario injects design doc passing word-count but missing trade-off analysis. PE must detect structural incompleteness.
- **Expected KPI impact:** mast_failure_coverage 11/14 -> 12/14

### PATTERN_043: BM25 Keyword Search
- **Source:** Standard IR technique, DSPy evaluation patterns
- **Applies to:** memory_search.py (new)
- **Implementation:** BM25 with k1=1.5, b=0.75 over JSONL event logs. Pure Python, zero dependencies.
- **Expected KPI impact:** Enables memory_query_relevance metric

### PATTERN_044: Runtime Dependency DAG Validation
- **Source:** LangGraph compile-time validation + MetaGPT cause_by ordering
- **Applies to:** dependency_checker.py (new)
- **Implementation:** Build DAG from depends_on fields, topological sort, detect cycles, validate execution order.
- **Expected KPI impact:** orchestration_reliability >= 0.98

---

## Logged for v0.5.0+ (Not Adopted)

| Pattern | ID | Reason to Defer |
|---------|----|-----------------|
| Checkpoint-Based Scenario Replay | PATTERN_039 | Current end-to-end simulation fast enough for 11 scenarios |
| Reflexion Memory | PATTERN_045 | Already tracking via kpi_results.json; formal reflection adds value after 5+ cycles |
| Nested Conversation for Challenge Resolution | PATTERN_046 | Challenge lifecycle states defined but volume doesn't justify runtime enforcement |

## Rejected Patterns

| Pattern | Source | Reason |
|---------|--------|--------|
| LLM-as-Judge quality scoring | CrewAI `crewai test` | Susceptible to reward hacking; deterministic assertions preferred |
| CrewAI Episodic Recall Memory | CrewAI memory | Already rejected in v0.3.0 (PATTERN_027); JSONL sufficient at current scale |
| Full MIPROv2 Optimization Loop | DSPy MIPROv2 | Insufficient historical data; revisit after 10+ cycles |
| Scatter-Gather Parallelism | LangGraph Send API | Sequential phase-gate model; not needed at 5-role scale |
| Selector Group Chat | AutoGen SelectorGroupChat | Conflicts with deterministic role ordering |
