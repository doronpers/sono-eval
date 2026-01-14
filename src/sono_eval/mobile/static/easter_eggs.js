// Easter Eggs & Speakeasy Discoveries for Sono-Eval
// Value-driven hidden features that reward exploration

(function() {
    'use strict';

    // Track discovered easter eggs
    const discoveredEggs = JSON.parse(localStorage.getItem('sono_eval_easter_eggs') || '[]');
    const eggPatterns = [];
    let konamiSequence = [];
    const konamiCode = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];

    // Easter egg definitions
    const easterEggs = {
        'konami_code': {
            name: 'Expert Mode',
            description: 'Unlocks advanced metrics and comparison tools',
            method: 'keyboard',
            unlock: function() {
                unlockFeature('expert_mode', 'Konami Code');
            }
        },
        'triple_click_logo': {
            name: 'Keyboard Shortcuts',
            description: 'Reveals comprehensive keyboard shortcuts cheat sheet',
            method: 'click',
            unlock: function() {
                unlockFeature('keyboard_shortcuts', 'Triple-click on logo');
            }
        },
        'insights_url': {
            name: 'Insights Dashboard',
            description: 'Unlocks hidden insights dashboard with trend analysis',
            method: 'url',
            unlock: function() {
                unlockFeature('insights_dashboard', 'URL pattern');
            }
        },
        'deep_dive_comment': {
            name: 'Pattern Recognition',
            description: 'Triggers bonus pattern recognition analysis',
            method: 'code',
            unlock: function() {
                unlockFeature('pattern_recognition', 'Code comment');
            }
        },
        'all_paths_complete': {
            name: 'Full Profile Analysis',
            description: 'Unlocks cross-path insights and comparison',
            method: 'achievement',
            unlock: function() {
                unlockFeature('full_profile', 'Completed all paths');
            }
        }
    };

    // Track click patterns on logo
    let logoClickCount = 0;
    let logoClickTimer = null;

    // Initialize easter egg detection
    function initEasterEggs() {
        // Konami code detection
        document.addEventListener('keydown', function(e) {
            konamiSequence.push(e.key);
            if (konamiSequence.length > konamiCode.length) {
                konamiSequence.shift();
            }
            
            if (konamiSequence.join(',') === konamiCode.join(',')) {
                triggerEasterEgg('konami_code');
                konamiSequence = [];
            }
        });

        // Triple-click logo detection
        const logo = document.querySelector('.logo');
        if (logo) {
            logo.addEventListener('click', function() {
                logoClickCount++;
                clearTimeout(logoClickTimer);
                
                if (logoClickCount === 3) {
                    triggerEasterEgg('triple_click_logo');
                    logoClickCount = 0;
                } else {
                    logoClickTimer = setTimeout(() => {
                        logoClickCount = 0;
                    }, 1000);
                }
            });
        }

        // URL pattern detection
        if (window.location.search.includes('insights') || window.location.pathname.includes('insights')) {
            triggerEasterEgg('insights_url');
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            // ? for help
            if (e.key === '?' && !e.ctrlKey && !e.metaKey && !e.altKey) {
                e.preventDefault();
                showKeyboardShortcuts();
            }
            
            // d for debug mode
            if (e.key === 'd' && e.ctrlKey && !e.metaKey && !e.altKey) {
                e.preventDefault();
                toggleDebugMode();
            }
        });

        // Right-click on scores (for results page)
        document.addEventListener('contextmenu', function(e) {
            if (e.target.classList.contains('path-score-badge') || e.target.closest('.score-number')) {
                e.preventDefault();
                showScoreExplanation(e.target);
            }
        });
    }

    // Trigger an easter egg
    function triggerEasterEgg(eggId) {
        const egg = easterEggs[eggId];
        if (!egg || discoveredEggs.includes(eggId)) return;

        discoveredEggs.push(eggId);
        localStorage.setItem('sono_eval_easter_eggs', JSON.stringify(discoveredEggs));

        // Track discovery
        if (window.sonoEvalTracking && window.sonoEvalTracking.trackEasterEgg) {
            window.sonoEvalTracking.trackEasterEgg(egg.name, egg.method);
        }

        // Unlock feature
        if (egg.unlock) {
            egg.unlock();
        }

        // Show discovery notification
        showDiscoveryNotification(egg.name, egg.description);
    }

    // Unlock a feature
    function unlockFeature(featureName, discoveryMethod) {
        const unlocked = JSON.parse(localStorage.getItem('sono_eval_unlocked_features') || '[]');
        if (!unlocked.includes(featureName)) {
            unlocked.push(featureName);
            localStorage.setItem('sono_eval_unlocked_features', JSON.stringify(unlocked));
        }
    }

    // Show discovery notification
    function showDiscoveryNotification(name, description) {
        const notification = document.createElement('div');
        notification.className = 'easter-egg-notification';
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-icon">🎉</span>
                <div class="notification-text">
                    <strong>Discovery Unlocked: ${name}</strong>
                    <p>${description}</p>
                </div>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => notification.classList.add('show'), 10);
        
        // Remove after 5 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    }

    // Show keyboard shortcuts
    function showKeyboardShortcuts() {
        const shortcuts = [
            { key: '?', desc: 'Show keyboard shortcuts' },
            { key: 'Ctrl+D', desc: 'Toggle debug mode' },
            { key: 'Esc', desc: 'Close modals/dialogs' },
            { key: 'Enter', desc: 'Submit forms' },
        ];

        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.style.display = 'flex';
        modal.innerHTML = `
            <div class="modal-content">
                <button class="modal-close" onclick="this.closest('.modal').remove()">&times;</button>
                <div class="modal-body">
                    <h3>Keyboard Shortcuts</h3>
                    <ul class="shortcuts-list">
                        ${shortcuts.map(s => `
                            <li>
                                <kbd>${s.key}</kbd>
                                <span>${s.desc}</span>
                            </li>
                        `).join('')}
                    </ul>
                    <button class="primary-button" onclick="this.closest('.modal').remove()">Got it!</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Close on outside click
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.remove();
            }
        });
    }

    // Toggle debug mode
    function toggleDebugMode() {
        const isDebug = localStorage.getItem('sono_eval_debug_mode') === 'true';
        localStorage.setItem('sono_eval_debug_mode', (!isDebug).toString());
        
        if (!isDebug) {
            showDiscoveryNotification('Debug Mode', 'Debug information is now visible. Check console for details.');
        }
    }

    // Show score explanation
    function showScoreExplanation(element) {
        const score = element.textContent || element.closest('.path-score-badge')?.textContent;
        if (!score) return;

        const explanation = `This score is calculated based on multiple factors including code quality, problem-solving approach, and best practices. Each path evaluates different aspects of your work.`;
        
        if (window.sonoEval && window.sonoEval.showSuccess) {
            window.sonoEval.showSuccess(`<strong>Score Explanation:</strong><br>${explanation}`);
        } else {
            alert(`Score Explanation: ${explanation}`);
        }
    }

    // Check for achievement-based easter eggs
    function checkAchievements() {
        // Check if all paths completed
        const completedPaths = JSON.parse(sessionStorage.getItem('completed_paths') || '[]');
        const allPaths = ['technical', 'design', 'collaboration', 'problem_solving'];
        
        if (allPaths.every(p => completedPaths.includes(p))) {
            triggerEasterEgg('all_paths_complete');
        }
    }

    // Public API
    window.sonoEvalEasterEggs = {
        trigger: triggerEasterEgg,
        checkAchievements: checkAchievements,
        isUnlocked: function(featureName) {
            const unlocked = JSON.parse(localStorage.getItem('sono_eval_unlocked_features') || '[]');
            return unlocked.includes(featureName);
        },
        getDiscovered: function() {
            return [...discoveredEggs];
        }
    };

    // Initialize on page load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initEasterEggs);
    } else {
        initEasterEggs();
    }

    // Check achievements periodically
    setInterval(checkAchievements, 2000);
})();
