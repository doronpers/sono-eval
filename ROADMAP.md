# Sono-Eval - Roadmap & TODOs

**Last Updated**: 2026-01-24
**Single Source of Truth**: This file contains all TODOs, planned features, and roadmap items.

**Note**: This consolidates high-priority items. See `Documentation/Governance/IMPLEMENTATION_GUIDE.md` for detailed implementation guides and code examples.

---

## ✅ Recently Completed

- **v0.4.0 Batch Processing**: Complete batch assessment API, Celery tasks, state management, and frontend. (2026-01-24)
- **v0.3.0 Web UI**: Full frontend implementation with Next.js, Dashboard, and Visualization. (2026-01-24)
- **Security Hardening**: Authentication, Rate Limiting, Input Validation, CORS. (2026-01-23)
- **ML Assessment Engine**: Hybrid scoring model with CodeBERT. (2026-01-23)
- **Production Setup**: Docker, CI/CD, Monitoring basics. (2026-01-23)

---

## 🚀 Upcoming Releases

### 📦 v0.4.0: Scalability & Backend Integration

**Focus**: Performance, background processing, and full backend-frontend integration.
**Status**: 🚧 33% Complete (1 of 3 major features done)

#### 1. Batch Assessment Processing ✅ COMPLETE

- [x] **API Endpoints**: `/api/v1/assessments/batch/` for bulk submission. ✅ (2026-01-24)
- [x] **Celery Tasks**: Async workers for processing large batches without timeouts. ✅ (2026-01-24)
- [x] **State Management**: Tracking batch progress and partial failures. ✅ (2026-01-24)
- [x] **Frontend**: Batch upload page with progress tracking. ✅ (2026-01-24)

**Files**:
- `src/sono_eval/api/routes/batch.py` - Batch API routes
- `src/sono_eval/tasks/assessment.py` - Celery task implementation
- `frontend/app/batch/page.tsx` - Frontend batch page
- `frontend/types/assessment.ts` - Type definitions

#### 2. Caching Layer (Redis)

**Current State**:
- Rate limiter already has Redis support implemented (`RedisRateLimiterState` class exists in `src/sono_eval/middleware/rate_limiter.py`)
- Cache middleware is in-memory only (`src/sono_eval/middleware/cache.py`)
- Rate limiting currently uses memory backend by default

**Tasks**:

- [ ] **Enable Redis Rate Limiting**
  - **Complexity**: Low (implementation exists, needs configuration)
  - **Recommended Models**: 1. GPT-5.1-Codex, 2. Claude Sonnet 4.5, 3. Gemini 3 Flash
  - **Files**: `src/sono_eval/middleware/rate_limiter.py`, `src/sono_eval/api/main.py`
  - **Changes**: Update `RateLimitMiddleware` initialization to use Redis when available, set `RATE_LIMIT_REDIS_URL` environment variable handling, verify Redis connection in startup, add fallback to memory if Redis unavailable
  - **Testing**: Integration tests for Redis rate limiting, fallback behavior

- [ ] **Migrate Cache to Redis**
  - **Complexity**: Medium (requires refactoring cache decorator)
  - **Recommended Models**: 1. GPT-5.1-Codex, 2. Claude Sonnet 4.5, 3. Gemini 3 Pro
  - **Files**: `src/sono_eval/middleware/cache.py`
  - **Changes**: Create `RedisCache` class similar to `RedisRateLimiterState` pattern, refactor `@cached` decorator to support Redis backend, add cache key management and TTL handling, implement cache invalidation patterns, add cache statistics endpoint
  - **Testing**: Unit tests for Redis cache operations, TTL expiration, invalidation

- [ ] **Assessment Result Caching**
  - **Complexity**: Medium (requires integration with assessment engine)
  - **Recommended Models**: 1. GPT-5.1-Codex, 2. Claude Sonnet 4.5, 3. Gemini 3 Pro
  - **Files**: `src/sono_eval/assessment/engine.py`, `src/sono_eval/api/main.py`
  - **Changes**: Add cache key generation based on assessment input hash, cache assessment results with configurable TTL, cache ML model outputs separately, implement cache warming for common assessments, add cache hit/miss metrics
  - **Testing**: Integration tests for cached assessments, cache invalidation on updates

