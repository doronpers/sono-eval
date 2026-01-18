// Mobile companion JavaScript utilities

// Smooth scroll behavior
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling to anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add touch feedback to buttons
    document.querySelectorAll('button, .path-card').forEach(element => {
        element.addEventListener('touchstart', function() {
            this.style.opacity = '0.7';
        });

        element.addEventListener('touchend', function() {
            this.style.opacity = '1';
        });
    });
});

// Utility functions for session storage
function saveToSession(key, value) {
    try {
        sessionStorage.setItem(key, typeof value === 'object' ? JSON.stringify(value) : value);
    } catch (e) {
        console.warn('Session storage not available:', e);
    }
}

function getFromSession(key, defaultValue = null) {
    try {
        const value = sessionStorage.getItem(key);
        if (value === null) return defaultValue;
        try {
            return JSON.parse(value);
        } catch {
            return value;
        }
    } catch (e) {
        console.warn('Session storage not available:', e);
        return defaultValue;
    }
}

// Progress tracking with value-driven messages
const progressMessages = {
    'welcome': [
        { percent: 0, message: 'Welcome! Let\'s discover your strengths' },
        { percent: 25, message: 'Exploring what makes Sono-Eval different' },
        { percent: 50, message: 'Understanding your assessment options' },
        { percent: 75, message: 'Almost ready to begin' },
        { percent: 100, message: 'Ready to start your journey' }
    ],
    'paths': [
        { percent: 0, message: 'Choosing your focus areas' },
        { percent: 33, message: 'Discovering which paths match your goals' },
        { percent: 66, message: 'Selecting areas to assess' },
        { percent: 100, message: 'Paths selected - ready to assess' }
    ],
    'assess': [
        { percent: 0, message: 'Starting your assessment' },
        { percent: 25, message: 'Sharing your work and thinking' },
        { percent: 50, message: 'Halfway through - you\'re doing great!' },
        { percent: 75, message: 'Almost done - finishing strong' },
        { percent: 100, message: 'Assessment complete - analyzing results' }
    ],
    'results': [
        { percent: 0, message: 'Analyzing your assessment' },
        { percent: 50, message: 'Identifying your strengths and growth areas' },
        { percent: 100, message: 'Your insights are ready!' }
    ]
};

function updateProgress(current, total, page = null) {
    const progressBar = document.querySelector('.progress-fill');
    const progressContainer = document.querySelector('.progress-bar');

    if (progressBar) {
        const percentage = (current / total) * 100;
        progressBar.style.width = `${percentage}%`;

        // Update progress message if container exists
        if (page && progressMessages[page]) {
            const messages = progressMessages[page];
            const currentMessage = messages.find(m => percentage >= m.percent) || messages[messages.length - 1];

            let messageElement = document.querySelector('.progress-message');
            if (!messageElement && progressContainer) {
                messageElement = document.createElement('div');
                messageElement.className = 'progress-message';
                progressContainer.parentElement.insertBefore(messageElement, progressContainer.nextSibling);
            }

            if (messageElement) {
                messageElement.textContent = currentMessage.message;
            }
        }
    }
}

// Track learning milestones
function trackLearningMilestone(milestoneName, data = {}) {
    if (window.sonoEvalTracking && window.sonoEvalTracking.trackMilestone) {
        window.sonoEvalTracking.trackMilestone(milestoneName, data);
    }

    // Show contextual achievement
    showContextualAchievement(milestoneName, data);
}

function showContextualAchievement(milestoneName, data) {
    const achievements = {
        'discovery_explored': 'You\'re exploring! This helps us personalize your experience.',
        'paths_selected': `Great choice! You've selected ${data.count || 0} focus area(s).`,
        'candidate_registered': 'Welcome! Your progress will be tracked.',
        'results_viewed': 'You\'ve completed an assessment! Check out your insights.',
    };

    const message = achievements[milestoneName];
    if (message && window.sonoEval && window.sonoEval.showSuccess) {
        window.sonoEval.showSuccess(message);
    }
}

// Form validation helpers
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validateRequired(fields) {
    let isValid = true;
    fields.forEach(field => {
        const input = document.querySelector(`[name="${field}"]`);
        if (input && !input.value.trim()) {
            input.style.borderColor = 'var(--error-color)';
            isValid = false;
        } else if (input) {
            input.style.borderColor = 'var(--border-color)';
        }
    });
    return isValid;
}

// Analytics tracking - integrated with tracking system
function trackEvent(category, action, label = null) {
    // Use the tracking system if available
    if (window.sonoEvalTracking && window.sonoEvalTracking.trackEvent) {
        window.sonoEvalTracking.trackEvent('custom', {
            category: category,
            action: action,
            label: label,
        });
    } else {
        // Fallback for compatibility
        console.log('Track:', category, action, label);
    }
}

