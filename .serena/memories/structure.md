# Repository structure

- `src/sono_eval/` core package
  - `assessment/` (engine, models, scorers)
  - `api/` (FastAPI app)
  - `cli/` (Click CLI)
  - `memory/` (MemU storage)
  - `tagging/` (TagGenerator, TagStudio)
  - `mobile/` (templates, static assets, mobile app)
  - `utils/` (config, logging, errors)
- `tests/` unit + integration tests
- `documentation/` docs hub, guides, governance, reports
- `config/` Superset configs
- `scripts/` utility scripts
- `launcher.sh` for Docker/dev commands
