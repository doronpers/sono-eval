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
- `src/sono_eval/utils/errors.py` lines 49–56 define `ErrorResponse` without any help payload.

### After (target)
- Add a `help` field with: `valid_examples`, `suggestion`, `docs_url`.

<<<<<<< HEAD:Documentation/Archive/Reports-Historical/IMPLEMENTATION_PLAN_2_API_ERRORS.md
2. Understand the current error response structure:

   ```python
   {
       "error": true,
       "error_code": "VALIDATION_ERROR",
       "message": "...",
       "details": {...},
       "request_id": "..."
   }
   ```

3. Test the current API:

   ```bash
   ./launcher.sh start
   # Open http://localhost:8000/docs
   # Try various error scenarios
   ```

4. Review FastAPI error handling:
   - OpenAPI/Swagger docs at `/docs`
   - Error response models
   - Validation patterns

---

## Task 1: Enhance Error Response Model

**File**: `src/sono_eval/utils/errors.py`

### Current Issues

- Error responses lack actionable guidance
- No examples of correct usage
- Missing links to documentation
- Generic messages without context

### Changes Required

#### 1.1: Extend ErrorResponse Model

**Replace lines 49-57** with enhanced model:
=======
#### Model Update (copy-paste)
**File**: `src/sono_eval/utils/errors.py`  
**Replace** the `ErrorResponse` class with:
>>>>>>> 6b7113d6352e4fb7d7504d7a7d221ee1ac543c33:Documentation/Reports/IMPLEMENTATION_PLAN_2_API_ERRORS.md

```python
class ErrorHelp(BaseModel):
    """Helpful guidance for API clients."""

    valid_examples: Optional[list[dict[str, Any]]] = None
    suggestion: Optional[str] = None
    docs_url: Optional[str] = None


class ErrorResponse(BaseModel):
<<<<<<< HEAD:Documentation/Archive/Reports-Historical/IMPLEMENTATION_PLAN_2_API_ERRORS.md
    """Standard error response format with actionable guidance."""
=======
    """Standard error response format."""
>>>>>>> 6b7113d6352e4fb7d7504d7a7d221ee1ac543c33:Documentation/Reports/IMPLEMENTATION_PLAN_2_API_ERRORS.md

    error: bool = True
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    request_id: Optional[str] = None
<<<<<<< HEAD:Documentation/Archive/Reports-Historical/IMPLEMENTATION_PLAN_2_API_ERRORS.md

    class Config:
        json_schema_extra = {
            "example": {
                "error": True,
                "error_code": "VALIDATION_ERROR",
                "message": "candidate_id must contain only alphanumeric characters, dashes, and underscores",
                "details": {
                    "field": "candidate_id",
                    "received": "john@doe",
                    "pattern": "^[a-zA-Z0-9_-]+$"
                },
                "help": {
                    "suggestion": "Replace special characters with dashes or underscores",
                    "valid_examples": ["john_doe", "candidate-001", "user123"],
                    "docs_url": "/docs#candidate-id-format"
                },
                "request_id": "abc-123-def-456"
            }
        }
=======
    help: Optional[ErrorHelp] = None
>>>>>>> 6b7113d6352e4fb7d7504d7a7d221ee1ac543c33:Documentation/Reports/IMPLEMENTATION_PLAN_2_API_ERRORS.md
```

---

## Task B — Add HelpContext builder utilities

### Goal
Provide consistent `help` payloads per error type: validation, not-found, file-upload, and service errors.

#### New builder module (copy-paste)
**File**: `src/sono_eval/utils/error_help.py` (new)

