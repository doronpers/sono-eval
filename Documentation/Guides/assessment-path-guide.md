# Assessment Path Guide

**Complete Guide to Sono-Eval Assessment Paths**

This guide provides detailed explanations of each assessment path in Sono-Eval, helping you understand what is being evaluated, how scores are determined, and how to prepare effectively.

---

## 📋 Overview

Sono-Eval evaluates candidates across **five distinct assessment paths**, each focusing on different aspects of software development. You can choose which paths to complete based on your goals and the requirements of your assessment.

### Why Multiple Paths?

Traditional assessments often focus only on code correctness. Sono-Eval recognizes that great developers excel in many dimensions:

- **Technical skills** are important, but so is **design thinking**
- **Problem-solving ability** matters, but **collaboration** is equally valuable
- **Communication** skills enable effective teamwork

By evaluating multiple paths, Sono-Eval provides a more complete picture of your capabilities and potential.

---

## 🔧 Technical Path

**Focus**: Code quality, algorithms, problem-solving efficiency, and technical best practices

### What Is Evaluated?

The Technical path assesses your ability to write clean, efficient, and correct code. This is the most traditional aspect of coding assessments, but Sono-Eval goes deeper than just "does it work?"

#### Key Metrics

1. **Code Quality** (30% weight)
   - Code structure and organization
   - Naming conventions and readability
   - Consistency in style
   - Best practices adherence

2. **Problem Solving** (30% weight)
   - Algorithm efficiency (time/space complexity)
   - Approach to solving problems
   - Edge case handling
   - Optimization strategies

3. **Testing** (20% weight)
   - Test coverage
   - Test quality and comprehensiveness
   - Edge case testing
   - Test organization

4. **Technical Correctness** (20% weight)
   - Functional correctness
   - Error handling
   - Resource management
   - Security considerations

### Scoring Criteria

**Excellent (80-100)**:
- Clean, well-structured code following best practices
- Efficient algorithms with appropriate complexity
- Comprehensive test coverage
- Handles edge cases gracefully
- No obvious bugs or security issues

**Good (60-79)**:
- Generally clean code with minor style issues
- Functional algorithms, may not be optimal
- Basic test coverage present
- Most edge cases handled

**Developing (40-59)**:
- Code works but needs refactoring
- Algorithms functional but inefficient
- Limited or missing tests
- Some edge cases not handled

**Learning (0-39)**:
- Code has significant structural issues
- Algorithms may not work correctly
- No tests or very basic tests
- Many edge cases missed

### Examples

**Strong Technical Example**:
```python
def find_duplicates(arr):
    """
    Find duplicate elements in an array.
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    
    Args:
        arr: List of integers
        
    Returns:
        Set of duplicate values
    """
    seen = set()
    duplicates = set()
    
    for item in arr:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    
    return duplicates
```

**What makes this strong**:
- Clear documentation with complexity analysis
- Efficient algorithm (O(n) time)
- Good naming and structure
- Handles edge cases (empty array, no duplicates)

### How to Prepare

1. **Practice Clean Code**
   - Focus on readability and maintainability
   - Use meaningful variable names
   - Follow language-specific style guides

2. **Study Algorithms**
   - Understand time/space complexity
   - Practice common patterns (two pointers, sliding window, etc.)
   - Learn when to optimize vs. when to prioritize clarity

3. **Write Tests**
   - Practice TDD (Test-Driven Development)
   - Test edge cases and error conditions
   - Organize tests clearly

4. **Review Best Practices**
   - Language-specific idioms
   - Common pitfalls to avoid
   - Security considerations

---

## 🎨 Design Path

**Focus**: Architecture decisions, design patterns, system thinking, and modularity

### What Is Evaluated?

The Design path assesses your ability to think about software architecture, make good design decisions, and create maintainable, scalable solutions.

#### Key Metrics

1. **Architecture** (40% weight)
   - System structure and organization
   - Separation of concerns
   - Modularity and component design
   - Scalability considerations

