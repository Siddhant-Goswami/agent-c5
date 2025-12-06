# Multi-Agent Systems: Learning Assignment

**Course:** Introduction to AI Agents and Multi-Agent Systems
**Duration:** 2-3 weeks
**Difficulty:** Intermediate (Python knowledge required)
**Learning Method:** Progressive, hands-on exercises building from first principles

---

## 📚 Learning Objectives

By completing this assignment, you will:

1. ✅ Understand the SPOAR (Sense-Plan-Act-Observe-Reflect) loop pattern
2. ✅ Learn how LLMs can be used as reasoning engines in agents
3. ✅ Grasp the concept of agent specialization
4. ✅ Master the manager/orchestrator pattern for multi-agent systems
5. ✅ Build practical agents that solve real-world problems
6. ✅ Understand when to use single vs. multi-agent approaches
7. ✅ Learn to design agent communication and coordination

---

## 🎯 Assignment Structure

This assignment is divided into 6 progressive parts:

| Part | Topic | Time | Difficulty |
|------|-------|------|------------|
| 1 | Understanding Single Agents | 3-4 hours | ⭐ Easy |
| 2 | Agent Specialization | 2-3 hours | ⭐⭐ Medium |
| 3 | Manager Pattern | 3-4 hours | ⭐⭐ Medium |
| 4 | Building Custom Agents | 4-5 hours | ⭐⭐⭐ Hard |
| 5 | Advanced Patterns | 5-6 hours | ⭐⭐⭐ Hard |
| 6 | Final Project | 8-10 hours | ⭐⭐⭐⭐ Very Hard |

**Total Time:** 25-32 hours

---

## Part 1: Understanding Single Agents (Foundation)

**Learning Goal:** Master the SPOAR loop and single-agent architecture.

### 📖 Reading (1 hour)

1. Read `README.md` - Understand the simple agent
2. Read the first half of `TUTORIAL.md` - Focus on SPOAR loop
3. Study `simple_agent.py` - Trace through the code

### 💻 Exercises

#### Exercise 1.1: Trace the SPOAR Loop (30 min)

Run the simple agent and answer these questions:

```bash
python simple_agent.py
```

**Questions:**
1. What happens in each phase (SENSE, PLAN, ACT, OBSERVE, REFLECT)?
2. How many iterations does the agent take to solve "What is 25 * 4 + 100?"
3. What would happen if you removed the REFLECT phase?
4. Why does the agent need multiple iterations?

**Deliverable:** A document (`part1_q1.md`) answering these questions with code references.

#### Exercise 1.2: Add a New Tool (1 hour)

Add a `get_weather` tool to `simple_agent.py`:

```python
TOOLS = {
    # ... existing tools ...
    "get_weather": {
        "description": "Get the current weather for a city",
        "function": lambda city: f"Weather in {city}: 72°F, sunny"
    }
}
```

**Task:**
- Add the tool
- Test with goal: "What's the weather in San Francisco?"
- Document how the agent discovers and uses the new tool

**Deliverable:** Modified `simple_agent.py` and test output.

#### Exercise 1.3: Understand LLM Decision Making (1 hour)

Modify the `_plan()` method to log the full LLM prompt and response:

```python
def _plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
    # ... build prompt ...

    print("\n=== LLM PROMPT ===")
    print(prompt)
    print("=== END PROMPT ===\n")

    response = self.llm.chat.completions.create(...)

    print("\n=== LLM RESPONSE ===")
    print(response.choices[0].message.content)
    print("=== END RESPONSE ===\n")

    # ... continue ...
```

**Questions:**
1. What information does the LLM receive in the prompt?
2. How does the LLM decide which tool to use?
3. What makes the LLM choose "COMPLETE" vs "USE_TOOL"?
4. What happens if the prompt is unclear?

**Deliverable:** Logged output and analysis document.

---

## Part 2: Agent Specialization

**Learning Goal:** Understand why and how to create specialized agents.

### 📖 Reading (30 min)

1. Read `ARCHITECTURE.md` - Focus on "Specialized Agents" section
2. Study one specialized agent in `multi_agent_system.py` (e.g., `InsightExtractorAgent`)

### 💻 Exercises

#### Exercise 2.1: Analyze Specialization (1 hour)

Compare `simple_agent.py` vs `InsightExtractorAgent`:

**Questions:**
1. What makes `InsightExtractorAgent` "specialized"?
2. What parts are inherited from `BaseAgent`?
3. What parts are customized?
4. Why inherit instead of copying the code?

**Deliverable:** Comparison document with code examples.

#### Exercise 2.2: Create a Sentiment Analyzer Agent (2 hours)

Create a new specialized agent that analyzes sentiment:

```python
class SentimentAnalyzerAgent(BaseAgent):
    """Agent specialized in analyzing sentiment and tone."""

    def __init__(self):
        super().__init__(
            "SentimentAnalyzer",
            "Analyze sentiment and emotional tone of text"
        )

    def _plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # TODO: Implement sentiment analysis
        # Should return: overall_sentiment, confidence, emotions, tone
        pass
```

