# Choosing Stages for Your Workflow

Not every project needs every stage. Learn how to choose the right stages for your situation.

## The Core Question

**What's at stake if this code fails?**

```
Low stakes → Fewer stages
High stakes → More stages
```

## The Risk-Based Approach

### Level 1: Throwaway Code (Minutes)

**Examples:**

- Learning exercises
- Quick experiments
- Temporary scripts
- Testing an idea

**Minimum stages:**

```
1. Build
2. Run it once
Done!
```

**Optional stages:**

- Planning (if unclear what to build)
- Testing (if you want to verify)

**Skip:**

- Documentation
- Review
- Deployment
- Everything else

**Example workflow:**

```
1. Have idea
2. Open editor
3. Code for 10 minutes
4. Run it
5. See results
6. Delete or keep
```

### Level 2: Personal Projects (Hours-Days)

**Examples:**

- Side projects
- Portfolio pieces
- Small tools for yourself
- Learning projects

**Minimum stages:**

```
1. Planning (quick - 5 min)
2. Building
3. Testing (manual is fine)
```

**Consider adding:**

- Documentation (future-you will thank you)
- Version control (git commits)
- Error handling

**Can skip:**

- Formal review
- Comprehensive testing
- Production deployment

**Example workflow:**

```
1. Write down Three Questions
2. Code the feature
3. Test manually
4. Fix obvious bugs
5. Commit to git
6. Move to next feature
```

### Level 3: Shared Projects (Days-Weeks)

**Examples:**

- Team projects
- Open source contributions
- Projects others will use
- Your startup MVP

**Recommended stages:**

```
1. Planning (document requirements)
2. Building (with version control)
3. Testing (automated tests)
4. Review (self or peer)
5. Deployment (to staging/production)
```

**Don't skip:**

- Planning (team needs alignment)
- Testing (others depend on it working)
- Review (catch issues early)

**Optional:**

- Security audit (if not handling sensitive data)
- Performance testing (if not many users)

**Example workflow:**

```
1. Write user stories or requirements
2. Break into tasks
3. Build feature with tests
4. Self-review
5. Create pull request
6. Address feedback
7. Merge and deploy
```

### Level 4: Production Systems (Weeks-Months)

**Examples:**

- Client projects
- Production applications
- Systems with users
- Revenue-generating products

**Required stages:**

```
1. Design (architecture)
2. Planning (detailed requirements)
3. Building (with best practices)
4. Testing (comprehensive)
5. Review (multiple reviewers)
6. Security audit
7. Deployment (with rollback plan)
8. Monitoring
```

**Never skip:**

- Planning (requirements prevent rework)
- Testing (bugs cost users and money)
- Review (quality matters)
- Security (breaches are expensive)
- Monitoring (need to know when things break)

**Example workflow:**

```
1. Gather requirements from stakeholders
2. Design architecture and database
3. Plan sprint/milestone
4. Build with TDD
5. Write integration tests
6. Self-review
7. AI code review
8. Peer review
9. Security scan
10. Deploy to staging
11. QA testing
12. Deploy to production
13. Monitor metrics
```

## Stage Selection Matrix

| Stage | Throwaway | Personal | Shared | Production |
|-------|-----------|----------|--------|------------|
| Design | ❌ | ❌ | 📝 | ✅ |
| Planning | 📝 | 📝 | ✅ | ✅ |
| Building | ✅ | ✅ | ✅ | ✅ |
| Testing | 📝 | 📝 | ✅ | ✅ |
| Review | ❌ | 📝 | ✅ | ✅ |
| Security | ❌ | ❌ | 📝 | ✅ |
| Deploy | ❌ | 📝 | ✅ | ✅ |
| Monitor | ❌ | ❌ | 📝 | ✅ |

Legend:

- ✅ = Required
- 📝 = Recommended
- ❌ = Optional

## Factor-Based Selection

### Factor 1: Number of Users

**Just you:**

```
→ Fewer stages, focus on functionality
→ Skip: Review, comprehensive testing
→ Keep: Basic testing to ensure it works
```

**Small team (2-10):**

```
→ Add review stage
→ Add documentation
→ Keep stages lightweight but present
```

**Many users (100+):**

```
→ All stages required
→ Can't afford downtime
→ Reputation at stake
```

**Thousands of users:**

```
→ Add: Performance testing
→ Add: Load testing
→ Add: Gradual rollout
→ Add: Feature flags
```

### Factor 2: Data Sensitivity

**No sensitive data:**

```
→ Standard security practices
→ Skip: Security audit
→ Keep: Input validation
```

