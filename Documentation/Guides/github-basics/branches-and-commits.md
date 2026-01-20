# Branches and Commits

Let's demystify two of the most important concepts in Git: branches and commits.

## What Are Commits?

### The Simple Version

A commit is a **snapshot** of your code at a specific moment in time.

Think of it like:

- Saving a video game at a checkpoint
- Taking a photo of your work
- Creating a labeled version you can return to

### Anatomy of a Commit

Every commit has:

1. **Changes** - What files were added, modified, or deleted
2. **Message** - What you did and why
3. **Author** - Who made the change
4. **Timestamp** - When it happened
5. **Unique ID** - A long string like `a3f2b9c`

### Example Commit

```
Commit: a3f2b9c
Author: Alex <alex@example.com>
Date: Mon Dec 16 14:30:00 2024
Message: Add user login functionality

Changes:
+ src/auth.py (new file)
+ src/main.py (modified)
- src/old_login.py (deleted)
```

## Writing Good Commit Messages

### The Formula

```
[Verb] [What you did]

Optional: Why you did it or additional context
```

### Good Examples

✅ `Add password validation to signup form`
✅ `Fix crash when user enters empty email`
✅ `Update README with installation instructions`
✅ `Refactor database queries for better performance`

### Not-So-Good Examples

❌ `Update` - What did you update?
❌ `Fix bug` - Which bug?
❌ `Changes` - Too vague
❌ `asdfasdf` - Come on now

### Why It Matters

Good commit messages help:

- Future you understand what you did
- Teammates understand your changes
- AI assistants provide better help
- Anyone reviewing the code

## What Are Branches?

### The Simple Version

A branch is a **parallel version** of your code where you can make changes without affecting the main version.

### The "Parallel Universes" Analogy

Imagine you're writing a novel:

**Main branch** - The official published version

**Feature branches** - Alternative versions where you try things:

- `chapter-5-alternate-ending` - Try a different plot
- `add-new-character` - Experiment with a new character
- `fix-typos` - Clean up mistakes

If you like the changes, you **merge** them into the main branch. If not, just delete that branch. The main branch is untouched.

### Why Branches Are Amazing

1. **Experiment safely** - Try things without breaking working code
2. **Work in parallel** - Multiple people/features at once
3. **Isolate changes** - Each feature gets its own space
4. **Easy cleanup** - Delete failed experiments

## Common Branch Names

| Branch Name | Purpose |
|------------|---------|
| `main` or `master` | The official version |
| `develop` | Staging area for next release |
| `feature/user-auth` | New feature: user authentication |
| `bugfix/login-crash` | Fix a bug in login |
| `hotfix/security-patch` | Urgent fix for production |

## The Branch Workflow

### 1. Start with Main

```
main: [A] → [B] → [C]
```

You have 3 commits on the main branch.

### 2. Create a Feature Branch

```
main:    [A] → [B] → [C]
                       ↓
feature:               [C]
```

Your new branch starts from commit C.

### 3. Make Changes on Feature Branch

```
main:    [A] → [B] → [C]
                       ↓
feature:               [C] → [D] → [E]
```

You make commits D and E on your feature branch. Main is unchanged.

### 4. Merge Back to Main

```
main:    [A] → [B] → [C] → [D] → [E]
```

Your changes are now in the main branch.

## Commits vs Branches vs Pull Requests

Let's clarify the relationship:

**Commit** = A single saved change

- "I added a button"
- One snapshot in time

**Branch** = A series of commits

- "I'm working on the user profile page"
- Contains multiple commits

**Pull Request** = "Can I merge my branch?"

- "I finished the user profile page, review it?"
- Merges all commits from your branch into main

## Hands-On Example

Let's walk through a real scenario:

### Scenario: Adding a New Feature

**Step 1: Create a branch**

```bash
git checkout -b feature/add-dark-mode
```

You're now on a new branch called `feature/add-dark-mode`.

**Step 2: Make changes and commit**

```bash
# Edit some files...
git add styles.css
git commit -m "Add dark mode toggle button"
```

**Step 3: Make more commits**

```bash
# Edit more files...
git add theme.js
git commit -m "Implement dark mode color scheme"
```

**Step 4: Push your branch to GitHub**

```bash
git push origin feature/add-dark-mode
```

**Step 5: Create Pull Request on GitHub**

- Go to your repo on GitHub
- Click "Pull Requests" → "New Pull Request"
- Select your branch
- Write description of what you did
- Click "Create Pull Request"

**Step 6: After review, merge**

- Reviewers approve your changes
- Click "Merge Pull Request"
- Your changes are now in main!

## Viewing Branches and Commits

### On GitHub (Web Interface)

- **See all branches:** Click the branch dropdown
- **See commits:** Click "commits" or "history"
- **Compare branches:** Go to "Pull Requests"

### With Git Commands

```bash
# See current branch
git branch

# See all branches
git branch -a

# See commit history
git log

# See recent commits (pretty)
git log --oneline -10

# See changes in a commit
git show <commit-id>
```

## Common Questions

### "How often should I commit?"

**Commit when you complete a logical unit of work:**

- Fixed a bug? Commit.
- Added a feature? Commit.
- About to try something risky? Commit first.

**Don't commit:**

- Every single keystroke
- Broken code (unless it's end of day)
- Half-finished thoughts

### "Can I change a commit message after I make it?"

Yes, but only if you haven't pushed to GitHub yet:

```bash
git commit --amend -m "New message"
```

If you've already pushed, it's safer to leave it and write a better message next time.

### "What if I commit to the wrong branch?"

Don't panic! See [When Things Break](when-things-break.md) for recovery strategies.

### "Do I really need branches for small projects?"

For solo projects, you can work on main directly when starting. But branches are helpful for:

- Trying experiments
- Working on multiple features
- Learning the workflow for team projects

## The Mental Model

Think of your repository as a **tree**:

```
         main (trunk)
           │
    ┌──────┴──────┐
    │             │
feature-1    feature-2 (branches)
    │             │
  [commits]   [commits]
    │
    └──> merge back to main
```

- **Main branch** = The trunk
- **Feature branches** = Branches growing out
- **Commits** = Leaves on each branch
- **Merging** = Grafting a branch back to trunk

## Feeling Stuck?

**If commits seem confusing:**

- Think: "Save game checkpoint"
- Practice making tiny commits
- Read commit messages on popular repos
- Ask AI: "Show me 10 good commit message examples"

**If branches seem abstract:**

- Try creating one! It's just a pointer
- Draw it out on paper
- Experiment in a test repo
- Remember: You can always delete branches

**If you accidentally commit something wrong:**

- Don't panic - everything is recoverable
- See [When Things Break](when-things-break.md)
- Ask AI: "How do I undo my last commit?"

## Next Steps

Now that you understand commits and branches:

- **[Pull Requests Explained](pull-requests-explained.md)** - How to collaborate
- **[First 10 Minutes](first-10-minutes.md)** - Try it yourself
- **[When Things Break](when-things-break.md)** - Fix mistakes

---

**Remember:** Making commits and branches is reversible. Experiment freely! 🌿
