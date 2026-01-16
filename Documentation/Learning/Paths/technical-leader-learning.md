# Scenario: Technical Leader Learning to Code

You're managing a development team but want to understand code yourself. Here's YOUR path - customize it to your unique situation.

## 🐴 Dark Horse for Leaders

**Leadership + coding is YOUR unique path.** Built on [Dark Horse principles](../Philosophy/dark-horse-approach.md):

**Your micro-motives as a leader might be:**

- Understanding to make better decisions (strategy-driven)
- Building credibility with technical team (relationship-driven)
- Personal intellectual curiosity (learning-driven)
- Wanting to contribute technically (hands-on driven)
- Need to evaluate technical claims (judgment-driven)

**Your micro-motives matter.** They determine:

- How deep you go (Overview? Hands-on? Deep technical?)
- What you prioritize (Reading code? Writing? Architecture?)
- Your learning style (Conceptual first? Hands-on first?)
- Your success metrics (Team trust? Decision quality? Personal satisfaction?)

**Permission: Your path will look different from a new developer's path - that's the point.**

[Do micro-motives exercise](../Exercises/discover-your-micro-motives.md) adapted for your leadership context.

---

## Your Situation

**Who You Are:**

- Technical leader, engineering manager, product manager, or founder
- Managing developers or technical projects
- Want to understand code, not become a full-time developer
- Limited time but high motivation
- Need practical knowledge for decision-making

**Your Goals:**

- Understand what your team is building
- Read and review code meaningfully
- Make informed technical decisions
- Communicate better with developers
- Spot potential issues early
- Build credibility with technical team

**Your Constraints:**

- Limited time (maybe 5-10 hours/week)
- Can't dedicate months to learning
- Need practical knowledge fast
- Must balance with management duties

## Your Learning Path

### Phase 1: Foundations (Weeks 1-2)

**Goal:** Understand basic concepts and terminology.

**Time:** 2-3 hours/week

#### Week 1: GitHub and Version Control

**Why This First:**
You'll interact with code repositories daily as a leader. Understanding Git/GitHub is essential for:

- Reviewing pull requests
- Understanding team workflow
- Managing releases
- Tracking project progress

**Focus On:**

1. **[Understanding Repositories](../Guides/github-basics/understanding-repositories.md)**
   - What repos are and why they matter
   - How code is organized

2. **[Branches and Commits](../Guides/github-basics/branches-and-commits.md)**
   - How developers work in parallel
   - Understanding commit history

3. **[Pull Requests Explained](../Guides/github-basics/pull-requests-explained.md)**
   - The code review process
   - How to give meaningful feedback

**Practical Exercise:**

- Create a personal GitHub account
- Create a test repository
- Make some commits
- Open a pull request to yourself

**Success Indicator:**
You can navigate your team's repositories and understand what you're looking at.

#### Week 2: Code Reading Basics

**Why:** Reading code is more important than writing it for your role.

**Focus On:**

1. **Pick your team's primary language:**
   - If they use Python: Learn basic Python syntax
   - If they use JavaScript: Learn basic JS syntax
   - If they use both: Start with the one used more

2. **Understand basic structures:**
   - Variables and data types
   - Functions/methods
   - If/else logic
   - Loops
   - Objects/classes (basic level)

**Use AI to Learn:**
Ask ChatGPT or Claude:

```
I'm a technical leader learning to read Python code.
Explain these concepts with simple examples:
1. What is a function?
2. What is a class?
3. What are common data structures (lists, dicts)?
Keep it practical - I need to read code, not write complex programs.
```

**Practical Exercise:**

- Take a simple file from your team's codebase
- Use AI to explain what it does, line by line
- Ask questions about unfamiliar patterns

**Success Indicator:**
You can read a simple file and understand its purpose.

### Phase 2: Practical Understanding (Weeks 3-4)

**Goal:** Build something small to understand the development process.

**Time:** 3-4 hours/week

#### Week 3: Build Your First Project

**Why:** Hands-on experience builds real understanding.

**Project:** Build a simple API or application

**Why This Project:**

- Simple enough to complete in hours
- Covers fundamental concepts
- Uses modern frameworks
- Result you can demo
- Foundation for understanding your team's APIs

**Process:**

