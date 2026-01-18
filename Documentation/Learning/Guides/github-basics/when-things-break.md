# When Things Break

Git is designed for recovery. Almost everything is fixable. Let's learn how to fix common issues calmly and confidently.

## The Golden Rules

1. **Don't panic** - You probably didn't break anything permanently
2. **Read the error** - Git usually tells you what's wrong
3. **Ask before forcing** - `--force` is dangerous on shared branches
4. **When in doubt, commit** - Save your work before trying fixes

## Quick Fixes

### "I Committed on the Wrong Branch"

**Scenario:** You made commits on `main` but meant to be on a feature branch.

**Solution:**

```bash
# Create new branch from current state (keeps your commits)
git branch feature/my-work

# Switch to main
git checkout main

# Reset main to before your commits (doesn't delete them - they're on feature/my-work)
git reset --hard origin/main

# Switch to your feature branch
git checkout feature/my-work
```

### "I Need to Undo My Last Commit"

**Scenario:** You committed too early or with mistakes.

**Solution (keep the changes, undo the commit):**

```bash
git reset --soft HEAD~1
```

Your files still have the changes, but the commit is gone.

**Solution (discard everything in the last commit):**

```bash
git reset --hard HEAD~1
```

⚠️ This deletes the changes permanently!

### "I Want to Change My Last Commit Message"

**Scenario:** Typo in commit message or forgot to mention something.

