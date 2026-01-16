# Pull Requests Explained

Pull Requests (PRs) are how developers collaborate on code. Let's make them less mysterious.

## What Is a Pull Request?

### The Simple Version

A Pull Request is asking: **"Can I merge my changes into the main code?"**

It's like:

- Proposing edits to a shared document
- Submitting homework for review
- Asking "Does this look good?" before making it official

### Not Actually "Pulling"

The name is confusing! You're not pulling anything - you're **requesting** that someone pull your changes into their code.

Better mental model: "Merge Request" (that's what GitLab calls it).

## Why Pull Requests Matter

### 1. Code Review

Someone looks at your changes before they're merged:

- Catch bugs early
- Share knowledge
- Maintain quality
- Learn from feedback

### 2. Discussion

Team members can:

- Comment on specific lines
- Ask questions
- Suggest improvements
- Explain decisions

### 3. Documentation

PRs create a record:

- Why a change was made
- Who reviewed it
- What was discussed
- When it was merged

## Anatomy of a Pull Request

Every PR has:

### Title

```
Add user authentication with JWT tokens
```

Clear, concise description of what it does.

### Description

```markdown
## What This Does
- Adds login/logout endpoints
- Implements JWT token generation
- Adds authentication middleware

## Why
Users need to log in to access protected features.

## How to Test
1. Run the server
2. POST to /login with valid credentials
3. Copy the token
4. Use token in Authorization header
```

### Changed Files

A list of every file you modified, with:

- Green lines (additions)
- Red lines (deletions)
- Side-by-side comparison

### Conversation Thread

Comments, questions, and discussion from reviewers.

### Checks/Tests

Automated tests that run on your code:

- ✅ Tests passing
- ✅ Code style checks
- ✅ Security scans

## The Pull Request Workflow

### Step 1: You Create a Branch

```bash
git checkout -b feature/user-profile
```

### Step 2: You Make Changes

```bash
# Write code...
git add .
git commit -m "Add user profile page"
git push origin feature/user-profile
```

### Step 3: You Open a PR on GitHub

1. Go to your repo on GitHub
2. Click "Pull Requests" → "New Pull Request"
3. Select your branch
4. Fill in title and description
5. Click "Create Pull Request"

### Step 4: Others Review

Reviewers:

- Read your code
- Test it locally
- Leave comments
- Approve or request changes

### Step 5: You Address Feedback

```bash
# Make requested changes...
git add .
git commit -m "Address review feedback"
git push origin feature/user-profile
```

The PR updates automatically!

### Step 6: Someone Merges It

Once approved:

- Click "Merge Pull Request"
- Your changes are now in main
- Your branch can be deleted

## Writing Great PR Descriptions

### The Template

```markdown
## What
Brief description of the change

## Why
Why this change is necessary

## How
Technical approach or key decisions

## Testing
How to verify it works

## Screenshots (if UI)
Before/after images

## Related Issues
Fixes #123
```

### Example: Good PR Description

```markdown
## What
Add password reset functionality

## Why
Users can't access their accounts if they forget their password

## How
- New /reset-password endpoint
- Sends email with temporary token
- Token expires after 1 hour
- Updates password in database

## Testing
1. Click "Forgot Password" on login page
2. Enter your email
3. Check email for reset link
4. Click link and enter new password
5. Log in with new password

## Related
Fixes #45
```

### Example: Too Brief

```markdown
update code
```

❌ Tells reviewers nothing.

## Types of Pull Requests

### Feature PR

Adding new functionality:

```
feat: Add dark mode toggle
```

### Bug Fix PR

Fixing something broken:

```
fix: Prevent crash when user enters invalid email
```

### Refactor PR

Improving code without changing behavior:

```
refactor: Simplify database query logic
```

### Documentation PR

Updating docs:

```
docs: Add API authentication examples
```

### Hot Fix PR

Urgent fix for production:

```
hotfix: Patch security vulnerability
```

## Code Review: The Other Side

When YOU review someone's PR:

### What to Look For

- **Does it work?** Test it locally
- **Does it make sense?** Understand the logic
- **Is it tested?** Check for test coverage
- **Is it secure?** Look for vulnerabilities
- **Is it maintainable?** Will future devs understand?

### How to Give Feedback

**Good feedback:**
✅ "Consider using a for loop here for better readability"
✅ "What happens if the user input is null?"
✅ "Nice solution! Have you thought about edge case X?"
✅ "This could be simplified by using the utility function"

**Not-so-good feedback:**
❌ "This is wrong" (not helpful)
❌ "I would never do it this way" (subjective)
❌ "Did you even test this?" (condescending)
❌ Nitpicking spaces and formatting (let linters handle it)

### Review Types

**Approve** ✅ - Looks good, ready to merge

**Request Changes** 🔄 - Needs fixes before merging

**Comment** 💬 - Thoughts/questions, but not blocking

## GitHub PR Features

### Inline Comments

Click on a line number to add a comment right there:

```python
def calculate_total(items):
    return sum(item.price for item in items)  # 💬 "What if items is empty?"
```

### Suggested Changes

Reviewers can propose code directly:

```diff
- if (user == null) return
+ if (!user) return
```

You can accept with one click!

### Draft PRs

Mark PR as "Draft" while still working on it:

- Shows it's not ready for review
- Still runs automated tests
- Can request early feedback

### Auto-Merge

Once approved, automatically merge when tests pass.

### Required Reviews

Repo settings can require:

- 1+ approvals before merging
- Specific reviewers
- Passing tests

## Common Scenarios

### Scenario 1: Merge Conflicts

```
× Conflict in src/main.py
```

**What happened:**
Someone else changed the same lines you did.

**How to fix:**

1. Pull the latest main branch
2. Merge main into your branch
3. Manually fix conflicts
4. Commit and push

See [When Things Break](when-things-break.md) for details.

### Scenario 2: Failing Tests

```
× Tests failed: 3 failed, 10 passed
```

**What to do:**

1. Check which tests failed
2. Run tests locally
3. Fix the issues
4. Commit and push fixes

### Scenario 3: Stale PR

Your PR has been open for weeks, main branch has moved on.

**What to do:**

1. Update your branch with latest main
2. Re-test everything
3. Ask reviewers to re-review

## The Social Side

### Etiquette Tips

**As author:**

- Respond to all comments (even if just "done")
- Say thank you for reviews
- Don't take criticism personally
- Explain your reasoning if you disagree

**As reviewer:**

- Be kind and constructive
- Explain the "why" behind suggestions
- Recognize good work
- Remember: code review is about the code, not the person

### Response Time

- **Small PRs:** Hours to 1 day
- **Large PRs:** 2-3 days
- **Urgent fixes:** ASAP

If your PR sits for a week, politely ping reviewers.

## Tips for Easier Reviews

### Keep PRs Small

**Good:**

- 50-200 lines changed
- One clear purpose
- Easy to understand

**Hard to Review:**

- 1000+ lines changed
- Multiple unrelated changes
- Requires hours to understand

Break big changes into smaller PRs.

### Explain Trade-offs

```markdown
## Decisions

I chose approach A over B because:
- A is simpler (more maintainable)
- B would be faster but more complex
- We can optimize later if needed
```

Helps reviewers understand your thinking.

### Add Screenshots

For UI changes, include before/after images. Worth 1000 words.

## Feeling Stuck?

**If PRs seem intimidating:**

- Start by reviewing others' PRs (read-only)
- Make a tiny PR (fix a typo)
- Remember: PRs are conversations, not tests
- Everyone's first PR was scary

**If your PR gets lots of feedback:**

- Good! It means people care about the code
- Each comment is a learning opportunity
- Address each one, even if just "done"
- Don't rush - quality over speed

**If you don't know how to respond to feedback:**

- Ask questions! "Can you show me an example?"
- Ask AI: "How do I implement [suggestion]?"
- Say "I'm not sure I understand, can you explain more?"

## Next Steps

Now that you understand PRs:

- **[First 10 Minutes](first-10-minutes.md)** - Try creating one
- **[Common Mistakes](common-mistakes.md)** - Avoid pitfalls
- **[When Things Break](when-things-break.md)** - Fix conflicts

Ready to practice?
→ **[Exercises: GitHub Fundamentals](../../exercises/github-fundamentals/04-pull-requests.md)**

---

**Remember:** PRs are collaboration tools, not judgment. Everyone learns together! 🤝
