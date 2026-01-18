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

<<<<<<< HEAD:Documentation/Archive/Reports-Historical/IMPLEMENTATION_PLAN_1_MOBILE_UX.md
2. Understand the current user flow:

   ```
   /mobile → index.html → start.html → paths.html → assess.html → results.html
   ```

3. Review the mobile configuration:
   - `src/sono_eval/mobile/mobile_config.yaml`
   - `src/sono_eval/mobile/app.py` (FastAPI routes)

4. Test the current mobile interface:

   ```bash
   ./launcher.sh start
   # Open http://localhost:8000/mobile in browser
   # Or use mobile device emulation in browser DevTools
   ```

---

## Task 1: Simplify Welcome Screen (index.html)

**File**: `src/sono_eval/mobile/templates/index.html`

### Current Issues

- 3 discovery cards + expandable section = too many decisions
- No clear visual priority or reading order
- Equal weight to all information (value prop, time, privacy)

### Changes Required

#### 1.1: Reduce Discovery Cards from 3 to 1 Primary Card

**Replace lines 11-100** with a single prominent value proposition:
=======
#### Replace HTML (copy-paste)
**File**: `src/sono_eval/mobile/templates/index.html`  
**Replace** lines 11–134 with:
>>>>>>> 6b7113d6352e4fb7d7504d7a7d221ee1ac543c33:Documentation/Reports/IMPLEMENTATION_PLAN_1_MOBILE_UX.md

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
<<<<<<< HEAD:Documentation/Archive/Reports-Historical/IMPLEMENTATION_PLAN_1_MOBILE_UX.md

=======
>>>>>>> 6b7113d6352e4fb7d7504d7a7d221ee1ac543c33:Documentation/Reports/IMPLEMENTATION_PLAN_1_MOBILE_UX.md
        <div class="detail-section">
            <h4>🔒 Privacy</h4>
            <ul>
                <li>✅ No account required</li>
                <li>✅ Your code stays private</li>
                <li>✅ Transparent scoring</li>
            </ul>
        </div>
<<<<<<< HEAD:Documentation/Archive/Reports-Historical/IMPLEMENTATION_PLAN_1_MOBILE_UX.md

        <div class="detail-section">
            <h4>📋 The Process</h4>
            <ol>
                <li>Choose 1-4 skill areas</li>
                <li>Complete interactive tasks</li>
                <li>Get detailed, explained feedback</li>
                <li>Receive growth recommendations</li>
            </ol>
        </div>
=======
>>>>>>> 6b7113d6352e4fb7d7504d7a7d221ee1ac543c33:Documentation/Reports/IMPLEMENTATION_PLAN_1_MOBILE_UX.md
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
<<<<<<< HEAD:Documentation/Archive/Reports-Historical/IMPLEMENTATION_PLAN_1_MOBILE_UX.md

    if (content.style.display === 'none') {
        content.style.display = 'block';
        icon.textContent = '▲';

        // Track interaction
        if (window.sonoEvalTracking && window.sonoEvalTracking.trackEvent) {
            window.sonoEvalTracking.trackEvent('engagement', {
                action: 'expanded_details',
                page: 'welcome'
            });
        }
    } else {
        content.style.display = 'none';
        icon.textContent = '▼';
    }
}
```

### Expected Outcome

- Single clear path forward (CTA button prominent)
- Reduced cognitive load (4 value items vs 3 expandable cards + section)
- Secondary info available but not blocking action

---

## Task 2: Add Step Progress Indicators

**Files**:

- `src/sono_eval/mobile/templates/base.html`
- `src/sono_eval/mobile/static/style.css`

### Current Issues

- Progress bar exists but lacks context
- Users don't know "step X of Y"
- No time estimates per step

### Changes Required

#### 2.1: Enhance Progress Bar Component

**In `base.html`**, replace the progress-bar div with:

```html
<div class="progress-container">
    <div class="progress-info">
        <span class="progress-label">{% block progress_label %}Getting Started{% endblock %}</span>
        <span class="progress-step">{% block progress_step %}{% endblock %}</span>
    </div>
    <div class="progress-bar">
        <div class="progress-fill" style="width: {% block progress_width %}0{% endblock %}%;"></div>
    </div>
    <div class="progress-time">
        <span class="time-estimate">{% block time_estimate %}{% endblock %}</span>
    </div>
