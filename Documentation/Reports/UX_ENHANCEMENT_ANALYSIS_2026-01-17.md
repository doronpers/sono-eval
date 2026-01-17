# UX Enhancement Analysis (2026-01-17)

## Summary

Sono-Eval’s UX opportunities cluster in three areas: mobile onboarding decision load, API error guidance, and documentation entry points. The recommendations below map to measurable outcomes and include implementation plans with exact file targets and code examples.

---

## 1) Mobile Onboarding & Progressive Disclosure

**Finding**: The mobile welcome screen asks users to expand three discovery cards plus a process accordion before reaching the CTA. This creates 5+ decisions before action. Additionally, path selection lacks a quick path for new users and the results page exposes all sections at once.

**Evidence**:
- `index.html` uses three `.discovery-card` blocks plus a separate `expandable-section` before CTA interaction. (See `src/sono_eval/mobile/templates/index.html` lines 11–134.)
- `results.html` shows score, summary, path scores, findings, strengths, motives, recommendations, and actions in a single linear flow. (See `src/sono_eval/mobile/templates/results.html` lines 6–80.)

**Goal**: Reduce cognitive load by 40% and increase completion rate by 25%.

---

## 2) API Error Responses & Developer Experience

**Finding**: Error responses lack actionable guidance (examples, suggestions, documentation links). The current `ErrorResponse` model does not include a help field, and health checks do not surface troubleshooting hints for each component.

**Evidence**:
- `ErrorResponse` currently contains only `error`, `error_code`, `message`, `details`, `request_id`. (See `src/sono_eval/utils/errors.py` lines 49–56.)
- Health checks return component status and details but no remediation guidance. (See `src/sono_eval/api/main.py` lines 230–534.)

**Goal**: 50% faster error resolution and 30% reduction in support burden.

---

## 3) Documentation Navigation & First-Time User Experience

**Finding**: The root README presents multiple competing CTAs (“Start Here”, “Quick Start”, “Documentation”, etc.), causing decision paralysis. CONTRIBUTING.md also contains overlapping quickstarts.

**Evidence**:
- README CTA line cluster at lines 18–23 shows multiple “Start here” options. (See `README.md` lines 18–23.)
- CONTRIBUTING.md has three separate Quick Start paths, each with its own instructions. (See `CONTRIBUTING.md` lines 6–64.)

**Goal**: 60% faster time-to-first-success and 35% improved retention.

---

## Recommended Execution Order

1. **API Errors** (quick implementation, immediate developer value)
2. **Mobile UX** (highest user impact)
3. **Docs Navigation** (high impact, low risk)

---

## Success Metrics & Validation

- **Mobile UX**: completion rate, time-to-first-step, mobile bounce rate.
- **API Errors**: reduction in repeated support tickets, improved API docs feedback.
- **Docs**: reduced onboarding time, improved README click-through.

Each implementation plan includes testing steps, success criteria, and rollback instructions.

