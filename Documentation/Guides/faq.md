# Frequently Asked Questions (FAQ)

Common questions about Sono-Eval, answered clearly and completely.

---

## For Candidates

### What is Sono-Eval and why am I using it?

Sono-Eval is an assessment system designed to help you understand your
strengths and identify growth areas. Unlike traditional tests, it:

- **Explains its scoring** - You'll see exactly why you received each score
- **Evaluates multiple dimensions** - Not just code quality, but design
  thinking, collaboration skills, and more
- **Provides actionable feedback** - Clear recommendations for improvement
- **Tracks your growth** - See how you progress over time

Think of it as a helpful coach, not just a grader!

### How does the assessment work?

The system evaluates your submissions across multiple "paths":

1. **Technical** - Code quality, algorithms, problem-solving
2. **Design** - Architecture decisions, design patterns
3. **Collaboration** - Documentation, code clarity, communication
4. **Problem Solving** - Your approach and methodology
5. **Communication** - How well you explain your thinking

Each path has specific metrics, and you'll get detailed feedback on each one.

### What does my score mean?

Scores range from 0-100:

- **80-100**: Excellent - You're demonstrating strong skills
- **60-79**: Good - You're on the right track with room to grow
- **40-59**: Developing - You're building skills, focus on the recommendations
- **0-39**: Learning - This is an area to focus your study

**Important**: Lower scores aren't failures—they're opportunities! The system
tells you exactly what to improve.

### What are "micro-motives" and why do they matter?

Micro-motives are your intrinsic motivations based on the "Dark Horse" model:

- **Mastery** - You love deeply understanding things
- **Exploration** - You enjoy trying new approaches
- **Collaboration** - You value teamwork and helping others
- **Innovation** - You seek creative solutions
- **Quality** - You care about craftsmanship and details

Understanding your micro-motives helps you:

- Play to your natural strengths
- Find work that energizes you
- Develop in ways that feel authentic

### Can I see examples of what "good" looks like?

Yes! Check out:

- [Examples Directory](resources/examples/) - Sample submissions with explanations
- [Learning Resources](resources/learning.md) - Tutorials and best practices
- Your assessment feedback - It highlights what you did well

### How can I improve my scores?

1. **Read your feedback carefully** - The system tells you exactly what to work on
2. **Focus on one area at a time** - Don't try to improve everything at once
3. **Look at the "strengths" section** - Do more of what's working
4. **Follow the recommendations** - They're tailored to you
5. **Iterate and resubmit** - Practice makes progress
6. **Use the learning resources** - We've curated helpful materials

### Is this system judging me?

No! Sono-Eval is a **learning tool**, not a judge. Think of it as:

- A mirror that helps you see your skills clearly
- A coach that provides specific guidance
- A tracker that shows your progress

Remember: Everyone starts somewhere, and growth is what matters.

### What if I disagree with my score?

That's okay! Here's what to do:

1. **Review the evidence** - The system shows specific examples
2. **Understand the criteria** - Check what's being measured
3. **Ask questions** - Talk to your mentor or team lead
4. **Learn and resubmit** - Show your improvement

The system isn't perfect, and human judgment always has a place.

### Can I retry or resubmit?

Absolutely! We encourage it. Each submission is a learning opportunity:

- Your history is saved (you can track progress)
- There's no penalty for multiple attempts
- Each attempt gets fresh, detailed feedback

### How long does an assessment take?

- **System processing**: Usually 5-30 seconds
- **Your time**: Depends on the challenge, but plan for:
  - Simple exercises: 15-30 minutes
  - Complex challenges: 1-3 hours
  - Take your time and do your best work!

---

## For Hiring Managers / Team Leads

### Why use Sono-Eval for candidate assessment?

Traditional coding tests often:

- Focus only on "right answers"
- Provide little meaningful feedback
- Miss important soft skills
- Don't help candidates grow

Sono-Eval provides:

- **Multi-dimensional evaluation** - Technical + design + collaboration
- **Explainable results** - Understand exactly why someone scored as they did
- **Candidate development** - Feedback helps everyone improve
- **Fair assessment** - Evidence-based, consistent criteria
- **Positive experience** - Candidates learn even if not hired

### How do I interpret assessment results?

Look at multiple dimensions:

1. **Overall Score** - Quick summary, but not the whole story
2. **Path Scores** - Where are their strengths?
3. **Micro-Motives** - What energizes them?
4. **Key Findings** - Specific observations
5. **Trend Over Time** - Are they improving?

**Pro Tip**: Two candidates with the same score might be very different! Look at
the details.

### What score should I expect from candidates?

Typical ranges by level:

- **Interns**: 40-60 (learning and growing)
- **Junior**: 50-70 (developing skills)
- **Mid-Level**: 65-80 (solid competence)
- **Senior**: 75-90 (strong across multiple areas)
- **Staff+**: 85+ (excellence plus teaching others)

**Important**: Scores depend on challenge difficulty. A 60 on a hard problem
might be better than 80 on an easy one.

### Can I customize the assessment criteria?

Yes! The system is configurable:

- Choose which paths to evaluate
- Adjust metric weights
- Fine-tune the ML model for your domain
- Create custom challenges

See the [Configuration Guide](user-guide/configuration.md) for details.

### How do I create effective challenges?

Good challenges:

1. **Have clear requirements** - Candidates know what's expected
2. **Are appropriately scoped** - Completable in allocated time
3. **Allow creativity** - Multiple valid approaches
4. **Test multiple skills** - Not just coding
5. **Have rubrics** - Clear evaluation criteria

See our [Challenge Design Guide](resources/challenge-design.md) (coming soon).

### What about bias and fairness?

We take this seriously:

- **Explainable AI** - Every score has evidence
- **Consistent criteria** - Same standards for everyone
- **Multiple dimensions** - Not just "one right way"
- **Focus on growth** - Everyone can improve
- **Regular audits** - Check for unintended biases

However, no system is perfect. Always use human judgment alongside automated assessment.

### How do I provide feedback to candidates?

The system generates feedback automatically, but you can:

1. **Review the automated feedback** - Make sure it's appropriate
2. **Add personal notes** - Human touch is valuable
3. **Schedule a debrief** - Discuss results together
4. **Create a growth plan** - If they're joining your team
5. **Share learning resources** - Help them improve

### Can I use this for team development?

Yes! Sono-Eval is great for:

- **Onboarding** - Assess and guide new hires
- **Growth planning** - Identify development areas
- **Skills tracking** - Monitor team capabilities
- **Learning culture** - Encourage continuous improvement

### What data is stored and for how long?

Stored data:

- Assessment results and scores
- Candidate submissions (anonymized option available)
- Progress history
- Configuration settings

**Retention**: Configurable, default is:

- Active candidates: Indefinitely
- Inactive: 2 years
- Deleted on request: 30 days

See [Privacy Policy](privacy.md) (coming soon) for details.

---

## Technical Questions

### What technologies does Sono-Eval use?

- **Backend**: Python, FastAPI
- **ML/NLP**: Hugging Face Transformers, T5, PEFT/LoRA
- **Storage**: PostgreSQL or SQLite, Redis
- **Analytics**: Apache Superset
- **Deployment**: Docker, Docker Compose

See [Architecture Overview](concepts/architecture.md) for details.

### Can I integrate Sono-Eval with my existing systems?

Yes! Integration options:

1. **REST API** - Standard HTTP endpoints
2. **Python SDK** - Direct integration in Python apps
3. **CLI** - Command-line automation
4. **Webhooks** - Event notifications (coming soon)

See [API Reference](user-guide/api-reference.md).

### What are the system requirements?

**Minimum** (development):

- CPU: 2 cores
- RAM: 4GB
- Disk: 5GB
- OS: Linux, macOS, Windows

**Recommended** (production):

- CPU: 4+ cores
- RAM: 8GB+
- Disk: 20GB+
- OS: Linux (Ubuntu/Debian)

**For ML** (T5 model):

- Additional RAM: +4GB
- GPU: Optional but recommended for large models

### Is Sono-Eval open source?

Yes! It's licensed under the MIT License.

- Source: [GitHub Repository](https://github.com/doronpers/sono-eval)
- Contributions welcome: See [Contributing Guide](../CONTRIBUTING.md)
- Issues and features: [GitHub Issues](https://github.com/doronpers/sono-eval/issues)

### Can I run Sono-Eval on-premises?

Absolutely! Sono-Eval is designed for on-premises deployment:

- No external API calls required
- Your data stays on your servers
- Full control over configuration
- Docker makes deployment easy

### What about security?

Security features:

- Configurable authentication (API keys, OAuth2)
- HTTPS/TLS support
- Input validation and sanitization
- Secure secret management
- Regular dependency updates

See [Security Guide](security.md) (coming soon) for best practices.

### How do I update Sono-Eval?

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run migrations (if any)
alembic upgrade head

# Restart services
./launcher.sh restart
```

See [Upgrade Guide](upgrade.md) (coming soon) for detailed instructions.

---

## Troubleshooting

### The assessment is taking a long time

Normal processing times:

- Simple code: 5-10 seconds
- Complex code: 15-30 seconds
- First run (model download): 2-5 minutes

If it's taking longer:

1. Check server logs: `./launcher.sh logs`
2. Verify system resources: `docker stats`
3. Check for network issues (model download)

### I'm getting low scores but don't know why

The system should provide detailed explanations. Check:

1. **Evidence section** - Specific examples from your code
2. **Metrics breakdown** - Which areas scored low
3. **Recommendations** - What to improve
4. **Learning resources** - Materials to help you

If feedback is unclear, please report it as a bug!

### The ML model isn't working

Common issues:

1. **First-time download** - T5 model takes time to download
2. **Insufficient disk space** - Model needs ~2GB
3. **Network issues** - Can't download model
4. **Fallback mode** - System uses heuristics instead

Check logs for details: `./launcher.sh logs`

### I found a bug or issue

Thank you for helping improve Sono-Eval!

1. **Check existing issues**: [GitHub Issues](https://github.com/doronpers/sono-eval/issues)
2. **Create new issue**: Include:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information
   - Logs (if applicable)

### Where can I get help?

- **Documentation**: You're reading it!
- **GitHub Issues**: Technical problems
- **GitHub Discussions**: Questions and ideas
- **Email**: <support@sono-eval.example>

---

## Best Practices

### Best Practices for Candidates

✅ Read feedback carefully
✅ Focus on learning, not just scores
✅ Ask questions if something is unclear
✅ Practice and resubmit
✅ Use learning resources
✅ Track your progress over time

❌ Don't game the system
❌ Don't ignore feedback
❌ Don't compare yourself to others (focus on your growth)

### For Evaluators

✅ Review automated feedback
✅ Add human context
✅ Focus on growth potential
✅ Use multiple data points
✅ Provide clear next steps
✅ Create a supportive environment

❌ Don't rely solely on scores
❌ Don't ignore context
❌ Don't skip the debrief

---

## Still Have Questions?

Can't find your answer? We're here to help!

- **Documentation**: Browse the [docs](README.md)
- **Examples**: Check [examples directory](resources/examples/)
- **Issues**: [GitHub Issues](https://github.com/doronpers/sono-eval/issues)
- **Email**: <support@sono-eval.example>

---

**Last Updated**: January 10, 2026
**Version**: 0.1.0
