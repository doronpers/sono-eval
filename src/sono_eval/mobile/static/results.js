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
            const response = await fetch(
                `/api/v1/assessments/${assessmentId}?candidate_id=${candidateId}`
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
        
        // Animate number
        let current = 0;
        const duration = 1500;
        const step = score / (duration / 16);
        
        const animate = () => {
            current = Math.min(current + step, score);
            scoreNumber.textContent = Math.round(current);
            
            // Animate ring
            const circumference = 2 * Math.PI * 45;
            const offset = circumference - (current / 100) * circumference;
            scoreRing.style.strokeDasharray = circumference;
            scoreRing.style.strokeDashoffset = offset;
            
            // Color based on score
            const color = this.getScoreColor(current);
            scoreRing.style.stroke = color;
            
            if (current < score) {
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
        const container = document.getElementById('path-scores');
        container.innerHTML = '';

        pathScores.forEach((ps, index) => {
            const bar = document.createElement('div');
            bar.className = 'path-score-bar';
            bar.innerHTML = `
                <div class="bar-label">
                    <span class="path-name">${this.formatPathName(ps.path)}</span>
                    <span class="path-score">${ps.overall_score.toFixed(1)}</span>
                </div>
                <div class="bar-track">
                    <div class="bar-fill" style="--target-width: ${ps.overall_score}%; --delay: ${index * 0.1}s; background: ${this.getScoreColor(ps.overall_score)}"></div>
                </div>
            `;
            container.appendChild(bar);
            
            // Animate bar fill
            setTimeout(() => {
                const fill = bar.querySelector('.bar-fill');
                fill.style.width = `${ps.overall_score}%`;
            }, index * 100);
        });
    }

    formatPathName(path) {
        return path.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
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
            item.innerHTML = `
                <span class="rec-number">${index + 1}</span>
                <span class="rec-text">${rec}</span>
            `;
            container.appendChild(item);
        });
    }

    renderMotives(motives) {
        const section = document.getElementById('motives-section');
        const chart = document.getElementById('motives-chart');
        
        section.style.display = 'block';
        chart.innerHTML = '';

        motives.forEach(motive => {
            const bar = document.createElement('div');
            bar.className = 'motive-bar';
            bar.innerHTML = `
                <div class="motive-label">${motive.motive_type}</div>
                <div class="motive-track">
                    <div class="motive-fill" style="width: ${motive.strength * 100}%"></div>
                </div>
                <div class="motive-value">${(motive.strength * 100).toFixed(0)}%</div>
            `;
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
