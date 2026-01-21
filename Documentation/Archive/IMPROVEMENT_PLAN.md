# Sono-Eval: Improvement Plan & Coding Agent Instructions

## Executive Summary

After a comprehensive review of the Sono-Eval repository (documentation, architecture, and code), I've identified **three areas** that would benefit most from further revision and UX enhancement. This document provides detailed instructional prompts for coding agents to successfully execute these improvements.

---

## Review Findings

### What Sono-Eval Does Well

1. **Solid Core Architecture**: The assessment engine with HeuristicScorer, MLScorer, and MicroMotiveScorer is well-designed and modular
2. **Comprehensive Data Models**: Pydantic models are well-structured with proper validation
3. **Security-First Approach**: Input validation, path traversal protection, and secret key validation are implemented
4. **Documentation Organization**: The Documentation/ directory follows good organizational standards
5. **Multi-Interface Design**: CLI, REST API, and Mobile interfaces provide flexibility

### Gaps Identified

1. **Mobile Experience Implementation Gap**: Documentation promises an interactive, discovery-based experience but the implementation is skeletal
2. **Results Visualization**: Assessment results are data-rich but visualization is underdeveloped
3. **CLI UX for New Users**: Commands work but lack progressive feedback and guided workflows

---

## Area 1: Mobile Companion Experience & Onboarding Flow

### Problem Statement

The documentation (particularly `candidate-guide.md`) promises a rich, interactive onboarding experience with:
- Progressive disclosure ("discovery cards")
- Interactive setup wizard
- "Why we ask this" explanations
- Guided mode for first-time users
- Mini-quizzes for self-reflection
- Easter eggs and hidden features

However, the current implementation in `/src/sono_eval/mobile/` consists of:
- Basic template stubs with minimal interactivity
- Static page templates without JavaScript-driven UX
- Missing progressive disclosure patterns
- No "delight" moments or discovery features

### Impact

This gap directly affects the candidate experience - the primary user persona. The documentation creates expectations the product doesn't fulfill, leading to user disappointment and confusion.

### Detailed Implementation Instructions for Coding Agents

```
## TASK: Enhance Mobile Companion Experience & Onboarding Flow

### Context
You are working on Sono-Eval, an explainable developer assessment system. The mobile
companion interface needs enhancement to match the documented UX vision.

### Files to Modify/Create
- src/sono_eval/mobile/templates/*.html (existing templates)
- src/sono_eval/mobile/static/css/mobile.css (create/enhance)
- src/sono_eval/mobile/static/js/mobile.js (create/enhance)
- src/sono_eval/mobile/mobile_config.yaml (enhance)
- src/sono_eval/mobile/app.py (add API endpoints)

### Requirements

#### 1. Welcome Page Enhancement (`templates/index.html`)

Implement the following features matching documentation promises:

a) **Progressive Disclosure System**
   - Create expandable "discovery cards" that explain what makes Sono-Eval different
   - Each card should have: title, icon, collapsed preview, expanded content
   - Cards: "Not a Pass/Fail Test", "Multi-Path Assessment", "Evidence-Based Feedback",
     "Micro-Motives (What Drives You)"
   - Animation: Smooth expand/collapse with 300ms ease-in-out

b) **Value Hint System**
   - Add "Why this matters" tooltips/popovers on key sections
   - These should appear on hover (desktop) or tap (mobile)
   - Content should be reassuring and educational, not intimidating

c) **Mini-Quiz Component**
   - Create an optional 3-question reflection quiz before starting
   - Questions: "What do you hope to learn?", "Current experience level?",
     "What energizes you about coding?"
   - Store answers in sessionStorage for personalization
   - Skip option always visible

d) **Call-to-Action**
   - Primary: "Let's Get Started" button
   - Secondary: "Explore First" link that scrolls to discovery cards
   - Tertiary: "I've done this before" quick-start link

#### 2. Path Selection Enhancement (`templates/paths.html`)

a) **Path Cards with Learn More**
   - Each path (Technical, Design, Collaboration, Problem-Solving, Communication)
     gets an interactive card
   - Default: Icon, title, one-sentence description, time estimate
   - "Learn more" expands to show: detailed description, what gets evaluated,
     example question preview, "Why this matters" hint
   - Selection state: Clear checkbox/toggle with visual feedback

b) **Personalized Recommendations**
   - Use the `/api/mobile/recommendations` endpoint
   - If mini-quiz was completed, use those answers
   - Show "Recommended for you" badges on suggested paths
   - Show reason: "Based on your goal to identify strengths"

c) **Progressive Selection**
   - Recommend 2-3 paths for first-time users
   - Show time estimate updating as paths are selected
   - Warning if selecting >3 paths: "This will take approximately X minutes"

d) **Continue Button State**
   - Disabled until at least 1 path selected
   - Shows count: "Continue with 2 paths"

#### 3. Assessment Page Enhancement (`templates/assess.html`)

a) **Guided Mode Toggle**
   - Default: ON for first-time users
   - When ON: Shows contextual hints, explanations, and tips
   - Persists preference in localStorage

b) **Section-by-Section Flow**
   - Instead of one long form, show one section at a time
   - Progress indicator: "Step 2 of 4"
   - "Why we ask this" button per section (expands inline explanation)
   - Smooth transitions between sections

c) **Rich Text Input**
   - Code input areas with syntax highlighting (use highlight.js or prism.js)
   - Character/word count
   - "Tips" collapsible section with writing suggestions
   - Auto-save to sessionStorage every 30 seconds

d) **Explanation Section**
   - Dedicated "Explain your thinking" textarea
   - Prompt: "Help us understand your approach (optional but valuable)"
   - Visual indicator showing this helps personalize feedback

#### 4. Results Page Enhancement (`templates/results.html`)

a) **Score Presentation**
   - Overall score with animated counter (0 to final score)
   - Visual representation (e.g., circular progress, bar chart)
   - Contextual message based on score range
   - Avoid "pass/fail" language - use growth-oriented framing

b) **Path Score Breakdown**
   - Collapsible sections for each evaluated path
   - Visual indicator (color-coded, but accessible)
   - Strengths list with checkmarks
   - Areas for improvement with growth-oriented language

c) **Evidence Display**
   - Show specific evidence quotes from their submission
   - Link evidence to scores: "We noticed [evidence]. This contributed to [score]."
   - Collapsible for detailed view

d) **Micro-Motives Section**
   - Visual display of detected micro-motives
   - Explain what each motive means
   - "This suggests you might enjoy..." personalized insight
   - Link to candidate-guide.md section on micro-motives

e) **Recommendations CTA**
   - "View Your Learning Path" button leading to insights page
   - Share results option (copy link or download PDF)
   - "Take Another Assessment" option

#### 5. Insights Page Enhancement (`templates/insights.html`)

a) **Learning Journey Visualization**
   - Timeline showing assessment history (if multiple)
   - Trend indicators (improving, stable, needs attention)
   - Achievement badges for milestones

b) **Actionable Recommendations**
   - Prioritized list based on assessment results
   - Each recommendation: title, description, resource links
   - "Mark as completed" interaction
   - Filter by path or priority

c) **Resource Links**
   - Link to Documentation/Guides/resources/
   - Categorized by skill area
   - External resource suggestions (with appropriate caveats)

d) **Next Steps Section**
   - Clear action items
   - Suggested timeline (without specific dates)
   - "Schedule a check-in" concept (track progress)

#### 6. JavaScript Architecture (`static/js/mobile.js`)

Create a modular JavaScript file with these modules:

```javascript
// Module structure
const SonoMobile = {
    // State management
    state: {
        candidateId: null,
        sessionId: null,
        selectedPaths: [],
        quizAnswers: {},
        guidedMode: true,
        currentStep: 0
    },

    // Initialization
    init() { },

    // Discovery cards
    discovery: {
        init() { },
        toggle(cardId) { },
        trackInteraction(cardId, action) { }
    },

    // Path selection
    paths: {
        init() { },
        togglePath(pathId) { },
        updateRecommendations() { },
        validateSelection() { }
    },

    // Assessment flow
    assess: {
        init() { },
        nextStep() { },
        prevStep() { },
        autoSave() { },
        submit() { }
    },

    // Results display
    results: {
        init() { },
        animateScores() { },
        toggleSection(sectionId) { },
        shareResults() { }
    },

    // Analytics (non-blocking)
    track: {
        event(eventType, data) { },
        pageView(page) { },
        milestone(milestone) { },
        flush() { }
    },

    // Utilities
    utils: {
        generateSessionId() { },
        saveToSession(key, value) { },
        getFromSession(key) { },
        showToast(message, type) { },
        animate(element, animation) { }
    }
};
```

#### 7. CSS Styling (`static/css/mobile.css`)

Implement mobile-first responsive design:

```css
/* Color variables matching Sono-Eval brand */
:root {
    --primary: #2563eb;
    --primary-light: #3b82f6;
    --success: #10b981;
    --warning: #f59e0b;
    --error: #ef4444;
    --text: #1f2937;
    --text-muted: #6b7280;
    --background: #ffffff;
    --surface: #f9fafb;
    --border: #e5e7eb;

    /* Spacing scale */
    --space-xs: 0.25rem;
    --space-sm: 0.5rem;
    --space-md: 1rem;
    --space-lg: 1.5rem;
    --space-xl: 2rem;

    /* Animation */
    --transition-fast: 150ms ease;
    --transition-normal: 300ms ease;
}

