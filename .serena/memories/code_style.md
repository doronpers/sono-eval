# Code style & conventions

- Formatting: Black, line length 100 (CI runs `black --check --line-length 100`).
- Linting: flake8 with max line length 100 and E203 ignored.
- Pydantic v2: use `model_dump()` / `model_validate()` (avoid `.dict()`).
- Tests: pytest (FastAPI TestClient common), mock module-level globals in `sono_eval.api.main` for API tests.
- Logging: use `sono_eval.utils.logger.get_logger`.
- Input validation: strict candidate_id pattern; follow existing validators in `assessment/models.py` and `api/main.py`.

Note: AGENTS.md mentions Black line length 88, but repository instructions indicate 100; follow 100 unless repo config confirms otherwise.
