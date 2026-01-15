# Glossary

A comprehensive reference of terms, concepts, technologies, and tools used in the Sono-Eval system.

---

## Table of Contents

- [Core Concepts](#core-concepts)
- [Assessment Terms](#assessment-terms)
- [Machine Learning & NLP](#machine-learning--nlp)
- [Technologies & Frameworks](#technologies--frameworks)
- [Development Tools](#development-tools)
- [Infrastructure & Deployment](#infrastructure--deployment)
- [Data Structures](#data-structures)

---

## Core Concepts

### Sono-Eval

The name of this explainable multi-path developer assessment system. "Sono" relates to sound/resonance, suggesting the system helps identify what resonates with each candidate's unique abilities.

### Explainable AI (XAI)

Artificial intelligence systems designed to provide clear, understandable explanations for their decisions and predictions. In Sono-Eval, every assessment score is backed by evidence and natural language explanations.

### Multi-Path Assessment

An evaluation approach that assesses candidates across multiple dimensions (paths) simultaneously, recognizing that excellence can manifest in different ways. Sono-Eval evaluates: Technical, Design, Collaboration, Problem-Solving, and Communication paths.

### Dark Horse Model

A theory based on the book "Dark Horse" by Todd Rose, which emphasizes individualized paths to success through understanding intrinsic motivations. In Sono-Eval, this is implemented through micro-motive tracking.

### tex-assist-coding Model

A research-based model for understanding developer motivations and learning patterns, used as the foundation for the Dark Horse micro-motive tracking in Sono-Eval.

---

## Assessment Terms

### Assessment Engine

The core module that performs evaluations. It takes candidate submissions, analyzes them across multiple paths, generates scores with evidence, and provides explanations.

### Evidence-Based Scoring

A scoring methodology where every score is backed by concrete evidence from the candidate's submission, including source references (file, line number), descriptions, and confidence weights.

### Micro-Motives

Intrinsic motivations that drive behavior and learning. Sono-Eval tracks six types:

- **Mastery**: Drive to deeply understand and perfect skills
- **Exploration**: Willingness to try new approaches and learn
- **Collaboration**: Team-oriented mindset and cooperative behavior
- **Innovation**: Creative problem-solving and novel thinking
- **Quality**: Attention to detail and craftsmanship
- **Efficiency**: Focus on optimal solutions and resource management

### Path Score

An evaluation score for a specific assessment dimension (e.g., Technical, Design). Each path score includes metrics, micro-motives, strengths, and areas for improvement.

### Scoring Metric

An individual measurement within an assessment path. Each metric has:

- Name and category
- Numerical score (0-100)
- Weight (importance in overall calculation)
- Evidence supporting the score
- Natural language explanation
- Confidence level

### Confidence Score

A measure (0.0-1.0) indicating the assessment engine's certainty about a particular score or finding, based on the strength and quantity of evidence.

### Evidence

Supporting information for a score, including:

- Type (code quality, documentation, testing, architecture, etc.)
- Description of what was observed
- Source reference (file path, line numbers)
- Weight (importance of this evidence)
- Metadata (additional context)

---

## Machine Learning & NLP

### T5 (Text-to-Text Transfer Transformer)

A transformer-based neural network model from Google Research that frames all NLP tasks as text-to-text problems. Used in Sono-Eval for semantic tag generation.

**Reference**: [Exploring Transfer Learning with T5](https://arxiv.org/abs/1910.10683)

### PEFT (Parameter-Efficient Fine-Tuning)

A set of techniques for adapting large pre-trained models to specific tasks by updating only a small fraction of parameters, reducing computational costs and memory requirements.

**Library**: Hugging Face PEFT

### LoRA (Low-Rank Adaptation)

A PEFT technique that injects trainable low-rank matrices into transformer layers, allowing efficient fine-tuning of large language models with minimal parameter updates.

**Configuration in Sono-Eval**:

- Rank (r): 8
- Alpha: 16
- Dropout: 0.1

**Reference**: [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)

### Transformer

A deep learning architecture based on self-attention mechanisms, introduced in "Attention Is All You Need" (Vaswani et al., 2017). Forms the basis of modern NLP models like T5.

### Semantic Tagging

Automatically generating meaningful tags or labels for code based on understanding its semantic content, not just keywords. Goes beyond syntax to understand intent and purpose.

### Fallback Heuristics

Rule-based tagging methods used when ML models are unavailable or for supplementing model predictions. Based on keyword matching and pattern recognition.

---

## Technologies & Frameworks

### Python

The primary programming language for Sono-Eval. Version 3.9+ required.

**Key Features Used**:

- Async/await for concurrent operations
- Type hints for code clarity
- Dataclasses and Pydantic models
- Context managers for resource handling

### FastAPI

A modern, high-performance Python web framework for building APIs with automatic OpenAPI documentation.

**Key Features**:

- Async/await support
- Automatic request validation with Pydantic
- Interactive API documentation (Swagger UI)
- CORS middleware for web client support

**Website**: <https://fastapi.tiangolo.com/>

### Pydantic

A data validation library using Python type annotations. Used extensively in Sono-Eval for defining data models and configuration.

**Key Features**:

- Type validation and coercion
- Settings management from environment variables
- JSON serialization/deserialization
- Field validation and constraints

**Website**: <https://docs.pydantic.dev/>

### Click

A Python package for creating command-line interfaces with minimal code.

**Usage in Sono-Eval**: All CLI commands (`sono-eval assess`, `candidate`, `tag`, etc.)

**Website**: <https://click.palletsprojects.com/>

### Rich

A Python library for rich text and formatting in the terminal.

**Features Used**:

- Colored console output
- Tables for displaying data
- Progress indicators
- Syntax highlighting

**Website**: <https://rich.readthedocs.io/>

### Uvicorn

An ASGI web server implementation for Python, used to run the FastAPI application.

**Features**:

- Async/await support
- WebSocket support
- Auto-reload for development
- Production-ready performance

---

## Development Tools

### Pytest

Python testing framework used for all unit and integration tests in Sono-Eval.

**Features Used**:

- Async test support (`pytest-asyncio`)
- Code coverage reporting (`pytest-cov`)
- Fixtures for test setup
- Parametrized tests

**Website**: <https://pytest.org/>

### Black

An opinionated Python code formatter that ensures consistent style.

**Configuration**: Line length = 100

**Website**: <https://black.readthedocs.io/>

### Flake8

A Python linting tool that checks code for style and programming errors.

**Website**: <https://flake8.pycqa.org/>

### MyPy

A static type checker for Python that verifies type hints.

**Website**: <https://mypy-lang.org/>

### Git

Distributed version control system used for source code management.

---

## Infrastructure & Deployment

### Docker

Containerization platform for packaging applications with their dependencies.

**Sono-Eval Containers**:

- Main application (Python + FastAPI)
- PostgreSQL database
- Redis cache
- Apache Superset analytics

**Website**: <https://www.docker.com/>

### Docker Compose

Tool for defining and running multi-container Docker applications using YAML configuration.

**File**: `docker-compose.yml`

**Website**: <https://docs.docker.com/compose/>

### PostgreSQL

Open-source relational database system.

**Usage**: Optional persistent storage for assessments and candidate data (default is SQLite)

**Website**: <https://www.postgresql.org/>

### Redis

In-memory data structure store used as cache and message broker.

**Usage in Sono-Eval**:

- Caching frequently accessed data
- Task queue backend
- Superset caching layer

**Website**: <https://redis.io/>

### Apache Superset

Open-source data visualization and business intelligence platform.

**Usage**: Pre-configured dashboards for candidate analytics, cohort comparisons, and micro-motive analysis

**Website**: <https://superset.apache.org/>

### SQLite

Lightweight, serverless SQL database engine.

**Usage**: Default database for local development and testing

**Website**: <https://www.sqlite.org/>

### ASGI (Asynchronous Server Gateway Interface)

A spiritual successor to WSGI, designed to provide a standard interface between async-capable Python web servers and applications.

### CORS (Cross-Origin Resource Sharing)

A security mechanism that allows web applications from one origin to access resources from another origin. Enabled in Sono-Eval API for web client support.

---

## Data Structures

### MemU (Memory Unit)

The hierarchical memory storage system in Sono-Eval for persistent candidate data.

**Features**:

- Multi-level tree structure (configurable depth)
- JSON-based persistence
- LRU (Least Recently Used) caching
- Path traversal operations

### Memory Node

A single unit in the MemU hierarchy containing:

- Unique ID
- Parent reference
- Level in hierarchy
- Timestamp
- Data payload
- Child references
- Metadata

### Candidate Memory

Complete memory structure for a candidate, including:

- Candidate ID
- Root node
- Dictionary of all nodes
- Last update timestamp
- Version information

### Assessment Result

Complete output from the assessment engine including:

- Overall score and confidence
- Path scores (one per evaluation path)
- Micro-motives identified
- Summary and key findings
- Recommendations
- Processing metadata

### Semantic Tag

A tag generated for code or content with:

- Tag text/label
- Category (language, pattern, quality, architecture, etc.)
- Confidence score
- Context snippet
- Metadata

### TagStudio

File management system with semantic tagging capabilities:

- File organization and storage
- Automated tagging integration
- Tag-based search and retrieval
- Tag statistics and analytics
- Reverse indexing for efficient queries

---

## Acronyms & Abbreviations

| Acronym | Full Form | Description |
|---------|-----------|-------------|
| API | Application Programming Interface | Interface for programmatic access |
| ASGI | Asynchronous Server Gateway Interface | Python async web server standard |
| CLI | Command-Line Interface | Terminal-based user interface |
| CORS | Cross-Origin Resource Sharing | Web security mechanism |
| LRU | Least Recently Used | Cache eviction policy |
| ML | Machine Learning | AI subset focused on learning from data |
| NLP | Natural Language Processing | AI for human language understanding |
| PEFT | Parameter-Efficient Fine-Tuning | Efficient model adaptation technique |
| REST | Representational State Transfer | Web API architectural style |
| XAI | Explainable AI | AI systems with interpretable decisions |

---

## Programming Languages

### Python

**Version**: 3.9+
**Usage**: Primary language for entire system
**Key Libraries**: FastAPI, Pydantic, Click, Transformers, PyTorch

### SQL

**Usage**: Database queries for PostgreSQL/SQLite
**Context**: Optional persistent storage, Superset analytics

### YAML

**Usage**: Configuration files (Docker Compose, CI/CD)
**Files**: `docker-compose.yml`

### JSON

**Usage**: Data serialization, API responses, MemU storage
**Context**: Assessment results, candidate memory, configuration

### Bash

**Usage**: Shell scripting for launcher and utilities
**Files**: `launcher.sh`

### Markdown

**Usage**: Documentation
**Files**: All `.md` files (README, CONTRIBUTING, etc.)

---

## File Formats

### .py (Python Source)

Python source code files

### .md (Markdown)

Documentation files with formatting

### .yml/.yaml (YAML)

Configuration files (Docker Compose, etc.)

### .json (JSON)

Data files for MemU storage and configuration

### .toml (TOML)

Python package configuration (`pyproject.toml`)

### .txt (Text)

Plain text files (requirements.txt)

### .env (Environment)

Environment variable definitions

---

## Development Patterns

### Async/Await

Python's asynchronous programming model for concurrent operations without blocking.

**Usage**: Assessment engine, API endpoints, I/O operations

### Dependency Injection

Design pattern where dependencies are provided to objects rather than created internally.

**Usage**: FastAPI endpoint dependencies, configuration injection

### Factory Pattern

Creational pattern for object instantiation.

**Usage**: `create_app()` function for FastAPI application

### Repository Pattern

Data access abstraction pattern.

**Usage**: MemU storage interface

### Singleton Pattern

Ensuring a class has only one instance.

**Usage**: Configuration object via `get_config()`

---

## Best Practices Referenced

### PEP 8

Python Enhancement Proposal 8 - Style Guide for Python Code

**Website**: <https://pep8.org/>

### Semantic Versioning

Version numbering scheme (MAJOR.MINOR.PATCH)

**Current Version**: 0.1.0

**Website**: <https://semver.org/>

### Twelve-Factor App

Methodology for building software-as-a-service applications.

**Applied**: Configuration via environment, stateless processes, port binding

**Website**: <https://12factor.net/>

---

## Research References

### Papers

1. **"Attention Is All You Need"** (Vaswani et al., 2017)
   - Introduced the Transformer architecture
   - Foundation for T5 and modern NLP

2. **"Exploring Transfer Learning with T5"** (Raffel et al., 2019)
   - T5 model paper
   - Text-to-text framework

3. **"LoRA: Low-Rank Adaptation of Large Language Models"** (Hu et al., 2021)
   - Parameter-efficient fine-tuning method
   - Used in Sono-Eval tag generator

4. **"Dark Horse: Achieving Success Through the Pursuit of Fulfillment"** (Rose & Ogas, 2018)
   - Book on individualized paths to success
   - Inspiration for micro-motive tracking

### Concepts

- **Explainable AI**: Making AI decisions transparent and interpretable
- **Transfer Learning**: Using pre-trained models for new tasks
- **Fine-Tuning**: Adapting pre-trained models to specific domains
- **Hierarchical Memory**: Multi-level data organization
- **Evidence-Based Assessment**: Scoring backed by concrete observations

---

## Command Reference

### CLI Commands

```bash
sono-eval assess run          # Run assessment
sono-eval candidate create    # Create candidate
sono-eval candidate list      # List candidates
sono-eval tag generate        # Generate tags
sono-eval server start        # Start API server
sono-eval config show         # Show configuration
```

### Launcher Commands

```bash
./launcher.sh start           # Start all services
./launcher.sh stop            # Stop all services
./launcher.sh restart         # Restart services
./launcher.sh status          # Show status
./launcher.sh logs            # View logs
./launcher.sh dev             # Setup dev environment
```

### Docker Commands

```bash
docker-compose up -d          # Start containers
docker-compose down           # Stop containers
docker-compose logs -f        # Follow logs
docker-compose ps             # List containers
```

---

## Environment Variables

Key configuration variables (see `.env.example` for complete list):

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_ENV` | Environment (development/production) | development |
| `API_PORT` | API server port | 8000 |
| `DATABASE_URL` | Database connection string | sqlite:///./sono_eval.db |
| `T5_MODEL_NAME` | T5 model to use | t5-base |
| `MEMU_MAX_DEPTH` | Max hierarchy depth | 5 |
| `ASSESSMENT_ENABLE_EXPLANATIONS` | Enable explanations | true |
| `DARK_HORSE_MODE` | Enable micro-motive tracking | enabled |

---

## Port Mappings

| Service | Port | Description |
|---------|------|-------------|
| API Server | 8000 | FastAPI REST API |
| PostgreSQL | 5432 | Database |
| Redis | 6379 | Cache/Queue |
| Superset | 8088 | Analytics Dashboard |

---

## Additional Resources

### Official Documentation

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [Transformers Docs](https://huggingface.co/docs/transformers)
- [Docker Docs](https://docs.docker.com/)
- [Superset Docs](https://superset.apache.org/docs/intro)

### Learning Resources

See `../../Guides/resources/learning.md` for tutorials and guides

### Community

- GitHub Issues: Bug reports and feature requests
- Discussions: Questions and ideas
- Contributing: See `CONTRIBUTING.md`

---

**Last Updated**: 2026-01-15
**Version**: 0.1.1