/* Mobile-first breakpoints */
/* Base: 0-640px (mobile) */
/* sm: 640px+ (tablet) */
/* md: 768px+ (small desktop) */
/* lg: 1024px+ (desktop) */
```

Key components to style:
- Discovery cards with expand/collapse animation
- Path selection cards with selection state
- Progress indicators
- Score visualizations (circular progress, bar charts)
- Toast notifications
- Collapsible sections
- Form inputs with validation states
- Buttons (primary, secondary, ghost variants)
- Loading states and skeleton screens

#### 8. API Endpoints to Add (`app.py`)

Add these endpoints to support the enhanced UX:

```python
@app.post("/api/mobile/quiz/submit")
async def submit_quiz(quiz_data: QuizSubmission):
    """Store quiz answers for personalization."""
    pass

@app.get("/api/mobile/progress/{candidate_id}")
async def get_progress(candidate_id: str):
    """Get candidate's assessment history and progress."""
    pass

@app.post("/api/mobile/autosave")
async def autosave_draft(draft: DraftSubmission):
    """Auto-save assessment draft."""
    pass

@app.get("/api/mobile/results/{assessment_id}/share")
async def get_shareable_results(assessment_id: str):
    """Generate shareable results link/data."""
    pass
```

### Testing Requirements

1. Test on multiple screen sizes (320px, 375px, 768px, 1024px)
2. Test keyboard navigation and screen reader compatibility
3. Test with slow network (3G simulation)
4. Test sessionStorage/localStorage handling
5. Test graceful degradation when JavaScript disabled

### Design Principles to Follow

From AGENT_KNOWLEDGE_BASE.md:
- Dieter Rams: "Less but better" - Remove clutter, unify styles
- Daniel Kahneman: Reduce cognitive load - "System 1 vs System 2"
- Julian Treasure: Conscious listening - Authentic presentation

### Success Criteria

1. New users can complete onboarding in <2 minutes
2. Path selection includes "Learn more" for each path
3. Assessment flow shows progress and estimated time
4. Results page animates and presents data progressively
5. Insights page provides actionable next steps
6. All interactions tracked for analytics
7. Works offline with previously loaded data
8. Lighthouse performance score >80
9. No console errors in production
```

---

## Area 2: Assessment Results Visualization & Dashboard

### Problem Statement

The system generates rich assessment data including:
- Overall scores with confidence levels
- Multi-path scores with individual metrics
- Evidence with sources and weights
- Micro-motives with strength indicators
- Recommendations and key findings
- Historical trends and statistics

However, the current visualization is limited to:
- Raw JSON returned from API
- Basic text rendering in templates
- The `DashboardData` class exists but is underutilized
- No interactive charts or visual representations

### Impact

Users (both candidates and evaluators) cannot quickly understand assessment results without parsing complex data structures. The "explainable" nature of the system is diminished when explanations require technical interpretation.

### Detailed Implementation Instructions for Coding Agents

```
## TASK: Enhance Assessment Results Visualization & Dashboard

### Context
Sono-Eval produces rich assessment data that needs compelling visualization. The goal
is to make results immediately understandable while preserving depth for those who
want details.

### Files to Modify/Create
- src/sono_eval/assessment/dashboard.py (enhance)
- src/sono_eval/mobile/templates/results.html (major enhancement)
- src/sono_eval/mobile/templates/insights.html (major enhancement)
- src/sono_eval/mobile/templates/partials/ (new directory)
- src/sono_eval/mobile/static/js/charts.js (create)
- src/sono_eval/mobile/static/js/results.js (create)
- src/sono_eval/api/main.py (add visualization endpoints)

### Requirements

#### 1. Dashboard Data Enhancement (`dashboard.py`)

Enhance the DashboardData class to prepare visualization-ready data:

```python
class DashboardData(BaseModel):
    """Visualization-ready dashboard data."""

    # Summary data
    summary: SummaryData

    # Chart-ready data structures
    radar_chart: RadarChartData      # Multi-path comparison
    progress_ring: ProgressRingData   # Overall score
    bar_chart: BarChartData           # Metric comparison
    trend_line: TrendLineData         # Historical performance
    motive_distribution: MotiveChartData  # Micro-motive breakdown

    # Evidence cards
    evidence_highlights: List[EvidenceCard]

    # Recommendations (prioritized)
    recommendations: List[RecommendationCard]

    # Comparison data (if available)
    benchmarks: Optional[BenchmarkData]

