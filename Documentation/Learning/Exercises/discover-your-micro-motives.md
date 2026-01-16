# Exercise: Discover Your Coding Micro-motives

**Time:** 30-45 minutes
**Goal:** Understand what SPECIFICALLY energizes you about coding
**Why:** So you can make choices aligned with your authentic motivations

## What Are Micro-motives?

Micro-motives are the specific aspects of an activity that personally energize you. They're more precise than "I like coding."

**Example:**

- ❌ Too vague: "I like coding"
- ✅ Specific micro-motive: "I love the moment when code I write immediately changes what I see on screen"

Two people can both "like coding" but for completely different reasons. Your micro-motives guide YOUR optimal path.

## Part 1: Reflection Questions

Answer these honestly. There are no wrong answers.

### Energy Inventory

**Think of your best coding experiences. When you were most energized, what was happening?**

*Write 2-3 specific moments:*

1.

2.

3.

**What made those moments energizing? Be specific:**

### Contrast Analysis

**Think of coding experiences that drained you. What was happening?**

*Write 2-3 moments:*

1.

2.

3.

**What specifically drained your energy?**

### Pattern Recognition

Look at your energizing moments above. What do they have in common?

**Common elements might be:**

- [ ] Seeing immediate visual results
- [ ] Solving a logical puzzle
- [ ] Learning how something works
- [ ] Creating something useful
- [ ] Helping another person
- [ ] Working independently
- [ ] Collaborating with others
- [ ] Teaching/explaining
- [ ] Optimizing and improving
- [ ] Building from scratch
- [ ] Debugging and fixing
- [ ] Experimenting freely
- [ ] Following a clear path
- [ ] Other: _______________

**Circle or check 3-5 that resonate most.**

## Part 2: Practical Experiments

You can't always know your micro-motives through reflection alone. Try these mini-projects and notice your energy.

### Experiment A: Visual/Interactive (60 minutes)

**Project:** Build a simple interactive web page with a button that changes something visual.

**Try:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Color Changer</title>
</head>
<body>
    <h1 id="heading">Click the button!</h1>
    <button onclick="changeColor()">Change Color</button>

    <script>
        function changeColor() {
            const colors = ['red', 'blue', 'green', 'purple', 'orange'];
            const randomColor = colors[Math.floor(Math.random() * colors.length)];
            document.getElementById('heading').style.color = randomColor;
        }
    </script>
</body>
</html>
```

**After completing, rate:**

- Energy during: ___/10
- Satisfaction after: ___/10
- Want to expand it: ___/10

**What specifically felt good or bad about this?**

### Experiment B: Logic Puzzle (60 minutes)

**Project:** Write a function to find the largest number in a list and explain how it works.

**Try:**

```python
def find_largest(numbers):
    """Find and return the largest number in a list."""
    if not numbers:
        return None

    largest = numbers[0]
    for num in numbers:
        if num > largest:
            largest = num
    return largest

# Test it
test_list = [3, 7, 2, 9, 1, 5]
result = find_largest(test_list)
print(f"Largest number: {result}")

