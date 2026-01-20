# Workflow Examples

Real workflows from real scenarios. Learn by seeing complete examples from idea to deployment.

## 🐴 Dark Horse Note

**These are examples, not prescriptions.** Your workflow should match:

- **Your micro-motives** - What energizes you?
- **Your context** - Your project's reality
- **Your style** - How you work best

**Use these as inspiration, not templates to copy exactly.**

If an example workflow feels wrong for you, trust that feeling and adapt it. Your optimal workflow emerges from YOUR experience, not from copying others.

---

## How to Use These Examples

Each example shows:

1. **The Scenario** - What you're building and why
2. **Risk Assessment** - Helps you choose similar workflows
3. **Complete Workflow** - Step-by-step with timing
4. **Tools Used** - Which AI and other tools
5. **What Worked** - Successes
6. **What Could Improve** - Lessons learned

Pick the example closest to your situation!

---

## Example 1: Personal Learning Project

### Scenario

**Project:** Build a command-line weather app
**Developer:** Complete beginner learning Python
**Timeline:** Weekend project (1-2 days)
**Users:** Just yourself
**Stakes:** Very low - learning exercise

### Risk Assessment

```
Users: Just me
If it breaks: No problem, rebuild it
Sensitive data: No
Duration: Will use for a few weeks
Complexity: Simple (< 200 lines)
Change frequency: Rarely
```

**Conclusion:** Minimal workflow appropriate

### The Workflow

#### Stage 1: Planning (15 minutes)

**Three Questions:**

```
1. WHAT: CLI app that shows current weather for a city
2. TEST: Type "python weather.py London" → shows temperature and conditions
3. EDGE: What if city name is invalid or API is down?
```

**Tools:** Just your brain and a text file

#### Stage 2: Building (3 hours)

**With GitHub Copilot:**

```python
# 1. Start with comment
# Create a weather app that fetches weather data from OpenWeatherMap API

# Copilot suggests imports
import requests
import sys

# Define API key and endpoint
# Copilot completes with sensible defaults

# Create function to get weather
def get_weather(city):
    # Copilot suggests API call
    pass

# Create main function
def main():
    # Copilot suggests argument parsing
    pass

if __name__ == "__main__":
    main()
```

**Questions to ChatGPT:**

```
Q: "How do I get an API key from OpenWeatherMap?"
A: [ChatGPT explains process]

Q: "How do I parse command line arguments in Python?"
A: [ChatGPT shows sys.argv and argparse options]

Q: "What's a good free weather API for learning?"
A: [ChatGPT suggests OpenWeatherMap with free tier]
```

**Time breakdown:**

- Set up API key: 20 min
- Write main logic: 1 hour
- Add error handling: 30 min
- Make output pretty: 40 min
- Fix bugs: 30 min

#### Stage 3: Testing (20 minutes)

**Manual testing:**

```bash
# Test normal case
python weather.py London
# ✓ Works

# Test invalid city
python weather.py AsdfGhjkl
# ✓ Shows error message

# Test without arguments
python weather.py
# ✓ Shows usage instructions
```

**Done!** No automated tests needed for personal project.

#### Total Time: ~4 hours

**Stages used:** 2 (Planning, Building with testing)
**Stages skipped:** Review, Documentation, Deployment, Monitoring

### What Worked

✅ Quick planning kept me focused
✅ Copilot sped up boilerplate
✅ ChatGPT answered questions quickly
✅ Manual testing was sufficient
✅ Learned a lot in one weekend

### What Could Improve

💡 Should have git committed more often
💡 Could have added tests for practice
💡 Documentation would help if I return in 6 months

---

## Example 2: Side Project with Users

### Scenario

**Project:** URL shortener web app
**Developer:** Intermediate developer
**Timeline:** 2 weeks
**Users:** Friends and small community (50-100 people)
**Stakes:** Medium - people will use it

### Risk Assessment

```
Users: ~100 people
If it breaks: Annoying for users
Sensitive data: No (just URLs)
Duration: Will maintain for months
Complexity: Medium (database, API, frontend)
Change frequency: Weekly updates planned
```

**Conclusion:** Balanced workflow with testing and review

### The Workflow

#### Week 1: Planning & Setup (Day 1-2)

**Day 1: Requirements (2 hours)**

With Claude:

```
You: "Help me plan a URL shortener. What features should I include in MVP?"

Claude: "Let's think through this:

MVP Features:
1. Shorten URL (POST endpoint)
2. Redirect (GET /{short_code})
3. Simple frontend form
4. Basic analytics (click count)

Future features (not MVP):
- Custom short codes
- Expiration dates
- User accounts
- Dashboard

Tech stack suggestions:
- FastAPI (Python backend)
- SQLite (database)
- Vanilla JS (frontend)
- Deployed on Railway

Does this match your vision?"

You: "Perfect! Let's detail the API design."

Claude: [provides API contract]
```

**Day 2: Setup (3 hours)**

- Initialize git repo
- Set up FastAPI project
- Create database schema
- Implement basic endpoints with Copilot

#### Week 1: Building (Day 3-5)

**Day 3: Backend (6 hours)**

Using GitHub Copilot:

```python
# Copilot completes as I type

# Database models
class URLMapping(Base):
    # Copilot suggests fields

# API endpoints
@app.post("/shorten")
async def shorten_url(...):
    # Copilot implements logic

@app.get("/{short_code}")
async def redirect(...):
    # Copilot implements redirect
```

Questions to ChatGPT when stuck:

```
Q: "How do I generate short random codes?"
Q: "What's the best way to validate URLs?"
Q: "How do I handle concurrent database writes?"
```

**Day 4: Frontend (4 hours)**

- Simple HTML/CSS/JS form
- Copilot helps with JavaScript
- Test manually in browser

**Day 5: Integration (4 hours)**

- Connect frontend to backend
- Fix CORS issues (ChatGPT helped)
- Test complete flow

#### Week 2: Testing & Deployment (Day 6-10)

**Day 6: Testing (4 hours)**

Generate tests with ChatGPT:

```
You: "Create pytest tests for this URL shortener:
[paste code]

Include:
- Test shorten endpoint with valid URL
- Test shorten endpoint with invalid URL
- Test redirect with existing code
- Test redirect with missing code"

ChatGPT: [generates comprehensive test suite]
```

Run tests, fix bugs found: 2 hours

**Day 7: Review (3 hours)**

Security review with Claude:

```
You: "Security audit this URL shortener code:
[paste complete codebase]

Especially check:
- URL validation
- SQL injection
- Rate limiting needs"

Claude: [identifies issues:
- Missing URL validation
- No rate limiting
- Should sanitize URLs
]
```

Fix security issues: 2 hours

**Day 8-9: Deployment (5 hours)**

- Set up Railway account
- Configure environment variables
- Deploy and test
- Fix deployment issues
- Set up custom domain

**Day 10: Documentation (2 hours)**

- Write README
- Add API documentation
- Create usage examples
- Share with friends

#### Total Time: ~35 hours over 2 weeks

**Stages used:** Planning, Building, Testing, Review, Deployment, Documentation

### What Worked

✅ Claude's planning saved time
✅ Copilot accelerated coding
✅ AI-generated tests were comprehensive
✅ Security review caught issues early
✅ Users happy with result

### What Could Improve

💡 Should have set up monitoring
💡 Could have used CI/CD
💡 More frequent git commits
💡 Should have tested mobile view

---

## Example 3: Client Project (Production)

### Scenario

**Project:** Customer dashboard for e-commerce analytics
**Developer:** Professional developer, client work
**Timeline:** 6 weeks
**Users:** Client's customers (1000+ users)
**Stakes:** High - client's business depends on it

### Risk Assessment

```
Users: 1000+ paying customers
If it breaks: Client loses money, reputation damage
Sensitive data: Yes (customer data, sales data)
Duration: Years (ongoing maintenance contract)
Complexity: High (multiple services, integrations)
Change frequency: Continuous updates
```

**Conclusion:** Comprehensive workflow required

### The Workflow

#### Week 1: Discovery & Design

**Days 1-2: Requirements (12 hours)**

With client:

- Gather requirements
- Define user stories
- Prioritize features
- Define success metrics

With Claude:

```
You: "Review these requirements for completeness:
[paste requirements doc]

Check for:
- Missing edge cases
- Security considerations
- Scalability concerns
- Integration points"

Claude: [detailed analysis with gaps identified]
```

**Days 3-5: Architecture Design (20 hours)**

With team and ChatGPT:

- Design database schema
- Plan API architecture
- Choose tech stack
- Design security model
- Plan deployment strategy