- [ ] **Session Store (Redis)**
  - **Complexity**: Medium-High (new feature)
  - **Recommended Models**: 1. Claude Opus 4.5, 2. GPT-5.2-Codex, 3. GPT-5.1-Codex-Max
  - **Files**: New `src/sono_eval/middleware/session.py` or extend existing session management
  - **Changes**: Implement Redis-backed session storage, session key management and expiration, session data serialization/deserialization, integration with authentication system
  - **Testing**: Session creation, retrieval, expiration, concurrent access

#### 3. Real-time Updates

**Current State**: No WebSocket implementation exists. Batch progress currently uses polling.

- [ ] **WebSocket Infrastructure**
  - **Complexity**: Medium-High (new feature)
  - **Recommended Models**: 1. Claude Opus 4.5, 2. GPT-5.2-Codex, 3. GPT-5.1-Codex-Max
  - **Files**: New `src/sono_eval/api/websocket.py`, `src/sono_eval/api/main.py`
  - **Changes**: Add FastAPI WebSocket endpoint for batch progress, implement connection management (connection pool, cleanup), add WebSocket authentication (JWT token validation), implement heartbeat/ping-pong for connection health, add reconnection handling on client side
  - **Dependencies**: `python-socketio` or native FastAPI WebSocket support
  - **Testing**: WebSocket connection, message delivery, reconnection, authentication

- [ ] **Batch Progress Broadcasting**
  - **Complexity**: Medium (integration with existing batch system)
  - **Recommended Models**: 1. GPT-5.1-Codex, 2. Claude Sonnet 4.5, 3. Gemini 3 Pro
  - **Files**: `src/sono_eval/api/routes/batch.py`, `src/sono_eval/tasks/assessment.py`
  - **Changes**: Emit progress updates from Celery tasks, use Redis pub/sub or in-memory event bus for progress events, map batch_id to WebSocket connections, broadcast progress updates to connected clients, handle multiple clients watching same batch
  - **Testing**: Progress updates delivered, multiple clients, batch completion events

- [ ] **Frontend WebSocket Integration**
  - **Complexity**: Medium (React WebSocket client)
  - **Recommended Models**: 1. Cursor Composer 2, 2. Claude Sonnet 4.5, 3. GPT-5.1-Codex
  - **Files**: `frontend/app/batch/page.tsx`, new `frontend/lib/websocket.ts`
  - **Changes**: Create WebSocket client hook (`useWebSocket`), replace polling with WebSocket connection, handle connection state (connecting, connected, disconnected), implement automatic reconnection, update progress UI in real-time
  - **Testing**: WebSocket connection, message handling, UI updates, reconnection

---

### 🧪 v0.5.0: Beta Candidate

**Focus**: User experience polish, advanced reporting, and stability testing.
**Status**: 📝 Planned (0% complete)

#### 1. Advanced Reporting

- [ ] **PDF Export Enhancement**
  - **Complexity**: Medium (enhancement of existing implementation)
  - **Recommended Models**: 1. GPT-5.1-Codex, 2. Claude Sonnet 4.5, 3. Gemini 3 Pro
  - **Current**: Basic PDF generator exists at `src/sono_eval/reporting/pdf_generator.py`
  - **Files**: `src/sono_eval/reporting/pdf_generator.py`, `src/sono_eval/api/main.py`
  - **Enhancements Needed**: Add branding/logo support, enhanced styling and layout, multi-page support for long reports, charts/graphs integration (score visualizations), executive summary section, detailed path breakdowns, micro-motive visualizations, export options (full report vs summary)
  - **Testing**: PDF generation, layout, multi-page handling, file download