2. **Design Patterns** (30% weight)
   - Appropriate pattern usage
   - Pattern implementation quality
   - Understanding of when to use patterns

3. **System Thinking** (20% weight)
   - Understanding of system interactions
   - Consideration of dependencies
   - Integration points
   - Future extensibility

4. **Code Organization** (10% weight)
   - File and directory structure
   - Module organization
   - Clear boundaries between components

### Scoring Criteria

**Excellent (80-100)**:
- Well-architected solution with clear separation of concerns
- Appropriate use of design patterns
- Considers scalability and future needs
- Clean, logical code organization

**Good (60-79)**:
- Generally good architecture with minor issues
- Some design patterns used appropriately
- Basic consideration of system interactions
- Reasonable code organization

**Developing (40-59)**:
- Architecture works but could be improved
- Limited use of design patterns
- Minimal system thinking
- Code organization needs work

**Learning (0-39)**:
- Poor architectural decisions
- No clear design patterns
- Little consideration of system design
- Disorganized code structure

### Examples

**Strong Design Example**:
```
project/
├── src/
│   ├── domain/
│   │   ├── models.py          # Core business logic
│   │   └── services.py
│   ├── infrastructure/
│   │   ├── database.py        # Data access layer
│   │   └── cache.py
│   └── api/
│       ├── routes.py          # API endpoints
│       └── middleware.py
├── tests/
│   ├── unit/
│   └── integration/
└── README.md
```

**What makes this strong**:
- Clear separation between domain, infrastructure, and API layers
- Tests organized by type
- Logical grouping of related functionality
- Easy to understand and navigate

### How to Prepare

1. **Study Architecture Patterns**
   - Layered architecture
   - Clean architecture principles
   - Microservices vs. monoliths
   - Domain-driven design

2. **Learn Design Patterns**
   - Common patterns (Factory, Strategy, Observer, etc.)
   - When to use each pattern
   - Anti-patterns to avoid

3. **Practice System Design**
   - Think about scalability
   - Consider integration points
   - Plan for future changes
   - Document architectural decisions

4. **Review Real Projects**
   - Study open-source projects
   - Analyze their structure
   - Understand design decisions

---

## 🤝 Collaboration Path

**Focus**: Code readability, documentation quality, communication clarity, and team-oriented thinking

### What Is Evaluated?

The Collaboration path assesses how well your code and documentation enable others to understand, maintain, and extend your work. Great developers write code that others can work with.

#### Key Metrics

1. **Documentation** (30% weight)
   - README quality and completeness
   - Inline comments and docstrings
   - API documentation
   - Setup and usage instructions

2. **Code Readability** (30% weight)
   - Self-documenting code
   - Clear naming conventions
   - Logical flow and structure
   - Comments where needed (not excessive)

3. **Communication** (25% weight)
   - Clear explanations of decisions
   - Thought process documentation
   - Assumptions stated explicitly
   - Trade-offs explained

4. **Team Orientation** (15% weight)
   - Consideration of other developers
   - Code review readiness
   - Maintainability focus
   - Onboarding considerations

### Scoring Criteria

**Excellent (80-100)**:
- Comprehensive, clear documentation
- Highly readable, self-documenting code
- Excellent communication of decisions and reasoning
- Code is easy for others to understand and modify

**Good (60-79)**:
- Good documentation with minor gaps
- Generally readable code
- Clear communication of most decisions
- Code is mostly maintainable

**Developing (40-59)**:
- Basic documentation present
- Code readable but needs improvement
- Some decisions explained
- Maintainability could be better

**Learning (0-39)**:
- Minimal or missing documentation
   - Code is difficult to understand
   - Little explanation of decisions
   - Hard for others to work with

### Examples

**Strong Collaboration Example**:

**README.md**:
```markdown
# Project Name

## Overview
Brief description of what this project does and why it exists.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Configure environment: `cp .env.example .env`
3. Run: `python main.py`

## Architecture
- `src/core/` - Core business logic
- `src/api/` - API endpoints
- `tests/` - Test suite

## Contributing
See CONTRIBUTING.md for guidelines.
```

