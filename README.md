# Sono-Eval

## Explainable Multi-Path Developer Assessment System

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.1.0-green.svg)](CHANGELOG.md)
[![Security Audit](https://img.shields.io/badge/security-audited-green.svg)](Documentation/Reports/SECRETS_AUDIT.md)
[![Documentation](https://img.shields.io/badge/docs-complete-brightgreen.svg)](Documentation/README.md)

> A growth-oriented assessment platform for candidates. Understand your strengths,
> track your progress, and get actionable feedback.
>
> ⚠️ **Active Development**: Sono-Eval is in **active development**.
> Features are being added and refined, APIs may change, and the system
> is not yet production-ready. Use at your own risk.

**[Start Here (Beginner-Friendly)](#-start-here-beginner-friendly)** • **[Quick Start](#-quick-start)** • **[Documentation](Documentation/README.md)** • **[Key Features](#-key-features)** • **[Usage Examples](#-usage-examples)**

---

## 🚀 Start Here (Beginner-Friendly)

### What is this?
Sono-Eval is a platform that evaluates developer submissions and provides detailed, explainable feedback. It's like a helpful coach that shows you exactly why you received each score and where to improve.

### Quick win (no terminal required)
1. **Open in Codespaces** (easiest way to try it):
   - Click the "Code" button above → "Codespaces" tab → "Create codespace"
   - Wait for the environment to load (~2 minutes)
   - In the VS Code web interface, open the Terminal
   - Run: `./launcher.sh start`
   - When services are ready, open `http://localhost:8000/docs` in the Ports tab
   - Try the `/health` endpoint to verify everything works

2. **First assessment in the browser**:
   - In the API docs (`/docs`), scroll to `POST /api/v1/assessments`
   - Click "Try it out"
   - Use this sample request:
     ```json
     {
       "candidate_id": "demo_user",
       "submission_type": "code",
       "content": {"code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)"},
       "paths_to_evaluate": ["TECHNICAL"]
     }
     ```
   - Click "Execute" and see your first assessment result!

### Sample files for testing
- `samples/` directory contains example code submissions
- Start with `samples/simple-function.py` for a basic assessment
- Try `samples/complex-class.py` for multi-path evaluation

### Fast path options
1. **Browser only (recommended for first try)**:
   - Use GitHub Codespaces as described above
2. **Local with Docker (no Python setup needed)**:
   ```bash
   git clone https://github.com/doronpers/sono-eval.git
   cd sono-eval
   ./launcher.sh start
   # Visit http://localhost:8000/docs
   ```
3. **Local Python development**:
   ```bash
   git clone https://github.com/doronpers/sono-eval.git
   cd sono-eval
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -e . --no-deps
   sono-eval server start --reload
   ```

### Contributing without fear
New to open source? No problem! Here are small first contributions:
- Add a note to this README about your experience ("What I saw when I opened /docs")
- Add a log message to an endpoint
- Create a test for a static endpoint
- Fix a typo in documentation

See our **[beginner-friendly contributing guide](CONTRIBUTING.md#quick-start-no-terminal)** for step-by-step instructions.

**Developer note:** To keep contributions consistent, install the project's pre-commit hooks locally:

```bash
pre-commit install
# If you run into SSL issues installing hooks, run:
./scripts/fix-pre-commit-ssl.sh
```

See `CONTRIBUTING.md` for full details on the development workflow.

### Common questions
- **What's an endpoint?** A URL you can call to do something (like `/health` to check if the server is running)
- **What's JSON?** A simple text format for data, like `{"name": "value"}`
- **How do I open a PR?** See [CONTRIBUTING.md](CONTRIBUTING.md) for browser-based PR creation
- **I'm stuck!** Open a GitHub Discussion or Issue - beginners are welcome!

---

## 🎯 What is Sono-Eval?

Sono-Eval is an assessment system designed to **help you understand and grow your
skills**. Unlike traditional tests that just give you a score, Sono-Eval:

- **Explains every score** with concrete evidence from your work
- **Evaluates multiple dimensions** - not just code, but design thinking,
  collaboration, and problem-solving
- **Identifies your strengths** and shows you exactly where to improve
- **Tracks your growth** over time with detailed history
- **Provides actionable feedback** you can use immediately

**For Candidates**: Think of it as a helpful coach, not just a grader!
**For Teams**: Get deep insights into skills and growth potential, not just
pass/fail.

---

## ⚡ Quick Start

Get Sono-Eval running in **5 minutes**:

### 🐳 Docker (Recommended)

```bash
# Clone and start
git clone https://github.com/doronpers/sono-eval.git
cd sono-eval
./launcher.sh start

# Access services
# 📚 API Docs: http://localhost:8000/docs
# 📊 Dashboard: http://localhost:8088 (admin/admin)
# 📱 Mobile: http://localhost:8000/mobile
```

### 🐍 Python Installation

```bash
# Setup
git clone https://github.com/doronpers/sono-eval.git
cd sono-eval
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .

# Run your first assessment
sono-eval assess run \
  --candidate-id demo_user \
  --content "def hello(): return 'world'" \
  --paths technical
```

### 📖 Next Steps

- **[Quick Start Guide](Documentation/Guides/QUICK_START.md)** - Detailed
  5-minute setup
- **[Installation Guide](Documentation/Guides/user-guide/installation.md)** - All
  installation options
- **[API Reference](Documentation/Guides/user-guide/api-reference.md)** -
  Complete API docs

---

## 🌟 Key Features

### For Candidates

- **📖 Clear Explanations** - Understand exactly why you received each score
- **🎯 Multiple Paths** - Evaluated on technical skills, design thinking,
  collaboration, and more
- **📈 Track Progress** - See how you improve over time
- **💡 Actionable Feedback** - Specific recommendations for growth
- **🏆 Identify Strengths** - Understand what you're naturally good at
- **📱 Mobile Companion** - Complete assessments on any device with guided,
  interactive experience

### For Evaluators

- **🔍 Deep Insights** - Go beyond surface-level scores
- **📊 Analytics** - Visualize candidate performance and cohorts
- **⚖️ Fair Assessment** - Consistent, evidence-based evaluation
- **🤝 Better Experience** - Candidates learn even if not hired
- **🚀 Easy Setup** - Docker deployment in minutes
- **📱 Mobile-Friendly** - Candidates can complete assessments anywhere

---

## 📚 Documentation

### Getting Started

- **[Quick Start](Documentation/Guides/QUICK_START.md)** - 5-minute setup guide
- **[Installation](Documentation/Guides/user-guide/installation.md)** -
  Detailed installation for all platforms
- **[For Candidates](Documentation/Guides/resources/candidate-guide.md)** -
  Welcome guide for candidates 👋

### User Guides

- **[CLI Reference](Documentation/Guides/user-guide/cli-reference.md)** -
  Complete command-line guide
- **[API Reference](Documentation/Guides/user-guide/api-reference.md)** - REST
  API documentation
- **[Configuration](Documentation/Guides/user-guide/configuration.md)** -
  Configure for your needs
- **[Configuration Presets](Documentation/Guides/user-guide/configuration-presets.md)**
  - Optimized presets for quick setup

### Concepts

- **[Architecture](Documentation/Core/concepts/architecture.md)** - System design
  and components
- **[Glossary](Documentation/Core/concepts/glossary.md)** - Comprehensive
  terminology

### Help & Resources

- **[Assessment Path Guide](Documentation/Guides/assessment-path-guide.md)** -
  Complete guide to all assessment paths
- **[FAQ](Documentation/Guides/faq.md)** - Frequently asked questions
- **[Troubleshooting](Documentation/Guides/troubleshooting.md)** - Solutions to
  common issues
- **[Learning Resources](Documentation/Guides/resources/learning.md)** -
  Tutorials and guides

📖 **[Browse All Documentation](Documentation/README.md)**

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

See **[Architecture Overview](Documentation/Core/concepts/architecture.md)** for
details.

---

## ⚠️ System Limits (Honesty Statement)

**Current State (v0.1.0 - Active Development):**

- **ML Integration**: Current "Hybrid" mode is primarily heuristic-driven.
  ML insights (T5/LoRA) are secondary and require high-compute
  environments (GPU) to be performant. The heuristic-first approach is
  currently the most reliable.
- **Concurrency**: `MemUStorage` is currently filesystem-based. While
  thread-safe for reads, concurrent writes to the same candidate profile
  may result in data race conditions. Use Redis for high-concurrency needs.
- **Assessment Retrieval**: The `GET /api/v1/assessments/{id}` endpoint
  retrieves assessments from hierarchical memory storage.
- **Dark Horse Mode**: The ML-based "Dark Horse" tracking and T5 tagging
  are primarily heuristic fallbacks. The documentation accurately reflects
  current capabilities.

**Security Requirements:**

- `SECRET_KEY` must be a 32-byte secure token (validated at startup).
- Candidate IDs are strictly sanitized (alphanumeric/dash/underscore only).
- File uploads enforce path traversal protection and content-type verification.

**Recommended Configuration:**

- Maintain `DARK_HORSE_MODE` as "enabled" to track micro-motives
  (Mastery vs. Efficiency), which reveal more about character than raw
  scores.
- The **Heuristic-First** approach is currently the most reliable for
  production use.

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

See **[Installation Guide](Documentation/Guides/user-guide/installation.md)** for
detailed instructions.

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
- **💬 Discussions**:
  [GitHub Discussions](https://github.com/doronpers/sono-eval/discussions)
- **📧 Email**: <support@sono-eval.example>

---

## 🗺️ Roadmap

### Current (v0.1.0 - Active Development)

- Explainable assessment engine (heuristic-first)
- Multi-path evaluation
- CLI and REST API
- Docker deployment
- Comprehensive documentation
- Repaired assessment retrieval endpoint
- Timezone-aware datetime handling
- LRU cache eviction for memory storage
- Enhanced security validation

### Next Release (v0.2.0)

- [ ] Real ML-based scoring (not placeholder)
- [ ] Batch assessment processing
- [ ] Authentication system
- [ ] Web UI for reviews
- [ ] Enhanced analytics
- [ ] Redis-backed memory storage for high concurrency

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

Built with ❤️ by the Sono-Eval Team

**Version**: 0.1.0 | **Last Updated**: January 2026 | **Status**: Active Development

[⬆ Back to top](#sono-eval)

## Agent Instructions

> **CRITICAL**: All AI agents MUST read
> [`AGENT_KNOWLEDGE_BASE.md`](AGENT_KNOWLEDGE_BASE.md) before performing any
> tasks. It contains non-negotiable Patent, Security, and Design rules.

Additional resources:

- [Agent Behavioral Standards](Documentation/Governance/AGENT_BEHAVIORAL_STANDARDS.md)
