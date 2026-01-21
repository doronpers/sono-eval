# Sono-Eval

> A growth-oriented assessment platform for candidates.
>
> **Note**: This system is in active development. Features are subject to change.

## 🚀 Start Here

**New to Sono-Eval?** → **[Get Started in 5 Minutes](Documentation/START_HERE.md)**

**Alternative paths:**

- [View documentation hub](Documentation/README.md) - Browse all docs
- [Quick Start Guide](Documentation/Guides/QUICK_START.md) - 5-minute setup
- [Contributing guide](CONTRIBUTING.md) - Help us improve

---

## ⚡ Quick Start

> **📖 For complete setup instructions, see:** [Quick Start Guide](documentation/Guides/QUICK_START.md)

**Quickest way to get started:**

```bash
# Clone and start
git clone https://github.com/doronpers/sono-eval.git
cd sono-eval
./launcher.sh start

# Access services
# 📚 API Docs: http://localhost:8000/docs
# 📊 Dashboard: http://localhost:8088 (admin/admin)
```

**Try your first assessment:**

```bash
# Using the CLI
./launcher.sh cli assess run \
  --candidate-id demo \
  --content "def hello(): return 'world'" \
  --paths technical
```

For detailed instructions, troubleshooting, and all installation options, see the [Quick Start Guide](Documentation/Guides/QUICK_START.md).

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

**For Individuals (Desktop)**: Think of it as a helpful coach, not just a grader.
**For Coaches/Reviewers (Optional)**: Review results and growth trends when you
choose to share them.

---

## 🌟 Key Features

### For Individuals

📖 **Clear Explanations** • 🎯 **Multiple Paths** • 📈 **Track Progress** • 💡 **Actionable Feedback**

### For Coaches (Optional)

🔍 **Deep Insights** • 📊 **Analytics** • ⚖️ **Fair Assessment** • 🚀 **Easy Setup**

**See all features** → [Documentation Hub](Documentation/README.md)

## 📚 Documentation

**Popular pages:**

- [Quick Start Guide](Documentation/Guides/QUICK_START.md) - 5-minute setup
- [API Reference](Documentation/Guides/user-guide/api-reference.md) - REST API docs
- [CLI Reference](Documentation/Guides/user-guide/cli-reference.md) - Command-line usage
- [FAQ](Documentation/Guides/faq.md) - Common questions

**[Browse all documentation →](Documentation/README.md)**

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

**Current State (v0.1.1 - Active Development):**

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

**Command Line:**

```bash
sono-eval assess run --candidate-id demo --file solution.py --paths technical
```

**Python API:**

```python
from sono_eval.assessment import AssessmentEngine
engine = AssessmentEngine()
result = await engine.assess(AssessmentInput(...))
```

**REST API:**

```bash
curl -X POST http://localhost:8000/api/v1/assessments -H "Content-Type: application/json" -d '{...}'
```

**See [API Reference](Documentation/Guides/user-guide/api-reference.md) and [CLI Reference](Documentation/Guides/user-guide/cli-reference.md) for complete examples.**

---

## 🧪 Development

See **[Contributing Guide](CONTRIBUTING.md)** for development setup, testing, and code quality guidelines.

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

---

## 🗺️ Roadmap

For the complete roadmap and TODO list, see [ROADMAP.md](ROADMAP.md).

### Current (v0.1.1 - Active Development)

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

- **Dark Horse Model** - Based on research on intrinsic motivation
- **T5** - Google's Text-to-Text Transfer Transformer
- **PEFT** - Hugging Face Parameter-Efficient Fine-Tuning
- **Apache Superset** - Modern data exploration platform

---

## 📊 Stats

- **Lines of Code**: ~2,500
- **Documentation Pages**: 100+
- **Test Coverage**: Core functionality tested
- **Docker Services**: 4 containers
- **API Endpoints**: 10+ REST endpoints
- **CLI Commands**: 15+ commands

---

Built with ❤️ by the Sono-Eval Team

**Version**: 0.1.1 | **Last Updated**: January 2026 | **Status**: Active Development

[⬆ Back to top](#sono-eval)

## 📦 Standalone Version

For beta testing or environments where Docker is not available, you can build a standalone executable:

```bash
# Build the standalone executable (requires Python 3.10+)
pip install pyinstaller
python scripts/build_standalone.py
```

**Running the Standalone Version:**

The executable at `dist/sono-eval` is self-contained. It:

- Uses local SQLite database (`sono_eval.db`)
- Stores data in `./sono_eval_data/`
- Does not require Docker or Redis

```bash
./dist/sono-eval assess run --candidate-id test --file solution.py --paths technical
```

---

## Agent Instructions

For AI agents working on this repository:

- [Agent Behavioral Standards](Documentation/Governance/AGENT_BEHAVIORAL_STANDARDS.md)
- [Documentation Organization Standards](Documentation/Governance/DOCUMENTATION_ORGANIZATION_STANDARDS.md)
