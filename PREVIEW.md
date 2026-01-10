# Sono-Eval System Preview

## 🎯 What is Sono-Eval?

**Sono-Eval** is an explainable multi-path developer assessment system that:
- Provides detailed explanations for every score
- Evaluates multiple skill dimensions (technical, design, collaboration, problem-solving)
- Tracks candidate progress over time
- Offers actionable feedback for improvement

---

## 📱 User Interfaces

### 1. **Mobile Companion Web Interface** (`/mobile/`)

A mobile-optimized, interactive assessment experience with:

#### **Home Page** (`/mobile/`)
- Welcome screen with hero section
- Explanation of what makes Sono-Eval different
- Privacy information
- "Let's Get Started" call-to-action
- Expandable "Learn more" section

#### **Start Page** (`/mobile/start`)
- Candidate information collection
- Simple, friendly onboarding

#### **Path Selection** (`/mobile/paths`)
- Interactive cards for each assessment path:
  - ⚙️ **Technical Skills** (15-20 min) - Code quality, architecture, testing
  - 🎨 **Design Thinking** (10-15 min) - Problem analysis, solution design
  - 🤝 **Collaboration** (10-15 min) - Communication, teamwork, code review
  - 🧩 **Problem Solving** (15-20 min) - Analytical thinking, debugging
- "Learn more" buttons for detailed explanations
- Real-time selection summary with estimated time
- Visual checkmarks for selected paths

#### **Assessment Page** (`/mobile/assess`)
- Interactive assessment interface
- Progress tracking
- Personalized based on selected paths

#### **Results Page** (`/mobile/results`)
- Overall score display
- Path-by-path breakdown
- Strengths and improvement areas
- Actionable recommendations
- Share functionality

**Design Features:**
- Modern, clean mobile-first design
- Smooth animations and transitions
- Progress bars and visual feedback
- Responsive layout
- Touch-optimized interactions

---

### 2. **REST API** (`http://localhost:8000`)

FastAPI-based REST API with:

#### **Interactive Documentation**
- Swagger UI at `/docs`
- ReDoc at `/redoc`
- Auto-generated from code

#### **Key Endpoints:**

**Health & Status:**
- `GET /` - API information
- `GET /health` - Health check
- `GET /status` - Detailed status

**Assessments:**
- `POST /api/v1/assessments` - Create assessment
- `GET /api/v1/assessments/{id}` - Get assessment

**Candidates:**
- `POST /api/v1/candidates` - Create candidate
- `GET /api/v1/candidates` - List candidates
- `GET /api/v1/candidates/{id}` - Get candidate
- `DELETE /api/v1/candidates/{id}` - Delete candidate

**Tagging:**
- `POST /api/v1/tags/generate` - Generate semantic tags
- `POST /api/v1/files/upload` - Upload file

**Mobile API:**
- `POST /api/mobile/assess` - Submit mobile assessment
- `GET /api/mobile/explain/{path}` - Get path explanation

---

### 3. **Command-Line Interface (CLI)**

Rich, interactive CLI with color-coded output:

#### **Command Structure:**

```bash
sono-eval
├── assess
│   └── run          # Run assessment
├── candidate
│   ├── create       # Create candidate
│   ├── show         # Show candidate info
│   ├── list         # List candidates
│   └── delete        # Delete candidate
├── tag
│   └── generate     # Generate tags
├── server
│   └── start        # Start API server
└── config
    └── show         # Show configuration
```

#### **Example Usage:**

```bash
# Create a candidate
sono-eval candidate create --id candidate_001

# Run assessment
sono-eval assess run \
  --candidate-id candidate_001 \
  --file solution.py \
  --paths technical design

# Generate tags
sono-eval tag generate --file mycode.js --max-tags 5

# Start server
sono-eval server start --reload
```

**CLI Features:**
- Rich formatted tables for results
- Color-coded output (green for success, red for errors)
- Progress indicators
- JSON output option
- Interactive confirmations

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Sono-Eval System                        │
├─────────────────────────────────────────────────────────────┤
│  Interfaces:  CLI  │  REST API  │  Mobile Web               │
├─────────────────────────────────────────────────────────────┤
│  Core Engine:                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  Assessment  │  │   Semantic   │  │    Memory    │    │
│  │    Engine    │  │    Tagging   │  │   (MemU)     │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
├─────────────────────────────────────────────────────────────┤
│  Storage:  PostgreSQL  │  Redis  │  File System            │
├─────────────────────────────────────────────────────────────┤
│  Analytics:  Apache Superset Dashboards                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 How to Run

### Option 1: Docker (Recommended)
```bash
./launcher.sh start
```

**Access Points:**
- API Server: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Mobile UI: http://localhost:8000/mobile/
- Superset: http://localhost:8088 (admin/admin)

### Option 2: Development Mode
```bash
./launcher.sh dev
source venv/bin/activate
sono-eval server start
```

---

## 🎨 UI/UX Highlights

### Mobile Interface Design:
- **Color Scheme:**
  - Primary: #2196F3 (Blue)
  - Secondary: #FF9800 (Orange)
  - Success: #4CAF50 (Green)
  - Clean, modern Material Design-inspired

- **Typography:**
  - System fonts for native feel
  - Clear hierarchy
  - Readable sizes

- **Interactions:**
  - Smooth transitions
  - Touch-friendly buttons
  - Visual feedback on actions
  - Progress indicators

- **Layout:**
  - Mobile-first responsive
  - Card-based design
  - Clear information hierarchy
  - Accessible and intuitive

---

## 📊 Assessment Features

### Multi-Path Evaluation:
1. **Technical Skills** - Code quality, architecture, best practices
2. **Design Thinking** - Problem analysis, solution design
3. **Collaboration** - Communication, teamwork
4. **Problem Solving** - Analytical thinking, debugging

### Assessment Output:
- Overall score (0-100)
- Confidence level
- Path-specific scores
- Detailed explanations
- Key findings
- Actionable recommendations
- Strengths identification
- Improvement areas

---

## 🔧 Technical Stack

- **Backend:** FastAPI (Python)
- **Frontend:** Jinja2 templates, vanilla JavaScript
- **ML/NLP:** PyTorch, Transformers, PEFT
- **Storage:** PostgreSQL, Redis
- **Analytics:** Apache Superset
- **CLI:** Click, Rich
- **Deployment:** Docker, Docker Compose

---

## 📝 Key Differentiators

1. **Explainable** - Every score comes with clear reasoning
2. **Multi-Path** - Evaluates different skill dimensions
3. **Growth-Focused** - Provides actionable feedback
4. **Interactive** - Mobile-optimized experience
5. **Personalized** - Candidates choose their focus areas
6. **Transparent** - Clear about what's being assessed

---

## 🎯 Use Cases

- **Technical Hiring** - Assess developer candidates
- **Skill Development** - Help developers identify growth areas
- **Team Assessment** - Evaluate team capabilities
- **Learning Tool** - Educational assessment platform
- **Code Review** - Automated code quality assessment

---

*For more information, see the [README.md](README.md) and [Documentation](Documentation/README.md)*
