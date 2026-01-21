/**
 * Results page functionality for Sono-Eval mobile companion.
 * Handles data visualization, animations, and user interactions.
 */

class ResultsDisplay {
    constructor() {
        this.assessmentData = null;
        this.init();
    }

    init() {
        // Try to get assessment ID from URL or sessionStorage
        const urlParams = new URLSearchParams(window.location.search);
        const assessmentId = urlParams.get('assessment_id');
        const candidateId = urlParams.get('candidate_id');

        // Check sessionStorage for recent assessment
        const storedResult = sessionStorage.getItem('lastAssessmentResult');

        if (storedResult) {
            try {
                this.assessmentData = JSON.parse(storedResult);
                this.renderResults();
            } catch (e) {
                console.error('Error parsing stored result:', e);
                if (assessmentId && candidateId) {
                    this.fetchAssessment(assessmentId, candidateId);
                } else {
                    this.showNoResults();
                }
            }
        } else if (assessmentId && candidateId) {
            this.fetchAssessment(assessmentId, candidateId);
        } else {
            this.showNoResults();
        }
    }

    async fetchAssessment(assessmentId, candidateId) {
        try {
            const safeAssessmentId = encodeURIComponent(assessmentId);
            const safeCandidateId = encodeURIComponent(candidateId);
            const response = await fetch(
                `/api/v1/assessments/${safeAssessmentId}?candidate_id=${safeCandidateId}`
            );
            if (response.ok) {
                this.assessmentData = await response.json();
                // Store in sessionStorage for future reference
                sessionStorage.setItem('lastAssessmentResult', JSON.stringify(this.assessmentData));
                this.renderResults();
            } else {
                this.showNoResults();
            }
        } catch (error) {
            console.error('Error fetching assessment:', error);
            this.showNoResults();
        }
    }

    renderResults() {
        const data = this.assessmentData;
        if (!data) return;

        document.getElementById('results-app').classList.remove('hidden');
        document.getElementById('no-results').classList.add('hidden');

        // Animate overall score
        this.animateScore(data.overall_score);

        // Confidence
        document.getElementById('confidence-value').textContent =
            `${(data.confidence * 100).toFixed(0)}%`;

        // Assessment ID
        document.getElementById('assessment-id').textContent =
            `ID: ${data.assessment_id}`;

        // Summary
        document.getElementById('summary-text').textContent = data.summary || '';

        // Path scores visualization
        this.renderPathScores(data.path_scores || []);

        // Key findings
        this.renderList('findings-list', data.key_findings || [], 'finding');

        // Strengths and improvements
        this.renderStrengthsAndImprovements(data.path_scores || []);

        // Recommendations
        this.renderRecommendations(data.recommendations || []);

        // Micro-motives (if present)
        if (data.micro_motives && data.micro_motives.length > 0) {
            this.renderMotives(data.micro_motives);
        }
    }

    animateScore(score) {
        const scoreNumber = document.getElementById('score-number');
        const scoreRing = document.getElementById('score-ring');
        const safeScore = Number.isFinite(score) ? Math.max(0, Math.min(score, 100)) : 0;

        // Animate number
        let current = 0;
        const duration = 1500;
        const step = safeScore / (duration / 16);

        const animate = () => {
            current = Math.min(current + step, safeScore);
            scoreNumber.textContent = Math.round(current);

            // Animate ring
            const circumference = 2 * Math.PI * 45;
            const offset = circumference - (current / 100) * circumference;
            scoreRing.style.strokeDasharray = circumference;
            scoreRing.style.strokeDashoffset = offset;

            // Color based on score
            const color = this.getScoreColor(current);
            scoreRing.style.stroke = color;

            if (current < safeScore) {
                requestAnimationFrame(animate);
            }
        };

        requestAnimationFrame(animate);
    }

    getScoreColor(score) {
        if (score >= 80) return '#22c55e';  // green
        if (score >= 60) return '#eab308';  // yellow
        return '#ef4444';  // red
    }