**User emails/names:**

```
→ Add: Security review
→ Add: GDPR compliance checks
→ Keep: Encryption in transit
```

**Passwords/payment info:**

```
→ Required: Security audit
→ Required: Penetration testing
→ Required: Compliance review
→ Consider: External audit
```

**Healthcare/financial:**

```
→ All security stages mandatory
→ Add: Compliance audit
→ Add: Legal review
→ Consider: Certification
```

### Factor 3: Code Complexity

**Single file, < 100 lines:**

```
→ Minimal stages
→ Self-review sufficient
→ Manual testing OK
```

**Multiple files, < 1000 lines:**

```
→ Add: Automated tests
→ Add: Code review
→ Keep: Documentation
```

**Large codebase, > 5000 lines:**

```
→ Required: Comprehensive tests
→ Required: Multiple reviews
→ Required: Architecture documentation
→ Consider: Performance testing
```

**Microservices, multiple repos:**

```
→ All stages for each service
→ Add: Integration testing
→ Add: API contract testing
→ Add: Service monitoring
```

### Factor 4: Change Frequency

**One-time script:**

```
→ Minimal stages
→ Focus on: Does it work now?
→ Skip: Maintenance, monitoring
```

**Monthly updates:**

```
→ Standard stages
→ Add: Documentation (you'll forget)
→ Keep: Version control
```

**Daily deployments:**

```
→ All stages streamlined
→ Required: CI/CD pipeline
→ Required: Automated testing
→ Required: Monitoring
```

**Continuous deployment:**

```
→ Fully automated pipeline
→ Required: Feature flags
→ Required: Automated rollback
→ Required: Canary deployments
```

## Decision Framework

### Step 1: Assess Your Project

Answer these questions:

```markdown
1. Who will use this? (Just me / Team / Public)
2. What if it breaks? (No problem / Inconvenient / Serious issue)
3. Does it handle sensitive data? (No / Yes)
4. How long will it be used? (Once / Months / Years)
5. How complex is it? (< 100 lines / < 1000 lines / > 1000 lines)
6. How often will it change? (Once / Sometimes / Frequently)
```

### Step 2: Apply the Rules

**If mostly "low risk" answers:**

```
→ Use Level 1 or 2 workflow
→ Minimum stages
→ Focus on speed and learning
```

**If mixed answers:**

```
→ Use Level 3 workflow
→ Standard stages
→ Balance speed and quality
```

**If mostly "high risk" answers:**

```
→ Use Level 4 workflow
→ All stages
→ Focus on quality and reliability
```

### Step 3: Customize

Start with the recommended level, then:

**Add stages if:**

- You keep finding bugs after deployment
- Security is more important than you thought
- More people are using it than expected
- Compliance requirements change

**Remove stages if:**

- They're not adding value
- Simpler process works fine
- You're moving too slowly
- The project is simpler than expected

## Common Patterns

### Pattern 1: The Minimalist

**For:** Solo developers, personal projects

```
Stages: Plan (2 min) → Build → Test manually
Time: Fast
Quality: Good enough
Best for: Learning, experiments, personal tools
```

**Skip:**

- Formal review
- Automated testing
- Documentation
- Deployment pipeline

### Pattern 2: The Balanced Developer

**For:** Small teams, side projects with users

```
Stages: Plan → Build → Test → Self-review → Deploy
Time: Moderate
Quality: Good
Best for: Most side projects, MVPs, small teams
```

**Skip:**

- Comprehensive security audit
- Performance testing
- Multiple reviews
- Complex deployment

### Pattern 3: The Professional

**For:** Production systems, client work

```
Stages: Design → Plan → Build → Test → Review → Security → Deploy → Monitor
Time: Thorough
Quality: High
Best for: Client work, production apps, revenue systems
```

**Don't skip:** Anything

### Pattern 4: The Startup

**For:** Fast-moving startups, rapid iteration

```
Stages: Quick Plan → Build → Basic Test → Ship → Monitor → Learn
Time: Very fast
Quality: "Good enough to test market"
Best for: Finding product-market fit
```

**Skip initially, add later:**

- Comprehensive tests
- Perfect architecture
- Full documentation
- Complex security (start with basics)

## Stage Efficiency Tips

### Making Planning Faster

**Instead of:**

```
Writing 10-page requirements document
Creating detailed diagrams
Planning every edge case
```

**Try:**

```
Answer Three Questions (2 min)
Sketch main flow on paper (5 min)
List must-have features (5 min)
```

### Making Testing Faster

**Instead of:**

