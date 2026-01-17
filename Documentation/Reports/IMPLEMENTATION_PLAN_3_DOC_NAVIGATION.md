# Implementation Plan 3: Documentation Navigation & First-Time UX

**Impact**: HIGH | **Effort**: LOW | **Time**: 2–3h

---

## Prerequisites (exact files)

1. Root README CTA cluster: `README.md` lines 18–23.  
2. Existing onboarding doc: `Documentation/START_HERE.md`.  
3. CONTRIBUTING quickstarts: `CONTRIBUTING.md` lines 6–64.

---

## Task A — Single CTA in README → START_HERE.md

### Before (current)
- Multiple “Start here / Quick Start / Documentation” options are listed at lines 18–23, competing for attention.

### After (target)
- Replace the CTA cluster with a **single primary CTA** pointing to a reworked `START_HERE.md`.

#### Replace README CTA block (copy-paste)
**File**: `README.md`  
**Replace** lines 18–23 with:

```markdown
**[Start Here →](Documentation/START_HERE.md)**
```

---

## Task B — START_HERE.md: 3 Visual Paths + Quick Navigation

### Goal
Provide a single, visually guided entry point with three paths:
- **Try** (5–10 min)
- **Learn** (15–20 min)
- **Build** (30–45 min)

#### START_HERE template (copy-paste)
**File**: `Documentation/START_HERE.md`

```markdown
# Start Here

Welcome! Choose the path that matches your goal:

| Path | Best for | Time | Link |
| --- | --- | --- | --- |
| 🚀 **Try** | First-time users | 5–10 min | [Quick Try](Guides/QUICK_START.md) |
| 📚 **Learn** | Understand the system | 15–20 min | [User Guide](Guides/user-guide/overview.md) |
| 🛠️ **Build** | Contribute or extend | 30–45 min | [Contributor Path](../CONTRIBUTING.md) |

## Quick Navigation

- **API Reference**: [API Reference](Guides/user-guide/api-reference.md)
- **Install Options**: [Installation Guide](Guides/user-guide/installation.md)
- **CLI Usage**: [CLI Guide](Guides/user-guide/cli.md)
- **Mobile Companion**: [Mobile Overview](Guides/user-guide/mobile.md)

## Reading Times

- Quick Try: ~5–10 minutes
- Learn the system: ~15–20 minutes
- Build + Contribute: ~30–45 minutes
```

---

## Task C — Add SEARCH.md and NAVIGATION.md

### SEARCH.md (keyword-based)
**File**: `Documentation/SEARCH.md` (new)

```markdown
# Search Guide

Use this index to quickly find what you need:

- **Getting started** → START_HERE.md, Guides/QUICK_START.md
- **API** → Guides/user-guide/api-reference.md
- **Assessment engine** → Core/assessment-engine.md
- **Mobile** → Guides/user-guide/mobile.md
- **Troubleshooting** → Guides/user-guide/troubleshooting.md
```

### NAVIGATION.md (visual site map)
**File**: `Documentation/NAVIGATION.md` (new)

```markdown
# Documentation Map

- START_HERE.md
  - Guides/QUICK_START.md
  - Guides/user-guide/overview.md
  - Guides/user-guide/installation.md
  - Guides/user-guide/api-reference.md
- Core/
- Governance/
- Learning/
- Reports/
```

---

## Task D — Simplify CONTRIBUTING.md Quickstarts

### Before (current)
- Three overlapping “Quick Start” sections (browser-only, codespaces, local) at lines 6–64.

### After (target)
- Replace with three clear pathways: **Browser**, **Codespaces**, **Local**. Each path should be 3–5 steps and link to deeper docs.

#### Replace contributing quickstarts (copy-paste)
**File**: `CONTRIBUTING.md`  
**Replace** lines 6–64 with:

```markdown
## Quick Start

Choose the path that matches your setup:

### 🌐 Browser (edit-only)
1. Fork the repo on GitHub.
2. Edit a file directly in the browser.
3. Commit changes and open a PR.

### ☁️ Codespaces (full dev in browser)
1. Open Codespaces from the “Code” menu.
2. Run `./launcher.sh start`.
3. Make changes, commit, and publish your branch.

### 💻 Local (full control)
1. Clone your fork.
2. Run `python3 -m venv venv && source venv/bin/activate`.
3. Install dependencies: `pip install -r requirements.txt`.
4. Start dev server: `./launcher.sh dev`.
```

---

## Testing Instructions

1. Open README and confirm only one CTA remains.
2. Verify START_HERE, SEARCH, and NAVIGATION links render correctly.
3. Confirm CONTRIBUTING quickstarts are succinct and non-overlapping.

---

## Success Criteria

- ✅ README has a single primary CTA.
- ✅ START_HERE provides three clear paths with time estimates.
- ✅ SEARCH and NAVIGATION docs exist and link to core docs.
- ✅ CONTRIBUTING quickstarts are simplified to three clear options.

---

## Rollback Procedure

1. Restore README CTA cluster and previous CONTRIBUTING instructions.
2. Remove START_HERE changes, SEARCH.md, NAVIGATION.md if needed.

