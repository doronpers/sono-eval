# AI Limitations: What AI Can't (Yet) Do

Let's be honest about what AI coding assistants can and can't do. Understanding limitations builds trust and prevents frustration.

## The Big Picture

AI is impressive but not magic. Think of it like:

- **Very smart autocomplete** - Recognizes patterns
- **Well-read junior developer** - Knows a lot but makes mistakes
- **Enthusiastic assistant** - Always willing but sometimes wrong

## What AI Is Great At

Before we dive into limitations, let's acknowledge strengths:

✅ **Pattern recognition** - Seen millions of code examples
✅ **Boilerplate generation** - Repetitive structures
✅ **Explaining concepts** - Breaking down ideas
✅ **Standard algorithms** - Common solutions
✅ **Syntax help** - Language rules and formatting
✅ **Quick suggestions** - Fast iterations

## Critical Limitations

### 1. AI Doesn't Understand Your Business Logic

**The Problem:**
AI has never worked at your company, seen your requirements, or talked to your users.

**Example:**

```python
# Your prompt:
"Create a function to calculate shipping cost"

# AI suggests:
def calculate_shipping(weight, distance):
    return weight * 0.5 + distance * 0.1
```

But your company's actual rules might be:

- Free shipping over $50
- Different rates by region
- Discounts for premium members
- Special handling for fragile items
- International customs fees

**AI can't know this!**

**What To Do:**

- Provide detailed requirements
- Expect to customize AI's suggestions
- You're the expert on YOUR business

### 2. AI Makes Confident Mistakes

**The Problem:**
AI presents wrong information with the same confidence as correct information.

**Example:**

```
You: "What's the latest FastAPI version?"
AI: "FastAPI 2.0.3" (confidently wrong - it's 0.104)
```

AI doesn't know what it doesn't know.

**What To Do:**

- Verify critical information
- Check official docs for latest versions
- Test before trusting
- Cross-reference important claims

### 3. AI Has Training Data Cutoffs

**The Problem:**
AI training stopped at a specific date. It doesn't know about:

- Features added after training
- Recent security patches
- New libraries
- Breaking changes
- Current best practices

**Example:**

```
You: "How do I use React 19 features?"
AI: [Might suggest React 18 patterns if trained before React 19]
```

**What To Do:**

- Specify versions in your prompts
- Check official docs for recent releases
- Verify with release notes
- Assume patterns might be outdated

### 4. AI Can't Test Your Code

**The Problem:**
AI generates code but can't run it to verify it works.

**Example:**

```python
# AI suggests:
def divide(a, b):
    return a / b

# Looks good! But crashes when b=0
```

**What To Do:**

- Always test AI-generated code
- Run tests before committing
- Check edge cases manually
- Treat AI code like Stack Overflow answers

### 5. AI Doesn't Know Your Codebase

**The Problem:**
(Except Cursor-style tools) AI only sees what you show it. It doesn't know:

- Your architecture
- Your naming conventions
- Your existing utilities
- Your team's patterns
- Your database schema

**Example:**

```python
# AI suggests creating a new date formatter
def format_date(date):
    return date.strftime("%Y-%m-%d")

# But you already have:
# utils/formatters.py with format_date_iso()
```

**What To Do:**

- Show relevant existing code
- Tell AI about utilities to reuse
- Review for duplication
- Refactor to use existing patterns

### 6. AI Can Suggest Insecure Code

**The Problem:**
AI learns from all code on the internet, including insecure examples.

**Common Issues:**

```python
# SQL Injection risk
query = f"SELECT * FROM users WHERE id = {user_id}"

# Hardcoded secrets
api_key = "sk-1234567890"

# Weak password validation
if len(password) > 6:  # Too weak!
    # allow

# Missing authentication checks
@app.get("/admin/users")
def get_all_users():  # No auth check!
    return users
```

**What To Do:**

- Always review for security
- Check for:
  - SQL injection risks
  - XSS vulnerabilities
  - Authentication missing
  - Hardcoded secrets
  - Weak validation
- Run security scanners
- Have security-focused code reviews

### 7. AI Can't Handle Ambiguity Well

**The Problem:**
Vague prompts get vague results.

**Example:**

```
Vague: "Create a user system"

AI thinks: Registration? Login? Profiles? Admin panel?
         OAuth? Email verification? Password reset?

Result: Generic half-solution to unclear problem
```

**What To Do:**

- Be extremely specific
- Provide examples
- Clarify requirements
- Iterate and refine

### 8. AI Doesn't Understand Context Across Conversations

**The Problem:**
Each response is somewhat independent. AI might:

- Forget what you discussed earlier
- Contradict previous suggestions
- Repeat itself
- Lose track of your goals

**Example:**

```
Early: "Use sessions for authentication"
Later: "Add JWT authentication" [contradicting earlier]
```

**What To Do:**

- Start fresh conversations for new topics
- Remind AI of important context
- Keep track of decisions yourself
- Don't rely on AI's memory

### 9. AI Can't Make Judgment Calls

**The Problem:**
Trade-offs require understanding your priorities.

**Example:**

```
You: "Should I optimize for speed or simplicity?"
AI: "It depends on..." [Can't decide for you]
```

Decisions that require judgment:

- Which framework to use
- Whether to refactor now or later
- What features to prioritize
- How much testing is enough
- When "good enough" is good enough

**What To Do:**

- Ask AI to explain options
- Make the decision yourself
- Consider your specific context
- Use AI for information, not decisions

### 10. AI Can't Debug Complex Issues

