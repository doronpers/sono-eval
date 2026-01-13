# Configuration Presets Guide

Sono-Eval provides optimized configuration presets for different use cases. These
presets help you get started quickly with sensible defaults.

---

## Available Presets

### Quick Test (`quick_test`)

**Purpose**: Fast setup for quick testing and demos

**Best For**:

- Quick demonstrations
- Testing basic functionality
- Minimal resource usage

**Key Settings**:

- Single API worker
- Minimal logging (ERROR only)
- Single path assessment only
- Small cache (100 entries)
- No auto-tagging

**Usage**:

```bash
# Apply preset
sono-eval config apply-preset --preset quick_test --output .env
```

---

### Development (`development`)

**Purpose**: Full-featured development environment

**Best For**:

- Local development
- Feature development
- Testing all features

**Key Settings**:

- 2 API workers
- INFO level logging
- All assessment paths enabled
- Dark Horse mode enabled
- Auto-tagging enabled
- Standard T5 model

**Usage**:

```bash
sono-eval config apply-preset --preset development --output .env
```

---

### Testing (`testing`)

**Purpose**: Optimized for running automated tests

**Best For**:

- Unit tests
- Integration tests
- CI/CD pipelines

**Key Settings**:

- Single worker
- WARNING level logging
- In-memory SQLite database
- Port 8001 (avoids conflicts)
- Minimal cache
- No auto-tagging

**Usage**:

```bash
sono-eval config apply-preset --preset testing --output .env
```

---

### Staging (`staging`)

**Purpose**: Pre-production environment

**Best For**:

- Staging deployments
- Pre-production testing
- Performance testing

**Key Settings**:

- 3 API workers
- INFO level logging
- All features enabled
- Larger cache (2000 entries)
- Higher concurrency (4 assessments)
- Security settings must be configured

**Usage**:

```bash
sono-eval config apply-preset --preset staging --output .env
# Then set required security values:
# SECRET_KEY=<strong-key>
# ALLOWED_HOSTS=<your-domains>
```

---

### Production (`production`)

**Purpose**: Production-ready configuration

**Best For**:

- Production deployments
- High-availability setups
- Enterprise use

**Key Settings**:

- 4 API workers
- INFO level logging
- All features enabled
- Large cache (5000 entries)
- High concurrency (8 assessments)
- **Security**: Must configure SECRET_KEY, ALLOWED_HOSTS, database

**Usage**:

```bash
sono-eval config apply-preset --preset production --output .env
# Then configure:
# SECRET_KEY=<generate-strong-key>
# ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com
# DATABASE_URL=postgresql://user:pass@host:5432/db
# SUPERSET_SECRET_KEY=<generate-strong-key>
```

---

### High Performance (`high_performance`)

**Purpose**: Maximum performance settings

**Best For**:

- High-traffic deployments
- Batch processing
- Performance-critical applications

**Key Settings**:

- 8 API workers
- WARNING level logging (less overhead)
- Very large cache (10000 entries)
- High concurrency (16 assessments)
- Large batch size (128)

**Usage**:

```bash
sono-eval config apply-preset --preset high_performance --output .env
```

---

### Low Resource (`low_resource`)

**Purpose**: Minimal resource usage

**Best For**:

- Resource-constrained environments
- Small deployments
- Development on low-end machines

**Key Settings**:

- Single worker
- ERROR level logging
- Minimal cache (50 entries)
- Single path assessment
- Smaller T5 model (t5-small)
- No auto-tagging

**Usage**:

```bash
sono-eval config apply-preset --preset low_resource --output .env
```

---

### ML Development (`ml_development`)

**Purpose**: ML model development and training

**Best For**:

- Training ML models
- Fine-tuning T5 models
- ML experimentation

**Key Settings**:

- DEBUG level logging (verbose)
- Higher LoRA rank (16) and alpha (32)
- All features enabled
- Standard T5 model
- Moderate cache

**Usage**:

```bash
sono-eval config apply-preset --preset ml_development --output .env
```

---

## Using Presets

### List All Presets

```bash
sono-eval config list-presets
```

### View Preset Values

```bash
sono-eval config apply-preset --preset development
```

### Apply Preset to .env File

```bash
# Save preset to .env file
sono-eval config apply-preset --preset production --output .env

# Review and edit if needed
nano .env

# Set required values (SECRET_KEY, etc.)
```

### Apply Preset Programmatically

```python
from sono_eval.utils.config import Config
import os

# Get preset values
preset = Config.get_preset("development")

# Apply to environment
for key, value in preset.items():
    os.environ[key] = str(value)

# Now get config (will use preset values)
from sono_eval.utils.config import get_config
config = get_config()
```

---

## Preset Comparison

Preset | Workers | Cache | Concurrency | Logging | Use Case
--------|---------|-------|-------------|---------|----------
quick_test | 1 | 100 | 1 | ERROR | Quick demos
development | 2 | 500 | 2 | INFO | Local dev
testing | 1 | 50 | 1 | WARNING | Tests
staging | 3 | 2000 | 4 | INFO | Pre-prod
production | 4 | 5000 | 8 | INFO | Production
high_performance | 8 | 10000 | 16 | WARNING | High traffic
low_resource | 1 | 50 | 1 | ERROR | Low resources
ml_development | 2 | 1000 | 2 | DEBUG | ML training

---

## Customizing Presets

Presets provide sensible defaults, but you can customize them:

```bash
# Apply preset
sono-eval config apply-preset --preset development --output .env

# Edit .env to override specific values
nano .env

# Add custom overrides
API_WORKERS=3
LOG_LEVEL=DEBUG
```

---

## Security Notes

**Important**: Production and staging presets require you to set:

1. **SECRET_KEY**: Generate a strong random key

   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **ALLOWED_HOSTS**: Set specific domains (comma-separated)

   ```bash
   ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com
   ```

3. **DATABASE_URL**: Use PostgreSQL in production

   ```bash
   DATABASE_URL=postgresql://user:password@host:5432/sono_eval
   ```

4. **SUPERSET_SECRET_KEY**: Generate a strong key

   ```bash
   openssl rand -base64 42
   ```

---

## Recommendations

### For Development

- Start with `development` preset
- Adjust logging to DEBUG if needed
- Enable all features for testing

### For Testing

- Use `testing` preset
- In-memory database for speed
- Minimal resources

### For Production

- Use `production` preset
- **Must** configure all security settings
- Use PostgreSQL, not SQLite
- Set up proper monitoring

### For High Traffic

- Use `high_performance` preset
- Monitor resource usage
- Adjust workers based on CPU cores
- Consider horizontal scaling

---

## See Also

- [Configuration Guide](configuration.md) - Complete configuration reference
- [Installation Guide](installation.md) - Setup instructions
- [Troubleshooting](../troubleshooting.md) - Common issues

---

**Last Updated**: January 10, 2026
