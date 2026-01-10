# Sono-Eval

**Explainable Multi-Path Developer Assessment System**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.1.0-green.svg)](CHANGELOG.md)

> A growth-oriented assessment platform that explains its reasoning, tracks your progress, and helps you improve.

---

## 🎯 What is Sono-Eval?

Sono-Eval is an assessment system designed to **help you understand and grow your skills**. Unlike traditional tests that just give you a score, Sono-Eval:

- **Explains every score** with concrete evidence from your work
- **Evaluates multiple dimensions** - not just code, but design thinking, collaboration, and problem-solving
- **Identifies your strengths** and shows you exactly where to improve
- **Tracks your growth** over time with detailed history
- **Provides actionable feedback** you can use immediately

**For Candidates**: Think of it as a helpful coach, not just a grader!  
**For Teams**: Get deep insights into skills and growth potential, not just pass/fail.

---

## ⚡ Quick Start

### 5-Minute Setup (Docker)

```bash
# 1. Clone and enter directory
git clone https://github.com/doronpers/sono-eval.git
cd sono-eval

# 2. Start everything
./launcher.sh start

# 3. Access services
# API Docs: http://localhost:8000/docs
# Dashboard: http://localhost:8088 (admin/admin)
```

### Run Your First Assessment

```bash
# Using the CLI
sono-eval assess run \
  --candidate-id your_name \
  --file your_code.py \
  --paths technical design

# Using the API
curl -X POST http://localhost:8000/api/v1/assessments \
  -H "Content-Type: application/json" \
  -d '{"candidate_id": "your_name", "submission_type": "code", ...}'
```

**New to Sono-Eval?** Start with the **[Quick Start Guide](Documentation/Guides/quick-start.md)** →

---

## 🌟 Key Features

### For Candidates

- **📖 Clear Explanations** - Understand exactly why you received each score
- **🎯 Multiple Paths** - Evaluated on technical skills, design thinking, collaboration, and more
- **📈 Track Progress** - See how you improve over time
- **💡 Actionable Feedback** - Specific recommendations for growth
- **🏆 Identify Strengths** - Understand what you're naturally good at

### For Evaluators

- **🔍 Deep Insights** - Go beyond surface-level scores
- **📊 Analytics** - Visualize candidate performance and cohorts
- **⚖️ Fair Assessment** - Consistent, evidence-based evaluation
- **🤝 Better Experience** - Candidates learn even if not hired
- **🚀 Easy Setup** - Docker deployment in minutes

---

## 📚 Documentation

### Getting Started
- **[Quick Start](Documentation/Guides/quick-start.md)** - 5-minute setup guide
- **[Installation](Documentation/Guides/user-guide/installation.md)** - Detailed installation for all platforms
- **[For Candidates](Documentation/Guides/resources/candidate-guide.md)** - Welcome guide for candidates 👋

### User Guides
- **[CLI Reference](Documentation/Guides/user-guide/cli-reference.md)** - Complete command-line guide
- **[API Reference](Documentation/Guides/user-guide/api-reference.md)** - REST API documentation
- **[Configuration](Documentation/Guides/user-guide/configuration.md)** - Configure for your needs

### Concepts
- **[Architecture](Documentation/Core/concepts/architecture.md)** - System design and components
- **[Glossary](Documentation/Core/concepts/glossary.md)** - Comprehensive terminology

### Help & Resources
- **[FAQ](Documentation/Guides/faq.md)** - Frequently asked questions
- **[Troubleshooting](Documentation/Guides/troubleshooting.md)** - Solutions to common issues
- **[Learning Resources](Documentation/Guides/resources/learning.md)** - Tutorials and guides

📖 **[Browse All Documentation](Documentation/README.md)** →

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

See **[Architecture Overview](Documentation/Core/concepts/architecture.md)** for details.

---

## 💻 Usage Examples

### Command Line
```bash
# Create a candidate
sono-eval candidate create --id candidate_001

# Run assessment
sono-eval assess run \
  --candidate-id candidate_001 \
  --file solution.py \
  --paths technical design collaboration

# Generate code tags
sono-eval tag generate --file mycode.js --max-tags 5

# Start API server
sono-eval server start --reload
```

