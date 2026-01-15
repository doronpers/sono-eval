# Pull Request

## Description

<!-- Provide a brief description of the changes in this PR -->

## Type of Change

<!-- Mark the relevant option with an 'x' -->

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality
  to not work as expected)
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement
- [ ] Security fix
- [ ] Test addition/improvement
- [ ] Build/CI improvement

## Related Issues

<!-- Link to related issues using #issue_number -->

Fixes #
Relates to #

## Changes Made

<!-- List the main changes made in this PR -->

-
-
-

## Testing

<!-- Describe the tests you ran and how to reproduce them -->

- [ ] Unit tests pass locally
- [ ] Integration tests pass locally
- [ ] Manual testing completed
- [ ] Security scan passed (if applicable)

**Test Configuration**:

- Python version:
- OS:
- Docker version (if applicable):

**Test commands run**:

```bash
# Add commands here
pytest
```

## Security Considerations

<!-- Address any security implications of this change -->

- [ ] No new security vulnerabilities introduced
- [ ] Security scan completed (bandit, safety)
- [ ] Sensitive data properly handled
- [ ] Input validation added where needed
- [ ] Authentication/authorization considered

## Documentation

<!-- Check all that apply -->

- [ ] Code is self-documenting with clear variable names
- [ ] Docstrings added/updated for new functions/classes
- [ ] README.md updated (if needed)
- [ ] API documentation updated (if needed)
- [ ] CHANGELOG.md updated
- [ ] Comments added for complex logic

## Breaking Changes

<!-- If this introduces breaking changes, describe them and the migration path -->

- [ ] This PR introduces breaking changes
- [ ] Migration guide added/updated
- [ ] Deprecation warnings added (if applicable)

**Breaking changes details**:

## Screenshots (if applicable)

<!-- Add screenshots for UI changes -->

## Checklist

<!-- Ensure all items are checked before requesting review -->

- [ ] My code follows the style guidelines of this project (Black, line length 100)
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Linting passes (`flake8`)
- [ ] No secrets or credentials are included in this change
- [ ] Any dependent changes have been merged and published

## Developer tips

- Install pre-commit hooks: `pre-commit install` (see `CONTRIBUTING.md` and
  `./scripts/fix-pre-commit-ssl.sh` if you encounter SSL issues).
- Use Pydantic v2 helpers: prefer `model_dump()` / `model_validate()` in tests
  and serialization checks.
- When changing APIs, update OpenAPI docs and add explicit tests for schema compatibility.

## Additional Notes

<!-- Add any additional context or notes for reviewers -->

## Reviewer Notes

<!-- For reviewers: Add your review comments and approval here -->

---

**By submitting this pull request, I confirm that my contribution is made
under the terms of the MIT License.**
