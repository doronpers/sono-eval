# Sono-Eval Documentation Hub

Welcome to the Sono-Eval documentation. This is your single source of truth for understanding, installing, and using the system.

**Primary experience**: desktop, single-user workflows.
**Optional companion**: a mobile-friendly interface for guided assessments.

---

## 🗺️ Navigation by Role

### 🚦 Start Here (Landing Guide)

- **[Start Here](START_HERE.md)** - Single landing page for first-time readers

### 👋 For Individuals (Desktop)

1. **[Candidate Guide](Guides/resources/candidate-guide.md)** - Your starting point
2. **[Quick Start](Guides/QUICK_START.md)** - Get running in 5 minutes
3. **[FAQ](Guides/faq.md)** - Common questions

### 🛠️ For Developers & Contributors

1. **[Architecture Overview](Core/concepts/architecture.md)** - How it's built
2. **[Installation Guide](Guides/user-guide/installation.md)** - Detailed setup
3. **[Implementation Details](Core/development/implementation.md)** - Code dive
4. **[Contributing](../CONTRIBUTING.md)** - How to help

### 📊 For Coaches (Optional)

1. **[Assessment Path Guide](Guides/assessment-path-guide.md)** - What we measure
2. **[API Reference](Guides/user-guide/api-reference.md)** - Integration points
3. **[Glossary](Core/concepts/glossary.md)** - Terminology

### 📱 Optional Mobile Companion

1. **[Mobile Companion Guide](Guides/mobile-companion.md)** - Touch-friendly flow

---

## 📚 Complete Document Catalog

### Core Concepts

- **[Architecture](Core/concepts/architecture.md)** - System design and data flow
- **[Glossary](Core/concepts/glossary.md)** - Comprehensive terminology
- **[Implementation](Core/development/implementation.md)** - Technical overview

### User Guides

- **[Quick Start](Guides/QUICK_START.md)** - 5-minute setup
- **[Installation](Guides/user-guide/installation.md)** - Platform-specific docs
- **[Configuration](Guides/user-guide/configuration.md)** - Full settings guide
- **[CLI Reference](Guides/user-guide/cli-reference.md)** - Command-line usage
- **[API Reference](Guides/user-guide/api-reference.md)** - REST API usage

### Reports & Audits

- **[Design Audit](Reports/DESIGN_AUDIT.md)** - Dieter Rams principles review
- **[Readiness Report](Reports/PUBLIC_READINESS_REPORT.md)** - Beta release status
- **[Security Audit](Reports/SECURITY_AUDIT_SUMMARY.md)** - Security review summary
- **[Secrets Audit](Reports/SECRETS_AUDIT.md)** - Credentials and PII check

### Maintenance & Governance

- **[Organization Standards](Governance/DOCUMENTATION_ORGANIZATION_STANDARDS.md)**
- **[Maintenance Notes](Governance/MAINTENANCE.md)**

---

## 🏗️ Architecture at a Glance

```text
┌─────────────────────────────────────────────────────────────┐
│                     Sono-Eval System                        │
├─────────────────────────────────────────────────────────────┤
│  Interfaces:  CLI  │  REST API  │  Python SDK  │  Mobile    │
├─────────────────────────────────────────────────────────────┤
│  Core Engine:                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  Assessment  │  │   Semantic   │  │    Memory    │    │
│  │    Engine    │  │    Tagging   │  │   (MemU)     │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
├─────────────────────────────────────────────────────────────┤
│  Storage:  PostgreSQL  │  Redis  │  File System            │
└─────────────────────────────────────────────────────────────┘
```

---

**Version**: 0.1.1 | **Last Updated**: January 15, 2026