```
Writing tests for every line
100% code coverage
Every possible edge case
```

**Try:**

```
Test happy path
Test one edge case per feature
Test what breaks in production
```

### Making Review Faster

**Instead of:**

```
Scheduling formal review meeting
Waiting for team review
Comprehensive audit
```

**Try:**

```
Quick self-review checklist
AI review in 2 minutes
Peer review async in PR
```

## When to Add Stages

### Start Minimal, Add When Needed

**Add Security when:**

- Handling user passwords
- Processing payments
- Storing personal data
- Getting security questions from users

**Add Performance Testing when:**

- Users complain about speed
- You expect traffic spikes
- You're adding caching
- Database queries are slow

**Add Documentation when:**

- New team members join
- You forget how your own code works
- Others will use your API
- It's been more than a month

**Add Monitoring when:**

- You have users in production
- You need to know when things break
- You want to understand usage
- You're making money from this

## Case Studies

### Case Study 1: Learning Exercise

**Project:** Build a calculator in Python
**Risk Level:** Zero
**Workflow:**

```
1. Open editor
2. Write calculator code
3. Test with a few numbers
4. Done

Total time: 30 minutes
Stages used: 1 (Build + manual test)
```

**What they skipped:** Everything else
**Result:** Learned Python, code deleted after

### Case Study 2: Personal Blog

**Project:** Static blog with markdown
**Risk Level:** Low
**Workflow:**

```
1. Plan structure (20 min)
2. Build with generator (2 hours)
3. Test locally (10 min)
4. Deploy to GitHub Pages (15 min)
5. Write first post

Total time: 3 hours
Stages used: 3 (Plan, Build, Test, Deploy)
```

**What they skipped:** Review, security audit, monitoring
**Result:** Blog running, no issues

### Case Study 3: Startup MVP

**Project:** SaaS product for team collaboration
**Risk Level:** High
**Workflow:**

```
1. Design system (1 week)
2. Plan sprints (ongoing)
3. Build features (4 weeks)
4. Write tests (ongoing with build)
5. Security review (2 days)
6. Deploy to production (1 day)
7. Monitor and iterate (ongoing)

Total time: 6 weeks
Stages used: 7 (All major stages)
```

**What they skipped:** Nothing critical
**Result:** Launched with confidence, few issues

## Quick Decision Guide

```
Are you learning? → Minimal stages
Is it just for you? → Few stages
Will others use it? → Standard stages
Is money involved? → All stages
Is data sensitive? → All stages + security
Could it harm users if broken? → All stages + extra review
```

## Common Questions

### "Can I skip testing?"

**For throwaway code:** Yes
**For anything else:** Not recommended
**Minimum:** Test that it works once
**Better:** Test happy path + one edge case

### "Do I always need review?"

**For solo personal projects:** Optional
**For team projects:** Recommended
**For production:** Required
**Alternative:** AI review is better than no review

### "Is planning really necessary?"

**For tiny scripts:** Can skip
**For everything else:** At least answer Three Questions
**Benefit:** 5 minutes planning saves 30 minutes debugging

### "What if I'm not sure?"

**Start minimal:** Use fewer stages
**Add as needed:** If you find bugs, add testing
**Observe pain points:** Add stages that would have prevented them
**Iterate:** Workflows evolve with experience

## Your Custom Workflow Builder

```markdown
## My Project: [Name]

### Risk Assessment
- Users: [Just me / Team / Public / Many]
- If it breaks: [No issue / Minor / Major problem]
- Sensitive data: [No / Yes - what kind?]
- Duration: [One time / Months / Years]
- Complexity: [Simple / Medium / Complex]
- Change frequency: [Rarely / Sometimes / Often]

### My Workflow
Based on above, I'll use these stages:

Required:
- [ ] Planning (level: ?)
- [ ] Building
- [ ] Testing (type: ?)

Optional:
- [ ] Review
- [ ] Security audit
- [ ] Performance testing
- [ ] Documentation
- [ ] Monitoring

### Why This Fits
[Explain your reasoning]

### Will Adjust If
- [What would make you add stages?]
- [What would make you remove stages?]
```

## Next Steps

**See examples:**
→ **[Workflow Examples](workflow-examples.md)** - Complete workflow walkthroughs

**Understand AI role:**
→ **[Using AI in Workflow](using-ai-in-workflow.md)** - AI assistance for each stage

**Make it evolve:**
→ **[Evolving Your Process](evolving-your-process.md)** - How workflows mature

---

**Remember:** The best workflow is the one you'll actually follow. Start simple! ⚡
