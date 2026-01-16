# Decision Framework

Quick decision trees to help you choose the right approach for any coding task.

## How to Use This Framework

When starting a new task, use these decision trees to quickly determine:

- Which workflow to use
- Which stages to include
- Which tools to use
- How thorough to be

**Time investment:** 2-5 minutes of thinking saves hours of work.

---

## Decision Tree 1: Which Workflow?

```
START: What are you building?

├─ Learning exercise or experiment?
│  └─ YES → Use MINIMAL WORKFLOW
│     • Three Questions
│     • Code
│     • Test it works
│     • Done
│
└─ NO → Is anyone else using it?
   │
   ├─ Just me
   │  └─ How long will you use it?
   │     ├─ One time → MINIMAL WORKFLOW
   │     ├─ Few weeks → LIGHT WORKFLOW (add git + docs)
   │     └─ Months+ → BALANCED WORKFLOW (add tests + review)
   │
   ├─ Small team/friends (< 50 users)
   │  └─ BALANCED WORKFLOW
   │     • Plan
   │     • Build with tests
   │     • Self-review or AI review
   │     • Deploy
   │
   └─ Many users (50+) or paying customers
      └─ COMPREHENSIVE WORKFLOW
         • Design
         • Plan thoroughly
         • Build with TDD
         • Multiple reviews
         • Security audit
         • Monitored deployment
```

---

## Decision Tree 2: Testing Strategy

```
START: How critical is this code?

├─ Learning or throwaway?
│  └─ Manual testing only
│     • Run it
│     • See if it works
│     • Done
│
├─ Personal project?
│  └─ What will break if there are bugs?
│     ├─ Nothing important → Manual testing
│     ├─ Will be annoying → Basic automated tests
│     └─ Will lose data → Comprehensive tests
│
├─ Shared project?
│  └─ Automated tests required
│     • Test happy paths
│     • Test one edge case per feature
│     • Test error handling
│
└─ Production system?
   └─ Comprehensive testing required
      • Unit tests (individual functions)
      • Integration tests (components together)
      • End-to-end tests (full flows)
      • Edge cases
      • Error scenarios
      • Performance tests
```

**Quick rule:** More users = more tests

---

## Decision Tree 3: Review Strategy

```
START: Who will maintain this code?

├─ Just me, one-time script
│  └─ No review needed
│     • Ship it
│
├─ Just me, ongoing project
│  └─ Self-review checklist
│     • Does it work?
│     • Is it readable?
│     • Will I understand it in 6 months?
│
├─ Small team
│  └─ Choose based on time:
│     ├─ Urgent → AI review only
│     ├─ Normal → AI + self-review
│     └─ Important → AI + peer review
│
└─ Production or client work
   └─ Multiple reviews required
      • Self-review checklist
      • AI code review (Claude)
      • Peer review
      • Security review (if handling data)
```

**Quick rule:** More users = more reviews

---

## Decision Tree 4: AI Tool Selection

```
START: What do you need help with?

├─ Real-time coding assistance?
│  └─ Use GitHub Copilot
│     • Autocomplete as you type
│     • Understands your codebase
│     • Fast and in-editor
│
├─ Explaining concepts or planning?
│  └─ Use ChatGPT or Claude
│     ├─ Quick questions → ChatGPT
│     ├─ Deep reasoning → Claude
│     └─ Both are good for learning
│
├─ Code review or security?
│  └─ Use Claude
│     • Thorough analysis
│     • Security-focused
│     • Explains reasoning well
│
├─ Generating tests?
│  └─ Use ChatGPT or Claude
│     • Either works great
│     • Give complete code context
│
└─ Complex multi-file refactoring?
   └─ Use Cursor or Windsurf
      • Built for codebase-wide changes
      • Better context management
```

**Can afford multiple tools?**

Ideal combination:

- Copilot: Daily coding
- ChatGPT: Questions and tests
- Claude: Reviews and security

---

## Decision Tree 5: Security Considerations

```
START: What data does this handle?

├─ No user data
│  └─ Basic security sufficient
│     • Validate inputs
│     • Handle errors
│     • Use HTTPS
│
├─ Public data (emails, names)
│  └─ Standard security
│     • Input validation
│     • SQL injection prevention
│     • HTTPS required
│     • Basic rate limiting
│     • AI security review
│
├─ Private data (passwords, phone numbers)
│  └─ Enhanced security required
│     • All of above, plus:
│     • Password hashing
│     • Encryption at rest
│     • Comprehensive security review
│     • External security audit
│     • Monitoring and alerts
│
└─ Sensitive data (financial, health)
   └─ Maximum security required
      • All of above, plus:
      • Compliance review (HIPAA, PCI, etc.)
      • Penetration testing
      • Regular security audits
      • Dedicated security team review
      • Legal review
```

