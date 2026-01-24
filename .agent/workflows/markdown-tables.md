---
description: Markdown table formatting rules
---

# Markdown Table Formatting

When creating or editing markdown tables, **ALWAYS** follow these formatting rules to prevent markdownlint errors:

## Rule: Proper Pipe Spacing

**CRITICAL**: Table separator rows MUST have spaces around pipes to comply with markdownlint MD060.

### ❌ INCORRECT (will fail linting)

```markdown
| Header 1 | Header 2 | Header 3 |
|---|---|---|
| Data 1 | Data 2 | Data 3 |
```

### ✅ CORRECT

```markdown
| Header 1 | Header 2 | Header 3 |
| --- | --- | --- |
| Data 1 | Data 2 | Data 3 |
```

## Key Points

1. **Separator row**: Use `| --- | --- | --- |` with spaces around each pipe
2. **Data rows**: While not strictly required, maintaining consistent spacing improves readability
3. **Pre-commit hooks**: Markdownlint will block commits with improperly formatted tables

## Quick Fix

If you encounter MD060 errors:

1. Locate the separator row (usually the second row)
2. Add spaces: `|---|` → `| --- |`
3. Apply to all columns in the separator row

## Examples

### Simple table

```markdown
| Name | Age | Role |
| --- | --- | --- |
| Alice | 30 | Developer |
| Bob | 25 | Designer |
```

### Table with alignment

```markdown
| Left | Center | Right |
| :--- | :---: | ---: |
| A | B | C |
```

**Note**: Even with alignment markers (`:---`, `:---:`, `---:`), maintain spaces around pipes.

## Verification

Before committing, verify your markdown tables:

```bash
# Run markdownlint on changed files
markdownlint **/*.md
```
