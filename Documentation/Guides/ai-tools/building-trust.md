# Building Trust with AI

How to know when to trust AI suggestions, when to verify, and when to ignore them completely.

## The Trust Spectrum

```
Always Verify ←―――――――――――――――――――→ Usually Trust
    ↑                                      ↑
Security code                      Boilerplate
Database queries                   Standard patterns
Critical logic                     Code formatting
```

## Trust Levels by Task

### Level 1: Trust and Use Immediately

**When:**

- Generating boilerplate code
- Standard patterns you recognize
- Formatting and style
- Simple utility functions
- Test data generation

**Example:**

```python
# AI suggests standard FastAPI endpoint structure
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

# ✅ This is standard - trust it
```

**Why Trust:**

- Well-established patterns
- Low risk if wrong
- Easy to spot issues
- Non-critical functionality

### Level 2: Review Then Use

**When:**

- Business logic implementation
- Data transformations
- API integrations
- File operations
- Most day-to-day code

**Example:**

```python
# AI suggests:
def calculate_discount(price, user_type):
    if user_type == "premium":
        return price * 0.9
    return price

# 🔍 Review:
# - Is discount correct? (10% seems reasonable)
# - What about other user types?
# - Should premium be hardcoded?
```

**How to Review:**

1. Read through the code
2. Check logic makes sense
3. Consider edge cases
4. Verify against requirements
5. Test with examples

### Level 3: Verify Before Using

**When:**

- Security-related code
- Database queries
- Authentication/authorization
- Input validation
- Error handling

**Example:**

```python
# AI suggests:
def login(username, password):
    user = db.execute(f"SELECT * FROM users WHERE username='{username}'")
    if user and user.password == password:
        return "Login successful"
    return "Login failed"

# ⚠️ VERIFY:
# - SQL injection vulnerability!
# - Password not hashed!
# - No rate limiting!
# - Timing attack possible!
```

**How to Verify:**

1. Check for security vulnerabilities
2. Verify against security best practices
3. Test with malicious inputs
4. Cross-reference with security docs
5. Run security scanners

### Level 4: Research and Understand

**When:**

- Algorithms you don't know
- Complex architectural patterns
- Performance-critical code
- Concurrency/async code
- System-level operations

**Example:**

```python
# AI suggests caching strategy:
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_computation(n):
    # ...

# 🔬 RESEARCH:
# - What is lru_cache?
# - Is 128 the right size for my use case?
# - Thread-safe?
# - How long are cached values kept?
# - What happens when cache is full?
```

**How to Research:**

1. Ask AI to explain in detail
2. Read official documentation
3. Look at examples from trusted sources
4. Understand the trade-offs
5. Test thoroughly

### Level 5: Don't Trust - Rebuild

**When:**

- AI gives obviously wrong answer
- Code doesn't match requirements
- Suggests deprecated approaches
- Over-engineered solutions
- Missing critical functionality

**Example:**

```python
# You asked: "Simple email validation"
# AI provides: [200 lines of complex regex and edge cases]

# 🚫 DON'T USE - Too complex
# Rebuild:
def validate_email(email):
    return "@" in email and "." in email and len(email) > 5
```

**When to Rebuild:**

- Solution is over-complicated
- Doesn't meet requirements
- Uses deprecated libraries
- Introduces unnecessary dependencies

## Red Flags: When NOT to Trust

### 🚩 Flag 1: Vague Variable Names

```python
# AI suggests:
def process(x, y):
    result = x + y
    return result

# Red flag: What are x and y? What's being processed?
```

### 🚩 Flag 2: No Error Handling

```python
# AI suggests:
def divide(a, b):
    return a / b

# Red flag: What if b is 0?
```

### 🚩 Flag 3: Hardcoded Values

```python
# AI suggests:
api_key = "sk-1234567890"
max_retries = 3

# Red flag: Should be in config/environment
```

### 🚩 Flag 4: SQL Concatenation

```python
# AI suggests:
query = f"SELECT * FROM users WHERE id = {user_id}"

# Red flag: SQL injection vulnerability!
```

### 🚩 Flag 5: Bare Except

```python
# AI suggests:
try:
    risky_operation()
except:  # Red flag: Catches everything!
    pass
```

### 🚩 Flag 6: No Type Hints (in Python)

```python
# AI suggests:
def calculate(value):
    return value * 2

# Red flag: What type is value? What's returned?
```

### 🚩 Flag 7: Ignoring Return Values

```python
# AI suggests:
save_to_database(user)  # What if this fails?
send_email(user.email)  # No error checking
```

### 🚩 Flag 8: Mysterious Algorithms

```python
# AI suggests:
def mystery_function(data):
    return [x for x in data if x & 0xFF00 >> 8]

# Red flag: What is this even doing?
```

## Green Flags: When TO Trust

### ✅ Flag 1: Clear, Descriptive Names

```python
def validate_user_email_format(email: str) -> bool:
    return "@" in email and "." in email
```

### ✅ Flag 2: Proper Error Handling

```python
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

### ✅ Flag 3: Type Hints Included

```python
def calculate_total(prices: List[float]) -> float:
    return sum(prices)
```

### ✅ Flag 4: Comprehensive Comments

```python
def process_payment(amount: float) -> bool:
    """
    Process a payment transaction.

    Args:
        amount: Payment amount in USD

    Returns:
        True if successful, False otherwise

    Raises:
        ValueError: If amount is negative
    """
