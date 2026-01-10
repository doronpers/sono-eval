# Quick Start Guide - Get Sono-Eval Running in 5 Minutes

## 🚀 Fastest Way: Docker

```bash
# 1. Copy environment file
cp .env.example .env

# 2. Start everything
./launcher.sh start

# 3. Open in browser
# - Mobile UI: http://localhost:8000/mobile/
# - API Docs: http://localhost:8000/docs
```

That's it! Docker handles all dependencies.

---

## 💻 Local Development (No Docker)

### Step 1: Verify Setup
```bash
python3 verify_setup.py
```

### Step 2: Install Dependencies
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install
pip install -r requirements.txt
pip install -e .
```

### Step 3: Configure
```bash
cp .env.example .env
# Edit .env if needed (defaults work for development)
```

### Step 4: Start Server
```bash
sono-eval server start --reload
```

### Step 5: Test It
- Open: http://localhost:8000/mobile/
- Or API docs: http://localhost:8000/docs

---

## ✅ What Was Fixed

1. ✅ **torch version** - Changed from 2.8.0 (doesn't exist) to >=2.1.0
2. ✅ **jinja2** - Added to requirements.txt (needed for templates)
3. ✅ **.env.example** - Created with all configuration options
4. ✅ **Data directories** - Auto-created by the system
5. ✅ **Setup verification** - Created verify_setup.py script

---

## 🎯 Test as a User

### 1. Web Interface
1. Go to http://localhost:8000/mobile/
2. Click "Let's Get Started"
3. Enter candidate ID
4. Select assessment paths
5. Complete assessment
6. View results

### 2. CLI
```bash
# Create candidate
sono-eval candidate create --id test_user

# Run assessment
sono-eval assess run \
  --candidate-id test_user \
  --file some_code.py \
  --paths technical

# List candidates
sono-eval candidate list
```

### 3. API
```bash
# Health check
curl http://localhost:8000/health

# Create candidate
curl -X POST http://localhost:8000/api/v1/candidates \
  -H "Content-Type: application/json" \
  -d '{"candidate_id": "api_user"}'

# List candidates
curl http://localhost:8000/api/v1/candidates
```

---

## ⚠️ Troubleshooting

**Port 8000 already in use?**
```bash
# Change port in .env
API_PORT=8001
```

**Dependencies won't install?**
```bash
# Try upgrading pip first
pip install --upgrade pip
pip install -r requirements.txt
```

**ML models slow to load?**
- First run downloads models (~500MB)
- Subsequent runs are faster
- Can skip ML features for basic testing

**Need help?**
- See [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) for detailed steps
- Check [Documentation/Guides/troubleshooting.md](Documentation/Guides/troubleshooting.md)

---

**You're ready to go!** 🎉
