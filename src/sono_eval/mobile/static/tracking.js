// Interaction Tracking System for Sono-Eval
// Tracks user interactions from first page load for personalization and analytics

(function() {
    'use strict';

    // Configuration
    const TRACKING_ENABLED = true;
    const BATCH_INTERVAL = 5000; // 5 seconds
    const MAX_QUEUE_SIZE = 50;
    const TRACKING_ENDPOINT = '/api/mobile/track';

    // Session management
    let sessionId = null;
    let candidateId = null;
    let pageStartTime = null;
    let maxScrollDepth = 0;
    let eventQueue = [];
    let batchTimer = null;

    // Initialize session
    function initSession() {
        // Get or create session ID
        sessionId = localStorage.getItem('sono_eval_session_id');
        if (!sessionId) {
            sessionId = 'anon_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('sono_eval_session_id', sessionId);
        }

        // Get candidate ID if available
        candidateId = sessionStorage.getItem('candidate_id') || localStorage.getItem('candidate_id') || null;

        // Track page view
        pageStartTime = Date.now();
        trackEvent('page_view', {
            page: getCurrentPage(),
            referrer: document.referrer || 'direct',
            user_agent: navigator.userAgent.substring(0, 100), // Truncate for privacy
        });

        // Setup tracking listeners
        setupTrackingListeners();
        startBatchTimer();
    }

    // Get current page identifier
    function getCurrentPage() {
        const path = window.location.pathname;
        if (path.includes('/mobile/')) {
            const page = path.split('/mobile/')[1] || 'index';
            return page.split('?')[0]; // Remove query params
        }
        return 'unknown';
    }

    // Setup event listeners
    function setupTrackingListeners() {
        // Track clicks
        document.addEventListener('click', function(e) {
            // Skip tracking on navigation links and buttons (handled separately)
            if (e.target.tagName === 'A' || e.target.tagName === 'BUTTON') {
                return;
            }

            trackEvent('click', {
                element: e.target.tagName,
                element_id: e.target.id || null,
                element_class: e.target.className || null,
                text: (e.target.textContent || '').substring(0, 50),
                x: e.clientX,
                y: e.clientY,
            });
        }, true); // Use capture phase

        // Track scroll depth
        let scrollTracking = debounce(function() {
            const scrollPercent = Math.round(
                (window.scrollY / Math.max(document.body.scrollHeight - window.innerHeight, 1)) * 100
            );
            if (scrollPercent > maxScrollDepth) {
                maxScrollDepth = scrollPercent;
                trackEvent('scroll', {
                    depth: scrollPercent,
                });
            }
        }, 500);

        window.addEventListener('scroll', scrollTracking, { passive: true });

        // Track form interactions
        document.addEventListener('input', function(e) {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
                trackEvent('form_input', {
                    field_name: e.target.name || e.target.id || 'unknown',
                    field_type: e.target.type || 'text',
                    has_value: !!e.target.value,
                });
            }
        }, true);

        document.addEventListener('change', function(e) {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') {
                trackEvent('form_change', {
                    field_name: e.target.name || e.target.id || 'unknown',
                    field_type: e.target.type || 'select',
                });
            }
        }, true);

        // Track focus events (for accessibility and engagement)
        document.addEventListener('focusin', function(e) {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
                trackEvent('focus', {
                    field_name: e.target.name || e.target.id || 'unknown',
                });
            }
        }, true);

        // Track page exit
        window.addEventListener('beforeunload', function() {
            const timeOnPage = Date.now() - pageStartTime;
            trackEvent('page_exit', {
                time_on_page: timeOnPage,
                max_scroll_depth: maxScrollDepth,
            }, true); // Send immediately
        });

        // Track visibility changes (tab switching)
        document.addEventListener('visibilitychange', function() {
            trackEvent('visibility_change', {
                hidden: document.hidden,
            });
        });
    }

    // Track an event
    function trackEvent(eventType, data = {}, immediate = false) {
        if (!TRACKING_ENABLED) return;

        const event = {
            event_type: eventType,
            session_id: sessionId,
            candidate_id: candidateId,
            page: getCurrentPage(),
            timestamp: new Date().toISOString(),
            data: data,
        };

        eventQueue.push(event);

        // Prevent queue overflow
        if (eventQueue.length > MAX_QUEUE_SIZE) {
            eventQueue.shift(); // Remove oldest
        }

        if (immediate) {
            flushQueue();
        }
    }

    // Start batch timer
    function startBatchTimer() {
        if (batchTimer) return;
        batchTimer = setInterval(flushQueue, BATCH_INTERVAL);
    }

    // Flush event queue to server
    function flushQueue() {
        if (eventQueue.length === 0 || !navigator.onLine) return;

        const events = eventQueue.splice(0); // Clear queue
        const payload = {
            events: events,
        };

        // Send to server
        fetch(TRACKING_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
            keepalive: true, // Important for beforeunload events
        }).catch(function(error) {
            // If send fails, re-queue events (up to limit)
            console.warn('Tracking failed, re-queuing events:', error);
            eventQueue.unshift(...events.slice(-MAX_QUEUE_SIZE));
        });
    }

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

    // Update candidate ID when provided
    function updateCandidateId(newCandidateId) {
        if (newCandidateId && newCandidateId !== candidateId) {
            candidateId = newCandidateId;
            trackEvent('candidate_id_linked', {
                previous_session: sessionId,
            });
        }
    }

    // Track easter egg discovery
    function trackEasterEgg(eggName, discoveryMethod) {
        trackEvent('easter_egg_discovered', {
            egg_name: eggName,
            discovery_method: discoveryMethod,
        }, true); // Send immediately for important events
    }

    // Track learning milestone
    function trackMilestone(milestoneName, data = {}) {
        trackEvent('milestone', {
            milestone: milestoneName,
            ...data,
        });
    }

    // Public API
    window.sonoEvalTracking = {
        trackEvent: trackEvent,
        trackEasterEgg: trackEasterEgg,
        trackMilestone: trackMilestone,
        updateCandidateId: updateCandidateId,
        getSessionId: () => sessionId,
        getCandidateId: () => candidateId,
        flush: flushQueue,
    };

    // Initialize on page load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSession);
    } else {
        initSession();
    }

    // Handle online/offline events
    window.addEventListener('online', function() {
        trackEvent('connection_restored');
        flushQueue();
    });

    window.addEventListener('offline', function() {
        trackEvent('connection_lost');
    });
})();