**Quick rule:** More sensitive data = more security stages

---

## Decision Tree 6: Documentation Needs

```
START: Will anyone else use this code?

├─ No, throwaway code
│  └─ No documentation needed
│
├─ Just me, keeping it
│  └─ Minimal documentation
│     • Add README with "What this does"
│     • Comment tricky parts
│     • That's enough
│
├─ Team project
│  └─ Standard documentation
│     • README with setup instructions
│     • Docstrings on functions
│     • Architecture overview
│     • How to run tests
│
├─ Open source or API
│  └─ Comprehensive documentation
│     • All of above, plus:
│     • Usage examples
│     • API reference
│     • Contributing guide
│     • Troubleshooting section
│
└─ Client deliverable
   └─ Professional documentation
      • All of above, plus:
      • Deployment guide
      • Maintenance guide
      • Troubleshooting
      • Technical architecture
```

**Quick rule:** More users = more documentation

---

## Decision Tree 7: Deployment Strategy

```
START: Where will this run?

├─ Just on my computer
│  └─ No deployment needed
│     • python main.py
│     • Done
│
├─ Shared with a few people
│  └─ Simple deployment
│     • Push to GitHub
│     • Deploy to Render/Railway (free tier)
│     • Share URL
│
├─ Growing user base (100+)
│  └─ Proper deployment
│     • Use proper hosting (AWS, GCP, Azure)
│     • Set up monitoring
│     • Have rollback plan
│     • Use environment variables
│     • HTTPS required
│
└─ Production system (1000+)
   └─ Enterprise deployment
      • All of above, plus:
      • CI/CD pipeline
      • Staging environment
      • Blue-green or canary deployment
      • Automated backups
      • Disaster recovery plan
      • Load balancing
      • Auto-scaling
```

**Quick rule:** More users = more deployment sophistication

---

## Decision Tree 8: Time vs Quality Trade-off

```
START: What's your timeline?

├─ Need it in 1 hour (emergency fix)
│  └─ SPEED MODE
│     • Skip planning
│     • Minimal testing
│     • Ship it
│     • Fix later if needed
│     • Add TODO for improvement
│
├─ Need it today (urgent feature)
│  └─ FAST MODE
│     • Quick plan (5 min)
│     • Build
│     • Basic test
│     • AI review
│     • Ship
│
├─ Need it this week (normal timeline)
│  └─ BALANCED MODE
│     • Proper planning
│     • Build with tests
│     • Self + AI review
│     • Deploy confidently
│
└─ Need it when it's ready (quality critical)
   └─ QUALITY MODE
      • Thorough design
      • Test-driven development
      • Multiple reviews
      • Security audit
      • Perfect before shipping
```

**Remember:** Fast, Good, Cheap - pick two!

---

## Quick Reference Cheat Sheet

### When to Use Minimal Workflow

- ✅ Learning
- ✅ Experiments
- ✅ Throwaway code
- ✅ One-time scripts
- ❌ Anything users depend on

### When to Use Balanced Workflow

- ✅ Side projects
- ✅ Small team work
- ✅ Personal tools you'll maintain
- ✅ Non-critical applications
- ❌ Mission-critical systems

### When to Use Comprehensive Workflow

- ✅ Production systems
- ✅ Client work
- ✅ Revenue-generating products
- ✅ Data-sensitive applications
- ❌ Learning projects (overkill)

---

## Context-Specific Quick Guides

### Scenario: Building API Endpoint

```
Question: How many users?
├─ Learning → Minimal (build + manual test with curl)
├─ Internal tool → Balanced (add tests + validation)
└─ Public API → Comprehensive (add security + docs + rate limiting)
```

### Scenario: Database Migration

```
Question: Can you afford data loss?
├─ Development → Test in dev, run in prod
├─ Staging → Test thoroughly, backup, run, verify
└─ Production → Backup, test on copy, peer review script, run with rollback ready
```

### Scenario: UI Component

```
Question: How visible to users?
├─ Internal admin → Build + test in browser
├─ User-facing → Build + test + design review
└─ Main landing page → Build + test + design review + A/B test + analytics
```

### Scenario: Bug Fix

