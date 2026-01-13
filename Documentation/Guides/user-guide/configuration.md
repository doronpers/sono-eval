# Configuration Guide

Complete guide to configuring Sono-Eval for your needs.

---

## Overview

Sono-Eval uses environment variables for configuration, managed through a `.env` file. This approach follows the [Twelve-Factor App](https://12factor.net/) methodology for portable, secure configuration.

---

## Quick Configuration

### Step 1: Create Configuration File

```bash
# Copy example configuration
cp .env.example .env
```

### Step 2: Edit Settings

```bash
# Edit with your preferred editor
nano .env
# or
vim .env
# or
code .env
```

### Step 3: Verify Configuration

```bash
sono-eval config show
```

---

## Configuration Sections

### Application Settings

```bash
# Application name
APP_NAME=sono-eval

# Environment: development, staging, production
APP_ENV=development

# Enable debug mode (verbose logging)
DEBUG=true

# Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO
```

**Recommendations:**

- Use `development` for local work
- Use `staging` for pre-production testing
- Use `production` for live deployment
- Set `DEBUG=false` in production

---

### API Server Settings

```bash
# Host to bind to
API_HOST=0.0.0.0

# Port to listen on
API_PORT=8000

# Number of worker processes
API_WORKERS=4
```

**Host Options:**

- `0.0.0.0` - Listen on all interfaces (accessible externally)
- `127.0.0.1` - Localhost only (more secure for development)

**Port Selection:**

- Default `8000` - Standard for development
- Choose available port if 8000 is in use
- Use standard ports (80/443) in production with reverse proxy

**Workers:**

- `1` - Single process (easier debugging)
- `4` - Good for development
- `CPU_COUNT * 2 + 1` - Production recommendation

---

### Database Settings

```bash
# SQLite (default, no setup needed)
DATABASE_URL=sqlite:///./sono_eval.db

# PostgreSQL (production)
# DATABASE_URL=postgresql://user:password@localhost:5432/sono_eval

# Connection pool settings (PostgreSQL only)
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
```

**Database Options:**

**SQLite** (Default):

- ✅ No setup required
- ✅ Perfect for development
- ✅ Self-contained file
- ⚠️ Limited concurrency
- ⚠️ Not recommended for production

**PostgreSQL** (Production):

- ✅ Better performance
- ✅ Better concurrency
- ✅ Better for multi-user
- ⚠️ Requires separate installation

**Setup PostgreSQL:**

```bash
# Install PostgreSQL
# Ubuntu/Debian: sudo apt-get install postgresql
# macOS: brew install postgresql

# Create database
createdb sono_eval

# Update .env
DATABASE_URL=postgresql://username:password@localhost:5432/sono_eval
```

---

### Redis Settings

```bash
# Redis host
REDIS_HOST=localhost

# Redis port
REDIS_PORT=6379

# Redis database number (0-15)
REDIS_DB=0

# Redis password (if required)
REDIS_PASSWORD=
```

**Redis Usage:**

- Caching assessment results
- Session storage
- Task queue backend
- Superset caching

**Setup Redis:**

```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis

# Start Redis
redis-server
```

---

### MemU Storage Settings

```bash
# Where to store candidate memory data
MEMU_STORAGE_PATH=./data/memory

# Maximum hierarchy depth (1-10)
MEMU_MAX_DEPTH=5

# LRU cache size (number of candidates in memory)
MEMU_CACHE_SIZE=1000
```

**Storage Path:**

- Use absolute path in production
- Ensure directory is writable
- Backup this directory regularly

**Max Depth:**

- `3` - Shallow hierarchy (simple use)
- `5` - Default (balanced)
- `7-10` - Deep hierarchy (complex tracking)

**Cache Size:**

- `100` - Small deployment
- `1000` - Default (medium)
- `10000` - Large deployment

---

### T5 Model Settings

```bash
# T5 model variant
T5_MODEL_NAME=t5-base

# Where to cache downloaded models
T5_CACHE_DIR=./models/cache

# LoRA configuration
T5_LORA_RANK=8
T5_LORA_ALPHA=16
T5_LORA_DROPOUT=0.1
```

**Model Options:**

- `t5-small` - Fast, less accurate (60MB)
- `t5-base` - Balanced (220MB) ⭐ Recommended
- `t5-large` - Better quality (850MB)
- `t5-3b` - Best quality (11GB, requires GPU)

**Cache Directory:**

- Models download on first use (~220MB for t5-base)
- Ensure sufficient disk space
- Reused across runs

**LoRA Settings:**

- Default values work well
- Higher rank = more parameters = better quality
- Lower rank = faster fine-tuning

---

### TagStudio Settings

```bash
# Root directory for tagged files
TAGSTUDIO_ROOT=./data/tagstudio

# Automatically tag files on import
TAGSTUDIO_AUTO_TAG=true
```

---

### Assessment Engine Settings

```bash
# Engine version
ASSESSMENT_ENGINE_VERSION=1.0

# Generate natural language explanations
ASSESSMENT_ENABLE_EXPLANATIONS=true

# Track multiple assessment paths
ASSESSMENT_MULTI_PATH_TRACKING=true

# Enable Dark Horse micro-motive tracking
DARK_HORSE_MODE=enabled
```

**Explanations:**

- `true` - Include detailed explanations (recommended)
- `false` - Scores only (faster)

**Multi-Path Tracking:**

- `true` - Evaluate across all paths
- `false` - Single path only

**Dark Horse Mode:**

- `enabled` - Track micro-motives
- `disabled` - Skip motive analysis

---

### Superset Settings

```bash
# Superset host
SUPERSET_HOST=localhost

# Superset port
SUPERSET_PORT=8088

# Superset secret key (change in production!)
SUPERSET_SECRET_KEY=change_this_secret_key_in_production
```

**Important:** Always change `SUPERSET_SECRET_KEY` in production!

---

### Security Settings

```bash
# Application secret key (for sessions, tokens, etc.)
SECRET_KEY=your-secret-key-here-change-in-production

# Allowed hosts (comma-separated)
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS origins (comma-separated, or * for all)
CORS_ORIGINS=*
```

**Production Security:**

- Generate strong random SECRET_KEY
- Restrict ALLOWED_HOSTS to your domains
- Limit CORS_ORIGINS to specific origins
- Use HTTPS/TLS

**Generate Secret Key:**

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

### File Upload Settings

```bash
# Maximum upload size in bytes (10MB default)
MAX_UPLOAD_SIZE=10485760

# Allowed file extensions (comma-separated)
ALLOWED_EXTENSIONS=py,js,ts,java,cpp,c,go,rs,rb,kt,swift
```

---

### Batch Processing Settings

```bash
# Batch size for concurrent processing
BATCH_SIZE=32

# Maximum concurrent assessments
MAX_CONCURRENT_ASSESSMENTS=4
```

---

## Configuration Profiles

### Development Profile

Optimized for local development:

```bash
APP_ENV=development
DEBUG=true
LOG_LEVEL=DEBUG
API_HOST=127.0.0.1
API_PORT=8000
API_WORKERS=1
DATABASE_URL=sqlite:///./sono_eval.db
MEMU_CACHE_SIZE=100
T5_MODEL_NAME=t5-small
ASSESSMENT_ENABLE_EXPLANATIONS=true
```

### Staging Profile

For testing before production:

```bash
APP_ENV=staging
DEBUG=false
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=2
DATABASE_URL=postgresql://user:pass@db:5432/sono_eval
MEMU_CACHE_SIZE=500
T5_MODEL_NAME=t5-base
ASSESSMENT_ENABLE_EXPLANATIONS=true
```

### Production Profile

Optimized for production use:

```bash
APP_ENV=production
DEBUG=false
LOG_LEVEL=WARNING
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=8
DATABASE_URL=postgresql://user:pass@db:5432/sono_eval
REDIS_HOST=redis
MEMU_CACHE_SIZE=10000
T5_MODEL_NAME=t5-base
ASSESSMENT_ENABLE_EXPLANATIONS=true
SECRET_KEY=<GENERATE_STRONG_KEY>
ALLOWED_HOSTS=yourdomain.com
CORS_ORIGINS=https://yourdomain.com
```

---

## Environment-Specific Configuration

### Using Multiple .env Files

Create environment-specific files:

```bash
.env.development
.env.staging
.env.production
```

Load appropriate file:

```bash
# Development
cp .env.development .env

# Staging
cp .env.staging .env

# Production
cp .env.production .env
```

---

## Docker Configuration

When using Docker, environment variables can be:

1. **In .env file** (recommended):

```bash
# .env is automatically loaded by docker-compose
./launcher.sh start
```

2. **In docker-compose.yml**:

```yaml
environment:
  - APP_ENV=production
  - DEBUG=false
```

3. **At runtime**:

```bash
docker-compose run -e APP_ENV=production sono-eval
```

---

## Configuration Validation

### Check Current Configuration

```bash
sono-eval config show
```

### Validate Configuration

```bash
# Start server in test mode
sono-eval server start --reload

# Check health endpoint
curl http://localhost:8000/api/v1/health
```

---

## Common Configuration Scenarios

### Scenario 1: Local Development

```bash
APP_ENV=development
DEBUG=true
DATABASE_URL=sqlite:///./sono_eval.db
API_WORKERS=1
```

### Scenario 2: Team Server

```bash
APP_ENV=development
API_HOST=0.0.0.0
DATABASE_URL=postgresql://team:pass@db:5432/sono_eval
REDIS_HOST=redis
API_WORKERS=4
```

### Scenario 3: Production Deployment

```bash
APP_ENV=production
DEBUG=false
DATABASE_URL=postgresql://prod:pass@db:5432/sono_eval
REDIS_HOST=redis
API_WORKERS=8
SECRET_KEY=<STRONG_KEY>
ALLOWED_HOSTS=app.company.com
```

---

## Troubleshooting

### Configuration Not Loading

```bash
# Verify .env exists
ls -la .env

# Check file permissions
chmod 644 .env

# Check for syntax errors
cat .env | grep -v '^#' | grep -v '^$'
```

### Database Connection Issues

```bash
# Test PostgreSQL connection
psql -h localhost -U username -d sono_eval

# Check DATABASE_URL format
# postgresql://username:password@host:port/database
```

### Redis Connection Issues

```bash
# Test Redis connection
redis-cli ping

# Should respond with: PONG
```

### Model Download Issues

```bash
# Check internet connection
# Check disk space
df -h ./models/cache

# Manually download (if needed)
python -c "from transformers import T5ForConditionalGeneration; T5ForConditionalGeneration.from_pretrained('t5-base')"
```

---

## Security Best Practices

1. **Never commit .env to git** (it's in .gitignore)
2. **Use strong SECRET_KEY in production**
3. **Restrict ALLOWED_HOSTS and CORS_ORIGINS**
4. **Use HTTPS/TLS in production**
5. **Rotate secrets regularly**
6. **Use environment-specific configurations**
7. **Limit file upload sizes**
8. **Use strong database passwords**

---

## See Also

- [Installation Guide](installation.md) - Setup instructions
- [Quick Start](../quick-start.md) - Get started quickly
- [Troubleshooting](../troubleshooting.md) - Common issues
- [Architecture](../concepts/architecture.md) - System design

---

**Last Updated**: January 10, 2026
**Version**: 0.1.0
