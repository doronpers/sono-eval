# Troubleshooting Guide

Solutions to common issues when using Sono-Eval.

---

## Quick Diagnostics

### Check System Health

```bash
# Check if services are running
./launcher.sh status

# View recent logs
./launcher.sh logs --tail=50

# Test API health
curl http://localhost:8000/api/v1/health

# Verify configuration
sono-eval config show
```

---

## Installation Issues

### Docker Not Found

**Symptoms**: `docker: command not found`

**Solution**:

```bash
# Install Docker
# Ubuntu/Debian
sudo apt-get update && sudo apt-get install docker.io docker-compose

# macOS
brew install docker docker-compose

# Verify installation
docker --version
docker-compose --version
```

### Permission Denied (Docker)

**Symptoms**: `Permission denied while trying to connect to Docker daemon`

**Solution**:

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and back in, or run:
newgrp docker

# Verify
docker ps
```

### Port Already in Use

**Symptoms**: `Bind for 0.0.0.0:8000 failed: port is already allocated`

**Solution**:

**Option 1**: Stop the conflicting service

```bash
# Find what's using the port
sudo lsof -i :8000
# or
sudo netstat -tulpn | grep 8000

# Kill the process
sudo kill <PID>
```

**Option 2**: Change Sono-Eval port

```bash
# Edit .env
API_PORT=9000

# Or edit docker-compose.yml
ports:
  - "9000:8000"
```

### Python Version Too Old

**Symptoms**: `Python 3.9+ required`

**Solution**:

```bash
# Check current version
python3 --version

# Install Python 3.9+
# Ubuntu/Debian
sudo apt-get install python3.9 python3.9-venv

# macOS
brew install python@3.9

# Use specific version
python3.9 -m venv venv
```

### Pip Install Fails

**Symptoms**: `ERROR: Could not install packages`

**Solution**:

```bash
# Upgrade pip
pip install --upgrade pip

# Install build tools
# Ubuntu/Debian
sudo apt-get install python3-dev build-essential

# macOS
xcode-select --install

# Retry with verbose output
pip install -r requirements.txt -v
```

---

## Runtime Issues

### Assessment Taking Forever

**Symptoms**: Assessment hangs or takes >5 minutes

**Causes & Solutions**:

**1. First-time model download**:

```bash
# T5 model downloads on first use (~2GB)
# Check download progress in logs
./launcher.sh logs -f

# Pre-download manually
python -c "from transformers import T5ForConditionalGeneration; T5ForConditionalGeneration.from_pretrained('t5-base')"
```

**2. Insufficient memory**:

```bash
# Check available memory
free -h

# Increase Docker memory (Docker Desktop settings)
# Or use smaller model:
T5_MODEL_NAME=t5-small
```

**3. CPU overload**:

```bash
# Check CPU usage
top

# Reduce concurrent assessments
MAX_CONCURRENT_ASSESSMENTS=1
```

### API Returns 500 Error

**Symptoms**: `{"detail": "Internal Server Error"}`

**Diagnosis**:

```bash
# Check server logs
./launcher.sh logs sono-eval

# Look for stack traces and error messages
```

**Common Causes**:

**1. Database connection failed**:

```bash
# Verify database is running
docker-compose ps postgres

# Test connection
psql -h localhost -U <user> -d sono_eval

# Check DATABASE_URL in .env
```

**2. Redis connection failed**:

```bash
# Verify Redis is running
docker-compose ps redis

# Test connection
redis-cli ping
# Should return: PONG
```

**3. Model loading error**:

```bash
# Check model cache
ls -lh models/cache/

