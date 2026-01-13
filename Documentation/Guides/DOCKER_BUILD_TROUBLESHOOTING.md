# Docker Build Troubleshooting Guide

Common Docker build errors and their solutions for Sono-Eval.

## 🔍 Quick Diagnosis

First, check the exact error:

```bash
# View full build output
docker-compose build --progress=plain 2>&1 | tee build.log

# Or for specific service
docker-compose build sono-eval --no-cache --progress=plain
```

---

## Common Build Errors

### 1. **torch Installation Fails**

**Error**: `ERROR: Could not find a version that satisfies the requirement torch==2.8.0`

**Cause**: torch 2.8.0 doesn't exist (we fixed this in requirements.txt)

**Solution**:
✅ Already fixed - requirements.txt now uses `torch>=2.1.0`

If you still see this error:

```bash
# Rebuild without cache
docker-compose build --no-cache sono-eval

# Or manually verify requirements.txt
grep torch requirements.txt
# Should show: torch>=2.1.0
```

---

### 2. **jinja2 Missing**

**Error**: `ModuleNotFoundError: No module named 'jinja2'`

**Cause**: jinja2 not in requirements.txt (we fixed this)

**Solution**:
✅ Already fixed - jinja2>=3.1.0 added to requirements.txt

If still failing:

```bash
# Verify it's in requirements.txt
grep jinja2 requirements.txt

# Rebuild
docker-compose build --no-cache sono-eval
```

---

### 3. **PyTorch Download Timeout**

**Error**: `Connection timeout` or `Failed to download torch`

**Cause**: Large download (~2GB), network issues

**Solution**:

```bash
# Option 1: Increase build timeout
docker-compose build --build-arg BUILDKIT_INLINE_CACHE=1 sono-eval

# Option 2: Use pip cache
docker-compose build --build-arg PIP_CACHE_DIR=/root/.cache/pip sono-eval

# Option 3: Build in stages (modify Dockerfile)
# Install torch separately with retry
```

**Temporary workaround** - Modify Dockerfile to install torch separately:

```dockerfile
# Add after line 22
RUN pip install --no-cache-dir torch>=2.1.0 --timeout=300 || \
    pip install --no-cache-dir torch>=2.1.0 --timeout=600
```

---

### 4. **Out of Memory During Build**

**Error**: `Killed` or `signal: killed` during pip install

**Cause**: Insufficient Docker memory for PyTorch build

**Solution**:

```bash
# Increase Docker memory (Docker Desktop)
# Settings > Resources > Memory > Increase to 4GB+

# Or build with less parallelism
docker-compose build --build-arg PIP_NO_CACHE_DIR=1 sono-eval

# Or use pre-built torch wheel
# Modify requirements.txt temporarily:
# torch>=2.1.0 --index-url https://download.pytorch.org/whl/cpu
```

---

### 5. **Build Context Issues**

**Error**: `COPY failed: file not found in build context`

**Cause**: Missing files or wrong build context

**Solution**:

```bash
# Verify all files exist
ls -la requirements.txt pyproject.toml src/ config/

# Check .dockerignore isn't excluding needed files
cat .dockerignore 2>/dev/null || echo "No .dockerignore"

# Rebuild with verbose output
docker-compose build --progress=plain sono-eval
```

---

### 6. **Python Version Mismatch**

**Error**: `Python version X.Y required, but Y.Z found`

**Cause**: Dockerfile uses python:3.11 but code needs different version

**Solution**:

```bash
# Check what Python version is needed
grep requires-python pyproject.toml
# Shows: requires-python = ">=3.9"

# Dockerfile uses 3.11 which is fine, but if issues:
# Edit Dockerfile line 3:
FROM python:3.9-slim  # or 3.10, 3.11
```

---

### 7. **System Dependencies Missing**

**Error**: `error: command 'gcc' failed` or `Microsoft Visual C++ 14.0 is required`

**Cause**: Missing build tools

**Solution**:
The Dockerfile already includes build-essential, but if issues:

```dockerfile
# Ensure these are in Dockerfile (lines 12-16):
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*
```

---

### 8. **pip Install Fails for Specific Package**

**Error**: `ERROR: Could not install packages due to an OSError`

