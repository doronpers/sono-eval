#!/bin/bash

# Sono-Eval Server Launcher
# Double-click this file to start the sono-eval API server

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
echo -e "${BLUE}  Sono-Eval Server Launcher${NC}"
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

# Check if Redis is running (for Celery)
REDIS_RUNNING=false
if command -v redis-cli &> /dev/null; then
    if redis-cli ping > /dev/null 2>&1; then
        REDIS_RUNNING=true
        echo -e "${GREEN}✓ Redis is running${NC}"
    else
        echo -e "${YELLOW}⚠ Redis is not running (Celery worker will not work)${NC}"
        echo -e "${YELLOW}  Start Redis with: brew services start redis${NC}"
    fi
else
    echo -e "${YELLOW}⚠ redis-cli not found (Celery worker may not work)${NC}"
fi
echo ""

# Start the server
echo -e "${BLUE}Starting Sono-Eval API server...${NC}"
echo -e "${BLUE}Server will be available at: http://localhost:$API_PORT${NC}"
echo -e "${BLUE}API Docs: http://localhost:$API_PORT/docs${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""
echo -e "${BLUE}========================================${NC}"
echo ""

# Try to use sono-eval CLI first
if command -v sono-eval &> /dev/null; then
    sono-eval server start --port $API_PORT --reload
else
    # Fallback to uvicorn directly
    export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
    python -m uvicorn sono_eval.api.main:app --host 0.0.0.0 --port $API_PORT --reload
fi

# Keep window open if there's an error
if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}Server stopped with an error${NC}"
    echo "Press any key to exit..."
    read -n 1
fi