**Requirements:**
1. Analyze text sentiment (positive, negative, neutral)
2. Detect specific emotions (joy, anger, fear, sadness, etc.)
3. Assess tone (professional, casual, urgent, etc.)
4. Return confidence scores

**Test Cases:**
```python
# Test 1: Positive
text = "This product is amazing! Best purchase ever!"

# Test 2: Negative
text = "Very disappointed. Waste of money."

# Test 3: Mixed
text = "The product is good but customer service was terrible."
```

**Deliverable:**
- `SentimentAnalyzerAgent` class
- Test results for 3 test cases
- Analysis of how specialization improves sentiment analysis vs. generic agent

---

## Part 3: Manager Pattern & Orchestration

**Learning Goal:** Understand how to coordinate multiple agents.

### 📖 Reading (1 hour)

1. Read "Manager Pattern" section in `ARCHITECTURE.md`
2. Study `ManagerAgent` class in `multi_agent_system.py`
3. Trace through `run_workflow()` method

### 💻 Exercises

#### Exercise 3.1: Understand Data Flow (1 hour)

Trace how data flows through the workflow:

**Task:** Create a diagram showing:
1. How `workflow_context` starts
2. What each agent adds to it
3. How data from one agent feeds into the next
4. What the final `workflow_results` contains

**Deliverable:** Flowchart or diagram (hand-drawn is fine, or use tools like Mermaid, draw.io)

#### Exercise 3.2: Add Your Sentiment Agent to the Workflow (2 hours)

Integrate your `SentimentAnalyzerAgent` into the manager:

```python
class ManagerAgent(BaseAgent):
    def __init__(self):
        # ... existing code ...
        self.agent_tools["sentiment_analyzer"] = SentimentAnalyzerAgent()

    def run_workflow(self, transcript: str):
        # ... existing steps ...

        # Add Step 6: Analyze Sentiment
        print("\n📍 STEP 6: Analyzing Sentiment")
        sentiment_result = self.agent_tools["sentiment_analyzer"].run(
            goal="Analyze meeting sentiment and tone",
            context=workflow_context,
            max_iterations=2
        )

        if sentiment_result["success"]:
            sentiment_data = sentiment_result["result"]
            self.workflow_results["sentiment"] = sentiment_data.get("sentiment", {})
```

**Requirements:**
1. Add sentiment analysis as Step 6
2. Use the transcript and insights as input
3. Save sentiment results to output
4. Test with sample transcript

**Deliverable:**
- Modified `multi_agent_system.py`
- Output showing sentiment analysis results
- Reflection on how sentiment adds value to the workflow

---

## Part 4: Building Custom Agents from Scratch

**Learning Goal:** Design and implement agents for specific use cases.

### 💻 Exercises

#### Exercise 4.1: Email Generator Agent (3 hours)

Create an agent that generates professional emails from meeting notes:

**Specification:**
```python
class EmailGeneratorAgent(BaseAgent):
    """Generate professional emails based on meeting outcomes."""

    def _plan(self, context):
        """
        Input: notes (from NoteTakerAgent)
        Output: {
            "subject": "...",
            "body": "...",
            "recipients": ["...", "..."],
            "tone": "formal/casual",
            "attachments": ["meeting_notes.pdf"]
        }
        """
```

**Test Cases:**

1. **Follow-up Email** - After a client meeting, send recap
2. **Action Items Email** - Send todos to team members
3. **Executive Summary** - Brief email for leadership

**Requirements:**
- Professional tone
- Clear subject lines
- Well-structured body
- Appropriate recipients based on context
- Signature and formatting

**Deliverable:**
- `EmailGeneratorAgent` implementation
- 3 test outputs (one for each test case)
- Comparison with manually written emails

#### Exercise 4.2: Risk Assessment Agent (3 hours)

Create an agent that identifies project risks from meeting discussions:

**Specification:**
```python
class RiskAssessmentAgent(BaseAgent):
    """Identify and assess project risks from discussions."""

    def _plan(self, context):
        """
        Input: transcript, notes
        Output: {
            "risks": [
                {
                    "risk": "Description",
                    "severity": "High/Medium/Low",
                    "probability": "High/Medium/Low",
                    "impact": "What could happen",
                    "mitigation": "How to prevent/reduce"
                },
                ...
            ],
            "overall_risk_level": "High/Medium/Low"
        }
        """
```

**Test Scenarios:**

1. **Technical Risk** - "We haven't tested the new API yet, launching next week"
2. **Resource Risk** - "Bob is the only one who knows this system and he's on vacation"
3. **Schedule Risk** - "Client expects delivery in 2 weeks, team says needs 4"

**Deliverable:**
- `RiskAssessmentAgent` implementation
- Test results identifying risks correctly
- Analysis of how this helps project management

---

## Part 5: Advanced Multi-Agent Patterns

**Learning Goal:** Implement sophisticated agent coordination patterns.

### 💻 Exercises

#### Exercise 5.1: Parallel Execution (3 hours)

Modify the manager to run independent agents in parallel:

**Current (Sequential):**
```
Step 1 → Step 2 → Step 3 → Step 4 → Step 5
  3s      3s      2s      2s      3s    = 13s total
```

