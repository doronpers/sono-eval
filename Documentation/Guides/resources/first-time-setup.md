# First-Time Setup Guide

For Remote Candidates Setting Up on Personal Machines

This guide will help you set up Sono-Eval on your personal computer for the
first time. We'll explain what each step does and why it matters.

---

## What You'll Need

- **Python 3.9 or higher** - The programming language Sono-Eval uses
- **Internet connection** - To download dependencies and access the web interface
- **About 15 minutes** - For the initial setup

---

## Step 1: Check Your Python Version

**Why this matters:** Sono-Eval requires Python 3.9 or newer to work properly.

**How to check:**

```bash
python3 --version
# or
python --version
```

**What you should see:** Something like `Python 3.9.0` or higher

**If you don't have Python:** Download from [python.org](https://www.python.org/downloads/)

---

## Step 2: Clone the Repository

**Why this matters:** This downloads Sono-Eval to your computer so you can run it.

**How to do it:**

```bash
git clone https://github.com/doronpers/sono-eval.git
cd sono-eval
```

**What happens:** Sono-Eval files are downloaded to a folder called
`sono-eval` on your computer.

---

## Step 3: Create a Virtual Environment

**Why this matters:** This keeps Sono-Eval's dependencies separate from other
Python projects on your computer. It prevents conflicts and keeps things
organized.

**How to do it:**

```bash
python3 -m venv venv
```

**What happens:** A new folder called `venv` is created with an isolated Python environment.

**Activate it:**

- **On Mac/Linux:** `source venv/bin/activate`
- **On Windows:** `venv\Scripts\activate`

**You'll know it worked when:** You see `(venv)` at the start of your command prompt.

---

## Step 4: Install Dependencies

**Why this matters:** Sono-Eval needs other software libraries to work. This
step downloads and installs them.

**How to do it:**

```bash
pip install -r requirements.txt
pip install -e .
```

**What happens:**

- Python downloads and installs all required libraries
- Sono-Eval is installed in "editable" mode (you can modify it if needed)

**This may take a few minutes** - be patient! You'll see progress messages.

---

## Step 5: Configure Environment

**Why this matters:** Sono-Eval needs some settings to know how to run. We'll
create a configuration file.

**How to do it:**

```bash
cp .env.example .env
```

**What happens:** A configuration file (`.env`) is created with default settings.

**You usually don't need to edit this** - the defaults work fine for getting started.

---

## Step 6: Verify Your Setup

**Why this matters:** This checks that everything is installed correctly before
you start.

**How to do it:**

```bash
python verify_setup.py
```

**What you should see:**

- ✅ Green checkmarks for each component
- "ALL CRITICAL CHECKS PASSED" message

**If something fails:** The script will tell you what's wrong and how to fix it.

---

## Step 7: Start Sono-Eval

**Why this matters:** This starts the web server so you can access Sono-Eval in
your browser.

**How to do it:**

```bash
sono-eval server start
```

**What happens:**

- The server starts running
- You'll see a message like "Starting Sono-Eval API server..."
- The server keeps running until you stop it (Ctrl+C)

---

## Step 8: Access Sono-Eval

**Why this matters:** This is how you'll actually use Sono-Eval!

**How to do it:**

1. Open your web browser
2. Go to: `http://localhost:8000/mobile`
3. You should see the Sono-Eval welcome page!

**What you can do:**

- Click "Let's Get Started" to begin an assessment
- Explore the interface
- Complete your first assessment

---

## Troubleshooting

### "Command not found" errors

**Problem:** Python or pip commands don't work

**Solutions:**

- Make sure Python is installed: `python3 --version`
- Try `python` instead of `python3` (or vice versa)
- On Windows, you might need to add Python to your PATH

### Port 8000 already in use

**Problem:** Another program is using port 8000

**Solutions:**

- Stop the other program using that port
- Or change the port: `sono-eval server start --port 8001`
- Then access at `http://localhost:8001/mobile`

### Installation takes a long time

**This is normal!** Some dependencies are large. Just wait for it to finish.

### "Permission denied" errors

**Problem:** Your computer won't let you install software

**Solutions:**

- On Mac/Linux: Try `sudo` (use carefully!)
- On Windows: Run terminal as Administrator
- Or install to a user directory instead

---

## What's Next?

Once you have Sono-Eval running:

1. **Complete your first assessment** - Follow the guided flow
2. **Explore the results** - See what insights you get
3. **Try different paths** - Assess different skill areas
4. **Discover hidden features** - Look for easter eggs! (Try pressing `?`
   for keyboard shortcuts)

---

## Getting Help

If you run into issues:

1. **Check the error message** - It usually tells you what's wrong
2. **Read the troubleshooting section** above
3. **Check the main documentation** - [Troubleshooting Guide](../troubleshooting.md)
4. **Ask for help** - Contact your evaluator or team lead

---

## Quick Reference

**Start the server:**

```bash
sono-eval server start
```

**Stop the server:**
Press `Ctrl+C` in the terminal

**Check if it's working:**
Visit `http://localhost:8000/mobile` in your browser

**Verify setup:**

```bash
python verify_setup.py
```

---

**Remember:** This is a learning tool. Take your time, explore, and don't worry
if something doesn't work perfectly the first time!