class RadarChartData(BaseModel):
    """Data structure for radar/spider chart."""
    labels: List[str]       # ["Technical", "Design", "Collaboration", ...]
    values: List[float]     # [85, 72, 90, ...]
    max_value: float = 100

class ProgressRingData(BaseModel):
    """Data structure for circular progress indicator."""
    value: float
    max_value: float = 100
    label: str
    color: str  # Based on score range
    message: str  # Contextual message

class EvidenceCard(BaseModel):
    """Card displaying a piece of evidence."""
    quote: str           # The actual evidence
    source: str          # Where it came from
    impact: str          # positive, negative, neutral
    metric: str          # Which metric it relates to
    explanation: str     # Why this matters
```

Add methods:

```python
@classmethod
def from_assessment_result(
    cls,
    result: AssessmentResult,
    historical: Optional[List[AssessmentResult]] = None
) -> "DashboardData":
    """
    Transform AssessmentResult into visualization-ready DashboardData.

    This method should:
    1. Extract and format data for each chart type
    2. Select top evidence items for highlighting
    3. Prioritize recommendations
    4. Calculate trends from historical data
    5. Generate contextual messages based on scores
    """
    pass

def to_chart_js_format(self) -> Dict[str, Any]:
    """Export data in Chart.js compatible format."""
    pass

def get_contextual_message(score: float) -> str:
    """
    Generate encouraging, growth-oriented message based on score.

    80-100: "Excellent work! You're demonstrating strong skills..."
    60-79: "Good progress! You have solid fundamentals..."
    40-59: "You're building skills! Focus on..."
    0-39: "Great starting point! With focused practice..."
    """
    pass
```

#### 2. Chart.js Integration (`static/js/charts.js`)

Create a chart module using Chart.js (include via CDN or bundle):

```javascript
const SonoCharts = {
    // Chart.js default configuration
    defaults: {
        font: {
            family: "'Inter', 'system-ui', sans-serif",
            size: 14
        },
        color: '#1f2937',
        responsive: true,
        maintainAspectRatio: false
    },

    /**
     * Create radar chart for multi-path comparison
     * @param {string} canvasId - Canvas element ID
     * @param {Object} data - { labels: [], values: [] }
     * @returns {Chart}
     */
    createRadarChart(canvasId, data) {
        // Implementation with:
        // - Filled area with gradient
        // - Point labels with scores
        // - Hover tooltip with path details
        // - Animation on load
    },

    /**
     * Create animated progress ring for overall score
     * @param {string} canvasId - Canvas element ID
     * @param {Object} data - { value, maxValue, color, label }
     * @returns {Chart}
     */
    createProgressRing(canvasId, data) {
        // Implementation with:
        // - Animated fill from 0 to value
        // - Center text showing score
        // - Color based on score range
        // - Optional pulse animation on completion
    },

    /**
     * Create horizontal bar chart for metrics comparison
     * @param {string} canvasId - Canvas element ID
     * @param {Object} data - { labels: [], values: [], colors: [] }
     * @returns {Chart}
     */
    createBarChart(canvasId, data) {
        // Implementation with:
        // - Horizontal bars (easier to read on mobile)
        // - Labels on left
        // - Value labels on bars
        // - Color coding by score range
    },

    /**
     * Create line chart for historical trends
     * @param {string} canvasId - Canvas element ID
     * @param {Object} data - { dates: [], values: [] }
     * @returns {Chart}
     */
    createTrendLine(canvasId, data) {
        // Implementation with:
        // - Smooth line with gradient fill below
        // - Point markers at each assessment
        // - Trend arrow indicator
        // - Responsive date labels
    },

    /**
     * Create doughnut chart for micro-motive distribution
     * @param {string} canvasId - Canvas element ID
     * @param {Object} data - { labels: [], values: [], colors: [] }
     * @returns {Chart}
     */
    createMotiveChart(canvasId, data) {
        // Implementation with:
        // - Doughnut with center icon
        // - Legend below chart
        // - Hover shows motive description
        // - Animated on load
    },

    // Utility functions
    utils: {
        getScoreColor(score) {
            if (score >= 80) return '#10b981'; // green
            if (score >= 60) return '#3b82f6'; // blue
            if (score >= 40) return '#f59e0b'; // yellow
            return '#ef4444'; // red
        },

        animateValue(element, start, end, duration) {
            // Animate number counting up
        },

        formatScore(score) {
            return Math.round(score * 10) / 10;
        }
    }
};
```

#### 3. Results Page Components (`templates/results.html`)

Structure the results page with these components:

```html
<!-- Results page structure -->

<!-- 1. Hero Section: Overall Score -->
<section class="results-hero">
    <div class="score-ring-container">
        <canvas id="overall-score-ring"></canvas>
    </div>
    <h1 class="score-message">{{ contextual_message }}</h1>
    <p class="score-subtitle">Assessment completed • {{ processing_time }}ms</p>
</section>

<!-- 2. Path Performance Radar -->
<section class="results-section">
    <h2>Your Performance Across Paths</h2>
    <div class="radar-container">
        <canvas id="path-radar"></canvas>
    </div>
    <p class="section-insight">{{ dominant_path_insight }}</p>
</section>

<!-- 3. Detailed Metrics -->
<section class="results-section">
    <h2>Detailed Breakdown</h2>
    {% for path_score in path_scores %}
    <div class="path-detail-card" data-path="{{ path_score.path }}">
        <div class="path-header" onclick="togglePathDetail(this)">
            <span class="path-icon">{{ path_icon }}</span>
            <span class="path-name">{{ path_score.path | title }}</span>
            <span class="path-score">{{ path_score.overall_score | round }}</span>
            <span class="expand-icon">▼</span>
        </div>
        <div class="path-content">
            <!-- Metrics bar chart -->
            <canvas id="metrics-{{ path_score.path }}"></canvas>

            <!-- Strengths -->
            <div class="strengths-list">
                <h4>✓ Strengths</h4>
                {% for strength in path_score.strengths %}
                <p class="strength-item">{{ strength }}</p>
                {% endfor %}
            </div>

            <!-- Areas for Improvement -->
            <div class="improvements-list">
                <h4>→ Areas to Develop</h4>
                {% for area in path_score.areas_for_improvement %}
                <p class="improvement-item">{{ area }}</p>
                {% endfor %}
            </div>
        </div>
    </div>
    {% endfor %}
</section>

<!-- 4. Evidence Highlights -->
<section class="results-section">
    <h2>What We Noticed</h2>
    <div class="evidence-cards">
        {% for evidence in evidence_highlights %}
        <div class="evidence-card {{ evidence.impact }}">
            <blockquote>"{{ evidence.quote }}"</blockquote>
            <p class="evidence-explanation">{{ evidence.explanation }}</p>
            <span class="evidence-source">{{ evidence.source }}</span>
        </div>
        {% endfor %}
    </div>
</section>

