# Learning Resources

This directory contains reusable learning resources extracted from [tex-assist-coding](https://github.com/doronpers/tex-assist-coding/tree/main/reusable), structured for use across multiple repositories.

**Source Repository**: The original source of these resources is [tex-assist-coding/reusable](https://github.com/doronpers/tex-assist-coding/tree/main/reusable). This directory is a copy/extraction for use within sono-eval.

## 📚 Contents

### Philosophy

- **[Dark Horse Approach](Philosophy/dark-horse-approach.md)** - Individualized learning framework based on Todd Rose's principles
- **[Micro-Motives Framework](Philosophy/micro-motives-framework.md)** - Understanding what energizes learners

### Learning Paths

- **[Complete Beginner Path](Paths/complete-beginner-path.md)** - Month-by-month roadmap for absolute beginners
- **[Technical Leader Learning](Paths/technical-leader-learning.md)** - Path for managers and technical leaders learning to code

### Exercises

- **[Discover Your Micro-Motives](Exercises/discover-your-micro-motives.md)** - Self-discovery exercise to identify what energizes you

### Templates

- **[Learning Journal](Templates/learning-journal.md)** - Progress tracking template
- **[Pull Request Description](Templates/pull-request-description.md)** - PR template for beginners
- **[Project README](Templates/project-readme.md)** - README template

### Guides

- **[GitHub Basics](Guides/github-basics/)** - Beginner-friendly GitHub documentation
- **[AI Tools](Guides/ai-tools/)** - AI coding tools guide
- **[Workflow Building](Guides/workflow-building/)** - Personal workflow development

## 🎯 How to Use in Other Repositories

### Option 1: Symlink (Recommended)

```bash
# From another repo
ln -s ../../sono-eval/documentation/Learning documentation/learning-resources
```

### Option 2: Copy Specific Files

```bash
# Copy only what you need
cp sono-eval/documentation/Learning/Philosophy/dark-horse-approach.md \
   your-repo/documentation/learning-philosophy.md
```

### Option 3: Reference in Documentation

```markdown
For learning resources, see [sono-eval Learning Resources](https://github.com/doronpers/sono-eval/tree/main/documentation/Learning)
```

## 📝 Notes

- These resources are designed to be **portable and reusable**
- **Source**: Original content is maintained in [tex-assist-coding/reusable](https://github.com/doronpers/tex-assist-coding/tree/main/reusable)
- Update paths/links when copying to other repos
- For contributions or updates, consider contributing back to tex-assist-coding

## 🔗 Related Resources

- [Portability Guide](PORTABILITY.md) - Detailed guide for reusing these resources
- [Sono-Eval Learning Guide](../Guides/resources/learning.md) - Integration with sono-eval's learning resources