**Code with good documentation**:
```python
def calculate_shipping_cost(weight: float, distance: float) -> float:
    """
    Calculate shipping cost based on weight and distance.
    
    Uses a tiered pricing model:
    - Base rate: $5.00
    - Weight surcharge: $0.50 per pound over 10 lbs
    - Distance surcharge: $0.10 per mile over 50 miles
    
    Args:
        weight: Package weight in pounds
        distance: Shipping distance in miles
        
    Returns:
        Total shipping cost in dollars
        
    Raises:
        ValueError: If weight or distance is negative
        
    Example:
        >>> calculate_shipping_cost(5.0, 30.0)
        5.0
        >>> calculate_shipping_cost(15.0, 100.0)
        7.5
    """
    if weight < 0 or distance < 0:
        raise ValueError("Weight and distance must be non-negative")
    
    base_rate = 5.00
    weight_surcharge = max(0, (weight - 10) * 0.50)
    distance_surcharge = max(0, (distance - 50) * 0.10)
    
    return base_rate + weight_surcharge + distance_surcharge
```

**What makes this strong**:
- Clear docstring explaining the algorithm
- Type hints for parameters and return
- Examples showing usage
- Error handling documented
- Formula explained

### How to Prepare

1. **Write Clear Documentation**
   - Practice writing README files
   - Document your thought process
   - Include examples and use cases
   - Explain "why" not just "what"

2. **Improve Code Readability**
   - Use descriptive names
   - Keep functions focused and small
   - Add comments for complex logic
   - Remove unnecessary comments (code should be self-documenting)

3. **Practice Explaining Decisions**
   - Write decision logs
   - Explain trade-offs
   - Document assumptions
   - Share your reasoning

4. **Think About Others**
   - Consider what someone new to your code would need
   - Write code as if someone else will maintain it
   - Make onboarding easy
   - Prepare for code reviews

---

## 🧩 Problem Solving Path

**Focus**: Analytical thinking, approach to challenges, creative solutions, and debugging skills

### What Is Evaluated?

The Problem Solving path assesses your approach to tackling challenges, breaking down complex problems, and finding creative solutions.

#### Key Metrics

1. **Problem Analysis** (30% weight)
   - Understanding of the problem
   - Breaking down complex problems
   - Identifying constraints and requirements
   - Edge case identification

2. **Solution Approach** (30% weight)
   - Logical problem-solving steps
   - Creative thinking
   - Multiple solution consideration
   - Optimal solution selection

3. **Debugging & Troubleshooting** (25% weight)
   - Systematic debugging approach
   - Error analysis
   - Testing hypotheses
   - Fixing issues effectively

4. **Adaptability** (15% weight)
   - Handling unexpected issues
   - Adjusting approach when needed
   - Learning from mistakes
   - Iterative improvement

### Scoring Criteria

**Excellent (80-100)**:
- Deep understanding of the problem
- Systematic, logical approach
- Creative solutions when appropriate
- Excellent debugging skills

**Good (60-79)**:
- Good problem understanding
- Generally logical approach
- Some creative thinking
- Solid debugging abilities

**Developing (40-59)**:
- Basic problem understanding
- Approach works but could be improved
- Limited creative solutions
- Basic debugging skills

**Learning (0-39)**:
- Poor problem analysis
- Unclear or inefficient approach
   - Little creative thinking
   - Struggles with debugging

### Examples

**Strong Problem Solving Example**:

**Problem**: Find the longest substring without repeating characters

**Approach Documentation**:
```
1. Problem Analysis:
   - Need to find longest substring (not subsequence)
   - Characters must be unique within substring
   - Edge cases: empty string, all same chars, all unique

2. Solution Strategy:
   - Use sliding window technique
   - Track characters in current window with set
   - Expand window when no duplicates
   - Shrink window when duplicate found

3. Algorithm:
   - Two pointers: left and right
   - Move right pointer, add to set
   - If duplicate found, move left until duplicate removed
   - Track maximum length seen

4. Complexity:
   - Time: O(n) - each character visited at most twice
   - Space: O(min(n, m)) where m is charset size
```