1. See [tex-assist-coding examples](https://github.com/doronpers/tex-assist-coding/tree/main/examples) for project ideas and build guides
2. Use AI assistance liberally
3. Focus on understanding, not memorizing
4. Take notes on concepts that click

**Success Indicator:**
You built a working API and can explain what each part does.

#### Week 4: Code Review Practice

**Why:** This is your primary technical leadership activity.

**Focus On:**

1. **[Building Trust with AI](../Guides/ai-tools/building-trust.md)**
   - When to trust AI suggestions
   - Red flags to watch for
   - Security concerns

2. **Practice Reviews:**
   - Review your own Hello API with AI
   - Review sample code with Claude
   - Learn what to look for in reviews

**Practical Exercise:**

```
Ask Claude:
"Review this code for potential issues, security concerns,
and maintainability. Explain each issue in terms a
non-developer can understand.

[Paste code from your team's recent PR]"
```

**Success Indicator:**
You can spot obvious issues in code and ask meaningful questions in PR reviews.

### Phase 3: Leadership Application (Weeks 5-8)

**Goal:** Apply knowledge to your actual work.

**Time:** 4-5 hours/week

#### Week 5-6: Active Code Review

**Start Participating:**

- Review 2-3 PRs per week from your team
- Ask questions (helps you learn AND helps your team)
- Focus on:
  - Does it meet requirements?
  - Is it understandable?
  - Are there obvious issues?
  - Edge cases handled?

**Use AI as Your Assistant:**
Before commenting on a PR:

```
Ask AI:
"I'm reviewing this code change. Help me understand:
1. What does this change do?
2. Are there any obvious issues?
3. What questions should I ask the developer?

[Paste the code]"
```

**Framework for PR Comments:**

**Instead of:**
"This looks good 👍" (not helpful)

**Try:**
"I see you're adding email validation. Questions:

- What happens if email is null?
- Does this handle international email formats?
- How do we test this?"

#### Week 7-8: Technical Discussions

**Apply Knowledge to Decisions:**

- Architecture discussions
- Technology choices
- Sprint planning
- Technical debt discussions

**Use Your New Vocabulary:**

- Understand APIs, databases, tests
- Ask informed questions
- Spot gaps in planning
- Identify risks earlier

**Example Scenarios:**

**Scenario 1: New Feature Discussion**

```
Before: "Can we add user authentication?"
After: "Can we add user authentication? Should we use JWT
tokens or session-based? What's the security model?
How will we handle password resets?"
```

**Scenario 2: Bug Discussion**

```
Before: "The app is slow."
After: "The app is slow. Is it the API response time or
frontend rendering? Can we add logging to identify the
bottleneck? Should we look at database query performance?"
```

### Phase 4: Ongoing Learning (Month 3+)

**Goal:** Continue growing technical knowledge while managing.

**Time:** 2-3 hours/week

**Sustainable Practices:**

1. **Weekly Code Reading** (30 min)
   - Read one interesting file from your codebase
   - Ask team to explain interesting patterns

2. **Active PR Review** (1 hour)
   - Review 2-3 PRs with AI assistance
   - Ask meaningful questions
   - Learn from team's responses

3. **Build Small Things** (1 hour)
   - Weekend projects
   - Try new tools/frameworks
   - Experiment with AI coding

4. **Technical Reading** (30 min)
   - Engineering blogs
   - Technology news
   - Architecture patterns

## Key Principles for Your Role

### 1. You Don't Need to Be the Best Coder

**Your value:**

- Asking good questions
- Spotting risks
- Understanding trade-offs
- Making informed decisions
- Communicating with stakeholders

**Not your value:**

- Writing production code
- Being faster than your team
- Knowing every syntax detail

### 2. Leverage AI Heavily

**AI is Perfect for You:**

- Explains code you're reviewing
- Helps you understand concepts
- Assists with simple scripts
- Acts as your patient tutor

**Example Daily AI Use:**

```
Morning: "Explain what this PR changes and potential risks"
Sprint Planning: "What are the technical challenges in this feature?"
Architecture Review: "Compare these two approaches for [system]"
```

### 3. Ask Questions Openly

**Your questions help everyone:**

- Forces team to explain clearly
- Identifies documentation gaps
- Uncovers assumptions
- Improves team communication

**Examples:**

- "Can you explain this in simpler terms?"
- "What happens if [edge case]?"
- "Why did we choose this approach over [alternative]?"
- "How do we test this?"

### 3. Focus on the "Why," Not the "How"

**Your focus:**

- Why this solution?
- Why this technology?
- Why now vs later?
- Why this complexity?

**Not your focus:**

- Exact syntax
- Implementation details (unless critical)
- Low-level optimization

**🐴 Dark Horse Addition:**

**Your role = Leadership + Technical Understanding = Unique value**

Don't try to be "as technical as your developers" - that's standardization thinking.

**Your unique value:**

- Leadership perspective + technical literacy
- Business context + engineering constraints
- Strategic thinking + implementation awareness
- People skills + technical judgment

**Focus on YOUR optimal combination, not matching someone else's profile.**

## Conversations You Can Now Have

### With Your Team

**Before:**
"How's the API development going?"

**After:**
"How's the API development going? Are we handling rate limiting?
What's our error response structure? How are we versioning the API?"

### With Stakeholders

**Before:**
"The team says it's technically complex."

**After:**
"This requires refactoring our authentication system, which touches
multiple services. The team estimates 2 weeks to do it safely with
proper testing. Rushing it risks security issues."

### With Leadership

**Before:**
"We need more time."

**After:**
"We need more time because we discovered the current database schema
doesn't support the new feature. We can either:

1) Extend timeline by 2 weeks for proper migration
2) Add technical debt with a workaround (risks issues later)
3) Reduce scope to what current schema supports
My recommendation: option 1."