**Solution**:

```bash
# Try installing packages in smaller batches
# Modify Dockerfile temporarily:

# Install core dependencies first
RUN pip install --no-cache-dir fastapi uvicorn pydantic pydantic-settings

# Then ML packages
RUN pip install --no-cache-dir torch>=2.1.0 --timeout=600

# Then rest
RUN pip install --no-cache-dir -r requirements.txt
```

---

### 9. **Network/SSL Issues**

**Error**: `SSL: CERTIFICATE_VERIFY_FAILED` or `Connection refused`

**Cause**: Corporate proxy, firewall, or SSL issues

**Solution**:

```bash
# Add to Dockerfile before pip install:
ENV PIP_TRUSTED_HOST=pypi.org files.pythonhosted.org
ENV PIP_INDEX_URL=https://pypi.org/simple

# Or use custom index
ENV PIP_INDEX_URL=https://your-custom-index.com/simple
```

---

### 10. **Docker Build Cache Issues**

**Error**: Stale cache causing weird errors

**Solution**:

```bash
# Clear all Docker cache
docker system prune -a

# Rebuild from scratch
docker-compose build --no-cache sono-eval

# Or just clear build cache
docker builder prune -a
```

---

## 🔧 Step-by-Step Debug Process

### Step 1: Check Error Location

```bash
# Build with verbose output
docker-compose build --progress=plain sono-eval 2>&1 | tee build.log

# Find the failing step
grep -i "error\|failed\|killed" build.log
```

### Step 2: Test Individual Steps

```bash
# Build up to a specific point
# Edit Dockerfile, add exit after problematic step
# Then: docker-compose build sono-eval
```

### Step 3: Test in Interactive Container

```bash
# Build base image
docker build -t sono-eval-test -f Dockerfile .

# Run interactive shell
docker run -it --rm sono-eval-test /bin/bash

# Manually test commands
pip install torch>=2.1.0
pip install -r requirements.txt
```

### Step 4: Check Dependencies

```bash
# Verify requirements.txt syntax
pip install --dry-run -r requirements.txt

# Check for version conflicts
pip check
```

---

## 🚀 Quick Fixes

### Minimal Build (Skip ML Dependencies)

If you just want to test the API without ML:

```dockerfile
# Create Dockerfile.minimal
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential curl git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-minimal.txt .
RUN pip install --no-cache-dir -r requirements-minimal.txt

COPY src/ /app/src/
COPY config/ /app/config/
RUN pip install -e .

EXPOSE 8000
CMD ["uvicorn", "sono_eval.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `requirements-minimal.txt`:

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
click>=8.1.7
rich>=13.7.0
jinja2>=3.1.0
python-dotenv>=1.0.0
sqlalchemy>=2.0.23
redis>=5.0.1
```

---

## 📋 Pre-Build Checklist

Before building, ensure:

- [ ] `requirements.txt` exists and is valid
- [ ] `pyproject.toml` exists
- [ ] `src/` directory exists
- [ ] `config/` directory exists (can be empty)
- [ ] Docker has enough memory (4GB+ recommended)
- [ ] Docker has enough disk space (10GB+ free)
- [ ] Network connection is stable
- [ ] No conflicting containers running

---

## 🆘 Still Having Issues?

1. **Share the exact error message** - Copy the full error output
2. **Check Docker version**: `docker --version` and `docker-compose --version`
3. **Check system resources**: `docker system df`
4. **Try building manually**:

   ```bash
   docker build -t sono-eval-test .
   ```

---

## Common Error Patterns

| Error Pattern | Likely Cause | Quick Fix |
|--------------|--------------|-----------|
| `torch==2.8.0` | Old requirements.txt | Use updated requirements.txt |
| `ModuleNotFoundError: jinja2` | Missing dependency | Already fixed in requirements.txt |
| `Killed` during pip install | Out of memory | Increase Docker memory |
| `Connection timeout` | Network/PyTorch download | Retry or use pip cache |
| `COPY failed` | Missing files | Check build context |
| `gcc failed` | Missing build tools | Already in Dockerfile |

---

**Last Updated**: After fixing torch and jinja2 dependencies
