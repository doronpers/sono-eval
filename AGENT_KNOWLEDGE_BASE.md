# Global Agent Knowledge Base & Instructional Set

This document is the **Single Source of Truth** for all AI agents (Claude, Cursor, etc.) working on Sonotheia and related repositories. You MUST refer to this before and during your tasks.

---

## 0. Prime Directives (NON-NEGOTIABLE)

1. **Patent Compliance**:
    * **NEVER** use Linear Predictive Coding (LPC), source-filter models, glottal closure/opening detection, or static formant values. These are patent-protected.
    * **ALWAYS** use dynamic trajectories, phase analysis, and velocity-based methods (e.g., GlottalInertia, PhaseCoherence).
    * See `documentation/PATENT_COMPLIANCE.md` if available.

2. **Security & Privacy**:
    * **NEVER** log raw audio bytes, PII (Personal Identifiable Information), or secrets (API keys).
    * **ALWAYS** use `get_error_response` for errors to avoid leaking internal stack traces to clients (log them instead).

3. **Design Philosophy (The Advisory Council)**:
    * **Dieter Rams**: "Less but Better". Remove clutter. Unify styles.
    * **Martin Dempsey**: "Make it matter". Focus on mission command and decentralized execution.
    * **Daniel Kahneman**: Reduce cognitive load. "System 1 vs System 2".
    * **Julian Treasure**: Conscious listening. Authentic sound.
    * **CONSTRAINT**: Use these "lenses" to audit and improve, but **DO NOT** brand features with these names (e.g., no "Rams Protocol"). Use descriptive functional names.

4. **Accuracy & Consistency**:
    * Prioritize increasing detection accuracy. Verify changes do not degrade performance.

---

## 1. Operational Guardrails

* **Configuration**: `backend/config/settings.yaml` (or equivalent) is the **SINGLE** source of truth for sensor weights, thresholds, and fusion config. **DO NOT** hardcode weights.
* **Audio Format**: All sensors expect **float32 mono numpy arrays at 16kHz**. Use `backend/sensors/utils.py` for loading/preprocessing.
* **Demo Mode**: **DO NOT** disable `DEMO_MODE` or convert demo features to production without explicit tests, configuration updates, and approval.
* **Dependencies**: **DO NOT** upgrade critical frontend deps (`react`, `react-dom`, `@mui/*`) beyond specified versions (React 18, MUI 5) to maintain build compatibility.

---

## 2. Coding Standards

* **Python**:
  * Formatter: `black`
  * Linter: `flake8`
  * Style: `snake_case` for functions/vars, `PascalCase` for classes.
  * Validation: Use **Pydantic** models for all data structures.
* **Frontend**:
  * Framework: React 18 + Material-UI (MUI).
  * Style: Functional components with hooks. `camelCase` for vars, `PascalCase` for components.
* **Testing**:
  * Backend: `pytest`. Run `pytest` before committing.
  * Frontend: `npm test` (Vitest/Jest).
* **Error Handling**:
  * Sensors must **NEVER** raise exceptions during `analyze()`. Return `SensorResult(passed=None, detail="...")`.

---

## 3. Sensor Development Workflow

When adding or modifying a sensor:

1. **Extend BaseSensor**: Inherit from `BaseSensor`.
2. **Define Category**:
    * `"prosecution"`: Detects FAKE (high score = suspicious).
    * `"defense"`: Detects REAL (high score = authentic).
    * **MUST** include `metadata={"category": self.category}` in `SensorResult`.
3. **Register**: Add to `backend/sensors/registry.py`.
4. **Configure**: Add weights/thresholds to `settings.yaml`.
5. **Test**: Add unit tests in `tests/`.

---

## 4. Common Patterns

**FastAPI Endpoint:**

```python
@router.post("/process")
@limiter.limit("20/minute")
async def process(request: Request, body: MyModel, api_key: str = Depends(verify_api_key)):
    # Validate and process
```

**Logging:**

* `logger.info`: High-level flow.
* `logger.error`: Exceptions (use `exc_info=True`).
* `logger.debug`: Detailed steps (NOT in production).

---

## 5. Quick Reference (Core Platform Map)

*(Note: File paths below refer to the primary `sono-platform` repository. Other repositories may follow `src/` and `tests/` structures.)*

* `backend/api/main.py`: Entry point.
* `backend/config/settings.yaml`: Configuration.
* `backend/sensors/`: Sensor implementations.
* `frontend/src/App.js`: Frontend entry.

---

## Documentation Standards

Follow [Documentation Organization Standards](documentation/Governance/DOCUMENTATION_ORGANIZATION_STANDARDS.md)

---

## Sono-Eval Specific Guidelines

### Project State: Beta (0.1.1)

**Core Philosophy**: Precision-first, evidence-based assessment. We value the "show, don't tell" approach in developer submissions.

### System Limits (Honesty Statement)

* **ML Integration**: Current "Hybrid" mode is primarily heuristic-driven. ML insights (T5/LoRA) are secondary and require high-compute environments (GPU) to be performant. The heuristic-first approach is currently the most reliable.
* **Concurrency**: `MemUStorage` is currently filesystem-based. While thread-safe for reads, concurrent writes to the same candidate profile may result in data race conditions. Use Redis for high-concurrency needs.
* **Assessment Retrieval**: The `GET /api/v1/assessments/{id}` endpoint retrieves assessments from hierarchical memory storage (repaired in v0.1.1).
* **Dark Horse Mode**: The ML-based "Dark Horse" tracking and T5 tagging are primarily heuristic fallbacks. The documentation accurately reflects current capabilities.

### Security Requirements

* `SECRET_KEY` must be a 32-byte secure token (validated at startup).
* Candidate IDs are strictly sanitized (alphanumeric/dash/underscore only).
* File uploads enforce path traversal protection and content-type verification.
* `DATABASE_URL` validation prevents default SQLite paths in production.

### Recommended Configuration

* Maintain `DARK_HORSE_MODE` as "enabled" to track micro-motives (Mastery vs. Efficiency), which reveal more about character than raw scores.
* The **Heuristic-First** approach is currently the most reliable for production use.

### Code Quality Analysis

The `_analyze_code_quality` method prioritizes "Density of Logic" over "Substantial Code" to align with minimalism and subtext preference. It evaluates:

* Logic density (meaningful code vs. whitespace/comments)
* Abstraction ratio (functions/classes relative to code size)
* Structure and error handling
* Testing awareness

### Dependencies

* **Removed**: `shared_ai_utils` dependency (replaced with local implementations)
* **Timezone Handling**: All datetime operations use `datetime.now(timezone.utc)` instead of deprecated `datetime.utcnow()`
* **Cache Management**: `MemUStorage` uses LRU-based eviction to prevent memory bloat
