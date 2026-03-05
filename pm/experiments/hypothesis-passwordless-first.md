# Hypothesis: Passwordless-First Improves Developer Conversion

**Date:** 2026-03-03  
**Owner:** Product Team (Auth Initiative)  
**Status:** Ready to Test

---

## Hypothesis Statement

We believe that **positioning authentication as "passwordless by default" with email/password as fallback**  
will cause **developer sign-up-to-integration conversion rate to increase by 15%+**  
for **engineers and tech leads evaluating OAuth providers**.

### Rationale

**Evidence supporting hypothesis:**
1. MojoAuth 2026 study: 68.4% of developers cite "implementation speed" as #1 factor in auth provider choice
2. Passwordless authentication now accounts for 73% of all logins (MojoAuth 2026)
3. Apple's 73% YoY growth and Google's passkey autofill adoption show passwordless is market expectation
4. Developer buyer psychology: "Implementation speed" and "not wasting time on auth complexity" drive adoption

**Why we think passwordless-first matters:**
- Traditional OAuth providers default to password + email, which feels outdated in 2026
- Developers perceive "passwordless-first" as more modern, secure-by-default, less maintenance burden
- Positioning creates perception of being "ahead of the curve" vs competitors
- Reduces developer anxiety about auth complexity ("passwordless is managed for us")

**Riskiest assumption:** Developers will actually value passwordless-first positioning enough to choose us over Google OAuth (which has 75% market share and is simpler to understand).

---

## Test Method

**Primary: Landed A/B Test** (Landing page conversion comparison)  
**Secondary: Developer Interview Validation** (Qualitative confirmation)

### Landing Page A/B Test

**What we're testing:**
- **Control (A):** Traditional messaging: "Sign in with Google, Apple, or GitHub. Full OAuth2 support."
- **Treatment (B):** Passwordless-first messaging: "Passwordless authentication by default. Passkeys, biometric, email—your choice. OAuth providers as backup."

**Where it lives:**
- Landing page for `/oauth-provider` product
- Targeted at developers evaluating auth providers
- Traffic from: Google Search ("OAuth2 for developers"), ProductHunt, GitHub trending

**Variants:**
```
Control (A): Traditional positioning
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Hero: "OAuth2 for Modern Apps"
Subheading: "Sign in with Google, Apple, GitHub. Full OAuth2 compliance."
CTA: "Start Building"

Treatment (B): Passwordless-first positioning
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Hero: "Passwordless Authentication. By Default."
Subheading: "Passkeys, biometrics, email magic links. No passwords needed. Integrate in 1 hour."
CTA: "Get Started (Free)"
```

---

## Key Metrics

### Primary Metric: Developer Sign-Up Conversion Rate
**Definition:** % of developers who land on OAuth provider page → create account → begin integration  
**Current Baseline:** Unknown (new product); estimate ~3% based on industry benchmarks  
**Success Target:** +15% improvement (4.5% conversion rate)

