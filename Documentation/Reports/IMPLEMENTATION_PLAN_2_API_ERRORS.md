# Implementation Plan 2: API Error Responses & Developer Experience

**Impact**: HIGH | **Effort**: LOW | **Time**: 2–3h

---

## Prerequisites (exact files)

1. Error models/utilities: `src/sono_eval/utils/errors.py` (ErrorResponse at lines 49–56).  
2. Health checks: `src/sono_eval/api/main.py` (health checks at lines 230–534).  
3. API router entry points: `src/sono_eval/api/main.py` (place new endpoint near existing `/health` endpoints).

---

## Task A — Extend ErrorResponse with `help`

### Before (current)
- `ErrorResponse` includes `error`, `error_code`, `message`, `details`, `request_id`. (See `errors.py` lines 49–56.)

### After (target)
- Add a `help` field with: `valid_examples`, `suggestion`, `docs_url`.

#### Model Update (copy-paste)
**File**: `src/sono_eval/utils/errors.py`  
**Replace** the `ErrorResponse` class with:

```python
class ErrorHelp(BaseModel):
    """Helpful guidance for API clients."""

    valid_examples: Optional[list[dict[str, Any]]] = None
    suggestion: Optional[str] = None
    docs_url: Optional[str] = None


class ErrorResponse(BaseModel):
    """Standard error response format."""

    error: bool = True
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    request_id: Optional[str] = None
    help: Optional[ErrorHelp] = None
```

---

## Task B — Add HelpContext builder utilities

### Goal
Provide consistent `help` payloads per error type: validation, not-found, file-upload, and service errors.

#### New builder module (copy-paste)
**File**: `src/sono_eval/utils/error_help.py` (new)

```python
from typing import Any, Dict, Optional

from .errors import ErrorHelp


def validation_help(field: str, example: Dict[str, Any], docs_url: str) -> ErrorHelp:
    return ErrorHelp(
        valid_examples=[example],
        suggestion=f"Ensure '{field}' matches the documented format.",
        docs_url=docs_url,
    )


def not_found_help(resource: str, example: Dict[str, Any], docs_url: str) -> ErrorHelp:
    return ErrorHelp(
        valid_examples=[example],
        suggestion=f"Confirm the {resource} exists or create it before retrying.",
        docs_url=docs_url,
    )


def file_upload_help(max_size_mb: int, extensions: list[str], docs_url: str) -> ErrorHelp:
    return ErrorHelp(
        valid_examples=[{"max_size_mb": max_size_mb, "extensions": extensions}],
        suggestion="Validate file type/size and retry the upload.",
        docs_url=docs_url,
    )


def service_help(service: str, docs_url: str, hint: Optional[str] = None) -> ErrorHelp:
    return ErrorHelp(
        valid_examples=[{"service": service}],
        suggestion=hint or f"Verify {service} is healthy and retry.",
        docs_url=docs_url,
    )
```

#### Wire into create_error_response (copy-paste)
**File**: `src/sono_eval/utils/errors.py`  
**Add** `help` argument to `create_error_response` and pass it into `ErrorResponse`:

```python
def create_error_response(
    error_code: str,
    message: str,
    status_code: int = status.HTTP_400_BAD_REQUEST,
    details: Optional[Dict[str, Any]] = None,
    request_id: Optional[str] = None,
    help: Optional[ErrorHelp] = None,
) -> HTTPException:
    error_response = ErrorResponse(
        error=True,
        error_code=error_code,
        message=message,
        details=details,
        request_id=request_id,
        help=help,
    )
```

#### Usage example (copy-paste)
**File**: `src/sono_eval/api/main.py` (near candidate ID validation)

```python
from sono_eval.utils.error_help import validation_help

# Example usage
raise validation_error(
    CANDIDATE_ID_ERROR_MESSAGE,
    field="candidate_id",
    request_id=request_id,
    details={"pattern": "[A-Za-z0-9_.-]+"},
    help=validation_help(
        "candidate_id",
        {"candidate_id": "demo_user"},
        "/api/v1/errors#validation",
    ),
)
```

---

## Task C — Add component troubleshooting hints to health checks

### Before (current)
- Health checks show status and details but no actionable “how to fix” hints.

### After (target)
- Add `troubleshooting` hints per component in the detailed health check response.

#### Add hints (copy-paste)
**File**: `src/sono_eval/api/main.py`  
**Within** `check_component_health`, extend `details` to include `troubleshooting` hints, e.g.:

```python
if include_details:
    details["assessment"]["troubleshooting"] = "Restart the server to reinitialize the assessment engine."
```

Provide hints for:
- `assessment`: missing initialization
- `memory`: storage path permissions
- `tagging`: missing model cache
- `database`: invalid SQLite path
- `redis`: optional dependency not installed
- `filesystem`: non-writable directories

---

## Task D — Interactive Error Documentation Endpoint

### Goal
Expose a new endpoint: `/api/v1/errors` listing known error codes with examples and troubleshooting guidance.

#### Endpoint (copy-paste)
**File**: `src/sono_eval/api/main.py`  
**Add** below the existing health endpoints:

```python
@app.get("/api/v1/errors")
async def error_reference():
    return {
        "errors": [
            {
                "error_code": ErrorCode.VALIDATION_ERROR,
                "message": "Input validation failed",
                "help": {
                    "valid_examples": [{"candidate_id": "demo_user"}],
                    "suggestion": "Ensure the field follows the required format.",
                    "docs_url": "/api/v1/errors#validation",
                },
            },
            {
                "error_code": ErrorCode.NOT_FOUND,
                "message": "Resource not found",
                "help": {
                    "valid_examples": [{"candidate_id": "demo_user"}],
                    "suggestion": "Confirm the resource exists before retrying.",
                    "docs_url": "/api/v1/errors#not-found",
                },
            },
        ]
    }
```

---

## Testing Instructions

1. Run the API: `./launcher.sh start`.
2. Trigger a validation error (e.g., invalid `candidate_id`) and confirm the response includes `help`.
3. Hit `/api/v1/health` and verify troubleshooting hints are present in `details`.
4. Hit `/api/v1/errors` and confirm it returns the error reference list.

---

## Success Criteria

- ✅ Error responses include `help` with examples, suggestions, and docs URLs.
- ✅ Health check details include troubleshooting hints per component.
- ✅ `/api/v1/errors` returns a readable JSON index of error codes.

---

## Rollback Procedure

1. Revert `errors.py` model and remove `ErrorHelp` / `help` field.
2. Remove any error help references in API handlers.
3. Remove `/api/v1/errors` endpoint and any troubleshooting hints.

