# Sono-Eval - Roadmap & TODOs

**Last Updated**: 2026-01-24
**Single Source of Truth**: This file contains all TODOs, planned features, and roadmap items.

**Note**: This consolidates high-priority items. See `Documentation/Governance/IMPLEMENTATION_GUIDE.md` for detailed implementation guides and code examples.

---

## ✅ Recently Completed

- **v0.3.0 Web UI**: Full frontend implementation with Next.js, Dashboard, and Visualization. (2026-01-24)
- **Security Hardening**: Authentication, Rate Limiting, Input Validation, CORS. (2026-01-23)
- **ML Assessment Engine**: Hybrid scoring model with CodeBERT. (2026-01-23)
- **Production Setup**: Docker, CI/CD, Monitoring basics. (2026-01-23)

---

## 🚀 Upcoming Releases

### 📦 v0.4.0: Scalability & Backend Integration

**Focus**: Performance, background processing, and full backend-frontend integration.
**Status**: 🚧 Preparation

#### 1. Batch Assessment Processing

- [ ] **API Endpoints**: `/api/v1/assessments/batch` for bulk submission.
- [ ] **Celery Tasks**: Async workers for processing large batches without timeouts.
- [ ] **State Management**: Tracking batch progress and partial failures.

#### 2. Caching Layer (Redis)

- [ ] **Assessment Caching**: Cache common assessment results and ML model outputs.
- [ ] **Rate Limiting Backend**: Move from memory to Redis for distributed limits.
- [ ] **Session Store**: Redis-backed session management for scale.

#### 3. Real-time Updates

- [ ] **WebSocket Integration**: Live progress updates for batch jobs on the frontend.

---

### 🧪 v0.5.0: Beta Candidate

**Focus**: User experience polish, advanced reporting, and stability testing.
**Status**: 📝 Planned

#### 1. Advanced Reporting

- [ ] **PDF Export**: Generate professional PDF reports of assessments.
- [ ] **Deep Analytics**: Advanced filtering and trend analysis views.

#### 2. Load Testing & Stability

- [ ] **Load Testing**: Locust tests simulating 100+ concurrent users.
- [ ] **Performance Tuning**: DB indexing and query optimization based on load test data.

#### 3. User Acceptance

- [ ] **Beta Testing Program**: Internal rollout to trusted users.
- [ ] **Feedback Loop**: In-app feedback mechanism.

#### 4. Documentation

- [ ] **Enhanced API Docs**: Comprehensive examples and tutorials.
- [ ] **User Guides**: Updated for Web UI workflows.

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

## 📝 Notes

- **Detailed Implementation Guides**: See `Documentation/Governance/IMPLEMENTATION_GUIDE.md`
- **Current Version**: 0.3.0 (Web UI implemented)
- **Target**: Production-ready 1.0.0
- **Changelog**: See `CHANGELOG.md` for release history
- **Documentation**: See `Documentation/README.md` for all documentation

---

## 🔄 How to Update This File

1. When starting work on a TODO, change status from `📝 TODO` to `🚧 In Progress`
2. When completing, move to "Recently Completed" section and mark as `✅`
3. Add new TODOs with appropriate priority and estimated effort
4. Update "Last Updated" date
5. Keep items organized by priority and category
