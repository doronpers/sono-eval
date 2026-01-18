# Pull Request Description Template

Use this template when creating pull requests to clearly communicate your changes.

## Copy This Template

```markdown
## What This PR Does

Brief description of your changes (2-3 sentences)

## Type of Change

- [ ] Bug fix (fixes an issue)
- [ ] New feature (adds functionality)
- [ ] Documentation update
- [ ] Code refactoring (no functional changes)
- [ ] Other (describe):

## Motivation

Why did you make this change? What problem does it solve?

## Changes Made

List the specific changes:
- Changed X to Y
- Added Z feature
- Fixed bug in component A

## How to Test

Steps to verify this works:
1. Run `[command]`
2. Check `[expected result]`
3. Verify `[behavior]`

## Screenshots (if applicable)

[Add screenshots for UI changes]

## Checklist

Before submitting:
- [ ] Code works locally
- [ ] Tests pass (if any)
- [ ] No console errors
- [ ] Code is readable
- [ ] I've tested edge cases
- [ ] Documentation updated (if needed)

## Questions or Concerns

[Any doubts or areas you want reviewers to focus on?]
```

## Why Use This Template?

**For you:**

- Forces you to think through your changes
- Catches issues before review
- Provides documentation for future

**For reviewers:**

- Understand context quickly
- Know what to focus on
- Can test effectively

## Example: Good PR Description

```markdown
## What This PR Does

Adds email validation to the user registration endpoint to prevent invalid emails from being stored in the database.

## Type of Change

- [x] New feature (adds functionality)

## Motivation

Users were able to register with invalid emails like "notanemail" which caused issues when we tried to send them confirmation emails. This resulted in support tickets and a poor user experience.

## Changes Made

- Added Pydantic EmailStr validation to User model
- Added error message for invalid emails
- Added test cases for email validation
- Updated API documentation with validation rules

## How to Test

1. Start the server: `python main.py`
2. Try to register with invalid email:
   ```bash
   curl -X POST http://localhost:8000/register \
     -d '{"email": "notanemail", "name": "Test"}'
   ```

3. Should return 422 error with message about invalid email
4. Try with valid email - should work normally

## Checklist

- [x] Code works locally
- [x] Tests pass (added 3 new tests)
- [x] No console errors
- [x] Code is readable
- [x] I've tested edge cases (empty string, @ only, etc.)
- [x] Documentation updated (API docs show email format)

## Questions or Concerns

Should we also check if the email domain exists? I didn't add that yet because it might slow down registration. Happy to add if you think it's important.

```

## Example: Bad PR Description

```markdown
## What This PR Does

Fixed stuff

## Changes Made

- Updated things
- Made it better

## How to Test

Just test it
```

**Problems:**

- Vague description
- No context
- Reviewer doesn't know what to test
- Future developers won't understand why changes were made

## Adapting for Different Situations

### For Small Changes

You can simplify:

```markdown
## What This PR Does

Fixed typo in README.md: "Helo" → "Hello"

## Type of Change

- [x] Documentation update
```

That's enough for trivial changes!

### For Large Features

Expand sections:

```markdown
## What This PR Does

[Detailed description with background]

## Architecture Changes

[How this fits into the system]

## Database Changes

[Any schema changes or migrations]

## Security Considerations

[Security implications reviewed]

## Performance Impact

[Any performance implications]
```

### For Bug Fixes

Add specific sections:

```markdown
## What This PR Does

Fixes bug where users couldn't delete their accounts

## Bug Description

- **What was broken:** Delete button did nothing
- **Error seen:** 500 Internal Server Error
- **Root cause:** Database constraint not handled

## The Fix

Added proper error handling for foreign key constraints...

## Verification

Tested with:
- User with no data: ✓ Deletes successfully
- User with posts: ✓ Deletes cascade works
- User with active session: ✓ Handles gracefully
```

## Tips for Great PR Descriptions

### Do

✅ Write for someone who doesn't know the context
✅ Explain the "why" not just the "what"
✅ Include steps to test
✅ Link to related issues or docs
✅ Mention any risks or concerns

### Don't

❌ Assume reviewers know the context
❌ Just list file names changed
❌ Skip the testing instructions
❌ Make reviewers guess what to check
❌ Leave concerns unspoken

## When Working with AI

**Good prompt to generate PR description:**

```
I made these changes:
[paste git diff or describe changes]

Create a pull request description following this template:
[paste template]

Focus on:
- Clear explanation of what changed and why
- How to test it
- Any concerns reviewers should know about
```

**AI can help:**

- Write clear descriptions
- Identify what needs testing
- Spot potential issues
- Suggest improvements

**But you should:**

- Review and edit AI output
- Add your own context
- Ensure accuracy
- Personalize it

## Common Mistakes

### Mistake 1: Too Vague

"Updated the code"

**Fix:** Specific details
"Added input validation to prevent SQL injection in the login form"

### Mistake 2: Too Technical

"Refactored AbstractFactoryBean to use dependency injection with IoC container"

**Fix:** Explain like teaching
"Reorganized how components connect to make the code easier to test and modify"

### Mistake 3: Missing Context

Just listing changes without explaining why

**Fix:** Always include motivation
"Users reported this error often, so I added validation to prevent it"

### Mistake 4: No Testing Instructions

"Test it and make sure it works"

**Fix:** Specific steps
"1. Do X, 2. Check Y appears, 3. Verify Z behavior"

## Saving This Template

**In your repository:**
Create `.github/PULL_REQUEST_TEMPLATE.md` with this content, and GitHub will automatically use it for new PRs!

**As a personal file:**
Save it somewhere you can copy-paste when needed.

**As a snippet:**
Set up a code snippet in your editor to insert it quickly.

## Review Your Own Description

Before submitting, ask:

- [ ] Could someone understand this without asking me?
- [ ] Are the testing steps clear enough?
- [ ] Did I explain why, not just what?
- [ ] Would this help me in 6 months when I've forgotten the context?

If you answer "no" to any, improve it!

---

**A great PR description saves everyone time and makes collaboration smoother!** 📝