// Error handling
function showError(message, details = null) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'info-box';
    errorDiv.setAttribute('role', 'alert');
    errorDiv.setAttribute('aria-live', 'assertive');
    errorDiv.style.background = '#FFEBEE';
    errorDiv.style.borderLeftColor = 'var(--error-color)';

    let detailsHtml = '';
    if (details) {
        if (typeof details === 'string') {
            detailsHtml = `<p style="margin-top: 0.5rem; font-size: 0.875rem; color: var(--text-secondary);">${details}</p>`;
        } else if (typeof details === 'object') {
            detailsHtml = `<p style="margin-top: 0.5rem; font-size: 0.875rem; color: var(--text-secondary);">${JSON.stringify(details, null, 2)}</p>`;
        }
    }

    errorDiv.innerHTML = `
        <p class="info-box-icon" aria-hidden="true">⚠️</p>
        <div class="info-box-content">
            <strong>Error:</strong> ${message}
            ${detailsHtml}
        </div>
    `;

    const container = document.querySelector('.mobile-content');
    if (container) {
        container.insertBefore(errorDiv, container.firstChild);
        // Scroll to error
        errorDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        // Remove after 8 seconds (longer for accessibility)
        setTimeout(() => {
            errorDiv.style.transition = 'opacity 0.3s';
            errorDiv.style.opacity = '0';
            setTimeout(() => errorDiv.remove(), 300);
        }, 8000);
    }
}

// Success message
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'info-box info-box-success';
    successDiv.setAttribute('role', 'status');
    successDiv.setAttribute('aria-live', 'polite');
    successDiv.innerHTML = `
        <p class="info-box-icon" aria-hidden="true">✓</p>
        <div class="info-box-content">
            ${message}
        </div>
    `;

    const container = document.querySelector('.mobile-content');
    if (container) {
        container.insertBefore(successDiv, container.firstChild);
        // Scroll to success message
        successDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        setTimeout(() => {
            successDiv.style.transition = 'opacity 0.3s';
            successDiv.style.opacity = '0';
            setTimeout(() => successDiv.remove(), 300);
        }, 3000);
    }
}

// Prevent double-tap zoom on iOS
let lastTouchEnd = 0;
document.addEventListener('touchend', function(event) {
    const now = Date.now();
    if (now - lastTouchEnd <= 300) {
        event.preventDefault();
    }
    lastTouchEnd = now;
}, false);

// Debounce helper
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Auto-save form data
function setupAutoSave(formId, storageKey) {
    const form = document.getElementById(formId);
    if (!form) return;

    // Load saved data
    const savedData = getFromSession(storageKey);
    if (savedData) {
        Object.entries(savedData).forEach(([name, value]) => {
            const input = form.querySelector(`[name="${name}"]`);
            if (input) {
                if (input.type === 'checkbox' || input.type === 'radio') {
                    input.checked = value;
                } else {
                    input.value = value;
                }
            }
        });
    }

    // Save on change
    const saveForm = debounce(() => {
        const formData = new FormData(form);
        const data = {};
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        saveToSession(storageKey, data);
    }, 500);

    form.addEventListener('input', saveForm);
    form.addEventListener('change', saveForm);
}

// Network status indicator
function checkNetworkStatus() {
    if (!navigator.onLine) {
        const banner = document.createElement('div');
        banner.id = 'offline-banner';
        banner.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: var(--error-color);
            color: white;
            padding: 0.5rem;
            text-align: center;
            font-size: 0.9rem;
            z-index: 10000;
        `;
        banner.textContent = '⚠️ You are offline. Some features may not work.';
        document.body.insertBefore(banner, document.body.firstChild);
    }
}

window.addEventListener('load', checkNetworkStatus);
window.addEventListener('online', () => {
    const banner = document.getElementById('offline-banner');
    if (banner) banner.remove();
});
window.addEventListener('offline', checkNetworkStatus);

// Track learning milestones
function trackMilestone(milestoneName, data = {}) {
    if (window.sonoEvalTracking && window.sonoEvalTracking.trackMilestone) {
        window.sonoEvalTracking.trackMilestone(milestoneName, data);
    }
}

// Track easter egg discoveries
function trackEasterEgg(eggName, discoveryMethod) {
    if (window.sonoEvalTracking && window.sonoEvalTracking.trackEasterEgg) {
        window.sonoEvalTracking.trackEasterEgg(eggName, discoveryMethod);
    }
}

// Export functions for use in other scripts
window.sonoEval = {
    saveToSession,
    getFromSession,
    updateProgress,
    validateEmail,
    validateRequired,
    trackEvent,
    trackMilestone,
    trackEasterEgg,
    showError,
    showSuccess,
    debounce,
    setupAutoSave
};
