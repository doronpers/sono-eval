# Start Simple: The Three Questions Workflow

The simplest possible workflow that actually works. Perfect for beginners and quick projects.

## The Entire Workflow

Before writing any code, ask yourself three questions:

### Question 1: What am I building?

*Answer in one clear sentence.*

### Question 2: How will I know it works?

*Give one specific test case.*

### Question 3: What could go wrong?

*Identify one potential issue.*

That's it! Everything else is optional.

## Why This Works

### It Forces Clarity

**Without these questions:**

```
"I need to... do something with users... and maybe emails...
or was it passwords? Let me just start coding..."
```

**With these questions:**

```
1. What: Create a function to validate email format
2. Test: validate_email("test@example.com") returns True
3. Edge case: What if email is empty string?
```

Clear thinking leads to clear code.

### It's Actually Achievable

Most workflow advice is overwhelming:

- ❌ "Write comprehensive test suites"
- ❌ "Design complete architecture"
- ❌ "Document every decision"

Three questions? Anyone can do that.

### It Builds Good Habits

Start with three questions, gradually add:

- Week 2: Answer all three for every function
- Week 4: Write the test case before coding
- Month 2: Add more edge cases
- Month 4: Add documentation
- Your habits grow naturally!

## How to Use It

### Step 1: Ask the Questions

**Before touching code**, write down answers.

Use a comment, text file, or paper:

```python
# PROJECT: User Registration System

# 1. WHAT am I building?
#    A function that registers a new user with email and password

# 2. HOW will I know it works?
#    register_user("alice@example.com", "securepass123")
#    should return {"success": True, "user_id": 1}

# 3. WHAT could go wrong?
#    Email might already exist in database
```

### Step 2: Now Code

With clarity, coding is easier:

```python
def register_user(email, password):
    # Check if email already exists
    if user_exists(email):
        return {"success": False, "error": "Email already registered"}

    # Create user
    user_id = create_user(email, password)
    return {"success": True, "user_id": user_id}
```

### Step 3: Test Your Test Case

Run the specific test you identified:

```python
# Test the case from Question 2
result = register_user("alice@example.com", "securepass123")
print(result)  # Should see {"success": True, "user_id": 1}
```

### Step 4: Test Your Edge Case

Check the potential issue from Question 3:

```python
# Try to register same email twice
result1 = register_user("bob@example.com", "pass1")
result2 = register_user("bob@example.com", "pass2")
print(result2)  # Should see error about email existing
```

## Real Examples

### Example 1: Calculate Shipping Cost

**The Three Questions:**

```
1. WHAT: Calculate shipping cost based on weight and distance
2. TEST: calculate_shipping(weight=5, distance=100) returns 15.0
3. EDGE: What if weight is 0 or negative?
```

**The Code:**

```python
def calculate_shipping(weight, distance):
    """Calculate shipping cost."""
    # Handle edge case from Question 3
    if weight <= 0:
        raise ValueError("Weight must be positive")

    # Simple formula for now
    cost_per_kg = 1.0
    cost_per_km = 0.1
    return (weight * cost_per_kg) + (distance * cost_per_km)

# Test from Question 2
assert calculate_shipping(5, 100) == 15.0

# Test edge case from Question 3
try:
    calculate_shipping(-5, 100)
    print("ERROR: Should have raised exception!")
except ValueError:
    print("✓ Edge case handled correctly")
```

### Example 2: Filter Active Users

**The Three Questions:**

```
1. WHAT: Filter list of users to only those active in last 30 days
2. TEST: Given users with last_login dates, return only recent ones
3. EDGE: What if list is empty?
```

**The Code:**

```python
from datetime import datetime, timedelta

def filter_active_users(users):
    """Return users active in last 30 days."""
    # Handle edge case from Question 3
    if not users:
        return []

    cutoff_date = datetime.now() - timedelta(days=30)
    return [user for user in users if user['last_login'] > cutoff_date]

# Test from Question 2
test_users = [
    {'name': 'Alice', 'last_login': datetime.now()},  # Active
    {'name': 'Bob', 'last_login': datetime.now() - timedelta(days=60)},  # Inactive
]
active = filter_active_users(test_users)
assert len(active) == 1
assert active[0]['name'] == 'Alice'

# Test edge case from Question 3
assert filter_active_users([]) == []
print("✓ All tests pass!")
```

### Example 3: API Endpoint

**The Three Questions:**

```
1. WHAT: API endpoint to get user by ID
2. TEST: GET /users/123 returns user data
3. EDGE: What if user doesn't exist?
```

**The Code:**

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    """Get user by ID."""
    # In real app, query database
    user = database.get_user(user_id)

    # Handle edge case from Question 3
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

# Manual test for Question 2
# Run server, then: curl http://localhost:8000/users/123

# Test edge case from Question 3
# curl http://localhost:8000/users/99999
# Should return 404 error
```

## Using with AI

### Ask AI Your Three Questions

**Prompt:**

```
I need to build: [Answer to Question 1]

Success looks like: [Answer to Question 2]

Potential issue: [Answer to Question 3]

Generate Python code that handles all of this.
```

**Example:**

```
I need to build: A function to validate email addresses

