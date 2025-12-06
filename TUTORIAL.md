# Multi-Agent Tutorial: From Single to Multi-Agent

This tutorial shows how we extend the simple SPOAR agent into a multi-agent system using the manager pattern.

---

## Part 1: Understanding the Foundation (SPOAR Loop)

### The Simple Agent

In `simple_agent.py`, we have one agent that can:
- Use tools (search, calculate)
- Follow the SPOAR loop
- Complete a single goal

```python
agent = SimpleAgent()
result = agent.run("What is 25 * 4?")
# Agent uses calculator tool and returns answer
```

**Limitation:** What if we need to do multiple complex tasks?

---

## Part 2: The Multi-Agent Approach

### Why Multiple Agents?

Imagine you need to:
1. Extract insights from a transcript
2. Create meeting notes
3. Generate todos
4. Set up a GitHub repo
5. Write an article

One agent doing all this would be:
- Complex to manage
- Hard to debug
- Difficult to specialize

**Solution:** Create specialized agents, each expert at one task!

---

## Part 3: Building the Base

### Step 1: Create a Reusable Base Agent

```python
class BaseAgent:
    """Base agent class implementing the SPOAR loop pattern."""

    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.llm = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "openai/gpt-oss-120b"

    def run(self, goal: str, context: Dict = None, max_iterations: int = 3):
        """Main SPOAR loop for the agent."""
        # ... SPOAR implementation ...
```

**Key Points:**
- `name` and `role` identify the agent
- `run()` implements the SPOAR loop
- `context` allows passing information between agents

### Step 2: Create Specialized Agents

Each specialized agent inherits from `BaseAgent` and overrides `_plan()`:

```python
class InsightExtractorAgent(BaseAgent):
    def __init__(self):
        super().__init__("InsightExtractor", "Extract key insights")

    def _plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Specialized planning for insight extraction."""

        transcript = context.get("transcript", "")

        prompt = f"""
        You are an expert at analyzing meeting transcripts.

        Transcript:
        {transcript}

        Extract 5-7 key insights.

        Respond with JSON:
        {{
          "action": "COMPLETE",
          "insights": ["insight 1", "insight 2", ...],
          "answer": "Extracted N insights"
        }}
        """

        response = self.llm.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You extract insights. Respond with JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return self._parse_json(response.choices[0].message.content)
```

**Key Points:**
- Inherits all SPOAR loop behavior from `BaseAgent`
- Only customizes `_plan()` for its specific task
- Returns structured JSON output

---

## Part 4: The Manager Pattern

### Step 3: Create Manager Agent

The manager treats agents as "tools":

```python
class ManagerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Manager", "Orchestrate specialized agents")

        # Agents become "tools"
        self.agent_tools = {
            "insight_extractor": InsightExtractorAgent(),
            "note_taker": NoteTakerAgent(),
            "todo_creator": TodoCreatorAgent(),
            "github_manager": GitHubManagerAgent(),
            "article_writer": ArticleWriterAgent()
        }

    def run_workflow(self, transcript: str):
        """Run the complete workflow."""

        workflow_context = {"transcript": transcript}

        # Step 1: Extract insights
        insights_result = self.agent_tools["insight_extractor"].run(
            goal="Extract key insights",
            context=workflow_context,
            max_iterations=2
        )

        # Pass results to next agent
        workflow_context["insights"] = insights_result["result"]

        # Step 2: Create notes
        notes_result = self.agent_tools["note_taker"].run(
            goal="Create meeting notes",
            context=workflow_context,
            max_iterations=2
        )

        # ... continue with more agents ...

        return all_results
```

**Key Points:**
- Manager doesn't do the work itself
- Manager coordinates specialized agents
- Context flows from one agent to the next
- Each agent builds on previous results

---

## Part 5: Data Flow

### How Information Flows

```
┌──────────────┐
│  Transcript  │
└──────┬───────┘
       │
       ▼
┌─────────────────────┐
│ InsightExtractor    │ ──► insights: ["...", "..."]
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ NoteTaker           │ ──► notes: {summary: "...", ...}
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ TodoCreator         │ ──► todos: [{task: "...", ...}]
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ GitHubManager       │ ──► github: {name: "...", ...}
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ ArticleWriter       │ ──► article: {title: "...", ...}
└─────────────────────┘
```

