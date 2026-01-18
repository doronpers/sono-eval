# Stages of Development

Understanding the stages of software development helps you build better workflows. Let's break down each stage in beginner-friendly terms.

## The Development Lifecycle

```
Idea → Plan → Build → Test → Review → Deploy → Learn
  ↑                                              ↓
  └──────────────── Iterate ←───────────────────┘
```

## Stage 1: Planning

**What it is:** Figuring out what you're going to build before you write code.

### Why Plan?

Without planning:

```
"I'll just start coding and figure it out..."
[2 hours later]
"Wait, what was I trying to do?"
```

With planning:

```
Clear requirements → Focused coding → Better results
```

### Planning Activities

**Minimal (5 minutes):**

- Answer the Three Questions
- Sketch basic approach
- Identify main components

**Moderate (15-30 minutes):**

- Write detailed requirements
- List all features
- Identify dependencies
- Consider edge cases
- Plan error handling

**Thorough (1+ hours):**

- Architecture diagrams
- Database schema design
- API contract design
- Security considerations
- Performance requirements
- Scalability planning

### Planning with AI

**Good prompts:**

```
"Help me plan a [feature]. What should I consider?"

"I want to build [description]. What's a good approach?"

"Break down [complex feature] into smaller tasks"
```

**Example:**

```
You: "Help me plan a user registration system. What should I consider?"

AI: "Here's what to think about:
1. Data collection: What fields (email, password, name?)
2. Validation: Email format, password strength
3. Storage: Database schema for users
4. Security: Password hashing, SQL injection prevention
5. Errors: Duplicate email handling
6. Confirmation: Email verification?
7. Success: What happens after registration?

Would you like help with any of these?"
```

### Planning Outputs

**Document your plan:**

```markdown
## Feature: User Registration

### Requirements
- Accept email and password
- Validate email format
- Require password min 8 characters
- Check for duplicate emails
- Hash passwords before storing
- Return success/error message

### Components Needed
- API endpoint: POST /register
- Validation function
- Database user table
- Password hashing utility

### Edge Cases
- Email already registered
- Invalid email format
- Weak password
- Database connection failure
```

### When to Skip Planning

**OK to skip detailed planning for:**

- Learning exercises
- Tiny scripts
- Quick experiments
- Throwaway prototypes

**Never skip planning for:**

- Production code
- Team projects
- Complex features
- Critical systems

## Stage 2: Building

**What it is:** Writing the actual code.

### Building Approaches

**Approach 1: Top-Down**

```
Start with high-level structure → Fill in details
```

**Example:**

```python
# First: Write the structure
def register_user(email, password):
    validate_email(email)
    validate_password(password)
    check_duplicate(email)
    save_user(email, password)
    return success_response()

# Later: Implement each function
```

**Approach 2: Bottom-Up**

```
Build small pieces → Combine them
```

**Example:**

```python
# First: Build helper functions
def is_valid_email(email):
    return '@' in email and '.' in email

def is_strong_password(password):
    return len(password) >= 8

# Later: Combine into main function
def register_user(email, password):
    if not is_valid_email(email):
        return error("Invalid email")
    if not is_strong_password(password):
        return error("Weak password")
    # ...
```

**Approach 3: Test-Driven (TDD)**

```
Write test → Write code to pass test → Refactor → Repeat
```

**Example:**

```python
# First: Write the test
def test_register_user():
    result = register_user("test@example.com", "Password123")
    assert result["success"] == True

# Then: Write code until test passes
def register_user(email, password):
    # Implementation here
    return {"success": True}
```

### Building with AI

**Single-agent approach:**

```
You: "Create a user registration function in Python with
email validation and password hashing"

AI: [generates complete code]

You: Review and test
```

**Iterative approach:**

```
You: "Create basic user registration function"
AI: [generates basic version]

You: "Add email validation"
AI: [adds validation]

You: "Add password hashing"
AI: [adds hashing]

You: "Add error handling"
AI: [adds error handling]
```

**Multi-agent approach:**

```
Agent 1 (Copilot): Generate code as you type
Agent 2 (ChatGPT): Explain complex parts
Agent 3 (Claude): Review for security issues
```

