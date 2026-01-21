# Changelog

All notable changes to Sono-Eval will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### In Development

The following features are currently being developed:

- Hybrid assessment engine combining heuristics with ML insights
- Enhanced configuration presets for different deployment scenarios
- Improved CLI experience with better feedback and guidance
- Mobile companion interface improvements

See [ROADMAP.md](ROADMAP.md) for planned features and priorities.

---

## [0.1.0] - 2026-01-10

- **Added**

- Initial release of Sono-Eval
- Assessment engine with explainable scoring
- Multi-path evaluation (Technical, Design, Collaboration, Problem-Solving, Communication)
- **MemU**: Created `src/sono_eval/memory/memu.py` for hierarchical candidate
  memory storage
- T5 + PEFT/LoRA semantic tagging
- TagStudio file management
- FastAPI REST backend
- Comprehensive CLI (Click + Rich)
- Docker + Docker Compose deployment
- Apache Superset configuration
- One-click launcher script
- Basic documentation (README, CONTRIBUTING, GLOSSARY)
- Test suite with pytest
- Configuration via environment variables

- **Features**

- Evidence-based assessment with explanations
- Confidence scoring for all evaluations
- LRU caching for performance
- Async/await throughout
- Type hints and Pydantic models
- Modular architecture
- MIT License

---

## Release Notes

### Version 0.1.0 - Initial Release

**Release Date**: January 2026

This is the first release of Sono-Eval, providing core assessment functionality
and a foundation for future development.

**Highlights**:

- Multi-path assessment engine (Technical, Design, Collaboration, Problem-Solving, Communication)
- Evidence-based scoring with explanations
- CLI and REST API interfaces
- Docker deployment support
- Comprehensive documentation (100+ pages)
- MemU hierarchical memory storage
- Semantic tagging capabilities
- Apache Superset dashboard integration

**Current Status**: Active Development (Alpha)

**Known Limitations**:

- Assessment engine primarily heuristic-based (ML integration in progress)
- No authentication system (development use only)
- Single-server deployment
- Limited batch processing
- Mobile companion interface is basic

**For Production Use**: Please review [ROADMAP.md](ROADMAP.md) for security
enhancements required before production deployment.

**Dependencies**:

- Python 3.13+
- Docker & Docker Compose (optional, for containerized deployment)
- PostgreSQL or SQLite (database)
- Redis (caching, optional)

---

## Future Development

See [ROADMAP.md](ROADMAP.md) for planned features and development priorities.

Key areas of focus:

- Security hardening (authentication, rate limiting, input validation)
- Real ML-based assessment engine
- Comprehensive testing and quality assurance
- Enhanced user interfaces and visualizations

---

## Contributing

Want to contribute? See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Reporting issues? Please include:

- Version number (check with `sono-eval --version`)
- Environment details (OS, Python version, Docker version)
- Steps to reproduce
- Expected vs actual behavior

---

## Versioning

Sono-Eval follows [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backward-compatible)
- **PATCH**: Bug fixes (backward-compatible)

**Alpha** (0.x.x): API may change, not production-ready
**Beta** (0.9.x): Feature-complete, stabilizing API
**Stable** (1.0.0+): Production-ready, stable API

---

## Links

- **Repository**: <https://github.com/doronpers/sono-eval>
- **Documentation**: [Documentation/README.md](Documentation/README.md)
- **Issues**: <https://github.com/doronpers/sono-eval/issues>
- **Discussions**: <https://github.com/doronpers/sono-eval/discussions>

---

**Last Updated**: January 21, 2026