**Solution (if you haven't pushed yet):**

```bash
git commit --amend -m "New correct message"
```

**If you already pushed:**
Don't change it - just make a new commit. Changing history after pushing causes problems for others.

### "I Added the Wrong File to a Commit"

**Scenario:** You committed a file you didn't mean to.

**Solution (before pushing):**

```bash
# Remove file from last commit but keep it in your working directory
git reset HEAD~1 path/to/wrong-file.txt

# Redo the commit without that file
git add .
git commit -m "Your message"
```

**Solution (after pushing):**

```bash
# Remove file from tracking but keep local copy
git rm --cached path/to/wrong-file.txt

# Commit the removal
git commit -m "Remove accidentally committed file"
git push
```

### "I Committed a Secret/Password"

**Scenario:** You accidentally committed an API key, password, or `.env` file.

**⚠️ Critical Steps:**

1. **IMMEDIATELY rotate/change the secret** - Consider it compromised!

2. **Remove from last commit (if not pushed):**

```bash
git reset HEAD~1
echo "secret-file.txt" >> .gitignore
git add .
git commit -m "Add proper files"
```

3. **If already pushed:**
The secret is in the history forever. You MUST:

- Rotate the credential immediately
- Use `git filter-branch` or `BFG Repo-Cleaner` (advanced)
- Consider making a new repo and marking the old one as compromised

**Prevention:**

```bash
# Always use .gitignore
echo ".env" >> .gitignore
echo "secrets.json" >> .gitignore
git add .gitignore
git commit -m "Ignore secrets"
```

## Merge Conflicts

### What Is a Merge Conflict?

Two people changed the same lines in a file. Git doesn't know which version to keep.

### Anatomy of a Conflict

```python
<<<<<<< HEAD
def greet(name):
    return f"Hello, {name}!"
=======
def greet(name):
    return f"Hi there, {name}!"
>>>>>>> feature/new-greeting
```

**Translation:**

- `<<<<<<< HEAD` - Your current branch's version
- `=======` - The divider
- `>>>>>>> feature/new-greeting` - The incoming branch's version

### How to Resolve

**Step 1: Open the file in your editor**

**Step 2: Decide what to keep:**

Option A - Keep yours:

```python
def greet(name):
    return f"Hello, {name}!"
```

Option B - Keep theirs:

```python
def greet(name):
    return f"Hi there, {name}!"
```

Option C - Combine both:

```python
def greet(name):
    # Using friendlier greeting per feedback
    return f"Hi there, {name}!"
```

**Step 3: Remove the conflict markers:**
Delete the `<<<<<<<`, `=======`, and `>>>>>>>` lines.

**Step 4: Save, stage, and commit:**

```bash
git add src/app.py
git commit -m "Resolve merge conflict in greet function"
```

### Using VS Code for Conflicts

VS Code makes this easier with buttons:

- **Accept Current Change** - Keep your version
- **Accept Incoming Change** - Keep their version
- **Accept Both Changes** - Keep both
- **Compare Changes** - See side-by-side

### Prevention

You can't always prevent conflicts, but you can reduce them:

- Pull frequently (`git pull` daily)
- Use feature branches
- Communicate with team about who's editing what
- Keep changes small and focused

### For Complex Conflicts

When conflicts involve many files or complex logic:

- **Use AI agents** - See **[Agent-Assisted Resolution](agent-assisted-resolution.md)** for step-by-step AI guidance
- **Ask for help** - Share your git status with AI tools like GitHub Copilot, ChatGPT, or Claude
- **Take it slow** - Resolve one file at a time, testing after each

## Recovering Lost Work

### "I Deleted My Changes!"

**Scenario:** You ran `git reset --hard` or `git checkout` and lost uncommitted work.

**Solution:**

If you committed at any point, even if you "deleted" the commit:

```bash
# See all commits, even deleted ones
git reflog

# Find the commit hash (like a3f2b9c)
# Restore it
git checkout a3f2b9c
```

If you never committed: The work is likely gone. 😢

**Lesson:** Commit early, commit often!

### "I Deleted a Branch by Accident"

**Scenario:** `git branch -D feature/my-work` - oops!

**Solution:**

```bash
# See all branch deletions
git reflog

# Find the commit where the branch was
# Recreate the branch
git checkout -b feature/my-work a3f2b9c
```

### Using `git reflog` (Your Safety Net)

`reflog` is Git's diary - it records everything you do:

```bash
git reflog
```

Output:

```
a3f2b9c HEAD@{0}: commit: Add feature
7d8e2f1 HEAD@{1}: checkout: moving from main to feature
4b9c3a2 HEAD@{2}: commit: Fix bug
```

You can go back to ANY of these points:

```bash
git checkout HEAD@{2}
# Or
git checkout 4b9c3a2
```

## "The Nuclear Option" (When All Else Fails)

### Reset to Remote State

**Scenario:** Your local repo is messed up. You want to match what's on GitHub.

**Solution:**

```bash
# Save your current work just in case
git stash

# Get latest from GitHub
git fetch origin

# Reset your branch to match GitHub exactly
git reset --hard origin/main
```

⚠️ This deletes all local changes!

### Start Fresh

**Scenario:** Everything is so broken you want to start over.

**Solution:**

```bash
# If you have uncommitted work you care about, save it somewhere

# Clone a fresh copy
cd ..
mv my-repo my-repo-broken-backup
git clone <your-repo-url>
cd my-repo
```

You have a clean slate, and the broken one is backed up.

## Fixing Common Errors

### "failed to push some refs"

**Error:**

```
! [rejected] main -> main (non-fast-forward)
```

**Translation:** Someone else pushed while you were working.

**Solution:**

```bash
git pull origin main
# Resolve any conflicts
git push origin main
```

### "You have divergent branches"

**Error:**

```
hint: You have divergent branches and need to specify how to reconcile them.
```

**Translation:** Your local and remote branches have different commits.

**Solution:**

```bash
# Option 1: Merge (creates a merge commit)
git pull --merge

# Option 2: Rebase (cleaner history)
git pull --rebase

# Then push
git push
```

### "refusing to merge unrelated histories"

**Error:**

```
fatal: refusing to merge unrelated histories
```

**Translation:** Git thinks these are two separate projects.

**Solution:**

```bash
git pull origin main --allow-unrelated-histories
```

Usually happens when you `git init` in a folder, then try to pull from a repo.

### "Your branch is behind"

**Error:**

```
Your branch is behind 'origin/main' by 3 commits
```

**Solution:**

```bash
git pull origin main
```

Simple! Just pull the latest changes.

## Undoing a Push

### "I Pushed Something I Shouldn't Have"

**Scenario:** You pushed a commit to GitHub that you regret.

**Solution (if it's just you on the branch):**

```bash
# Undo the commit locally
git reset --hard HEAD~1

# Force push (⚠️ only if you're alone on this branch!)
git push --force origin feature/my-branch
```

**Solution (if others might have pulled your branch):**

```bash
# Create a new commit that undoes the changes
git revert HEAD

# Push the revert commit
git push origin feature/my-branch
```

`git revert` is safer because it doesn't rewrite history.

## When to Ask for Help

### Signs You Should Stop and Ask

- You're about to use `--force` on a shared branch
- You see errors you don't understand after 2 tries
- You're considering deleting the repo
- Other people's work might be affected
- You're unsure if something is reversible

### Where to Ask

1. **AI assistants** - "How do I fix this Git error: [error message]"
2. **Stack Overflow** - Search first, many questions already answered
3. **Your team** - They've probably seen it before
4. **GitHub Issues** on this repo - We're here to help!

### How to Ask

**Good question:**

```
I'm trying to merge my feature branch into main, but I get this error:
[paste error message]

I've tried:
- git pull origin main (got a merge conflict)
- Resolving the conflict in app.py
- git add app.py

What should I do next?
```

**Not-so-helpful question:**

```
Git is broken, help!
```

## Prevention Checklist

Before you get into trouble:

```bash
# Daily habits
git pull                    # Get latest changes
git status                  # See what's changed
git diff                    # Review before committing

# Before committing
git diff --staged           # See exactly what you're committing
git status                  # Double-check files

# Before pushing
git log -3                  # Review your last 3 commits
git diff origin/main        # See what you're about to push

# Before trying a fix
git stash                   # Save your work
```

## Advanced Recovery (Use with Caution)

### Rewriting History with Interactive Rebase

**Use case:** Clean up your last few commits before pushing.

```bash
git rebase -i HEAD~3
```

Opens an editor where you can:

- `pick` - Keep the commit
- `squash` - Combine with previous commit
- `reword` - Change commit message
- `drop` - Delete the commit

⚠️ **Never do this on commits you've already pushed to a shared branch!**

### Cherry-Picking Commits

**Use case:** Copy a specific commit to another branch.

```bash
# On target branch
git checkout main

# Copy commit from another branch
git cherry-pick a3f2b9c
```

### Stashing Multiple Times

**Use case:** Save work-in-progress without committing.

```bash
# Save current work
git stash save "Work on feature X"

# Do something else...

# See all stashes
git stash list

# Restore a specific stash
git stash apply stash@{1}
```

## Feeling Stuck?

**If nothing here helps:**

- Take a breath - you'll figure it out
- Ask AI with your exact error message
- Post on Stack Overflow with details
- Ask in this repo's Issues
- Remember: Even experts Google Git errors

**If you're afraid to try a fix:**

- Create a backup: `cp -r my-repo my-repo-backup`
- Try the fix in the original
- If it breaks, delete it and rename the backup
- Nothing is permanently broken if you have backups

**If you broke a shared branch:**

- Communicate with your team immediately
- Don't try to hide it - ask for help
- You'll figure it out together
- Everyone's done this once

## Next Steps

Now that you know how to recover:

- **[Agent-Assisted Resolution](agent-assisted-resolution.md)** - Use AI agents for complex scenarios
- **[Common Mistakes](common-mistakes.md)** - Prevent problems
- **[Branches and Commits](branches-and-commits.md)** - Understand the fundamentals
- **[Exercises](../../Exercises/)** - Practice exercises (see available exercises)

---

**Remember:** Git is designed for recovery. You're more resilient than you think! 🔧
