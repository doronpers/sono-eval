# Implementation Plan: Mobile Onboarding & Progressive Disclosure UX

**Area**: Mobile Companion Interface Enhancement  
**Priority**: HIGH  
**Impact**: HIGH  
**Effort**: MEDIUM  
**Estimated Time**: 4-6 hours  
**Agent Type**: General-purpose or UI/UX specialist

---

## Overview

This plan provides step-by-step instructions for coding agents to enhance the mobile onboarding experience in Sono-Eval. The goal is to reduce cognitive load, improve information hierarchy, and increase assessment completion rates through better progressive disclosure and guided flows.

---

## Prerequisites

**Before starting, the agent must:**

1. Read the existing mobile interface code:
   - `src/sono_eval/mobile/templates/index.html` (welcome screen)
   - `src/sono_eval/mobile/templates/start.html` (candidate entry)
   - `src/sono_eval/mobile/templates/paths.html` (path selection)
   - `src/sono_eval/mobile/static/style.css` (styling)
   - `src/sono_eval/mobile/static/script.js` (interactions)

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

```html
<div class="hero-section">
    <div class="hero-icon">🎯</div>
    <h2 class="hero-title">Welcome to Sono-Eval</h2>
    <p class="hero-subtitle">Understand your strengths and get actionable feedback</p>
</div>

<div class="value-proposition">
    <div class="value-grid">
        <div class="value-item">
            <span class="value-icon">💡</span>
            <h4>Explained Scores</h4>
            <p>See exactly why you received each score with clear evidence</p>
        </div>
        <div class="value-item">
            <span class="value-icon">🎯</span>
            <h4>Choose Your Focus</h4>
            <p>Pick 1-4 areas that matter most to you</p>
        </div>
        <div class="value-item">
            <span class="value-icon">📈</span>
            <h4>Grow Skills</h4>
            <p>Get specific recommendations you can use immediately</p>
        </div>
        <div class="value-item">
            <span class="value-icon">⏱️</span>
            <h4>Your Pace</h4>
            <p>10-90 minutes depending on areas selected</p>
        </div>
    </div>
</div>
```

#### 1.2: Move Secondary Information to Collapsible Section

Move time commitment and privacy info into a **single** collapsible "Learn More" section **after** the CTA:

```html
<div class="cta-section">
    <button class="primary-button" onclick="location.href='/mobile/start'">
        Start Your Assessment
        <span class="button-arrow">→</span>
    </button>
    <p class="cta-subtext">No account needed • 10-90 minutes</p>
</div>

<div class="info-details">
    <button class="details-toggle" onclick="toggleDetails(this)">
        <span>How does this work?</span>
        <span class="toggle-icon">▼</span>
    </button>
    <div class="details-content" style="display: none;">
        <div class="detail-section">
            <h4>⏱️ Time Commitment</h4>
            <ul>
                <li><strong>1 area:</strong> 10-20 minutes</li>
                <li><strong>2-3 areas:</strong> 30-60 minutes</li>
                <li><strong>All areas:</strong> 60-90 minutes</li>
            </ul>
            <p class="detail-note">You can save progress and return later</p>
        </div>

        <div class="detail-section">
            <h4>🔒 Privacy</h4>
            <ul>
                <li>✅ No account required to try</li>
                <li>✅ Your code stays private</li>
                <li>✅ Full transparency on scoring</li>
            </ul>
        </div>

        <div class="detail-section">
            <h4>📋 The Process</h4>
            <ol>
                <li>Choose 1-4 skill areas</li>
                <li>Complete interactive tasks</li>
                <li>Get detailed, explained feedback</li>
                <li>Receive growth recommendations</li>
            </ol>
        </div>
    </div>
</div>
```

#### 1.3: Update JavaScript for New Toggle

**Add after line 189:**

```javascript
function toggleDetails(button) {
    const content = button.nextElementSibling;
    const icon = button.querySelector('.toggle-icon');

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
    if (window.sonoEvalTracking && window.sonoEvalTracking.trackEvent) {
        window.sonoEvalTracking.trackEvent('path_selection', {
            method: 'quick_pick',
            type: pathType,
            paths: paths
        });
    }

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

---

## Task 4: Enhance Results Page Hierarchy

**File**: `src/sono_eval/mobile/templates/results.html`

### Current Issues

- Flat information hierarchy
- Scores not prominent enough
- Recommendations buried in evidence

### Changes Required

#### 4.1: Add Results Summary Section

**At the top of results**, add a summary card:

```html
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
</div>
```

#### 4.2: Restructure Path Results

Organize each path result with clear sections:

```html
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
</div>
```

#### 4.3: Add Action Items Section

At the bottom, add clear next steps:

```html
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