```python
<<<<<<< HEAD:Documentation/Archive/Reports-Historical/IMPLEMENTATION_PLAN_2_API_ERRORS.md
class HelpContext:
    """Builder for help context in error responses."""

    @staticmethod
    def for_validation(
        field: str,
        pattern: Optional[str] = None,
        examples: Optional[List[str]] = None,
        docs_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create help context for validation errors."""
        help_dict = {}

        if examples:
            help_dict["valid_examples"] = examples

        if pattern:
            help_dict["pattern"] = pattern
            help_dict["explanation"] = f"Must match pattern: {pattern}"

        if docs_path:
            help_dict["docs_url"] = docs_path

        return help_dict

    @staticmethod
    def for_not_found(
        resource_type: str,
        search_endpoint: Optional[str] = None,
        create_endpoint: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create help context for not found errors."""
        help_dict = {
            "suggestion": f"Verify the {resource_type} exists or create a new one"
        }

        if search_endpoint:
            help_dict["search_url"] = search_endpoint

        if create_endpoint:
            help_dict["create_url"] = create_endpoint
            help_dict["next_steps"] = f"Create a new {resource_type} using POST {create_endpoint}"

        return help_dict

    @staticmethod
    def for_file_upload(
        max_size_mb: int,
        allowed_types: List[str],
        example_curl: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create help context for file upload errors."""
        help_dict = {
            "requirements": {
                "max_size": f"{max_size_mb}MB",
                "allowed_types": allowed_types
            },
            "suggestion": "Ensure file meets size and type requirements"
        }

        if example_curl:
            help_dict["example_request"] = example_curl

        return help_dict

    @staticmethod
    def for_service_error(
        service_name: str,
        health_check_url: Optional[str] = None,
        retry_seconds: Optional[int] = None
    ) -> Dict[str, Any]:
        """Create help context for service unavailable errors."""
        help_dict = {
            "suggestion": f"The {service_name} is temporarily unavailable"
        }

        if health_check_url:
            help_dict["health_check_url"] = health_check_url
            help_dict["next_steps"] = f"Check service status at {health_check_url}"

        if retry_seconds:
            help_dict["retry_after"] = f"{retry_seconds} seconds"

        return help_dict
=======
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
>>>>>>> 6b7113d6352e4fb7d7504d7a7d221ee1ac543c33:Documentation/Reports/IMPLEMENTATION_PLAN_2_API_ERRORS.md
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
<<<<<<< HEAD:Documentation/Archive/Reports-Historical/IMPLEMENTATION_PLAN_2_API_ERRORS.md
    """
    Create a standardized HTTP exception with error response.

    Args:
        error_code: Standard error code from ErrorCode
        message: Human-readable error message
        status_code: HTTP status code
        details: Optional additional error details
        help_context: Optional actionable help/guidance for resolving the error
        request_id: Optional request ID for tracking

    Returns:
        HTTPException with standardized error response

    Example:
        >>> help_ctx = HelpContext.for_validation(
        ...     field="email",
        ...     pattern="^[^@]+@[^@]+\\.[^@]+$",
        ...     examples=["user@example.com"]
        ... )
        >>> raise create_error_response(
        ...     ErrorCode.VALIDATION_ERROR,
        ...     "Invalid email format",
        ...     help_context=help_ctx
        ... )
    """
=======
>>>>>>> 6b7113d6352e4fb7d7504d7a7d221ee1ac543c33:Documentation/Reports/IMPLEMENTATION_PLAN_2_API_ERRORS.md
    error_response = ErrorResponse(
        error=True,
        error_code=error_code,
        message=message,
        details=details,
        request_id=request_id,
<<<<<<< HEAD:Documentation/Archive/Reports-Historical/IMPLEMENTATION_PLAN_2_API_ERRORS.md
    )

    return HTTPException(
        status_code=status_code,
        detail=error_response.model_dump(exclude_none=True),
=======
        help=help,
>>>>>>> 6b7113d6352e4fb7d7504d7a7d221ee1ac543c33:Documentation/Reports/IMPLEMENTATION_PLAN_2_API_ERRORS.md
    )
```

#### Usage example (copy-paste)
**File**: `src/sono_eval/api/main.py` (near candidate ID validation)

