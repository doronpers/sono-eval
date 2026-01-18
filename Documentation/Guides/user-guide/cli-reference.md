# CLI Reference

Complete command-line interface reference for Sono-Eval.

---

## Overview

The Sono-Eval CLI provides intuitive commands for all major operations:

```bash
sono-eval [OPTIONS] COMMAND [ARGS]...
```

**Global Options:**

- `--version` - Show version and exit
- `--help` - Show help message and exit

---

## Commands

### Assessment Commands

#### `assess run`

Run an assessment on code or content.

**Usage:**

```bash
sono-eval assess run [OPTIONS]
```

**Required Options:**

- `--candidate-id TEXT` - Unique candidate identifier

**Input Options (choose one):**

- `--file PATH` - Path to code file to assess
- `--content TEXT` - Direct content to assess

**Assessment Options:**

- `--type TEXT` - Submission type (default: "code")
- `--paths TEXT` - Assessment paths (can specify multiple)
  - Options: `technical`, `design`, `collaboration`, `problem_solving`, `communication`
- `--output PATH` - Save results to JSON file

**Examples:**

```bash
# Assess a Python file
sono-eval assess run \
  --candidate-id user001 \
  --file solution.py \
  --paths technical design

# Assess with all paths and save results
sono-eval assess run \
  --candidate-id user002 \
  --file app.js \
  --paths technical design collaboration problem_solving communication \
  --output results.json

# Assess direct content
sono-eval assess run \
  --candidate-id user003 \
  --content "def hello(): return 'world'" \
  --paths technical
```

**Output:**
Displays assessment results including:

- Overall score and confidence
- Summary
- Path scores table
- Key findings
- Recommendations

---

### Candidate Management Commands

#### `candidate create`

Create a new candidate profile.

**Usage:**

```bash
sono-eval candidate create [OPTIONS]
```

**Required Options:**

- `--id TEXT` - Candidate identifier

**Optional Options:**

- `--data JSON` - Initial data as JSON string

**Examples:**

```bash
# Create basic candidate
sono-eval candidate create --id candidate_001

# Create with initial data
sono-eval candidate create \
  --id candidate_002 \
  --data '{"name": "John Doe", "level": "senior"}'
```

---

#### `candidate show`

Display candidate information.

**Usage:**

```bash
sono-eval candidate show [OPTIONS]
```

**Required Options:**

- `--id TEXT` - Candidate identifier

**Examples:**

```bash
sono-eval candidate show --id candidate_001
```

**Output:**

- Candidate ID
- Last updated timestamp
- Number of memory nodes
- Version
- Root data (JSON)

---

#### `candidate list`

List all candidates.

**Usage:**

```bash
sono-eval candidate list
```

**Examples:**

```bash
sono-eval candidate list
```

**Output:**
List of all candidate IDs with count.

---

#### `candidate delete`

Delete a candidate (with confirmation).

**Usage:**

```bash
sono-eval candidate delete [OPTIONS]
```

**Required Options:**

- `--id TEXT` - Candidate identifier

**Examples:**

```bash
sono-eval candidate delete --id candidate_001
# Prompts for confirmation before deletion
```

---

### Tagging Commands

#### `tag generate`

Generate semantic tags for code or text.

**Usage:**

```bash
sono-eval tag generate [OPTIONS]
```

**Input Options (choose one):**

- `--file PATH` - Path to file to tag
- `--text TEXT` - Direct text to tag

**Optional Options:**

- `--max-tags INTEGER` - Maximum number of tags (default: 5)

**Examples:**

```bash
# Tag a file
sono-eval tag generate --file mycode.js

# Tag with more tags
sono-eval tag generate --file app.py --max-tags 10

# Tag direct text
sono-eval tag generate \
  --text "async function fetchData() { ... }" \
  --max-tags 3
```

**Output:**
List of tags with:

- Tag text
- Category
- Confidence score

---

### Server Commands

#### `server start`

Start the FastAPI server.

**Usage:**

```bash
sono-eval server start [OPTIONS]
```

**Optional Options:**

- `--host TEXT` - Host to bind to (default: from config)
- `--port INTEGER` - Port to bind to (default: from config)
- `--reload` - Enable auto-reload for development

**Examples:**

```bash
# Start with default settings
sono-eval server start

# Start with custom host/port
sono-eval server start --host 0.0.0.0 --port 9000

# Start in development mode with auto-reload
sono-eval server start --reload
```

