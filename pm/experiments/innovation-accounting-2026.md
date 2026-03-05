# Innovation Accounting Dashboard — OAuth2 Social Login Feature

**Product:** OAuth2 Social Login (Passwordless-First, Privacy-Focused)  
**Report Date:** 2026-03-03  
**Reporting Period:** Q1 2026 (Validation Phase)

---

## Current Baseline (Pre-Launch)

As of 2026-03-03, we have not shipped the OAuth2 product yet. This dashboard establishes baselines for the validation experiments we're about to run.

| Metric | Baseline Value | Source | Notes |
|--------|---|---|---|
| Developer sign-up conversion (landing → account) | ~3% (estimated industry) | Benchmark | Will measure in Experiment 1 |
| Privacy-conscious switching intent | 2/10 (very low) | Buyer psychology research | Google has 75% mindshare; hard to break |
| Passwordless adoption in new auth flows | 73% of logins (market) | MojoAuth 2026 | Our feature parity target |
| Developer time-to-integrate | 30-40 hours (competitors) | Buyer research | Our target: <2 hours |
| Privacy audit availability | 0% (we don't have audits yet) | Internal | Must be built before launch |

---

## Experiments This Quarter (Q1 2026)

### Experiment 1: Passwordless-First Messaging

| Aspect | Details |
|--------|---------|
| **Hypothesis** | Positioning as "passwordless by default" increases developer conversion by 15%+ |
| **Primary Metric** | Developer sign-up conversion: 3% → 3.45% |
| **Duration** | 4 weeks (2026-03-10 to 2026-04-07) |
| **Sample** | ~2,000 developers (1,000 per variant) |
| **Status** | Ready to launch |
| **Expected Outcome** | **SHIP** if +10% improvement; **ITERATE** if +5-10%; **KILL** if <5% |

**How It Moves the Needle:**
- If successful: Confirms developers care about passwordless-first positioning
- If fails: We pivot to feature-based positioning (privacy + speed)
- Informs entire product strategy and positioning for launch

---

### Experiment 2: Privacy Proof vs. Features

| Aspect | Details |
|--------|---------|
| **Hypothesis** | Emphasizing transparency (audits, open-source) drives privacy-conscious switching intent more than features |
| **Primary Metric** | Willingness-to-switch intent: 2.0 → 3.5+ on 1-10 scale |
| **Duration** | 6 weeks (2026-03-10 to 2026-04-21) |
| **Sample** | ~600 compliance officers / privacy advocates (300 per variant) |
| **Status** | Ready to launch |
| **Expected Outcome** | **SHIP** if +1.5 point increase; **ITERATE** if +0.5-1.5; **KILL** if <0.5 |

**How It Moves the Needle:**
- If successful: Confirms privacy audits / transparency are key differentiator
- If fails: We focus on features (email masking) or feature+speed combo
- Informs roadmap priority (audits vs. feature development)

---

## Learning Velocity Metrics

| Metric | Target | Status | Notes |
|--------|--------|--------|-------|
| **Experiments per quarter** | ≥3 | 2 planned | Adding 1 more if resources allow |
| **Win rate (positive experiments)** | 50%+ | TBD | Industry baseline is 40-50% |
| **Experiment cycle time (idea → result)** | 4-6 weeks | 4-6 weeks | Passwordless test runs 4 weeks |
| **Time to decision (result → Ship/Iterate/Kill)** | 1 week | Target | Friday result review, Monday decision |
| **Team engagement in experiments** | 80%+ awareness | Target | All hands briefing before launch |

---

## Three Engines of Growth — Current State

### Engine 1: Sticky (Retention)

**Goal:** Users who sign up stay and use the product repeatedly

| Metric | Target | Current | Gap |
|--------|--------|---------|-----|
| Day 1 retention (developer signup → first integration attempt) | >80% | Unknown | Need to measure post-launch |
| Day 7 retention (developer continues using) | >50% | Unknown | Need to measure post-launch |
| DAU/MAU ratio (daily / monthly active) | >40% | Unknown | Depends on developer workflow |
| NPS (developer satisfaction) | >50 | Unknown | Measured in experiments via survey |

**Hypothesis:** If passwordless-first and fast setup resonate (Exp 1 succeeds), retention will be high because developers feel they made the right choice.

**Worry:** If setup is still complex or passwordless isn't actually frictionless, retention will drop (developer realizes it's not as easy as promised).

---

### Engine 2: Viral

**Goal:** Users refer/recommend our OAuth provider to others

| Metric | Target | Current | Gap |
|--------|--------|---------|-----|
| Viral coefficient (K) | >1.0 | Unknown | Need usage data |
| Referral rate (% of developers who refer) | >20% | Unknown | Measured post-launch |
| NPS referral (% who would recommend) | >60% | Unknown | Measured in experiments |
| Time-to-referral (days from signup to first referral) | <30 days | Unknown | Depends on developer velocity |