- [ ] **Deep Analytics**
  - **Complexity**: High (new feature with complex data processing)
  - **Recommended Models**: 1. Claude Opus 4.5, 2. GPT-5.2-Codex, 3. GPT-5.1-Codex-Max
  - **Files**: `src/sono_eval/assessment/dashboard.py`, `frontend/app/analytics/page.tsx`
  - **Features**: Advanced filtering (date range, score range, path type, candidate attributes), trend analysis (score trends over time, path performance trends), comparative analytics (compare candidates, compare time periods), statistical summaries (mean, median, percentiles), export analytics data (CSV, JSON)
  - **Backend**: New analytics endpoints, aggregation queries
  - **Frontend**: Enhanced analytics dashboard with filters and visualizations
  - **Testing**: Filtering logic, trend calculations, data export

#### 2. Load Testing & Stability

- [ ] **Load Testing Implementation**
  - **Complexity**: Medium (Locust is already installed)
  - **Recommended Models**: 1. GPT-5.1-Codex, 2. Claude Sonnet 4.5, 3. Gemini 3 Pro
  - **Files**: `tests/load/locustfile.py` (exists but may need updates)
  - **Tasks**: Create comprehensive load test scenarios, test assessment creation (single and batch), test API endpoints under load, simulate 100+ concurrent users, test rate limiting under load, test database performance, test Redis caching under load, generate load test reports
  - **Targets**: 100+ concurrent users, 1000+ requests/minute, <500ms p95 latency
  - **Testing**: Run load tests, analyze results, identify bottlenecks

- [ ] **Performance Tuning**
  - **Complexity**: Medium-High (requires profiling and optimization)
  - **Recommended Models**: 1. GPT-5.1-Codex-Max, 2. Claude Opus 4.5, 3. GPT-5.2-Codex
  - **Files**: Database models, query code, API endpoints
  - **Tasks**: Profile database queries (identify N+1 queries, missing indexes), add database indexes based on load test findings, optimize slow API endpoints, optimize assessment engine performance, cache optimization (TTL tuning, cache key strategy), connection pooling optimization, query result pagination
  - **Testing**: Performance benchmarks, load test improvements

#### 3. User Acceptance

- [ ] **Beta Testing Program**
  - **Complexity**: Low-Medium (organizational, not technical)
  - **Recommended Models**: 1. Claude Sonnet 4.5, 2. Gemini 3 Flash, 3. Claude Haiku 4.5
  - **Tasks**: Define beta user criteria and selection process, create beta user onboarding materials, set up beta feedback collection mechanism, create beta user communication channel, define beta testing scope and goals, track beta user engagement and feedback

- [ ] **Feedback Loop**
  - **Complexity**: Medium (new feature)
  - **Files**: New `src/sono_eval/api/routes/feedback.py`, `frontend/components/Feedback/`
  - **Features**: In-app feedback form (rating, comments, bug reports), feedback submission endpoint, feedback dashboard (admin view), feedback categorization and prioritization, integration with issue tracking (optional)
  - **Testing**: Feedback submission, storage, retrieval, admin dashboard

#### 4. Documentation

- [ ] **Enhanced API Docs**
  - **Complexity**: Low-Medium (content creation)
  - **Recommended Models**: 1. Claude Sonnet 4.5, 2. GPT-5.1, 3. Gemini 3 Flash
  - **Files**: FastAPI auto-generated docs, new examples
  - **Tasks**: Add comprehensive request/response examples to all endpoints, create API usage tutorials, add authentication examples, add error handling examples, create API client examples (Python, JavaScript), add rate limiting documentation, document WebSocket API (when implemented)

- [ ] **User Guides**
  - **Complexity**: Low-Medium (content creation)
  - **Recommended Models**: 1. Claude Sonnet 4.5, 2. GPT-5.1, 3. Gemini 3 Flash
  - **Files**: `documentation/Guides/user-guide/`
  - **Tasks**: Update existing guides for Web UI workflows, create Web UI quick start guide, create batch processing guide, create analytics guide, create PDF export guide, update CLI guides if needed, create troubleshooting guide for common issues

---

### 🎉 v1.0.0: Production General Availability

