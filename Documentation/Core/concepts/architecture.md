# Architecture Overview

Understanding the Sono-Eval system design, components, and data flow.

---

## System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        User Interfaces                           │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────┐  │
│  │     CLI     │  │  REST API   │  │    Python SDK        │  │
│  │   (Click)   │  │  (FastAPI)  │  │  (Direct Import)     │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬───────────┘  │
│         │                 │                     │              │
└─────────┼─────────────────┼─────────────────────┼──────────────┘
          │                 │                     │
┌─────────▼─────────────────▼─────────────────────▼──────────────┐
│                      Core Engine Layer                           │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────┐  ┌───────────────────┐                │
│  │ Assessment Engine  │  │  Semantic Tagger  │                │
│  │                    │  │                   │                │
│  │ • Path Evaluation  │  │ • T5 + PEFT/LoRA │                │
│  │ • Evidence Builder │  │ • Tag Generation  │                │
│  │ • Motive Tracker   │  │ • Fallback Logic  │                │
│  │ • Scoring Logic    │  │ • Category Infer  │                │
│  └─────────┬──────────┘  └─────────┬─────────┘                │
│            │                       │                            │
│            │    ┌──────────────────▼─────┐                     │
│            │    │    MemU Storage        │                     │
│            │    │                        │                     │
│            │    │ • Hierarchical Memory  │                     │
│            │    │ • LRU Caching          │                     │
│            │    │ • JSON Persistence     │                     │
│            │    │ • Path Traversal       │                     │
│            │    └────────────────────────┘                     │
│            │                                                    │
└────────────┼────────────────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────────────────┐
│                      Storage Layer                               │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────┐  ┌────────────┐  ┌─────────────────────┐      │
│  │ PostgreSQL │  │   Redis    │  │   File System       │      │
│  │ or SQLite  │  │            │  │                     │      │
│  │            │  │ • Caching  │  │ • MemU JSON Files   │      │
│  │ • Sessions │  │ • Tasks    │  │ • Model Cache       │      │
│  │ • Metadata │  │ • Sessions │  │ • TagStudio Files   │      │
│  └────────────┘  └────────────┘  └─────────────────────┘      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────────────────┐
│                     Analytics Layer                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐│
│  │              Apache Superset                               ││
│  │                                                            ││
│  │  • Candidate Performance Dashboard                        ││
│  │  • Cohort Analytics                                       ││
│  │  • Micro-Motive Analysis                                  ││
│  │  • Assessment Insights                                    ││
│  └────────────────────────────────────────────────────────────┘│
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. Assessment Engine

**Location**: `src/sono_eval/assessment/engine.py`

**Purpose**: Multi-path evaluation with explainable, evidence-based scoring.

**Key Features**:

- Evaluates submissions across multiple paths (Technical, Design, Collaboration, etc.)
- Generates evidence for every score
- Identifies micro-motives using Dark Horse model
- Provides natural language explanations
- Calculates confidence scores

**Data Flow**:

```
Input → Path Evaluation → Evidence Collection → Scoring → Explanation → Result
```

**Models** (`assessment/models.py`):

- `AssessmentInput` - Submission data
- `AssessmentResult` - Complete evaluation results
- `PathScore` - Individual path evaluation
- `ScoringMetric` - Individual metric within a path
- `Evidence` - Supporting evidence for scores
- `MicroMotive` - Motivation indicators

---

### 2. MemU Hierarchical Memory

**Location**: `src/sono_eval/memory/memu.py`

**Purpose**: Persistent, hierarchical storage for candidate data.

**Key Features**:

- Multi-level tree structure (configurable depth)
- JSON-based persistence
- LRU caching for performance
- Path traversal operations
- Version tracking

**Structure**:

```
CandidateMemory
└── Root Node (Level 0)
    ├── Child Node (Level 1)
    │   ├── Child Node (Level 2)
    │   │   └── ...
    │   └── Child Node (Level 2)
    └── Child Node (Level 1)
```

**Use Cases**:

- Store assessment history
- Track candidate progress
- Maintain contextual information
- Build comprehensive profiles

---

### 3. Semantic Tagging System

**Location**: `src/sono_eval/tagging/`

**Purpose**: Automated code tagging using T5 transformer model.