<!-- 5. Micro-Motives -->
<section class="results-section">
    <h2>What Drives You</h2>
    <p class="section-intro">Based on your submission, we identified these micro-motives:</p>
    <div class="motive-chart-container">
        <canvas id="motive-chart"></canvas>
    </div>
    <div class="motive-explanations">
        {% for motive in micro_motives %}
        <div class="motive-card">
            <span class="motive-icon">{{ motive_icon }}</span>
            <h4>{{ motive.motive_type | title }}</h4>
            <p>Strength: {{ (motive.strength * 100) | round }}%</p>
            <p class="motive-insight">{{ motive_insight }}</p>
        </div>
        {% endfor %}
    </div>
</section>

<!-- 6. Recommendations -->
<section class="results-section">
    <h2>Your Next Steps</h2>
    <div class="recommendations-list">
        {% for rec in recommendations %}
        <div class="recommendation-card">
            <span class="rec-priority">{{ loop.index }}</span>
            <div class="rec-content">
                <h4>{{ rec.title }}</h4>
                <p>{{ rec.description }}</p>
                {% if rec.resources %}
                <a href="{{ rec.resources }}" class="rec-link">Learn more →</a>
                {% endif %}
            </div>
        </div>
        {% endfor %}
    </div>
</section>

<!-- 7. Actions -->
<section class="results-actions">
    <button onclick="viewDetailedInsights()" class="btn-primary">
        View Detailed Insights
    </button>
    <button onclick="shareResults()" class="btn-secondary">
        Share Results
    </button>
    <button onclick="startNewAssessment()" class="btn-ghost">
        Take Another Assessment
    </button>
</section>
```

#### 4. Results JavaScript (`static/js/results.js`)

```javascript
const SonoResults = {
    data: null,
    charts: {},

    async init(assessmentId) {
        // Fetch dashboard data
        this.data = await this.fetchDashboardData(assessmentId);

        // Initialize all charts
        this.initOverallScore();
        this.initRadarChart();
        this.initMetricCharts();
        this.initMotiveChart();

        // Animate entrance
        this.animateEntrance();
    },

    async fetchDashboardData(assessmentId) {
        const candidateId = SonoMobile.state.candidateId;
        const response = await fetch(
            `/api/v1/assessments/${assessmentId}/dashboard?candidate_id=${candidateId}&include_history=true`
        );
        return response.json();
    },

    initOverallScore() {
        const ring = this.data.progress_ring;
        this.charts.overall = SonoCharts.createProgressRing('overall-score-ring', ring);

        // Animate the score number
        const scoreEl = document.querySelector('.score-value');
        SonoCharts.utils.animateValue(scoreEl, 0, ring.value, 1500);
    },

    initRadarChart() {
        const radar = this.data.radar_chart;
        this.charts.radar = SonoCharts.createRadarChart('path-radar', radar);
    },

    initMetricCharts() {
        this.data.path_scores.forEach(ps => {
            const canvasId = `metrics-${ps.path}`;
            const chartData = {
                labels: ps.metrics.map(m => m.name),
                values: ps.metrics.map(m => m.score),
                colors: ps.metrics.map(m => SonoCharts.utils.getScoreColor(m.score))
            };
            this.charts[canvasId] = SonoCharts.createBarChart(canvasId, chartData);
        });
    },

    initMotiveChart() {
        const motive = this.data.motive_distribution;
        this.charts.motive = SonoCharts.createMotiveChart('motive-chart', motive);
    },

    animateEntrance() {
        // Intersection Observer for scroll-triggered animations
        const sections = document.querySelectorAll('.results-section');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, { threshold: 0.1 });

        sections.forEach(section => observer.observe(section));
    },

    togglePathDetail(header) {
        const card = header.closest('.path-detail-card');
        card.classList.toggle('expanded');

        // Trigger chart resize if needed
        const canvas = card.querySelector('canvas');
        if (canvas && this.charts[canvas.id]) {
            this.charts[canvas.id].resize();
        }
    },

    async shareResults() {
        const shareData = {
            title: 'My Sono-Eval Assessment Results',
            text: `I scored ${this.data.summary.overall_score} on my developer assessment!`,
            url: window.location.href
        };

        if (navigator.share) {
            await navigator.share(shareData);
        } else {
            // Fallback: copy to clipboard
            await navigator.clipboard.writeText(shareData.url);
            SonoMobile.utils.showToast('Link copied to clipboard!', 'success');
        }
    }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    const assessmentId = new URLSearchParams(window.location.search).get('assessment_id');
    if (assessmentId) {
        SonoResults.init(assessmentId);
    }
});
```

#### 5. Insights Page (`templates/insights.html`)

Create a dedicated insights page for deeper analysis:

```html
<!-- Insights page for learning journey -->

<!-- 1. Progress Over Time -->
<section class="insights-section">
    <h2>Your Progress</h2>
    {% if historical_data %}
    <div class="trend-container">
        <canvas id="trend-chart"></canvas>
    </div>
    <div class="trend-summary">
        <span class="trend-indicator {{ trend_direction }}">
            {{ trend_arrow }} {{ trend_message }}
        </span>
    </div>
    {% else %}
    <p class="no-history">This is your first assessment. Take more to see your progress!</p>
    {% endif %}
</section>

<!-- 2. Learning Path -->
<section class="insights-section">
    <h2>Your Learning Path</h2>
    <div class="learning-path">
        {% for step in learning_steps %}
        <div class="learning-step {{ step.status }}">
            <div class="step-marker">{{ loop.index }}</div>
            <div class="step-content">
                <h4>{{ step.title }}</h4>
                <p>{{ step.description }}</p>
                {% if step.resources %}
                <div class="step-resources">
                    {% for resource in step.resources %}
                    <a href="{{ resource.url }}" class="resource-link">
                        {{ resource.icon }} {{ resource.title }}
                    </a>
                    {% endfor %}
                </div>
                {% endif %}
                {% if step.status == 'current' %}
                <button class="btn-small" onclick="markComplete({{ loop.index }})">
                    Mark as Completed
                </button>
                {% endif %}
            </div>
        </div>
        {% endfor %}
    </div>
</section>

<!-- 3. Skill Breakdown -->
<section class="insights-section">
    <h2>Skills Deep Dive</h2>
    <div class="skills-grid">
        {% for skill in skills_breakdown %}
        <div class="skill-card">
            <h4>{{ skill.name }}</h4>
            <div class="skill-bar">
                <div class="skill-fill" style="width: {{ skill.score }}%"></div>
            </div>
            <p class="skill-tip">{{ skill.improvement_tip }}</p>
        </div>
        {% endfor %}
    </div>
</section>

<!-- 4. Recommended Resources -->
<section class="insights-section">
    <h2>Resources For You</h2>
    <div class="resources-grid">
        {% for resource in recommended_resources %}
        <a href="{{ resource.url }}" class="resource-card">
            <span class="resource-icon">{{ resource.icon }}</span>
            <h4>{{ resource.title }}</h4>
            <p>{{ resource.description }}</p>
            <span class="resource-type">{{ resource.type }}</span>
        </a>
        {% endfor %}
    </div>