    renderPathScores(pathScores) {
        if (!pathScores || pathScores.length === 0) return;

        // Use Chart.js radar chart if available
        if (window.SonoCharts && window.SonoCharts.createRadarChart) {
            const labels = pathScores.map(ps => this.formatPathName(ps.path));
            const data = pathScores.map(ps => Number(ps.overall_score) || 0);

            const chartData = {
                labels: labels,
                datasets: [{
                    label: 'Path Scores',
                    data: data,
                    backgroundColor: 'rgba(59, 130, 246, 0.2)',
                    borderColor: 'rgb(59, 130, 246)',
                }],
                options: {}
            };

            try {
                window.SonoCharts.createRadarChart('path-radar-chart', chartData);
            } catch (e) {
                console.error('Error creating radar chart:', e);
                this.renderPathScoresFallback(pathScores);
            }

            // Also show detailed breakdowns if available
            const breakdowns = pathScores.filter(ps => ps.metrics && ps.metrics.length > 0);
            if (breakdowns.length > 0 && window.SonoCharts && window.SonoCharts.createPathBreakdownCharts) {
                document.getElementById('path-breakdowns-section').style.display = 'block';

                const chartsData = breakdowns.map(ps => ({
                    path: ps.path,
                    labels: ps.metrics.map(m => m.name),
                    datasets: [{
                        label: 'Score',
                        data: ps.metrics.map(m => m.score),
                        backgroundColor: ps.metrics.map(() => this.getScoreColor(ps.overall_score)),
                    }],
                    options: {}
                }));

                window.SonoCharts.createPathBreakdownCharts('path-breakdowns', chartsData);
            }
        } else {
            this.renderPathScoresFallback(pathScores);
        }
    }

    renderPathScoresFallback(pathScores) {
        const container = document.getElementById('path-scores-table');
        container.innerHTML = '';

        pathScores.forEach((ps, index) => {
            const bar = document.createElement('div');
            bar.className = 'path-score-bar';
            const label = document.createElement('div');
            label.className = 'bar-label';

            const name = document.createElement('span');
            name.className = 'path-name';
            name.textContent = this.formatPathName(ps.path);

            const score = Number(ps.overall_score);
            const clampedScore = Number.isFinite(score) ? Math.max(0, Math.min(score, 100)) : 0;
            const scoreLabel = document.createElement('span');
            scoreLabel.className = 'path-score';
            scoreLabel.textContent = Number.isFinite(score) ? score.toFixed(1) : '--';

            label.appendChild(name);
            label.appendChild(scoreLabel);

            const track = document.createElement('div');
            track.className = 'bar-track';

            const fill = document.createElement('div');
            fill.className = 'bar-fill';
            fill.style.setProperty('--target-width', `${clampedScore}%`);
            fill.style.setProperty('--delay', `${index * 0.1}s`);
            fill.style.background = this.getScoreColor(clampedScore);

            track.appendChild(fill);
            bar.appendChild(label);
            bar.appendChild(track);
            container.appendChild(bar);

            // Animate bar fill
            setTimeout(() => {
                fill.style.width = `${clampedScore}%`;
            }, index * 100);
        });
    }

    formatPathName(path) {
        if (!path) {
            return 'Unknown';
        }
        return String(path).replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    }

    renderList(elementId, items, className) {
        const list = document.getElementById(elementId);
        list.innerHTML = '';

        items.forEach(item => {
            const li = document.createElement('li');
            li.className = className;
            li.textContent = item;
            list.appendChild(li);
        });
    }

    renderStrengthsAndImprovements(pathScores) {
        const strengths = [];
        const improvements = [];

        pathScores.forEach(ps => {
            if (ps.strengths) strengths.push(...ps.strengths);
            if (ps.areas_for_improvement) improvements.push(...ps.areas_for_improvement);
        });

        this.renderList('strengths-list', strengths.slice(0, 5), 'strength-item');
        this.renderList('improvements-list', improvements.slice(0, 5), 'improvement-item');
    }

