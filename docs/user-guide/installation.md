# Installation Guide

Complete guide to installing and setting up Sono-Eval.

---

## Quick Overview

**Choose your installation method:**

| Method | Best For | Time | Difficulty |
|--------|----------|------|------------|
| [Docker](#docker-installation-recommended) | Production, quick start | 5 min | Easy |
| [Local Python](#local-python-installation) | Development | 10 min | Medium |
| [From Source](#from-source-installation) | Contributing | 15 min | Medium |

---

## Prerequisites

### Required
- **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Install Git](https://git-scm.com/downloads)

### Optional (for Docker)
- **Docker** - [Get Docker](https://www.docker.com/get-started)
- **Docker Compose** - Usually included with Docker Desktop

### Verify Prerequisites
```bash
# Check Python version (must be 3.9+)
python3 --version

# Check Git
git --version

# Check Docker (if using Docker method)
docker --version
docker-compose --version
```

---

## Docker Installation (Recommended)

Best for: Production deployment, quick evaluation, team environments

### Step 1: Clone Repository
```bash
git clone https://github.com/doronpers/sono-eval.git
cd sono-eval
```

### Step 2: Configure (Optional)
```bash
# Configuration is automatic, but you can customize
cp .env.example .env
nano .env  # Edit if desired
```

### Step 3: Start Services
```bash
./launcher.sh start
```

The launcher will:
- Create `.env` if it doesn't exist
- Pull/build Docker images
- Start all containers (sono-eval, PostgreSQL, Redis, Superset)
- Display service URLs

### Step 4: Verify Installation
```bash
# Check services are running
./launcher.sh status

# Test API
curl http://localhost:8000/api/v1/health

# View logs
./launcher.sh logs
```

### Step 5: Access Services
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (interactive)
- **Superset**: http://localhost:8088 (login: admin/admin)

### Docker Commands
```bash
# Start services
./launcher.sh start

# Stop services
./launcher.sh stop

# Restart services
./launcher.sh restart

# View logs
./launcher.sh logs

# Check status
./launcher.sh status

# Run CLI commands
./launcher.sh cli candidate list
```

---

## Local Python Installation

Best for: Local development, customization, no Docker

### Step 1: Clone Repository
```bash
git clone https://github.com/doronpers/sono-eval.git
cd sono-eval
```

### Step 2: Create Virtual Environment
```bash
# Create venv
python3 -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
# Install requirements
pip install --upgrade pip
pip install -r requirements.txt

# Install Sono-Eval in editable mode
pip install -e .

# Install development dependencies (optional)
pip install -e ".[dev]"
```

### Step 4: Configure
```bash
# Copy example configuration
cp .env.example .env

# Edit configuration
nano .env
```

**Minimum configuration for local dev:**
```bash
APP_ENV=development
DEBUG=true
DATABASE_URL=sqlite:///./sono_eval.db
API_PORT=8000
```

### Step 5: Initialize Storage
```bash
# Create data directories
mkdir -p data/memory data/tagstudio models/cache

# Verify permissions
chmod -R 755 data/
```

### Step 6: Verify Installation
```bash
# Check CLI works
sono-eval --version

# Show configuration
sono-eval config show

# Run tests (if dev dependencies installed)
pytest
```

### Step 7: Start Using
```bash
# Option 1: Use CLI directly
sono-eval assess run --candidate-id test --content "print('hello')" --paths technical

# Option 2: Start API server
sono-eval server start --reload

# Option 3: Use as Python package
python
>>> from sono_eval.assessment import AssessmentEngine
>>> engine = AssessmentEngine()
```

---

## From Source Installation

Best for: Contributors, advanced customization

### Step 1: Fork and Clone
```bash
# Fork on GitHub first, then:
git clone https://github.com/YOUR-USERNAME/sono-eval.git
cd sono-eval

# Add upstream remote
git remote add upstream https://github.com/doronpers/sono-eval.git
```

### Step 2: Setup Development Environment
```bash
# Use the dev setup script
./launcher.sh dev

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e ".[dev]"
```

### Step 3: Install Pre-commit Hooks (Optional)
```bash
# Install pre-commit
pip install pre-commit

# Setup hooks
pre-commit install
```

### Step 4: Verify Setup
```bash
# Run tests
pytest

# Run linter
flake8 src/ tests/

# Run type checker
mypy src/

# Format code
black src/ tests/
```

### Step 5: Create Branch
```bash
git checkout -b feature/your-feature-name
```

---

## Platform-Specific Notes

### Linux (Ubuntu/Debian)

**Install system dependencies:**
```bash
sudo apt-get update
sudo apt-get install -y \
    python3.9 python3.9-venv python3-pip \
    git build-essential python3-dev \
    docker.io docker-compose
```

**Add user to docker group:**
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Linux (RHEL/CentOS/Fedora)

```bash
sudo dnf install -y \
    python39 python39-devel \
    git gcc gcc-c++ \
    docker docker-compose
```

### macOS

**Using Homebrew:**
```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python@3.9 git docker docker-compose

# Start Docker Desktop
open -a Docker
```

### Windows

**Using WSL2 (Recommended):**
1. Install [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install)
2. Install Ubuntu from Microsoft Store
3. Follow Linux instructions inside WSL2

**Native Windows:**
1. Install [Python 3.9+](https://www.python.org/downloads/windows/)
2. Install [Git for Windows](https://git-scm.com/download/win)
3. Install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
4. Use PowerShell or Command Prompt
5. Replace `./launcher.sh` with manual Docker commands or WSL

---

## Database Setup

### SQLite (Default)
No setup needed! SQLite is included with Python.

**Pros**: Zero configuration, easy for development  
**Cons**: Limited concurrency, not recommended for production

### PostgreSQL (Production)

**Install PostgreSQL:**
```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql

# Start PostgreSQL
sudo systemctl start postgresql  # Linux
brew services start postgresql   # macOS
```

**Create database:**
```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE sono_eval;
CREATE USER sono_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE sono_eval TO sono_user;
\q
```

**Update configuration:**
```bash
# Edit .env
DATABASE_URL=postgresql://sono_user:secure_password@localhost:5432/sono_eval
```

---

## Redis Setup (Optional)

Redis improves performance but is optional for local development.

**Install Redis:**
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis

# Start Redis
sudo systemctl start redis    # Linux
brew services start redis     # macOS
```

**Update configuration:**
```bash
# Edit .env
REDIS_HOST=localhost
REDIS_PORT=6379
```

**Test connection:**
```bash
redis-cli ping
# Should return: PONG
```

---

## Verifying Installation

### Health Checks

**1. Check CLI:**
```bash
sono-eval --version
# Should show: 0.1.0

sono-eval config show
# Should display configuration
```

**2. Test Assessment:**
```bash
sono-eval assess run \
  --candidate-id test_user \
  --content "def hello(): return 'world'" \
  --paths technical
# Should complete and show score
```

**3. Test API:**
```bash
# Start server
sono-eval server start &

# Wait a moment, then test
curl http://localhost:8000/api/v1/health
# Should return: {"status": "healthy", ...}

# Stop server
pkill -f "sono-eval server"
```

**4. Run Tests (dev install):**
```bash
pytest -v
# Should run and pass all tests
```

---

## Post-Installation

### Recommended Next Steps

1. **Read Quick Start**: [docs/quick-start.md](../quick-start.md)
2. **Configure**: [docs/user-guide/configuration.md](../user-guide/configuration.md)
3. **Try Examples**: [docs/resources/examples/](../resources/examples/)
4. **Explore API**: http://localhost:8000/docs

### Optional Setup

**Create config profiles:**
```bash
# Development
cp .env .env.development

# Production
cp .env .env.production
# Edit .env.production with production settings
```

**Setup log rotation:**
```bash
# Create logrotate config
sudo nano /etc/logrotate.d/sono-eval
```

**Configure backups:**
```bash
# Backup script
mkdir -p backups
tar -czf backups/sono-eval-$(date +%Y%m%d).tar.gz data/
```

---

## Troubleshooting

### Common Installation Issues

**Problem**: `python3: command not found`  
**Solution**: Install Python 3.9+ from python.org

**Problem**: `Permission denied` when running Docker  
**Solution**: Add user to docker group (see Linux section)

**Problem**: `Port 8000 already in use`  
**Solution**: Change `API_PORT` in `.env` or stop conflicting service

**Problem**: `ModuleNotFoundError: No module named 'sono_eval'`  
**Solution**: Activate venv and run `pip install -e .`

**Problem**: Model download fails  
**Solution**: Check internet connection, disk space, and retry

For more issues, see [Troubleshooting Guide](../troubleshooting.md).

---

## Upgrading

### Docker Deployment
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

### Local Installation
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Reinstall package
pip install -e .

# Run migrations (if any)
alembic upgrade head
```

---

## Uninstalling

### Docker Deployment
```bash
# Stop and remove containers
docker-compose down

# Remove volumes (WARNING: deletes data)
docker-compose down -v

# Remove repository
cd .. && rm -rf sono-eval
```

### Local Installation
```bash
# Deactivate virtual environment
deactivate

# Remove repository
cd .. && rm -rf sono-eval
```

---

## Getting Help

- **Documentation**: [docs/README.md](../README.md)
- **Troubleshooting**: [docs/troubleshooting.md](../troubleshooting.md)
- **FAQ**: [docs/faq.md](../faq.md)
- **Issues**: [GitHub Issues](https://github.com/doronpers/sono-eval/issues)

---

**Last Updated**: January 10, 2026  
**Version**: 0.1.0