### Building Best Practices

**1. Commit frequently:**

```bash
git add .
git commit -m "Add email validation"
# Code more
git commit -m "Add password hashing"
# Code more
git commit -m "Add error handling"
```

**2. Keep functions small:**

```python
# Bad: One giant function doing everything
def do_everything():
    # 200 lines of code

# Good: Many small focused functions
def validate_input():
    # 10 lines

def process_data():
    # 15 lines

def save_results():
    # 12 lines
```

**3. Document as you go:**

```python
def register_user(email: str, password: str) -> dict:
    """
    Register a new user with email and password.

    Args:
        email: User's email address
        password: User's chosen password (will be hashed)

    Returns:
        Dict with 'success' boolean and 'user_id' or 'error'

    Raises:
        ValueError: If email or password invalid
    """
    # Implementation
```

## Stage 3: Testing

**What it is:** Verifying your code actually works.

### Testing Levels

**Level 1: Manual Testing**

```python
# Just run it and see what happens
result = my_function(test_input)
print(result)
```

**Pros:** Quick, no setup
**Cons:** Can't automate, easy to miss cases

**Level 2: Automated Testing**

```python
def test_my_function():
    result = my_function(test_input)
    assert result == expected_output
```

**Pros:** Repeatable, catches regressions
**Cons:** Takes time to write

**Level 3: Comprehensive Testing**

```python
# Test normal cases
# Test edge cases
# Test error handling
# Test performance
# Test security
```

### Types of Tests

**Unit Tests** - Test individual functions

```python
def test_validate_email():
    assert validate_email("test@example.com") == True
    assert validate_email("invalid") == False
    assert validate_email("") == False
```

**Integration Tests** - Test components working together

```python
def test_user_registration_flow():
    # Test the whole registration process
    result = register_user("test@example.com", "Pass123")
    assert result["success"] == True
    assert user_exists_in_db("test@example.com")
```

**End-to-End Tests** - Test the complete system

```python
def test_complete_user_journey():
    # Register
    register_result = api_client.post("/register", data)
    # Login
    login_result = api_client.post("/login", credentials)
    # Access protected resource
    profile_result = api_client.get("/profile")
    # All should succeed
```

### Testing with AI

**Generate tests:**

```
You: "Create unit tests for this function:
[paste your function]"

AI: [generates comprehensive tests]
```

**Generate test data:**

```
You: "Generate 10 different email addresses for testing,
including valid and invalid examples"

AI: [generates test data]
```

**Identify missing tests:**

```
You: "What test cases am I missing for this code?
[paste your code and tests]"

AI: "You should also test:
- Empty string input
- Very long input (1000+ characters)
- Special characters in email
- SQL injection attempts
- Unicode characters"
```

## Stage 4: Review

**What it is:** Checking code quality before considering it "done".

### What to Review

**Functionality:**

- ✅ Does it work as intended?
- ✅ Are all requirements met?
- ✅ Are edge cases handled?

**Code Quality:**

- ✅ Is it readable?
- ✅ Are names clear?
- ✅ Is it properly documented?
- ✅ Is there duplication?

**Security:**

- ✅ Is user input validated?
- ✅ Are passwords hashed?
- ✅ Is SQL injection prevented?
- ✅ Are secrets kept out of code?

**Performance:**

- ✅ Will it be fast enough?
- ✅ Are there obvious inefficiencies?
- ✅ Does it handle scale?

### Review Methods

**Self-Review:**

```
1. Walk away for 30 minutes
2. Come back with fresh eyes
3. Read your code as if you didn't write it
4. Look for issues
```

**AI Review:**

```
You: "Review this code for bugs, security issues,
and improvements:
[paste code]"

AI: [provides detailed review with suggestions]
```

**Peer Review:**

```
1. Create pull request
2. Ask colleague to review
3. Discuss feedback
4. Make improvements
```

### Review Checklist

```markdown
- [ ] Code works correctly
- [ ] All tests pass
- [ ] Edge cases handled
- [ ] Errors handled gracefully
- [ ] Code is readable
- [ ] Functions are small
- [ ] Names are clear
- [ ] Comments explain why, not what
- [ ] No secrets in code
- [ ] Security best practices followed
- [ ] Performance acceptable
- [ ] Documentation updated
```