### Python API
```python
from sono_eval.assessment import AssessmentEngine, AssessmentInput, PathType

# Initialize engine
engine = AssessmentEngine()

# Run assessment
result = await engine.assess(AssessmentInput(
    candidate_id="candidate_001",
    submission_type="code",
    content={"code": your_code},
    paths_to_evaluate=[PathType.TECHNICAL, PathType.DESIGN]
))

# View results
print(f"Score: {result.overall_score}/100")
print(f"Summary: {result.summary}")
for finding in result.key_findings:
    print(f"• {finding}")
```

### REST API
```bash
# Create assessment
curl -X POST http://localhost:8000/api/v1/assessments \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": "candidate_001",
    "submission_type": "code",
    "content": {"code": "def hello(): return \"world\""},
    "paths_to_evaluate": ["TECHNICAL"]
  }'
```

---

## 🚀 Deployment

### Docker (Recommended)
```bash
# Start all services
./launcher.sh start

# View status
./launcher.sh status

# View logs
./launcher.sh logs

# Stop services
./launcher.sh stop
```

### Local Development
```bash
# Setup environment
./launcher.sh dev

# Activate virtual environment
source venv/bin/activate

# Run directly
sono-eval assess run --candidate-id test --file test.py
```

See **[Installation Guide](Documentation/Guides/user-guide/installation.md)** for detailed instructions.

---

## 🧪 Development

### Setup
```bash
# Clone repository
git clone https://github.com/doronpers/sono-eval.git
cd sono-eval

# Setup dev environment
./launcher.sh dev
source venv/bin/activate

# Install with dev dependencies
pip install -e ".[dev]"
```

### Testing
```bash
# Run tests
pytest

# With coverage
pytest --cov=src/sono_eval --cov-report=html

# Specific test file
pytest tests/test_assessment.py
```

### Code Quality
```bash
# Format code
black src/ tests/

# Lint
flake8 src/ tests/

# Type check
mypy src/
```

See **[Contributing Guide](CONTRIBUTING.md)** for more details.

---

## 🤝 Contributing

We welcome contributions! Whether you're:
- 🐛 Reporting bugs
- 💡 Suggesting features
- 📝 Improving documentation
- 🔧 Submitting code

**[Read our Contributing Guide](CONTRIBUTING.md)** to get started.

---

## 📄 License

Sono-Eval is licensed under the **[MIT License](LICENSE)**.

You're free to use, modify, and distribute it. See the LICENSE file for details.

---

## 🆘 Getting Help

- **📚 Documentation**: [Documentation/README.md](Documentation/README.md)
- **❓ FAQ**: [Documentation/Guides/faq.md](Documentation/Guides/faq.md)
- **🐛 Issues**: [GitHub Issues](https://github.com/doronpers/sono-eval/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/doronpers/sono-eval/discussions)
- **📧 Email**: support@sono-eval.example

---

## 🗺️ Roadmap

### Current (v0.1.0) ✅
- Explainable assessment engine
- Multi-path evaluation
- CLI and REST API
- Docker deployment
- Comprehensive documentation

### Next Release (v0.2.0)
- [ ] Real ML-based scoring (not placeholder)
- [ ] Batch assessment processing
- [ ] Authentication system
- [ ] Web UI for reviews
- [ ] Enhanced analytics

### Future
- [ ] Multi-language support
- [ ] Plugin system
- [ ] Real-time collaboration
- [ ] Integration with GitHub/GitLab
- [ ] Mobile dashboards

See **[CHANGELOG.md](CHANGELOG.md)** for version history.

---

## 🙏 Acknowledgments

- **Dark Horse Model** - Based on tex-assist-coding research
- **T5** - Google's Text-to-Text Transfer Transformer
- **PEFT** - Hugging Face Parameter-Efficient Fine-Tuning
- **Apache Superset** - Modern data exploration platform

---

## 📊 Stats

- **Lines of Code**: ~2,500
- **Documentation Pages**: 15+
- **Test Coverage**: Core functionality tested
- **Docker Services**: 4 containers
- **API Endpoints**: 10+ REST endpoints
- **CLI Commands**: 15+ commands

---

**Built with ❤️ by the Sono-Eval Team**

**Version**: 0.1.0 | **Last Updated**: January 10, 2026

[⬆ Back to top](#sono-eval)