</div>
```

#### 2.2: Update Each Template with Progress Info

**In `start.html`**, add:

```html
{% block progress_label %}Step 1: Enter ID{% endblock %}
{% block progress_step %}1/4{% endblock %}
{% block progress_width %}25{% endblock %}
{% block time_estimate %}< 1 min{% endblock %}
```

**In `paths.html`**, add:

```html
{% block progress_label %}Step 2: Choose Areas{% endblock %}
{% block progress_step %}2/4{% endblock %}
{% block progress_width %}50{% endblock %}
{% block time_estimate %}1-2 min{% endblock %}
```

**In `assess.html`**, add:

```html
{% block progress_label %}Step 3: Assessment{% endblock %}
{% block progress_step %}3/4{% endblock %}
{% block progress_width %}75{% endblock %}
{% block time_estimate %}{{ estimated_time }} min remaining{% endblock %}
```

**In `results.html`**, add:

```html
{% block progress_label %}Complete!{% endblock %}
{% block progress_step %}4/4{% endblock %}
{% block progress_width %}100{% endblock %}
```

#### 2.3: Add Progress Styles

**In `style.css`**, add after line 99:

```css
/* Enhanced Progress Container */
.progress-container {
    background: var(--bg-white);
    padding: 0.75rem 1rem;
    border-bottom: 1px solid var(--border-color);
}

.progress-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
}

.progress-label {
    font-size: var(--text-sm);
    font-weight: 600;
    color: var(--text-primary);
}

.progress-step {
    font-size: var(--text-sm);
    color: var(--text-secondary);
    font-weight: 500;
}

.progress-time {
    margin-top: 0.25rem;
    text-align: right;
}

.time-estimate {
    font-size: var(--text-xs);
    color: var(--text-muted);
    font-style: italic;
}
```

### Expected Outcome

- Clear context: "Step 2 of 4"
- Time awareness: "1-2 min" estimates
- Visual progress: More informative progress bar

---

## Task 3: Improve Path Selection with Guidance

**File**: `src/sono_eval/mobile/templates/paths.html`

### Current Issues

- All 5 paths shown with equal weight
- No guidance on which to choose
- No indication of difficulty or time per path

### Changes Required

#### 3.1: Add Path Selection Guidance

**Before the path cards**, add:

```html
<div class="guidance-section">
    <h3>Choose Your Focus Areas</h3>
    <p class="guidance-text">
        Select 1-4 areas based on your goals. Not sure? Start with
        <strong>Technical</strong> for a quick assessment.
    </p>

    <div class="quick-picks">
        <button class="quick-pick-btn" onclick="selectQuickPath('beginner')">
            <span class="pick-icon">🌱</span>
            <span class="pick-label">New to coding</span>
            <span class="pick-desc">Technical + Problem Solving</span>
        </button>

        <button class="quick-pick-btn" onclick="selectQuickPath('comprehensive')">
            <span class="pick-icon">🎯</span>
            <span class="pick-label">Complete profile</span>
            <span class="pick-desc">All 4 areas (60-90 min)</span>
        </button>
    </div>

    <p class="or-divider">or choose specific areas below</p>
</div>
```

#### 3.2: Enhance Path Cards with Metadata

For each path card, add time estimate and difficulty:

```html
<div class="path-card" data-path="technical">
    <div class="path-header">
        <span class="path-icon">⚙️</span>
        <h4>Technical Skills</h4>
        <span class="path-badge">15-20 min</span>
    </div>
    <p class="path-description">
        Code quality, architecture, and technical implementation
    </p>
    <div class="path-details">
        <span class="detail-item">🎯 Core assessment</span>
        <span class="detail-item">✨ Great for beginners</span>
    </div>
    <button class="path-select-btn">Select</button>