## Stage 5: Deploy

**What it is:** Making your code available for use.

### Deployment Levels

**Level 1: Local**

```bash
python main.py
# Runs on your computer only
```

**Level 2: Shared Server**

```bash
# Deploy to a server where others can access it
# Example: Deploy to Railway, Heroku, Render
```

**Level 3: Production**

```bash
# Full production deployment with:
# - Load balancing
# - Auto-scaling
# - Monitoring
# - Backups
# - CI/CD pipeline
```

### Deployment Considerations

**Before deploying:**

- ✅ All tests pass
- ✅ Code reviewed
- ✅ Security checked
- ✅ Performance tested
- ✅ Documentation complete
- ✅ Rollback plan ready

**Deployment checklist:**

```markdown
- [ ] Environment variables set
- [ ] Dependencies installed
- [ ] Database migrations run
- [ ] Health checks configured
- [ ] Logs configured
- [ ] Monitoring set up
- [ ] Backups enabled
- [ ] SSL/HTTPS enabled
```

## Stage 6: Learn

**What it is:** Reflecting on what worked and what didn't.

### Learning Activities

**After every project:**

```markdown
## What Went Well
- Clear requirements saved time
- AI helped with boilerplate
- Tests caught bugs early

## What Could Improve
- Spent too long on perfect code
- Didn't consider scalability
- Should have asked for help sooner

## Next Time
- Use simpler approach first
- Think about scale earlier
- Pair program for complex parts
```

**Track your growth:**

```markdown
## Month 1
- Can build simple APIs
- Understanding basic patterns
- Still struggle with error handling

## Month 2
- Error handling improved
- Can use GitHub confidently
- Learning test-driven development

## Month 3
- TDD feels natural now
- Can review others' code
- Starting to see design patterns
```

## Combining Stages

### Quick Projects (Minutes)

```
Plan (2 min) → Build (10 min) → Test (3 min) → Done
```

### Small Projects (Hours)

```
Plan (15 min) → Build (2 hrs) → Test (30 min) → Review (15 min) → Deploy
```

### Real Projects (Days/Weeks)

```
Plan → Build → Test → Review → Deploy
  ↓      ↓      ↓      ↓       ↓
Iterate multiple times before done
```

### Production Projects (Weeks/Months)

```
Design → Plan → Build → Test → Review → Security → Performance → Deploy → Monitor → Learn
```

## Customizing Your Stages

### You Might Add

- **Research** stage before planning
- **Design** stage for UI work
- **Documentation** stage
- **Performance testing** stage
- **Security audit** stage

### You Might Skip

- Review for personal projects
- Automated tests for one-off scripts
- Deployment for local tools

### You Might Split

- **Build** into: Structure + Implementation + Refactor
- **Test** into: Unit + Integration + E2E
- **Review** into: Self + AI + Peer

## Common Questions

### "Do I need all these stages?"

No! Start simple:

- Learning: Plan → Build → Test
- Side projects: Plan → Build → Test → Review
- Production: All stages

### "How long should each stage take?"

Depends on project size:

- Tiny: Minutes each
- Small: 15-30 minutes each
- Medium: Hours each
- Large: Days each

### "Can stages overlap?"

Yes! In practice:

- Test while building
- Review while testing
- Learn while building

Stages are guidelines, not rules.

### "What if I skip a stage?"

**Planning:** You'll get stuck or build the wrong thing
**Testing:** Bugs will surprise you in production
**Review:** Quality issues will pile up
**Deployment:** Your code won't be useful to others
**Learning:** You'll repeat the same mistakes

## Next Steps

**Understand your stages:**
→ **[Using AI in Your Workflow](using-ai-in-workflow.md)** - AI assistance for each stage

**Choose what you need:**
→ **[Choosing Stages](choosing-stages.md)** - Customize your workflow

**See examples:**
→ **[Workflow Examples](workflow-examples.md)** - Complete workflow walkthroughs

---

**Remember:** These stages exist to help you, not burden you. Start simple and add stages as needed! 🚀
