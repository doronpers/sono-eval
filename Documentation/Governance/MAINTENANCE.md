# Documentation Maintenance Notes

## Version and Date Updates

Several documentation files contain hardcoded version numbers and dates:

- Version: 0.1.1
- Last Updated: January 18, 2026

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

Consider implementing a script or CI/CD step to automatically update these
values across all files when releasing a new version. Example approaches:

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
find . -name "*.md" -exec sed -i \
  's/support@sono-eval\.example/actual@email.com/g' {} \;
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

## Link Conventions

To prevent broken links, follow these conventions when linking between documentation files:

### Linking to Root Files

From `documentation/Guides/*` or `documentation/Reports/*`:

- Use `../../SECURITY.md` for root-level files (SECURITY.md, CHANGELOG.md, etc.)
- Use `../../README.md` for root README
- Use `../../CONTRIBUTING.md` for root CONTRIBUTING

### Linking Within Documentation

From `documentation/Guides/*`:

- To other Guides: `../QUICK_START.md` (same level)
- To Reports: `../Reports/ASSESSMENT_SUMMARY.md`
- To Governance: `../Governance/IMPLEMENTATION_GUIDE.md`
- To Core: `../Core/concepts/architecture.md`

From `documentation/Reports/*`:

- To other Reports: `ASSESSMENT_SUMMARY.md` (same directory)
- To Guides: `../Guides/QUICK_REFERENCE.md`
- To Governance: `../Governance/IMPLEMENTATION_GUIDE.md`
- To root files: `../../SECURITY.md`

### File Name Case Sensitivity

- Use exact case: `QUICK_START.md` not `quick-start.md`
- Check actual filename before linking

### Common Broken Link Patterns to Avoid

❌ **BAD**: `[SECURITY.md](SECURITY.md)` from `documentation/Guides/` (assumes same directory)
✅ **GOOD**: `[SECURITY.md](../../SECURITY.md)` from `documentation/Guides/`

❌ **BAD**: `[quick-start.md](../quick-start.md)` (wrong case)
✅ **GOOD**: `[QUICK_START.md](../QUICK_START.md)` (matches actual filename)

---

**Maintainer**: Update this file when adding new documentation or changing
maintenance procedures.
