# Common Mistakes (And How to Avoid Them)

Everyone makes these mistakes when learning GitHub. Let's learn from them together!

## The Big Picture

**Good news:** Most "mistakes" in Git are reversible.
**Better news:** After making each mistake once, you'll never make it again.
**Best news:** We're going to show you how to avoid them in the first place.

## Mistake 1: Committing to the Wrong Branch

### What Happens

You're on the `main` branch and make changes, but you meant to create a feature branch first.

### Why It Happens

You forget to create/switch branches before coding.

### How to Avoid

**Before you start coding:**

```bash
# Check which branch you're on
git branch

# Create and switch to new branch
git checkout -b feature/your-feature
```

### How to Fix If It Happens

**If you haven't committed yet:**

```bash
# Stash your changes
git stash

# Create and switch to correct branch
git checkout -b feature/your-feature

# Restore your changes
git stash pop
```

**If you already committed:**

```bash
# Create new branch from current position
git checkout -b feature/your-feature

# Go back to main
git checkout main

# Remove the last commit from main (but keep the changes in your feature branch)
git reset --hard HEAD~1
```

## Mistake 2: Forgetting to Pull Before Pushing

### What Happens

You try to push, and Git says:

```
! [rejected] main -> main (non-fast-forward)
```

### Why It Happens

Someone else pushed changes while you were working. Your local copy is outdated.

### How to Avoid

**Before you start working each day:**

```bash
git pull
```

**Or use this workflow:**

```bash
# Always pull before you start
git checkout main
git pull origin main

# Then create your branch
git checkout -b feature/new-stuff
```

### How to Fix

```bash
# Pull the latest changes
git pull origin main

# If there are conflicts, resolve them
# Then commit and push
git push origin main
```

## Mistake 3: Committing Secrets or Passwords

### What Happens

You accidentally commit:

- API keys
- Passwords
- `.env` files with secrets
- Database credentials

**⚠️ This is serious!** Even if you delete the commit, it's in the history.

### How to Avoid

**Before your first commit:**

1. **Create a `.gitignore` file:**

```
.env
.env.local
secrets.json
config/database.yml
*.key
*.pem
```

2. **Use environment variables:**

```python
# Don't do this:
api_key = "sk-1234567890"

# Do this:
import os
api_key = os.getenv("API_KEY")
```

3. **Double-check before committing:**

```bash
# See what you're about to commit
git diff --staged
```

### How to Fix If It Happens

**If you haven't pushed yet:**

```bash
# Remove the file from staging
git reset HEAD .env

# Add to .gitignore
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Add .env to gitignore"
```

**If you already pushed:**

1. **Rotate the secret immediately** (change the password/key)
2. Remove from history (complex - see [When Things Break](when-things-break.md))
3. Consider the secret compromised

## Mistake 4: Too-Large or Too-Small Commits

### What Happens

**Too Large:**

```
Changed 50 files, 3000 lines
Commit message: "Updates"
```

Impossible to review or understand.

**Too Small:**

```
Commit 1: "Add f"
Commit 2: "Add u"
Commit 3: "Add n"
Commit 4: "Add c"
```

Annoying commit history.

### How to Avoid

**Good commit size:**

- One logical unit of work
- 50-200 lines typically
- Can be described in one sentence

**Examples of good commits:**

- "Add user authentication endpoint"
- "Fix crash when email field is empty"
- "Refactor database queries for performance"

### Guidelines

```bash
# See what you're committing
git diff

# Commit related changes together
git add src/auth.py src/models.py
git commit -m "Add authentication models"

# Commit unrelated changes separately
git add src/homepage.py
git commit -m "Update homepage styling"
```

## Mistake 5: Vague Commit Messages

### What Happens

```
git commit -m "fix"
git commit -m "update"
git commit -m "changes"
git commit -m "asdf"
```

Future you has no idea what these did.

### How to Avoid

**Use this template:**

```
[Verb] [what you did]

Optional: More details about why
```

**Good examples:**

- "Add password validation to signup form"
- "Fix crash when user enters invalid email"
- "Refactor database queries to use connection pooling"

**Bad examples:**

- "update code"
- "fix bug"
- "changes"

### Pro Tip

Ask yourself: "If I read this in 6 months, would I understand what this commit does?"

## Mistake 6: Working Directly on Main

### What Happens

You make all your changes on the `main` branch instead of feature branches.

Problems:

- Can't experiment without risk
- Can't work on multiple features
- Hard to collaborate
- Messy history

### How to Avoid

**Always use branches:**

```bash
# Start new work
git checkout -b feature/my-feature

# Make changes and commits
git add .
git commit -m "Add feature"

# Push your branch
git push origin feature/my-feature

# Open PR to merge into main
```

### When It's OK

- Solo projects in early stages
- Small documentation changes
- Learning/experimenting in a test repo

## Mistake 7: Not Reading the Error Message

### What Happens

```
error: failed to push some refs...
```

You immediately panic and ask for help.

### How to Avoid

**Read the error message!** Git actually tells you what's wrong:

```
! [rejected] main -> main (non-fast-forward)
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. Integrate the remote changes (e.g., 'git pull')
hint: before pushing again.
```

Translation: "Someone else pushed changes. Pull them first."

Solution: `git pull` then `git push`

### Pro Tip

Copy the error message and ask AI:

```
"What does this git error mean and how do I fix it?
[paste error]"
```

## Mistake 8: Force Pushing to Main

### What Happens

```bash
git push --force origin main
```

You just **overwrote everyone else's work**. 💀

### How to Avoid

**Never force push to main or shared branches.**

Force push is only OK:

- On your own feature branches
- When you're alone on the branch
- When you know exactly what you're doing

### If You Did This

1. Apologize to your team
2. See if GitHub has a backup (sometimes there are safety nets)
3. Restore from someone else's local copy
4. Learn the lesson forever

## Mistake 9: Merge Conflicts Panic

### What Happens

```
CONFLICT (content): Merge conflict in src/app.py
```

You freeze in terror. 😱

### How to Avoid

You can't always avoid conflicts, but you can reduce them:

- Pull frequently
- Coordinate with teammates on who's editing what
- Keep changes small
- Use feature branches

### How to Fix

**Conflicts aren't scary:**

1. **Open the conflicted file:**

```python
<<<<<<< HEAD
def greet(name):
    return f"Hello, {name}!"
=======
def greet(name):
    return f"Hi there, {name}!"
>>>>>>> feature/new-greeting
```

2. **Choose what to keep:**

```python
# Keep one version
def greet(name):
    return f"Hi there, {name}!"
```

3. **Save, stage, commit:**

```bash
git add src/app.py
git commit -m "Resolve merge conflict in greet function"
```

See [When Things Break](when-things-break.md) for detailed help.

## Mistake 10: Not Using `.gitignore`

### What Happens

Your repo fills with:

- `node_modules/` (thousands of files)
- `__pycache__/` (Python cache)
- `.DS_Store` (Mac files)
- Build artifacts
- IDE settings

### How to Avoid

**Create `.gitignore` in the first commit:**

For Python:

```
__pycache__/
*.pyc
.env
venv/
.pytest_cache/
```

For Node.js:

```
node_modules/
.env
npm-debug.log
.next/
build/
```

For General:

```
.DS_Store
.vscode/
.idea/
*.log
```

### GitHub Templates

When creating a repo, GitHub offers `.gitignore` templates:

- Choose Python, Node, Java, etc.
- It generates the right ignores automatically

## Mistake 11: Deleting the `.git` Folder

### What Happens

```bash
rm -rf .git
```

You just deleted all Git history. The folder is now a regular folder.

### How to Avoid

**Never delete `.git` unless you really mean to.**

If you want to start over:

```bash
# Better: Create a new branch
git checkout -b fresh-start
```

### If You Did This

If you've pushed to GitHub before:

```bash
# Clone from GitHub to recover
git clone <your-repo-url>
```

If you haven't pushed: Your history is gone. 😢 Start over.

## Mistake 12: Committing Large Binary Files

### What Happens

You commit:

- Large datasets (GBs)
- Video files
- Large PDFs
- Database dumps

Git slows down. Cloning takes forever.

### How to Avoid

**Use `.gitignore` for large files:**

```
*.mp4
*.mov
*.pdf
data/
*.db
*.sql
```

**For large files you need to track:**

- Use Git LFS (Large File Storage)
- Store them elsewhere (S3, etc.) and reference them
- Use `.gitattributes` to mark them as binary

## Quick Reference: When You Make a Mistake

| Mistake | Quick Fix |
|---------|-----------|
| Committed to wrong branch | `git stash`, switch branch, `git stash pop` |
| Forgot to pull | `git pull` then resolve conflicts |
| Typo in commit message | `git commit --amend -m "New message"` |
| Added wrong file | `git reset HEAD <file>` |
| Want to undo last commit | `git reset --soft HEAD~1` |
| Merge conflict | Edit file, remove markers, `git add`, `git commit` |
| Pushed by accident | Ask team, might need `git revert` |

## Feeling Stuck?

**If you made a mistake:**

- Don't panic - almost everything is fixable
- Read the error message
- See [When Things Break](when-things-break.md)
- Ask AI: "How do I fix [your situation]?"
- Ask a human if unsure

**If you're afraid of making mistakes:**

- Create a test repo to experiment
- Practice on your own repos first
- Remember: Git is designed for undoing things
- Every developer makes these mistakes

**If you keep making the same mistake:**

- Add a checklist (like pilots do)
- Use Git aliases or scripts
- Set up pre-commit hooks
- It's okay - muscle memory takes time

## Next Steps

Now that you know common pitfalls:

- **[When Things Break](when-things-break.md)** - Detailed fixes
- **[Branches and Commits](branches-and-commits.md)** - Understanding the fundamentals
- **[Exercises](../../exercises/github-fundamentals/)** - Practice safely

---

**Remember:** Every expert has made all these mistakes. You're in good company! 💪
