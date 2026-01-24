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

**Version 0.2.0**: JWT Authentication is required for core endpoints.

### 1. Obtain Token

To access protected resources, first obtain a JWT access token:

#### `POST /api/v1/auth/token`

**Request (Form Data):**

- `username` (required)
- `password` (required)

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Example:**

```bash
curl -X POST http://localhost:8000/api/v1/auth/token \
  -F "username=admin" \
  -F "password=secret"
```

### 2. Use Token

Include the token in the `Authorization` header for subsequent requests:

```
Authorization: Bearer <your_access_token>
```

**Protected Endpoints:**

- `POST /api/v1/assessments`
- `POST /api/v1/candidates`
- `POST /api/v1/tags/generate`
- `POST /api/v1/files/upload`

---

---

## Response Format

Success responses return JSON objects as shown in each endpoint example.

Errors use FastAPI's standard `detail` wrapper with Sono-Eval error metadata:

```json
{
  "detail": {
    "error": true,
    "error_code": "VALIDATION_ERROR",
    "message": "candidate_id must contain only alphanumeric characters, dashes,
                and underscores",
    "details": {"field": "candidate_id"},
    "request_id": "..."
  }
}
```

---

## Endpoints

### Health & Status

#### `GET /health`

Basic health check endpoint. Returns component status without sensitive details.
Suitable for load balancers and monitoring tools.

**Response:**

```json
{
  "status": "healthy",
  "version": "0.1.1",
  "timestamp": "2026-01-10T12:00:00Z",
  "components": {
    "assessment": "operational",
    "memory": "operational",
    "tagging": "operational",
    "database": "operational",
    "redis": "operational",
    "filesystem": "operational"
  },
  "details": null
}
```

**Status Codes:**

- `200 OK`: System is healthy
- `503 Service Unavailable`: One or more components are unhealthy

**Example:**

```bash
curl http://localhost:8000/health
```

#### `GET /api/v1/health`

Detailed health check endpoint. Returns component status with detailed information.
Suitable for monitoring and debugging. Sensitive paths are sanitized.

**Response:**

```json
{
  "status": "healthy",
  "version": "0.1.1",
  "timestamp": "2026-01-10T12:00:00Z",
  "components": {
    "assessment": "operational",
    "memory": "operational",
    "tagging": "operational",
    "database": "operational",
    "redis": "operational",
    "filesystem": "operational"
  },
  "details": {
    "assessment": {
      "version": "1.0",
      "initialized": true
    },
    "memory": {
      "candidates_count": 5,
      "accessible": true
    },
    "tagging": {
      "model_name": "t5-base",
      "initialized": true
    },
    "database": {
      "type": "sqlite",
      "exists": true
    },
    "redis": {
      "connected": true
    },
    "filesystem": {
      "storage": {"writable": true},
      "cache": {"writable": true},
      "tagstudio": {"writable": true}
    }
  }
}
```

**Status Codes:**

- `200 OK`: System is healthy
- `503 Service Unavailable`: One or more components are unhealthy

**Component Status Values:**

- `operational`: Component is working correctly
- `degraded`: Component has issues but may still function
- `unavailable`: Component is not available (may be optional)
- `unhealthy`: Component has critical issues

**Note**: Health checks are cached for 5 seconds to avoid expensive operations
on every request.

**Example:**

```bash
curl http://localhost:8000/api/v1/health
```

#### `GET /`

Root endpoint with API information. Returns health status with details.

**Response:** Same format as `/api/v1/health`

#### `GET /status`

Detailed status information about the API configuration.

**Response:**

