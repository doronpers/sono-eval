# Code Examples

Practical examples to help you understand what good submissions look like.

---

## Overview

These examples show actual code submissions with Sono-Eval assessments. Each example includes:
- The challenge/problem
- The submitted solution
- Assessment results and feedback
- What was done well
- What could be improved

**Use these to**:
- Understand expectations
- See what "good" looks like
- Learn from feedback patterns
- Improve your own submissions

---

## Examples by Level

### Beginner Level
- **[Example 1: String Manipulation](example-01-string-manipulation.md)** - Basic function with good documentation
- **[Example 2: List Processing](example-02-list-processing.md)** - Simple algorithm with tests

### Intermediate Level
- **[Example 3: API Design](example-03-api-design.md)** - RESTful endpoint with error handling
- **[Example 4: Data Processing](example-04-data-processing.md)** - File parsing with validation

### Advanced Level
- **[Example 5: System Design](example-05-system-design.md)** - Multi-component architecture
- **[Example 6: Performance Optimization](example-06-optimization.md)** - Algorithm improvement

---

## Examples by Path

### Technical Path
- Strong code quality
- Efficient algorithms
- Comprehensive testing
- Error handling

### Design Path
- Clear architecture
- Good abstractions
- Maintainable structure
- Design patterns

### Collaboration Path
- Excellent documentation
- Clear README
- Helpful comments
- Good communication

---

## Example Structure

Each example follows this format:

```markdown
# Challenge
What was asked

# Solution
The submitted code

# Assessment Results
Scores and feedback

# Analysis
What went well, what to improve

# Learning Points
Key takeaways
```

---

## Quick Example

### Challenge: Factorial Function

**Task**: Write a function to calculate factorial with proper error handling.

### Solution A (Score: 65/100)

```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
```

**Feedback**:
- ✅ Correct algorithm
- ❌ No input validation
- ❌ No documentation
- ❌ No tests
- ❌ Stack overflow risk for large n

### Solution B (Score: 90/100)

```python
def factorial(n: int) -> int:
    """
    Calculate factorial of n using recursion.

    Args:
        n: Non-negative integer

    Returns:
        Factorial of n

    Raises:
        ValueError: If n is negative
        RecursionError: If n is too large (>1000)
    """
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")
    if n > 1000:
        raise RecursionError("n too large for recursive solution")

    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)


# Tests
def test_factorial():
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(5) == 120

    try:
        factorial(-1)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
```

**Feedback**:
- ✅ Complete documentation
- ✅ Type hints
- ✅ Input validation
- ✅ Tests included
- ✅ Error handling
- 💡 Could use iterative approach for better performance

### Learning Points

1. **Documentation matters**: Explain what your code does
2. **Validate inputs**: Check for edge cases
3. **Add type hints**: Makes code clearer
4. **Include tests**: Shows you care about correctness
5. **Consider alternatives**: There might be better approaches

---

## How to Use These Examples

### 1. Before Your Assessment
- Read through examples at your level
- Note common patterns in good solutions
- Understand what evaluators look for
- Practice similar challenges

### 2. While Working
- Remember: documentation, tests, error handling
- Think about multiple paths (technical, design, collaboration)
- Include a README if appropriate
- Comment complex logic

### 3. After Receiving Feedback
- Compare your solution to examples
- Find similar patterns in feedback
- Identify areas to practice
- Try resubmitting with improvements

---

## Contributing Examples

Have a great submission you'd like to share? Contribute it!

See [Contributing Guide](../../CONTRIBUTING.md) for details.

---

## More Resources

- **[Candidate Guide](candidate-guide.md)** - Welcome guide for candidates
- **[Learning Resources](learning.md)** - Tutorials and best practices
- **[FAQ](../faq.md)** - Common questions
- **[Quick Start](../quick-start.md)** - Get started with Sono-Eval

---

**Last Updated**: January 10, 2026  
**Version**: 0.1.0
