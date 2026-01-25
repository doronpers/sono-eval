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

### Pre-Commit Hook Requirements (CRITICAL)

**Before creating any new code, ensure you follow these requirements to avoid commit failures:**

#### 1. Import Requirements
- **All imports must be present**: When creating new files, ensure ALL required imports are included at the top of the file.
  - FastAPI: `from fastapi import APIRouter, Depends, HTTPException, status`
  - Pydantic: `from pydantic import BaseModel, Field`
  - Typing: `from typing import Any, Dict, List, Optional`
  - Standard library: `from datetime import datetime`, `from io import BytesIO`, etc.
- **Check existing files**: If you're adding functionality similar to existing code, check what imports those files use.
- **Run mypy locally**: `mypy src/sono_eval/` to catch missing imports before committing.

#### 2. Type Annotations & mypy
- **All new functions must have type hints**: `def function_name(param: str) -> bool:`
- **Return types matter**: If a function returns `Any` from a library call, use `# type: ignore[no-any-return]` or configure mypy to allow it.
- **Missing imports cause mypy failures**: If mypy says "Name X is not defined", add the import.

#### 3. Docstring Formatting
- **One-line docstrings**: Use `"""Single line description."""` (no blank line, period at end).
- **Multi-line docstrings**: Use proper formatting with blank lines.
- **All public modules need docstrings**: Empty `__init__.py` files should have at least `"""Module description."""`

#### 4. FastAPI-Specific Patterns
- **Depends() in function signatures**: This is acceptable and should use `# noqa: B008` to suppress flake8 warnings:
  ```python
  async def endpoint(param: str, user: User = Depends(get_current_user)):  # noqa: B008
  ```
- **Import order matters**: FastAPI imports should come before local imports.

#### 5. YAML Files
- **Indentation must be consistent**: Use 2 spaces (not tabs, not 4 spaces).
- **Check existing YAML files**: Match the indentation style of similar files in the repo.
- **Run yamllint**: `yamllint .` to check before committing.

#### 6. Unused Imports
- **Remove unused imports**: Before committing, check for imports that aren't used.
- **Test files**: Be especially careful - remove unused imports from test files.
- **Common culprits**: `json`, `pytest`, `unittest.mock` imports that aren't actually used.

#### 7. Line Length
- **Max 100 characters**: Black handles most cases, but long strings/comments need manual wrapping.
- **Break long lines**: If a line exceeds 100 chars, break it appropriately.

#### 8. Pre-Commit Checklist

**Before finishing any task, run this checklist:**

```bash
# 1. Format code
black .

# 2. Check linting
flake8 .

# 3. Check types
mypy src/sono_eval/ --ignore-missing-imports --no-strict-optional

# 4. Check YAML
yamllint .

# 5. Run all pre-commit hooks
pre-commit run --all-files
```

**If any step fails, fix the issues before committing. Do not bypass hooks with `--no-verify` unless explicitly instructed for structural migrations.**

#### 9. Bandit Security Checks

**Common Bandit Failures:**
- **B104 (0.0.0.0 bind)**: If intentional for Docker/local dev, add `# nosec B104` comment
- **B404/B603 (subprocess)**: Scripts directory is excluded - these are intentional for security audit tools
- **B615 (HuggingFace)**: If model versioning is handled, add `# nosec B615` comment

**Configuration Notes:**
- `scripts/` directory is excluded from bandit checks (contains security tools)
- Bandit runs with `-ll` flag (only reports High severity issues)
- Medium/Low severity issues in excluded directories or with nosec comments are acceptable

## Planning & Roadmap Guidelines

### Time Estimation Rule

**Rule for Future Planning Agents**: When creating plans or roadmaps:

1. **Do NOT include time estimates** (days, weeks, months) unless you have:
   - Actual historical data from similar completed tasks in the same codebase
   - Verified duration data from project management systems
   - User-provided time constraints

2. **Instead, use**:
   - **Complexity indicators**: Low, Medium, High, Very High
   - **Effort indicators**: Small, Medium, Large
   - **Dependencies**: List blocking dependencies
   - **Prerequisites**: What must be done first

3. **If time estimates are requested**:
   - Base them on similar completed tasks in the codebase
   - Clearly state the assumptions and data sources
   - Mark estimates as "rough" or "tentative"
   - Prefer ranges over specific dates

4. **Rationale**: Time estimates are highly variable and depend on:
   - Developer experience and familiarity
   - Unexpected technical challenges
   - External dependencies
   - Scope changes during implementation
   - Context switching and interruptions

This rule should be followed when updating `ROADMAP.md`, `BETA_REQUIREMENTS.md`, or any planning documents.
