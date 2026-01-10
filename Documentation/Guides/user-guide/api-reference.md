# API Reference

Complete REST API documentation for Sono-Eval.

---

## Base URL

**Local Development**: `http://localhost:8000`  
**Production**: Configure via `API_HOST` and `API_PORT` in `.env`

---

## API Documentation

Interactive API documentation is available at:

- **Swagger UI**: `http://localhost:8000/docs` (recommended)
- **ReDoc**: `http://localhost:8000/redoc` (alternative view)

---

## Authentication

**Version 0.1.0**: No authentication required (development mode)  
**Production**: Will require API keys (coming soon)

---

## Response Format

All responses follow this structure:

**Success (200-299):**
```json
{
  "data": { ... },
  "status": "success"
}
```

**Error (400-599):**
```json
{
  "detail": "Error message",
  "status": "error",
  "code": "ERROR_CODE"
}
```

---

## Endpoints

### Health & Status

#### `GET /api/v1/health`
Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2026-01-10T12:00:00Z"
}
```

**Example:**
```bash
curl http://localhost:8000/api/v1/health
```

---

### Assessment Endpoints

#### `POST /api/v1/assessments`
Create and run a new assessment.

**Request Body:**
```json
{
  "candidate_id": "string",
  "submission_type": "code",
  "content": {
    "code": "string",
    "description": "string (optional)"
  },
  "paths_to_evaluate": ["TECHNICAL", "DESIGN"],
  "metadata": {
    "challenge_id": "string (optional)",
    "timestamp": "ISO 8601 (optional)"
  }
}
```

**Path Types:**
- `TECHNICAL` - Code quality, algorithms, problem-solving
- `DESIGN` - Architecture, patterns, system design
- `COLLABORATION` - Documentation, communication
- `PROBLEM_SOLVING` - Analytical thinking, approach
- `COMMUNICATION` - Clarity, explanation quality

**Response:**
```json
{
  "candidate_id": "string",
  "assessment_id": "string",
  "overall_score": 85.5,
  "confidence": 0.9,
  "path_scores": [
    {
      "path": "TECHNICAL",
      "overall_score": 88.0,
      "metrics": [...],
      "motives": [...],
      "strengths": [...],
      "areas_for_improvement": [...]
    }
  ],
  "micro_motives": [...],
  "dominant_path": "TECHNICAL",
  "summary": "string",
  "key_findings": [...],
  "recommendations": [...],
  "engine_version": "1.0",
  "processing_time_ms": 1234.56,
  "timestamp": "ISO 8601"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/v1/assessments \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": "candidate_001",
    "submission_type": "code",
    "content": {
      "code": "def factorial(n):\n    return 1 if n <= 1 else n * factorial(n-1)"
    },
    "paths_to_evaluate": ["TECHNICAL", "DESIGN"]
  }'
```

**Python Example:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/assessments",
    json={
        "candidate_id": "candidate_001",
        "submission_type": "code",
        "content": {"code": "def hello(): return 'world'"},
        "paths_to_evaluate": ["TECHNICAL"]
    }
)

result = response.json()
print(f"Score: {result['overall_score']}")
```

---

#### `GET /api/v1/assessments/{assessment_id}`
Get assessment by ID.

**Parameters:**
- `assessment_id` (path) - Assessment identifier

**Response:**
Same structure as POST response above.

**Example:**
```bash
curl http://localhost:8000/api/v1/assessments/assess_1234567890
```

---

### Candidate Endpoints

#### `POST /api/v1/candidates`
Create a new candidate profile.

**Request Body:**
```json
{
  "candidate_id": "string",
  "initial_data": {
    "name": "string (optional)",
    "email": "string (optional)",
    "level": "string (optional)",
    "custom_field": "any (optional)"
  }
}
```

**Response:**
```json
{
  "candidate_id": "string",
  "created_at": "ISO 8601",
  "version": "1.0",
  "message": "Candidate created successfully"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/v1/candidates \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": "candidate_001",
    "initial_data": {"name": "Alex Chen", "level": "intern"}
  }'
```

---

#### `GET /api/v1/candidates/{candidate_id}`
Get candidate information.

**Parameters:**
- `candidate_id` (path) - Candidate identifier

**Response:**
```json
{
  "candidate_id": "string",
  "last_updated": "ISO 8601",
  "version": "string",
  "nodes": 5,
  "root_data": {...},
  "memory_structure": {
    "depth": 5,
    "total_nodes": 10
  }
}
```