```json
{
  "api_version": "0.1.1",
  "assessment_engine_version": "1.0",
  "config": {
    "multi_path_tracking": true,
    "explanations_enabled": true,
    "dark_horse_mode": "enabled"
  }
}
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

**Notes:**

- `candidate_id` must contain only alphanumeric characters, dashes, and underscores.

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
- `candidate_id` (query, required) - Candidate identifier (alphanumeric, dashes,
  underscores)

**Response:**
Same structure as POST response above.

**Example:**

```bash
curl "http://localhost:8000/api/v1/assessments/assess_1234567890?candidate_id=candidate_001"
```

---

#### `GET /api/v1/assessments/{assessment_id}/dashboard`

Get visualization-ready dashboard data for an assessment.

**Parameters:**

- `assessment_id` (path) - Assessment identifier
- `candidate_id` (query, required) - Candidate identifier (alphanumeric, dashes,
  underscores)
- `include_history` (query, optional) - Include historical trend data
  (`true`/`false`)

**Response:**

```json
{
  "overall_score": 85.5,
  "overall_grade": "B",
  "confidence": 0.9,
  "summary": "Short summary...",
  "path_scores": [...],
  "trend_data": [...],
  "assessment_id": "assess_1234567890",
  "candidate_id": "candidate_001"
}
```

**Example:**

```bash
curl "http://localhost:8000/api/v1/assessments/assess_1234567890/dashboard?candidate_id=candidate_001&include_history=true"
```

#### `POST /api/v1/assessments/async`

**NEW in v0.2.0**: Create an assessment asynchronously using the task queue.

This endpoint queues the assessment for background processing and immediately
returns a job ID. Use this for long-running assessments or batch processing.

**Request Body:** Same as `POST /api/v1/assessments`

```json
{
  "candidate_id": "candidate_001",
  "submission_type": "code",
  "content": {
    "code": "def hello(): return 'world'"
  },
  "paths_to_evaluate": ["technical", "design"]
}
```

**Response:**

```json
{
  "job_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "assessment_id": "assess_1234567890",
  "candidate_id": "candidate_001",
  "status": "queued",
  "message": "Assessment queued for processing",
  "status_url": "/api/v1/assessments/jobs/a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

**Status Codes:**

- `200 OK`: Assessment queued successfully
- `400 Bad Request`: Invalid input data
- `500 Internal Server Error`: Failed to queue assessment

**Example:**

```bash
curl -X POST http://localhost:8000/api/v1/assessments/async \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": "candidate_001",
    "submission_type": "code",
    "content": {"code": "def hello(): return '\''world'\''"},
    "paths_to_evaluate": ["technical"]
  }'
```

**Benefits:**

- **Non-blocking**: Returns immediately without waiting for assessment completion
- **Scalable**: Multiple assessments can be processed in parallel by workers
- **Reliable**: Automatic retry on failures with exponential backoff
- **Trackable**: Monitor progress using the job status endpoint

#### `GET /api/v1/assessments/jobs/{job_id}`

**NEW in v0.2.0**: Get the status of an asynchronous assessment job.

**Parameters:**

- `job_id` (path) - Celery task ID returned from async assessment creation

**Response States:**

**Queued (PENDING):**

```json
{
  "job_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "PENDING",
  "message": "Assessment is queued and waiting to start"
}
```

**Processing (PROCESSING):**

```json
{
  "job_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "PROCESSING",
  "assessment_id": "assess_1234567890",
  "candidate_id": "candidate_001",
  "progress": 50
}
```

**Completed (SUCCESS):**

```json
{
  "job_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "completed",
  "message": "Assessment completed successfully",
  "result": {
    "assessment_id": "assess_1234567890",
    "candidate_id": "candidate_001",
    "overall_score": 85.5,
    "confidence": 0.9,
    "path_scores": [...],
    "micro_motives": [...],
    "summary": "...",
    "processing_time_ms": 1234.56
  }
}
```

**Failed (FAILURE):**

```json
{
  "job_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "failed",
  "error": "Assessment validation failed",
  "message": "Assessment failed with error"
}
```

**Status Codes:**

- `200 OK`: Job status retrieved successfully
- `404 Not Found`: Job ID not found
- `503 Service Unavailable`: Task queue system unavailable

**Example:**

```bash
# Poll for job status
curl http://localhost:8000/api/v1/assessments/jobs/a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

**Polling Best Practices:**

- Start with 1-second intervals
- Increase to 5 seconds after 10 polls
- Set maximum poll duration (e.g., 5 minutes)
- Check for `completed` or `failed` status

**Example Polling Script:**

```bash
#!/bin/bash
JOB_ID="$1"
MAX_ATTEMPTS=60
POLL_INTERVAL=2

for i in $(seq 1 $MAX_ATTEMPTS); do
  STATUS=$(curl -s "http://localhost:8000/api/v1/assessments/jobs/$JOB_ID" | jq -r '.status')

  if [ "$STATUS" = "completed" ]; then
    echo "Assessment completed!"
    curl -s "http://localhost:8000/api/v1/assessments/jobs/$JOB_ID" | jq '.result'
    exit 0
  elif [ "$STATUS" = "failed" ]; then
    echo "Assessment failed!"
    curl -s "http://localhost:8000/api/v1/assessments/jobs/$JOB_ID" | jq '.error'
    exit 1
  fi

  echo "Status: $STATUS (attempt $i/$MAX_ATTEMPTS)"
  sleep $POLL_INTERVAL
done

echo "Timeout waiting for assessment"
exit 1
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

**Notes:**

- `candidate_id` must contain only alphanumeric characters, dashes, and underscores.

**Response:**

```json
{
  "candidate_id": "string",
  "created": "ISO 8601",
  "status": "created"
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

- `candidate_id` (path) - Candidate identifier (alphanumeric, dashes, underscores)

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

**Response:**

```json
{
  "candidates": ["candidate_001", "candidate_002", ...],
  "count": 10
}
```

**Example:**

```bash
curl "http://localhost:8000/api/v1/candidates"
```

---

#### `DELETE /api/v1/candidates/{candidate_id}`

Delete a candidate.

**Parameters:**

- `candidate_id` (path) - Candidate identifier (alphanumeric, dashes, underscores)

**Response:**

```json
{
  "status": "deleted",
  "candidate_id": "string"
}
```

**Example:**

```bash
curl -X DELETE http://localhost:8000/api/v1/candidates/candidate_001
```

---

#### `GET /api/v1/candidates/{candidate_id}/stats`

Get aggregate statistics and trend information for a candidate.

**Parameters:**

- `candidate_id` (path) - Candidate identifier (alphanumeric, dashes, underscores)

**Response:**

```json
{
  "candidate_id": "candidate_001",
  "total_assessments": 3,
  "statistics": {
    "average_score": 82.3,
    "best_score": 90.1,
    "worst_score": 74.5,
    "latest_score": 85.0,
    "average_confidence": 0.78,
    "score_std_dev": 6.2
  },
  "path_averages": {"technical": 84.0, "design": 79.5},
  "trend": {
    "direction": "stable",
    "recent_average": 83.0,
    "historical_average": 81.5
  },
  "first_assessment": "2024-01-10T12:00:00Z",
  "last_assessment": "2024-01-20T12:00:00Z"
}
```

**Example:**

```bash
curl "http://localhost:8000/api/v1/candidates/candidate_001/stats"
```

---

### Tagging Endpoints

#### `POST /api/v1/tags/generate`

Generate semantic tags for code or text.

**Request Body:**

```json
{
  "text": "string",
  "max_tags": 5
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
  "count": 1
}
```

**Example:**

```bash
curl -X POST http://localhost:8000/api/v1/tags/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "async function fetchData() { const res = await fetch(url); "
            "return res.json(); }",
    "max_tags": 3
  }'
