# Codex Environment Setup for sono-eval

Complete configuration guide for setting up a Codex development environment for `sono-eval`.

## Quick Configuration

### 1. Name & Description
- **Name**: `sono-eval / dev + tests`
- **Description**: `Full sono-eval dev env with dependencies, pytest, linting, Celery/Redis support, and API access.`

### 2. Container Image & Workspace
- **Container image**: `universal`
- **Workspace directory**: `/workspace/sono-eval` (default)

### 3. Setup Script & Caching
- **Setup script (Manual)**: `/workspace/sono-eval/scripts/codex-setup.sh`
- **Container Caching**: `On`
- **Maintenance script**: `pip install -e ".[dev]"`

### 4. Environment Variables
```
SONO_EVAL_ENV=codex
SONO_EVAL_LOG_LEVEL=INFO
PYTHONUNBUFFERED=1
PYTHONUTF8=1
```

### 5. Secrets (API Keys)
- `OPENAI_API_KEY` - For OpenAI models
- `ANTHROPIC_API_KEY` - For Anthropic models
- `GEMINI_API_KEY` - For Google Gemini models

### 6. Agent Internet Access
- **Agent internet access**: `On`
- **Domain allowlist**: Start with `Common dependencies`, then add:
  - `api.openai.com`
  - `api.anthropic.com`
  - `generativelanguage.googleapis.com`
  - `pypi.org`
  - `files.pythonhosted.org`
  - `github.com`
  - `raw.githubusercontent.com`
- **Allowed HTTP Methods**: `All methods`

## Special Considerations

### Celery & Redis
If testing batch processing features:
- Redis may need to be available (or use in-memory fallback)
- Celery workers run in separate processes
- Consider using test Redis instance or mocking

### Python 3.13 Requirement
- sono-eval requires Python 3.13+
- Codex universal image should provide this
- Verify with: `python3 --version`
