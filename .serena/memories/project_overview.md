# Sono-Eval project overview

## Purpose
Sono-Eval is an explainable, multi-path developer assessment platform. It evaluates submissions across technical/design/collaboration/problem-solving/communication paths, generates evidence-backed scores, tracks micro-motives (Dark Horse model), and stores results in hierarchical memory (MemU). Interfaces include REST API, CLI, Python SDK, and an optional mobile companion UI.

## Tech stack
- Python (project targets 3.9+; docs mention 3.13+ for some workflows)
- FastAPI (API)
- Pydantic v2 (models/validation)
- Click + Rich (CLI)
- Transformers + PyTorch + PEFT/LoRA (semantic tagging)
- Redis (optional cache/task queue), PostgreSQL (optional), SQLite default
- Apache Superset (analytics)
- Docker + Docker Compose (dev/prod)

## Entry points
- API: `src/sono_eval/api/main.py`
- Assessment Engine: `src/sono_eval/assessment/engine.py`
- Memory: `src/sono_eval/memory/memu.py`
- Tagging: `src/sono_eval/tagging/`
- Mobile companion: `src/sono_eval/mobile/`
- CLI: `src/sono_eval/cli/main.py`
