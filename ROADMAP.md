# Sono-Eval - Roadmap & TODOs

**Last Updated**: 2026-01-16  
**Single Source of Truth**: This file contains all TODOs, planned features, and roadmap items.

**Note**: This consolidates items from `documentation/Governance/IMPROVEMENT_ROADMAP.md`. See that file for detailed implementation guides and code examples.

---

## ✅ Recently Completed

*No completed items to report yet.*

---

## 🔴 High Priority - Critical (Before Any Public Use)

### Security Hardening (2-4 weeks)

#### 1. Authentication System

- **Status**: 📝 TODO
- **Description**: Implement OAuth2 authentication, API key support, JWT tokens
- **Estimated Effort**: 1-2 weeks
- **Details**: See `documentation/Governance/IMPROVEMENT_ROADMAP.md` section "Security Hardening"

#### 2. Rate Limiting

- **Status**: 📝 TODO
- **Description**: Add rate limiting with Redis backend
- **Estimated Effort**: 1 week
- **Details**: See `documentation/Governance/IMPROVEMENT_ROADMAP.md`

#### 3. Input Validation & Sanitization

- **Status**: 📝 TODO
- **Description**: Comprehensive Pydantic validators, file upload validation
- **Estimated Effort**: 1-2 weeks
- **Details**: See `documentation/Governance/IMPROVEMENT_ROADMAP.md`

#### 4. CORS Enforcement

- **Status**: 📝 TODO
- **Description**: Remove wildcard CORS in production
- **Estimated Effort**: 1 week
- **Details**: See `documentation/Governance/IMPROVEMENT_ROADMAP.md`

#### 5. Secret Validation

- **Status**: 📝 TODO
- **Description**: Add startup validation for default secrets
- **Estimated Effort**: 1 week
- **Details**: See `documentation/Governance/IMPROVEMENT_ROADMAP.md`

#### 6. Security Headers

- **Status**: 📝 TODO
- **Description**: Add HSTS, X-Content-Type-Options, CSP headers
- **Estimated Effort**: 1 week
- **Details**: See `documentation/Governance/IMPROVEMENT_ROADMAP.md`

#### 7. Audit Logging

- **Status**: 📝 TODO
- **Description**: Log all authentication, authorization, and data modifications
- **Estimated Effort**: 1-2 weeks
- **Details**: See `documentation/Governance/IMPROVEMENT_ROADMAP.md`

#### 8. Security Audit

- **Status**: 📝 TODO
- **Description**: Run OWASP ZAP, Bandit, Safety scans
- **Estimated Effort**: 1-2 weeks
- **Details**: See `documentation/Governance/IMPROVEMENT_ROADMAP.md`

---

## 🟡 Medium Priority - Core Functionality (Release 0.2.0)

### Real ML Assessment Engine (6-8 weeks)

#### 9. Model Selection & Training

- **Status**: 📝 TODO
- **Description**: Select architecture, collect training data, train baseline model
- **Estimated Effort**: 2-4 weeks
- **Details**: See `documentation/Governance/IMPROVEMENT_ROADMAP.md` section "Real ML Assessment Engine"

#### 10. Assessment Logic Implementation

- **Status**: 📝 TODO
- **Description**: Replace placeholder scoring, implement model inference
- **Estimated Effort**: 2-4 weeks
- **Details**: See `documentation/Governance/IMPROVEMENT_ROADMAP.md`

#### 11. Model Evaluation

- **Status**: 📝 TODO
- **Description**: Evaluate against test set, measure accuracy/precision/recall
- **Estimated Effort**: 1 week
- **Details**: See `documentation/Governance/IMPROVEMENT_ROADMAP.md`

### Comprehensive Testing (Weeks 5-6)

#### 12. API Integration Tests

- **Status**: 📝 TODO
- **Description**: Test all endpoints, error conditions, authentication
- **Estimated Effort**: 1-2 weeks
- **Details**: See `documentation/Governance/IMPROVEMENT_ROADMAP.md`

#### 13. Load Testing

- **Status**: 📝 TODO
- **Description**: Test with realistic workloads, identify bottlenecks
- **Estimated Effort**: 1 week
- **Details**: See `documentation/Governance/IMPROVEMENT_ROADMAP.md`

---

## 🟢 Low Priority - Future Enhancements

### Documentation

#### 14. Enhanced API Documentation

- **Status**: 📝 TODO
- **Description**: Expand API reference with more examples
- **Estimated Effort**: 2-3 days

### Features

#### 15. Advanced Assessment Features

- **Status**: 📝 TODO
- **Description**: Additional assessment paths, custom scoring
- **Estimated Effort**: 2-3 weeks

---

## 📊 Progress Summary

- **Completed**: 0 items
- **High Priority (Critical)**: 8 items
- **Medium Priority (Core)**: 5 items
- **Low Priority (Future)**: 2 items

**Total Estimated Time to v1.0.0**: 12-16 weeks (with dedicated development team)

---

## 📝 Notes

- **Detailed Roadmap**: See `documentation/Governance/IMPROVEMENT_ROADMAP.md` for comprehensive implementation guides
- **Version Target**: 0.1.0 → 1.0.0
- **Status**: Planning Phase
- **Changelog**: See `CHANGELOG.md` for release history

---

## 🔄 How to Update This File

1. When starting work on a TODO, change status from `📝 TODO` to `🚧 In Progress`
2. When completing, move to "Recently Completed" section and mark as `✅`
3. Add new TODOs with appropriate priority and estimated effort
4. Update "Last Updated" date
5. Keep items organized by priority and category