</div>
```

#### 3.3: Add Quick Path Selection Logic

**In the script section**, add:

```javascript
function selectQuickPath(pathType) {
    // Clear any existing selections
    document.querySelectorAll('.path-card').forEach(card => {
        card.classList.remove('selected');
    });

    const pathMap = {
        'beginner': ['technical', 'problem_solving'],
        'comprehensive': ['technical', 'design', 'collaboration', 'problem_solving']
    };

    const paths = pathMap[pathType];
    paths.forEach(pathId => {
        const card = document.querySelector(`[data-path="${pathId}"]`);
        if (card) {
            card.classList.add('selected');
            card.querySelector('.path-select-btn').textContent = 'Selected ✓';
        }
    });

    // Show continue button
    document.querySelector('.continue-btn').style.display = 'block';

    // Track selection
=======
    const isOpen = content.style.display === 'block';

    content.style.display = isOpen ? 'none' : 'block';
    icon.textContent = isOpen ? '▼' : '▲';

>>>>>>> 6b7113d6352e4fb7d7504d7a7d221ee1ac543c33:Documentation/Reports/IMPLEMENTATION_PLAN_1_MOBILE_UX.md
    if (window.sonoEvalTracking && window.sonoEvalTracking.trackEvent) {
        window.sonoEvalTracking.trackEvent('discovery', {
            action: isOpen ? 'collapsed' : 'expanded',
            section: 'how_it_works',
        });
    }
<<<<<<< HEAD:Documentation/Archive/Reports-Historical/IMPLEMENTATION_PLAN_1_MOBILE_UX.md

    // Scroll to continue button
    document.querySelector('.continue-btn').scrollIntoView({
        behavior: 'smooth',
        block: 'center'
    });
}
```

### Expected Outcome

- Reduced decision paralysis with quick-pick options
- Better informed choices with time estimates
- Guided experience for new users

=======
}
```

>>>>>>> 6b7113d6352e4fb7d7504d7a7d221ee1ac543c33:Documentation/Reports/IMPLEMENTATION_PLAN_1_MOBILE_UX.md
---

## Task B — Add Step Progress Indicators + Time Estimates

### Before (current)
- `src/sono_eval/mobile/templates/start.html` lines 4–89 show no progress indicator.
- `src/sono_eval/mobile/templates/paths.html` lines 4–79 show no progress indicator.
- `src/sono_eval/mobile/templates/assess.html` (top of main container) has no step indicator.
- `src/sono_eval/mobile/templates/results.html` lines 4–25 show score and meta without a step indicator.

<<<<<<< HEAD:Documentation/Archive/Reports-Historical/IMPLEMENTATION_PLAN_1_MOBILE_UX.md
### Current Issues

- Flat information hierarchy
- Scores not prominent enough
- Recommendations buried in evidence
=======
### After (target)
- Add a compact progress row on each step:
  - Step 1/4: “About you” (1 min)
  - Step 2/4: “Pick focus areas” (1–2 min)
  - Step 3/4: “Complete tasks” (10–60 min)
  - Step 4/4: “Review results” (2–5 min)
>>>>>>> 6b7113d6352e4fb7d7504d7a7d221ee1ac543c33:Documentation/Reports/IMPLEMENTATION_PLAN_1_MOBILE_UX.md

#### Insert HTML (copy-paste)
**File**: `src/sono_eval/mobile/templates/start.html`  
**Insert** after line 4:

```html
<<<<<<< HEAD:Documentation/Archive/Reports-Historical/IMPLEMENTATION_PLAN_1_MOBILE_UX.md
<div class="results-summary">
    <div class="score-hero">
        <div class="score-display">
            <span class="score-number">{{ overall_score }}</span>
            <span class="score-label">/100</span>
        </div>
        <p class="score-context">{{ score_context }}</p>
    </div>

    <div class="key-highlights">
        <div class="highlight-item positive">
            <span class="highlight-icon">✨</span>
            <div>
                <h5>Top Strength</h5>
                <p>{{ top_strength }}</p>
            </div>
        </div>

        <div class="highlight-item improvement">
            <span class="highlight-icon">📈</span>
            <div>
                <h5>Growth Opportunity</h5>
                <p>{{ top_improvement }}</p>
            </div>
        </div>
    </div>
=======
<div class="step-progress">
    <span class="step-pill active">Step 1/4</span>
    <span class="step-label">About you • 1 min</span>
>>>>>>> 6b7113d6352e4fb7d7504d7a7d221ee1ac543c33:Documentation/Reports/IMPLEMENTATION_PLAN_1_MOBILE_UX.md
</div>
```

**File**: `src/sono_eval/mobile/templates/paths.html`  
**Insert** after line 4:

```html
<<<<<<< HEAD:Documentation/Archive/Reports-Historical/IMPLEMENTATION_PLAN_1_MOBILE_UX.md
<div class="path-result" data-path="{{ path.name }}">
    <!-- Score at top -->
    <div class="path-score-header">
        <h3>{{ path.display_name }}</h3>
        <span class="path-score">{{ path.score }}/100</span>
    </div>

    <!-- Executive summary -->
    <div class="path-summary">
        <p class="summary-text">{{ path.summary }}</p>
    </div>

    <!-- Strengths (collapsible) -->
    <div class="collapsible-section">
        <button class="section-toggle" onclick="toggleSection(this)">
            <span>✨ Your Strengths ({{ path.strengths|length }})</span>
            <span class="toggle-icon">▼</span>
        </button>
        <div class="section-content">
            <ul class="strengths-list">
                {% for strength in path.strengths %}
                <li>{{ strength }}</li>
                {% endfor %}
            </ul>
        </div>
    </div>

    <!-- Areas for improvement (expanded by default) -->
    <div class="collapsible-section expanded">
        <button class="section-toggle" onclick="toggleSection(this)">
            <span>📈 Growth Opportunities ({{ path.improvements|length }})</span>
            <span class="toggle-icon">▲</span>
        </button>
        <div class="section-content" style="display: block;">
            <ul class="improvements-list">
                {% for improvement in path.improvements %}
                <li>
                    <strong>{{ improvement.title }}</strong>
                    <p>{{ improvement.description }}</p>
                    {% if improvement.resources %}
                    <div class="improvement-resources">
                        {% for resource in improvement.resources %}
                        <a href="{{ resource.url }}" class="resource-link">
                            {{ resource.title }}
                        </a>
                        {% endfor %}
                    </div>
                    {% endif %}
                </li>
                {% endfor %}
            </ul>
        </div>
    </div>

    <!-- Evidence (collapsible, closed by default) -->
    <div class="collapsible-section">
        <button class="section-toggle" onclick="toggleSection(this)">
            <span>🔍 Supporting Evidence ({{ path.evidence|length }})</span>
            <span class="toggle-icon">▼</span>
        </button>
        <div class="section-content">
            <!-- Evidence items -->
        </div>
    </div>
=======
<div class="step-progress">
    <span class="step-pill active">Step 2/4</span>
    <span class="step-label">Pick focus areas • 1–2 min</span>
>>>>>>> 6b7113d6352e4fb7d7504d7a7d221ee1ac543c33:Documentation/Reports/IMPLEMENTATION_PLAN_1_MOBILE_UX.md
</div>
```

**File**: `src/sono_eval/mobile/templates/assess.html`  
**Insert** near the top of the main container:

```html
<<<<<<< HEAD:Documentation/Archive/Reports-Historical/IMPLEMENTATION_PLAN_1_MOBILE_UX.md
<div class="next-steps">
    <h3>What's Next?</h3>
    <div class="action-cards">
        <div class="action-card">
            <span class="action-icon">💾</span>
            <h4>Save Your Results</h4>
            <p>Download a detailed PDF report</p>
            <button class="action-btn">Download PDF</button>
        </div>

        <div class="action-card">
            <span class="action-icon">🔄</span>
            <h4>Try Another Path</h4>
            <p>Explore other skill areas</p>
            <button class="action-btn" onclick="location.href='/mobile/paths'">
                Select Paths
            </button>
        </div>

        <div class="action-card">
            <span class="action-icon">📚</span>
            <h4>Learn More</h4>
            <p>Resources to improve your skills</p>
            <button class="action-btn" onclick="location.href='/docs'">
                View Resources
            </button>
        </div>
    </div>
</div>
```

### Expected Outcome

- Clear visual hierarchy: Score → Summary → Actions → Details
- Actionable focus: Improvements prominent, evidence secondary
- Better engagement: Clear next steps
=======
<div class="step-progress">
    <span class="step-pill active">Step 3/4</span>
    <span class="step-label">Complete tasks • 10–60 min</span>
</div>
```

**File**: `src/sono_eval/mobile/templates/results.html`  
**Insert** after line 4:
>>>>>>> 6b7113d6352e4fb7d7504d7a7d221ee1ac543c33:Documentation/Reports/IMPLEMENTATION_PLAN_1_MOBILE_UX.md

```html
<div class="step-progress">
    <span class="step-pill active">Step 4/4</span>
    <span class="step-label">Review results • 2–5 min</span>