**Focus**: Security assurance, community readiness, and public launch.
**Status**: 📝 Planned

#### 1. Final Security Assurance

- [ ] **Third-Party Audit**: External review of security posture.
- [ ] **Penetration Testing**: Targeted tests against production environment.

#### 2. Community Capabilities

- [ ] **Public Documentation Hub**: Final polish of all guides.
- [ ] **Contributing Guidelines**: Detailed workflows for community PRs.
- [ ] **Plugin System Architecture**: Initial design for community extensions.

#### 3. Launch

- [ ] **Marketing Assets**: Screenshots, demo videos.
- [ ] **Public Release**: GitHub release and announcement.

---

## Critical Requirements for Beta

### Test Coverage: 50% → 80%+

**Current Gap**: 1,490 statements need coverage (30% increase)

**Current Status**: 2,458 covered / 4,935 statements (50%)
**Target**: 3,948+ covered statements (80%)

**Priority Modules**:
1. CLI Commands (0% → 70%): +721 statements
   - `cli/commands/assess.py` - 0% (171 statements)
   - `cli/commands/candidate.py` - 0% (194 statements)
   - `cli/commands/session.py` - 0% (118 statements)
   - `cli/commands/setup.py` - 0% (174 statements)
   - `cli/commands/tag.py` - 0% (64 statements)
2. API Main (46% → 80%): +~100 statements
3. Dashboard (43% → 80%): +~50 statements
4. Other modules: +~619 statements

**Tasks**:
- [ ] Fix 10 test failures (9 in `test_formatters.py`, 1 in `test_pattern_checks.py`)
- [ ] Expand CLI command tests in `tests/test_cli_commands.py`
- [ ] Increase API coverage in `tests/test_api.py` and `tests/test_api_extended.py`
- [ ] Increase dashboard coverage in `tests/test_dashboard.py`

### Security Hardening

**Tasks**:
- [ ] **Enable Redis rate limiting** (implementation exists, needs configuration)
  - **Complexity**: Low
  - **Recommended Models**: 1. GPT-5.1-Codex, 2. Claude Sonnet 4.5, 3. Gemini 3 Flash
- [ ] **Complete third-party security audit**
  - **Complexity**: External dependency
  - **Recommended Models**: 1. Claude Opus 4.5, 2. GPT-5.2, 3. GPT-5.1-Codex-Max (Note: External audit recommended)
- [ ] **Fix all critical/high vulnerabilities** from security scans
  - **Complexity**: Variable
  - **Recommended Models**: 1. Claude Opus 4.5, 2. GPT-5.2, 3. GPT-5.1-Codex-Max
- [ ] **Enhance audit logging** for all sensitive operations
  - **Complexity**: Medium
  - **Recommended Models**: 1. GPT-5.1-Codex, 2. Claude Sonnet 4.5, 3. Gemini 3 Pro

### Performance & Stability

**Tasks**:
- [ ] **Establish performance baselines** (<500ms per assessment, 100+ assessments/minute)
  - **Complexity**: Low-Medium
  - **Recommended Models**: 1. Gemini 3 Flash, 2. Claude Sonnet 4.5, 3. Raptor mini
- [ ] **Complete load testing** (100+ concurrent users)
  - **Complexity**: Medium
  - **Recommended Models**: 1. GPT-5.1-Codex, 2. Claude Sonnet 4.5, 3. Gemini 3 Pro
- [ ] **Optimize based on load test findings**
  - **Complexity**: Medium-High
  - **Recommended Models**: 1. GPT-5.1-Codex-Max, 2. Claude Opus 4.5, 3. GPT-5.2-Codex

---

## Implementation Priority

### Phase 1: Quick Wins
1. Fix Test Failures - Low complexity, high impact (100% test pass rate)
2. Enable Redis Rate Limiting - Low complexity (code exists, needs config)
3. Add CLI Tests - Medium complexity, high coverage impact (+10%)