**Hypothesis:** Developers who successfully integrate in 1 hour will immediately tell peers ("Check out this easy OAuth provider"). Viral coefficient likely >1.0 if experience is exceptional.

**Worry:** If integration is still complex or experience is average, no viral loop forms. Developers won't recommend us naturally.

---

### Engine 3: Paid (Monetization)

**Goal:** Free users convert to paid plans at acceptable cost

| Metric | Target | Current | Gap |
|--------|--------|---------|-----|
| Free-to-paid conversion | >5% | Unknown | Need pricing / feature tiers |
| LTV:CAC ratio | >3:1 | Unknown | Depends on pricing + acquisition cost |
| ARPU (Average Revenue Per User) | $100/mo | Unknown | Freemium model TBD |
| CAC payback period | <12 months | Unknown | Depends on conversion + pricing |

**Strategy:** Start with freemium (free core OAuth, paid advanced features like passkeys, audit logging, custom branding). Premium features unlock for developers at scale.

**Note:** Monetization is Phase 8+ (Launch). Phase 1-7 focus on product validation, not revenue.

---

## Decision Logic: Persevere / Pivot / Accelerate

```
Current State (2026-03-03): Validation Phase

CURRENT DECISION: VALIDATE
├─ Experiment 1 (Passwordless-First) results:
│  ├─ If SHIP ✓ → Move to Phase 2: Passwordless development
│  ├─ If ITERATE → Refine positioning, test again
│  └─ If KILL ✗ → Pivot to feature-based positioning
│
└─ Experiment 2 (Privacy Proof) results:
   ├─ If SHIP ✓ → Prioritize audits + open-source in roadmap
   ├─ If ITERATE → Test hybrid messaging (features + transparency)
   └─ If KILL ✗ → Focus on features, defer audits to Phase 8+

POST-EXPERIMENTS (April 2026): Strategic Decision
├─ If both experiments SHIP ✓✓:
│  └─ ACCELERATE → Full investment in passwordless + privacy positioning
│
├─ If one experiments SHIPS, one ITERATES:
│  └─ PERSEVERE → Proceed with strongest signal, iterate other axis
│
├─ If both experiments show mixed/kill signals:
│  └─ PIVOT → Reassess entire positioning, test new hypothesis
│     (e.g., "Developer-friendly OAuth" without passwordless/privacy focus)
│
└─ If experiments show conflicting results (dev segment wants speed, privacy segment wants proof):
   └─ SEGMENT → Build two products or two positioning tracks
```

---

## Red Flags & Course Correction Triggers

| Warning Sign | Trigger Action | Responsible |
|--------------|-------------|-------------|
| **Exp 1 shows 0% lift** | Kill passwordless-first positioning | PM + CPO |
| **Exp 1 shows negative lift** | Revert to traditional OAuth messaging | PM + CPO |
| **Exp 2 shows <10% click privacy audit** | Revise transparency message (too technical) | Product Marketing |
| **Guardrail breach (e.g., NPS <5)** | Pause test, debug messaging immediately | PM |
| **Lower than expected traffic** | Extend test duration or increase traffic allocation | Growth team |
| **Confusing feedback >15%** | Messaging is not resonating, iterate | Product + Marketing |

---

## Post-Experiment Learning Plan

### Week 4 (End of Exp 1): Passwordless Results Review

**Team meeting (2 hours):**
1. Review data: control vs. treatment conversion rates
2. Analyze qualitative feedback: "What did developers like/dislike?"
3. Check guardrails: bounce rate, NPS, feature requests
4. Make decision: Ship / Iterate / Kill
5. If Ship/Iterate: Design next test or proceed to development

**Stakeholders:** Product, Engineering, Marketing, CEO

---

### Week 6 (End of Exp 2): Privacy Results Review

**Team meeting (2 hours):**
1. Review data: switching intent control vs. treatment
2. Analyze interview themes: "What actually drives switching?"
3. Check guardrails: audit clicks, confusion feedback
4. Make decision: Ship / Iterate / Kill
5. If Ship: Create audit roadmap; if Kill: Focus on feature differentiation

**Stakeholders:** Product, Legal/Compliance, Marketing, CEO

---

### Week 7 (Strategic Synthesis): Integrated Decision

**Executive meeting (1 hour):**
1. Combine learnings from both experiments
2. Assess market fit signals (is our positioning resonating?)
3. Decide: Proceed to Phase 2 Validation or loop back to Phase 1 with new hypothesis
4. Set Phase 2-3 goals (validation → planning)

**Stakeholders:** CEO, CPO, CTO, VP Marketing

---

## Success Definition for Phase 1

**Phase 1 is successful if:**
1. ✅ Experiment 1 (Passwordless) shows +10% lift OR directional signal in interviews
2. ✅ Experiment 2 (Privacy Proof) shows +1.5 point switching intent OR strong interview validation
3. ✅ Combined signals indicate clear market differentiation (passwordless-first + privacy-transparent)
4. ✅ Team has confidence to commit to Phase 2 Validation

