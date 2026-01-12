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

// Progress tracking
function updateProgress(current, total) {
    const progressBar = document.querySelector('.progress-fill');
    if (progressBar) {
        const percentage = (current / total) * 100;
        progressBar.style.width = `${percentage}%`;
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

// Analytics tracking (placeholder)
function trackEvent(category, action, label = null) {
    console.log('Track:', category, action, label);
    // In production, integrate with analytics service
    // e.g., gtag('event', action, { category, label });
}

// Error handling
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'info-box';
    errorDiv.style.background = '#FFEBEE';
    errorDiv.style.borderLeftColor = 'var(--error-color)';
    errorDiv.innerHTML = `
        <p class="info-box-icon">⚠️</p>
        <div class="info-box-content">
            <strong>Error:</strong> ${message}
        </div>
    `;

    const container = document.querySelector('.mobile-content');
    if (container) {
        container.insertBefore(errorDiv, container.firstChild);
        setTimeout(() => errorDiv.remove(), 5000);
    }
}

// Success message
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'info-box info-box-success';
    successDiv.innerHTML = `
        <p class="info-box-icon">✓</p>
        <div class="info-box-content">
            ${message}
        </div>
    `;

    const container = document.querySelector('.mobile-content');
    if (container) {
        container.insertBefore(successDiv, container.firstChild);
        setTimeout(() => successDiv.remove(), 3000);
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

// Export functions for use in other scripts
window.sonoEval = {
    saveToSession,
    getFromSession,
    updateProgress,
    validateEmail,
    validateRequired,
    trackEvent,
    showError,
    showSuccess,
    debounce,
    setupAutoSave
};