Document everything:

```markdown
## Architecture

### Tech Stack
- Backend: FastAPI + PostgreSQL
- Frontend: React + TypeScript
- Auth: OAuth 2.0 with JWT
- Deployment: AWS ECS
- Monitoring: DataDog

### Database Schema
[detailed tables and relationships]

### API Design
[complete API specification]

### Security Model
[authentication, authorization, data protection]
```

#### Week 2-4: Implementation

**Iterative Development:**

Each feature follows this pattern:

**Day N: Feature Planning (2 hours)**

```
1. Review user story
2. Break into tasks
3. Design tests first (TDD)
4. Plan implementation
```

**Day N: Building (4-6 hours)**

```
1. Write failing tests
2. Implement with Copilot
3. Run tests, iterate
4. Commit frequently
```

**Day N: Review (1-2 hours)**

```
1. Self-review checklist
2. AI review (Claude)
3. Create pull request
4. Team review
5. Address feedback
```

**Repeat for each feature**

**Tools:**

- GitHub Copilot: Real-time coding
- ChatGPT: Complex algorithm design
- Claude: Security reviews
- Team: Peer reviews

**Git workflow:**

```bash
# Create feature branch
git checkout -b feature/customer-analytics

# Frequent commits
git commit -m "Add database models"
git commit -m "Add API endpoint"
git commit -m "Add tests"
git commit -m "Handle edge cases"

# Push and create PR
git push origin feature/customer-analytics
```

#### Week 5: Integration & Testing

**Integration Testing (10 hours)**

```python
# Test complete user journeys
def test_analytics_dashboard_flow():
    # 1. User logs in
    # 2. Fetches analytics
    # 3. Filters by date range
    # 4. Exports data
    # All should work end-to-end
```

**Performance Testing (8 hours)**

```
- Load test with 1000 concurrent users
- Optimize slow queries
- Add caching where needed
- Test with production-like data
```

**Security Audit (12 hours)**

```
With Claude:
- Review all endpoints
- Check authentication
- Verify authorization
- Test input validation
- Check for OWASP Top 10

External:
- Penetration testing
- Dependency vulnerability scan
```

**User Acceptance Testing (10 hours)**

```
- Client reviews on staging
- Gather feedback
- Make adjustments
- Repeat until approved
```

#### Week 6: Deployment & Launch

**Pre-deployment (8 hours)**

```
- Final security check
- Final performance check
- Backup plan ready
- Rollback plan tested
- Monitoring configured
- Documentation complete
```

**Deployment (4 hours)**

```
1. Deploy to staging
2. Run all tests on staging
3. Client final approval
4. Deploy to production
5. Smoke tests on production
6. Monitor closely
```

**Post-deployment (Ongoing)**

```
- Monitor errors (DataDog)
- Monitor performance
- Respond to issues
- Gather user feedback
- Plan next iteration
```

#### Total Time: 240 hours over 6 weeks

**Stages used:** All stages, multiple reviews, comprehensive testing

### What Worked

✅ Thorough planning prevented rework
✅ TDD caught bugs early
✅ Multiple AI agents provided different perspectives
✅ Team reviews caught issues AI missed
✅ Monitoring helped catch production issues quickly
✅ Client very satisfied

### What Could Improve

💡 Could have parallelized some work with more team members
💡 More frequent client demos would have caught UX issues sooner
💡 Documentation could be even more detailed

---

## Example 4: Startup MVP

### Scenario

**Project:** Social media scheduling tool (SaaS)
**Team:** 2 co-founders
**Timeline:** 4 weeks to launch
**Users:** Early adopters (targeting 100 users in month 1)
**Stakes:** High - business depends on it, but speed critical

### Risk Assessment

```
Users: Starting with 100, growing
If it breaks: Bad for reputation, but can fix quickly
Sensitive data: Yes (social media credentials)
Duration: Will iterate for years
Complexity: High
Change frequency: Daily updates
```

**Conclusion:** Fast but safe workflow - balance speed and quality

### The Workflow

#### Week 1: Speed Planning

**Day 1: Core Features Only (4 hours)**

Brutal prioritization:

```markdown
## MUST HAVE (Week 1)
- [ ] Connect Twitter account
- [ ] Schedule one tweet
- [ ] View scheduled tweets

## SHOULD HAVE (Week 2)
- [ ] Edit scheduled tweets
- [ ] Delete scheduled tweets
- [ ] Connect multiple accounts

## NICE TO HAVE (After launch)
- [ ] Instagram support
- [ ] Analytics
- [ ] Team features
- Everything else
```

**Day 2-5: Build MVP (30 hours)**

Parallel work:

- Founder 1: Frontend (React)
- Founder 2: Backend (FastAPI)

**Using AI heavily:**

```
Copilot: Generate boilerplate fast
ChatGPT: Quick questions while coding
Claude: Quick security check on OAuth flow
```

**Cutting corners strategically:**

- SQLite instead of PostgreSQL (can migrate later)
- Basic CSS instead of perfect design
- Manual testing instead of full test suite
- Deploy to Render free tier

#### Week 2: Critical Features

**Day 6-10: Must-have features (35 hours)**

Features that would embarrass us if missing:

- Edit scheduled posts
- Error handling
- Basic user auth
- Minimal UI polish

**Testing:**

- Manual testing of critical paths
- No automated tests yet (adding later)
- Both founders test everything

#### Week 3: Security & Reliability

**Day 11-12: Security (12 hours)**

Can't compromise on security:

```
With Claude:
- Audit OAuth implementation
- Check credential storage
- Verify API security
- Add rate limiting
```

**Day 13-15: Reliability (18 hours)**

Make it not break:

- Add error handling everywhere
- Add logging
- Add health checks
- Test failure scenarios

#### Week 4: Launch Prep

**Day 16-17: Polish (12 hours)**

- Fix obvious UI bugs
- Add loading states
- Improve error messages
- Test on mobile

**Day 18: Deploy (6 hours)**

- Deploy to production
- Set up monitoring
- Test live
- Fix immediate issues

**Day 19: Soft Launch (4 hours)**

- Launch to 10 friends
- Monitor closely
- Fix urgent bugs
- Gather feedback

**Day 20: Public Launch**

- Post on Product Hunt
- Monitor like crazy
- Fix bugs in real-time
- Iterate based on feedback

#### Total Time: 120 hours over 4 weeks

### What Worked

✅ Brutal prioritization kept us focused
✅ AI tools let us move incredibly fast
✅ Security review prevented disaster
✅ Soft launch caught major bugs
✅ Shipped in 4 weeks (would have taken 3 months normally)

### What Could Improve

💡 Should have added analytics from day 1
💡 No automated tests hurt when bugs appeared
💡 Code quality is technical debt we'll pay later
💡 Should have documented architecture better

### What We're Adding Post-Launch

Now that we're live, adding gradually:

```
Week 5: Add automated tests for critical paths
Week 6: Refactor messy code
Week 7: Add proper monitoring
Week 8: Improve documentation
```

**Strategy:** Ship fast, improve continuously

---

## Choosing Your Workflow

### If you're like Example 1 (Learning)

→ Use minimal workflow
→ Focus on functionality over process
→ Learn by doing

### If you're like Example 2 (Side Project)

→ Use balanced workflow
→ Add tests and review
→ Make it maintainable

### If you're like Example 3 (Client Work)

→ Use comprehensive workflow
→ Don't skip stages
→ Quality is essential

### If you're like Example 4 (Startup)

→ Use fast workflow with strategic corners cut
→ Security is non-negotiable
→ Improve after launch

## Common Patterns Across Examples

**Everyone should:**
✅ Plan before coding (even if just 5 minutes)
✅ Test that it works
✅ Use git version control
✅ Get some form of review

**Add as stakes increase:**

- More comprehensive planning
- Automated testing
- Multiple reviews
- Security audits
- Monitoring

**AI helps most with:**

- Planning (brainstorming, gap finding)
- Building (autocomplete, generation)
- Testing (test generation)
- Review (bug finding, security)

## Next Steps

**Customize your workflow:**
→ **[Choosing Stages](choosing-stages.md)** - Pick what you need

**Understand the stages:**
→ **[Stages of Development](stages-of-development.md)** - Deep dive into each

**Use AI effectively:**
→ **[Using AI in Workflow](using-ai-in-workflow.md)** - Single vs multi-agent

**See it evolve:**
→ **[Evolving Your Process](evolving-your-process.md)** - How workflows mature

---

**Remember:** Your first workflow will be imperfect. That's OK! Iterate and improve! 🚀