Success looks like: validate_email("test@example.com") returns True

Potential issue: What if the email is None or empty string?

Generate Python code that handles all of this.
```

AI will generate code that addresses all three points!

### Let AI Help With Question 3

If you can't think of an edge case:

**Prompt:**

```
I'm building a function to [description].

What's one common edge case I should handle?
```

**Example:**

```
I'm building a function to calculate average of a list of numbers.

What's one common edge case I should handle?

AI response: "Empty list! It will cause division by zero."
```

## Evolving Beyond Three Questions

### After 2 Weeks: Add More Tests

```
1. WHAT: [Same]
2. TESTS: (plural now!)
   - Happy path: [normal case]
   - Edge case 1: [first edge case]
   - Edge case 2: [second edge case]
3. WHAT could go wrong: [Same]
```

### After 1 Month: Add "Why"

```
0. WHY: Why am I building this?
1. WHAT: [Same]
2. TEST: [Same]
3. EDGE: [Same]
```

Understanding "why" helps make better decisions.

### After 2 Months: Add "How"

```
1. WHAT: [Same]
1.5 HOW: What's my approach?
2. TEST: [Same]
3. EDGE: [Same]
```

Plan before coding.

### After 6 Months: Your Own Questions

By now, you've discovered what questions YOU need to ask.

Maybe you add:

- "Who will use this?"
- "How will I debug it?"
- "What dependencies do I need?"

The Three Questions were training wheels. Now you're riding!

## Common Mistakes

### Mistake 1: Skipping the Questions

```
"I'll just start coding, the questions are obvious."
```

Even when "obvious," writing them down forces clarity.

### Mistake 2: Vague Answers

**Vague:**

```
1. WHAT: Make the app better
2. TEST: It should work
3. EDGE: Bad stuff might happen
```

**Specific:**

```
1. WHAT: Add password strength validation to registration
2. TEST: "abc123" should fail, "Abc123!@#" should pass
3. EDGE: What if password is over 1000 characters?
```

### Mistake 3: Answering in Your Head

**Brain:** "I know what I'm building!"

**Reality:** Write it down anyway. You'll be surprised how it clarifies thinking.

### Mistake 4: Not Testing Edge Case

```python
# I wrote code to handle empty strings
# But never actually tested it
# It crashes in production
```

Always test what you identified in Question 3!

## Quick Reference

### The Questions

```
1. WHAT am I building? (1 sentence)
2. HOW will I know it works? (1 test case)
3. WHAT could go wrong? (1 edge case)
```

### The Process

```
Ask questions → Write answers → Code → Test normal case → Test edge case → Done
```

### The Benefits

- ✅ Clear thinking
- ✅ Better code
- ✅ Fewer bugs
- ✅ Easy to maintain
- ✅ Actually simple to follow

## Practice Exercise

Let's practice right now!

**Your task:** Create a function to check if a number is even.

### Answer These

1. **WHAT are you building?**
   *[Write your answer]*

2. **HOW will you know it works?**
   *[Write a specific test]*

3. **WHAT could go wrong?**
   *[Identify an edge case]*

### Now Code It

Try implementing it based on your answers.

### Compare to This

**Sample answers:**

```
1. WHAT: Function that returns True if number is even, False if odd
2. TEST: is_even(4) returns True, is_even(5) returns False
3. EDGE: What if number is 0? Or negative?
```

**Sample code:**

```python
def is_even(n):
    """Check if number is even."""
    # Works for positive, negative, and zero
    return n % 2 == 0

# Tests
assert is_even(4) == True   # From Question 2
assert is_even(5) == False  # From Question 2
assert is_even(0) == True   # Edge case from Question 3
assert is_even(-2) == True  # Edge case from Question 3
print("✓ All tests pass!")
```

## When to Use This Workflow

### Perfect For

- ✅ Learning to code
- ✅ Small functions
- ✅ Quick scripts
- ✅ Side projects
- ✅ Prototypes

### Graduate to More When

- Building production systems
- Working in teams
- Managing complex projects
- Dealing with critical data

Then add: detailed planning, comprehensive tests, code review, etc.

But start here!

## Feeling Stuck?

**If three questions seem like too much:**

- Start with just Question 1
- Add Question 2 next week
- Add Question 3 the week after

**If you can't answer the questions:**

- You're not ready to code yet!
- Research more
- Ask AI for help
- Break problem into smaller pieces

**If it feels too simple:**

- Good! Simple is powerful
- Use it for 2 weeks
- Then add complexity as needed
- Build your own workflow stages *(See [Choosing Stages](choosing-stages.md))*

## Next Steps

Once comfortable with Three Questions:

- **Using AI Assistance** - Add AI tools to your workflow *(See [AI Tools](../02-ai-tools/README.md))*
- **Agent-Assisted Resolution** - Complex problem solving with AI *(See [Agent-Assisted Resolution](../01-github-basics/agent-assisted-resolution.md))*
- **Workflow Evolution** - Grow your process over time *(See [Evolving Your Process](evolving-your-process.md))*

---

**Remember:** Every expert started with something this simple! 🎯