```python
<<<<<<< HEAD:Documentation/Archive/Reports-Historical/IMPLEMENTATION_PLAN_2_API_ERRORS.md
def validation_error(
    message: str,
    field: Optional[str] = None,
    received_value: Optional[str] = None,
    pattern: Optional[str] = None,
    examples: Optional[List[str]] = None,
    details: Optional[Dict[str, Any]] = None,
    request_id: Optional[str] = None,
) -> HTTPException:
    """
    Create a validation error response with actionable help.

    Args:
        message: Error message
        field: Field name that failed validation
        received_value: The invalid value that was received
        pattern: Regex pattern for valid values
        examples: List of valid example values
        details: Additional error details
        request_id: Request tracking ID

    Returns:
        HTTPException with validation error and help context
    """
    error_details = details or {}
    if field:
        error_details["field"] = field
    if received_value:
        error_details["received"] = received_value
    if pattern:
        error_details["pattern"] = pattern

    # Build help context
    help_context = None
    if field and (pattern or examples):
        help_context = HelpContext.for_validation(
            field=field,
            pattern=pattern,
            examples=examples,
            docs_path=f"/docs#field-{field.replace('_', '-')}"
        )

        # Add specific suggestion based on common patterns
        if "candidate_id" in field.lower():
            help_context["suggestion"] = "Replace special characters with dashes or underscores"
        elif "email" in field.lower():
            help_context["suggestion"] = "Ensure email includes @ symbol and domain"
        elif "url" in field.lower():
            help_context["suggestion"] = "Include protocol (http:// or https://)"

    return create_error_response(
        error_code=ErrorCode.VALIDATION_ERROR,
        message=message,
        status_code=status.HTTP_400_BAD_REQUEST,
        details=error_details,
        help_context=help_context,
        request_id=request_id,
    )
```

#### 2.2: Enhance not_found_error

**Replace lines 113-129** with:

```python
def not_found_error(
    resource_type: str,
    resource_id: Optional[str] = None,
    search_endpoint: Optional[str] = None,
    create_endpoint: Optional[str] = None,
    request_id: Optional[str] = None,
) -> HTTPException:
    """
    Create a not found error response with next steps.

    Args:
        resource_type: Type of resource (e.g., "Assessment", "Candidate")
        resource_id: ID of the resource that wasn't found
        search_endpoint: Endpoint to search for resources
        create_endpoint: Endpoint to create new resource
        request_id: Request tracking ID

    Returns:
        HTTPException with not found error and help context
    """
    message = f"{resource_type} not found"
    if resource_id:
        message += f": {resource_id}"

    help_context = HelpContext.for_not_found(
        resource_type=resource_type.lower(),
        search_endpoint=search_endpoint,
        create_endpoint=create_endpoint
    )

    return create_error_response(
        error_code=ErrorCode.NOT_FOUND,
        message=message,
        status_code=status.HTTP_404_NOT_FOUND,
        details={
            "resource_type": resource_type,
            "resource_id": resource_id
        },
        help_context=help_context,
        request_id=request_id,
    )
```

#### 2.3: Enhance file_upload_error

**Replace lines 161-174** with:

```python
def file_upload_error(
    message: str,
    error_type: str = ErrorCode.INVALID_FILE_TYPE,
    max_size_mb: int = 10,
    allowed_types: Optional[List[str]] = None,
    details: Optional[Dict[str, Any]] = None,
    request_id: Optional[str] = None,
) -> HTTPException:
    """
    Create a file upload error response with requirements and examples.

    Args:
        message: Error message
        error_type: Specific error code
        max_size_mb: Maximum file size in MB
        allowed_types: List of allowed MIME types
        details: Additional error details
        request_id: Request tracking ID

    Returns:
        HTTPException with file upload error and help context
    """
    allowed = allowed_types or ["text/plain", "text/x-python", "application/javascript"]

    example_curl = f"""curl -X POST http://localhost:8000/api/v1/assessments \\
  -H "Content-Type: multipart/form-data" \\
  -F "file=@solution.py" \\
  -F "candidate_id=candidate_001" \\
  -F "paths=TECHNICAL"
"""

    help_context = HelpContext.for_file_upload(
        max_size_mb=max_size_mb,
        allowed_types=allowed,
        example_curl=example_curl
    )

    return create_error_response(
        error_code=error_type,
        message=message,
        status_code=status.HTTP_400_BAD_REQUEST,
        details=details,
        help_context=help_context,
        request_id=request_id,
    )
```

#### 2.4: Enhance service_unavailable_error

**Replace lines 147-158** with:

```python
def service_unavailable_error(
    service: str,
    health_check_url: Optional[str] = None,
    retry_after: Optional[int] = 30,
    request_id: Optional[str] = None,
) -> HTTPException:
    """
    Create a service unavailable error response with troubleshooting.

    Args:
        service: Name of unavailable service
        health_check_url: URL to check service health
        retry_after: Suggested retry delay in seconds
        request_id: Request tracking ID

    Returns:
        HTTPException with service unavailable error and help context
    """
    help_context = HelpContext.for_service_error(
        service_name=service,
        health_check_url=health_check_url or "/api/v1/health",
        retry_seconds=retry_after
    )

    return create_error_response(
        error_code=ErrorCode.SERVICE_UNAVAILABLE,
        message=f"{service} is currently unavailable",
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        details={"service": service},
        help_context=help_context,
        request_id=request_id,
    )
```

