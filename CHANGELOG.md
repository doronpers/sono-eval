# Changelog

All notable changes to Sono-Eval will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Comprehensive documentation structure in `docs/` folder
- Quick Start Guide for 5-minute setup
- Complete API Reference with examples
- Detailed CLI Reference with tips and tricks
- Configuration Guide with profiles and best practices
- Candidate-focused FAQ for interns and new hires
- Architecture overview with diagrams
- Troubleshooting guide with solutions
- Design audit based on Dieter Rams' 10 principles

### Changed
- Reorganized documentation from root to `docs/` folder
- Moved GLOSSARY.md to `docs/concepts/glossary.md`
- Moved learning-resources.md to `docs/resources/learning.md`
- Moved IMPLEMENTATION_SUMMARY.md to `docs/development/implementation.md`
- Enhanced README.md with clearer structure

### Improved
- Documentation is now production-ready for hiring/onboarding
- Better onboarding experience for candidates
- Clearer navigation and organization
- More practical examples and guidance

---

## [0.1.0] - 2026-01-10

### Added
- Initial release of Sono-Eval
- Assessment engine with explainable scoring
- Multi-path evaluation (Technical, Design, Collaboration, Problem-Solving, Communication)
- Dark Horse micro-motive tracking
- MemU hierarchical memory storage
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

### Features
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

**Release Date**: January 10, 2026

This is the first alpha release of Sono-Eval, focusing on core functionality and developer experience.

**Highlights**:
- Complete assessment engine with explainable AI
- Multi-path evaluation framework
- Semantic tagging with transformer models
- Hierarchical memory storage
- Production-ready API and CLI
- Docker deployment support

**Target Users**:
- Development teams evaluating candidates
- Companies hiring interns and junior developers
- Technical assessors seeking explainable results
- Candidates wanting growth-oriented feedback

**Known Limitations**:
- Assessment engine uses example/placeholder scoring (ML models need fine-tuning)
- No authentication in default configuration
- Single-server deployment only
- Limited batch processing capabilities
- No web UI for reviews

**Next Steps** (Planned for 0.2.0):
- Real ML-based assessment scoring
- Batch assessment processing
- Authentication and authorization
- Web-based review interface
- Enhanced analytics dashboards
- Performance optimizations

**Upgrade Path**:
- First release, no upgrades needed

**Breaking Changes**:
- None (initial release)

**Dependencies**:
- Python 3.9+
- Docker & Docker Compose (for containerized deployment)
- PostgreSQL or SQLite (database)
- Redis (caching, optional)

**Documentation**:
- Comprehensive documentation in `docs/` folder
- Quick Start Guide for rapid setup
- Complete API and CLI references
- Architecture and implementation details

**Support**:
- GitHub Issues for bugs and features
- GitHub Discussions for questions
- Email support available

---

## Future Roadmap

### Version 0.2.0 (Planned)
- Real ML-based scoring (not placeholder)
- Batch assessment processing
- Authentication system (API keys, OAuth2)
- Web UI for assessment reviews
- Enhanced Superset dashboards
- Performance optimizations
- Migration guides

### Version 0.3.0 (Planned)
- Advanced analytics features
- Multi-language support
- Plugin system for extensibility
- Real-time collaboration features
- Enhanced ML model fine-tuning tools
- Integration with GitHub, GitLab

### Version 1.0.0 (Planned)
- Production-ready with extensive testing
- Complete web interface
- Enterprise features
- High availability deployment
- Comprehensive API v2
- Mobile-friendly dashboards

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

- **Repository**: https://github.com/doronpers/sono-eval
- **Documentation**: [docs/README.md](docs/README.md)
- **Issues**: https://github.com/doronpers/sono-eval/issues
- **Discussions**: https://github.com/doronpers/sono-eval/discussions

---

**Last Updated**: January 10, 2026