**What makes this strong**:
- Clear problem analysis
- Systematic approach documented
- Edge cases considered
- Complexity analyzed
- Efficient solution chosen

### How to Prepare

1. **Practice Problem Decomposition**
   - Break large problems into smaller parts
   - Identify sub-problems
   - Understand dependencies
   - Map out solution steps

2. **Study Problem-Solving Techniques**
   - Sliding window
   - Two pointers
   - Dynamic programming
   - Greedy algorithms
   - Backtracking

3. **Improve Debugging Skills**
   - Practice systematic debugging
   - Use debugging tools effectively
   - Read error messages carefully
   - Test hypotheses methodically

4. **Think Creatively**
   - Consider multiple approaches
   - Don't settle for first solution
   - Look for patterns
   - Learn from others' solutions

---

## 💬 Communication Path

**Focus**: Clarity of explanations, documentation quality, ability to convey technical concepts, and teaching ability

### What Is Evaluated?

The Communication path assesses how well you can explain technical concepts, document your work, and help others understand your solutions.

#### Key Metrics

1. **Clarity** (35% weight)
   - Clear, concise explanations
   - Appropriate technical detail level
   - Easy to understand
   - Well-structured communication

2. **Documentation Quality** (30% weight)
   - Comprehensive documentation
   - Clear examples
   - Proper formatting
   - Up-to-date information

3. **Technical Writing** (25% weight)
   - Proper use of technical terms
   - Logical flow of information
   - Appropriate detail level
   - Professional tone

4. **Teaching Ability** (10% weight)
   - Ability to explain complex concepts simply
   - Anticipates questions
   - Provides context
   - Helps others learn

### Scoring Criteria

**Excellent (80-100)**:
- Exceptionally clear and well-structured communication
- Comprehensive, high-quality documentation
- Excellent technical writing
- Makes complex topics accessible

**Good (60-79)**:
- Clear communication with minor issues
- Good documentation quality
- Solid technical writing
- Generally helpful explanations

**Developing (40-59)**:
- Communication is understandable but could be clearer
- Basic documentation present
- Technical writing needs improvement
- Some explanations are unclear

**Learning (0-39)**:
- Unclear or confusing communication
- Poor or missing documentation
- Weak technical writing
- Difficult for others to understand

### Examples

**Strong Communication Example**:

**Technical Explanation**:
```markdown
## Why We Use Dependency Injection

Dependency Injection (DI) is a design pattern that makes our code more
testable and maintainable.

### The Problem
When classes create their own dependencies directly, they become tightly
coupled and hard to test:

```python
class UserService:
    def __init__(self):
        self.db = Database()  # Hard to test!
```

### The Solution
With DI, dependencies are provided from outside:

```python
class UserService:
    def __init__(self, db: Database):
        self.db = db  # Easy to mock in tests!
```

### Benefits
1. **Testability**: Can inject mock dependencies
2. **Flexibility**: Easy to swap implementations
3. **Maintainability**: Changes are isolated

### Example Usage
```python
# Production
db = PostgreSQLDatabase()
service = UserService(db)

# Testing
mock_db = MockDatabase()
service = UserService(mock_db)
```
```

**What makes this strong**:
- Explains the "why" not just "what"
- Shows problem and solution
- Provides concrete examples
- Lists benefits clearly
- Uses code examples effectively

### How to Prepare

1. **Practice Technical Writing**
   - Write blog posts or documentation
   - Explain concepts to others
   - Get feedback on your writing
   - Study good technical documentation

2. **Improve Clarity**
   - Use simple language when possible
   - Structure information logically
   - Use examples liberally
   - Anticipate questions

3. **Develop Teaching Skills**
   - Explain concepts to beginners
   - Create tutorials or guides
   - Use analogies effectively
   - Break down complex topics