# Clear and retry
rm -rf models/cache/*
```

### Candidate Not Found

**Symptoms**: `404: Candidate not found`

**Solution**:

```bash
# List all candidates
sono-eval candidate list

# Check exact ID (case-sensitive)
sono-eval candidate show --id <EXACT_ID>

# Create if missing
sono-eval candidate create --id <NEW_ID>
```

### Import Errors

**Symptoms**: `ModuleNotFoundError: No module named 'sono_eval'`

**Solution**:

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall in editable mode
pip install -e .

# Verify installation
python -c "import sono_eval; print(sono_eval.__version__)"
```

---

## Configuration Issues

### .env Not Loading

**Symptoms**: Default values used instead of .env values

**Solution**:

```bash
# Verify .env exists
ls -la .env

# Check file is readable
cat .env

# Ensure no syntax errors (KEY=VALUE, no spaces around =)
grep -v '^#' .env | grep -v '^$'

# Restart after changes
./launcher.sh restart
```

### Database Migration Errors

**Symptoms**: `alembic.util.exc.CommandError`

**Solution**:

```bash
# Check current version
alembic current

# View migration history
alembic history

# Upgrade to latest
alembic upgrade head

# If corrupted, reset (WARNING: loses data)
rm -f sono_eval.db
alembic upgrade head
```

### Model Cache Issues

**Symptoms**: `OSError: Can't load model`

**Solution**:

```bash
# Check cache directory exists and is writable
ls -ld models/cache
chmod -R 755 models/cache

# Clear cache
rm -rf models/cache/*

# Re-download
# Model will download on next use
```

---

## Performance Issues

### Slow Response Times

**Symptoms**: API requests take >10 seconds

**Diagnosis**:

```bash
# Check system resources
docker stats

# Check database performance
# Log slow queries in PostgreSQL

# Profile Python code
python -m cProfile sono_eval/api/main.py
```

**Solutions**:

**1. Increase cache size**:

```bash
MEMU_CACHE_SIZE=10000
REDIS_DB=0
```

**2. Use PostgreSQL instead of SQLite**:

```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/sono_eval
```

**3. Add more workers**:

```bash
API_WORKERS=8
```

**4. Optimize Docker**:

```bash
# Increase Docker resources (Desktop settings)
# CPU: 4+ cores
# Memory: 8GB+
```

### High Memory Usage

**Symptoms**: Out of memory errors, system slowdown

**Solutions**:

**1. Use smaller model**:

```bash
T5_MODEL_NAME=t5-small  # Instead of t5-base
```

**2. Reduce cache**:

```bash
MEMU_CACHE_SIZE=100
```

**3. Limit concurrent assessments**:

```bash
MAX_CONCURRENT_ASSESSMENTS=2
```

**4. Monitor and restart**:

```bash
# Check memory
docker stats

# Restart if needed
./launcher.sh restart
```

---

## Docker-Specific Issues

### Container Won't Start

**Symptoms**: Container exits immediately

**Diagnosis**:

```bash
# View container logs
docker-compose logs sono-eval

# Check exit code
docker-compose ps
```

**Common Causes**:

**1. Port conflict**: See "Port Already in Use" above

**2. Volume mount issues**:

```bash
# Check volume permissions
ls -la data/

# Fix permissions
chmod -R 755 data/
```

**3. Missing dependencies**:

```bash
# Rebuild image
docker-compose build --no-cache sono-eval
```

### Docker Compose Not Found

**Symptoms**: `docker-compose: command not found`

**Solution**:

```bash
# Try docker compose (newer version)
docker compose version

# Or install docker-compose
pip install docker-compose
```

### Image Build Fails

**Symptoms**: `ERROR: failed to solve`

**Solution**:

```bash
# Clear build cache
docker system prune -a

# Rebuild from scratch
docker-compose build --no-cache

# Check Dockerfile syntax
cat Dockerfile
```

---

## API-Specific Issues

### CORS Errors (Browser)

**Symptoms**: `Access to fetch blocked by CORS policy`

**Solution**:

```bash
# Enable CORS for your origin
CORS_ORIGINS=https://yourdomain.com

# Or allow all (development only)
CORS_ORIGINS=*

# Restart server
./launcher.sh restart
```

### Authentication Fails

**Symptoms**: `401 Unauthorized`

**Solution**:

```bash
# Verify API key (if configured)
# Check headers include: Authorization: Bearer <key>

# Disable auth for testing (development only)
# Set AUTH_DISABLED=true in .env
```

### Request Too Large

**Symptoms**: `413: Request Entity Too Large`

**Solution**:

```bash
# Increase max upload size
MAX_UPLOAD_SIZE=52428800  # 50MB

# Restart server
./launcher.sh restart
```

---

## ML Model Issues

### Tags Are Low Quality

**Symptoms**: Generated tags are generic or irrelevant

**Solutions**:

**1. Fine-tune model**:

```python
from sono_eval.tagging import TagGenerator

generator = TagGenerator()
generator.fine_tune(your_training_data, epochs=3)
```

**2. Provide more context**:

```bash
# Include surrounding code, not just snippet
sono-eval tag generate --file entire_module.py
```

**3. Adjust max_tags**:

```bash
# Request more tags, pick best ones
sono-eval tag generate --file code.py --max-tags 10
```

### Model Fallback Mode

**Symptoms**: `Using fallback tagging (model not available)`

**Causes**:

- Model not downloaded
- Insufficient memory
- Model file corrupted

**Solution**:

```bash
# Force model download
python -c "from transformers import T5ForConditionalGeneration; T5ForConditionalGeneration.from_pretrained('t5-base')"

# Check model cache
ls -lh models/cache/

# Verify memory available
free -h
```

---

## Data Issues

### Candidate Data Lost

**Symptoms**: Previously created candidate not found

**Diagnosis**:

```bash
# Check storage path exists
ls -la data/memory/

# Look for candidate files
find data/memory/ -name "*.json"

# Check file permissions
ls -l data/memory/
```

**Recovery**:

```bash
# Restore from backup (if available)
cp backup/memory/* data/memory/

# Rebuild index
# (manual process, contact support)
```

### Assessment Results Missing

**Symptoms**: Assessment completed but results not saved

**Solution**:

```bash
# Check output file was specified
sono-eval assess run --output results.json

# Verify write permissions
touch data/test.json && rm data/test.json

# Check disk space
df -h
```

---

## Common Error Messages

### `OSError: [Errno 28] No space left on device`

**Solution**: Free up disk space

```bash
# Check space
df -h

# Clean Docker
docker system prune -a

# Remove old logs
find . -name "*.log" -mtime +7 -delete
```

### `ConnectionRefusedError: [Errno 111] Connection refused`

**Solution**: Service not running

```bash
# Check if service is up
./launcher.sh status

# Start services
./launcher.sh start
```

### `TimeoutError: Operation timed out`

**Solution**: Increase timeout

```bash
# For API requests
requests.post(url, timeout=60)

# For assessments
ASSESSMENT_TIMEOUT=300  # seconds
```

### `ValidationError: Invalid input`

**Solution**: Check input format

```bash
# Verify JSON structure
echo '{"key": "value"}' | jq .

# Check API docs for correct format
open http://localhost:8000/docs
```

---

## Development Issues

### Pre-commit Hook SSL Certificate Errors

**Symptoms**: When committing, you see:

```
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
```

**Cause**: Python 3.13 installed from python.org doesn't have SSL certificates configured by default, causing pre-commit hooks (like `markdownlint-cli`) to fail when downloading dependencies.

**Solution**:

```bash
# Run the SSL fix script
./scripts/fix-pre-commit-ssl.sh

# Or manually set certificate path
export SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())")
pre-commit install
```

**Prevention**: Always run `./scripts/fix-pre-commit-ssl.sh` after running `pre-commit install`. See [scripts/README.md](../../scripts/README.md) for details.

---

## Getting More Help

### Gather Diagnostic Information

```bash
# System info
uname -a
python3 --version
docker --version

# Service status
./launcher.sh status

# Recent logs
./launcher.sh logs --tail=100 > logs.txt

# Configuration (redact secrets!)
sono-eval config show > config.txt
```

### Where to Get Help

1. **Documentation**: Check relevant guides first
   - [Installation](../user-guide/installation.md)
   - [Configuration](../user-guide/configuration.md)
   - [FAQ](../faq.md)

2. **GitHub Issues**: [Open an issue](https://github.com/doronpers/sono-eval/issues)
   - Include diagnostic info
   - Describe steps to reproduce
   - Attach logs (redact sensitive data)

3. **Discussions**: [GitHub Discussions](https://github.com/doronpers/sono-eval/discussions)
   - General questions
   - Usage tips
   - Feature requests

4. **Email**: <support@sono-eval.example>
   - Enterprise support
   - Security issues
   - Private concerns

---

## Prevention Tips

### Regular Maintenance

```bash
# Weekly
docker system prune -f
./launcher.sh restart

# Monthly
pip install -r requirements.txt --upgrade
docker-compose pull
```

### Monitoring

```bash
# Set up log rotation
# Configure alerts for errors
# Monitor disk space
# Track API response times
```

### Backups

```bash
# Backup data directory
tar -czf backup-$(date +%Y%m%d).tar.gz data/

# Backup database
pg_dump sono_eval > backup.sql
```

---

**Last Updated**: January 10, 2026
**Version**: 0.1.0

**Still having issues?** [Open an issue](https://github.com/doronpers/sono-eval/issues) with:

- Clear description
- Steps to reproduce
- System information
- Relevant logs
