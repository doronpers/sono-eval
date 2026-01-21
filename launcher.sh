#!/bin/bash
# One-click launcher for Sono-Eval system

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Header
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║                Sono-Eval System Launcher                  ║"
echo "║     Explainable Multi-Path Developer Assessment System    ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check environment
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Error: Docker is not installed${NC}"
        echo "Please install Docker from https://www.docker.com/get-started"
        exit 1
    fi
}

# Function to check if .env exists
check_env() {
    if [ ! -f .env ]; then
        echo -e "${YELLOW}⚠️  No .env file found. Creating from .env.example...${NC}"
        cp .env.example .env
        echo -e "${GREEN}✓ .env file created.${NC}"
    fi
}

# Function to check if a port is available
is_port_available() {
    local port=$1

    # Check if port is in use by system processes (works on macOS and Linux)
    if lsof -Pi :"$port" -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 1  # Port is in use
    fi

    # Check if port is in use by Docker containers
    if docker ps --format '{{.Ports}}' 2>/dev/null | grep -q ":$port->"; then
        return 1  # Port is in use by Docker
    fi

    # Try to bind to the port (most reliable check)
    if command -v nc >/dev/null 2>&1; then
        if nc -z localhost "$port" 2>/dev/null; then
            return 1  # Port is in use
        fi
    fi

    return 0  # Port is available
}

# Function to find an available port
find_available_port() {
    local start_port=${1:-8000}
    local port=$start_port
    local max_port=$((start_port + 100))  # Check up to 100 ports ahead

    while [ "$port" -le $max_port ]; do
        if is_port_available "$port"; then
            echo "$port"
            return 0
        fi
        port=$((port + 1))
    done

    # Fallback: return start_port if we can't find one (user will see error)
    echo "$start_port"
    return 1
}

# Function to get or set the API port
get_api_port() {
    local port_file=".sono-eval-port"

    if [ -f "$port_file" ]; then
        # Check if the stored port is still available
        local stored_port
        stored_port=$(cat "$port_file")
        if is_port_available "$stored_port"; then
            echo "$stored_port"
            return 0
        fi
        # Port is in use, find a new one
        rm -f "$port_file"
    fi

    # Find and store a new port
    local new_port
    new_port=$(find_available_port 8000)
    echo "$new_port" > "$port_file"
    echo "$new_port"
}

# START Services
start_services() {
    check_env

    # Get or find an available port
    local api_port
    api_port=$(get_api_port)
    export SONO_EVAL_API_PORT=$api_port

    echo -e "${BLUE}🚀 Starting Sono-Eval services...${NC}"
    echo -e "${CYAN}📍 Using API port: $api_port${NC}"

    # Export port for docker-compose
    export API_PORT=$api_port
    docker-compose up -d

    # Wait a moment for services to start
    sleep 2

    # Verify the port is actually being used
    local actual_port
    actual_port=$(docker ps --format '{{.Ports}}' | grep sono-eval-app | sed -n 's/.*:\([0-9]*\)->8000.*/\1/p' | head -1)
    if [ -n "$actual_port" ]; then
        api_port=$actual_port
        echo "$api_port" > .sono-eval-port
    fi

    echo ""
    echo -e "${GREEN}✅ Services started successfully!${NC}"
    echo ""
    echo -e "  • ${CYAN}API Server:${NC}     http://localhost:$api_port"
    echo -e "  • ${CYAN}API Docs:${NC}       http://localhost:$api_port/docs"
    echo -e "  • ${CYAN}Superset:${NC}       http://localhost:8088"
    echo ""
    echo -e "${YELLOW}💡 Tip: Run './launcher.sh logs' to view logs${NC}"
}

# STOP Services
stop_services() {
    echo -e "${BLUE}🛑 Stopping Sono-Eval services...${NC}"
    docker-compose down
    # Clean up port file when stopping
    rm -f .sono-eval-port
    echo -e "${GREEN}✓ Services stopped${NC}"
}

# STATUS
show_status() {
    echo -e "${BLUE}📊 Service Status:${NC}"
    docker-compose ps

    # Show current API port if services are running
    if docker ps --format '{{.Names}}' | grep -q "^sono-eval-app$"; then
        local api_port
        api_port=$(docker ps --format '{{.Ports}}' | grep sono-eval-app | sed -n 's/.*:\([0-9]*\)->8000.*/\1/p' | head -1)
        if [ -n "$api_port" ]; then
            echo ""
            echo -e "${CYAN}📍 API is running on port: $api_port${NC}"
            echo -e "   ${CYAN}URL:${NC} http://localhost:$api_port"
        fi
    fi
}

# LOGS
show_logs() {
    docker-compose logs -f "${1:-}"
}

# DEV SETUP
setup_dev() {
    echo -e "${BLUE}🛠️  Setting up development environment...${NC}"

    if [ ! -d "venv" ]; then
        python3 -m venv venv
        echo -e "${GREEN}✓ Virtual environment created${NC}"
    fi

    # shellcheck disable=SC1091
    source venv/bin/activate
    pip install -r requirements.txt
    pip install -e ".[dev]"

    echo -e "${GREEN}✅ Development environment ready${NC}"
    echo -e "${YELLOW}Activate with: source venv/bin/activate${NC}"
}

# CHECK READINESS
check_readiness() {
    echo -e "${BLUE}🔍 Checking environment readiness...${NC}"

    # Check Docker
    if command -v docker &> /dev/null; then
        echo -e "  [${GREEN}✓${NC}] Docker installed"
    else
        echo -e "  [${RED}✗${NC}] Docker not found"
    fi

    # Check .env
    if [ -f .env ]; then
        echo -e "  [${GREEN}✓${NC}] .env file exists"
    else
        echo -e "  [${YELLOW}!${NC}] .env file missing"
    fi

    echo -e "${GREEN}✓ Readiness check complete.${NC}"
}

# USAGE
show_usage() {
    echo "Usage: $0 {start|stop|restart|status|logs|dev|check}"
    echo ""
    echo "Commands:"
    echo "  ${GREEN}start${NC}    - Start all services (Docker)"
    echo "  ${RED}stop${NC}     - Stop all services (Docker)"
    echo "  ${YELLOW}restart${NC}  - Restart all services"
    echo "  ${CYAN}status${NC}   - Show service status"
    echo "  ${MAGENTA}logs${NC}     - Show logs (Ctrl+C to exit)"
    echo "  dev       - Setup local python venv"
    echo "  check     - Check environment readiness"
    echo ""
    exit 1
}

# Main Logic
case "${1:-}" in
    start)   check_docker; start_services ;;
    stop)    stop_services ;;
    restart) stop_services; sleep 2; check_docker; start_services ;;
    status)  show_status ;;
    logs)    show_logs "$2" ;;
    dev)     setup_dev ;;
    check)   check_readiness ;;
    *)       show_usage ;;
esac
