# Discovery Exercises: Finding Your AI Tools

Hands-on exercises to discover which AI tools work best for you. No right answers - just exploration!

## The Goal

By the end of these exercises, you'll:

- Have tried multiple AI tools
- Understand your preferences
- Know when to use which tool
- Feel confident experimenting

## Exercise 1: The Same Question, Three Ways

**Time:** 15-20 minutes

**Task:** Ask the same coding question to three different AI tools.

### The Question

Pick one of these (or create your own):

**Option A:**

```
Explain how to read a CSV file in Python and convert it to a list of dictionaries.
Include example code and explain each step.
```

**Option B:**

```
I'm getting this error: "ModuleNotFoundError: No module named 'requests'"
How do I fix it?
```

**Option C:**

```
What's the difference between a list and a tuple in Python?
When should I use each one?
```

### Try These Tools

1. **ChatGPT** (free version)
   - Go to chat.openai.com
   - Ask your question
   - Note the response

2. **Claude** (free version)
   - Go to claude.ai
   - Ask the same question
   - Note the response

3. **GitHub Copilot** (if you have it)
   - Open VS Code
   - Create a Python file
   - Write the question as a comment
   - See what Copilot suggests

### Reflection

After trying all three, answer:

- Which response did you understand best?
- Which was most helpful?
- Which format did you prefer?
- Any surprising differences?

**There's no "right" answer!** Your preference matters most.

## Exercise 2: Code Generation Comparison

**Time:** 20-30 minutes

**Task:** Generate the same piece of code with different tools.

### The Code

Create a Python function that:

- Accepts a list of numbers
- Returns only the even numbers
- Returns them sorted in descending order

### Method 1: Chat-Based (ChatGPT or Claude)

**Prompt:**

```
Create a Python function that:
- Accepts a list of numbers
- Returns only the even numbers
- Returns them sorted in descending order

Include type hints and a docstring.
```

Copy the code to a file.

### Method 2: Inline (GitHub Copilot)

**In VS Code:**

```python
def filter_and_sort_evens(numbers):
    """
    Filter even numbers and sort them in descending order.

    Args:
        numbers: List of integers

    Returns:
        List of even integers sorted descending
    """
    # Let Copilot complete this
```

### Method 3: Iteration with Chat

**Start simple:**

```
Create a function to filter even numbers from a list
```

**Then refine:**

```
Now modify it to also sort them descending
```

**Then polish:**

```
Add type hints and a docstring
```

### Test All Versions

```python
# Test each version
test_data = [5, 2, 8, 1, 9, 4, 7, 6, 3]
result = filter_and_sort_evens(test_data)
print(result)  # Should be [8, 6, 4, 2]
```

### Reflection

- Which method was fastest?
- Which gave the best code?
- Which felt most natural to you?
- Which would you use for real work?

## Exercise 3: Debugging Practice

**Time:** 15-20 minutes

**Task:** Use AI to debug broken code.

### The Broken Code

```python
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

# Test it
scores = [85, 90, 78, 92, 88]
print(calculate_average(scores))  # Works!

empty_scores = []
print(calculate_average(empty_scores))  # Crashes!
```

### Try Different Approaches

**Approach 1: Direct Question to Chat AI**

```
This code crashes when given an empty list:
[paste code]
How do I fix it?
```

**Approach 2: Copilot Comment**

```python
# TODO: Fix this function to handle empty lists
def calculate_average(numbers):
    # Let Copilot suggest fixes
```

**Approach 3: Ask for Explanation First**

```
This code crashes with "ZeroDivisionError: division by zero"
Explain why this happens and suggest a fix:
[paste code]
```

### Reflection

- Which approach helped you learn more?
- Did you understand the fixes?
- Which would you use when stuck?

## Exercise 4: Learning a Concept

**Time:** 20-30 minutes

**Task:** Learn something new using AI.

### Pick a Topic

Choose something you don't know well:

- List comprehensions in Python
- Async/await in JavaScript
- SQL JOINs
- React hooks
- Git rebase
- [Your choice]

### Try Different Learning Styles

**Style 1: Ask for Simple Explanation**

```
Explain [topic] like I'm a beginner.
Use a real-world analogy.
```

**Style 2: Request Progression**

```
Teach me [topic] in this order:
1. Simple example
2. Why it's useful
3. Common mistakes
4. Practice exercise
```

**Style 3: Interactive Learning**

```
I want to learn [topic].
Can you give me a challenge to solve,
then explain the solution?
```

### Reflection

- Which style helped you learn best?
- Did you actually understand the concept?
- Could you explain it to someone else?
- Which AI was the best teacher for you?

## Exercise 5: Code Review

**Time:** 15-20 minutes

**Task:** Get AI to review code.

### The Code to Review

```python
def process_users(users):
    result = []
    for user in users:
        if user["age"] >= 18:
            result.append(user["name"])
    return result
```

### Different Review Approaches

**Approach 1: General Review**

```
Review this Python code for potential issues:
[paste code]
```

**Approach 2: Specific Focus**

```
Review this code specifically for:
1. Potential bugs
2. Readability issues
3. Pythonic improvements

[paste code]
```

**Approach 3: Security Review**

```
Review this code for security issues
and edge cases that could cause crashes:
[paste code]
```

### Compare Results

- Which review was most helpful?
- Did different AIs catch different issues?
- Which feedback did you actually apply?

### Reflection

- Would you use AI for code reviews?
- Which AI gave the best feedback?
- What kind of reviews are most useful to you?