**Components**:

**Tag Generator** (`generator.py`):

- T5-base model with PEFT/LoRA fine-tuning
- Generates semantic tags from code
- Confidence scoring
- Category inference
- Fallback heuristics when model unavailable

**TagStudio** (`tagstudio.py`):

- File organization and management
- Automated tagging on import
- Tag-based search and retrieval
- Statistics and analytics
- Reverse indexing

**Model Architecture**:

```
Input Text → T5 Encoder → LoRA Adapter → T5 Decoder → Generated Tags
```

**Tag Categories**:

- Language features
- Design patterns
- Code quality indicators
- Architecture concepts
- Best practices

---

### 4. REST API

**Location**: `src/sono_eval/api/main.py`

**Purpose**: HTTP interface for programmatic access.

**Framework**: FastAPI (async Python web framework)

**Key Features**:

- Auto-generated OpenAPI documentation
- Async request handling
- Pydantic validation
- CORS support
- Health check endpoints

**Endpoints**:

- `/api/v1/assessments` - Assessment operations
- `/api/v1/candidates` - Candidate management
- `/api/v1/tags` - Tag generation
- `/api/v1/health` - Health check

**Authentication**: Configurable (API keys, OAuth2)

---

### 5. Command-Line Interface

**Location**: `src/sono_eval/cli/main.py`

**Purpose**: Terminal-based interface for all operations.

**Framework**: Click (Python CLI framework)

**Key Features**:

- Intuitive command structure
- Rich terminal output (colors, tables)
- Comprehensive help text
- JSON output support

**Command Groups**:

- `assess` - Assessment operations
- `candidate` - Candidate management
- `tag` - Tagging operations
- `server` - Server management
- `config` - Configuration display

---

## Data Flow

### Assessment Flow

```
1. User submits code
   ↓
2. Input validation (Pydantic)
   ↓
3. Assessment Engine processes
   │
   ├─→ Path 1: Technical
   │   ├─ Generate metrics
   │   ├─ Collect evidence
   │   ├─ Identify motives
   │   └─ Calculate score
   │
   ├─→ Path 2: Design
   │   └─ (same process)
   │
   └─→ Path N: ...
   ↓
4. Aggregate results
   ↓
5. Generate explanations
   ↓
6. Store in MemU
   ↓
7. Return to user
```

### Tag Generation Flow

```
1. User provides code/text
   ↓
2. Check model availability
   ↓
3a. Model Available:           3b. Model Unavailable:
    ├─ Tokenize input              ├─ Use fallback heuristics
    ├─ T5 + LoRA inference         └─ Pattern matching
    ├─ Generate tags
    └─ Calculate confidence
   ↓
4. Infer categories
   ↓
5. Sort by confidence
   ↓
6. Return top N tags
```

### Memory Storage Flow

```
1. Create/Retrieve candidate memory
   ↓
2. Check LRU cache
   │
   ├─ Hit: Return from cache
   │
   └─ Miss: Load from disk
       ↓
3. Perform operation (add node, update, etc.)
   ↓
4. Update cache
   ↓
5. Persist to JSON file
   ↓
6. Return result
```

---

## Deployment Architecture

### Docker Compose Deployment

```
┌─────────────────────────────────────────┐
│          Docker Network                 │
│                                         │
│  ┌──────────────┐                      │
│  │  Sono-Eval   │ :8000                │
│  │  Container   │                      │
│  └──────┬───────┘                      │
│         │                               │
│  ┌──────▼───────┐  ┌────────────────┐ │
│  │ PostgreSQL   │  │     Redis      │ │
│  │  :5432       │  │     :6379      │ │
│  └──────┬───────┘  └────────┬───────┘ │
│         │                    │         │
│  ┌──────▼────────────────────▼──────┐ │
│  │    Apache Superset :8088         │ │
│  └──────────────────────────────────┘ │
│                                         │
└─────────────────────────────────────────┘
         │
    ┌────▼────┐
    │  Volumes │
    ├──────────┤
    │ • data/  │
    │ • models/│
    └──────────┘
```

**Services**:

1. **sono-eval**: Main application
2. **postgres**: Database (optional, SQLite default)
3. **redis**: Caching and task queue
4. **superset**: Analytics dashboards

