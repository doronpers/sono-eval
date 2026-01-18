# Setup Checklist - Getting Sono-Eval Running

This checklist covers everything needed to preview and use Sono-Eval as a real user.

## ✅ Prerequisites

### 1. **Python Environment**

- [ ] Python 3.13+ installed
- [ ] Virtual environment created (or use Docker)

### 2. **Docker (Optional but Recommended)**

- [ ] Docker installed
- [ ] Docker Compose installed
- [ ] Docker daemon running

### 3. **System Dependencies**

- [ ] Git installed
- [ ] curl installed (for health checks)

---

## 🔧 Configuration Steps

### 1. **Fix Dependencies**

- [x] ✅ Fixed torch version (was 2.8.0, now >=2.1.0)
- [x] ✅ Added jinja2 to requirements.txt
- [ ] Install dependencies: `pip install -r requirements.txt`

### 2. **Environment Configuration**

- [x] ✅ Created .env.example template
- [ ] Copy .env.example to .env: `cp .env.example .env`
- [ ] Review and update .env if needed (defaults work for development)

### 3. **Data Directories**

The system will auto-create these, but you can create them manually:

- [ ] `./data/memory` - For MemU storage
- [ ] `./data/tagstudio` - For TagStudio data
- [ ] `./models/cache` - For ML model cache

---

## 🚀 Running Options

### Option A: Docker (Easiest - Recommended)

```bash
# 1. Ensure .env exists
cp .env.example .env

# 2. Start all services
./launcher.sh start

# 3. Access the system
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - Mobile Companion (optional): http://localhost:8000/mobile/
# - Superset: http://localhost:8088 (admin/admin)
```

**What Docker provides:**

- ✅ PostgreSQL database
- ✅ Redis cache
- ✅ Apache Superset analytics
- ✅ All dependencies pre-installed
- ✅ Isolated environment

### Option B: Local Development

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt
pip install -e ".[dev]"

# 3. Create .env file
cp .env.example .env

# 4. Start the API server
sono-eval server start --reload

# 5. Access the system
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - Mobile Companion (optional): http://localhost:8000/mobile/
```

**Note:** Local development uses:

- SQLite instead of PostgreSQL (default)
- No Redis (optional, can run separately)
- No Superset (optional)

---

## 🧪 Testing the System

### 1. **Health Check**

```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy","version":"0.1.1",...}
```

### 2. **CLI Test**

```bash
# Show configuration
sono-eval config show

# Create a candidate
sono-eval candidate create --id test_candidate

# List candidates
sono-eval candidate list
```

### 3. **API Test**

```bash
# Create candidate via API
curl -X POST http://localhost:8000/api/v1/candidates \
  -H "Content-Type: application/json" \
  -d '{"candidate_id": "api_test"}'

# List candidates
curl http://localhost:8000/api/v1/candidates
```

### 4. **Web Interface Test**

- Open browser: <http://localhost:8000/mobile/>
- Should see welcome page
- Click "Let's Get Started"
- Select assessment paths
- Complete assessment flow

---

## ⚠️ Known Issues & Solutions

### Issue 1: torch Installation Fails

**Problem:** torch==2.8.0 doesn't exist
**Solution:** ✅ Fixed - now uses torch>=2.1.0

### Issue 2: Missing jinja2

**Problem:** Mobile templates need jinja2
**Solution:** ✅ Fixed - added to requirements.txt

### Issue 3: ML Models Not Loading

**Problem:** TagGenerator tries to load T5 model on first use
**Solution:**

- Models download automatically on first use
- Can take several minutes and ~500MB download
- For basic testing, tagging can be skipped

### Issue 4: Redis Not Available

**Problem:** Redis connection fails in local dev
**Solution:**

- Redis is optional for basic functionality
- System will work without it (just no caching)
- Or run: `docker run -d -p 6379:6379 redis:7-alpine`

### Issue 5: PostgreSQL Not Available

**Problem:** Database connection fails
**Solution:**

- Default uses SQLite (no setup needed)
- For PostgreSQL, update DATABASE_URL in .env
- Or use Docker which includes PostgreSQL

---

## 📋 Minimal Setup (Quick Test)

For the fastest preview without ML models:

```bash
# 1. Install core dependencies only
pip install fastapi uvicorn pydantic pydantic-settings click rich jinja2 python-dotenv

# 2. Install package in dev mode
pip install -e .

# 3. Create .env
cp .env.example .env

# 4. Start server
sono-eval server start

# 5. Test web interface
# Open: http://localhost:8000/mobile/
```

**Note:** Assessment and tagging will use placeholder/mock implementations
without ML dependencies.

---

## ✅ Verification Checklist

Before considering setup complete:

- [ ] API server starts without errors
- [ ] Health endpoint returns 200: `curl http://localhost:8000/health`
- [ ] API docs accessible: <http://localhost:8000/docs>
- [ ] Mobile UI loads: <http://localhost:8000/mobile/>
- [ ] CLI commands work: `sono-eval config show`
- [ ] Can create candidate via CLI
- [ ] Can create candidate via API
- [ ] Can run basic assessment (may be placeholder without ML)

---

## 🎯 Next Steps After Setup

1. **Explore the Mobile Interface**
   - Visit <http://localhost:8000/mobile/>
   - Complete a sample assessment
   - Review results

2. **Try the CLI**
   - Create candidates
   - Run assessments
   - Generate tags

3. **Use the API**
   - Explore Swagger docs
   - Make API calls
   - Integrate with other tools

4. **Review Documentation**
   - Read [Quick Start Guide](QUICK_START.md)
   - Check [API Reference](user-guide/api-reference.md)
   - See [CLI Reference](user-guide/cli-reference.md)

---

## 🆘 Getting Help

If you encounter issues:

1. Check [Troubleshooting Guide](troubleshooting.md)
2. Review error messages in logs
3. Verify all prerequisites are met
4. Check .env configuration
5. Ensure ports 8000, 5432, 6379, 8088 are available

---

**Last Updated:** After standardization and dependency fixes