## Exercise 6: Build Something Small

**Time:** 30-45 minutes

**Task:** Build a tiny project using your preferred AI tool.

### The Project Options

**Option A: Todo List (Command Line)**

- Add tasks
- List tasks
- Mark complete
- Save to file

**Option B: Number Guessing Game**

- Computer picks random number 1-100
- User guesses
- Give "higher" or "lower" hints
- Count number of guesses

**Option C: Simple Calculator**

- Add, subtract, multiply, divide
- Handle errors gracefully
- Keep running until user quits

### Build It Your Way

Use whatever combination of AI tools feels right:

- Plan with ChatGPT/Claude
- Implement with Copilot
- Debug with Chat AI
- Review with Claude

### Track Your Process

Note:

- Which tools you used for what
- What worked well
- What was frustrating
- How long each part took

### Reflection

- Did you enjoy the process?
- Would you change your approach?
- What tool was most helpful?
- What would you do differently next time?

## Exercise 7: Prompt Iteration

**Time:** 20-30 minutes

**Task:** Practice improving prompts.

### Start Vague, Get Specific

**Iteration 1:**

```
Create a login function
```

Note the response.

**Iteration 2:**

```
Create a Python login function that accepts username and password
```

Note how it improved.

**Iteration 3:**

```
Create a Python login function that:
- Accepts username and password
- Checks against a database
- Returns a JWT token if valid
- Returns an error message if invalid
```

Note the improvement.

**Iteration 4:**

```
Create a Python FastAPI login endpoint that:
- Accepts username and password via POST
- Validates against PostgreSQL database
- Returns JWT token (1 hour expiry) if valid
- Returns 401 status with error message if invalid
- Includes error handling for database failures
- Uses password hashing (bcrypt)
- Includes rate limiting (5 attempts per minute)

Include type hints, docstrings, and example usage.
```

### Reflection

- How did responses improve?
- At what point was it "good enough"?
- How specific should you be?
- When is too much detail overwhelming?

## Exercise 8: Find Your Workflow

**Time:** 30 minutes

**Task:** Design your personal AI workflow.

### Reflect on Previous Exercises

Based on what you learned, answer:

**1. Which tool do you prefer for:**

- Quick questions?
- Learning new concepts?
- Writing code?
- Debugging?
- Code review?

**2. What's your ideal workflow?**

```
Example:
1. Learn concepts: ChatGPT
2. Plan code: Claude
3. Implement: Copilot
4. Review: Claude
5. Debug: ChatGPT
```

**3. What did you enjoy most?**

- Chat-based help?
- Inline suggestions?
- Mix of both?

**4. What frustrated you?**

- Copy-pasting code?
- Waiting for responses?
- Context switching?

### Create Your Workflow Document

Write down your personalized approach:

```markdown
# My AI Coding Workflow

## Daily Coding
- Tool: [your choice]
- Why: [reason]

## Learning New Things
- Tool: [your choice]
- Why: [reason]

## Debugging
- Tool: [your choice]
- Why: [reason]

## Code Review
- Tool: [your choice]
- Why: [reason]

## When I Get Stuck
- First try: [tool/approach]
- If that doesn't work: [alternative]
```

## Exercise 9: Evaluate AI Mistakes

**Time:** 15-20 minutes

**Task:** Practice spotting AI errors.

### The Test

Ask an AI:

```
Show me a Python function to check if a string is a valid URL
```

### Review the Response

Check for:

- [ ] Does it actually validate URLs?
- [ ] Does it handle edge cases?
- [ ] Is the regex correct?
- [ ] What about localhost URLs?
- [ ] What about IP addresses?
- [ ] What about international domains?

### Ask Follow-Up

```
What edge cases does this function miss?
```

See if AI catches its own limitations!

### Reflection

- How good are you at spotting issues?
- What should you always verify?
- When do you need to research further?

## Exercise 10: Share Your Findings

**Time:** 15-30 minutes

**Task:** Teach someone else what you learned.

### Write It Down

Create a document:

```markdown
# What I Learned About AI Coding Tools

## Tools I Tried
- [List them]

## My Favorite Tool
- [Which one and why]

## Biggest Surprise
- [What surprised you]

## Best Use Case
- [When AI was most helpful]

## Worst Use Case
- [When AI wasn't helpful]

## My Recommendation
- [Advice for others starting out]
```

### Share It

- Post in this repo's discussions
- Share with friends learning to code
- Tweet it
- Blog about it

Teaching others solidifies your learning!

## Your Next Steps

After completing these exercises:

**You're ready for:**

- **[Workflow Building](../../03-workflow-building/README.md)** - Design your process
- **Examples**: See [tex-assist-coding examples](https://github.com/doronpers/tex-assist-coding/tree/main/examples) for project ideas
- **[Patterns](../../04-patterns/README.md)** - Learn common solutions

**Keep practicing:**

- Use AI daily
- Track what works
- Adjust your workflow
- Stay curious!

## Feeling Stuck?

**If exercises feel overwhelming:**

- Do just 2-3 exercises
- Take breaks between them
- No need to finish all at once
- Come back when curious

**If you can't decide on tools:**

- That's okay! Keep exploring
- Your preferences will emerge
- No wrong choices
- Use what feels natural

**If nothing seems to work:**

- Take a break from AI
- Code without it for a bit
- Come back fresh
- Remember: AI is optional

---

**Remember:** The best tool is the one you'll actually use! Explore and have fun! 🔍