</div>
```

#### CSS additions (copy-paste)
**File**: `src/sono_eval/mobile/static/style.css`

<<<<<<< HEAD:Documentation/Archive/Reports-Historical/IMPLEMENTATION_PLAN_1_MOBILE_UX.md
### Add the following styles (append to file)

=======
>>>>>>> 6b7113d6352e4fb7d7504d7a7d221ee1ac543c33:Documentation/Reports/IMPLEMENTATION_PLAN_1_MOBILE_UX.md
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

<<<<<<< HEAD:Documentation/Archive/Reports-Historical/IMPLEMENTATION_PLAN_1_MOBILE_UX.md
.guidance-section h3 {
    font-size: var(--text-xl);
    margin-bottom: 0.5rem;
    color: var(--text-primary);
}

.guidance-text {
    font-size: var(--text-base);
    color: var(--text-secondary);
    margin-bottom: 1rem;
    line-height: 1.5;
}

.quick-picks {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin: 1rem 0;
}

.quick-pick-btn {
    background: var(--bg-white);
    border: 2px solid var(--border-color);
    border-radius: var(--radius);
    padding: 1rem;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: left;
}

.quick-pick-btn:hover {
    border-color: var(--primary-color);
    background: var(--bg-light);
}

.pick-icon {
    font-size: 1.5rem;
    margin-right: 0.75rem;
}

.pick-label {
    display: block;
    font-weight: 600;
    font-size: var(--text-base);
    color: var(--text-primary);
    margin-bottom: 0.25rem;
}

.pick-desc {
    display: block;
    font-size: var(--text-sm);
    color: var(--text-secondary);
}

.or-divider {
    text-align: center;
    font-size: var(--text-sm);
    color: var(--text-muted);
    margin: 1.5rem 0 1rem 0;
    position: relative;
}

.or-divider::before,
.or-divider::after {
    content: '';
    position: absolute;
    top: 50%;
    width: 40%;
    height: 1px;
    background: var(--border-color);
}

.or-divider::before {
    left: 0;
}

.or-divider::after {
    right: 0;
}

/* Path Card Enhancements */
.path-badge {
    font-size: var(--text-xs);
    padding: 0.25rem 0.5rem;
    background: var(--bg-light);
    border-radius: var(--radius);
    color: var(--text-secondary);
    font-weight: 500;
}

.path-details {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    margin: 0.75rem 0;
}

.detail-item {
    font-size: var(--text-sm);
    color: var(--text-secondary);
}

/* Results Summary */
.results-summary {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
    color: white;
    padding: 2rem 1rem;
    margin-bottom: 1.5rem;
    border-radius: var(--radius-lg);
}

.score-hero {
    text-align: center;
    margin-bottom: 1.5rem;
}

.score-display {
    margin-bottom: 0.5rem;
}

.score-number {
    font-size: 4rem;
    font-weight: 700;
    line-height: 1;
}

.score-label {
    font-size: 1.5rem;
    color: rgba(255, 255, 255, 0.8);
}

.score-context {
    font-size: var(--text-base);
    color: rgba(255, 255, 255, 0.9);
}

.key-highlights {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.highlight-item {
    background: rgba(255, 255, 255, 0.1);
    padding: 1rem;
    border-radius: var(--radius);
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
}

.highlight-icon {
    font-size: 1.5rem;
}

.highlight-item h5 {
    margin: 0 0 0.25rem 0;
    font-size: var(--text-base);
    font-weight: 600;
}

.highlight-item p {
    margin: 0;
    font-size: var(--text-sm);
    color: rgba(255, 255, 255, 0.9);
}

/* Collapsible Sections */
.collapsible-section {
    margin-bottom: 1rem;
    background: var(--bg-white);
    border-radius: var(--radius);
    overflow: hidden;
}

.section-toggle {
    width: 100%;
    padding: 1rem;
    background: transparent;
    border: none;
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    font-size: var(--text-base);
    font-weight: 600;
    text-align: left;
}

.section-toggle:hover {
    background: var(--bg-light);
}

.section-content {
    padding: 0 1rem 1rem 1rem;
    display: none;
}

.collapsible-section.expanded .section-content {
    display: block;
}

.collapsible-section.expanded .toggle-icon {
    transform: rotate(180deg);
}

/* Next Steps Actions */
.next-steps {
    margin: 2rem 1rem;
}

.next-steps h3 {
    font-size: var(--text-xl);
    margin-bottom: 1rem;
    text-align: center;
}

.action-cards {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.action-card {
    background: var(--bg-white);
    padding: 1.5rem;
    border-radius: var(--radius-lg);
    border: 1px solid var(--border-color);
    text-align: center;
}

.action-icon {
    font-size: 2.5rem;
    display: block;
    margin-bottom: 0.75rem;
}

.action-card h4 {
    font-size: var(--text-lg);
    margin-bottom: 0.5rem;
    color: var(--text-primary);
}

.action-card p {
    font-size: var(--text-sm);
    color: var(--text-secondary);
    margin-bottom: 1rem;
}

.action-btn {
    background: var(--primary-color);
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: var(--radius);
    font-size: var(--text-base);
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s ease;
}

.action-btn:hover {
    background: var(--primary-dark);
}

/* Responsive adjustments */
@media (min-width: 640px) {
    .value-grid {
        grid-template-columns: repeat(4, 1fr);
    }

    .quick-picks {
        flex-direction: row;
    }

    .action-cards {
        flex-direction: row;
=======
    if (window.sonoEvalTracking && window.sonoEvalTracking.trackEvent) {
        window.sonoEvalTracking.trackEvent('paths', {
            action: 'quick_pick',
            type: type,
            selected: picks,
        });
>>>>>>> 6b7113d6352e4fb7d7504d7a7d221ee1ac543c33:Documentation/Reports/IMPLEMENTATION_PLAN_1_MOBILE_UX.md
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

<<<<<<< HEAD:Documentation/Archive/Reports-Historical/IMPLEMENTATION_PLAN_1_MOBILE_UX.md
```python
@app.get("/results", response_class=HTMLResponse)
async def results_page(request: Request, session_id: Optional[str] = None):
    """Display assessment results with enhanced summary."""
    # ... existing code ...

    # Calculate top strength and improvement
    top_strength = calculate_top_strength(assessment_result)
    top_improvement = calculate_top_improvement(assessment_result)
    score_context = get_score_context(assessment_result.overall_score)

    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "result": assessment_result,
            "overall_score": assessment_result.overall_score,
            "top_strength": top_strength,
            "top_improvement": top_improvement,
            "score_context": score_context,
            # ... other context ...
        }
    )