    renderRecommendations(recommendations) {
        const container = document.getElementById('recommendations-list');
        container.innerHTML = '';

        recommendations.forEach((rec, index) => {
            const item = document.createElement('div');
            item.className = 'recommendation-item';
            const number = document.createElement('span');
            number.className = 'rec-number';
            number.textContent = String(index + 1);

            const text = document.createElement('span');
            text.className = 'rec-text';
            text.textContent = String(rec ?? '');

            item.appendChild(number);
            item.appendChild(text);
            container.appendChild(item);
        });
    }

    renderMotives(motives) {
        if (!motives || motives.length === 0) return;

        const section = document.getElementById('motives-section');
        section.style.display = 'block';

        // Use Chart.js if available
        if (window.SonoCharts && window.SonoCharts.createHorizontalBarChart) {
            const sortedMotives = motives
                .sort((a, b) => b.strength - a.strength)
                .slice(0, 8); // Top 8

            const labels = sortedMotives.map(m =>
                String(m.motive_type ?? '').replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())
            );
            const data = sortedMotives.map(m => (Number(m.strength) || 0) * 100);
            const colors = [
                '#3b82f6', '#8b5cf6', '#22c55e', '#f59e0b',
                '#06b6d4', '#ec4899', '#84cc16', '#f97316'
            ];

            const chartData = {
                labels: labels,
                datasets: [{
                    label: 'Strength',
                    data: data,
                    backgroundColor: colors.slice(0, sortedMotives.length),
                }],
                options: {}
            };

            try {
                window.SonoCharts.createHorizontalBarChart('motives-chart', chartData);

                // Show dominant motive
                if (sortedMotives.length > 0) {
                    const dominant = sortedMotives[0];
                    const dominantEl = document.getElementById('dominant-motive');
                    if (dominantEl) {
                        dominantEl.innerHTML = `
                            <div class="p-4 bg-blue-50 rounded-lg border border-blue-200">
                                <p class="text-sm text-gray-600">Your dominant motive:</p>
                                <p class="text-lg font-semibold text-blue-600 capitalize">
                                    ${String(dominant.motive_type).replace(/_/g, ' ')}
                                </p>
                            </div>
                        `;
                    }
                }
            } catch (e) {
                console.error('Error creating motives chart:', e);
                this.renderMotivesFallback(motives);
            }
        } else {
            this.renderMotivesFallback(motives);
        }
    }

    renderMotivesFallback(motives) {
        const chart = document.getElementById('motives-chart');
        chart.innerHTML = '';
        chart.style.height = 'auto';

        motives.forEach(motive => {
            const bar = document.createElement('div');
            bar.className = 'motive-bar';
            const label = document.createElement('div');
            label.className = 'motive-label';
            label.textContent = String(motive.motive_type ?? '');

            const track = document.createElement('div');
            track.className = 'motive-track';

            const fill = document.createElement('div');
            fill.className = 'motive-fill';
            const strength = Number(motive.strength);
            const clampedStrength = Number.isFinite(strength)
                ? Math.max(0, Math.min(strength, 1))
                : 0;
            fill.style.width = `${clampedStrength * 100}%`;

            const value = document.createElement('div');
            value.className = 'motive-value';
            value.textContent = `${Math.round(clampedStrength * 100)}%`;

            track.appendChild(fill);
            bar.appendChild(label);
            bar.appendChild(track);
            bar.appendChild(value);
            chart.appendChild(bar);
        });
    }

    showNoResults() {
        document.getElementById('results-app').classList.add('hidden');
        document.getElementById('no-results').classList.remove('hidden');
    }
}

// Utility functions
function downloadResults() {
    const stored = sessionStorage.getItem('lastAssessmentResult');
    if (!stored) {
        alert('No results available to download');
        return;
    }

    try {
        const data = JSON.parse(stored);
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `assessment-${data.assessment_id || 'result'}.json`;
        a.click();
        URL.revokeObjectURL(url);
    } catch (e) {
        console.error('Error downloading results:', e);
        alert('Error downloading results');
    }
}

function startNewAssessment() {
    sessionStorage.removeItem('lastAssessmentResult');
    location.href = '/mobile/start';
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    new ResultsDisplay();
});