</section>
```

#### 6. API Endpoints for Visualization

Add to `api/main.py`:

```python
@app.get("/api/v1/assessments/{assessment_id}/visualization")
async def get_visualization_data(
    request: Request,
    assessment_id: str,
    candidate_id: str,
    chart_type: Optional[str] = None,  # radar, progress, bar, trend, motive
):
    """
    Get chart-ready visualization data for an assessment.

    Optionally filter by chart_type for efficiency.
    Returns Chart.js-compatible data structures.
    """
    pass

@app.get("/api/v1/candidates/{candidate_id}/learning-path")
async def get_learning_path(
    request: Request,
    candidate_id: str,
):
    """
    Generate personalized learning path based on assessment history.

    Returns prioritized steps with resources.
    """
    pass

@app.get("/api/v1/candidates/{candidate_id}/trends")
async def get_trends(
    request: Request,
    candidate_id: str,
    path: Optional[str] = None,
    limit: int = 10,
):
    """
    Get historical trends for a candidate.

    Returns time-series data for visualization.
    """
    pass
```

### Testing Requirements

1. Test charts render correctly at different sizes
2. Test data updates trigger chart re-renders
3. Test empty states (no data, single data point)
4. Test accessibility (screen readers can access data)
5. Test performance with large datasets
6. Test print stylesheet for results

### Success Criteria

1. Overall score animates on page load
2. Radar chart shows all paths with accurate values
3. Path details expand/collapse smoothly
4. Evidence cards display with appropriate styling
5. Micro-motives chart is interactive
6. Trend line shows historical progress
7. All charts are responsive
8. Page loads in <3 seconds
9. Charts accessible via ARIA labels
```

---

## Area 3: CLI Developer Experience & Guided Workflows

### Problem Statement

The CLI (`sono-eval`) provides functional commands but lacks:
- Progressive output during long operations
- Guided mode for first-time users
- Contextual help and suggestions
- Visual feedback and formatting
- Interactive prompts for complex operations
- Error recovery guidance

Current state:
- Commands work but output is minimal
- No progress indicators during assessment
- Errors show technical messages without guidance
- No interactive mode for exploration

### Impact

Developers using the CLI miss the "explainable" experience that's central to Sono-Eval's value proposition. The tool works but doesn't teach or guide.

### Detailed Implementation Instructions for Coding Agents

```
## TASK: Enhance CLI Developer Experience & Guided Workflows

### Context
The Sono-Eval CLI needs enhancement to provide a better developer experience with
progressive feedback, guided workflows, and rich output formatting.

### Files to Modify/Create
- src/sono_eval/cli/main.py (enhance)
- src/sono_eval/cli/commands/assess.py (major enhancement)
- src/sono_eval/cli/commands/candidate.py (enhance)
- src/sono_eval/cli/commands/setup.py (enhance)
- src/sono_eval/cli/interactive.py (create)
- src/sono_eval/cli/formatters.py (create)
- src/sono_eval/cli/progress.py (create)

### Requirements

#### 1. Rich Console Output (`formatters.py`)

Create a formatting module using Rich library:

```python
"""Rich console formatters for CLI output."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.tree import Tree
from rich.syntax import Syntax
from rich.markdown import Markdown

console = Console()

class AssessmentFormatter:
    """Format assessment results for CLI display."""

    @staticmethod
    def print_result(result: AssessmentResult) -> None:
        """Print formatted assessment result."""
        # Overall score with color coding
        score = result.overall_score
        score_color = "green" if score >= 80 else "yellow" if score >= 60 else "red"

        console.print(Panel(
            f"[bold {score_color}]{score:.1f}[/] / 100",
            title="Overall Score",
            subtitle=result.summary[:50] + "..."
        ))

        # Path scores table
        table = Table(title="Path Scores")
        table.add_column("Path", style="cyan")
        table.add_column("Score", justify="right")
        table.add_column("Strengths", style="green")
        table.add_column("Areas to Improve", style="yellow")

        for ps in result.path_scores:
            table.add_row(
                ps.path.value.title(),
                f"{ps.overall_score:.1f}",
                str(len(ps.strengths)),
                str(len(ps.areas_for_improvement))
            )

        console.print(table)

        # Recommendations
        console.print("\n[bold]Recommendations:[/]")
        for i, rec in enumerate(result.recommendations, 1):
            console.print(f"  {i}. {rec}")

    @staticmethod
    def print_path_detail(path_score: PathScore) -> None:
        """Print detailed path score with tree structure."""
        tree = Tree(f"[bold]{path_score.path.value.title()}[/]")

        strengths = tree.add("[green]✓ Strengths[/]")
        for s in path_score.strengths:
            strengths.add(s)

        improvements = tree.add("[yellow]→ Areas to Develop[/]")
        for i in path_score.areas_for_improvement:
            improvements.add(i)

        if path_score.metrics:
            metrics = tree.add("[blue]Metrics[/]")
            for m in path_score.metrics:
                metrics.add(f"{m.name}: {m.score:.1f} ({m.explanation})")

        console.print(tree)

class ProgressFormatter:
    """Format progress output for CLI."""

    @staticmethod
    def create_assessment_progress() -> Progress:
        """Create progress bar for assessment."""
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        )

    @staticmethod
    def print_step(step: str, status: str = "running") -> None:
        """Print a step in the process."""
        icons = {
            "running": "⏳",
            "done": "✓",
            "error": "✗",
            "skip": "○"
        }
        colors = {
            "running": "yellow",
            "done": "green",
            "error": "red",
            "skip": "dim"
        }
        icon = icons.get(status, "•")
        color = colors.get(status, "white")
        console.print(f"[{color}]{icon}[/] {step}")

class ErrorFormatter:
    """Format errors with helpful guidance."""

    @staticmethod
    def print_error(error: Exception, context: str = "") -> None:
        """Print formatted error with suggestions."""
        console.print(Panel(
            f"[bold red]Error:[/] {str(error)}",
            title="Something went wrong",
            border_style="red"
        ))

        # Contextual suggestions
        suggestions = ErrorFormatter.get_suggestions(error, context)
        if suggestions:
            console.print("\n[bold]Suggestions:[/]")
            for s in suggestions:
                console.print(f"  • {s}")

        console.print("\n[dim]Run 'sono-eval --help' for usage information[/]")

    @staticmethod
    def get_suggestions(error: Exception, context: str) -> list:
        """Get contextual suggestions for error."""
        suggestions = []
        error_str = str(error).lower()

        if "candidate" in error_str and "not found" in error_str:
            suggestions.append("Create a candidate first: sono-eval candidate create <id>")
            suggestions.append("List existing candidates: sono-eval candidate list")

        if "connection" in error_str or "network" in error_str:
            suggestions.append("Check if the server is running: sono-eval server status")
            suggestions.append("Start the server: sono-eval server start")

        if "permission" in error_str:
            suggestions.append("Check file permissions in the storage directory")
            suggestions.append("Run setup: sono-eval setup run")

        return suggestions
```

#### 2. Interactive Mode (`interactive.py`)

Create an interactive REPL for exploration:

```python
"""Interactive CLI mode for Sono-Eval."""

import click
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from rich.console import Console

from sono_eval.cli.formatters import console, AssessmentFormatter

class InteractiveSession:
    """Interactive session for exploring Sono-Eval."""

    def __init__(self):
        self.commands = {
            "help": self.show_help,
            "assess": self.run_assessment,
            "candidate": self.manage_candidate,
            "result": self.show_result,
            "explain": self.explain_concept,
            "quit": self.quit,
            "exit": self.quit,
        }

        self.completer = WordCompleter(
            list(self.commands.keys()) + [
                "technical", "design", "collaboration",
                "problem_solving", "communication"
            ]
        )

        self.session = PromptSession(
            history=FileHistory(".sono_eval_history"),
            completer=self.completer
        )

        self.state = {
            "candidate_id": None,
            "last_result": None,
        }

    def run(self):
        """Run the interactive session."""
        self.show_welcome()

        while True:
            try:
                user_input = self.session.prompt("sono-eval> ")
                self.handle_input(user_input)
            except KeyboardInterrupt:
                continue
            except EOFError:
                break

    def show_welcome(self):
        """Show welcome message."""
        console.print(Panel(
            "[bold]Welcome to Sono-Eval Interactive Mode[/]\n\n"
            "Type [cyan]help[/] for available commands\n"
            "Type [cyan]explain <concept>[/] to learn about any concept\n"
            "Press [cyan]Tab[/] for auto-completion",
            title="Interactive Mode",
            border_style="blue"
        ))

    def handle_input(self, user_input: str):
        """Parse and handle user input."""
        parts = user_input.strip().split()
        if not parts:
            return

        command = parts[0].lower()
        args = parts[1:]

        if command in self.commands:
            self.commands[command](args)
        else:
            console.print(f"[yellow]Unknown command: {command}[/]")
            console.print("Type 'help' for available commands")

    def show_help(self, args=None):
        """Show help information."""
        help_table = Table(title="Available Commands")
        help_table.add_column("Command", style="cyan")
        help_table.add_column("Description")
        help_table.add_column("Example")

        commands = [
            ("assess <paths>", "Run an assessment", "assess technical design"),
            ("candidate <action>", "Manage candidates", "candidate create john"),
            ("result [id]", "Show last/specific result", "result"),
            ("explain <concept>", "Explain a concept", "explain micro-motives"),
            ("help", "Show this help", "help"),
            ("quit/exit", "Exit interactive mode", "quit"),
        ]

        for cmd, desc, example in commands:
            help_table.add_row(cmd, desc, example)

        console.print(help_table)

    def explain_concept(self, args):
        """Explain a Sono-Eval concept."""
        if not args:
            console.print("[yellow]Usage: explain <concept>[/]")
            console.print("Concepts: paths, micro-motives, evidence, scoring, confidence")
            return

        concept = args[0].lower()
        explanations = {
            "paths": """
