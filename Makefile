.PHONY: help install install-dev run test test-cov format lint clean docker-start docker-stop

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt
	pip install -e .

install-dev: ## Install development dependencies
	pip install -r requirements.txt
	pip install -e ".[dev]"

run: ## Run the API server (development mode)
	sono-eval server start --reload

run-cli: ## Run a sample CLI assessment
	sono-eval assess run \
		--candidate-id demo_user \
		--content "def hello(): return 'world'" \
		--paths technical

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage report
	pytest --cov=src/sono_eval --cov-report=html --cov-report=term

format: ## Format code with black
	black src/ tests/

lint: ## Run linting checks
	flake8 src/ tests/
	@echo "Lint check complete!"

clean: ## Clean up generated files
	find . -depth -type d -name "__pycache__" -exec rm -rf {} + || true
	find . -type f -name "*.pyc" -delete
	find . -depth -type d -name "*.egg-info" -exec rm -rf {} + || true
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf dist build

docker-start: ## Start all Docker services
	./launcher.sh start

docker-stop: ## Stop all Docker services
	./launcher.sh stop

docker-logs: ## View Docker service logs
	./launcher.sh logs

docker-status: ## Check Docker service status
	./launcher.sh status

dev: ## Setup development environment
	./launcher.sh dev
	@echo "Environment ready! Activate with: source venv/bin/activate"

verify: ## Verify setup and configuration
	python verify_setup.py
