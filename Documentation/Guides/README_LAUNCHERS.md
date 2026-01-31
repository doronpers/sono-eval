# Sono-Eval One-Click Launchers

Two convenient launcher scripts for starting sono-eval:

## 🚀 Quick Start (API Server Only)

**File:** `start-sono-eval-server.command`

Double-click this file to start just the API server. Perfect for:
- Quick testing
- Development without batch processing
- When you don't need Celery worker

**What it does:**
- Checks Python version
- Creates virtual environment if needed
- Installs sono-eval if needed
- Finds available port (starts at 8001)
- Starts API server
- Opens browser to API docs

## 🔧 Full Stack (API + Celery Worker)

**File:** `start-sono-eval-full.command`

Double-click this file to start both API server and Celery worker. Perfect for:
- Testing batch processing
- Full functionality testing
- Production-like setup

**What it does:**
- Everything from the quick start, plus:
- Checks for Redis
- Starts Redis if needed (via Homebrew)
- Starts Celery worker for async tasks
- Runs both servers in background
- Shows status and logs

## 📋 Requirements

- **Python 3.13** (will attempt with 3.12 if needed)
- **Redis** (for Celery worker - optional for API-only)
- **Homebrew** (for auto-starting Redis - optional)

## 🎯 Usage

1. **Navigate to sono-eval directory:**
   ```bash
   cd /Volumes/Treehorn/Gits/sono-eval
   ```

2. **Double-click the launcher:**
   - `start-sono-eval-server.command` - API only
   - `start-sono-eval-full.command` - Full stack

3. **Wait for servers to start** (you'll see status messages)

4. **Access the API:**
   - API Docs: http://localhost:8001/docs
   - Health: http://localhost:8001/api/v1/health
   - Batch Endpoint: http://localhost:8001/api/v1/assessments/batch/

## 🛑 Stopping Servers

- Press `Ctrl+C` in the terminal window
- Or close the terminal window

## 📝 Notes

- Ports are auto-detected (starts at 8001, increments if busy)
- Logs are written to `/tmp/sono-eval-api.log` and `/tmp/sono-eval-celery.log`
- Virtual environment is created automatically if missing
- Dependencies are installed automatically if missing

## 🔍 Troubleshooting

**"Command not found: sono-eval"**
- The script will fall back to running uvicorn directly
- Make sure dependencies are installed: `pip install fastapi uvicorn celery redis`

**"Redis not running"**
- Install Redis: `brew install redis`
- Start Redis: `brew services start redis`
- Or use the full launcher which tries to start it automatically

**"Port already in use"**
- The script will try the next available port
- Or manually stop the process using that port

**Python version issues**
- Install Python 3.13: `pyenv install 3.13.0`
- Set local version: `pyenv local 3.13.0`
- The script will attempt to work with 3.12 but may have issues
