# Testing Guide

This document describes the testing strategy and coverage for Sono-Eval.

## Test Suite Overview

### Test Files

1. **test_assessment.py** - Assessment engine tests (6 tests)
   - Engine initialization
   - Basic assessment flow
   - Multi-path assessment
   - Evidence generation
   - Micro-motive tracking
   - Explanation generation

2. **test_validation.py** - Input validation tests (11 tests)
   - Valid/invalid candidate IDs
   - Candidate ID length limits
   - Valid/invalid submission types
   - Content validation (empty, size limits)
   - Field length constraints

3. **test_api.py** - API endpoint tests (14 tests)
   - Health check endpoint
   - Request ID tracking and propagation
   - CORS headers
   - Assessment endpoint validation
   - Tag generation endpoint
   - Candidate creation endpoint
   - Error handling for invalid inputs

4. **test_security.py** - Security configuration tests (7 tests)
   - Secret validation in development/production
   - CORS configuration validation
   - Production config validation
   - Configuration field constraints

5. **test_logging.py** - Structured logging tests (10 tests)
   - Logger creation
   - Structured JSON formatting
   - Request ID inclusion
   - Duration tracking
   - User ID tracking
   - Exception formatting
   - Production vs development logging
   - ISO 8601 timestamp format

6. **test_config.py** - Configuration tests (6 tests)
   - Default configuration
   - Environment variable loading
   - Storage path management
   - Singleton pattern

7. **test_memory.py** - Memory storage tests
   - MemU storage functionality

8. **test_tagging.py** - Tag generation tests
   - Tag generation functionality

9. **test_smoke.py** - Basic smoke tests (6 tests)
   - File existence checks
   - Module structure validation

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_validation.py
```

### Run with Coverage
```bash
pytest --cov=src/sono_eval --cov-report=html --cov-report=term
```

### Run Tests by Category
```bash
# Run only validation tests
pytest tests/test_validation.py

# Run only API tests
pytest tests/test_api.py

# Run only security tests
pytest tests/test_security.py
```

## Coverage Goals

### Current Coverage
- **Baseline**: ~40% (original tests)
- **Target**: 80%+
- **New Coverage**: ~65-70% (with new tests)

### Coverage by Module

| Module | Coverage Target | Status |
|--------|----------------|--------|
| assessment/models.py | 90% | ✅ Improved |
| api/main.py | 80% | ✅ Improved |
| utils/logger.py | 85% | ✅ Improved |
| utils/config.py | 75% | ✅ Existing |
| assessment/engine.py | 70% | ✅ Existing |
| memory/memu.py | 60% | ⚠️ Basic |
| tagging/generator.py | 60% | ⚠️ Basic |

## Test Categories

### Unit Tests
- Individual function/method testing
- Mock external dependencies
- Fast execution
- Examples: test_validation.py, test_logging.py

### Integration Tests
- API endpoint testing
- Service interaction
- Database operations
- Examples: test_api.py, test_assessment.py

### Security Tests
- Input validation
- Configuration validation
- Secret management
- Examples: test_security.py, test_validation.py

### Smoke Tests
- Basic functionality checks
- File existence
- Import validation
- Examples: test_smoke.py

## Testing Best Practices

### 1. Test Naming
- Use descriptive names: `test_valid_candidate_id_accepts_alphanumeric`
- Follow pattern: `test_<what>_<condition>_<expected_result>`

### 2. Test Structure
- **Arrange**: Set up test data
- **Act**: Execute the code under test
- **Assert**: Verify the results

### 3. Assertions
- Use specific assertions
- Include helpful error messages
- Test both positive and negative cases

### 4. Mocking
- Mock external dependencies
- Use `unittest.mock` or `pytest-mock`
- Don't mock the code under test

### 5. Fixtures
- Use pytest fixtures for shared setup
- Keep fixtures simple and focused
- Name fixtures clearly

## CI/CD Integration

Tests are automatically run by GitHub Actions:
- On every push to main/develop
- On every pull request
- Multiple Python versions (3.9, 3.10, 3.11)
- Coverage reports uploaded to Codecov

## Test Data

### Valid Test Data Examples
```python
# Valid candidate IDs
valid_ids = ["test123", "test_candidate", "test-candidate"]

# Valid submission types
valid_types = ["code", "project", "interview", "portfolio", "test"]

# Valid content
valid_content = {"code": "print('hello')"}
```

### Invalid Test Data Examples
```python
# Invalid candidate IDs (should be rejected)
invalid_ids = ["test@invalid", "test candidate", "test#123"]

# Invalid submission types
invalid_types = ["invalid_type", "unknown"]

# Invalid content
invalid_content = {}  # Empty
```

## Coverage Reports

After running tests with coverage, view the HTML report:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## Adding New Tests

When adding new features:
1. Write tests first (TDD approach)
2. Ensure at least 80% coverage
3. Include both positive and negative test cases
4. Add edge case tests
5. Update this documentation

## Known Limitations

1. **ML Model Testing**: Placeholder logic means some tests use mock data
2. **Database Tests**: Some tests require database setup (handled by CI)
3. **Integration Tests**: Full integration tests require all services running

## Future Test Improvements

- [ ] Add performance/load tests
- [ ] Add end-to-end tests
- [ ] Add contract tests for API
- [ ] Add mutation testing
- [ ] Add property-based testing (Hypothesis)
- [ ] Increase integration test coverage
- [ ] Add API security penetration tests

## Test Environment Variables

For local testing, set these environment variables:
```bash
export APP_ENV=development
export DATABASE_URL=sqlite:///test.db
export SECRET_KEY=test-secret-key
export DEBUG=true
```

## Troubleshooting Tests

### Common Issues

1. **Import Errors**: Ensure package is installed (`pip install -e .`)
2. **Missing Dependencies**: Install test dependencies (`pip install -e ".[dev]"`)
3. **Database Errors**: Use test database or SQLite in-memory
4. **Async Test Errors**: Use `@pytest.mark.asyncio` decorator

### Debug Mode

Run tests with verbose output:
```bash
pytest -vv -s
```

Show print statements:
```bash
pytest -s
```

Stop on first failure:
```bash
pytest -x
```

## Test Metrics

### Current Test Suite
- **Total Tests**: 60+ tests
- **Test Files**: 9 files
- **Average Test Time**: < 5 seconds
- **Code Coverage**: ~65-70% (target: 80%)

### Quality Metrics
- All tests pass ✅
- No flaky tests ✅
- Clear test names ✅
- Good documentation ✅
- Proper mocking ✅

## Contributing Tests

When contributing tests:
1. Follow existing test patterns
2. Add docstrings to test functions
3. Use descriptive assertions
4. Keep tests focused and simple
5. Run full test suite before committing
6. Update this documentation

---

**Last Updated**: 2026-01-11  
**Maintained by**: Sono-Eval Team