---

## Task 5: Add CSS for New Components

**File**: `src/sono_eval/mobile/static/style.css`

### Add the following styles (append to file)

```css
/* Value Proposition Grid */
.value-proposition {
    margin: 2rem 0;
    padding: 0 1rem;
}

.value-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}

.value-item {
    background: var(--bg-white);
    padding: 1rem;
    border-radius: var(--radius);
    border: 1px solid var(--border-color);
    text-align: center;
}

.value-icon {
    font-size: 2rem;
    display: block;
    margin-bottom: 0.5rem;
}

.value-item h4 {
    font-size: var(--text-base);
    margin-bottom: 0.25rem;
    color: var(--text-primary);
}

.value-item p {
    font-size: var(--text-sm);
    color: var(--text-secondary);
    margin: 0;
}

/* Info Details Section */
.info-details {
    margin: 2rem 1rem;
    background: var(--bg-white);
    border-radius: var(--radius-lg);
    overflow: hidden;
}

.details-toggle {
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
    color: var(--primary-color);
}

.details-toggle:hover {
    background: var(--bg-light);
}

.details-content {
    padding: 0 1rem 1rem 1rem;
}

.detail-section {
    margin-bottom: 1.5rem;
}

.detail-section:last-child {
    margin-bottom: 0;
}

.detail-section h4 {
    font-size: var(--text-base);
    margin-bottom: 0.5rem;
    color: var(--text-primary);
}

.detail-section ul {
    list-style: none;
    padding: 0;
    margin: 0.5rem 0;
}

.detail-section ul li {
    padding: 0.25rem 0;
    font-size: var(--text-sm);
    color: var(--text-secondary);
}

.detail-section ol {
    padding-left: 1.5rem;
    margin: 0.5rem 0;
}

.detail-section ol li {
    padding: 0.25rem 0;
    font-size: var(--text-sm);
    color: var(--text-secondary);
}

.detail-note {
    font-size: var(--text-xs);
    color: var(--text-muted);
    font-style: italic;
    margin-top: 0.5rem;
}

/* Guidance Section */
.guidance-section {
    padding: 1rem;
    margin-bottom: 1.5rem;
}

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
    }
}
```

---

## Task 6: Update Mobile App Routes

**File**: `src/sono_eval/mobile/app.py`

### Ensure route handlers pass new context variables

Update the results route to include summary data:

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

def get_score_context(score: float) -> str:
    """Get contextual message for score."""
    if score >= 85:
        return "Excellent work! Strong performance across areas."
    elif score >= 70:
        return "Good job! Solid foundation with room to grow."
    elif score >= 55:
        return "Making progress! Focus on key improvements."
    else:
        return "Keep going! Every expert was once a beginner."

def calculate_top_strength(result: AssessmentResult) -> str:
    """Extract the single best strength."""
    # Implementation: Find highest scoring metric
    pass

def calculate_top_improvement(result: AssessmentResult) -> str:
    """Extract the single most impactful improvement."""
    # Implementation: Find lowest scoring metric or highest-impact improvement
    pass
```

---

## Testing Instructions

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

---

## Success Criteria

**Before marking as complete, verify:**

- [ ] Welcome screen has single clear CTA
- [ ] Information hierarchy follows: Action → Value → Details
- [ ] Progress indicators show at all steps with time estimates
- [ ] Path selection has quick-pick options
- [ ] Results page shows score → summary → actions → details
- [ ] All collapsible sections work smoothly
- [ ] Mobile responsive (tested on 3+ viewport sizes)
- [ ] No console errors
- [ ] Analytics events fire correctly
- [ ] Performance meets targets (page loads < 1s)

---

## Follow-Up Enhancements (Future)

After core implementation:

1. **A/B Testing**: Compare old vs new welcome screen completion rates
2. **Heatmaps**: Track where users click most
3. **Time Tracking**: Measure time spent per section
4. **Accessibility**: Add ARIA labels and keyboard navigation
5. **Animations**: Add subtle transitions for better polish
6. **Offline Support**: Add service worker for offline functionality

---

**Document Version**: 1.0  
**Last Updated**: January 17, 2026  
**Estimated Implementation Time**: 4-6 hours  
**Difficulty**: Medium