---

## Task 3: Update API Validation Error Messages

**File**: `src/sono_eval/api/main.py`

### Enhance candidate ID validation

#### 3.1: Update Candidate ID Validation

**Find line 73-74** and **update line 219-222**:

```python
# At top of file (line 73-74) - Keep constant but enhance usage
CANDIDATE_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+$")
CANDIDATE_ID_EXAMPLES = ["john_doe", "candidate-001", "user_123", "test-candidate"]

# Update the validation function (around line 214-222)
def _validate_candidate_id(candidate_id: str, request_id: Optional[str] = None) -> None:
    """
    Validate candidate_id format to prevent path traversal and injection.

    Args:
        candidate_id: Candidate identifier to validate
        request_id: Request ID for error tracking

    Raises:
        HTTPException: If candidate_id format is invalid
    """
    if not CANDIDATE_ID_PATTERN.match(candidate_id):
        raise validation_error(
            message="candidate_id must contain only alphanumeric characters, dashes, and underscores",
            field="candidate_id",
            received_value=candidate_id,
            pattern=r"^[a-zA-Z0-9_-]+$",
            examples=CANDIDATE_ID_EXAMPLES,
            request_id=request_id,
        )
```

#### 3.2: Enhance Assessment Not Found Errors

**Find the assessment retrieval endpoint** (around line 500-600):

```python
@app.get("/api/v1/assessments/{assessment_id}")
async def get_assessment(
    assessment_id: str,
    request: Request,
    include_details: bool = True
):
    """
    Retrieve a specific assessment by ID.

    Args:
        assessment_id: Assessment identifier
        include_details: Whether to include detailed evidence

    Returns:
        Assessment result with scores and explanations

    Raises:
        HTTPException: If assessment not found
    """
    request_id = getattr(request.state, "request_id", None)

    try:
        result = memu_storage.get_assessment(assessment_id)
        if not result:
            raise not_found_error(
                resource_type="Assessment",
                resource_id=assessment_id,
                search_endpoint="/api/v1/assessments",
                create_endpoint="/api/v1/assessments",
                request_id=request_id,
            )

        return result
    except Exception as e:
        logger.error(f"Error retrieving assessment: {e}", exc_info=True)
        raise internal_error(
            message="Failed to retrieve assessment",
            details={"assessment_id": assessment_id},
            request_id=request_id
        )
```

#### 3.3: Add Better File Upload Error Messages

**Find file upload endpoint** (if exists, otherwise this is informational):

```python
@app.post("/api/v1/assessments/upload")
async def upload_assessment(
    file: UploadFile = File(...),
    candidate_id: str = Form(...),
    paths: List[str] = Form(...),
    request: Request = None
):
    """Upload and assess a code file."""
    request_id = getattr(request.state, "request_id", None)

    # Validate file size
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise file_upload_error(
            message=f"File too large. Maximum size is 10MB, received {len(content) / 1024 / 1024:.1f}MB",
            error_type=ErrorCode.FILE_TOO_LARGE,
            max_size_mb=10,
            details={"received_size_mb": len(content) / 1024 / 1024},
            request_id=request_id
        )

    # Validate file type
    ALLOWED_TYPES = ["text/plain", "text/x-python", "application/javascript", "text/x-java"]
    if file.content_type not in ALLOWED_TYPES:
        raise file_upload_error(
            message=f"Invalid file type: {file.content_type}",
            error_type=ErrorCode.INVALID_FILE_TYPE,
            allowed_types=ALLOWED_TYPES,
            details={"received_type": file.content_type},
            request_id=request_id
        )

    # ... rest of upload logic ...
```

---

## Task 4: Enhance Health Check Response

**File**: `src/sono_eval/api/main.py`

### Add troubleshooting hints to health check

#### 4.1: Enhance Health Check Details

**Find the health check endpoint** (around line 350-400):

