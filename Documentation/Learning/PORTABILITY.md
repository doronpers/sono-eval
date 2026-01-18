# Portability Guide

This directory is designed to be easily reused in other repositories.

## Quick Copy Commands

### Copy Everything

```bash
cp -r sono-eval/documentation/Learning your-repo/documentation/learning-resources
```

### Copy Specific Sections

```bash
# Just philosophy
cp -r sono-eval/documentation/Learning/Philosophy your-repo/documentation/learning/

# Just templates
cp sono-eval/documentation/Learning/Templates/*.md your-repo/templates/

# Just beginner guides
cp -r sono-eval/documentation/Learning/Guides/github-basics your-repo/documentation/guides/
```

## Link Updates Required

When copying to another repo, update:

1. **Relative paths in markdown files**
   - Old: `../documentation/01-github-basics/`
   - New: `Guides/github-basics/` (or appropriate relative path)
   - Old: `../exercises/discover-your-micro-motives.md`
   - New: `../Exercises/discover-your-micro-motives.md`

2. **References to "tex-assist-coding"**
   - Search and replace with your repo name or remove if not relevant

3. **Repo-specific examples**
   - Update any code examples or references to match your repo's context

## Integration Examples

### In README.md

```markdown
## Learning Resources

See [Learning Resources](documentation/learning-resources/) for:
- Beginner-friendly guides
- Learning path templates
- Micro-motives discovery exercises
```

### In Documentation

```markdown
For learning philosophy, see [Dark Horse Approach](learning-resources/Philosophy/dark-horse-approach.md)
```

### In Contributing Guide

```markdown
## For Beginners

If you're new to coding or this project, check out:
- [Complete Beginner Path](documentation/learning-resources/Paths/complete-beginner-path.md)
- [GitHub Basics](documentation/learning-resources/Guides/github-basics/)
```

## File Structure After Copying

After copying, your structure might look like:

```
your-repo/
├── documentation/
│   └── learning-resources/  # or just "learning/"
│       ├── README.md
│       ├── Philosophy/
│       ├── Paths/
│       ├── Exercises/
│       ├── Templates/
│       └── Guides/
└── README.md
```

## Symlink Approach (Advanced)

For active development across multiple repos, use symlinks:

```bash
# From your-repo root
ln -s ../../sono-eval/documentation/Learning documentation/learning-resources
```

**Benefits:**

- Single source of truth
- Updates propagate automatically
- No duplication

**Drawbacks:**

- Requires sono-eval to be accessible
- Git doesn't track symlinks well (use git submodules if needed)

## Customization

Feel free to:

- Extract only what you need
- Modify content to match your repo's context
- Add repo-specific examples
- Combine with your existing documentation

## Maintenance

- **Primary source**: [tex-assist-coding/reusable](https://github.com/doronpers/tex-assist-coding/tree/main/reusable)
- **This directory**: Copy/extraction for sono-eval use
- **Updates**: For improvements, consider contributing to tex-assist-coding first
- **Versioning**: Consider tagging versions if breaking changes occur
