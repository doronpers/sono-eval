# Sono-Eval

**Explainable Multi-Path Developer Assessment System**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Sono-Eval is a comprehensive developer assessment platform featuring:
- 🧠 **Explainable Scoring** - Evidence-based assessments with detailed explanations
- 🛤️ **Multi-Path Evaluation** - Technical, design, collaboration, and more
- 🎯 **Dark Horse Tracking** - Micro-motive analysis based on the tex-assist-coding model
- 🏷️ **Semantic Tagging** - T5 + PEFT (LoRA) for intelligent code tagging
- 💾 **Hierarchical Memory** - MemU persistent candidate memory storage
- 📊 **Analytics Dashboard** - Apache Superset for cohort insights
- 🚀 **Easy Deployment** - Docker + one-click launcher

---

## Table of Contents

- [Quick Start](#quick-start)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
  - [CLI](#cli)
  - [API](#api)
  - [Docker](#docker)
- [Configuration](#configuration)
- [Development](#development)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## Quick Start

### One-Click Launcher

```bash
# Clone the repository
git clone https://github.com/doronpers/sono-eval.git
cd sono-eval

# Start all services
./launcher.sh start

# Access the services
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - Superset: http://localhost:8088 (admin/admin)
```

### Local Development

```bash
# Setup development environment
./launcher.sh dev

# Activate virtual environment
source venv/bin/activate

# Run CLI
sono-eval --help

# Start API server
sono-eval server start
```

---

## Features

### 🧠 Explainable Assessment Engine

The core assessment engine provides:
- **Evidence-Based Scoring**: Every score backed by concrete evidence
- **Multi-Path Evaluation**: Technical, design, collaboration, problem-solving paths
- **Confidence Metrics**: Understand the reliability of assessments
- **Detailed Explanations**: Natural language explanations for all scores

Example assessment:
```python
from sono_eval.assessment import AssessmentEngine, AssessmentInput, PathType

engine = AssessmentEngine()
result = await engine.assess(AssessmentInput(
    candidate_id="candidate_001",
    submission_type="code",
    content={"code": "..."},
    paths_to_evaluate=[PathType.TECHNICAL, PathType.DESIGN]
))

print(f"Score: {result.overall_score}/100")
print(f"Summary: {result.summary}")
```

### 🎯 Dark Horse Micro-Motive Tracking

Based on the tex-assist-coding model, Sono-Eval tracks:
- **Mastery** - Deep technical skill development
- **Exploration** - Willingness to try new approaches
- **Collaboration** - Team-oriented behaviors
- **Innovation** - Creative problem-solving
- **Quality** - Attention to detail and craftsmanship

### 🏷️ Semantic Tagging with T5 + PEFT

Automated code tagging using:
- **T5 Base Model** - Pre-trained transformer for text generation
- **LoRA Fine-Tuning** - Parameter-efficient adaptation
- **Semantic Understanding** - Context-aware tag generation

```python
from sono_eval.tagging import TagGenerator

generator = TagGenerator()
tags = generator.generate_tags(code_text, max_tags=5)

for tag in tags:
    print(f"{tag.tag} ({tag.category}): {tag.confidence:.2f}")
```

### 💾 MemU Hierarchical Memory

Persistent, hierarchical storage for candidate data:
- **Multi-Level Structure** - Configurable depth (default: 5 levels)
- **Efficient Caching** - LRU cache for frequently accessed data
- **Version Control** - Track memory evolution over time
- **Fast Retrieval** - Optimized for quick access patterns

```python
from sono_eval.memory import MemUStorage

storage = MemUStorage()
memory = storage.create_candidate_memory("candidate_001")
storage.add_memory_node(
    "candidate_001",
    memory.root_node.node_id,
    data={"assessment": "results..."}
)
```

### 📊 Analytics with Apache Superset

Pre-configured dashboards for:
- **Candidate Performance** - Score trends and distributions
- **Cohort Analytics** - Comparative analysis across groups
- **Assessment Insights** - Deep dive into evaluation metrics
- **Micro-Motive Analysis** - Dark Horse model tracking

---

## Architecture

```
sono-eval/
├── src/sono_eval/           # Main package
│   ├── assessment/          # Assessment engine
│   │   ├── engine.py        # Core assessment logic
│   │   └── models.py        # Data models
│   ├── memory/              # MemU storage
│   │   └── memu.py          # Hierarchical memory
│   ├── tagging/             # Semantic tagging
│   │   ├── generator.py     # T5 tag generator
│   │   └── tagstudio.py     # File management
│   ├── api/                 # FastAPI backend
│   │   └── main.py          # REST endpoints
│   ├── cli/                 # CLI interface
│   │   └── main.py          # Click commands
│   └── utils/               # Utilities
│       ├── config.py        # Configuration
│       └── logger.py        # Logging
├── config/                  # Configuration files
│   └── superset/            # Superset config
├── docs/                    # Documentation
├── tests/                   # Test suite
├── docker-compose.yml       # Docker orchestration
├── Dockerfile               # Container definition
├── launcher.sh              # One-click launcher
└── pyproject.toml           # Package configuration
```

---

## Installation

### Prerequisites

- Python 3.9+
- Docker & Docker Compose (for containerized deployment)
- Git

### Option 1: Docker (Recommended)

```bash
git clone https://github.com/doronpers/sono-eval.git
cd sono-eval
./launcher.sh start
```

### Option 2: Local Installation

```bash
# Clone repository
git clone https://github.com/doronpers/sono-eval.git
cd sono-eval

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Copy environment configuration
cp .env.example .env
# Edit .env with your settings

# Initialize storage directories
mkdir -p data/memory data/tagstudio models/cache
```

---

## Usage

### CLI

The CLI provides commands for all major operations:

#### Configuration

```bash
# Show current configuration
sono-eval config show
```

#### Assessment

```bash
# Run assessment on a file
sono-eval assess run \
  --candidate-id candidate_001 \
  --file solution.py \
  --paths technical design \
  --output results.json

# View results
cat results.json
```

#### Candidate Management

```bash
# Create candidate
sono-eval candidate create --id candidate_001

# List candidates
sono-eval candidate list

# View candidate details
sono-eval candidate show --id candidate_001

# Delete candidate
sono-eval candidate delete --id candidate_001
```

#### Tagging

```bash
# Generate tags for file
sono-eval tag generate --file code.py --max-tags 5

# Generate tags from text
sono-eval tag generate --text "async function..." --max-tags 3
```

#### Server Management

```bash
# Start API server
sono-eval server start

# Start with custom settings
sono-eval server start --host 0.0.0.0 --port 9000 --reload
```

### API

The REST API provides programmatic access to all features.

#### Start the Server

```bash
sono-eval server start
# or
uvicorn sono_eval.api.main:app --reload
```

#### API Documentation

Interactive API docs available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

#### Example Requests

**Create Assessment:**
```bash
curl -X POST http://localhost:8000/api/v1/assessments \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": "candidate_001",
    "submission_type": "code",
    "content": {"code": "def hello(): return \"world\""},
    "paths_to_evaluate": ["TECHNICAL"]
  }'
```

**Generate Tags:**
```bash
curl -X POST http://localhost:8000/api/v1/tags/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "async function fetchData() { ... }",
    "max_tags": 5
  }'
```

**Create Candidate:**
```bash
curl -X POST http://localhost:8000/api/v1/candidates \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": "candidate_001",
    "initial_data": {"name": "John Doe"}
  }'
```

### Docker

Using Docker Compose for full deployment:

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after changes
docker-compose up -d --build
```

**Services:**
- **sono-eval**: Main application (port 8000)
- **postgres**: Database (port 5432)
- **redis**: Cache/queue (port 6379)
- **superset**: Analytics (port 8088)

---

## Configuration

Configuration is managed via environment variables. Copy `.env.example` to `.env` and customize:

```bash
# Application
APP_NAME=sono-eval
APP_ENV=development
DEBUG=true

# API Server
API_HOST=0.0.0.0
API_PORT=8000

# Database
DATABASE_URL=sqlite:///./sono_eval.db

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Assessment
ASSESSMENT_ENABLE_EXPLANATIONS=true
ASSESSMENT_MULTI_PATH_TRACKING=true
DARK_HORSE_MODE=enabled

# T5 Model
T5_MODEL_NAME=t5-base
T5_LORA_RANK=8
T5_LORA_ALPHA=16

# Storage
MEMU_STORAGE_PATH=./data/memory
MEMU_MAX_DEPTH=5
```

See `.env.example` for all available options.

---

## Development

### Setup Development Environment

```bash
# Use the launcher script
./launcher.sh dev

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/sono_eval --cov-report=html

# Run specific test file
pytest tests/test_assessment.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint
flake8 src/ tests/

# Type checking
mypy src/
```

### Project Structure

- `src/sono_eval/` - Main application code
- `tests/` - Test suite
- `docs/` - Documentation
- `config/` - Configuration files
- `scripts/` - Utility scripts

---

## Documentation

Additional documentation:

- **[API Reference](docs/api.md)** - Complete API documentation
- **[Assessment Guide](docs/assessment.md)** - Assessment system details
- **[Configuration](docs/configuration.md)** - Configuration options
- **[Development Guide](docs/development.md)** - Contributing guidelines
- **[Architecture](docs/architecture.md)** - System architecture

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contributing Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Format code (`black src/`)
6. Commit changes (`git commit -m 'Add amazing feature'`)
7. Push to branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

---

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

## Acknowledgments

- **Dark Horse Model** - Based on tex-assist-coding research
- **T5** - Google's Text-to-Text Transfer Transformer
- **PEFT** - Hugging Face Parameter-Efficient Fine-Tuning
- **Apache Superset** - Modern data exploration platform

---

## Support

- 📧 Email: support@sono-eval.local
- 💬 Issues: [GitHub Issues](https://github.com/doronpers/sono-eval/issues)
- 📖 Docs: [Documentation](docs/)

---

## Roadmap

- [ ] Batch assessment processing
- [ ] Web-based review interface
- [ ] Advanced onboarding analytics
- [ ] Multi-language support
- [ ] Real-time collaboration features
- [ ] Enhanced ML model fine-tuning tools
- [ ] Integration with popular code platforms

---

**Built with ❤️ by the Sono-Eval Team**