**Why this metric:**
- Directly measures whether positioning influences developer decision to try us
- Early indicator of market fit (do developers want passwordless-first?)
- Actionable (if it doesn't move, positioning is wrong)
- Auditable (tracked via event instrumentation)

### Secondary Metrics (Guardrails)

| Metric | Baseline | Guardrail | Reason |
|--------|----------|-----------|--------|
| **Bounce rate** | 45% | <60% | Don't scare away traffic with confusing messaging |
| **Time on page** | 45 seconds | >30 seconds | Ensure message is being read, not ignored |
| **Feature request: "Do you support passwords?"** | Baseline | <20% increase | Don't create false expectation that passwords don't exist |
| **NPS of sign-up experience** | — | >7/10 | Early signal that message resonates |

---

## Sample Size & Duration

### Statistical Power Calculation

**Assumptions:**
- Baseline conversion rate: 3.0%
- Minimum detectable effect (MDE): 15% relative improvement (3.0% → 3.45%)
- Confidence level: 95% (p < 0.05)
- Statistical power: 80%
- Two-tailed test

**Sample size calculation:**
Using online calculator (statsmodels):
- Required sample per variant: ~10,000 developers
- Total sample: 20,000 developers (A + B)

**Traffic & Duration:**
- Current OAuth product traffic: ~500 developers/week
- To reach 20,000 sample: 40 weeks (9.5 months)
- **Option A (Patience):** Run for 40 weeks, collect full sample, high confidence
- **Option B (Shorter runway):** Run for 4 weeks with ~2,000 samples, accept higher variance, make directional call
- **Recommendation:** Option B — 4 weeks. If we see 10%+ improvement trend, that's signal enough to proceed; if flat or negative, stop and pivot.

**Revised Sample Sizing (4-week test):**
- Weeks to run: 4
- Projected traffic: ~2,000 developers (50/50 split, 1,000 per variant)
- Statistical power: 50% (lower, but directional)
- Interpretation: 10%+ relative improvement = proceed; <5% = stop and iterate messaging

---

## Success Criteria

### Ship It 🚀
- **Primary metric:** Conversion rate improves by 10%+ (absolute measurement or statistical significance at p < 0.10)
- **Secondary signals:** Time on page >35 seconds, bounce rate <55%, NPS feedback positive
- **Qualitative:** Developer interviews confirm "passwordless-first" resonates and differentiates from Google
- **Decision:** Invest in passwordless-first product development; make this our core positioning

### Iterate 🔄
- **Primary metric:** Conversion rate improves by 5-10% (directional signal, not statistically significant)
- **Secondary signals:** Mixed signals (some guardrails pass, some fail)
- **Decision:** Iterate messaging; test variations (e.g., "Passwordless + Privacy" combined, or "Fastest setup + Passwordless")

### Kill It 🛑
- **Primary metric:** Conversion rate flat or declines vs control (<5% improvement)
- **Secondary signals:** Higher bounce rate, lower NPS, developer feedback indicates "passwordless-first is confusing"
- **Decision:** Abandon passwordless-first positioning; fall back to "Privacy-first OAuth" or "Developer-friendly OAuth" positioning

### Guardrails (Hard Stops)
- **Feature request spike:** If >25% of signups ask "Do you support passwords?", messaging is creating false expectations → adjust immediately
- **NPS < 5:** If early feedback is negative, messaging isn't resonating → iterate within 2 weeks

---

## Measurement Approach

### Event Instrumentation

Track these events in analytics:
```
Event: oauth_landing_page_view
  variant: "control" | "treatment"
  source: "google_search" | "producthunt" | "github" | "direct"
  timestamp: [UTC]

Event: oauth_signup_attempt
  variant: "control" | "treatment"
  email: [hashed]
  timestamp: [UTC]

Event: oauth_integration_begin
  variant: "control" | "treatment"
  email: [hashed]
  selected_provider: "google" | "apple" | "github" | "webauthn"
  timestamp: [UTC]

Event: oauth_integration_complete
  variant: "control" | "treatment"
  email: [hashed]
  provider: [selected]
  time_to_complete_hours: [integer]
  timestamp: [UTC]

Event: developer_feedback
  variant: "control" | "treatment"
  email: [hashed]
  feedback: [open text]
  nps_score: [1-10]
  timestamp: [UTC]
```

### Data Collection

| Metric | Collection Method | Frequency | Owner |
|--------|------------------|-----------|-------|
| Conversion rate | Analytics (event tracking) | Real-time, reported daily | Data team |
| Bounce rate | Google Analytics / Segment | Real-time | Product |
| Time on page | Google Analytics | Real-time | Product |
| NPS | In-page survey popup (exit intent) | Ongoing | Product |
| Feature requests | Intercom/support tickets | Ongoing | Customer Success |
| Developer quotes | Manual collection during interviews | Weekly | PM |

---

## Launch Checklist

- [ ] Events instrumented and tested in staging
- [ ] A/B test configured (50/50 split, random assignment)
- [ ] Baseline metrics captured and documented
- [ ] Sample size and duration agreed (4 weeks)
- [ ] Success/failure criteria socialized with team
- [ ] Rollback plan documented (if guardrails breached, revert to control)
- [ ] Daily monitoring dashboard set up
- [ ] Team briefed on experiment and what to expect

---

## Risk Mitigation

### What could go wrong?

1. **Passwordless message confuses non-technical audiences**
   - Risk: Landing page gets traffic from non-developers (students, hobbyists)
   - Mitigation: Add audience targeting filter to analytics (e.g., "professional developer email domain")
   - Mitigation: Add messaging to clarify "For developers / engineers"

2. **Passkey support isn't actually ready**
   - Risk: Developers sign up expecting passkeys, find they don't exist
   - Mitigation: Show mockup/roadmap of passkey support, set expectation: "In development, available Q2 2026"
   - Mitigation: Segment experiment to developers who understand "in development" vs "available now"

3. **Google OAuth being 75% market share means developers just choose default**
   - Risk: No messaging will overcome the habit of using Google
   - Mitigation: This is the test! If conversion doesn't improve, we learn that positioning doesn't matter (features do)
   - Mitigation: If flat, pivot to Feature-based differentiation (privacy + speed)

4. **Competitor sees test, copies messaging**
   - Risk: Competitors (Auth0, FusionAuth) add passwordless-first positioning
   - Mitigation: Passwordless-first is positioning, not feature; move fast to build actual product
   - Mitigation: Patent if possible (unlikely), or focus on feature + positioning combo

---

## Decision Tree

```
Test Results →

If conversion ↑ 10%+ AND NPS > 7 AND guardrails pass:
  → SHIP: Passwordless-first is our positioning
  → Next: Design passwordless-first product experience
  
If conversion ↑ 5-9% OR mixed signals:
  → ITERATE: Test variations (e.g., "Passwordless + Privacy")
  → Next: Run variant test with adjusted messaging
  
If conversion flat/↓ OR NPS < 5 OR guardrails breach:
  → KILL: Passwordless-first messaging doesn't work
  → Next: Test alternative positioning ("Privacy-first" or "Developer-friendly")
```

---

## Success Looks Like

**Week 1:** Events flowing correctly, 250 users per variant enrolled  
**Week 2:** Early signal emerges (10%+ trend toward treatment)  
**Week 4:** Final results: treatment conversion is 3.4-3.6% vs control 3.0%, NPS positive, developer interviews confirm value  
**Outcome:** Team votes to pursue passwordless-first product development

---

## Owner & Accountability

- **Test Owner:** Product Manager (Auth Initiative)
- **Analytics Owner:** Data Engineer (event instrumentation)
- **Decision Maker:** Chief Product Officer (Ship/Iterate/Kill call)
- **Review Cadence:** Daily during test, post-test review with team

---

## Reference & Data Sources

- MojoAuth 2026 Developer Authentication Preferences Study
- Market trends: 73% of authentications are passwordless
- Buyer psychology profile: Developer-First segment (implementation speed priority)
- Competitor analysis: None of top 4 providers position passwordless-first