```

### ✅ Flag 5: Standard Patterns

```python
# Context manager pattern
with open('file.txt', 'r') as f:
    data = f.read()
# File automatically closed
```

### ✅ Flag 6: Parameterized Queries

```python
# Safe from SQL injection
cursor.execute(
    "SELECT * FROM users WHERE id = %s",
    (user_id,)
)
```

## Building Your Trust Radar

### Phase 1: Question Everything

**Week 1-4 of using AI:**

- Verify every suggestion
- Ask AI to explain each line
- Test extensively
- Compare with documentation
- Build pattern recognition

**Goal:** Learn what good code looks like

### Phase 2: Spot the Patterns

**Month 2-3:**

- Recognize common AI mistakes
- Trust standard patterns
- Quickly identify red flags
- Verify only risky parts
- Faster review process

**Goal:** Efficient evaluation

### Phase 3: Informed Trust

**Month 4+:**

- Trust routine code immediately
- Deep dive on critical code
- Catch subtle issues
- Guide AI away from mistakes
- Confident code review

**Goal:** Productive collaboration

## Verification Checklist

### For Every AI Suggestion

**Quick Check (30 seconds):**

- [ ] Do I understand what this code does?
- [ ] Are there obvious red flags?
- [ ] Does it match what I asked for?

**Standard Review (2-5 minutes):**

- [ ] Read through each line
- [ ] Check for error handling
- [ ] Verify edge cases considered
- [ ] Test with example data
- [ ] Check for security issues

**Deep Verification (10-30 minutes):**

- [ ] Understand the algorithm
- [ ] Research unfamiliar patterns
- [ ] Test comprehensive edge cases
- [ ] Review security implications
- [ ] Check performance characteristics
- [ ] Verify against official docs

### Security-Specific Checklist

For any security-related code:

- [ ] No SQL injection vulnerabilities
- [ ] Input validation present
- [ ] Authentication checked
- [ ] Authorization enforced
- [ ] Secrets not hardcoded
- [ ] Error messages don't leak info
- [ ] Rate limiting considered
- [ ] HTTPS/encryption used
- [ ] Passwords properly hashed
- [ ] XSS prevented

## Trust But Verify: Real Examples

### Example 1: Email Validation

**AI Suggests:**

```python
import re

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```

**Your Review:**
✅ Regex looks reasonable
✅ Returns boolean
✅ No security issues
❓ Does it handle all edge cases?

**Verify:**

```python
# Test it
assert validate_email("test@example.com") == True
assert validate_email("invalid") == False
assert validate_email("test@.com") == False  # Edge case
```

**Decision:** Trust with minor testing

### Example 2: Database Query

**AI Suggests:**

```python
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)
```

**Your Review:**
🚩 SQL injection vulnerability!
🚩 No error handling
🚩 Returns raw database object

**Fix:**

```python
def get_user(user_id: int) -> Optional[User]:
    try:
        query = "SELECT * FROM users WHERE id = %s"
        result = db.execute(query, (user_id,))
        return User.from_db(result) if result else None
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise
```

**Decision:** Don't trust - rebuild with security in mind

### Example 3: Async Function

**AI Suggests:**

```python
import asyncio

async def fetch_data(urls):
    tasks = [asyncio.create_task(fetch_url(url)) for url in urls]
    return await asyncio.gather(*tasks)
```

**Your Review:**
✅ Standard async pattern
❓ I don't fully understand asyncio.gather

**Research:**

- Read asyncio.gather docs
- Understand what happens if one task fails
- Learn about return_exceptions parameter

**Test:**

```python
# Test with various scenarios
urls = ["http://example.com", "invalid-url"]
result = await fetch_data(urls)
```

**Decision:** Research, understand, then trust

## When Experts Still Verify

Even experienced developers verify AI suggestions for:

1. **Security code** - Always verify
2. **Performance-critical paths** - Measure, don't guess
3. **Unfamiliar domains** - Research before trusting
4. **Complex algorithms** - Verify correctness
5. **API integrations** - Check against docs

## Building Long-Term Trust

### Keep a Learning Journal

Track AI suggestions:

```markdown
## Date: 2024-12-16
**AI Suggested:** [code]
**Issue Found:** [problem]
**Lesson:** [what I learned]

## Date: 2024-12-17
**AI Suggested:** [code]
**Worked Great:** [why it was good]
**Pattern:** [what to trust in future]
```

### Pattern Recognition

After a few months, you'll notice:

- AI always misses this edge case
- AI's error handling is usually incomplete
- AI's security suggestions need review
- AI's standard patterns are reliable

### Calibrate Continuously

- Adjust trust based on experience
- Learn from mistakes (yours and AI's)
- Share learnings with team
- Update your mental checklist

## Feeling Stuck?

**If you don't know whether to trust:**

- Start with verification
- Build trust gradually
- When in doubt, verify
- Better safe than sorry

**If you're too skeptical:**

- You'll slow down unnecessarily
- Trust routine patterns
- Use verification checklist
- Build confidence over time

**If you're too trusting:**

- You'll commit bugs
- Start verifying more
- Learn common AI mistakes
- Remember: you're responsible

## Next Steps

Now you understand trust:

- **[Discovery Exercises](discovery-exercises.md)** - Practice evaluation
- **[Workflow Building](../../03-workflow-building/README.md)** - Integrate AI safely
- **Examples**: See [tex-assist-coding examples](https://github.com/doronpers/tex-assist-coding/tree/main/examples) for project ideas

---

**Remember:** Trust is earned through experience, not given blindly! 🔐