**Target (Parallel):**
```
Step 1 → [Step 2, Step 3, Step 4] → Step 5
  3s           3s (parallel)          3s    = 9s total
```

**Implementation:**
```python
from concurrent.futures import ThreadPoolExecutor

def run_workflow_parallel(self, transcript: str):
    # Step 1: Insights (must go first)
    insights_result = self.agent_tools["insight_extractor"].run(...)

    # Steps 2-4: Run in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        notes_future = executor.submit(...)
        todos_future = executor.submit(...)
        github_future = executor.submit(...)

        notes_result = notes_future.result()
        todos_result = todos_future.result()
        github_result = github_future.result()

    # Step 5: Article (depends on notes)
    article_result = self.agent_tools["article_writer"].run(...)
```

**Requirements:**
1. Identify which agents can run in parallel
2. Implement parallel execution
3. Measure performance improvement
4. Handle errors in parallel execution

**Deliverable:**
- Parallel workflow implementation
- Performance comparison (sequential vs parallel)
- Dependency graph showing what can/can't be parallelized

#### Exercise 5.2: Agent Feedback Loop (3 hours)

Implement a feedback loop where agents review each other's work:

**Pattern:**
```
NoteTaker → EditorAgent → NoteTaker (refine)
                 ↓
           (provides feedback)
```

**Implementation:**
```python
class EditorAgent(BaseAgent):
    """Reviews and provides feedback on content."""

    def _plan(self, context):
        """
        Reviews notes and provides:
        - Clarity score
        - Completeness score
        - Suggested improvements
        - Specific edits
        """

# In manager:
def run_workflow_with_review(self, transcript: str):
    # First draft
    notes_v1 = self.agent_tools["note_taker"].run(...)

    # Review
    feedback = self.agent_tools["editor"].run(
        goal="Review and provide feedback on notes",
        context={"notes": notes_v1}
    )

    # Refine based on feedback
    notes_v2 = self.agent_tools["note_taker"].run(
        goal="Improve notes based on feedback",
        context={"notes": notes_v1, "feedback": feedback}
    )
```

**Deliverable:**
- `EditorAgent` implementation
- Workflow with feedback loop
- Comparison of v1 vs v2 notes quality
- Analysis of when feedback loops are beneficial

#### Exercise 5.3: Conditional Agent Selection (2 hours)

Implement dynamic agent selection based on meeting type:

```python
def run_adaptive_workflow(self, transcript: str):
    # Classify meeting type
    meeting_type = self._classify_meeting(transcript)

    if meeting_type == "technical":
        # Use technical writer
        article = self.agent_tools["technical_writer"].run(...)
    elif meeting_type == "customer":
        # Use customer communications specialist
        article = self.agent_tools["customer_comms"].run(...)
    elif meeting_type == "executive":
        # Use executive summary writer
        article = self.agent_tools["exec_summary"].run(...)
```

**Requirements:**
1. Create a meeting classifier
2. Implement 2-3 specialized article writers
3. Route to appropriate agent based on classification
4. Compare outputs for same content with different agents

**Deliverable:**
- Meeting classification logic
- Specialized article writer agents
- Adaptive workflow implementation
- Test results showing different outputs for different meeting types

---

## Part 6: Final Project

**Learning Goal:** Design and implement a complete multi-agent system for a real-world use case.

### 🎯 Project Options

Choose ONE of these projects (or propose your own):

#### Option A: Code Review Assistant

**Problem:** Developers need automated code review with multiple perspectives.

**Requirements:**
- **SecurityAgent** - Identifies security vulnerabilities
- **PerformanceAgent** - Suggests performance improvements
- **StyleAgent** - Checks code style and consistency
- **DocumentationAgent** - Reviews and suggests docs improvements
- **ManagerAgent** - Orchestrates all reviews and produces final report

**Input:** Code files or GitHub PR
**Output:** Comprehensive review report with actionable feedback

#### Option B: Research Paper Analyzer

**Problem:** Researchers need to quickly understand and summarize academic papers.

**Requirements:**
- **AbstractExtractorAgent** - Extracts and summarizes abstract
- **MethodologyAgent** - Analyzes research methods used
- **ResultsAgent** - Summarizes key findings
- **CitationAgent** - Analyzes citations and related work
- **CriticAgent** - Provides critical analysis and limitations
- **ManagerAgent** - Produces comprehensive summary

**Input:** PDF or text of research paper
**Output:** Structured analysis with summaries and insights

#### Option C: Customer Support System

**Problem:** Customer support teams need intelligent ticket routing and response suggestions.

**Requirements:**
- **TicketClassifierAgent** - Categorizes support tickets
- **SentimentAgent** - Analyzes customer emotion and urgency
- **KnowledgeBaseAgent** - Searches for relevant solutions
- **ResponseGeneratorAgent** - Drafts appropriate responses
- **EscalationAgent** - Determines if human escalation needed
- **ManagerAgent** - Coordinates full support workflow

**Input:** Customer support ticket
**Output:** Ticket classification, suggested response, escalation decision

#### Option D: Content Creation Pipeline

**Problem:** Content creators need help generating multi-platform content from a single topic.

