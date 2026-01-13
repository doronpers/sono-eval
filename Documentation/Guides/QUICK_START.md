# Quick Start Guide

Get Sono-Eval running in 5 minutes! This guide will help you install, configure, and run your first assessment.

---

## ⚡ Prerequisites

Before starting, ensure you have:

- **Python 3.9+** installed ([Download](https://www.python.org/downloads/))
- **Docker & Docker Compose** (for containerized deployment)
- **Git** for cloning the repository

Check your versions:

```bash
python3 --version  # Should be 3.9 or higher
docker --version
docker-compose --version
```

---

## 🚀 Option 1: One-Click Docker Deployment (Recommended)

The fastest way to get started:

### Step 1: Clone the Repository

```bash
git clone https://github.com/doronpers/sono-eval.git
cd sono-eval
```

### Step 2: Start All Services

```bash
./launcher.sh start
```

That's it! The launcher will:

- Create `.env` from `.env.example` if needed
- Start all Docker containers
- Display service URLs

### Step 3: Access Services

```bash
# API Documentation (interactive)
open http://localhost:8000/docs

# API Server
curl http://localhost:8000/api/v1/health

# Analytics Dashboard (login: admin/admin)
open http://localhost:8088
```

### Step 4: Run Your First Assessment

Using the CLI in Docker:

```bash
./launcher.sh cli assess run \
  --candidate-id demo_user \
  --content "def hello(): return 'world'" \
  --paths technical
```

Using curl:

```bash
curl -X POST http://localhost:8000/api/v1/assessments \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": "demo_user",
    "submission_type": "code",
    "content": {"code": "def hello(): return \"world\""},
    "paths_to_evaluate": ["TECHNICAL"]
  }'
```

---

## 🐍 Option 2: Local Python Installation

For development or if you prefer not to use Docker:

### Step 1: Clone and Setup

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
```

### Step 2: Configure Environment

```bash
# Copy example configuration
cp .env.example .env

# Edit if needed (optional for quick start)
nano .env
```

### Step 3: Initialize Storage

```bash
# Create data directories
mkdir -p data/memory data/tagstudio models/cache
```

### Step 4: Verify Installation

```bash
# Check CLI is working
sono-eval --version

# Show configuration
sono-eval config show
```

### Step 5: Run Your First Assessment

```bash
# Create a sample file
cat > sample.py << 'EOF'
def factorial(n):
    """Calculate factorial of n."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)
EOF

# Run assessment
sono-eval assess run \
  --candidate-id demo_user \
  --file sample.py \
  --paths technical design \
  --output results.json

# View results
cat results.json | python -m json.tool
```

### Step 6: Start API Server (Optional)

```bash
# Start in development mode
sono-eval server start --reload

# Access at http://localhost:8000/docs
```

---

## 📊 Common Operations

### Create a Candidate

```bash
sono-eval candidate create --id candidate_001
```

### List All Candidates

```bash
sono-eval candidate list
```

### View Candidate Details

```bash
sono-eval candidate show --id candidate_001
```

### Generate Code Tags

```bash
sono-eval tag generate --file mycode.js --max-tags 5
```

### Run Multi-Path Assessment

```bash
sono-eval assess run \
  --candidate-id candidate_001 \
  --file solution.py \
  --paths technical design collaboration \
  --output full_assessment.json
```

---

## 🔧 Configuration

### Essential Settings

The default configuration works out of the box, but you can customize:

```bash
# .env file
APP_ENV=development           # development or production
DEBUG=true                    # Enable debug logging

API_HOST=0.0.0.0             # API server host
API_PORT=8000                # API server port

MEMU_STORAGE_PATH=./data/memory        # Where to store candidate data
ASSESSMENT_ENABLE_EXPLANATIONS=true    # Include explanations
DARK_HORSE_MODE=enabled                # Enable micro-motive tracking
```

See the [Configuration Guide](user-guide/configuration.md) for all options.

---

## 📈 Next Steps

### Learn More

- **[User Guide](user-guide/installation.md)** - Detailed installation and usage
- **[API Reference](user-guide/api-reference.md)** - Complete API documentation
- **[CLI Reference](user-guide/cli-reference.md)** - All CLI commands
- **[Concepts](concepts/architecture.md)** - Understand the architecture

### Try Advanced Features

- **Multi-Path Assessment** - Evaluate across all dimensions
- **Semantic Tagging** - Auto-tag code with T5 model
- **Memory Storage** - Track candidate progress over time
- **Analytics** - Visualize results in Superset dashboards

### Customize

- **[Configuration](user-guide/configuration.md)** - Tune settings for your needs
- **[Examples](resources/examples/)** - Practical code examples
- **[API Integration](user-guide/api-reference.md)** - Integrate with your systems

---

## 🐛 Troubleshooting

### Docker Issues

**Services won't start:**

```bash
# Check Docker is running
docker ps

# View logs
./launcher.sh logs

# Restart services
./launcher.sh restart
```

**Port conflicts:**

```bash
# Edit docker-compose.yml and change ports
# Or stop conflicting services
```

### Local Installation Issues

**Import errors:**

```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Reinstall in editable mode
pip install -e .
```

**Permission errors:**

```bash
# Ensure data directories are writable
chmod -R 755 data/
```

**Model download issues:**

```bash
# T5 model downloads on first use - requires internet
# Check connection and disk space
```

See the full [Troubleshooting Guide](troubleshooting.md) for more help.

---

## ✅ Verification

To verify everything is working:

### Docker Deployment

```bash
# Check all services are running
./launcher.sh status

# Test API
curl http://localhost:8000/api/v1/health

# Run test assessment
./launcher.sh cli assess run --candidate-id test --content "print('test')" --paths technical
```

### Local Installation

```bash
# Run tests
pytest

# Start server
sono-eval server start &

# Test API
curl http://localhost:8000/api/v1/health

# Run assessment
sono-eval assess run --candidate-id test --content "print('test')" --paths technical
```

---

## 🎉 You're Ready

Congratulations! You now have Sono-Eval running. Here are some things to try:

1. **Assess some real code** from your projects
2. **Explore the API docs** at <http://localhost:8000/docs>
3. **Create dashboards** in Superset for your assessments
4. **Integrate with your CI/CD** pipeline

Need help? Check the [documentation](README.md) or [open an issue](https://github.com/doronpers/sono-eval/issues).

---

**Estimated Time**: 5 minutes
**Difficulty**: Beginner
**Next**: [User Guide](user-guide/installation.md) | [API Reference](user-guide/api-reference.md) | [Examples](resources/examples/)
