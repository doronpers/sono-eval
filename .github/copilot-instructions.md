# Copilot / AI Agent Instructions for Sono-Eval ✅

Purpose: Make AI coding agents productive quickly by documenting the project's
purpose, architecture, developer workflows, conventions, and concrete examples.
Follow `documentation/Governance/AGENT_BEHAVIORAL_STANDARDS.md` for behavioral
rules and quality expectations.

## Quick elevator (what to do first) 💡

- Run the system (Docker-first): `./launcher.sh start` → API:
  <http://localhost:8000>, API docs: `/docs`, Superset: <http://localhost:8088>
  (admin/admin in dev). See `docker-compose.yml` for services and insecure
  default credentials (dev-only).
- Local dev: `./launcher.sh dev` or `sono-eval server start --reload` (after
  `venv` and `pip install -e .[dev]`). See `launcher.sh`.
- Run tests: `pytest`. Run lint & formatting checks locally:
  `black src/ tests/` and `flake8 src/ tests/`.

## High-level architecture (read these files) 🔎

- API / entry points: `src/sono_eval/api/main.py` (FastAPI, health:
  `/api/v1/health`).
- Assessment domain: `src/sono_eval/assessment/` (core `AssessmentEngine`,
  `models`).
- Memory store (in-memory/hierarchical): `src/sono_eval/memory/memu.py` (MemU
  storage used for candidate history and storing assessment results).
- Tagging / semantic analysis: `src/sono_eval/tagging/` (`TagGenerator` usage,
  `POST /api/v1/tags/generate`).
- Mobile companion (touch UI): `src/sono_eval/mobile/` (mounted at `/mobile`).
- CLI utilities: `src/sono_eval/cli/main.py` (useful examples for expected
  behavior and CLIs).

Why this matters: The `POST /api/v1/assessments` flow calls
`AssessmentEngine.assess()` and commonly saves results to MemU; tests and
changes should respect that flow and safety checks.

## Project conventions and gotchas (do this, not generic advice) 🛠️

- Formatting: Black with **line-length 100** (CI runs
  `black --check --line-length 100`). Use `pre-commit install` when available.
- Lint rules: `flake8` with `--max-line-length 100` and `--extend-ignore E203`
  in CI.
- Pydantic v2: Use `model_dump()` / `model_validate()` for
  serialization/validation (not .dict()). Many models use `pydantic` +
  `pydantic-settings` (see `src/sono_eval/*`).
- Input validation: Candidate IDs and many inputs are validated with Pydantic
  validators — mimic existing validators (see `SECURITY.md` example and
  `assessment/models.py`).
- Tests: Use `pytest` and FastAPI `TestClient`. Common testing pattern: patch
  module-level globals in `sono_eval.api.main` (e.g. `assessment_engine`,
  `memu_storage`, `tag_generator`) instead of creating full integration
  environments. Example: `@patch("sono_eval.api.main.assessment_engine")`.
- Logging & errors: Prefer clear error messages and include `request_id`
  propagation (`X-Request-ID`) when possible.

## Commands & CI expectations (copy/paste examples) ⌨️

- Start dev system: `./launcher.sh start` (Docker) or `./launcher.sh dev`
  (create venv + install deps).
- Run tests: `pytest --cov=src/sono_eval --cov-report=term` (CI also stores
  coverage artifacts).
- Lint locally: `black --check --line-length 100 src/ tests/` and
  `flake8 --max-line-length 100 --extend-ignore E203 src/ tests/`.
- Security scans in CI: Bandit, Safety, pip-audit; Docker images are scanned
  with Trivy in CI.

## Integration points & external deps to be mindful of 🔗

- Docker compose services: PostgreSQL, Redis, Superset (see
  `docker-compose.yml` - default credentials are **development only**).
- Configuration: `.env` (copy from `.env.example`) — **do not commit secrets**.
  See `SECURITY.md` for production notes (SECRET_KEYs, CORS, rate limits).
- API docs: `/docs` (Swagger) - useful to craft example requests during implementation.

## Testing and PR expectations ✅

- Add tests for behavioral changes and edge cases (use mocking to keep tests fast).
- Always run `black` and `flake8` locally; tests should pass in CI.
- If adding or changing public schemas, update docs and tests that assert
  validation errors.
- PR checklist in `CONTRIBUTING.md`: include tests, formatting, lint fixes, and
  updated docs where applicable.

## PR Reviewer Mini-Checklist ✅

- Run tests locally: `pytest` and check coverage changes only when appropriate.
- Run linters/formatters: `black --check --line-length 100 src/ tests/` and
  `flake8 --max-line-length 100 src/ tests/`.
- Verify CI matrix expectations (Python 3.9–3.11) and fix or document any
  environment-specific failures.
- Check Pydantic schema changes for compatibility; prefer
  `model_dump(mode="json")`/`model_validate()` tests for serialization changes.
- Confirm API contract changes are documented (update `documentation/*` and
  OpenAPI if needed) and add examples to `/docs` when helpful.
- Ensure no secrets or default credentials were introduced (check `.env`,
  `docker-compose.yml`, `config/`).
- Verify request logging and `X-Request-ID` propagation on modified endpoints
  when relevant.
- Prefer small, focused PRs. If the PR is large, include a clear implementation
  plan and manual testing steps in the description.

## Troubleshooting FAQ ❓

- Services not starting with `./launcher.sh start`:
  - Confirm Docker is running and `.env` exists (`cp .env.example .env` if missing).
  - Check `docker-compose ps` and run `./launcher.sh logs` or
    `docker-compose logs -f sono-eval` to inspect issues.
- Tests fail locally but pass in CI:
  - Activate the virtualenv and install dev deps: `pip install -e ".[dev]"`.
  - Ensure `pre-commit` hooks aren't modifying files mid-test; run
    `pre-commit run --all-files` to surface issues.
- Port conflicts on 8000/8088:
  - Start the server on a different port: `sono-eval server start --port 8001`
    or adjust `docker-compose` port mappings.
- Formatting / type checks failing (black/flake8/mypy):
  - Run `black src/ tests/`, fix style issues, then `flake8` and `mypy` as
    needed (mypy is allowed to be permissive in CI: `--ignore-missing-imports`).
- Database or migration problems:
  - Use `alembic` (see `migrations/`) and ensure `DATABASE_URL` points to a
    writable DB; check `migrations/README.md` if present.
- Security concerns (found secrets or unsafe defaults):
  - Refer to `SECURITY.md` immediately and remove secrets from commits. Never
    commit `.env` or credentials.

## Small, concrete examples from the codebase ✂️

- Assess from CLI:
  sono-eval assess run --candidate-id john_doe --file solution.py
- Test pattern (mocking the engine):
  @patch("sono_eval.api.main.assessment_engine")
  def test_assessment_endpoint(mock_engine, client): ...
- Use Pydantic v2 serialization in tests/assertions:
  `result.model_dump(mode="json")` or `AssessmentResult.model_validate(data)`.

## Where to read more (priority order) 📚

1. `README.md` - quick start & sample requests
2. `documentation/Core/concepts/architecture.md` - system flow and design rationale
3. `documentation/Governance/AGENT_BEHAVIORAL_STANDARDS.md` - agent mandates
   and quality rules
4. `CONTRIBUTING.md` - PR and local dev workflow
5. `SECURITY.md` - secrets, production hardening, input validation patterns
6. `./launcher.sh`, `docker-compose.yml`, `.github/workflows/ci.yml` -
   operational commands and CI rules

---
If anything above is unclear, missing, or you'd like a short snippet added (e.g.,
more test examples or exact Pydantic patterns), ask and I will refine the
instructions. 👋
