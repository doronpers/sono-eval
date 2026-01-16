# Prompt Engineering for Coding

The art of asking AI the right questions. Better prompts = better results.

## What Is Prompt Engineering?

**The Simple Version:**
How you phrase your question dramatically affects the AI's response.

Think of it like asking a librarian:

- ❌ "Book?" → Confused librarian
- ✅ "Do you have Python programming books for beginners?" → Helpful response

## The Core Principle

**Bad prompts → Vague, unhelpful responses**
**Good prompts → Specific, useful responses**

The AI can only work with what you give it.

## The Anatomy of a Good Prompt

### The Formula

```
[Context] + [Task] + [Constraints] + [Format]
```

**Context:** What's the situation?
**Task:** What do you want?
**Constraints:** Any limits or requirements?
**Format:** How should the response look?

### Example

**Bad Prompt:**

```
Create a function
```

**Good Prompt:**

```
Context: I'm building a FastAPI application for a todo list.
Task: Create a function to validate todo items before saving to database.
Constraints:
- Title must be 1-200 characters
- Description is optional
- Due date must be in the future
- Use Pydantic for validation
Format: Provide the Pydantic model and validation function with comments.
```

## Techniques That Work

### 1. Be Specific

**Vague:**

```
How do I use Python?
```

**Specific:**

```
How do I read a CSV file in Python 3.11 and convert it to a list of dictionaries?
```

### 2. Provide Context

**No Context:**

```
Fix this code:
[code]
```

**With Context:**

```
I'm writing a Flask app in Python 3.11.
This code should validate user registration but throws a KeyError.
Expected: Return error message for invalid input
Actual: Crashes with KeyError on line 5

[code]
```

### 3. Show Examples

**Without Examples:**

```
Create test cases for my function
```

**With Examples:**

```
Create test cases for my add() function.

Example format I want:
def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-1, -1) == -2
```

### 4. Specify Your Level

**Generic:**

```
Explain async/await
```

**Level-Appropriate:**

```
I'm a Python beginner (1 month experience).
Explain async/await with a simple real-world analogy before showing code.
```

### 5. Request Structure

**Unstructured:**

```
Tell me about API security
```

**Structured:**

```
Explain API security in this format:
1. Most critical vulnerability
2. How to prevent it
3. Code example
4. How to test it works

Keep each section to 2-3 sentences.
```

### 6. Iterate and Refine

**First Prompt:**

```
Create a user registration endpoint
```

**Follow-up:**

```
Add password validation:
- Min 8 characters
- At least one uppercase
- At least one number
```

**Continue:**

```
Add rate limiting to prevent spam
```

**Polish:**

```
Add unit tests for all validation rules
```

## Prompt Templates

### Template 1: Learning a Concept

```
I'm a [experience level] developer learning [language/framework].

Explain [concept] in this order:
1. Simple analogy
2. Basic code example
3. When to use it
4. Common mistakes

Keep it under 200 words.
```

**Example:**

```
I'm a beginner Python developer.

Explain list comprehensions in this order:
1. Simple analogy
2. Basic code example
3. When to use it
4. Common mistakes

Keep it under 200 words.
```

### Template 2: Debugging

```
I'm getting this error: [exact error message]

Context:
- Language/Framework: [details]
- What I'm trying to do: [goal]
- What's happening: [actual behavior]

Here's the relevant code:
[code]

What's wrong and how do I fix it?
```

### Template 3: Code Generation

```
Create a [component] in [language] that:
- [requirement 1]
- [requirement 2]
- [requirement 3]

Constraints:
- [constraint 1]
- [constraint 2]

Include:
- Comments explaining key parts
- Error handling
- Example usage
```

### Template 4: Code Review

```
Review this [language] code for:
1. Bugs
2. Security issues
3. Performance problems
4. Readability

[code]

For each issue found:
- Explain the problem
- Show the fix
- Explain why the fix is better
```

### Template 5: Refactoring

```
This [language] code works but has [problem]:
[code]

Refactor it to:
- [improvement 1]
- [improvement 2]

Show:
1. The refactored code
2. What changed and why
3. Any trade-offs
```

## Advanced Techniques

### Chain of Thought Prompting

Ask AI to explain its reasoning:

**Without CoT:**

```
Is this code correct?
[code]
```

**With CoT:**

```
Is this code correct? Think through it step by step:
1. What does each line do?
2. What could go wrong?
3. Are there edge cases not handled?
4. Final verdict: correct or not?

[code]
```

### Role Prompting

Ask AI to take a specific perspective:

```
Act as a senior Python developer reviewing code for security.

Review this authentication code:
[code]
```

### Comparison Prompting

Ask for multiple options:

```
Show me 3 different ways to implement user authentication in FastAPI:
1. Sessions
2. JWT tokens
3. OAuth

For each, explain:
- How it works
- Pros and cons
- When to use it
```

### Negative Instructions

Tell AI what NOT to do:

```
Explain recursion in Python.

Do NOT:
- Use mathematical examples (factorials, Fibonacci)
- Use technical jargon without explanation
- Make it longer than 150 words

DO:
- Use a real-world analogy
- Show a simple code example
- Explain when to use vs when to avoid
```

## Common Mistakes and Fixes

