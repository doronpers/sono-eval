# Implementation Plan 1: Mobile Onboarding & Progressive Disclosure

**Impact**: HIGH | **Effort**: MEDIUM | **Time**: 4–6h  
**Scope**: Mobile companion templates + CSS + client-side logic

---

## Prerequisites (exact files)

1. Welcome screen template: `src/sono_eval/mobile/templates/index.html` (current discovery cards at lines 11–134).  
2. Candidate start screen: `src/sono_eval/mobile/templates/start.html` (lines 4–123).  
3. Path selection: `src/sono_eval/mobile/templates/paths.html` (lines 4–210+).  
4. Results page: `src/sono_eval/mobile/templates/results.html` (lines 4–80).  
5. Styling and interactions: `src/sono_eval/mobile/static/style.css` + `src/sono_eval/mobile/static/script.js`.

---

## Task A — Replace Expandable Cards With 4-Value Grid

### Before (current)
- `src/sono_eval/mobile/templates/index.html` lines 11–134 contain three `.discovery-card` blocks plus a separate process accordion.

### After (target)
- Replace the discovery cards with a 4-value grid and a single “Learn more” accordion **after** the CTA.

#### Replace HTML (copy-paste)
**File**: `src/sono_eval/mobile/templates/index.html`  
**Replace** lines 11–134 with:

```html
<div class="value-grid" role="list">
    <div class="value-item" role="listitem">
        <span class="value-icon">✨</span>
        <h3>Explained Scores</h3>
        <p>See evidence for every score—no black boxes.</p>
    </div>
    <div class="value-item" role="listitem">
        <span class="value-icon">🎯</span>
        <h3>Choose Your Focus</h3>
        <p>Pick 1–4 skills that matter most to you.</p>
    </div>
    <div class="value-item" role="listitem">
        <span class="value-icon">⏱️</span>
        <h3>10–90 Minutes</h3>
        <p>Complete one area or a full profile at your pace.</p>
    </div>
    <div class="value-item" role="listitem">
        <span class="value-icon">📈</span>
        <h3>Actionable Growth</h3>
        <p>Get specific next steps to improve.</p>
    </div>
</div>

<div class="cta-section">
    <button class="primary-button" onclick="location.href='/mobile/start'">
        Let's Get Started
        <span class="button-arrow">→</span>
    </button>
    <p class="cta-subtext">No account needed • 10–90 minutes</p>
</div>

<div class="info-details">
    <button class="details-toggle" onclick="toggleDetails(this)">
        <span>How it works</span>
        <span class="toggle-icon">▼</span>
    </button>
    <div class="details-content" style="display: none;">
        <div class="detail-section">
            <h4>📋 The Process</h4>
            <ol>
                <li>Choose 1–4 skill areas</li>
                <li>Complete guided tasks</li>
                <li>Review scores + evidence</li>
                <li>Act on recommendations</li>
            </ol>
        </div>
        <div class="detail-section">
            <h4>🔒 Privacy</h4>
            <ul>
                <li>✅ No account required</li>
                <li>✅ Your code stays private</li>
                <li>✅ Transparent scoring</li>
            </ul>
        </div>
    </div>
</div>
```

#### Add JS toggle (copy-paste)
**File**: `src/sono_eval/mobile/templates/index.html`  
**Replace** the existing `toggleExpand` + `exploreDiscovery` functions (lines 140–187) with:

```javascript
function toggleDetails(button) {
    const content = button.nextElementSibling;
    const icon = button.querySelector('.toggle-icon');
    const isOpen = content.style.display === 'block';

    content.style.display = isOpen ? 'none' : 'block';
    icon.textContent = isOpen ? '▼' : '▲';

    if (window.sonoEvalTracking && window.sonoEvalTracking.trackEvent) {
        window.sonoEvalTracking.trackEvent('discovery', {
            action: isOpen ? 'collapsed' : 'expanded',
            section: 'how_it_works',
        });
    }
}
```

---

## Task B — Add Step Progress Indicators + Time Estimates

### Before (current)
- `src/sono_eval/mobile/templates/start.html` lines 4–89 show no progress indicator.
- `src/sono_eval/mobile/templates/paths.html` lines 4–79 show no progress indicator.
- `src/sono_eval/mobile/templates/assess.html` (top of main container) has no step indicator.
- `src/sono_eval/mobile/templates/results.html` lines 4–25 show score and meta without a step indicator.

### After (target)
- Add a compact progress row on each step:
  - Step 1/4: “About you” (1 min)
  - Step 2/4: “Pick focus areas” (1–2 min)
  - Step 3/4: “Complete tasks” (10–60 min)
  - Step 4/4: “Review results” (2–5 min)

#### Insert HTML (copy-paste)
**File**: `src/sono_eval/mobile/templates/start.html`  
**Insert** after line 4:

```html
<div class="step-progress">
    <span class="step-pill active">Step 1/4</span>
    <span class="step-label">About you • 1 min</span>
</div>
```

**File**: `src/sono_eval/mobile/templates/paths.html`  
**Insert** after line 4:

```html
<div class="step-progress">
    <span class="step-pill active">Step 2/4</span>
    <span class="step-label">Pick focus areas • 1–2 min</span>
</div>
```

**File**: `src/sono_eval/mobile/templates/assess.html`  
**Insert** near the top of the main container:

```html
<div class="step-progress">
    <span class="step-pill active">Step 3/4</span>
    <span class="step-label">Complete tasks • 10–60 min</span>
</div>
```

