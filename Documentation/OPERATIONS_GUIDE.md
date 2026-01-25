# Sono-Eval Operations Guide

This guide provides a comprehensive reference for all commands and operations required to launch, manage, and maintain the Sono-Eval system.

---

## 🚀 Launching the System

### Option 1: Docker (Recommended)

The fastest way to get all services (API, Redis, DB, Superset) running.

| Command | Description |
| :--- | :--- |
| `./launcher.sh start` | Start all services in the background |
| `./launcher.sh stop` | Stop and remove all containers |
| `./launcher.sh restart` | Stop and start services |
| `./launcher.sh status` | Show status of running containers |
| `./launcher.sh logs` | Follow all service logs |
| `./launcher.sh logs app` | Follow logs for only the API server |

### Option 2: Local Deployment

For developers working directly on the Python source code.

| Command | Description |
| :--- | :--- |
| `python -m venv venv` | Create virtual environment |
| `source venv/bin/activate` | Activate venv (linux/mac) |
| `venv\Scripts\activate` | Activate venv (Windows) |
| `pip install -e .` | Install Sono-Eval in editable mode |
| `sono-eval server start` | Start the API server locally |
| `sono-eval server start --reload` | Start server with auto-reload enabled |

---

## 🎯 Core Operations (CLI)

Use the `sono-eval` command-line tool for direct interaction.

### Assessments

| Command | Description | Example |
| :--- | :--- | :--- |
| `assess run` | Evaluate code/text | `sono-eval assess run --candidate-id x --file y.py` |
| `--paths` | Specify evaluation paths | `--paths technical design collaboration` |
| `--type` | Submission type | `--type code` (default), `project`, `interview` |
| `--output` | Save results to file | `--output result.json` |

### Candidate Management

| Command | Description |
| :--- | :--- |
| `candidate create` | Initialize a new candidate profile |
| `candidate list` | List all tracked candidates |
| `candidate show` | Display details for a specific candidate |
| `candidate history` | Show assessment history for a candidate |
| `candidate report` | Generate a comprehensive PDF/MD report |

### Session Management

| Command | Description |
| :--- | :--- |
| `session list` | List previous assessment sessions |
| `session report` | Summary of the current active session |
| `session end` | Conclude session and generate final summary |

### Semantic Tagging

| Command | Description |
| :--- | :--- |
| `tag generate` | Auto-tag code using the T5 model |
| `--max-tags` | Limit the number of generated tags |

---

## 🔧 Maintenance & Setup

### Environment & Verification

| Command | Description |
| :--- | :--- |
| `python verify_setup.py` | Run the system verification suite |
| `sono-eval setup init` | Run the interactive setup wizard |
| `sono-eval setup init --quick` | Quick setup with defaults |

### Utility Operations

- **Config**: Edit `.env` to change ports, database URLs, and API keys.
- **Wipe Memory**: Delete `data/memory/` and `data/tagstudio/` to start fresh.
- **REPL**: Run `sono-eval repl` for an interactive assessment shell.

---

## 💡 Quick Tips

- Access **Interactive Docs** at `http://localhost:8000/docs`.
- Access **Mobile Companion** at `http://localhost:8000/mobile`.
- Run health checks with `curl http://localhost:8000/api/v1/health`.