=======
```html
<div class="results-section">
    <h3 class="section-title">📝 Summary</h3>
    <p class="summary-text" id="summary-text"></p>
</div>
>>>>>>> 6b7113d6352e4fb7d7504d7a7d221ee1ac543c33:Documentation/Reports/IMPLEMENTATION_PLAN_1_MOBILE_UX.md

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

<<<<<<< HEAD:Documentation/Archive/Reports-Historical/IMPLEMENTATION_PLAN_1_MOBILE_UX.md
After implementing all changes, test thoroughly:

### 1. Visual Testing

```bash
./launcher.sh start
# Open http://localhost:8000/mobile
# Test on desktop and mobile viewports
```

**Check:**

- Welcome screen has 4 value items in grid
- CTA button is prominent
- Details section collapses/expands smoothly
- Quick-pick buttons work correctly
- Progress indicators show at each step
- Results page hierarchy is clear

### 2. Interaction Testing

**User Flow:**

1. Land on welcome → Click "Start Your Assessment"
2. Enter candidate ID → See progress "Step 1/4"
3. Click quick-pick "New to coding" → See 2 paths selected
4. Complete assessment → See score hero and highlights first
5. Expand/collapse evidence sections → Verify smooth animation

### 3. Mobile Device Testing

Test on actual mobile devices or use browser DevTools:

- iPhone SE (375px)
- iPhone 12 Pro (390px)
- iPad (768px)
- Android phones (various)

**Verify:**

- Touch targets are at least 44x44px
- Text is readable without zooming
- Buttons are accessible
- No horizontal scrolling

### 4. Analytics Verification

Check that tracking events fire:

- Welcome page discovery interactions
- Quick-pick selections
- Section toggles on results page

### 5. Performance Testing

```bash
# Test page load times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/mobile
```

**Targets:**

- Welcome page: < 500ms
- Path selection: < 300ms
- Results rendering: < 800ms

---

## Rollback Plan

If issues arise:

1. **Code Backup**: Before starting, create a branch:

   ```bash
   git checkout -b mobile-ux-enhancement
   ```

2. **Incremental Commits**: Commit after each task:

   ```bash
   git add src/sono_eval/mobile/templates/index.html
   git commit -m "Task 1: Simplify welcome screen"
   ```

3. **Quick Rollback**: If a task causes issues:

   ```bash
   git checkout HEAD~1 -- src/sono_eval/mobile/templates/index.html
   ```
=======
1. Run the server: `./launcher.sh start`.
2. Open `/mobile` and confirm:
   - Welcome page shows 4-value grid and a single CTA.
   - Step indicators appear on start/paths/assess/results.
   - “New to coding” quick-pick selects two paths and updates the time estimate.
   - Results page shows score + summary + actions, with evidence collapsed by default.
>>>>>>> 6b7113d6352e4fb7d7504d7a7d221ee1ac543c33:Documentation/Reports/IMPLEMENTATION_PLAN_1_MOBILE_UX.md

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