**File**: `src/sono_eval/mobile/templates/results.html`  
**Insert** after line 4:

```html
<div class="step-progress">
    <span class="step-pill active">Step 4/4</span>
    <span class="step-label">Review results • 2–5 min</span>
</div>
```

#### CSS additions (copy-paste)
**File**: `src/sono_eval/mobile/static/style.css`

```css
.step-progress {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 16px;
}

.step-pill {
    background: #111827;
    color: #fff;
    font-size: 12px;
    padding: 4px 10px;
    border-radius: 999px;
}

.step-label {
    font-size: 13px;
    color: #6b7280;
}
```

---

## Task C — Quick-Pick Path Selection (“New to coding”)

### Before (current)
- `src/sono_eval/mobile/templates/paths.html` lines 13–68 show tips and recommendations, but no quick-pick CTA.
- `src/sono_eval/mobile/templates/paths.html` lines 117–173 show recommendation logic without auto-select.

### After (target)
- Add a “New to coding” quick-pick button that auto-selects **technical + problem_solving**.

#### Insert CTA (copy-paste)
**File**: `src/sono_eval/mobile/templates/paths.html`  
**Insert** after line 18:

```html
<div class="quick-pick">
    <button type="button" class="secondary-button" onclick="applyQuickPick('new')">
        👶 New to coding? Pick a starter path
    </button>
    <p class="quick-pick-note">We’ll preselect Technical + Problem Solving.</p>
</div>
```

#### Add JS (copy-paste)
**File**: `src/sono_eval/mobile/templates/paths.html`  
**Insert** after line 110:

```javascript
function applyQuickPick(type) {
    const quickPickMap = {
        new: ['technical', 'problem_solving'],
    };

    const picks = quickPickMap[type] || [];
    document.querySelectorAll('.path-checkbox').forEach(checkbox => {
        const pathId = checkbox.closest('.path-card').dataset.path;
        checkbox.checked = picks.includes(pathId);
        checkbox.dispatchEvent(new Event('change'));
    });

    if (window.sonoEvalTracking && window.sonoEvalTracking.trackEvent) {
        window.sonoEvalTracking.trackEvent('paths', {
            action: 'quick_pick',
            type: type,
            selected: picks,
        });
    }
}
```

---

## Task D — Results Page: score → summary → actions → evidence (collapsible)

### Before (current)
- `src/sono_eval/mobile/templates/results.html` lines 6–80 render all sections in a single linear flow (score, summary, charts, findings, strengths, motives, recommendations, actions).

### After (target)
- Reorder to: **Score** → **Summary** → **Actions** → **Evidence** (collapsible sections for scores, findings, strengths, motives, recommendations).

#### Replace HTML (copy-paste)
**File**: `src/sono_eval/mobile/templates/results.html`  
**Replace** lines 27–80 with:

```html
<div class="results-section">
    <h3 class="section-title">📝 Summary</h3>
    <p class="summary-text" id="summary-text"></p>
</div>

<div class="results-actions">
    <button class="secondary-button" onclick="downloadResults()">
        <span>📥</span> Download Report
    </button>
    <button class="primary-button" onclick="startNewAssessment()">
        <span>🔄</span> New Assessment
    </button>
</div>

<div class="results-section">
    <button class="details-toggle" onclick="toggleDetails(this)">
        <span>Evidence & Details</span>
        <span class="toggle-icon">▼</span>
    </button>
    <div class="details-content" style="display: none;">
        <div class="results-section">
            <h3 class="section-title">📊 Path Scores</h3>
            <div class="path-scores-chart" id="path-scores"></div>
        </div>
        <div class="results-section">
            <h3 class="section-title">🔍 Key Findings</h3>
            <ul class="findings-list" id="findings-list"></ul>
        </div>
        <div class="results-section dual-column">
            <div class="column strengths">
                <h4><span class="icon">💪</span> Strengths</h4>
                <ul class="strength-list" id="strengths-list"></ul>
            </div>
            <div class="column improvements">
                <h4><span class="icon">🎯</span> Areas to Improve</h4>
                <ul class="improvement-list" id="improvements-list"></ul>
            </div>
        </div>
        <div class="results-section" id="motives-section" style="display: none;">
            <h3 class="section-title">🧠 Your Micro-Motives</h3>
            <p class="motives-intro">These reveal what drives your approach:</p>
            <div class="motives-chart" id="motives-chart"></div>
        </div>
        <div class="results-section">
            <h3 class="section-title">💡 Recommendations</h3>
            <div class="recommendations-list" id="recommendations-list"></div>
        </div>
    </div>
</div>
```

---

## Testing Instructions

1. Run the server: `./launcher.sh start`.
2. Open `/mobile` and confirm:
   - Welcome page shows 4-value grid and a single CTA.
   - Step indicators appear on start/paths/assess/results.
   - “New to coding” quick-pick selects two paths and updates the time estimate.
   - Results page shows score + summary + actions, with evidence collapsed by default.

---

## Success Criteria

- ✅ Welcome screen presents 4-value grid, no expandable cards.
- ✅ Each step shows progress indicator with time estimate.
- ✅ Quick-pick auto-selects 2 paths and updates the selection summary.
- ✅ Results page is reordered with collapsible evidence.

---

## Rollback Procedure

1. Revert the changes in templates and CSS to the previous commit.
2. Ensure `index.html` reverts to discovery cards + expandable process section.
3. Remove `toggleDetails` from results template if added.
