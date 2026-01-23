# Suggested commands (macOS/Darwin)

## Run app / services
- `./launcher.sh start` (Docker-based system)
- `./launcher.sh dev` (local dev setup)
- `sono-eval server start --reload` (API server)

## CLI usage
- `sono-eval assess run --candidate-id demo --file solution.py --paths technical`
- `sono-eval candidate list`
- `sono-eval tag generate --file mycode.js --max-tags 5`

## Tests / format / lint
- `pytest`
- `black src/ tests/ --line-length 100`
- `flake8 src/ tests/ --max-line-length 100 --extend-ignore E203`

## Docker
- `docker-compose up -d`
- `docker-compose logs -f sono-eval`

## Utilities (Darwin)
- `ls`, `pwd`, `find`, `grep`, `sed`, `awk`, `cat`, `open <url>`