## Measuring Your Progress

### Month 1

- [ ] Can navigate GitHub repositories
- [ ] Understand basic code structure
- [ ] Know key terminology
- [ ] Built one simple project

### Month 2

- [ ] Actively reviewing PRs
- [ ] Asking meaningful technical questions
- [ ] Understanding architecture discussions
- [ ] Can explain basic technical concepts

### Month 3

- [ ] Confident in code reviews
- [ ] Making informed technical decisions
- [ ] Spotting potential issues early
- [ ] Teaching others what you've learned

## Common Challenges

### Challenge 1: Imposter Syndrome

**Feeling:** "I'll never be as good as my developers"

**Reality:** You don't need to be! You need to:

- Understand enough to lead effectively
- Ask good questions
- Make informed decisions
- Build credibility through consistent learning

**Action:** Remember your unique value as a leader + technical knowledge.

### Challenge 2: Time Constraints

**Feeling:** "I don't have time to learn this"

**Reality:** Start small:

- 30 minutes daily is enough
- Code reviews count as learning
- Every conversation with developers is education

**Action:** Block 30-60 minutes daily. Make it routine.

### Challenge 3: Moving Too Fast

**Feeling:** "I need to master this quickly"

**Reality:** Sustainable pace wins:

- Better to learn 10% per week consistently
- Than 100% in week 1 and burn out

**Action:** Follow the timeline. Don't rush.

### Challenge 4: Not Feeling "Technical Enough"

**Feeling:** "My team knows so much more"

**Reality:** They should! That's their job.

- Your value: Leadership + technical understanding
- Their value: Deep technical expertise

**Action:** Complement each other's strengths.

## Tools for Your Role

### AI Tools

**Primary: ChatGPT or Claude**

- Explain code during reviews
- Answer technical questions
- Help with architecture discussions

**Secondary: GitHub Copilot**

- If you're writing any code/scripts
- Helps with personal projects

### Reading Tools

**GitHub Web Interface**

- Learn to navigate your team's repos
- Read code online
- Review PRs directly

**VS Code** (optional)

- If you want to read code locally
- Helpful for larger codebases

### Learning Resources

**This Repository**

- Structured learning path
- Practical examples
- Templates and guides

**Your Team**

- Best resource for your specific tech stack
- Schedule regular "teach me" sessions
- Pair on reviews

## Success Story Template

**Share Your Journey:**

After 3 months:

```
I started knowing nothing about code. Now I:
- Review PRs meaningfully
- Make informed technical decisions
- Communicate better with my team
- Spot potential issues early
- Feel confident in technical discussions

My team notices the difference. Conversations are more productive.
Decisions are better informed. I'm a more effective technical leader.

Time investment: ~5 hours/week consistently
Best tool: ChatGPT for explaining concepts
Best practice: Daily code reading

Worth it? Absolutely.
```

## Your Next Steps

**This Week:**

1. Read [Understanding Repositories](../Guides/github-basics/understanding-repositories.md)
2. Create a GitHub account if you don't have one
3. Browse your team's main repository
4. Ask AI to explain one file

**This Month:**

1. Complete GitHub basics section
2. Learn basic syntax of your team's language
3. Build the Hello API project
4. Start reviewing PRs with AI assistance

**This Quarter:**

1. Consistently review 2-3 PRs weekly
2. Make informed technical decisions
3. Build 2-3 small projects
4. Teach someone else what you learned

## Remember

You're not trying to replace your developers. You're becoming a more effective technical leader.

Every hour you invest in understanding code:

- Improves team communication
- Increases your influence
- Accelerates decision-making
- Reduces project risks
- Builds team confidence in your leadership

You've got this! 🚀

---

**Questions? Stuck? Want to share progress?**
Open an issue or discussion in this repository. We're here to help!