```
Question: How critical is the bug?
├─ Typo → Fix and deploy
├─ Feature broken → Fix + test + deploy
└─ Security issue → Fix + comprehensive test + security review + urgent deploy
```

---

## Common Decision Patterns

### The "Prototype to Production" Pattern

```
Phase 1 (Week 1): Minimal workflow
• Just make it work
• No tests, no review
• Validate the idea

Phase 2 (Week 2): If idea is good
• Add tests
• Add basic review
• Clean up code

Phase 3 (Month 1): If getting users
• Add monitoring
• Add documentation
• Add security review

Phase 4 (Month 2+): If successful
• Add comprehensive testing
• Add multiple reviews
• Professional deployment
```

### The "Client Work" Pattern

```
Always use comprehensive workflow:
• Design → Plan → Build → Test → Review → Deploy → Monitor

No exceptions because:
• Reputation at stake
• Payment depends on quality
• Legal implications
• Client expects professionalism
```

### The "Startup MVP" Pattern

```
Balance speed and essential quality:

Must have:
• Basic planning
• Core functionality
• Security for sensitive data
• Monitoring

Can skip initially:
• Perfect code
• Comprehensive tests
• Full documentation
• Nice-to-have features

Add later after validation
```

---

## Meta-Decision: When to Use This Framework

### Use this framework when

✅ Starting a new project
✅ Unsure which approach to take
✅ Want to validate your instincts
✅ Team needs alignment
✅ Stakes feel unclear

### Don't need this framework when

❌ Doing something you've done 100 times
❌ Time is so urgent that deciding is slower than doing
❌ The decision is obvious
❌ You have a strong instinct and low stakes

**Trust your instincts as you gain experience!**

---

## Framework for Building Your Own Framework

Eventually, you'll develop your own decision-making process:

```markdown
## My Personal Decision Framework

### For API work, I:
[Your approach]

### For frontend work, I:
[Your approach]

### For data work, I:
[Your approach]

### When in doubt, I:
[Your fallback approach]
```

**This evolves with experience!**

---

## Emergency Override

Sometimes you need to break your own rules:

### Override rules when

**Production is down**
→ Fix first, process later

**Opportunity is time-sensitive**
→ Ship fast, improve later

**Learning is the goal**
→ Experiment freely, ignore process

**Stakes changed mid-project**
→ Adjust workflow immediately

**New information appears**
→ Re-evaluate decisions

**The framework says one thing but your gut says another**
→ Trust experience over rules

---

## Practice Scenarios

Test your decision-making:

### Scenario 1

**Task:** Build a URL shortener for your team (10 people)
**Timeline:** 2 weeks
**Your decision:** _________________
**Recommended:** Balanced workflow with tests and review

### Scenario 2

**Task:** Fix typo in documentation
**Timeline:** Now
**Your decision:** _________________
**Recommended:** Just fix it and commit

### Scenario 3

**Task:** Add user authentication to production app
**Timeline:** 1 week
**Your decision:** _________________
**Recommended:** Comprehensive workflow + security review

### Scenario 4

**Task:** Try out a new Python library
**Timeline:** 30 minutes
**Your decision:** _________________
**Recommended:** Minimal - just experiment

---

## Summary: One-Page Quick Reference

```
┌─────────────────────────────────────────────────────┐
│           DECISION FRAMEWORK SUMMARY                │
├─────────────────────────────────────────────────────┤
│                                                     │
│  LEARNING?        → Minimal workflow                │
│  JUST FOR ME?     → Light workflow + git            │
│  FOR TEAM?        → Balanced workflow + tests       │
│  PRODUCTION?      → Comprehensive workflow          │
│                                                     │
│  SENSITIVE DATA?  → Add security review             │
│  MANY USERS?      → Add monitoring                  │
│  URGENT?          → Reduce stages, ship fast        │
│  CRITICAL?        → All stages, no shortcuts        │
│                                                     │
│  ONE TOOL?        → GitHub Copilot                  │
│  REVIEWING?       → Claude                          │
│  LEARNING?        → ChatGPT                         │
│  ALL TOOLS?       → Use each for its strengths      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Next Steps

**See the stages:**
→ **[Stages of Development](stages-of-development.md)** - Understand each stage deeply

**See them in action:**
→ **[Workflow Examples](workflow-examples.md)** - Real decisions in real scenarios

**Choose your stages:**
→ **[Choosing Stages](choosing-stages.md)** - Match stages to your project

**Make it grow:**
→ **[Evolving Your Process](evolving-your-process.md)** - Improve over time

---

**Remember: The best decision is the informed one, made quickly!** 🎯