```python
@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check(request: Request, detailed: bool = False):
    """
    Health check endpoint with optional troubleshooting hints.

    Args:
        detailed: Include detailed component status and troubleshooting

    Returns:
        Health status of all components
    """
    request_id = getattr(request.state, "request_id", None)
    components = await check_component_health(include_details=detailed)

    # Determine overall status
    overall_status = "healthy"
    if any(v == "unavailable" for v in components["components"].values()):
        overall_status = "unavailable"
    elif any(v == "degraded" for v in components["components"].values()):
        overall_status = "degraded"

    response = {
        "status": overall_status,
        "version": API_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "components": components["components"],
    }

    if detailed:
        response["details"] = components.get("details", {})

        # Add troubleshooting hints for unhealthy components
        if overall_status != "healthy":
            response["troubleshooting"] = generate_troubleshooting_hints(components)

    return response

def generate_troubleshooting_hints(health_data: Dict[str, Any]) -> Dict[str, List[str]]:
    """Generate troubleshooting hints based on component health."""
    hints = {}
    components = health_data.get("components", {})
    details = health_data.get("details", {})

    for component, status in components.items():
        if status in ["unavailable", "degraded"]:
            component_hints = []

            if component == "assessment":
                component_hints = [
                    "Verify AssessmentEngine initialized correctly",
                    "Check application logs for startup errors",
                    "Ensure all required dependencies are installed",
                    "Try: docker-compose restart sono-eval"
                ]

            elif component == "memory":
                storage_path = details.get("memory", {}).get("storage_path")
                component_hints = [
                    "Verify storage directory exists and is writable",
                    f"Check path: {storage_path}",
                    "Ensure sufficient disk space available",
                    "Check file permissions on storage directory"
                ]

            elif component == "tagging":
                component_hints = [
                    "Verify TagGenerator initialized correctly",
                    "Check if ML models are downloaded",
                    "Review memory requirements (T5 models need ~2GB RAM)",
                    "Consider using heuristic mode if resources limited"
                ]

            hints[component] = component_hints

    return hints
```

---

## Task 5: Add API Examples to Error Responses

**File**: `src/sono_eval/utils/errors.py`

### Add common usage examples

#### 5.1: Create Examples Helper

**Add at the end of the file**:

```python
class APIExamples:
    """Common API usage examples for error responses."""

    @staticmethod
    def assessment_creation() -> str:
        """Example of creating an assessment."""
        return """
# Create assessment via curl:
curl -X POST http://localhost:8000/api/v1/assessments \\
  -H "Content-Type: application/json" \\
  -d '{
    "candidate_id": "john_doe",
    "submission_type": "code",
    "content": {"code": "def hello(): return \"world\""},
    "paths_to_evaluate": ["TECHNICAL"]
  }'

# Python example:
import requests
response = requests.post(
    "http://localhost:8000/api/v1/assessments",
    json={
        "candidate_id": "john_doe",
        "submission_type": "code",
        "content": {"code": "def hello(): return 'world'"},
        "paths_to_evaluate": ["TECHNICAL"]
    }
)
result = response.json()
"""

    @staticmethod
    def candidate_creation() -> str:
        """Example of creating a candidate."""
        return """
# Create candidate via curl:
curl -X POST http://localhost:8000/api/v1/candidates \\
  -H "Content-Type: application/json" \\
  -d '{
    "candidate_id": "john_doe",
    "initial_data": {"name": "John Doe"}
  }'
"""

    @staticmethod
    def assessment_retrieval() -> str:
        """Example of retrieving an assessment."""
        return """
# Get assessment by ID:
curl http://localhost:8000/api/v1/assessments/{assessment_id}

# List all assessments for a candidate:
curl http://localhost:8000/api/v1/candidates/{candidate_id}/assessments
"""

    @staticmethod
    def tag_generation() -> str:
        """Example of generating tags."""
        return """
# Generate semantic tags:
curl -X POST http://localhost:8000/api/v1/tags/generate \\
  -H "Content-Type: application/json" \\
  -d '{
    "text": "async function fetchData() { return await api.get() }",
    "max_tags": 5
  }'
"""


def add_example_to_help(help_context: Dict[str, Any], example_type: str) -> Dict[str, Any]:
    """Add usage example to help context."""
    examples = {
        "assessment": APIExamples.assessment_creation(),
        "candidate": APIExamples.candidate_creation(),
        "retrieval": APIExamples.assessment_retrieval(),
        "tags": APIExamples.tag_generation()
    }

    if example_type in examples:
        help_context["example"] = examples[example_type]

    return help_context
```

