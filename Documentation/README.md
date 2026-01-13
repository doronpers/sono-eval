# Sono-Eval Documentation

Welcome to the Sono-Eval documentation! This guide will help you understand,
install, and use the Sono-Eval explainable multi-path developer assessment
system.

> 📖 **Complete Index**: See [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) for
> a complete catalog of all documentation.

## 📚 Documentation Structure

This documentation is organized following our
[Documentation Organization Standards](Governance/DOCUMENTATION_ORGANIZATION_STANDARDS.md):

### 🚀 Getting Started (Guides)

- **[Quick Start Guide](Guides/QUICK_START.md)** - Get up and running in 5
  minutes
- **[Installation Guide](Guides/user-guide/installation.md)** - Detailed
  installation instructions
- **[Configuration Guide](Guides/user-guide/configuration.md)** - Configure
  Sono-Eval for your needs
- **[Configuration Presets](Guides/user-guide/configuration-presets.md)** -
  Optimized presets for quick setup

### 📖 User Guides

- **[CLI Reference](Guides/user-guide/cli-reference.md)** - Complete
  command-line interface documentation
- **[API Reference](Guides/user-guide/api-reference.md)** - REST API endpoints
  and usage

### 🧠 Core Concepts

- **[Architecture Overview](Core/concepts/architecture.md)** - System design and
  components
- **[Glossary](Core/concepts/glossary.md)** - Comprehensive terminology reference

### 💻 Development

- **[Implementation Details](Core/development/implementation.md)** - Technical
  implementation overview
- **[Contributing](../CONTRIBUTING.md)** - How to contribute to Sono-Eval

### 📚 Resources & Help

- **[Assessment Path Guide](Guides/assessment-path-guide.md)** - Complete guide
  to all assessment paths
- **[Candidate Guide](Guides/resources/candidate-guide.md)** - Welcome guide for
  candidates
- **[Learning Resources](Guides/resources/learning.md)** - Tutorials and
  educational content
- **[Examples](Guides/resources/examples/)** - Practical code examples
- **[Troubleshooting](Guides/troubleshooting.md)** - Common issues and solutions
- **[FAQ](Guides/faq.md)** - Frequently asked questions

### 📊 Reports & Reviews

- **[Design Audit](Reports/DESIGN_AUDIT.md)** - Comprehensive design review and
  improvements
- **[Final Report](Reports/FINAL_REPORT.md)** - Summary of design improvements
- **[Code Review Report](Reports/CODE_REVIEW_REPORT.md)** - Detailed code quality
  analysis
- **[Assessment Summary](Reports/ASSESSMENT_SUMMARY.md)** - Consolidated
  assessment findings

### 📋 Reference

- **[Changelog](../CHANGELOG.md)** - Version history and changes
- **[Documentation Index](DOCUMENTATION_INDEX.md)** - Complete catalog of all
  docs

---

## 🚀 Quick Links

### For Users

- New to Sono-Eval? Start with the
  **[Quick Start Guide](Guides/QUICK_START.md)**
- Need to configure? Check the
  **[Configuration Presets](Guides/user-guide/configuration-presets.md)** or
  **[Configuration Guide](Guides/user-guide/configuration.md)**
- Having issues? See **[Troubleshooting](Guides/troubleshooting.md)**

### For Developers

- Want to contribute? **[Contributing Guide](../CONTRIBUTING.md)**
- Understanding the code?
  **[Implementation Details](Core/development/implementation.md)**
- Setting up? Check **[Installation Guide](Guides/user-guide/installation.md)**

### For Architects

- System design? **[Architecture Overview](Core/concepts/architecture.md)**
- Terminology? **[Glossary](Core/concepts/glossary.md)**
- API integration? **[API Reference](Guides/user-guide/api-reference.md)**

---

## 🎯 What is Sono-Eval?

Sono-Eval is an explainable multi-path developer assessment system that provides:

- **🧠 Explainable Scoring** - Evidence-based assessments with detailed
  explanations
- **🛤️ Multi-Path Evaluation** - Technical, design, collaboration, and more
- **🎯 Dark Horse Tracking** - Micro-motive analysis for individualized
  assessment
- **🏷️ Semantic Tagging** - T5 + PEFT for intelligent code tagging
- **💾 Hierarchical Memory** - Persistent candidate memory storage
- **📊 Analytics Dashboard** - Apache Superset for insights
- **🚀 Easy Deployment** - Docker + one-click launcher

---

## 💡 Key Features

### Assessment Engine

Multi-dimensional evaluation with evidence-based scoring:

```python
from sono_eval.assessment import AssessmentEngine, AssessmentInput, PathType

engine = AssessmentEngine()
result = await engine.assess(AssessmentInput(
    candidate_id="candidate_001",
    submission_type="code",
    content={"code": "..."},
    paths_to_evaluate=[PathType.TECHNICAL, PathType.DESIGN]
))
```

### Command-Line Interface

Intuitive commands for all operations:

```bash
sono-eval assess run --candidate-id user001 --file solution.py
sono-eval candidate list
sono-eval tag generate --file code.js
```

### REST API

Programmatic access with auto-generated documentation:

```bash
curl -X POST http://localhost:8000/api/v1/assessments \
  -H "Content-Type: application/json" \
  -d '{"candidate_id": "001", "submission_type": "code", ...}'
```

---

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                     Sono-Eval System                        │
├─────────────────────────────────────────────────────────────┤
│  Interfaces:  CLI  │  REST API  │  Python SDK               │
├─────────────────────────────────────────────────────────────┤
│  Core Engine:                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  Assessment  │  │   Semantic   │  │    Memory    │    │
│  │    Engine    │  │    Tagging   │  │   (MemU)     │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
├─────────────────────────────────────────────────────────────┤
│  Storage:  PostgreSQL  │  Redis  │  File System            │
├─────────────────────────────────────────────────────────────┤
│  Analytics:  Apache Superset Dashboards                    │
└─────────────────────────────────────────────────────────────┘
```

See **[Architecture Overview](Core/concepts/architecture.md)** for detailed
diagrams.

---

## 🤝 Getting Help

- **Documentation**: You're reading it! Explore the sections above
- **Issues**: [GitHub Issues](https://github.com/doronpers/sono-eval/issues)
- **Discussions**:
  [GitHub Discussions](https://github.com/doronpers/sono-eval/discussions)
- **Email**: <support@sono-eval.example>

---

## 📄 License

Sono-Eval is licensed under the [MIT License](../LICENSE).

---

**Version**: 0.1.0
**Last Updated**: January 10, 2026
