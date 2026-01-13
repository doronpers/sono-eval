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

# START Services
start_services() {
    check_env
    echo -e "${BLUE}🚀 Starting Sono-Eval services...${NC}"
    docker-compose up -d

    echo ""
    echo -e "${GREEN}✅ Services started successfully!${NC}"
    echo ""
    echo -e "  • ${CYAN}API Server:${NC}     http://localhost:8000"
    echo -e "  • ${CYAN}API Docs:${NC}       http://localhost:8000/docs"
    echo -e "  • ${CYAN}Superset:${NC}       http://localhost:8088"
    echo ""
    echo -e "${YELLOW}💡 Tip: Run './launcher.sh logs' to view logs${NC}"
}

# STOP Services
stop_services() {
    echo -e "${BLUE}🛑 Stopping Sono-Eval services...${NC}"
    docker-compose down
    echo -e "${GREEN}✓ Services stopped${NC}"
}

# STATUS
show_status() {
    echo -e "${BLUE}📊 Service Status:${NC}"
    docker-compose ps
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