4. **Study Great Communicators**
   - Read excellent technical blogs
   - Watch technical talks
   - Analyze what makes them effective
   - Practice their techniques

---

## 🎯 Choosing Your Paths

### Which Paths Should You Complete?

**For Technical Roles**:
- **Required**: Technical, Problem Solving
- **Recommended**: Design, Communication
- **Optional**: Collaboration

**For Senior/Architecture Roles**:
- **Required**: Technical, Design, Problem Solving
- **Recommended**: Communication, Collaboration

**For Team Lead Roles**:
- **Required**: Collaboration, Communication
- **Recommended**: Technical, Design, Problem Solving

**For Learning & Growth**:
- **Complete all paths** to get a comprehensive view of your skills

### Path Combinations

Some paths complement each other well:

- **Technical + Design**: Shows both coding ability and architectural thinking
- **Collaboration + Communication**: Demonstrates strong team skills
- **Problem Solving + Technical**: Highlights analytical and coding skills together

---

## 📊 Understanding Your Scores

### Score Interpretation

Each path is scored independently on a 0-100 scale:

- **80-100**: Excellent - You're demonstrating strong skills in this area
- **60-79**: Good - You're on the right track with room to grow
- **40-59**: Developing - You're building skills, focus on the recommendations
- **0-39**: Learning - This is an area to focus your study

### Overall Score

Your overall score is calculated as a weighted average of the paths you completed. Each path contributes equally unless specified otherwise.

### What Matters Most?

**Remember**: Lower scores aren't failures—they're opportunities! Sono-Eval provides specific recommendations for each path, telling you exactly what to improve.

---

## 💡 Tips for Success

### General Tips

1. **Read the Requirements Carefully**
   - Understand what each path evaluates
   - Review the scoring criteria
   - Know what's expected

2. **Show Your Work**
   - Document your thought process
   - Explain your decisions
   - Include comments and documentation

3. **Think About the User**
   - Write code others can understand
   - Consider maintainability
   - Make it easy to use

4. **Don't Rush**
   - Take time to think through problems
   - Review your work
   - Test thoroughly

### Path-Specific Tips

**Technical Path**:
- Focus on clean, efficient code
- Write tests
- Handle edge cases
- Follow best practices

**Design Path**:
- Think about architecture
- Use appropriate patterns
- Consider scalability
- Organize code logically

**Collaboration Path**:
- Write clear documentation
- Make code readable
- Explain your decisions
- Think about others

**Problem Solving Path**:
- Analyze problems thoroughly
- Show your approach
- Consider multiple solutions
- Document your thinking

**Communication Path**:
- Write clearly and concisely
- Use examples
- Explain complex concepts simply
- Structure information well

---

## 🔄 Improving Over Time

### Track Your Progress

Sono-Eval tracks your scores over time, allowing you to see improvement in each path. Use this to:

- Identify areas of growth
- Focus your learning efforts
- Celebrate improvements
- Set goals for next assessments

### Focus Areas

Based on your scores, focus on:

- **Low Technical scores**: Practice algorithms, study best practices
- **Low Design scores**: Learn architecture patterns, study system design
- **Low Collaboration scores**: Improve documentation, practice code reviews
- **Low Problem Solving scores**: Practice problem decomposition, study techniques
- **Low Communication scores**: Write more, explain concepts, get feedback

---

## 📚 Additional Resources

- **[Candidate Guide](resources/candidate-guide.md)** - General guide for candidates
- **[Learning Resources](resources/learning.md)** - Educational content and tutorials
- **[Examples](resources/examples/)** - Code examples for each path
- **[FAQ](faq.md)** - Frequently asked questions

---

## ❓ Questions?

If you have questions about assessment paths:

1. Check the [FAQ](faq.md)
2. Review the [Candidate Guide](resources/candidate-guide.md)
3. Contact your assessment coordinator

---

**Remember**: Sono-Eval is designed to help you grow. Use the feedback to improve, and don't be discouraged by lower scores—they're just starting points for your development journey!
