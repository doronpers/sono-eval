# Learning Resources

This guide provides resources to help you understand and use the Sono-Eval system effectively.

## Core Concepts

### 1. Explainable AI in Assessment

**What is Explainable Scoring?**
- Every assessment score is backed by concrete evidence
- Transparent reasoning for all evaluations
- Natural language explanations for findings

**Why It Matters:**
- Build trust in automated assessments
- Help candidates understand their performance
- Enable continuous improvement

**Resources:**
- [Explainable AI - A Review](https://arxiv.org/abs/2001.00234)
- [LIME: Local Interpretable Model-Agnostic Explanations](https://arxiv.org/abs/1602.04938)

### 2. Multi-Path Assessment

**Assessment Paths:**
1. **Technical** - Code quality, algorithms, problem-solving
2. **Design** - Architecture, patterns, system design
3. **Collaboration** - Documentation, communication, teamwork
4. **Problem Solving** - Analytical thinking, approach
5. **Communication** - Clarity, documentation quality

**Benefits:**
- Comprehensive evaluation beyond just code
- Recognition of diverse strengths
- Personalized feedback

### 3. Dark Horse Model & Micro-Motives

Based on the tex-assist-coding model, we track intrinsic motivations:

**Micro-Motives:**
- **Mastery** - Drive to deeply understand and perfect skills
- **Exploration** - Willingness to try new approaches
- **Collaboration** - Team-oriented mindset
- **Innovation** - Creative problem-solving
- **Quality** - Attention to detail and craftsmanship

**Resources:**
- [Dark Horse Theory](https://www.darkhorseinstitute.com/)
- Research on individualized learning paths

### 4. Semantic Tagging with T5

**What is T5?**
- Text-to-Text Transfer Transformer from Google
- Pre-trained language model for various NLP tasks
- Frames all tasks as text generation

**PEFT & LoRA:**
- Parameter-Efficient Fine-Tuning
- LoRA: Low-Rank Adaptation of Large Language Models
- Efficient way to adapt large models to specific tasks

**Resources:**
- [T5 Paper: Exploring Transfer Learning](https://arxiv.org/abs/1910.10683)
- [LoRA: Low-Rank Adaptation](https://arxiv.org/abs/2106.09685)
- [Hugging Face PEFT Documentation](https://huggingface.co/docs/peft)

### 5. Hierarchical Memory (MemU)

**Concept:**
- Multi-level storage structure for candidate data
- Efficient retrieval with caching
- Version control for memory evolution

**Use Cases:**
- Track candidate progress over time
- Store assessment history
- Build comprehensive profiles

## Getting Started Tutorials

### Tutorial 1: Your First Assessment

```python
import asyncio
from sono_eval.assessment import AssessmentEngine, AssessmentInput, PathType

async def main():
    # Create engine
    engine = AssessmentEngine()
    
    # Sample code submission
    code = """
    def factorial(n):
        if n <= 1:
            return 1
        return n * factorial(n - 1)
    """
    
    # Create assessment input
    assessment_input = AssessmentInput(
        candidate_id="tutorial_user",
        submission_type="code",
        content={"code": code},
        paths_to_evaluate=[PathType.TECHNICAL]
    )
    
    # Run assessment
    result = await engine.assess(assessment_input)
    
    # Display results
    print(f"Overall Score: {result.overall_score}/100")
    print(f"Summary: {result.summary}")
    
    for path_score in result.path_scores:
        print(f"\n{path_score.path.value}:")
        for metric in path_score.metrics:
            print(f"  {metric.name}: {metric.score}")
            print(f"    {metric.explanation}")

asyncio.run(main())
```

### Tutorial 2: Working with Memory

```python
from sono_eval.memory import MemUStorage

# Initialize storage
storage = MemUStorage()

# Create candidate
memory = storage.create_candidate_memory(
    "candidate_001",
    initial_data={"name": "John Doe", "level": "junior"}
)

# Add assessment result
storage.add_memory_node(
    "candidate_001",
    memory.root_node.node_id,
    data={
        "assessment_date": "2026-01-10",
        "score": 85.5,
        "path": "technical"
    },
    metadata={"type": "assessment"}
)

# Retrieve memory
retrieved = storage.get_candidate_memory("candidate_001")
print(f"Candidate: {retrieved.root_node.data['name']}")
print(f"Nodes: {len(retrieved.nodes)}")
```

### Tutorial 3: Tag Generation

```python
from sono_eval.tagging import TagGenerator

# Initialize generator
generator = TagGenerator()

# Generate tags
code = """
async function fetchUserData(userId) {
    const response = await fetch(`/api/users/${userId}`);
    return response.json();
}
"""

tags = generator.generate_tags(code, max_tags=5)

for tag in tags:
    print(f"{tag.tag} ({tag.category}): {tag.confidence:.2f}")
```

### Tutorial 4: Using the CLI

```bash
# Create a candidate
sono-eval candidate create --id dev_001

# Run an assessment
sono-eval assess run \
    --candidate-id dev_001 \
    --file solution.py \
    --paths technical design \
    --output results.json

# View results
cat results.json | jq '.overall_score'

# List all candidates
sono-eval candidate list

# Generate tags
sono-eval tag generate --file mycode.js
```

### Tutorial 5: REST API Integration

```python
import requests

# Base URL
base_url = "http://localhost:8000"

# Create candidate
response = requests.post(
    f"{base_url}/api/v1/candidates",
    json={
        "candidate_id": "api_user_001",
        "initial_data": {"source": "api_integration"}
    }
)
print(response.json())

# Run assessment
assessment_response = requests.post(
    f"{base_url}/api/v1/assessments",
    json={
        "candidate_id": "api_user_001",
        "submission_type": "code",
        "content": {"code": "print('Hello World')"},
        "paths_to_evaluate": ["TECHNICAL"]
    }
)
result = assessment_response.json()
print(f"Score: {result['overall_score']}")
```

## Best Practices

### Assessment Design

1. **Use Multiple Paths**: Don't rely on a single dimension
2. **Provide Context**: Include problem statements and requirements
3. **Set Clear Criteria**: Define what constitutes good performance
4. **Review Evidence**: Check the evidence backing each score

### Memory Management

1. **Regular Updates**: Keep candidate memory current
2. **Hierarchical Organization**: Use levels meaningfully
3. **Clean Metadata**: Include relevant context in metadata
4. **Cache Awareness**: Understand caching for performance

### Tagging Strategy

1. **Consistent Taxonomy**: Maintain a stable tag vocabulary
2. **Quality over Quantity**: Focus on meaningful tags
3. **Regular Fine-tuning**: Update models with new data
4. **Validation**: Review auto-generated tags periodically

## Advanced Topics

### Custom Assessment Metrics

Extend the assessment engine with custom metrics:

```python
from sono_eval.assessment.models import ScoringMetric, Evidence, EvidenceType

custom_metric = ScoringMetric(
    name="Code Reusability",
    category="technical",
    score=90.0,
    weight=0.2,
    evidence=[
        Evidence(
            type=EvidenceType.CODE_QUALITY,
            description="Well-abstracted functions",
            source="module.py:15-30",
            weight=0.8
        )
    ],
    explanation="Code demonstrates excellent reusability",
    confidence=0.85
)
```

### Model Fine-Tuning

Fine-tune T5 for your specific domain:

```python
from sono_eval.tagging import TagGenerator

generator = TagGenerator()

# Prepare training data
training_data = [
    {
        "input": "code snippet 1",
        "output": "tag1, tag2, tag3"
    },
    # ... more examples
]

# Fine-tune
generator.fine_tune(
    training_data,
    epochs=3,
    batch_size=8
)
```

### Dashboard Configuration

Create custom Superset dashboards for your needs:

1. Connect to Sono-Eval database
2. Create datasets from assessment tables
3. Build visualizations
4. Compose dashboards
5. Share with team

## Troubleshooting

### Common Issues

**Issue: Low confidence scores**
- Solution: Provide more context and evidence in submissions
- Check assessment configuration

**Issue: Model loading errors**
- Solution: Verify model cache directory permissions
- Ensure sufficient disk space
- Check internet connection for downloads

**Issue: Memory storage errors**
- Solution: Check file permissions on storage path
- Verify disk space
- Review candidate ID format

## Further Reading

### Books
- "Explainable AI" by Leilani H. Gilpin
- "Dark Horse: Achieving Success Through the Pursuit of Fulfillment" by Todd Rose
- "Attention Is All You Need" (Transformer paper)

### Papers
- T5: Text-to-Text Transfer Transformer
- LoRA: Low-Rank Adaptation of Large Language Models
- PEFT: Parameter-Efficient Fine-Tuning

### Online Resources
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Apache Superset Documentation](https://superset.apache.org/docs/intro)

## Community

- GitHub Issues: Report bugs and request features
- Discussions: Share ideas and ask questions
- Contributing: See CONTRIBUTING.md for guidelines

---

Happy Learning! 📚
