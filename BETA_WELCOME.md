# Welcome to Sono-Eval Beta (v0.5.0)

Congratulations! You are now running the **Beta** version of the Sonotheia Evaluation System. This release bridges the gap between a robust backend and a polished, user-friendly frontend.

## 🚀 The Basics: Mechanics of the Repo

Sono-Eval is designed as a **hybrid** system that runs locally on your machine but with the power of a modern web application.

### Core Components

1. **FastAPI Backend** (`src/sono_eval`): The brain. Handles assessments, scoring, and batch processing.
2. **Next.js Frontend** (`frontend/`): The face. A beautiful, reactive interface for viewing results and analytics.
3. **Celery & Redis**: The muscle. Handles heavy lifting (batch processing) in the background so the UI stays snappy.
4. **PostgreSQL (or SQLite)**: The memory. Stores your data securely.

### Interfaces

You have two primary ways to interact with Sono-Eval:

* **Web Dashboard (The "Commander" View)**:
  * **URL**: `http://localhost:3000`
  * **Best for**: Viewing visual analytics, reading detailed explanation paths, and managing candidates.
  * **Key Feature**: The "Dark Horse" mode toggles high-contrast visuals for focused work.

* **CLI (The "Engineer" View)**:
  * **Command**: `sono-eval` (or `./launcher.sh repl`)
  * **Best for**: Quick checks, scripting, and direct access to the assessment engine.

---

## 🎯 Strategies for Success

### 1. The "Multi-Path" Approach

Don't just look at the overall score. Sono-Eval breaks down performance into distinct paths:

* **Technical**: Raw coding ability and correctness.
* **Problem Solving**: Algorithmic thinking and edge-case handling.
* **Communication**: (If applicable) Documentation and clarity.

**Strategy**: Use the **Radar Chart** on the dashboard to spot "spiky" profiles—candidates who might be geniuses in one area but weak in others.

### 2. Batch Processing Power

Got a folder of submissions? Don't run them one by one.

* Use the **Batch Upload** feature (in the UI or via API endpoint `POST /api/v1/assessments/batch`).
* The system processes them asynchronously. You can close the tab and come back later to see the results.

### 3. PDF Reporting

Need to share results with a hiring manager?

* Go to any **Assessment Detail** page.
* Click **"Export PDF"**.
* You get a professional, branded report with executive summaries and key findings.

---

## 💡 Quick Tips

* **Dark Horse Mode**: Toggle the theme in the UI settings for a distraction-free, terminal-inspired aesthetic.
* **Search Smart**: The candidate search bar supports "fuzzy matching". Typing partial IDs works great.
* **Health Check**: If something feels stuck, check `http://localhost:8000/api/v1/status/system`. It gives you a real-time heartbeat of all components (Redis, DB, etc.).

## 🛠 Troubleshooting

* **"Worker not found"**: Make sure you ran `docker-compose up` so the Celery worker is active.
* **"No module named..."**: If running locally without Docker, ensure your `pip` environment is synced (`pip install -e .[dev,all]`).

Enjoy the Beta! 🚀
