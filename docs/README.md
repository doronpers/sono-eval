# Sono-Eval Documentation

Welcome to the Sono-Eval documentation! This guide will help you understand, install, and use the Sono-Eval explainable multi-path developer assessment system.

## 📚 Documentation Structure

### Getting Started
- **[Quick Start Guide](quick-start.md)** - Get up and running in 5 minutes
- **[Installation Guide](user-guide/installation.md)** - Detailed installation instructions
- **[Configuration Guide](user-guide/configuration.md)** - Configure Sono-Eval for your needs

### User Guides
- **[CLI Reference](user-guide/cli-reference.md)** - Complete command-line interface documentation
- **[API Reference](user-guide/api-reference.md)** - REST API endpoints and usage
- **[Docker Deployment](user-guide/docker.md)** - Container-based deployment guide

### Core Concepts
- **[Architecture Overview](concepts/architecture.md)** - System design and components
- **[Assessment Paths](concepts/assessment-paths.md)** - Understanding multi-path assessment
- **[Dark Horse Model](concepts/dark-horse.md)** - Micro-motive tracking explained
- **[Glossary](concepts/glossary.md)** - Comprehensive terminology reference

### Development
- **[Development Setup](development/setup.md)** - Set up your development environment
- **[Testing Guide](development/testing.md)** - Write and run tests
- **[Implementation Details](development/implementation.md)** - Technical implementation overview
- **[Contributing](../CONTRIBUTING.md)** - How to contribute to Sono-Eval

### Resources
- **[Learning Resources](resources/learning.md)** - Tutorials and educational content
- **[Examples](resources/examples/)** - Practical code examples
- **[Troubleshooting](troubleshooting.md)** - Common issues and solutions
- **[FAQ](faq.md)** - Frequently asked questions

### Reference
- **[Design Audit](DESIGN_AUDIT.md)** - Comprehensive design review and improvements
- **[Changelog](../CHANGELOG.md)** - Version history and changes

---

## 🚀 Quick Links

### For Users
- New to Sono-Eval? Start with the **[Quick Start Guide](quick-start.md)**
- Need to configure? Check the **[Configuration Guide](user-guide/configuration.md)**
- Having issues? See **[Troubleshooting](troubleshooting.md)**

### For Developers
- Setting up dev environment? **[Development Setup](development/setup.md)**
- Want to contribute? **[Contributing Guide](../CONTRIBUTING.md)**
- Understanding the code? **[Implementation Details](development/implementation.md)**

### For Architects
- System design? **[Architecture Overview](concepts/architecture.md)**
- Assessment logic? **[Assessment Paths](concepts/assessment-paths.md)**
- API integration? **[API Reference](user-guide/api-reference.md)**

---

## 🎯 What is Sono-Eval?

Sono-Eval is an explainable multi-path developer assessment system that provides:

- **🧠 Explainable Scoring** - Evidence-based assessments with detailed explanations
- **🛤️ Multi-Path Evaluation** - Technical, design, collaboration, and more
- **🎯 Dark Horse Tracking** - Micro-motive analysis for individualized assessment
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

```
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

See **[Architecture Overview](concepts/architecture.md)** for detailed diagrams.

---

## 🤝 Getting Help

- **Documentation**: You're reading it! Explore the sections above
- **Issues**: [GitHub Issues](https://github.com/doronpers/sono-eval/issues)
- **Discussions**: [GitHub Discussions](https://github.com/doronpers/sono-eval/discussions)
- **Email**: support@sono-eval.example

---

## 📄 License

Sono-Eval is licensed under the [MIT License](../LICENSE).

---

**Version**: 0.1.0  
**Last Updated**: January 10, 2026