```

---

### File Upload

#### `POST /api/v1/files/upload`

Upload a UTF-8 text file for assessment and optional tag generation.

**Request (multipart/form-data):**

- `file` (required) - Text file with an allowed extension

**Response:**

```json
{
  "filename": "solution.py",
  "original_filename": "solution.py",
  "size": 1234,
  "tags": [],
  "status": "uploaded"
}
```

**Example:**

```bash
curl -X POST http://localhost:8000/api/v1/files/upload \
  -H "Content-Type: multipart/form-data" \
  -F "file=@solution.py"
```

---

## Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| `VALIDATION_ERROR` | Request validation failed | 400 |
| `INVALID_FORMAT` | Invalid payload format | 400 |
| `NOT_FOUND` | Resource not found | 404 |
| `DUPLICATE_RESOURCE` | Resource already exists | 409 |
| `SERVICE_UNAVAILABLE` | Required component unavailable | 503 |
| `FILE_TOO_LARGE` | Upload exceeds size limit | 400 |
| `INVALID_FILE_TYPE` | Upload file type not allowed | 400 |
| `INTERNAL_ERROR` | Server error | 500 |

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
- [Quick Start](../QUICK_START.md) - Get started quickly
- [Examples](../resources/examples/README.md) - Practical code examples
- [Architecture](../../Core/concepts/architecture.md) - System design

---

**Last Updated**: January 15, 2026
**Version**: 0.2.0
