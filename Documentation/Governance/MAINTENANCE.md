# Documentation Maintenance Notes

## Version and Date Updates

Several documentation files contain hardcoded version numbers and dates:

- Version: 0.1.0
- Last Updated: January 10, 2026

### Files to Update on Version Changes

- README.md
- documentation/README.md
- documentation/Guides/QUICK_START.md
- documentation/Guides/user-guide/*.md
- documentation/Guides/resources/*.md
- documentation/Core/concepts/*.md
- documentation/Guides/troubleshooting.md
- documentation/Guides/faq.md
- CHANGELOG.md

### Automation Recommendation

Consider implementing a script or CI/CD step to automatically update these values across all files when releasing a new version. Example approaches:

1. Use templating (Jinja2, mustache)
2. Pre-release script with find/replace
3. CI/CD action on tag creation

### Manual Update Process

```bash
# Find all occurrences
grep -r "0.1.0" documentation/
grep -r "January 10, 2026" documentation/

# Update with new version/date
find documentation -name "*.md" -exec sed -i 's/0.1.0/NEW_VERSION/g' {} \;
find documentation -name "*.md" -exec sed -i 's/January 10, 2026/NEW_DATE/g' {} \;
```

## Email Addresses

Current placeholder: `support@sono-eval.example`

**Action Required**: Update to actual support email before production deployment:

```bash
find . -name "*.md" -exec sed -i 's/support@sono-eval\.example/actual@email.com/g' {} \;
```

## Pre-commit Hooks

MyPy type checking is disabled by default due to:

- Slow performance (adds ~30s to commit time)
- Requires additional stub packages
- Type errors in dependencies

To enable locally:

```bash
# Edit .pre-commit-config.yaml and uncomment mypy section
# Or run manually:
pre-commit run mypy --all-files
```

---

**Maintainer**: Update this file when adding new documentation or changing maintenance procedures.
