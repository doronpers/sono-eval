#!/bin/bash

# Sono-Eval Full Stack Launcher
# Starts both API server and Celery worker
# Double-click this file to start everything

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Sono-Eval Full Stack Launcher${NC}"
echo -e "${BLUE}  (API Server + Celery Worker)${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
REQUIRED_VERSION="3.13"

echo -e "${YELLOW}Checking Python version...${NC}"
if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${RED}⚠ Warning: Python $PYTHON_VERSION detected, but sono-eval requires Python 3.13${NC}"
    echo -e "${YELLOW}Attempting to continue anyway...${NC}"
    echo ""
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating one...${NC}"
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ Failed to create virtual environment${NC}"
        echo "Press any key to exit..."
        read -n 1
        exit 1
    fi
    echo -e "${GREEN}✓ Virtual environment created${NC}"
    echo ""
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source .venv/bin/activate

# Check if sono-eval is installed
if ! python -c "import sono_eval" 2>/dev/null; then
    echo -e "${YELLOW}sono-eval not installed. Installing...${NC}"
    pip install -e . > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ Failed to install sono-eval${NC}"
        echo -e "${YELLOW}Trying to run directly with uvicorn...${NC}"
        export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
    else
        echo -e "${GREEN}✓ sono-eval installed${NC}"
    fi
    echo ""
fi

# Check Redis
REDIS_RUNNING=false
if command -v redis-cli &> /dev/null; then
    if redis-cli ping > /dev/null 2>&1; then
        REDIS_RUNNING=true
        echo -e "${GREEN}✓ Redis is running${NC}"
    else
        echo -e "${RED}✗ Redis is not running${NC}"
        echo -e "${YELLOW}Starting Redis...${NC}"
        if command -v brew &> /dev/null; then
            brew services start redis
            sleep 2
            if redis-cli ping > /dev/null 2>&1; then
                REDIS_RUNNING=true
                echo -e "${GREEN}✓ Redis started${NC}"
            else
                echo -e "${RED}✗ Failed to start Redis${NC}"
                echo -e "${YELLOW}Please start Redis manually: brew services start redis${NC}"
            fi
        else
            echo -e "${YELLOW}Please start Redis manually${NC}"
        fi
    fi
else
    echo -e "${YELLOW}⚠ redis-cli not found. Celery may not work properly.${NC}"
fi
echo ""

# Find available port
API_PORT=8001
while lsof -Pi :$API_PORT -sTCP:LISTEN -t >/dev/null 2>&1; do
    echo -e "${YELLOW}Port $API_PORT is in use, trying next port...${NC}"
    API_PORT=$((API_PORT + 1))
    if [ $API_PORT -gt 8010 ]; then
        echo -e "${RED}✗ Could not find available port${NC}"
        echo "Press any key to exit..."
        read -n 1
        exit 1
    fi
done

echo -e "${GREEN}Using port: $API_PORT${NC}"
echo ""

# Create a function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Shutting down servers...${NC}"
    kill $API_PID $CELERY_PID 2>/dev/null
    wait $API_PID $CELERY_PID 2>/dev/null
    echo -e "${GREEN}✓ Servers stopped${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start API server in background
echo -e "${BLUE}Starting API server on port $API_PORT...${NC}"
if command -v sono-eval &> /dev/null; then
    sono-eval server start --port $API_PORT --reload > /tmp/sono-eval-api.log 2>&1 &
else
    export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
    python -m uvicorn sono_eval.api.main:app --host 0.0.0.0 --port $API_PORT --reload > /tmp/sono-eval-api.log 2>&1 &
fi
API_PID=$!

# Wait a moment for server to start
sleep 3

# Check if API server started
if kill -0 $API_PID 2>/dev/null; then
    echo -e "${GREEN}✓ API server started (PID: $API_PID)${NC}"
else
    echo -e "${RED}✗ API server failed to start${NC}"
    echo "Check logs: tail -f /tmp/sono-eval-api.log"
    echo "Press any key to exit..."
    read -n 1
    exit 1
fi

# Start Celery worker if Redis is running
if [ "$REDIS_RUNNING" = true ]; then
    echo -e "${BLUE}Starting Celery worker...${NC}"
    celery -A sono_eval.core.celery_app worker --loglevel=info > /tmp/sono-eval-celery.log 2>&1 &
    CELERY_PID=$!
    sleep 2

    if kill -0 $CELERY_PID 2>/dev/null; then
        echo -e "${GREEN}✓ Celery worker started (PID: $CELERY_PID)${NC}"
    else
        echo -e "${YELLOW}⚠ Celery worker may have failed to start${NC}"
        echo "Check logs: tail -f /tmp/sono-eval-celery.log"
    fi
else
    echo -e "${YELLOW}⚠ Skipping Celery worker (Redis not available)${NC}"
    CELERY_PID=""
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✓ Servers are running!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "  ${CYAN}API Server:${NC}     http://localhost:$API_PORT"
echo -e "  ${CYAN}API Docs:${NC}       http://localhost:$API_PORT/docs"
echo -e "  ${CYAN}Health Check:${NC}    http://localhost:$API_PORT/api/v1/health"
echo ""
if [ "$CELERY_PID" != "" ]; then
    echo -e "  ${CYAN}Celery Worker:${NC}  Running (PID: $CELERY_PID)"
fi
echo ""
echo -e "${YELLOW}Logs:${NC}"
echo -e "  API:    tail -f /tmp/sono-eval-api.log"
if [ "$CELERY_PID" != "" ]; then
    echo -e "  Celery: tail -f /tmp/sono-eval-celery.log"
fi
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all servers${NC}"
echo ""

# Open browser to API docs after a short delay
(sleep 3 && open "http://localhost:$API_PORT/docs" 2>/dev/null) &

# Wait for user to stop
wait $API_PID
