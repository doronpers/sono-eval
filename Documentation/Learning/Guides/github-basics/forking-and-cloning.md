# Forking and Cloning

Two ways to get a copy of a repository: forking and cloning. Let's understand when to use each.

## What's the Difference?

### Forking

**Creating your own copy on GitHub**

Like making a photocopy of a book - you now have your own version you can write in.

### Cloning

**Downloading a repo to your computer**

Like checking a book out from the library - you have it locally to read and work with.

## When to Fork

Fork when you want to:

- **Contribute to someone else's project**
- **Build on top of an existing project**
- **Experiment without affecting the original**
- **Create your own version**

### Example: Contributing to Open Source

1. Fork the project to your GitHub account
2. Clone your fork to your computer
3. Make changes
4. Push to your fork
5. Open a PR to the original project

## When to Clone

Clone when you want to:

- **Work on your own repo locally**
- **Just explore the code**
- **Run the project on your computer**
- **You have write access to the repo**

### Example: Working on Your Project

1. Clone your repo to your computer
2. Make changes
3. Commit
4. Push directly to your repo

## How to Fork

### On GitHub (Web)

1. Go to the repository you want to fork
2. Click the "Fork" button (top right)
3. Choose where to fork it (your account)
4. Wait a few seconds - done!

You now have `yourusername/project-name` as a copy of `original-owner/project-name`.

### What You Get

- A complete copy of all code
- All branches and history
- Your own repo you can modify
- Linked to the original (can sync updates)

## How to Clone

### Using Command Line

```bash
# Clone a repo
git clone https://github.com/username/repo-name.git

# Clone to a specific folder
git clone https://github.com/username/repo-name.git my-folder

# Clone a specific branch
git clone -b branch-name https://github.com/username/repo-name.git
```

### Using GitHub Desktop

1. Open GitHub Desktop
2. File → Clone Repository
3. Choose from your repos or paste URL
4. Select where to save it
5. Click "Clone"

### Using VS Code

1. Open VS Code
2. View → Command Palette (Cmd/Ctrl + Shift + P)
3. Type "Git: Clone"
4. Paste the repo URL
5. Choose folder location

## The Fork-and-Clone Workflow

The most common workflow for contributing:

### Step 1: Fork on GitHub

```
Original: github.com/owner/repo
   ↓
Your Fork: github.com/yourusername/repo
```

### Step 2: Clone Your Fork

```bash
git clone https://github.com/yourusername/repo.git
cd repo
```

### Step 3: Add Original as "Upstream"

```bash
git remote add upstream https://github.com/owner/repo.git
```

Now you have two remotes:

- **origin** - Your fork (you can push here)
- **upstream** - Original repo (you can pull updates)

### Step 4: Make Changes

```bash
git checkout -b feature/my-improvement
# Make changes...
git add .
git commit -m "Add my improvement"
```

### Step 5: Push to Your Fork

```bash
git push origin feature/my-improvement
```

### Step 6: Open Pull Request

1. Go to your fork on GitHub
2. Click "Compare & pull request"
3. Write description
4. Submit to original repo

## Keeping Your Fork Updated

The original repo changes over time. Stay in sync:

### Fetch Updates from Original

```bash
# Get latest from original repo
git fetch upstream

# Switch to your main branch
git checkout main

# Merge updates
git merge upstream/main

# Push to your fork
git push origin main
```

### One Command Version

```bash
git pull upstream main
git push origin main
```

Do this regularly to avoid conflicts!

## Fork vs Clone: The Decision Tree

```
Do you want to contribute back to the original?
├─ Yes → FORK then clone your fork
└─ No
    ├─ Is it your own repo?
    │   └─ Yes → CLONE directly
    └─ Do you just want to explore the code?
        └─ Yes → CLONE directly
```

## Common Scenarios

### Scenario 1: Learning from an Example Project

**Goal:** Just want to see how it works

**Action:** Clone directly