# Assessment Paths

Sono-Eval evaluates developers across multiple dimensions:

- **Technical**: Code quality, algorithms, testing
- **Design**: Architecture, patterns, system thinking
- **Collaboration**: Code readability, documentation
- **Problem-Solving**: Approach, debugging, edge cases
- **Communication**: Clarity, explanations, intent

Each path is scored independently, giving a nuanced view of skills.
            """,
            "micro-motives": """
# Micro-Motives (Dark Horse Model)

Micro-motives reveal what intrinsically motivates a developer:

- **Mastery**: Deep understanding and expertise
- **Exploration**: Trying new approaches
- **Collaboration**: Working with others
- **Innovation**: Creative solutions
- **Quality**: Craftsmanship and polish
- **Efficiency**: Optimization and speed

There are no "good" or "bad" motives - they're insights into work style.
            """,
            "evidence": """
# Evidence-Based Scoring

Every score in Sono-Eval is backed by evidence:

- Specific quotes from code
- Line numbers and file references
- Weighted by relevance
- Explained in context

This makes assessments transparent and actionable.
            """,
        }

        if concept in explanations:
            console.print(Markdown(explanations[concept]))
        else:
            console.print(f"[yellow]Unknown concept: {concept}[/]")

    def quit(self, args=None):
        """Exit interactive mode."""
        console.print("[dim]Goodbye![/]")
        raise EOFError()


@click.command()
def interactive():
    """Start interactive mode."""
    session = InteractiveSession()
    session.run()
```

#### 3. Enhanced Assess Command (`commands/assess.py`)

```python
"""Assessment command with rich output and progress."""

import asyncio
import click
from rich.live import Live
from rich.panel import Panel

from sono_eval.assessment.engine import AssessmentEngine
from sono_eval.assessment.models import AssessmentInput, PathType
from sono_eval.cli.formatters import (
    console,
    AssessmentFormatter,
    ProgressFormatter,
    ErrorFormatter
)

@click.group()
def assess():
    """Assessment commands."""
    pass

@assess.command()
@click.option("--candidate-id", "-c", required=True, help="Candidate identifier")
@click.option("--content", "-i", help="Content to assess (file path or text)")
@click.option("--paths", "-p", multiple=True, help="Paths to evaluate")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed output")
@click.option("--guided", "-g", is_flag=True, help="Run in guided mode")
@click.option("--output", "-o", type=click.Choice(["text", "json", "table"]), default="text")
def run(candidate_id, content, paths, verbose, guided, output):
    """
    Run an assessment.

    Examples:
        sono-eval assess run -c john -i code.py -p technical
        sono-eval assess run -c john --guided
    """
    if guided:
        # Interactive guided mode
        run_guided_assessment(candidate_id)
        return

    # Validate paths
    path_types = []
    for p in paths:
        try:
            path_types.append(PathType(p.lower()))
        except ValueError:
            console.print(f"[yellow]Warning: Unknown path '{p}', skipping[/]")

    if not path_types:
        path_types = list(PathType)  # Default to all paths

    # Load content
    if content:
        if Path(content).exists():
            with open(content) as f:
                content_data = {"code": f.read()}
        else:
            content_data = {"code": content}
    else:
        console.print("[yellow]No content provided. Running demo assessment.[/]")
        content_data = {"code": "# Demo code\ndef hello():\n    return 'world'"}

    # Run assessment with progress
    asyncio.run(run_assessment_with_progress(
        candidate_id, content_data, path_types, verbose, output
    ))

async def run_assessment_with_progress(
    candidate_id: str,
    content: dict,
    paths: list,
    verbose: bool,
    output: str
):
    """Run assessment with progress indication."""
    engine = AssessmentEngine()

    # Create progress display
    progress = ProgressFormatter.create_assessment_progress()

    with progress:
        task = progress.add_task("Running assessment...", total=100)

        # Phase 1: Initialization (0-20%)
        progress.update(task, description="Initializing engine...")
        await asyncio.sleep(0.1)  # Allow UI update
        progress.update(task, advance=20)

        # Phase 2: Analysis (20-60%)
        progress.update(task, description="Analyzing submission...")

        assessment_input = AssessmentInput(
            candidate_id=candidate_id,
            submission_type="code",
            content=content,
            paths_to_evaluate=paths
        )

        result = await engine.assess(assessment_input)
        progress.update(task, advance=40)

        # Phase 3: Scoring (60-80%)
        progress.update(task, description="Calculating scores...")
        await asyncio.sleep(0.1)
        progress.update(task, advance=20)

        # Phase 4: Generating report (80-100%)
        progress.update(task, description="Generating report...")
        await asyncio.sleep(0.1)
        progress.update(task, advance=20)

    # Display result
    console.print()  # Blank line

    if output == "json":
        console.print_json(result.model_dump_json())
    elif output == "table":
        AssessmentFormatter.print_result(result)
    else:
        # Rich text output
        AssessmentFormatter.print_result(result)

        if verbose:
            console.print("\n[bold]Detailed Path Analysis:[/]")
            for ps in result.path_scores:
                AssessmentFormatter.print_path_detail(ps)

    console.print(f"\n[dim]Assessment ID: {result.assessment_id}[/]")
    console.print("[dim]Run 'sono-eval assess explain <id>' for detailed analysis[/]")

def run_guided_assessment(candidate_id: str):
    """Run assessment in guided mode with prompts."""
    console.print(Panel(
        "[bold]Guided Assessment Mode[/]\n\n"
        "I'll walk you through the assessment process step by step.",
        title="Welcome",
        border_style="blue"
    ))

    # Step 1: Confirm candidate
    console.print(f"\n[cyan]Step 1:[/] Assessing candidate: [bold]{candidate_id}[/]")
    if not click.confirm("Is this correct?", default=True):
        candidate_id = click.prompt("Enter candidate ID")

    # Step 2: Select paths
    console.print("\n[cyan]Step 2:[/] Select assessment paths")
    console.print("Available paths:")
    for p in PathType:
        console.print(f"  • {p.value}: {get_path_description(p)}")

    paths_input = click.prompt(
        "Enter paths (comma-separated, or 'all')",
        default="all"
    )

    if paths_input.lower() == "all":
        paths = list(PathType)
    else:
        paths = [PathType(p.strip()) for p in paths_input.split(",")]

    # Step 3: Content input
    console.print("\n[cyan]Step 3:[/] Provide content to assess")
    content_type = click.prompt(
        "Content type",
        type=click.Choice(["file", "paste", "demo"]),
        default="demo"
    )

    if content_type == "file":
        file_path = click.prompt("File path")
        with open(file_path) as f:
            content = {"code": f.read()}
    elif content_type == "paste":
        console.print("Paste your code (end with Ctrl+D or Ctrl+Z):")
        lines = []
        try:
            while True:
                lines.append(input())
        except EOFError:
            pass
        content = {"code": "\n".join(lines)}
    else:
        content = {"code": "# Demo code\ndef example(): pass"}

    # Step 4: Run
    console.print("\n[cyan]Step 4:[/] Running assessment...")
    asyncio.run(run_assessment_with_progress(
        candidate_id, content, paths, verbose=True, output="text"
    ))

def get_path_description(path: PathType) -> str:
    """Get brief description for a path."""
    descriptions = {
        PathType.TECHNICAL: "Code quality, algorithms, testing",
        PathType.DESIGN: "Architecture, patterns, system thinking",
        PathType.COLLABORATION: "Readability, documentation, teamwork",
        PathType.PROBLEM_SOLVING: "Approach, debugging, edge cases",
        PathType.COMMUNICATION: "Clarity, explanations, intent",
    }
    return descriptions.get(path, "")

@assess.command()
@click.argument("assessment_id")
def explain(assessment_id):
    """
    Get detailed explanation of an assessment.

    Shows evidence, reasoning, and suggestions for each score.
    """
    console.print(f"[bold]Explaining Assessment: {assessment_id}[/]\n")
    # TODO: Implement retrieval and explanation
    console.print("[yellow]Assessment explanation coming soon![/]")
```

#### 4. Setup Command Enhancement (`commands/setup.py`)

```python
"""Enhanced setup command with guided workflow."""

import click
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt

from sono_eval.cli.formatters import console, ProgressFormatter
from sono_eval.utils.config import get_config

@click.group()
def setup():
    """Setup and configuration commands."""
    pass

@setup.command()
@click.option("--quick", is_flag=True, help="Quick setup with defaults")
def run(quick):
    """
    Run interactive setup wizard.

    Guides you through configuring Sono-Eval for first use.
    """
    if quick:
        run_quick_setup()
        return

    run_guided_setup()

def run_guided_setup():
    """Run the full guided setup wizard."""
    console.print(Panel(
        "[bold]Welcome to Sono-Eval Setup![/]\n\n"
        "I'll help you configure Sono-Eval for your environment.\n"
        "This takes about 2-3 minutes.",
        title="Setup Wizard",
        border_style="blue"
    ))

    steps = [
        ("Checking Python version", check_python),
        ("Checking dependencies", check_dependencies),
        ("Creating directories", create_directories),
        ("Creating configuration", create_config),
        ("Validating setup", validate_setup),
    ]

    console.print()

    for step_name, step_func in steps:
        with console.status(f"[bold blue]{step_name}..."):
            result = step_func()

        if result["success"]:
            ProgressFormatter.print_step(step_name, "done")
        else:
            ProgressFormatter.print_step(step_name, "error")
            console.print(f"  [red]Error: {result['error']}[/]")
            if result.get("suggestion"):
                console.print(f"  [yellow]Suggestion: {result['suggestion']}[/]")

            if not Confirm.ask("Continue anyway?", default=False):
                return

    # Success!
    console.print(Panel(
        "[bold green]Setup Complete![/]\n\n"
        "You're ready to use Sono-Eval:\n\n"
        "  [cyan]sono-eval assess run --guided[/]  Run a guided assessment\n"
        "  [cyan]sono-eval server start[/]         Start the API server\n"
        "  [cyan]sono-eval --help[/]               See all commands",
        title="Success",
        border_style="green"
    ))

def check_python() -> dict:
    """Check Python version."""
    import sys
    version = sys.version_info
    if version >= (3, 13):
        return {"success": True}
    return {
        "success": False,
        "error": f"Python 3.13+ required, found {version.major}.{version.minor}",
        "suggestion": "Install Python 3.13 from python.org"
    }

def check_dependencies() -> dict:
    """Check required dependencies."""
    missing = []
    for package in ["fastapi", "click", "pydantic", "rich"]:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    if missing:
        return {
            "success": False,
            "error": f"Missing packages: {', '.join(missing)}",
            "suggestion": "Run: pip install -e '.[dev]'"
        }
    return {"success": True}

def create_directories() -> dict:
    """Create required directories."""
    from pathlib import Path

    config = get_config()
    dirs = [
        config.get_storage_path(),
        config.get_cache_dir(),
        config.get_tagstudio_root(),
    ]

    try:
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

def create_config() -> dict:
    """Create configuration file if needed."""
    from pathlib import Path

    env_file = Path(".env")
    env_example = Path(".env.example")

    if env_file.exists():
        return {"success": True}

    if env_example.exists():
        import shutil
        shutil.copy(env_example, env_file)
        return {"success": True}

    # Create minimal config
    minimal_config = """# Sono-Eval Configuration