**Access:**

- API: `http://localhost:8000`
- Interactive Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

### Configuration Commands

#### `config show`

Display current configuration.

**Usage:**

```bash
sono-eval config show
```

**Examples:**

```bash
sono-eval config show
```

**Output:**
Displays configuration sections:

- Application settings
- API settings
- Assessment settings
- Storage settings

---

## Output Formatting

### Colors and Styling

The CLI uses Rich for beautiful terminal output:

- **Blue** - Informational messages
- **Green** - Success messages
- **Yellow** - Warnings
- **Red** - Errors
- **Cyan** - Emphasis
- **Bold** - Headers and important info

### Tables

Assessment results and lists are displayed in formatted tables for easy reading.

### JSON Output

Use `--output` flag to save structured results to JSON files:

```bash
sono-eval assess run --candidate-id user001 --file code.py --output results.json
cat results.json | jq .
```

---

## Environment Variables

CLI commands respect environment variables from `.env`:

```bash
# Application
APP_ENV=development
DEBUG=true

# API Server
API_HOST=0.0.0.0
API_PORT=8000

# Assessment
ASSESSMENT_ENABLE_EXPLANATIONS=true
DARK_HORSE_MODE=enabled
```

See [Configuration Guide](configuration.md) for all variables.

---

## Exit Codes

- `0` - Success
- `1` - General error
- `2` - Invalid usage

---

## Common Workflows

### Basic Assessment Workflow

```bash
# 1. Create candidate
sono-eval candidate create --id new_candidate

# 2. Run assessment
sono-eval assess run \
  --candidate-id new_candidate \
  --file submission.py \
  --paths technical design \
  --output assessment.json

# 3. View candidate info
sono-eval candidate show --id new_candidate

# 4. Generate tags
sono-eval tag generate --file submission.py
```

### Batch Assessment Workflow

```bash
# Assess multiple files for same candidate
for file in submissions/*.py; do
  sono-eval assess run \
    --candidate-id batch_candidate \
    --file "$file" \
    --paths technical \
    --output "results/$(basename $file .py)_results.json"
done
```

### Development Workflow

```bash
# 1. Check config
sono-eval config show

# 2. Start server with auto-reload
sono-eval server start --reload

# 3. In another terminal, run assessments
sono-eval assess run --candidate-id dev_test --file test.py

# 4. View results in API docs
open http://localhost:8000/docs
```

---

## Tips and Tricks

### Use Shell Aliases

```bash
# Add to ~/.bashrc or ~/.zshrc
alias se='sono-eval'
alias sea='sono-eval assess run'
alias sec='sono-eval candidate'

# Then use shortcuts
se config show
sea --candidate-id user1 --file code.py
sec list
```

### Pipe Output

```bash
# Format JSON output
sono-eval candidate show --id user001 | jq .

# Count candidates
sono-eval candidate list | wc -l

# Search in output
sono-eval config show | grep -i debug
```

### Combine with Other Tools

```bash
# Assess all Python files in directory
find . -name "*.py" -exec sono-eval assess run \
  --candidate-id candidate1 \
  --file {} \
  --paths technical \;

# Watch for changes and reassess
watch -n 30 'sono-eval assess run --candidate-id watcher --file code.py'
```

### Docker Usage

```bash
# Run CLI commands in Docker
./launcher.sh cli assess run --candidate-id docker_user --file /path/to/file

# Interactive shell in container
docker-compose exec sono-eval bash
sono-eval --help
```

---

## Troubleshooting

### Command Not Found

```bash
# Ensure sono-eval is installed
pip install -e .

# Or add to PATH
export PATH=$PATH:/path/to/sono-eval
```

### Import Errors

```bash
# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Permission Errors

```bash
# Ensure data directories exist and are writable
mkdir -p data/memory data/tagstudio models/cache
chmod -R 755 data/
```

### Slow Performance

```bash
# T5 model loads on first use (can be slow)
# Subsequent runs use cached model

# Check model cache
ls -lh models/cache/
```

See the [Troubleshooting Guide](../troubleshooting.md) for more help.

---

## See Also

- [API Reference](api-reference.md) - REST API documentation
- [Configuration Guide](configuration.md) - Configure Sono-Eval
- [Examples](../resources/examples/) - Practical examples
- [Architecture](../concepts/architecture.md) - System architecture

---

**Last Updated**: January 10, 2026
**Version**: 0.1.1