**Requirements:**
- **ResearchAgent** - Gathers information on topic
- **OutlineAgent** - Creates content structure
- **BlogWriterAgent** - Writes long-form blog post
- **TwitterAgent** - Creates thread (280 char tweets)
- **LinkedInAgent** - Creates professional LinkedIn post
- **SEOAgent** - Optimizes content for search
- **ManagerAgent** - Orchestrates content creation

**Input:** Topic or content brief
**Output:** Blog post, Twitter thread, LinkedIn post, SEO recommendations

### 📋 Project Requirements

Your final project must include:

#### 1. Design Document (2-3 hours)

Create `project_design.md` with:

- **Problem Statement** - What problem are you solving?
- **Architecture Diagram** - Visual representation of your multi-agent system
- **Agent Specifications** - Each agent's role, inputs, outputs
- **Data Flow** - How information moves through the system
- **Challenges & Solutions** - What difficulties you anticipate

#### 2. Implementation (6-8 hours)

- Minimum 4 specialized agents
- 1 manager/orchestrator agent
- Working code that runs end-to-end
- Error handling and validation
- Clear logging and debugging output

#### 3. Testing & Validation (2-3 hours)

- At least 3 comprehensive test cases
- Edge cases and error scenarios
- Performance measurements
- Quality assessment of outputs

#### 4. Documentation (2 hours)

- `README.md` for your project
- Installation instructions
- Usage examples
- Code comments and docstrings
- Known limitations and future work

#### 5. Reflection Paper (1-2 hours)

Write `reflection.md` addressing:

- **What worked well?** - Successful design decisions
- **What was challenging?** - Difficulties and how you overcame them
- **Single vs Multi-Agent** - When would single agent be better?
- **Key Learnings** - What did you learn about multi-agent systems?
- **Future Improvements** - How would you extend this system?

---

## 📊 Grading Rubric

### Part 1: Single Agents (10 points)
- Exercise 1.1: Understanding SPOAR (3 pts)
- Exercise 1.2: Adding tools (3 pts)
- Exercise 1.3: LLM analysis (4 pts)

### Part 2: Specialization (15 points)
- Exercise 2.1: Analysis (5 pts)
- Exercise 2.2: Sentiment agent (10 pts)
  - Functionality (5 pts)
  - Testing (3 pts)
  - Documentation (2 pts)

### Part 3: Manager Pattern (15 points)
- Exercise 3.1: Data flow diagram (5 pts)
- Exercise 3.2: Integration (10 pts)
  - Correct integration (5 pts)
  - Testing (3 pts)
  - Analysis (2 pts)

### Part 4: Custom Agents (20 points)
- Exercise 4.1: Email generator (10 pts)
- Exercise 4.2: Risk assessment (10 pts)

### Part 5: Advanced Patterns (15 points)
- Exercise 5.1: Parallel execution (5 pts)
- Exercise 5.2: Feedback loops (5 pts)
- Exercise 5.3: Conditional selection (5 pts)

### Part 6: Final Project (25 points)
- Design document (5 pts)
- Implementation quality (10 pts)
  - Architecture (3 pts)
  - Code quality (3 pts)
  - Functionality (4 pts)
- Testing & validation (4 pts)
- Documentation (3 pts)
- Reflection paper (3 pts)

**Total: 100 points**

---

## 🎓 Learning Principles

This assignment teaches multi-agent systems through:

### 1. Progressive Complexity
Start simple (single agent) → Add specialization → Coordinate multiple agents → Advanced patterns

### 2. Hands-On Learning
Every concept is immediately applied through coding exercises

### 3. Real-World Applications
All examples solve actual problems (meetings, code review, content creation)

### 4. First Principles Thinking
- **Part 1:** What is an agent? (SPOAR loop)
- **Part 2:** Why specialize? (Single responsibility)
- **Part 3:** How to coordinate? (Manager pattern)
- **Part 4:** Building from scratch (Understanding deeply)
- **Part 5:** Advanced patterns (Real-world complexity)
- **Part 6:** Complete system (Integration)

### 5. Reflection & Analysis
Not just coding - understanding WHY things work the way they do

---

## 🚀 Getting Started

### Week 1
- **Day 1-2:** Part 1 (Single Agents)
- **Day 3-4:** Part 2 (Specialization)
- **Day 5-6:** Part 3 (Manager Pattern)
- **Day 7:** Review and catch up

### Week 2
- **Day 1-2:** Part 4 (Custom Agents)
- **Day 3-5:** Part 5 (Advanced Patterns)
- **Day 6-7:** Start Final Project (design + initial implementation)

### Week 3
- **Day 1-4:** Complete Final Project implementation
- **Day 5-6:** Testing, documentation, reflection
- **Day 7:** Final review and submission

---

## 📚 Additional Resources

### Recommended Reading