**Phase 1 is unsuccessful if:**
1. ❌ Both experiments show no lift (flat or declining conversion/intent)
2. ❌ Guardrails breached significantly (NPS <4, >20% "confusing" feedback)
3. ❌ Interviews reveal contradictory signals (developers want speed, market wants privacy; can't have both)
4. ❌ Competitive threat emerges (Google/Apple launches same features before we do)

---

## Budget & Resource Allocation

| Activity | Effort | Cost | Timeline |
|----------|--------|------|----------|
| **Experiment 1 (Passwordless)** | 2 weeks setup + 4 weeks runtime | $5K (traffic, survey tools) | Mar 10 - Apr 7 |
| **Experiment 2 (Privacy Proof)** | 2 weeks setup + 6 weeks runtime | $8K (survey, interviews) | Mar 10 - Apr 21 |
| **Interview follow-ups** | 40 hours (10 interviews × 4 hrs) | $3K (external recruiting) | Apr 1 - May 1 |
| **Data analysis + reporting** | 30 hours | $2K (data analyst time) | Apr 1 - May 15 |
| **Total Phase 1 Budget** | 12 weeks | $18K | Through May 2026 |

**Funding approved by:** CEO  
**Budget owner:** Product Manager

---

## Key Metrics & Dashboards

### Real-Time Experiment Dashboard (Updated Daily)

```
Experiment 1: Passwordless-First (Days 1-28)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Control (A): [Conversion: 3.0% | N: 500]
Treatment (B): [Conversion: ? | N: 500]
Status: [Running / Paused / Complete]
Guardrails: [All green / Yellow alert / Red]
Recommendation: [On track / Investigate / Halt]

Experiment 2: Privacy Proof (Days 1-42)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Control (A): [Intent: 2.1/10 | N: 150]
Treatment (B): [Intent: ? | N: 150]
Status: [Running / Paused / Complete]
Survey response rate: [X%]
Interviews scheduled: [5/15]
Recommendation: [On track / Investigate / Adjust]
```

### Learning Velocity Dashboard (Updated Weekly)

```
Q1 2026 Learning Goals
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Experiments planned: 2 / 3 (67%)
Experiments launched: 2 / 2 (100%) [✓ On track]
Experiments completed: 0 / 2 (0%)
Expected completion: Week 4-6 (On track)
Key learnings: [Updates as results arrive]
Team engagement: [8/10 team members participating]
```

---

## Measures of Success (Post-Experiment)

| Dimension | Success | Partial | Failure |
|-----------|---------|---------|---------|
| **Passwordless messaging resonance** | +10% conversion lift | +5-10% lift | <5% or negative |
| **Privacy proof value** | +1.5 point switching intent | +0.5-1.5 point lift | No lift |
| **Developer feedback** | >70% positive NPS | 50-70% positive | <50% positive |
| **Privacy-conscious feedback** | "Audits are game-changer" | "Interesting but not decisive" | "Don't care about audits" |
| **Team confidence** | "Definitely ship" | "Need clarification" | "Complete pivot needed" |
| **Competitive signal** | "We're differentiated" | "On par with competitors" | "Competitors ahead" |

---

## Next Phases (Gated by Experiment Results)

### Phase 2: Validation (Starts April 2026, gated on Exp 1 + 2 Ship/Iterate signals)
- Validate product assumptions (setup <2 hrs, passwordless works end-to-end)
- Test with developer cohort for 2 weeks
- Measure activation, time-to-integration, satisfaction

### Phase 3: Planning (Starts May 2026, gated on Phase 2 validation)
- Lock down feature set, roadmap, effort estimate
- Get stakeholder alignment on Phase 4-8 timeline
- Publish PRD and engineering requirements

### Phase 4+: Build, Test, Launch (Gated on Phase 1-3 validation)
- Only invest in build phase after learning from experiments
- Build with confidence, knowing market wants what we're building

---

## Ownership & Cadence

| Responsibility | Owner | Cadence |
|---|---|---|
| Daily experiment monitoring | Data Engineer | Daily standup |
| Weekly results summary | Product Manager | Weekly review |
| Guardrail escalation | Product Manager | Real-time alert |
| Interview recruitment & execution | Customer Research | Ongoing (Exp 2) |
| Analysis & synthesis | Data Analyst + PM | Weekly |
| Executive updates | VP Product | Weekly (CPO) + Monthly (CEO) |
| Strategic decision | CPO + CEO | End of experiment |

---

## Approval & Sign-Off

**Experiment Plan Approved By:**
- Chief Product Officer: _______________  Date: ___
- CEO: _______________  Date: ___
- Engineering Lead: _______________  Date: ___

**Ready to launch:** 2026-03-10 (pending approvals)

---

## References

- Hypothesis cards: `.pm/experiments/hypothesis-*.md`
- Buyer psychology profiles: `.pm/research/buyer-profile-*.md`
- Gap analysis: `.pm/gaps/2026-03-03-oauth-gaps.md`
- Market research: `.pm/competitors/oauth-market-trends-2026.md`
