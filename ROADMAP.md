# Sono-Eval - Roadmap & TODOs

**Last Updated**: 2026-01-21
**Single Source of Truth**: This file contains all TODOs, planned features, and roadmap items.

**Note**: This consolidates high-priority items. See `Documentation/Governance/IMPROVEMENT_ROADMAP.md` for detailed implementation guides and code examples.

---

## ✅ Recently Completed

*No completed items to report yet.*

---

## 🔴 High Priority - Critical (Before Production Use)

### Security Hardening

**Status**: Required for production deployment

#### 1. Authentication System

- **Status**: 📝 TODO
- **Description**: Implement OAuth2 authentication, API key support, JWT tokens
- **Details**: See `Documentation/Governance/IMPROVEMENT_ROADMAP.md` section "Security Hardening"

#### 2. Rate Limiting

- **Status**: 📝 TODO
- **Description**: Add rate limiting with Redis backend to prevent abuse
- **Details**: See `Documentation/Governance/IMPROVEMENT_ROADMAP.md`

#### 3. Input Validation & Sanitization

- **Status**: 📝 TODO
- **Description**: Comprehensive Pydantic validators, file upload validation, XSS prevention
- **Details**: See `Documentation/Governance/IMPROVEMENT_ROADMAP.md`

#### 4. CORS Enforcement

- **Status**: 📝 TODO
- **Description**: Remove wildcard CORS in production, implement whitelist
- **Details**: See `Documentation/Governance/IMPROVEMENT_ROADMAP.md`

#### 5. Secret Validation

- **Status**: 📝 TODO
- **Description**: Add startup validation to prevent use of default/weak secrets
- **Details**: See `Documentation/Governance/IMPROVEMENT_ROADMAP.md`

#### 6. Security Headers

- **Status**: 📝 TODO
- **Description**: Add HSTS, X-Content-Type-Options, CSP headers
- **Details**: See `Documentation/Governance/IMPROVEMENT_ROADMAP.md`

#### 7. Audit Logging

- **Status**: 📝 TODO
- **Description**: Log all authentication, authorization, and data modifications
- **Details**: See `Documentation/Governance/IMPROVEMENT_ROADMAP.md`

#### 8. Security Audit

- **Status**: 📝 TODO
- **Description**: Run OWASP ZAP, Bandit, Safety scans before production
- **Details**: See `Documentation/Governance/IMPROVEMENT_ROADMAP.md`

---

## 🟡 Medium Priority - Core Functionality

### Real ML Assessment Engine

**Status**: In development

#### 9. Model Selection & Training

- **Status**: 📝 TODO
- **Description**: Select architecture, collect training data, train baseline model
- **Details**: See `Documentation/Governance/IMPROVEMENT_ROADMAP.md` section "Real ML Assessment Engine"

#### 10. Assessment Logic Implementation

- **Status**: 📝 TODO
- **Description**: Replace placeholder scoring with trained model inference
- **Details**: See `Documentation/Governance/IMPROVEMENT_ROADMAP.md`

#### 11. Model Evaluation

- **Status**: 📝 TODO
- **Description**: Evaluate against test set, measure accuracy/precision/recall, iterate
- **Details**: See `Documentation/Governance/IMPROVEMENT_ROADMAP.md`

### Comprehensive Testing

**Status**: Ongoing

#### 12. API Integration Tests

- **Status**: 📝 TODO
- **Description**: Test all endpoints, error conditions, authentication flows
- **Details**: See `Documentation/Governance/IMPROVEMENT_ROADMAP.md`

#### 13. Load Testing

- **Status**: 📝 TODO
- **Description**: Test with realistic workloads, identify and address bottlenecks
- **Details**: See `Documentation/Governance/IMPROVEMENT_ROADMAP.md`

---

## 🟢 Low Priority - Future Enhancements

### Documentation

#### 14. Enhanced API Documentation

- **Status**: 📝 TODO
- **Description**: Expand API reference with more examples and use cases

### Features

#### 15. Advanced Assessment Features

- **Status**: 📝 TODO
- **Description**: Additional assessment paths, custom scoring, configurable evaluation criteria

### User Experience

#### 16. Web UI for Results

- **Status**: 📝 TODO
- **Description**: Browser-based interface for viewing and analyzing assessment results

#### 17. Batch Processing

- **Status**: 📝 TODO
- **Description**: Process multiple assessments in parallel

---

## 📊 Progress Summary

- **Completed**: 0 items
- **High Priority (Critical)**: 8 items (security)
- **Medium Priority (Core)**: 5 items (ML engine and testing)
- **Low Priority (Future)**: 4 items (enhancements)

---

## 📝 Notes

- **Detailed Implementation Guides**: See `Documentation/Governance/IMPROVEMENT_ROADMAP.md`
- **Current Version**: 0.1.1 (Alpha)
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