#### 5.2: Use Examples in Errors

**Update not_found_error** to include examples:

```python
def not_found_error(
    resource_type: str,
    resource_id: Optional[str] = None,
    search_endpoint: Optional[str] = None,
    create_endpoint: Optional[str] = None,
    include_example: bool = True,  # NEW parameter
    request_id: Optional[str] = None,
) -> HTTPException:
    """Create a not found error response with next steps and examples."""
    message = f"{resource_type} not found"
    if resource_id:
        message += f": {resource_id}"

    help_context = HelpContext.for_not_found(
        resource_type=resource_type.lower(),
        search_endpoint=search_endpoint,
        create_endpoint=create_endpoint
    )

    # Add relevant example
    if include_example:
        if "assessment" in resource_type.lower():
            help_context = add_example_to_help(help_context, "assessment")
        elif "candidate" in resource_type.lower():
            help_context = add_example_to_help(help_context, "candidate")

    return create_error_response(
        error_code=ErrorCode.NOT_FOUND,
        message=message,
        status_code=status.HTTP_404_NOT_FOUND,
        details={
            "resource_type": resource_type,
            "resource_id": resource_id
        },
        help_context=help_context,
        request_id=request_id,
    )
=======
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
>>>>>>> 6b7113d6352e4fb7d7504d7a7d221ee1ac543c33:Documentation/Reports/IMPLEMENTATION_PLAN_2_API_ERRORS.md
```

---

## Task C — Add component troubleshooting hints to health checks

### Before (current)
- `src/sono_eval/api/main.py` lines 230–534 return component status/details without troubleshooting hints.

### After (target)
- Add `troubleshooting` hints per component in the detailed health check response.

#### Add hints (copy-paste)
**File**: `src/sono_eval/api/main.py`  
**Within** `check_component_health`, extend `details` to include `troubleshooting` hints, e.g.:

```python
<<<<<<< HEAD:Documentation/Archive/Reports-Historical/IMPLEMENTATION_PLAN_2_API_ERRORS.md
"""
Interactive error documentation for Sono-Eval API.

Provides browsable error code reference and troubleshooting guide.
"""

from typing import Dict, List, Any
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/errors", tags=["Documentation"])


class ErrorDocumentation(BaseModel):
    """Documentation for a specific error code."""

    code: str
    name: str
    http_status: int
    description: str
    common_causes: List[str]
    solutions: List[str]
    example_request: str
    example_response: Dict[str, Any]


ERROR_DOCS = {
    "VALIDATION_ERROR": ErrorDocumentation(
        code="VALIDATION_ERROR",
        name="Validation Error",
        http_status=400,
        description="Request data failed validation checks",
        common_causes=[
            "Invalid candidate_id format (must be alphanumeric, dash, or underscore)",
            "Missing required fields",
            "Field values outside allowed range",
            "Invalid enum values"
        ],
        solutions=[
            "Check field formats match requirements",
            "Ensure all required fields are provided",
            "Review API documentation for field constraints",
            "Use provided examples as templates"
        ],
        example_request="""
POST /api/v1/assessments
{
  "candidate_id": "john@doe",  // INVALID: contains @
  "submission_type": "code",
  "content": {"code": "..."},
  "paths_to_evaluate": ["TECHNICAL"]
}
""",
        example_response={
            "error": True,
            "error_code": "VALIDATION_ERROR",
            "message": "candidate_id must contain only alphanumeric characters, dashes, and underscores",
            "details": {
                "field": "candidate_id",
                "received": "john@doe",
                "pattern": "^[a-zA-Z0-9_-]+$"
            },
            "help": {
                "suggestion": "Replace special characters with dashes or underscores",
                "valid_examples": ["john_doe", "candidate-001", "user123"]
            }
        }
    ),

    "NOT_FOUND": ErrorDocumentation(
        code="NOT_FOUND",
        name="Resource Not Found",
        http_status=404,
        description="The requested resource does not exist",
        common_causes=[
            "Incorrect resource ID",
            "Resource was deleted",
            "Resource not yet created",
            "Typo in endpoint URL"
        ],
        solutions=[
            "Verify the resource ID is correct",
            "List available resources using GET endpoint",
            "Create the resource if it doesn't exist",
            "Check API documentation for correct endpoint"
        ],
        example_request="GET /api/v1/assessments/nonexistent-id",
        example_response={
            "error": True,
            "error_code": "NOT_FOUND",
            "message": "Assessment not found: nonexistent-id",
            "details": {
                "resource_type": "Assessment",
                "resource_id": "nonexistent-id"
            },
            "help": {
                "suggestion": "Verify the assessment exists or create a new one",
                "search_url": "/api/v1/assessments",
                "create_url": "/api/v1/assessments"
            }
        }
    ),

    # Add more error documentation...
}


@router.get("/", response_model=List[str])
async def list_error_codes():
    """List all documented error codes."""
    return list(ERROR_DOCS.keys())


@router.get("/{error_code}", response_model=ErrorDocumentation)
async def get_error_documentation(error_code: str):
    """Get detailed documentation for a specific error code."""
    if error_code not in ERROR_DOCS:
        return {
            "error": True,
            "message": f"No documentation found for error code: {error_code}",
            "available_codes": list(ERROR_DOCS.keys())
        }

    return ERROR_DOCS[error_code]


@router.get("/search/{keyword}")
async def search_errors(keyword: str):
    """Search error documentation by keyword."""
    results = []
    keyword_lower = keyword.lower()

    for code, doc in ERROR_DOCS.items():
        if (keyword_lower in doc.name.lower() or
            keyword_lower in doc.description.lower() or
            any(keyword_lower in cause.lower() for cause in doc.common_causes)):
            results.append({
                "code": code,
                "name": doc.name,
                "description": doc.description
            })

    return results
=======
if include_details:
    details["assessment"]["troubleshooting"] = "Restart the server to reinitialize the assessment engine."
>>>>>>> 6b7113d6352e4fb7d7504d7a7d221ee1ac543c33:Documentation/Reports/IMPLEMENTATION_PLAN_2_API_ERRORS.md
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

<<<<<<< HEAD:Documentation/Archive/Reports-Historical/IMPLEMENTATION_PLAN_2_API_ERRORS.md
### 1. Test Enhanced Error Responses

```bash
# Start the server
./launcher.sh start

# Test validation error
curl -X POST http://localhost:8000/api/v1/assessments \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": "john@doe.com",
    "submission_type": "code",
    "content": {"code": "def test(): pass"},
    "paths_to_evaluate": ["TECHNICAL"]
  }' | jq

# Expected: Error with help.valid_examples and help.suggestion

# Test not found error
curl http://localhost:8000/api/v1/assessments/nonexistent | jq

# Expected: Error with help.search_url and help.create_url

# Test error documentation
curl http://localhost:8000/api/v1/errors/ | jq
curl http://localhost:8000/api/v1/errors/VALIDATION_ERROR | jq
```

### 2. Test Health Check Enhancement

```bash
# Basic health check
curl http://localhost:8000/api/v1/health | jq

# Detailed health check with troubleshooting
curl http://localhost:8000/api/v1/health?detailed=true | jq

# Expected: troubleshooting hints if any component is degraded
```

### 3. Verify OpenAPI Documentation

```bash
# Open browser to Swagger docs
open http://localhost:8000/docs

# Check that:
# - Error response models show new help field
# - Examples are visible in schema
# - Error documentation endpoint is listed
```

### 4. Integration Tests

Create test file `tests/test_enhanced_errors.py`:

```python
"""Tests for enhanced error responses."""

import pytest
from fastapi.testclient import TestClient
from src.sono_eval.api.main import app

client = TestClient(app)


def test_validation_error_includes_help():
    """Test that validation errors include help context."""
    response = client.post(
        "/api/v1/assessments",
        json={
            "candidate_id": "john@doe",  # Invalid format
            "submission_type": "code",
            "content": {"code": "def test(): pass"},
            "paths_to_evaluate": ["TECHNICAL"]
        }
    )

    assert response.status_code == 400
    error = response.json()

    # Verify error structure
    assert error["error"] is True
    assert error["error_code"] == "VALIDATION_ERROR"
    assert "help" in error

    # Verify help context
    help_ctx = error["help"]
    assert "valid_examples" in help_ctx
    assert "suggestion" in help_ctx
    assert len(help_ctx["valid_examples"]) > 0


