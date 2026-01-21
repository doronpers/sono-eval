/**
 * Chart.js integration for Sono-Eval visualizations
 *
 * Provides reusable chart components for assessment results.
 */

// Chart.js will be loaded from CDN in the HTML templates

/**
 * Initialize Chart.js with global defaults
 */
function initChartDefaults() {
    if (typeof Chart === 'undefined') {
        console.warn('Chart.js not loaded');
        return;
    }

    Chart.defaults.font.family = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
    Chart.defaults.font.size = 13;
    Chart.defaults.color = '#6b7280';
    Chart.defaults.plugins.legend.display = false;
}

/**
 * Create a radar chart for path scores
 * @param {string} canvasId - Canvas element ID
 * @param {object} data - Chart data from dashboard API
 * @returns {Chart} Chart instance
 */
function createRadarChart(canvasId, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.error(`Canvas element ${canvasId} not found`);
        return null;
    }

    return new Chart(ctx, {
        type: 'radar',
        data: {
            labels: data.labels,
            datasets: data.datasets.map(dataset => ({
                ...dataset,
                fill: true,
                backgroundColor: dataset.backgroundColor || 'rgba(59, 130, 246, 0.2)',
                borderColor: dataset.borderColor || 'rgb(59, 130, 246)',
                borderWidth: 2,
                pointBackgroundColor: dataset.pointBackgroundColor || 'rgb(59, 130, 246)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: dataset.pointHoverBorderColor || 'rgb(59, 130, 246)',
                pointRadius: 4,
                pointHoverRadius: 6,
            }))
        },
        options: {
            ...data.options,
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        stepSize: 20,
                        backdropColor: 'transparent'
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    pointLabels: {
                        font: {
                            size: 12,
                            weight: '500'
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: ${context.parsed.r.toFixed(1)}/100`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Create a progress ring (doughnut) chart
 * @param {string} canvasId - Canvas element ID
 * @param {object} data - Chart data from dashboard API
 * @returns {Chart} Chart instance
 */
function createProgressRing(canvasId, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.error(`Canvas element ${canvasId} not found`);
        return null;
    }

    const score = data.datasets[0].data[0];
    const scoreColor = getScoreColor(score);

    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.labels,
            datasets: [{
                ...data.datasets[0],
                backgroundColor: [scoreColor, '#e5e7eb'],
                borderWidth: 0,
                cutout: '75%'
            }]
        },
        options: {
            ...data.options,
            responsive: true,
            maintainAspectRatio: true,
            rotation: -90,
            circumference: 360,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            }
        },
        plugins: [{
            id: 'centerText',
            beforeDraw: function(chart) {
                const width = chart.width;
                const height = chart.height;
                const ctx = chart.ctx;
                ctx.restore();

                const fontSize = (height / 100).toFixed(2);
                ctx.font = `bold ${fontSize}em sans-serif`;
                ctx.textBaseline = 'middle';
                ctx.fillStyle = scoreColor;

                const text = `${score.toFixed(0)}`;
                const textX = Math.round((width - ctx.measureText(text).width) / 2);
                const textY = height / 2;

                ctx.fillText(text, textX, textY);

                // Subtitle
                ctx.font = `${(fontSize * 0.4).toFixed(2)}em sans-serif`;
                ctx.fillStyle = '#6b7280';
                const subtitle = '/100';
                const subtitleX = Math.round((width - ctx.measureText(subtitle).width) / 2);
                const subtitleY = textY + (fontSize * 20);
                ctx.fillText(subtitle, subtitleX, subtitleY);

                ctx.save();
            }
        }]
    });
}

/**
 * Create a horizontal bar chart for path breakdown or motives
 * @param {string} canvasId - Canvas element ID
 * @param {object} data - Chart data from dashboard API
 * @returns {Chart} Chart instance
 */
function createHorizontalBarChart(canvasId, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.error(`Canvas element ${canvasId} not found`);
        return null;
    }

    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: data.datasets.map(dataset => ({
                ...dataset,
                borderRadius: 8,
                barThickness: 20,
                maxBarThickness: 30
            }))
        },
        options: {
            ...data.options,
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    beginAtZero: true,
                    max: 100,
                    grid: {
                        display: true,
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        callback: function(value) {
                            return value;
                        }
                    }
                },
                y: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 12
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: ${context.parsed.x.toFixed(1)}`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Create a trend line chart
 * @param {string} canvasId - Canvas element ID
 * @param {object} data - Chart data from dashboard API
 * @returns {Chart} Chart instance
 */
function createTrendChart(canvasId, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.error(`Canvas element ${canvasId} not found`);
        return null;
    }

    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: data.datasets.map(dataset => ({
                ...dataset,
                tension: 0.4,
                fill: true,
                pointRadius: 4,
                pointHoverRadius: 6,
                borderWidth: 2
            }))
        },
        options: {
            ...data.options,
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45,
                        font: {
                            size: 10
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            return `Score: ${context.parsed.y.toFixed(1)}`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Create multiple path breakdown charts
 * @param {string} containerId - Container element ID
 * @param {array} chartsData - Array of chart data objects
 */
function createPathBreakdownCharts(containerId, chartsData) {
    const container = document.getElementById(containerId);
    if (!container) {
        console.error(`Container element ${containerId} not found`);
        return;
    }

    chartsData.forEach((chartData, index) => {
        // Create canvas element
        const wrapper = document.createElement('div');
        wrapper.className = 'chart-wrapper mb-6';
        wrapper.innerHTML = `
            <h3 class="text-lg font-semibold mb-3 capitalize">
                ${chartData.path.replace('_', ' ')}
            </h3>
            <div class="chart-container" style="height: 200px;">
                <canvas id="breakdown-${index}"></canvas>
            </div>
        `;
        container.appendChild(wrapper);

        // Create chart
        createHorizontalBarChart(`breakdown-${index}`, chartData);
    });
}

/**
 * Get color for score value
 * @param {number} score - Score value (0-100)
 * @returns {string} Hex color
 */
function getScoreColor(score) {
    if (score >= 85) return '#22c55e'; // green
    if (score >= 70) return '#3b82f6'; // blue
    if (score >= 60) return '#f59e0b'; // amber
    return '#ef4444'; // red
}

/**
 * Get grade for score value
 * @param {number} score - Score value (0-100)
 * @returns {string} Letter grade
 */
function getScoreGrade(score) {
    if (score >= 90) return 'A';
    if (score >= 80) return 'B';
    if (score >= 70) return 'C';
    if (score >= 60) return 'D';
    return 'F';
}

/**
 * Animate chart on appear
 * @param {Chart} chart - Chart instance
 */
function animateChart(chart) {
    if (!chart) return;

    chart.options.animation = {
        duration: 1000,
        easing: 'easeInOutQuart'
    };
    chart.update();
}

/**
 * Create all charts from dashboard data
 * @param {object} dashboardData - Complete dashboard data object
 */
async function createAllCharts(dashboardData) {
    initChartDefaults();

    // Overall score ring
    if (dashboardData.overall_score !== undefined) {
        const ringData = {
            labels: ['Score', 'Remaining'],
            datasets: [{
                data: [dashboardData.overall_score, 100 - dashboardData.overall_score]
            }],
            options: {}
        };
        createProgressRing('overall-score-chart', ringData);
    }

    // Radar chart for path scores
    if (dashboardData.radar_chart_data) {
        createRadarChart('path-radar-chart', dashboardData.radar_chart_data);
    }

    // Trend chart
    if (dashboardData.trend_data && dashboardData.trend_data.length > 0) {
        // Convert trend data to chart format
        const trendChartData = {
            labels: dashboardData.trend_data.map(t => t.timestamp),
            datasets: [{
                label: 'Score Over Time',
                data: dashboardData.trend_data.map(t => t.score),
                borderColor: getTrendColor(dashboardData.trend_direction)
            }],
            options: {}
        };
        createTrendChart('trend-chart', trendChartData);
    }

    // Motives chart
    if (dashboardData.motives && dashboardData.motives.length > 0) {
        const motivesData = {
            labels: dashboardData.motives.map(m => m.label),
            datasets: [{
                label: 'Strength',
                data: dashboardData.motives.map(m => m.strength * 100),
                backgroundColor: dashboardData.motives.map(m => m.color)
            }],
            options: {}
        };
        createHorizontalBarChart('motives-chart', motivesData);
    }
}

/**
 * Get color for trend direction
 * @param {string} direction - 'improving', 'declining', or 'stable'
 * @returns {string} Hex color
 */
function getTrendColor(direction) {
    switch(direction) {
        case 'improving': return '#22c55e';
        case 'declining': return '#ef4444';
        default: return '#6b7280';
    }
}

/**
 * Export chart as image
 * @param {Chart} chart - Chart instance
 * @returns {string} Base64 encoded image
 */
function exportChartImage(chart) {
    if (!chart) return null;
    return chart.toBase64Image();
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initChartDefaults);
} else {
    initChartDefaults();
}

// Export functions for use in other modules
window.SonoCharts = {
    initChartDefaults,
    createRadarChart,
    createProgressRing,
    createHorizontalBarChart,
    createTrendChart,
    createPathBreakdownCharts,
    createAllCharts,
    getScoreColor,
    getScoreGrade,
    animateChart,
    exportChartImage
};