# Now try edge cases
print(find_largest([]))  # Empty list
print(find_largest([-5, -2, -10]))  # All negative
```

**After completing, rate:**

- Energy during: ___/10
- Satisfaction after: ___/10
- Want to expand it: ___/10

**What specifically felt good or bad about this?**

### Experiment C: Practical Tool (60 minutes)

**Project:** Automate something annoying from your daily life.

**Examples:**

- Rename multiple files following a pattern
- Calculate something you do regularly
- Generate text you need repeatedly
- Parse data from a format you use

**Pick something YOU actually need.**

**After completing, rate:**

- Energy during: ___/10
- Satisfaction after: ___/10
- Want to expand it: ___/10

**What specifically felt good or bad about this?**

## Part 3: Synthesis

### Compare Your Experiments

**Which had highest energy ratings?**

**Which did you WANT to keep working on?**

**Which did you finish because you "should" vs. because you wanted to?**

### Your Micro-motive Statements

Based on everything above, complete these sentences:

**I am energized when:**

1.

2.

3.

**I am drained when:**

1.

2.

3.

**The aspects of coding I find most fulfilling are:**

1.

2.

3.

## Part 4: Application

### Choosing Projects

**Given your micro-motives, which project types align?**

**If you're energized by immediate visual feedback:**

- Frontend development
- Data visualization
- Game development
- Interactive tools

**If you're energized by logic puzzles:**

- Algorithms and data structures
- Backend optimization
- Security challenges
- System design

**If you're energized by helping people:**

- Projects solving real problems
- Open source contributions
- Teaching and documentation
- Accessibility work

**If you're energized by understanding systems:**

- Reading codebases
- Infrastructure work
- Database design
- API architecture

**Write 3 project ideas that align with YOUR micro-motives:**

1.

2.

3.

### Choosing Learning Resources

**Given your micro-motives, what learning style fits?**

**If you love building:**

- Project-based tutorials
- Build challenges
- Clone existing apps
- Create portfolio pieces

**If you love understanding:**

- Conceptual courses
- System design content
- "How it works" deep dives
- Architecture discussions

**If you love experimenting:**

- Open-ended exercises
- Playground environments
- "What if?" explorations
- Breaking things safely

**What learning resources match YOUR style?**

### Choosing Technologies

**Given your micro-motives, what technologies might energize you?**

**Don't pick based on "what's popular" - pick based on alignment:**

**If immediate feedback energizes you:**

- JavaScript (instant browser results)
- Python with Jupyter notebooks
- Frontend frameworks like React
- Game engines

**If solving puzzles energizes you:**

- Languages with strong typing (TypeScript, Rust)
- Functional programming
- Algorithm-focused work
- Backend languages

**If helping people energizes you:**

- Web technologies (reach many people)
- Automation tools (save people time)
- Documentation tools
- Accessibility tech

**What technologies want to explore?**

## Part 5: Your Micro-motive Map

Fill this out as your personal reference:

### My Primary Micro-motives

**Top 3 things that energize me in coding:**

1.
2.
3.

### My Drainers

**Top 3 things that drain me in coding:**

1.
2.
3.

### My Optimal Alignment

**Project types that match my micro-motives:**
-

-
-

**Learning styles that match my micro-motives:**
-

-
-

**Technologies I want to explore:**
-

-
-

**Work environments that energize me:**
-

-
-

### My Commitment

**Based on my micro-motives, I commit to:**

- [ ] Choosing projects that align with what energizes me
- [ ] Saying no to paths that drain me (even if they're "should"s)
- [ ] Learning in ways that fit MY style
- [ ] Trusting that my unique combination is valuable
- [ ] Adjusting when I notice misalignment
- [ ] Honoring my micro-motives as my compass

## Ongoing Discovery

**Your micro-motives aren't fixed.** They evolve as you grow.

**Every month, check in:**

- What's energizing me NOW?
- What's draining me NOW?
- Do my projects still align?
- Do I need to adjust my path?

**Use the [Learning Journal](../templates/learning-journal.md) to track patterns over time.**

## What If You're Still Unsure?

**That's perfect!** Uncertainty means you're at the discovery stage.

**Keep experimenting:**

- Try diverse projects
- Pay attention to your energy
- Notice what you want to keep doing
- Notice what feels like a chore
- Patterns will emerge

**The goal isn't to find your "one true calling" - it's to develop awareness of what energizes you SO you can make aligned choices.**

## Next Steps

**Now that you know your micro-motives:**

1. **Choose projects**: Pick from [examples](../examples/) that align with your micro-motives
2. **Design workflow**: Use [Workflow Builder](../Guides/workflow-building/workflow-builder.md) with your micro-motives in mind
3. **Select learning path**: Use paths in [README](../README.md) as menu, choosing what aligns
4. **Read Dark Horse approach**: See [Dark Horse Approach](../Philosophy/dark-horse-approach.md) for full framework

**Remember:** Your micro-motives are your compass. Trust them over external "shoulds."

---

**Done with this exercise?**

Save your micro-motive map somewhere you can reference it when making decisions about:

- What to learn next
- Which projects to build
- Which jobs to pursue
- How to structure your workflow
- When to say no

**Your unique combination of micro-motives is your competitive advantage.** 🎯