def test_not_found_includes_next_steps():
    """Test that not found errors include next steps."""
    response = client.get("/api/v1/assessments/nonexistent-id")

    assert response.status_code == 404
    error = response.json()

    assert "help" in error
    help_ctx = error["help"]
    assert "suggestion" in help_ctx
    assert "search_url" in help_ctx or "create_url" in help_ctx


def test_error_documentation_endpoint():
    """Test error documentation endpoint."""
    # List error codes
    response = client.get("/api/v1/errors/")
    assert response.status_code == 200
    codes = response.json()
    assert isinstance(codes, list)
    assert "VALIDATION_ERROR" in codes

    # Get specific error docs
    response = client.get("/api/v1/errors/VALIDATION_ERROR")
    assert response.status_code == 200
    doc = response.json()
    assert doc["code"] == "VALIDATION_ERROR"
    assert "common_causes" in doc
    assert "solutions" in doc


def test_health_check_troubleshooting():
    """Test that detailed health check includes troubleshooting."""
    response = client.get("/api/v1/health?detailed=true")
    assert response.status_code == 200
    health = response.json()

    # If any component is unhealthy, should have troubleshooting
    if health["status"] != "healthy":
        assert "troubleshooting" in health
```

Run tests:

```bash
pytest tests/test_enhanced_errors.py -v
```
=======
1. Run the API: `./launcher.sh start`.
2. Trigger a validation error (e.g., invalid `candidate_id`) and confirm the response includes `help`.
3. Hit `/api/v1/health` and verify troubleshooting hints are present in `details`.
4. Hit `/api/v1/errors` and confirm it returns the error reference list.
>>>>>>> 6b7113d6352e4fb7d7504d7a7d221ee1ac543c33:Documentation/Reports/IMPLEMENTATION_PLAN_2_API_ERRORS.md

---

## Success Criteria

- ✅ Error responses include `help` with examples, suggestions, and docs URLs.
- ✅ Health check details include troubleshooting hints per component.
- ✅ `/api/v1/errors` returns a readable JSON index of error codes.

---

## Rollback Procedure

<<<<<<< HEAD:Documentation/Archive/Reports-Historical/IMPLEMENTATION_PLAN_2_API_ERRORS.md
### Before

```json
{
  "error": true,
  "error_code": "VALIDATION_ERROR",
  "message": "candidate_id must contain only alphanumeric characters, dashes, and underscores"
}
```

### After

```json
{
  "error": true,
  "error_code": "VALIDATION_ERROR",
  "message": "candidate_id must contain only alphanumeric characters, dashes, and underscores",
  "details": {
    "field": "candidate_id",
    "received": "john@doe",
    "pattern": "^[a-zA-Z0-9_-]+$"
  },
  "help": {
    "suggestion": "Replace special characters with dashes or underscores",
    "valid_examples": ["john_doe", "candidate-001", "user123"],
    "docs_url": "/docs#field-candidate-id"
  },
  "request_id": "abc-123"
}
```

**Improvements:**

- Clear next steps (suggestion)
- Concrete examples (valid_examples)
- Technical details (pattern, received value)
- Documentation link (docs_url)
- Tracking support (request_id)

---

## Rollback Plan

```bash
# Create backup branch
git checkout -b api-error-enhancement

# Commit incrementally
git add src/sono_eval/utils/errors.py
git commit -m "Task 1: Enhance error response model"

# Rollback if needed
git checkout HEAD~1 -- src/sono_eval/utils/errors.py
```

---

**Document Version**: 1.0  
**Last Updated**: January 17, 2026  
**Estimated Implementation Time**: 2-3 hours  
**Difficulty**: Low-Medium
=======
1. Revert `errors.py` model and remove `ErrorHelp` / `help` field.
2. Remove any error help references in API handlers.
3. Remove `/api/v1/errors` endpoint and any troubleshooting hints.
>>>>>>> 6b7113d6352e4fb7d7504d7a7d221ee1ac543c33:Documentation/Reports/IMPLEMENTATION_PLAN_2_API_ERRORS.md