**Example:**
```bash
curl http://localhost:8000/api/v1/candidates/candidate_001
```

---

#### `GET /api/v1/candidates`
List all candidates.

**Query Parameters:**
- `limit` (optional) - Maximum results (default: 100)
- `offset` (optional) - Pagination offset (default: 0)

**Response:**
```json
{
  "candidates": ["candidate_001", "candidate_002", ...],
  "total": 10,
  "limit": 100,
  "offset": 0
}
```

**Example:**
```bash
curl "http://localhost:8000/api/v1/candidates?limit=50&offset=0"
```

---

#### `DELETE /api/v1/candidates/{candidate_id}`
Delete a candidate.

**Parameters:**
- `candidate_id` (path) - Candidate identifier

**Response:**
```json
{
  "message": "Candidate deleted successfully",
  "candidate_id": "string"
}
```

**Example:**
```bash
curl -X DELETE http://localhost:8000/api/v1/candidates/candidate_001
```

---

### Tagging Endpoints

#### `POST /api/v1/tags/generate`
Generate semantic tags for code or text.

**Request Body:**
```json
{
  "text": "string",
  "max_tags": 5,
  "context": "string (optional)"
}
```

**Response:**
```json
{
  "tags": [
    {
      "tag": "async-programming",
      "category": "pattern",
      "confidence": 0.92,
      "context": "async function fetchData...",
      "metadata": {}
    }
  ],
  "total_generated": 5,
  "model_used": "t5-base"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/v1/tags/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "async function fetchData() { const res = await fetch(url); return res.json(); }",
    "max_tags": 3
  }'
```

---

## Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| `INVALID_INPUT` | Request validation failed | 400 |
| `NOT_FOUND` | Resource not found | 404 |
| `INTERNAL_ERROR` | Server error | 500 |
| `ASSESSMENT_FAILED` | Assessment processing failed | 500 |
| `CANDIDATE_EXISTS` | Candidate already exists | 409 |
| `MODEL_ERROR` | ML model error | 500 |

---

## Rate Limiting

**Current**: No rate limiting (development)  
**Production**: Will implement rate limiting (details TBD)

---

## CORS

CORS is enabled for all origins in development mode.

**Production**: Will be restricted to allowed origins.

---

## Webhooks

**Coming Soon**: Webhook support for assessment completion notifications.

---

## SDKs and Client Libraries

### Python
```python
# Use requests library
import requests

class SonoEvalClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def assess(self, candidate_id, code, paths=None):
        response = requests.post(
            f"{self.base_url}/api/v1/assessments",
            json={
                "candidate_id": candidate_id,
                "submission_type": "code",
                "content": {"code": code},
                "paths_to_evaluate": paths or ["TECHNICAL"]
            }
        )
        return response.json()

# Usage
client = SonoEvalClient()
result = client.assess("user001", "def hello(): pass")
print(result['overall_score'])
```

### JavaScript/TypeScript
```javascript
// Use fetch API
class SonoEvalClient {
  constructor(baseUrl = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }

  async assess(candidateId, code, paths = ['TECHNICAL']) {
    const response = await fetch(`${this.baseUrl}/api/v1/assessments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        candidate_id: candidateId,
        submission_type: 'code',
        content: { code },
        paths_to_evaluate: paths
      })
    });
    return response.json();
  }
}

// Usage
const client = new SonoEvalClient();
const result = await client.assess('user001', 'function hello() {}');
console.log(result.overall_score);
```

---

## Best Practices

### Error Handling
Always check response status and handle errors gracefully:

```python
response = requests.post(url, json=data)
if response.status_code == 200:
    result = response.json()
else:
    error = response.json()
    print(f"Error: {error['detail']}")
```

### Timeouts
Set reasonable timeouts for assessment requests:

```python
response = requests.post(url, json=data, timeout=30)
```

### Retry Logic
Implement exponential backoff for retries:

```python
from time import sleep

def assess_with_retry(data, max_retries=3):
    for i in range(max_retries):
        try:
            response = requests.post(url, json=data, timeout=30)
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException:
            if i < max_retries - 1:
                sleep(2 ** i)  # Exponential backoff
    raise Exception("Max retries exceeded")
```

---

## See Also

- [CLI Reference](cli-reference.md) - Command-line interface
- [Quick Start](../quick-start.md) - Get started quickly
- [Examples](../resources/examples/) - Practical code examples
- [Architecture](../concepts/architecture.md) - System design

---

**Last Updated**: January 10, 2026  
**Version**: 0.1.0
