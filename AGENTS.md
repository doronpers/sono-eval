# Repository Guidelines

## Project Structure & Module Organization

- `src/sono_eval/` holds the Python package (API, assessment engine, CLI, tagging, utils).
- `tests/` contains `unit/` and `integration/` suites; pytest discovers `test_*.py`.
- `migrations/` and `alembic.ini` manage database schema changes.
- `config/` stores configuration files; `scripts/` holds utility scripts.
- `documentation/` and `README.md` cover user-facing docs.

## Build, Test, and Development Commands

- `make install` / `make install-dev`: install runtime or dev dependencies.
- `make run`: start the API server with reload enabled.
- `make run-cli`: run a sample CLI assessment.
- `make test`: run the full pytest suite.
- `make test-cov`: run tests with coverage reports (HTML + terminal).
- `make format`: format code with Black.
- `make lint`: run Flake8 checks.
- `make docker-start` / `make docker-stop`: manage Docker services.
- `make verify`: validate local setup.

## Coding Style & Naming Conventions

- Python 3.13+, package layout uses `src/`.
- Formatting is managed by Black (configured in `pyproject.toml`, line length 88).
- Imports follow isort with the Black profile.
- Linting uses Flake8; optional type checks use mypy.
- Follow pytest naming: `test_*.py`, classes `Test*`, functions `test_*`.

## Testing Guidelines

- Framework: pytest with `pytest-asyncio` and `pytest-cov`.
- Coverage config defaults to `--cov=src/sono_eval` in `pyproject.toml`.
- Add/extend tests for logic changes; prefer unit tests in `tests/unit/`.

## Commit & Pull Request Guidelines

- Commit history mixes conventional prefixes (`feat:`, `style:`, `chore:`) with descriptive sentences; keep messages short and action-oriented.
- PRs should include a clear description, test status, and any relevant docs updates.
- Use the PR checklist in `CONTRIBUTING.md` (tests, Black, Flake8).

## Security & Configuration Tips

- Do not commit secrets; use local env files and `config/` as needed.
- Run `make verify` after setup changes or dependency updates.

## Common Pitfalls

### Linting Protocols for Agents

To prevent common issues and save time:

- **Pre-emptive Formatting**: Always run `black .` and `flake8 .` *before* attempting to commit or finishing a task. This catches simple syntax/style errors early.
- **Handling Imports**:
  - **E402 (Module level import not at top of file)**: When using `sys.path` hacks (common in scripts), put the imports *after* the `sys.path` modification and add `# noqa: E402` to the import lines.
  - **F401 (Unused imports)**: Remove them! Do not leave them unless specifically needed for some dynamic reason, in which case use `# noqa: F401`.
- **String Formatting**:
  - **F541 (f-string missing placeholders)**: If a string doesn't have `{variable}`, it shouldn't be an f-string. Remove the `f` prefix.
- **Line Length (E501)**: `black` handles most of this, but for long strings or comments, manually wrap them.
- **Test Files**: Be careful not to delete imports in test files when "cleaning up" blank lines. `flake8` E303 calls for removing blank lines, not the code around them.

### Script Permissions

- **Executable Scripts**: Ensure that all scripts with shebangs (e.g., `#!/usr/bin/env python3`) have the executable permission set (`chmod +x`). The pre-commit hooks will fail if this is not done.