### Mistake 1: Too Vague

**Problem:**

```
Make this better
```

**Fix:**

```
Improve this code's readability by:
1. Adding descriptive variable names
2. Breaking long functions into smaller ones
3. Adding docstrings
```

### Mistake 2: Missing Context

**Problem:**

```
Why doesn't this work?
[code snippet]
```

**Fix:**

```
Python 3.11, FastAPI 0.104
This endpoint should return user data but returns 500 error.
Error message: [exact error]
[complete relevant code]
```

### Mistake 3: No Format Specified

**Problem:**

```
Explain classes in Python
```

**Fix:**

```
Explain Python classes in this format:
1. What they are (1 sentence)
2. Simple example (5-10 lines of code)
3. One real-world use case
4. How they're different from functions
```

### Mistake 4: Assuming Too Much Knowledge

**Problem:**

```
[Asking about advanced topic without stating level]
```

**Fix:**

```
I understand basic Python (variables, functions, loops)
but haven't used decorators yet.

Explain decorators starting from what I know.
```

### Mistake 5: No Constraints

**Problem:**

```
Create a web server
```

**Fix:**

```
Create a Python web server using Flask that:
- Runs on port 5000
- Has one endpoint: GET /hello returning "Hello World"
- Includes error handling
- Under 20 lines of code
```

## Language-Specific Tips

### Python

**Good prompts include:**

- Python version (3.11, 3.9, etc.)
- Type hints preference
- Style guide (PEP 8, Black, etc.)
- Framework specifics (FastAPI, Flask, Django)

```
Create a Python 3.11 function with type hints following PEP 8 that...
```

### JavaScript/TypeScript

**Good prompts include:**

- JS vs TS
- ES6+ features
- Framework (React, Vue, Node)
- Async preferences (callbacks, promises, async/await)

```
Create a TypeScript React component using hooks that...
```

### SQL

**Good prompts include:**

- Database type (PostgreSQL, MySQL, SQLite)
- Schema context
- Performance concerns

```
Write a PostgreSQL query that...
```

## Testing Your Prompts

### The Iteration Process

**Try 1:**

```
Create a login function
```

→ Generic response, not quite right

**Try 2:**

```
Create a login function in Python using Flask that validates username and password
```

→ Better, but missing details

**Try 3:**

```
Create a Flask login function that:
- Accepts username and password via POST
- Checks against database
- Returns JWT token if valid
- Returns 401 if invalid
- Includes error handling for database failures
```

→ Much better!

### A/B Testing Prompts

Try different phrasings:

**Version A:**

```
How do I make my code faster?
```

**Version B:**

```
Profile this Python code and suggest 3 specific optimizations:
[code]
```

See which gives better results!

## Prompt Libraries

### Keep Your Own Collection

Save prompts that work well for you:

```
# My Debugging Prompt
I'm getting this error in Python 3.11: [error]
Context: [what I'm doing]
Code: [relevant code]
Expected: [what should happen]
Actual: [what happens]

---

# My Code Review Prompt
Review this Python code for:
1. Bugs
2. Security issues
3. Pythonic style
[code]
```

### Share and Learn

- Look at others' successful prompts
- Adapt to your needs
- Contribute your discoveries

## Real-World Examples

### Example 1: From Bad to Good

**Bad:**

```
Error in code help
```

**Okay:**

```
My Python code has an error
```

**Good:**

```
Python 3.11 code throwing TypeError: 'NoneType' object is not subscriptable
[code]
What's wrong?
```

**Excellent:**

```
Python 3.11, FastAPI 0.104

Error: TypeError: 'NoneType' object is not subscriptable on line 47

Context: Fetching user from database, then accessing user['email']
Suspect: User might not exist but not handling it

Code:
[complete function with line numbers]

How should I handle this case properly?
```

### Example 2: Progressive Refinement

**First ask:**

```
Create a TODO app in Python
```

**Refine:**

```
Create a command-line TODO app in Python that:
- Adds tasks
- Lists tasks
- Marks tasks complete
- Stores in JSON file
```

**Polish:**

```
Create a command-line TODO app in Python 3.11:

Features:
- Add task with description and priority
- List all tasks or filter by priority
- Mark complete
- Delete tasks
- Persist in JSON file

Requirements:
- Use argparse for CLI
- Handle file not found
- Validate inputs
- Include docstrings
- Under 150 lines

Show: Main code + example usage
```

## Feeling Stuck?

**If AI responses aren't helpful:**

- Add more context about your situation
- Be more specific about what you want
- Show examples of what "good" looks like
- Try rephrasing completely

**If responses are too complicated:**

- Add "Explain like I'm a beginner"
- Request "Simple example first, then complex"
- Specify "Under 100 words"

**If you don't know what to ask:**

- Start with "What should I ask about [topic]?"
- Try "What do I need to know to [goal]?"
- Ask "What are common questions about [topic]?"

## Next Steps

Now that you understand prompting:

- **[AI Limitations](ai-limitations.md)** - Know what AI can't do
- **[Building Trust](building-trust.md)** - When to verify responses
- **[Discovery Exercises](discovery-exercises.md)** - Practice your skills

---

**Remember:** Prompting is a skill. You'll get better with practice! 🎯