### Context Dictionary

The context dictionary carries information:

```python
# After InsightExtractor
workflow_context = {
    "transcript": "original transcript text",
    "insights": ["insight 1", "insight 2", ...]
}

# After NoteTaker
workflow_context = {
    "transcript": "original transcript text",
    "insights": ["insight 1", "insight 2", ...],
    "notes": {
        "summary": "...",
        "key_points": ["...", "..."],
        "decisions": ["...", "..."]
    }
}

# Each agent adds to the context
```

---

## Part 6: Complete Example

### Creating a New Specialized Agent

Let's create a `SentimentAnalyzerAgent`:

```python
class SentimentAnalyzerAgent(BaseAgent):
    """Agent that analyzes sentiment of meeting discussions."""

    def __init__(self):
        super().__init__(
            "SentimentAnalyzer",
            "Analyze sentiment and tone of discussions"
        )

    def _plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Plan sentiment analysis."""

        transcript = context.get("transcript", "")

        prompt = f"""You are a sentiment analysis expert.

Transcript:
{transcript}

Analyze the overall sentiment and tone of this meeting.

Consider:
- Overall mood (positive, neutral, negative)
- Team dynamics (collaborative, tense, productive)
- Energy level (high, medium, low)
- Key concerns or excitement

Respond with ONLY valid JSON:
{{
  "action": "COMPLETE",
  "sentiment": {{
    "overall_mood": "positive",
    "team_dynamics": "collaborative",
    "energy_level": "high",
    "summary": "Brief summary of the sentiment"
  }},
  "answer": "Analyzed meeting sentiment"
}}"""

        response = self.llm.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You analyze sentiment. Respond with JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        plan = self._parse_json(response.choices[0].message.content)
        self._log_phase("🧠 PLAN", {
            "action": "COMPLETE",
            "mood": plan.get("sentiment", {}).get("overall_mood", "N/A")
        })

        return plan
```

### Adding to Manager

```python
class ManagerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Manager", "Orchestrate specialized agents")

        self.agent_tools = {
            # ... existing agents ...
            "sentiment_analyzer": SentimentAnalyzerAgent(),  # Add new agent
        }

    def run_workflow(self, transcript: str):
        # ... existing workflow ...

        # Add new step
        print("\n📍 STEP 6: Analyzing Sentiment")
        sentiment_result = self.agent_tools["sentiment_analyzer"].run(
            goal="Analyze meeting sentiment",
            context=workflow_context,
            max_iterations=2
        )

        if sentiment_result["success"]:
            sentiment_data = json.loads(sentiment_result["result"])
            self.workflow_results["sentiment"] = sentiment_data.get("sentiment", {})
```

---

## Part 7: Advanced Patterns

### Pattern 1: Conditional Workflows

Run different agents based on conditions:

```python
def run_workflow(self, transcript: str):
    # Always extract insights
    insights_result = self.agent_tools["insight_extractor"].run(...)

    # Check if meeting was about technical topics
    if "engineering" in transcript.lower() or "code" in transcript.lower():
        # Run technical writer
        article_result = self.agent_tools["technical_writer"].run(...)
    else:
        # Run general article writer
        article_result = self.agent_tools["article_writer"].run(...)
```

### Pattern 2: Feedback Loops

Let agents refine each other's work:

```python
def run_workflow_with_refinement(self, transcript: str):
    # Step 1: Create notes
    notes_result = self.agent_tools["note_taker"].run(...)

    # Step 2: Review notes (different agent)
    review_result = self.agent_tools["editor"].run(
        goal="Review and improve notes",
        context={"notes": notes_result["result"]},
        max_iterations=2
    )

    # Step 3: Final refinement
    final_notes = self.agent_tools["note_taker"].run(
        goal="Apply reviewer feedback",
        context={"original_notes": notes_result["result"],
                 "feedback": review_result["result"]},
        max_iterations=2
    )
```

### Pattern 3: Parallel Execution

Run independent agents simultaneously:

```python
from concurrent.futures import ThreadPoolExecutor

def run_workflow_parallel(self, transcript: str):
    workflow_context = {"transcript": transcript}

    # Step 1: Extract insights (required first)
    insights_result = self.agent_tools["insight_extractor"].run(...)
    workflow_context["insights"] = insights_result["result"]

    # Steps 2-4: Run in parallel (independent of each other)
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit all tasks
        notes_future = executor.submit(
            self.agent_tools["note_taker"].run,
            "Create notes", workflow_context, 2
        )
        todos_future = executor.submit(
            self.agent_tools["todo_creator"].run,
            "Create todos", workflow_context, 2
        )
        sentiment_future = executor.submit(
            self.agent_tools["sentiment_analyzer"].run,
            "Analyze sentiment", workflow_context, 2
        )

        # Get results
        notes_result = notes_future.result()
        todos_result = todos_future.result()
        sentiment_result = sentiment_future.result()

    # Continue with dependent tasks...
```

---

## Part 8: Best Practices

### 1. Clear Agent Responsibilities

Each agent should have ONE clear purpose:

**Good:**
```python
class NoteTakerAgent(BaseAgent):
    """Creates concise, structured meeting notes."""
```

**Bad:**
```python
class NoteTakerAndTodoAndEmailAgent(BaseAgent):
    """Does everything related to meetings."""
```

### 2. Consistent Output Format

All agents should return the same structure:

```python
{
    "success": True/False,
    "result": {...},  # The actual output
    "agent": "AgentName"
}
```

### 3. Context Management

Keep context clean and organized:

```python
# Good - clear keys
workflow_context = {
    "transcript": "...",
    "insights": [...],
    "notes": {...}
}

# Bad - unclear keys
workflow_context = {
    "data": "...",
    "stuff": [...],
    "results": {...}
}
```

### 4. Error Handling

Each agent should handle its own errors:

```python
def _plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
    try:
        # Normal planning logic
        response = self.llm.chat.completions.create(...)
        return self._parse_json(response.choices[0].message.content)
    except Exception as e:
        # Return error structure
        return {
            "action": "COMPLETE",
            "answer": f"Error: {str(e)}",
            "error": True
        }
```

### 5. Logging and Observability

Log important steps:

```python
def run_workflow(self, transcript: str):
    print("\n📍 STEP 1: Extracting Insights")
    print("-" * 80)

    insights_result = self.agent_tools["insight_extractor"].run(...)

    if insights_result["success"]:
        print(f"✅ Extracted {len(insights_result['insights'])} insights")
    else:
        print(f"❌ Failed: {insights_result.get('error', 'Unknown error')}")
```

---

## Part 9: Testing Your Multi-Agent System

### Unit Test Individual Agents

```python
def test_insight_extractor():
    agent = InsightExtractorAgent()

    test_transcript = """
    Meeting about product launch.
    Key points: Launch in Q1, target SMBs, need docs.
    """

    result = agent.run(
        goal="Extract insights",
        context={"transcript": test_transcript},
        max_iterations=2
    )

    assert result["success"] == True
    assert len(result["result"]["insights"]) > 0
```

### Integration Test Workflow

```python
def test_full_workflow():
    manager = ManagerAgent()

    test_transcript = "Sample meeting transcript..."

    results = manager.run_workflow(test_transcript)

    # Check all expected outputs
    assert "insights" in results
    assert "notes" in results
    assert "todos" in results
    assert "github" in results
    assert "article" in results
```

---

## Part 10: Summary

### Key Concepts

1. **SPOAR Loop** - The foundation for all agents
2. **Base Agent** - Reusable implementation of SPOAR
3. **Specialized Agents** - Each has one clear purpose
4. **Manager Pattern** - Orchestrates agents as tools
5. **Context Flow** - Data passes between agents

### Progression Path

```
Simple Agent (simple_agent.py)
    ↓
Base Agent Class (reusable SPOAR)
    ↓
Specialized Agents (inherit from Base)
    ↓
Manager Agent (orchestrates specialists)
    ↓
Multi-Agent System (complete workflow)
```

### When to Use Each

| Scenario | Approach |
|----------|----------|
| Simple task | Simple Agent |
| Need specialization | Specialized Agent |
| Multiple related tasks | Manager + Specialists |
| Complex workflow | Multi-Agent System |

---

## Next Steps

1. Try creating your own specialized agent
2. Add it to the manager workflow
3. Experiment with parallel execution
4. Build conditional workflows
5. Add real API integrations

Happy building! 🚀