```bash
git clone https://github.com/owner/repo.git
cd repo
# Explore and run it
```

### Scenario 2: Building Your Own Version

**Goal:** Use as a starting point for your project

**Action:** Fork it

1. Fork on GitHub
2. Clone your fork
3. Change the code to fit your needs
4. It's now yours!

### Scenario 3: Contributing a Bug Fix

**Goal:** Fix a bug and contribute back

**Action:** Fork → Clone → Fix → PR

1. Fork the repo
2. Clone your fork
3. Create a branch
4. Fix the bug
5. Push to your fork
6. Open PR to original

### Scenario 4: Working on Team Project

**Goal:** Collaborate with teammates

**Action:** Clone directly (if you have access)

```bash
git clone https://github.com/team/project.git
# Make changes on branches
# Push directly to team repo
```

## Understanding Remotes

After cloning, check your remotes:

```bash
git remote -v
```

### If You Just Cloned

```
origin  https://github.com/username/repo.git (fetch)
origin  https://github.com/username/repo.git (push)
```

### If You Cloned a Fork and Added Upstream

```
origin    https://github.com/you/repo.git (fetch)
origin    https://github.com/you/repo.git (push)
upstream  https://github.com/owner/repo.git (fetch)
upstream  https://github.com/owner/repo.git (push)
```

### What This Means

- **origin** = Default remote (usually your fork)
- **upstream** = Original repo (read-only for you)

## GitHub's Network Graph

See how forks relate to the original:

1. Go to any repo on GitHub
2. Click "Insights" → "Network"
3. See visual tree of all forks and branches

Cool way to see how projects evolve!

## Tips and Best Practices

### Before Forking

- **Check the license** - Can you legally fork it?
- **Check activity** - Is the project maintained?
- **Read CONTRIBUTING.md** - Any special rules?

### After Forking

- **Customize README** - Make it clear it's your fork
- **Credit the original** - Link back to source
- **Keep updated** - Sync with upstream regularly

### When Cloning

- **Choose a good location** - Projects folder, not Desktop
- **Clone via HTTPS** - Easier than SSH for beginners
- **Name it clearly** - Use the folder name parameter

## Common Issues

### "I Forked But Can't Push"

You forked someone else's repo, then cloned the ORIGINAL instead of your fork.

**Fix:**

```bash
# Check your remote
git remote -v

# If it shows the original owner's repo, change it:
git remote set-url origin https://github.com/YOURUSERNAME/repo.git
```

### "My Fork Is Outdated"

Your fork is behind the original repo.

**Fix:**

```bash
# Add upstream if you haven't
git remote add upstream https://github.com/original-owner/repo.git

# Fetch and merge
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

### "I Cloned But Changes Disappeared"

You made changes but didn't commit them before pulling updates.

**Fix:**

```bash
# Stash your changes
git stash

# Pull updates
git pull

# Restore your changes
git stash pop
```

## Feeling Stuck?

**If fork vs clone is confusing:**

- Think: Fork = Make your own copy online
- Think: Clone = Download to your computer
- You often do BOTH (fork then clone your fork)
- Try both with a test repo to see difference

**If remotes are confusing:**

- Draw it out: You ← Your Fork ← Original
- origin = your fork (you can write)
- upstream = original (read-only)
- Run `git remote -v` to see what's configured

**If you're not sure which to use:**

- Start with cloning - it's simpler
- Fork when you need to contribute back
- Ask AI: "Should I fork or clone in this situation?"

## Next Steps

Now you understand forking and cloning:

- **[First 10 Minutes](first-10-minutes.md)** - Try it yourself
- **[Branches and Commits](branches-and-commits.md)** - Work with your clone
- **[Pull Requests Explained](pull-requests-explained.md)** - Contribute from your fork

Ready to practice?
→ **[Exercises: Forking and Cloning](../../exercises/github-fundamentals/03-branches.md)**

---

**Remember:** Fork makes a copy online. Clone downloads to your computer. Often you do both! 🔄