### Phase 2: Core v0.4.0 Completion
1. Migrate Cache to Redis - Medium complexity
2. Assessment Result Caching - Medium complexity
3. WebSocket Infrastructure - Medium-High complexity
4. Batch Progress Broadcasting - Medium complexity
5. Frontend WebSocket Integration - Medium complexity

### Phase 3: v0.5.0 Beta Features
1. PDF Export Enhancement - Medium complexity
2. Deep Analytics - High complexity
3. Load Testing - Medium complexity
4. Performance Tuning - Medium-High complexity
5. Documentation Updates - Low-Medium complexity

### Phase 4: Critical Beta Requirements
1. Test Coverage to 80% - Medium-High complexity (ongoing)
2. Security Audit - External dependency
3. Security Fixes - Variable complexity
4. Performance Benchmarking - Low-Medium complexity

---

## Dependencies and Prerequisites

### Technical Dependencies
- Redis server (for caching and rate limiting)
- WebSocket support (FastAPI native or python-socketio)
- Locust (already installed for load testing)
- ReportLab (already installed for PDF generation)

### External Dependencies
- Security audit vendor selection and scheduling
- Beta user recruitment and onboarding

### Infrastructure
- Redis availability and configuration
- Database performance tuning capabilities
- Load testing environment

---

## Risk Assessment

### High Risk Items
- **Test Coverage**: Large gap (30%) may take longer than expected
- **Security Audit**: External dependency, timeline not fully controllable
- **WebSocket Implementation**: New technology, may have unexpected complexity
- **Performance Tuning**: May reveal architectural issues requiring refactoring

### Medium Risk Items
- **Redis Migration**: Well-understood technology, but integration complexity
- **Load Testing**: May reveal scalability issues requiring infrastructure changes
- **Deep Analytics**: Complex data processing, may require database schema changes

### Low Risk Items
- **Test Failure Fixes**: Straightforward data structure alignment
- **PDF Export Enhancement**: Incremental improvement of existing code
- **Documentation**: Content creation, low technical risk

---

## Success Criteria

### Beta Release Readiness
- [ ] All test failures fixed (10 tests)
- [ ] Test coverage ≥80% (currently 50%)
- [ ] Security audit completed and critical issues fixed
- [ ] Load testing completed (100+ concurrent users)
- [ ] Performance benchmarks met (<500ms per assessment)
- [ ] Redis caching operational
- [ ] WebSocket real-time updates working
- [ ] PDF export enhanced and tested
- [ ] Documentation updated for Web UI
- [ ] Beta testing program established

### Quality Gates
- All tests passing
- No critical security vulnerabilities
- Performance targets met
- Documentation complete
- Production deployment guide updated

---

## Notes

- **Current Version**: 0.3.0 (Web UI implemented)
- **Next Milestone**: v0.4.0 (Scalability)
- **Beta Target**: v0.5.0
- **Production Target**: v1.0.0

- **Rate Limiting**: Redis support already implemented in `src/sono_eval/middleware/rate_limiter.py`, just needs to be enabled via environment variables.

- **Test Coverage**: Biggest gap is CLI commands (0% coverage). Existing test file (`test_cli_commands.py`) exists but may not be running or may need expansion.

- **Batch Processing**: Completed 2026-01-24, demonstrates implementation velocity for similar features.

- **Similar Implementations**: Production hardening (2026-01-22) and batch processing (2026-01-24) provide reference for complexity of middleware and async task implementations.

---

## 🔄 How to Update This File

1. When starting work on a TODO, change status from `📝 TODO` to `🚧 In Progress`
2. When completing, move to "Recently Completed" section and mark as `✅`
3. Add new TODOs with complexity indicators (Low, Medium, High) rather than time estimates
4. Update "Last Updated" date
5. Keep items organized by priority and category
6. Focus on dependencies and prerequisites rather than timelines

---

**Detailed Implementation Guides**: See `Documentation/Governance/IMPLEMENTATION_GUIDE.md`  
**Changelog**: See `CHANGELOG.md` for release history  
**Documentation**: See `Documentation/README.md` for all documentation