**Volumes**:

- Persistent data storage
- Model cache
- Configuration files

---

## Technology Stack

### Backend

- **Python 3.9+**: Core language
- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation

### Machine Learning

- **PyTorch**: Deep learning framework
- **Transformers**: Hugging Face library
- **T5**: Text-to-text model
- **PEFT/LoRA**: Efficient fine-tuning

### Storage

- **PostgreSQL**: Primary database (prod)
- **SQLite**: Default database (dev)
- **Redis**: Caching and sessions
- **JSON Files**: MemU storage

### Analytics

- **Apache Superset**: Visualization platform
- **SQL**: Data queries

### CLI

- **Click**: Command framework
- **Rich**: Terminal formatting
- **Tabulate**: Table display

### Deployment

- **Docker**: Containerization
- **Docker Compose**: Orchestration

---

## Design Patterns

### Assessment Engine

- **Strategy Pattern**: Different evaluation strategies per path
- **Builder Pattern**: Evidence and result construction
- **Template Method**: Standardized evaluation flow

### Memory System

- **Composite Pattern**: Hierarchical node structure
- **Repository Pattern**: Abstract storage access
- **Memento Pattern**: Version tracking

### API Layer

- **Dependency Injection**: FastAPI dependencies
- **Factory Pattern**: Application creation
- **Middleware Pattern**: Request/response processing

---

## Scalability Considerations

### Horizontal Scaling

- Stateless API (can run multiple instances)
- Redis for shared session state
- PostgreSQL for shared persistence
- Load balancer for distribution

### Vertical Scaling

- Async I/O for concurrency
- LRU caching reduces database load
- Lazy model loading saves memory
- Configurable worker processes

### Performance Optimization

- **Caching**:
  - Memory cache (MemU LRU)
  - Redis cache (assessment results)
  - Model cache (T5 on disk)
- **Async Operations**:
  - Non-blocking I/O
  - Concurrent assessments
  - Background tasks
- **Database**:
  - Connection pooling
  - Indexed queries
  - Batch operations

---

## Security Architecture

### Authentication & Authorization

- API key authentication (configurable)
- OAuth2 support (planned)
- Role-based access control (planned)

### Data Protection

- Input validation (Pydantic)
- SQL injection prevention (ORM)
- XSS prevention (FastAPI)
- CORS configuration
- HTTPS/TLS support

### Secret Management

- Environment variables
- Secure key storage
- Secret rotation support

---

## Monitoring & Observability

### Logging

- Structured logging (JSON)
- Log levels (DEBUG, INFO, WARNING, ERROR)
- Request/response logging
- Error tracking

### Metrics (Planned)

- Assessment latency
- API response times
- Cache hit rates
- Resource utilization

### Health Checks

- API health endpoint
- Database connectivity
- Redis connectivity
- Model availability

---

## Extension Points

### Custom Assessment Paths

Add new evaluation dimensions:

```python
class CustomPath(PathType):
    SECURITY = "security"

def evaluate_security_path(self, input_data):
    # Custom evaluation logic
    pass
```

### Custom Metrics

Define new scoring metrics:

```python
custom_metric = ScoringMetric(
    name="Custom Metric",
    category="custom",
    score=calculate_score(),
    evidence=collect_evidence(),
    explanation=generate_explanation()
)
```

### Model Fine-Tuning

Adapt T5 model to your domain:

```python
generator = TagGenerator()
generator.fine_tune(training_data, epochs=3)
```

### Custom Dashboards

Create Superset visualizations for your needs.

---

## Future Architecture

### Planned Enhancements

1. **Microservices**: Split into smaller services
2. **Message Queue**: Async assessment processing
3. **Real-time Updates**: WebSocket support
4. **Distributed Storage**: Multi-node MemU
5. **ML Pipeline**: Automated model training
6. **API Gateway**: Centralized routing
7. **Service Mesh**: Advanced networking

---

## See Also

- [API Reference](../user-guide/api-reference.md) - Endpoint details
- [Configuration](../user-guide/configuration.md) - System configuration
- [Development](../development/setup.md) - Dev environment setup
- [Implementation](../development/implementation.md) - Technical details

---

**Last Updated**: January 10, 2026
**Version**: 0.1.0