**The Problem:**
AI can help with simple bugs but struggles with:

- Race conditions
- Memory leaks
- Timing issues
- Complex interactions
- System-level problems

**Example:**

```
"My app crashes randomly in production but works locally"
→ AI can guess, but can't actually debug this
```

**What To Do:**

- Use AI for initial ideas
- Use proper debugging tools
- Add logging and monitoring
- Test systematically
- Don't rely solely on AI

## Specific Gotchas

### Mathematical/Algorithmic Errors

AI can confidently present wrong algorithms:

```python
# AI might suggest:
def is_prime(n):
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

# Works, but inefficient! Should check only up to sqrt(n)
```

**Always verify:**

- Mathematical correctness
- Algorithm efficiency
- Edge cases

### Outdated Patterns

AI might suggest deprecated approaches:

```python
# AI might suggest (outdated):
from flask_jwt import JWT  # Deprecated

# Current best practice:
from flask_jwt_extended import JWTManager
```

**What To Do:**

- Check library documentation
- Verify import statements
- Look for deprecation warnings

### Over-Engineering

AI might create more complexity than needed:

```python
# You asked for simple validation
# AI creates:
class ValidationEngine:
    def __init__(self):
        self.rules = []
        self.validators = {}
    # ... 100 lines later

# You needed:
def validate_email(email):
    return "@" in email and "." in email
```

**What To Do:**

- Start simple
- Add complexity only when needed
- Question over-engineered solutions

### Copy-Paste Without Understanding

This is a YOU limitation, not AI:

```python
# Copying AI code you don't understand
[mysterious code]  # How does this work? ¯\_(ツ)_/¯
```

**What To Do:**

- Always understand before using
- Ask AI to explain
- Break down complex code
- Learn from each suggestion

## What AI Will NEVER Do

(At least not yet...)

### 1. Replace Your Judgment

AI doesn't understand your project goals, user needs, or business constraints.

### 2. Guarantee Correctness

AI can't prove code is bug-free or will work in all cases.

### 3. Understand Impact

AI doesn't know if a change will break production or affect users negatively.

### 4. Take Responsibility

When AI-generated code causes issues, you're responsible.

### 5. Maintain Long-Term Vision

AI can't plan your architecture or technical strategy.

## Working Within Limitations

### The Productive Mindset

**Think of AI as:**

- A very capable assistant (not a replacement)
- A source of ideas (not final answers)
- A learning tool (not a crutch)
- A productivity booster (not a substitute for skill)

### Best Practices

**1. Verify Important Code**

```
AI suggests → You review → You test → You commit
```

**2. Use AI for First Draft**

```
AI generates → You understand → You refine → You perfect
```

**3. Cross-Check Critical Logic**

```
AI suggests approach → You verify with docs → You test edge cases
```

**4. Learn from AI, Don't Just Copy**

```
AI shows pattern → You understand why → You can apply independently
```

**5. Keep AI in the Loop, Not in Control**

```
You design → AI assists → You review → You decide → You implement
```

## Red Flags to Watch For

### 🚩 Red Flag 1: "Just Trust Me" Code

Code you don't understand but use anyway.

**Fix:** Ask AI to explain until you understand.

### 🚩 Red Flag 2: No Error Handling

AI often omits error handling for brevity.

**Fix:** Always add comprehensive error handling.

### 🚩 Red Flag 3: Hardcoded Values

Magic numbers and strings without explanation.

**Fix:** Use constants, environment variables, or configuration.

### 🚩 Red Flag 4: No Tests

AI rarely includes comprehensive tests.

**Fix:** Write tests yourself or ask AI specifically for tests.

### 🚩 Red Flag 5: Security Assumptions

Code that assumes inputs are always valid/safe.

**Fix:** Validate all inputs, sanitize data, check authentication.

## Real-World Disaster Scenarios

### Scenario 1: The Production Crash

**What Happened:**
Developer copy-pasted AI code for database queries without testing edge cases. Crashed when database returned null.

**Lesson:**
Test all code paths, especially error cases.

### Scenario 2: The Security Breach

**What Happened:**
AI suggested code vulnerable to SQL injection. Developer didn't recognize it. Production database exposed.

**Lesson:**
Review all code for security, especially database and user input handling.

### Scenario 3: The Technical Debt

**What Happened:**
AI generated quick solutions for 6 months. Codebase became unmaintainable mess of inconsistent patterns.

**Lesson:**
Refactor AI suggestions to match your codebase patterns.

### Scenario 4: The Lost Knowledge

**What Happened:**
Team relied 100% on AI. When AI couldn't solve a complex problem, no one understood the codebase anymore.

**Lesson:**
Use AI to assist, not replace, your understanding.

## Feeling Stuck?

**If AI keeps giving wrong answers:**

- Provide more context
- Be more specific
- Show examples
- Try different AI
- Verify with documentation

**If you don't trust AI anymore:**

- Good! Healthy skepticism is important
- Use AI as one tool among many
- Verify everything critical
- Learn to spot common AI mistakes

**If you're too dependent on AI:**

- Try coding without AI for a bit
- Focus on understanding fundamentals
- Ensure you can explain your code
- Build confidence in your own skills

## Next Steps

Now that you understand limitations:

- **[Building Trust](building-trust.md)** - When to verify
- **[Comparing Tools](comparing-tools.md)** - Which tool for what
- **[Discovery Exercises](discovery-exercises.md)** - Practice critical evaluation

---

**Remember:** AI is powerful but imperfect. Your judgment is irreplaceable! 🧠
