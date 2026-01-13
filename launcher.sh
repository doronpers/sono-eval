#!/bin/bash
# One-click launcher for Sono-Eval system

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║              Sono-Eval System Launcher                    ║"
echo "║   Explainable Multi-Path Developer Assessment System     ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    echo "Please install Docker from https://www.docker.com/get-started"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not installed${NC}"
    exit 1
fi

# Function to check if .env exists
check_env() {
    if [ ! -f .env ]; then
        echo -e "${YELLOW}No .env file found. Creating from .env.example...${NC}"
        cp .env.example .env
        echo -e "${GREEN}.env file created. Please review and update if needed.${NC}"
    fi
}

# Function to start services
start_services() {
    echo -e "${BLUE}Starting Sono-Eval services...${NC}"
    docker-compose up -d

    echo ""
    echo -e "${GREEN}Services started successfully!${NC}"
    echo ""
    echo -e "${BLUE}Service URLs:${NC}"
    echo -e "  • API Server:     ${GREEN}http://localhost:8000${NC}"
    echo -e "  • API Docs:       ${GREEN}http://localhost:8000/docs${NC}"
    echo -e "  • Superset:       ${GREEN}http://localhost:8088${NC} (admin/admin)"
    echo ""
    echo -e "${YELLOW}Tip: Run 'docker-compose logs -f' to view logs${NC}"
}

# Function to stop services
stop_services() {
    echo -e "${BLUE}Stopping Sono-Eval services...${NC}"
    docker-compose down
    echo -e "${GREEN}Services stopped${NC}"
}

# Function to show status
show_status() {
    echo -e "${BLUE}Service Status:${NC}"
    docker-compose ps
}

# Function to show logs
show_logs() {
    docker-compose logs -f "${1:-}"
}

# Function to run CLI commands
run_cli() {
    docker-compose exec sono-eval sono-eval "$@"
}

# Function to setup development environment
setup_dev() {
    echo -e "${BLUE}Setting up development environment...${NC}"

    # Create virtual environment
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        echo -e "${GREEN}Virtual environment created${NC}"
    fi

    # Activate and install dependencies
    source venv/bin/activate
    pip install -r requirements.txt
    pip install -e ".[dev]"

    echo -e "${GREEN}Development environment ready${NC}"
    echo -e "${YELLOW}Activate with: source venv/bin/activate${NC}"
}

# Main menu
case "${1:-}" in
    start)
        check_env
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        stop_services
        sleep 2
        start_services
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs "$2"
        ;;
    cli)
        shift
        run_cli "$@"
        ;;
    dev)
        setup_dev
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs|cli|dev}"
        echo ""
        echo "Commands:"
        echo "  start    - Start all services"
        echo "  stop     - Stop all services"
        echo "  restart  - Restart all services"
        echo "  status   - Show service status"
        echo "  logs     - Show logs (optionally specify service)"
        echo "  cli      - Run CLI commands (e.g., $0 cli assess --help)"
        echo "  dev      - Setup development environment"
        echo ""
        echo "Examples:"
        echo "  $0 start"
        echo "  $0 logs sono-eval"
        echo "  $0 cli config show"
        exit 1
        ;;
esac