APP_ENV=development
DEBUG=true
LOG_LEVEL=INFO
"""
    env_file.write_text(minimal_config)
    return {"success": True}

def validate_setup() -> dict:
    """Validate the complete setup."""
    try:
        config = get_config()
        # Try to initialize engine
        from sono_eval.assessment.engine import AssessmentEngine
        engine = AssessmentEngine()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

@setup.command()
def check():
    """
    Check current setup status.

    Reports on configuration and component health.
    """
    console.print("[bold]Checking Sono-Eval Setup...[/]\n")

    checks = [
        ("Python version", check_python),
        ("Dependencies", check_dependencies),
        ("Directories", lambda: {"success": True}),  # Simplified
        ("Configuration", lambda: {"success": True}),
        ("Engine", validate_setup),
    ]

    all_ok = True
    for check_name, check_func in checks:
        result = check_func()
        if result["success"]:
            console.print(f"[green]✓[/] {check_name}")
        else:
            console.print(f"[red]✗[/] {check_name}: {result.get('error', 'Failed')}")
            all_ok = False

    console.print()
    if all_ok:
        console.print("[green]All checks passed![/]")
    else:
        console.print("[yellow]Some checks failed. Run 'sono-eval setup run' to fix.[/]")
```

#### 5. Main CLI Enhancement (`main.py`)

```python
"""Enhanced CLI entry point."""

import click
from rich.console import Console

from sono_eval.cli.commands.assess import assess
from sono_eval.cli.commands.candidate import candidate
from sono_eval.cli.commands.server import server
from sono_eval.cli.commands.setup import setup
from sono_eval.cli.commands.tag import tag
from sono_eval.cli.interactive import interactive
from sono_eval.cli.formatters import ErrorFormatter

console = Console()

@click.group(invoke_without_command=True)
@click.version_option(version="0.1.1")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.pass_context
def cli(ctx, verbose):
    """
    Sono-Eval: Explainable Multi-Path Developer Assessment System.

    \b
    Quick Start:
      sono-eval setup run       Configure Sono-Eval
      sono-eval assess --guided Run an interactive assessment
      sono-eval server start    Start the API server

    \b
    Learn More:
      sono-eval interactive     Start interactive exploration mode
      sono-eval explain <topic> Get explanation of a concept
    """
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose

    # If no command, show welcome
    if ctx.invoked_subcommand is None:
        show_welcome()

def show_welcome():
    """Show welcome message for first-time users."""
    from rich.panel import Panel

    console.print(Panel(
        "[bold]Welcome to Sono-Eval![/]\n\n"
        "An explainable, evidence-based developer assessment system.\n\n"
        "[cyan]Getting Started:[/]\n"
        "  • Run [bold]sono-eval setup run[/] to configure\n"
        "  • Run [bold]sono-eval assess --guided[/] for your first assessment\n"
        "  • Run [bold]sono-eval interactive[/] to explore\n\n"
        "[dim]Run 'sono-eval --help' for all commands[/]",
        title="Sono-Eval v0.1.1",
        border_style="blue"
    ))

@cli.command()
@click.argument("topic", required=False)
def explain(topic):
    """
    Explain a Sono-Eval concept.

    Topics: paths, motives, evidence, scoring, confidence, engine
    """
    from sono_eval.cli.interactive import InteractiveSession
    session = InteractiveSession()
    session.explain_concept([topic] if topic else [])

# Register command groups
cli.add_command(assess)
cli.add_command(candidate)
cli.add_command(server)
cli.add_command(tag)
cli.add_command(setup)
cli.add_command(interactive)

# Error handling wrapper
def main():
    """Main entry point with error handling."""
    try:
        cli()
    except Exception as e:
        ErrorFormatter.print_error(e)
        raise SystemExit(1)

if __name__ == "__main__":
    main()
```

### Testing Requirements

1. Test all commands with --help flag
2. Test guided mode for first-time users
3. Test error messages and suggestions
4. Test progress indicators update correctly
5. Test interactive mode commands
6. Test output formats (text, json, table)

### Success Criteria

1. Running `sono-eval` without args shows welcome message
2. `sono-eval assess --guided` walks through assessment interactively
3. `sono-eval setup run` guides through configuration
4. Progress indicators show during long operations
5. Errors include actionable suggestions
6. `sono-eval interactive` provides REPL exploration
7. `sono-eval explain <topic>` teaches concepts
8. All output is formatted with Rich
9. Commands complete without errors
```

---

## Implementation Priority

| Area | Priority | Effort | Impact | Dependencies |
|------|----------|--------|--------|--------------|
| Mobile Companion | High | High | High | None |
| Results Visualization | High | Medium | High | DashboardData exists |
| CLI Experience | Medium | Medium | Medium | Rich library |

## Recommended Execution Order

1. **Phase 1: CLI Enhancement** (Foundation)
   - Enhances developer experience immediately
   - Provides testing capability for other areas
   - Lower risk, faster iteration

2. **Phase 2: Results Visualization** (Core Value)
   - Dashboard data structure exists
   - Directly improves "explainable" value prop
   - Mobile and CLI can share visualization logic

3. **Phase 3: Mobile Companion** (Polish)
   - Builds on visualization work
   - Highest effort but highest user impact
   - Can be delivered incrementally

---

## Notes for Coding Agents

1. **Follow Existing Patterns**: The codebase uses Pydantic models, async/await, and type hints consistently. Maintain this style.

2. **Security First**: All user input must be validated. Follow the patterns in `AssessmentInput` validation.

3. **Test Coverage**: Add tests for new functionality. See `tests/` for patterns.

4. **Documentation**: Update docstrings and user-facing docs when adding features.

5. **No Breaking Changes**: Ensure backward compatibility with existing API endpoints.

6. **Reference Files**:
   - `AGENT_KNOWLEDGE_BASE.md` - Critical agent instructions
   - `Documentation/Governance/DOCUMENTATION_ORGANIZATION_STANDARDS.md` - Doc standards
   - `src/sono_eval/assessment/models.py` - Data model patterns

---

*Generated: January 2026*
*For: Sono-Eval v0.1.1*
