# Sample Code Submissions

This directory contains example code submissions for testing the Sono-Eval assessment system.

## Files

### `simple-function.py`
**Complexity**: Beginner
**Assessment Paths**: TECHNICAL
**Description**: A simple recursive Fibonacci implementation. Good for testing basic code evaluation.

**Try it**:
```bash
sono-eval assess run \
  --candidate-id test_user \
  --file samples/simple-function.py \
  --paths technical
```

### `complex-class.py`
**Complexity**: Intermediate
**Assessment Paths**: TECHNICAL, DESIGN, COLLABORATION
**Description**: Object-oriented task management system with proper documentation, error handling, and type hints.

**Try it**:
```bash
sono-eval assess run \
  --candidate-id test_user \
  --file samples/complex-class.py \
  --paths technical design collaboration
```

### `with-tests.py`
**Complexity**: Intermediate
**Assessment Paths**: ALL
**Description**: Statistical functions with comprehensive tests included. Demonstrates testing awareness and documentation.

**Try it**:
```bash
sono-eval assess run \
  --candidate-id test_user \
  --file samples/with-tests.py \
  --paths technical design collaboration
```

## Using Samples in API

You can also test these via the REST API at `/docs`:

1. Start the server: `./launcher.sh start` or `sono-eval server start`
2. Navigate to `http://localhost:8000/docs`
3. Use the `POST /api/v1/assessments` endpoint
4. Example request body:

```json
{
  "candidate_id": "demo_user",
  "submission_type": "code",
  "content": {
    "code": "< paste contents of any sample file >"
  },
  "paths_to_evaluate": ["TECHNICAL"]
}
```

## Creating Your Own Samples

Want to add your own sample? Great! Follow these guidelines:

1. **Add meaningful docstrings** - Explain what the code does
2. **Include variety** - Different complexity levels help test different assessment paths
3. **Show best practices** - Error handling, type hints, testing awareness
4. **Keep it focused** - Each sample should demonstrate specific aspects
5. **Update this README** - Add a description of your sample

Submit your sample via a pull request!