1. **Agent Fundamentals**
   - [LangChain Agent Documentation](https://python.langchain.com/docs/modules/agents/)
   - [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)

2. **Multi-Agent Systems**
   - ["Multi-Agent Systems" - Wikipedia](https://en.wikipedia.org/wiki/Multi-agent_system)
   - [AutoGen Framework](https://microsoft.github.io/autogen/)

3. **Design Patterns**
   - Manager/Worker Pattern
   - Chain of Responsibility Pattern
   - Strategy Pattern

### Tools & Frameworks

- **This Project** - Simple, educational implementation
- **LangChain** - Production-ready agent framework
- **AutoGen** - Microsoft's multi-agent framework
- **CrewAI** - Role-based multi-agent framework

---

## ❓ FAQs

**Q: Can I work in a team?**
A: Parts 1-5 should be done individually. Part 6 (final project) can be done in pairs if approved.

**Q: Can I use a different LLM provider?**
A: Yes! OpenAI, Anthropic, local models (Ollama) all work. Just adapt the API calls.

**Q: I don't have an API key / limited budget**
A: Use the free tier of Groq (fast, generous limits) or run local models with Ollama.

**Q: Can I propose my own final project?**
A: Absolutely! Discuss with instructor first to ensure appropriate scope.

**Q: How much prior knowledge do I need?**
A: You should be comfortable with Python (classes, inheritance, async). AI/ML knowledge helpful but not required.

**Q: What if I get stuck?**
A:
1. Read the documentation thoroughly
2. Check the tutorial and examples
3. Post in the discussion forum
4. Attend office hours
5. Debug systematically (print statements are your friend!)

---

## 📝 Submission

### What to Submit

Create a folder structure:
```
student_name_multiagent/
├── part1/
│   ├── part1_q1.md
│   ├── simple_agent_modified.py
│   └── llm_analysis.md
├── part2/
│   ├── comparison.md
│   └── sentiment_analyzer.py
├── part3/
│   ├── data_flow_diagram.png
│   └── multi_agent_system_modified.py
├── part4/
│   ├── email_generator.py
│   └── risk_assessment.py
├── part5/
│   ├── parallel_execution.py
│   ├── feedback_loop.py
│   └── conditional_selection.py
├── final_project/
│   ├── project_design.md
│   ├── README.md
│   ├── src/
│   │   ├── agent1.py
│   │   ├── agent2.py
│   │   └── manager.py
│   ├── tests/
│   ├── outputs/
│   └── reflection.md
└── README.md (overview of all parts)
```

### Submission Checklist

- [ ] All code runs without errors
- [ ] All required files present
- [ ] Code is well-commented
- [ ] All deliverables complete
- [ ] Tests pass
- [ ] Documentation clear and complete
- [ ] Reflection paper thoughtful and thorough

---

## 🎯 Success Criteria

You'll know you've succeeded when you can:

- ✅ Explain the SPOAR loop to someone else
- ✅ Decide when to use single vs multi-agent approaches
- ✅ Design a multi-agent system for a new problem
- ✅ Implement agents that coordinate effectively
- ✅ Debug and troubleshoot multi-agent systems
- ✅ Articulate the tradeoffs of different patterns
- ✅ Build production-ready multi-agent applications

---

## 🌟 Going Beyond

Want to go further? Try these extensions:

1. **Add human-in-the-loop** - Require approval before certain actions
2. **Implement agent memory** - Agents remember previous interactions
3. **Build a web interface** - Flask/FastAPI + React frontend
4. **Add real integrations** - GitHub API, Slack, email, databases
5. **Implement learning** - Agents improve based on feedback
6. **Multi-modal agents** - Process images, audio, video
7. **Distributed agents** - Run agents on different machines
8. **Agent marketplaces** - Share and discover agents

---

**Ready to build amazing multi-agent systems?**

Start with Part 1 and work your way through. Remember: **understanding beats completion**. Take time to really grasp each concept.

Good luck! 🚀

---

*Have questions or feedback? Open an issue or discussion on the repository.*


---

# Appendix: Teacher's Guide

# Teacher's Guide: Multi-Agent Systems Assignment

**For Instructors:** This guide provides solutions outlines, common pitfalls, grading guidance, and teaching notes.

---

## 📋 Course Overview

### Learning Arc

The assignment follows a deliberate progression:

```
Single Agent → Specialization → Orchestration → Custom Building → Advanced Patterns → Integration
   (What)         (Why)            (How)          (Practice)        (Real-world)      (Mastery)
```

### Time Management

**Typical Student Breakdown:**
- Fast students: 20-25 hours
- Average students: 25-30 hours
- Students needing help: 30-35 hours

**Critical checkpoints:**
- End of Week 1: Parts 1-3 complete (fundamentals)
- Mid Week 2: Part 4 complete (can build agents)
- End Week 2: Part 5 started (understands patterns)

---

## Part 1: Solution Outlines

### Exercise 1.1: Expected Answers

**Q: What happens in each phase?**

Good answer includes:
- **SENSE:** Gathers context (goal, available tools, previous actions)
- **PLAN:** LLM decides next action (which tool or complete)
- **ACT:** Executes the tool function
- **OBSERVE:** Records result and checks for errors
- **REFLECT:** LLM evaluates if progress was made

**Q: How many iterations?**
- Should observe: 2 iterations
  - Iteration 1: Uses calculator tool
  - Iteration 2: Returns complete answer

**Q: What if REFLECT removed?**
- Agent continues without self-evaluation
- Less likely to recover from errors
- No learning or adaptation

**Common mistakes:**
- Students confuse OBSERVE (records data) with REFLECT (evaluates progress)
- Don't understand why iterations are needed

### Exercise 1.2: Get Weather Tool

**Key learning:**
- Agent automatically discovers new tools
- No changes needed to agent logic
- LLM reads tool descriptions and chooses appropriately

**Testing hint:**
```python
# Good test
agent.run("What's the weather in Tokyo?")
# Should use get_weather tool

# Edge case test
agent.run("Is it sunny in Paris?")
# Should still use get_weather, then interpret result
```

**Common issues:**
- Tool function not returning string
- Tool description unclear to LLM
- Forgetting to update tools dict

### Exercise 1.3: LLM Analysis

**Expected observations:**

Students should notice:
1. **Prompt structure:** System message + user message
2. **Context passing:** Previous results included in prompt
3. **JSON requirement:** LLM must respond in specific format
4. **Temperature:** Low (0.3) for consistency

**Good analysis includes:**
- How LLM uses tool descriptions to decide
- Role of JSON schema in guiding output
- Impact of temperature on creativity vs consistency

---

## Part 2: Solution Outlines

### Exercise 2.1: Specialization Analysis

**Key points students should identify:**

| Aspect | Simple Agent | InsightExtractorAgent |
|--------|-------------|----------------------|
| Purpose | General problem solving | Extract insights only |
| Tools | Multiple (search, calculate) | None (LLM-only) |
| Prompt | Generic "use tools or complete" | Specific "extract 5-7 insights" |
| Output | Variable | Structured (list of insights) |

**What makes it specialized:**
- Focused prompt engineering
- Domain-specific output format
- Single clear responsibility

### Exercise 2.2: Sentiment Analyzer

**Evaluation criteria:**

**Basic (60%):**
```python
{
  "overall_sentiment": "positive/negative/neutral",
  "confidence": 0.85
}
```

**Good (80%):**
```python
{
  "overall_sentiment": "positive",
  "confidence": 0.85,
  "emotions": ["joy", "excitement"],
  "tone": "enthusiastic"
}
```

**Excellent (100%):**
```python
{
  "overall_sentiment": "positive",
  "confidence": 0.85,
  "emotions": [
    {"emotion": "joy", "intensity": 0.9},
    {"emotion": "excitement", "intensity": 0.7}
  ],
  "tone": "enthusiastic",
  "key_phrases": ["amazing", "best purchase"],
  "sentiment_shifts": "None detected"
}
```

**Common mistakes:**
- Returning sentiment as string instead of structured data
- Not handling mixed sentiment well
- Overly complex prompts that confuse the LLM
- Not testing edge cases (sarcasm, mixed sentiment)

---

## Part 3: Solution Outlines

### Exercise 3.1: Data Flow Diagram

**Minimum acceptable:**
```
Transcript → InsightExtractor → insights[]
insights[] → NoteTaker → notes{}
notes{} → TodoCreator → todos[]
notes{} → GitHubManager → github{}
notes{} + insights[] → ArticleWriter → article{}
```

**Excellent diagram shows:**
- Context accumulation at each step
- Which agents depend on which outputs
- Parallel opportunities (GitHubManager and TodoCreator)
- What goes into final results

### Exercise 3.2: Integration

**Grading checklist:**
- [ ] Agent correctly added to `agent_tools` dict
- [ ] Workflow step properly positioned
- [ ] Context passed correctly
- [ ] Results saved to `workflow_results`
- [ ] Tested with actual transcript
- [ ] Output makes sense

**Common issues:**
- Forgetting to initialize agent in `__init__`
- Not passing workflow_context
- Hardcoding max_iterations too low
- Not handling case where agent fails

---

## Part 4: Teaching Notes

### Exercise 4.1: Email Generator

**What makes a good email agent:**

```python
# Good prompt structure
prompt = f"""
You are a professional email writer.

Context: {notes}

Task: Write a follow-up email with:
- Clear subject line
- Professional greeting
- Summary of meeting
- Action items with owners
- Next steps
- Professional closing

Tone: {tone}
Recipients: {recipients}

Output JSON with: subject, body, cc, tone
"""
```

**Key teaching points:**
1. **Prompt engineering matters** - Specific instructions = better output
2. **Context is key** - More context = more relevant emails
3. **Structured output** - JSON makes it usable programmatically
4. **Tone control** - Important for different situations

**Red flags in student work:**
- Generic emails that don't use context
- No clear structure
- Missing personalization
- Inappropriate tone

### Exercise 4.2: Risk Assessment

**Good risk assessment characteristics:**

```python
{
  "risks": [
    {
      "risk": "Single point of failure - Bob is only engineer familiar with legacy system",
      "severity": "High",
      "probability": "Medium",
      "impact": "Project delays if Bob unavailable",
      "mitigation": "Knowledge transfer sessions, documentation",
      "category": "Resource risk"
    }
  ],
  "overall_risk_level": "Medium-High",
  "recommendation": "Prioritize knowledge transfer before Bob's vacation"
}
```

**Students should understand:**
- Different risk categories (technical, resource, schedule, scope)
- Risk matrix (severity × probability)
- Actionable mitigation strategies
- Prioritization of risks

---

## Part 5: Teaching Notes

### Exercise 5.1: Parallel Execution

**Key concepts:**

1. **Dependency Analysis:**
   ```
   Independent agents can run in parallel:
   - TodoCreator only needs notes
   - GitHubManager only needs notes
   - SentimentAnalyzer only needs transcript

   These can ALL run in parallel after NoteTaker
   ```

2. **Performance gains:**
   - Sequential: Sum of all times
   - Parallel: Max of parallel group times

3. **Error handling:**
   ```python
   try:
       result = future.result(timeout=30)
   except TimeoutError:
       # Handle timeout
   except Exception as e:
       # Handle other errors
   ```

**Common mistakes:**
- Running dependent tasks in parallel (will fail)
- Not handling exceptions from futures
- Not understanding GIL implications (Python)
- Not measuring actual performance

### Exercise 5.2: Feedback Loops

**Teaching emphasis:**

**When feedback loops help:**
- Quality-critical outputs (legal docs, medical reports)
- Iterative improvement (writing, design)
- Learning systems (improve over time)

**When they don't:**
- Time-sensitive tasks
- Simple, clear-cut outputs
- When marginal gains don't justify cost

**Cost analysis:**
```
Without feedback: 1 agent × 3 seconds = 3 seconds
With feedback: 2 agents × 3 seconds + 1 refinement × 3 seconds = 9 seconds

Is 3× cost worth the quality improvement?
```

**Students should implement:**
- Measurable quality metrics
- Max iteration limits
- Early stopping criteria

### Exercise 5.3: Conditional Selection

**Pattern recognition:**

```python
def classify_meeting(self, transcript):
    # Use LLM to classify
    prompt = f"""
    Classify this meeting as one of:
    - technical: Engineering, architecture, code review
    - customer: Sales, support, client meetings
    - executive: Strategy, planning, leadership
    - team: Standups, retrospectives, 1:1s

    Transcript: {transcript}

    Return only the category.
    """
```

**Discussion questions:**
1. Why not hard-code rules (if "code" in transcript...)?
2. What if meeting spans multiple categories?
3. How to handle misclassification?

---

## Part 6: Final Project Guidance

### Project Evaluation Framework

#### Design Document (5 points)

**Excellent (5/5):**
- Clear problem statement with real-world context
- Detailed architecture diagram
- Well-defined agent responsibilities
- Data flow clearly explained
- Anticipated challenges with solutions

**Good (3-4/5):**
- Clear problem statement
- Basic architecture diagram
- Agent roles defined
- Some consideration of challenges

**Needs improvement (1-2/5):**
- Vague problem
- Missing or unclear diagram
- Unclear agent boundaries

#### Implementation (10 points)

**Architecture (3 points):**
- Clean separation of concerns
- Appropriate agent granularity
- Sensible manager orchestration

**Code Quality (3 points):**
- Well-structured and readable
- Proper error handling
- Good naming conventions
- Appropriate comments

**Functionality (4 points):**
- All agents work correctly
- Workflow completes successfully
- Handles edge cases
- Produces useful output

#### Common Project Issues

**Over-engineering:**
```python
# Too complex
class SuperIntelligentAgent:
    def analyze_with_ml_pipeline(self):
        # 500 lines of unnecessary complexity
```

**Under-engineering:**
```python
# Too simple
class BasicAgent:
    def run(self):
        return "generic output"
```

**Right level:**
```python
class FocusedAgent:
    """Does one thing well."""
    def _plan(self, context):
        # Clear, focused implementation
        # ~30-50 lines
```

### Project-Specific Notes

#### Option A: Code Review Assistant

**Key challenges:**
- Parsing code files correctly
- Context window limits (large files)
- Different languages need different analysis

**Success indicators:**
- Actually finds real issues
- Actionable suggestions
- Appropriate severity levels

#### Option B: Research Paper Analyzer

**Key challenges:**
- PDF parsing
- Academic jargon
- Citation extraction

**Success indicators:**
- Accurate methodology extraction
- Useful summary for non-experts
- Identifies key contributions

#### Option C: Customer Support System

**Key challenges:**
- Real-time requirements
- Response quality
- Escalation criteria

**Success indicators:**
- Correct classification
- Helpful responses
- Appropriate escalation decisions

#### Option D: Content Creation Pipeline

**Key challenges:**
- Maintaining consistency across platforms
- Platform-specific formatting
- SEO optimization

**Success indicators:**
- Platform-appropriate content
- Consistent messaging
- Actual SEO value

---

## Grading Guidelines

### Philosophical Approach

**Value understanding over completion:**
- Student who completes 70% but deeply understands > 100% completion with shallow understanding
- Encourage experimentation and learning from failures
- Reward thoughtful reflection

### Partial Credit Guidelines

**Part 1-5 Exercises:**
- Attempted but incomplete: 50%
- Works but has issues: 70%
- Works well: 90%
- Exceptional (goes beyond): 100%+

**Final Project:**
- Minimum viable (basic functionality): 60%
- Good implementation: 75%
- Excellent with thorough testing: 90%
- Outstanding with innovation: 100%+

### Red Flags

**Academic integrity issues:**
- Code clearly copied without understanding
- Can't explain their own implementation
- Documentation doesn't match code

**Insufficient effort:**
- Minimal changes to provided code
- No testing or validation
- Copy-paste from examples without adaptation

---

## Office Hours FAQ

**Q: "My agent isn't working!"**

Debugging checklist:
1. Is the API key set correctly?
2. Is the LLM returning JSON?
3. Is the JSON being parsed correctly?
4. Are you passing the right context?
5. Is max_iterations too low?

**Q: "My agents are too slow!"**

Optimization strategies:
1. Lower temperature (faster, more deterministic)
2. Use faster model (haiku vs sonnet)
3. Parallel execution
4. Cache results when possible
5. Reduce prompt length

**Q: "Output quality is poor"**

Improvement strategies:
1. Better prompt engineering
2. More specific instructions
3. Few-shot examples in prompt
4. Higher temperature for creativity
5. Feedback loops for refinement

**Q: "I don't understand when to use multiple agents"**

Decision framework:
```
Use single agent when:
- Simple, focused task
- Linear workflow
- Speed is critical

Use multiple agents when:
- Complex, multi-faceted problem
- Different expertise needed
- Can benefit from specialization
- Parallel processing possible
```

---

## Extension Activities

For advanced students who finish early:

### 1. Agent Communication Protocols

Design agents that message each other:
```python
class NegotiatorAgent:
    def negotiate_with(self, other_agent, proposal):
        # Back-and-forth communication
        pass
```

### 2. Learning Agents

Implement agents that improve based on feedback:
```python
class LearningAgent:
    def __init__(self):
        self.feedback_history = []

    def learn_from_feedback(self, feedback):
        self.feedback_history.append(feedback)
        # Adjust behavior
```

### 3. Multi-Modal Agents

Process images, audio, or video:
```python
class ImageAnalyzerAgent:
    def _plan(self, context):
        image = context["image"]
        # Use vision model
```

---

## Assessment Rubric Details

### Code Quality Indicators

**Excellent:**
- Clear, self-documenting code
- Proper error handling
- Well-organized structure
- Appropriate abstractions
- Good test coverage

**Good:**
- Readable code
- Basic error handling
- Logical organization
- Some testing

**Needs Improvement:**
- Hard to follow
- No error handling
- Disorganized
- No testing

### Documentation Quality

**Excellent:**
- Clear setup instructions
- Usage examples
- API documentation
- Known limitations
- Future work

**Good:**
- Basic setup instructions
- Some examples
- Key functions documented

**Needs Improvement:**
- Minimal or confusing docs
- Missing critical information

---

## Common Misconceptions

### "More agents = better system"

**Reality:** More agents = more complexity

Teach students:
- Each agent has overhead (time, cost, complexity)
- Start simple, add agents only when justified
- One good agent > three mediocre agents

### "Agents are just prompts"

**Reality:** Agents are autonomous systems that use LLMs

Key differences:
- Agents can take actions (tools)
- Agents iterate until goal achieved
- Agents observe and reflect

### "Multi-agent = parallel execution"

**Reality:** Multi-agent is about specialization

Clarify:
- Can run sequentially or in parallel
- Value is in focused expertise
- Coordination is the challenge

---

## Tips for Effective Teaching

### Week 1: Foundation

- **Live demo:** Walk through SPOAR loop with debugger
- **Group exercise:** Design agents for a coffee shop (OrderTaker, Barista, CashierAgent)
- **Discussion:** When have you seen specialization in real life?

### Week 2: Practice

- **Code review sessions:** Students review each other's agents
- **Debugging workshop:** Common issues and solutions
- **Pattern discussion:** Manager vs peer-to-peer architectures

### Week 3: Projects

- **Check-ins:** Brief 1:1s on project progress
- **Peer presentations:** Students present designs to each other
- **Office hours:** Extended availability for debugging

---

## Success Metrics

Track these to improve the course:

- **Completion rate per part** - Where do students struggle?
- **Time spent** - Is pacing realistic?
- **Office hours questions** - Common confusion points?
- **Final project quality** - Are students ready?
- **Student feedback** - What worked? What didn't?

---

## Additional Resources for Teaching

### Recommended Videos

1. "How LLMs Work" - 3Blue1Brown
2. "Agent Fundamentals" - Andrej Karpathy
3. "Multi-Agent Systems in Practice" - Various

### Papers

1. "ReAct: Synergizing Reasoning and Acting in Language Models"
2. "Generative Agents: Interactive Simulacra of Human Behavior"
3. "Communicative Agents for Software Development"

### Tools

1. LangSmith - Trace and debug agent runs
2. Weights & Biases - Track experiments
3. Streamlit - Quick UI for demos

---

**Remember:** The goal isn't perfect code, it's deep understanding. Encourage experimentation, celebrate learning from failures, and foster curiosity about multi-agent systems.

**Built with ❤️ by Siddhant and his wife Claudia.**
