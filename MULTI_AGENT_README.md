# Multi-Agent System with Manager Pattern

A beginner-friendly multi-agent system built on the **SPOAR (Sense-Plan-Act-Observe-Reflect)** pattern. This system uses specialized agents orchestrated by a manager agent to handle complex workflows.

---

## Architecture Overview

### Manager Pattern

The **Manager Agent** acts as an orchestrator that coordinates multiple specialized agents. Each agent is a "tool" that the manager can use.

```
┌─────────────────────────────────────────────────┐
│           MANAGER AGENT                         │
│  (Orchestrates the entire workflow)             │
└────────────┬────────────────────────────────────┘
             │
             ├─────► InsightExtractorAgent
             │       (Extracts key insights)
             │
             ├─────► NoteTakerAgent
             │       (Creates structured notes)
             │
             ├─────► TodoCreatorAgent
             │       (Generates action items)
             │
             ├─────► GitHubManagerAgent
             │       (Plans repository structure)
             │
             └─────► ArticleWriterAgent
                     (Writes Medium article outline)
```

### The SPOAR Loop

Each agent follows the same pattern:

| Phase | Purpose | What Happens |
|-------|---------|--------------|
| **SENSE** | Gather context | Collect current state, goal, and available information |
| **PLAN** | Decide action | LLM determines what to do next |
| **ACT** | Execute | Perform the planned action |
| **OBSERVE** | Record results | Log what happened and check success |
| **REFLECT** | Evaluate | Assess progress toward the goal |

---

## Quick Start

### 1. Install Dependencies

```bash
pip install groq python-dotenv
```

### 2. Setup API Key

```bash
# Create .env file
echo "GROQ_API_KEY=your-groq-api-key-here" > .env
```

Get your API key at: [console.groq.com/keys](https://console.groq.com/keys)

### 3. Run the Multi-Agent System

```bash
python multi_agent_system.py
```

---

## How It Works

### Workflow Steps

The manager runs a sequential workflow:

1. **Extract Insights** - Analyzes meeting transcript and extracts 5-7 key insights
2. **Create Notes** - Generates structured meeting notes (summary, key points, decisions, next steps)
3. **Create Todos** - Produces actionable todo items with priorities
4. **Plan GitHub Repo** - Designs repository structure and README outline
5. **Write Article** - Creates Medium article outline with sections

### Example Output

```
============================================================
🎬 STARTING MULTI-AGENT WORKFLOW
============================================================

📍 STEP 1: Extracting Key Insights
------------------------------------------------------------
🤖 AGENT: InsightExtractor
🎯 GOAL: Extract key insights from the meeting transcript

--- INSIGHTEXTRACTOR - ITERATION 1 ---
👁️  SENSE
  iteration: 1
  goal: Extract key insights from the meeting transcript

🧠 PLAN
  action: COMPLETE
  insights_count: 7

✅ COMPLETE
  result: Task completed

📍 STEP 2: Creating Concise Notes
------------------------------------------------------------
...

✅ WORKFLOW COMPLETE - SUMMARY
============================================================
📊 Insights Extracted: 7
📝 Notes Sections: 4
✅ Todos Created: 6
🔨 GitHub Repo: ai-analytics-dashboard
📰 Article Title: Building Scalable ML Analytics: Our Journey

💡 Check 'workflow_results.json' for detailed output!
```

---

## Code Structure

### Base Agent Class

All agents inherit from `BaseAgent`:

```python
class BaseAgent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.llm = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "openai/gpt-oss-120b"

    def run(self, goal: str, context: Dict = None, max_iterations: int = 3):
        # Implements SPOAR loop
        for iteration in range(1, max_iterations + 1):
            context = self._sense(context)
            plan = self._plan(context)
            if plan["action"] == "COMPLETE":
                return plan
            result = self._act(plan)
            observation = self._observe(plan, result)
            reflection = self._reflect(context, observation)
```

### Specialized Agents

Each specialized agent overrides `_plan()`:

```python
class InsightExtractorAgent(BaseAgent):
    def __init__(self):
        super().__init__("InsightExtractor", "Extract key insights")

    def _plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # Custom planning logic for insight extraction
        prompt = f"""Extract key insights from: {context['transcript']}"""
        # LLM call and JSON response
        return plan
```

### Manager Agent

Coordinates all agents:

```python
class ManagerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Manager", "Orchestrate specialized agents")
        self.agent_tools = {
            "insight_extractor": InsightExtractorAgent(),
            "note_taker": NoteTakerAgent(),
            # ... more agents
        }

    def run_workflow(self, transcript: str):
        # Step 1: Extract insights
        insights = self.agent_tools["insight_extractor"].run(...)

        # Step 2: Create notes
        notes = self.agent_tools["note_taker"].run(...)

        # ... continue workflow
```

---

## Customization Guide

### 1. Add a New Specialized Agent

```python
class SummarizerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Summarizer", "Create executive summaries")

    def _plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""Create a 3-sentence summary of: {context['notes']}"""

        response = self.llm.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You create concise summaries. Respond with JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return self._parse_json(response.choices[0].message.content)
```

Then add to manager:

```python
class ManagerAgent(BaseAgent):
    def __init__(self):
        # ... existing code ...
        self.agent_tools["summarizer"] = SummarizerAgent()
```

### 2. Modify the Workflow

Edit `run_workflow()` in ManagerAgent:

```python
def run_workflow(self, transcript: str):
    # ... existing steps ...

    # Add new step
    print("\n📍 STEP 6: Creating Executive Summary")
    summary = self.agent_tools["summarizer"].run(
        goal="Create executive summary",
        context=workflow_context,
        max_iterations=2
    )
```

### 3. Change Agent Behavior

Modify the prompt in any agent's `_plan()` method:

```python
def _plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
    prompt = f"""
    You are a creative writer.  # ← Change persona

    Style: Casual and engaging    # ← Add style guide

    Task: {context['goal']}

    Requirements:                  # ← Add specific requirements
    - Use bullet points
    - Keep it under 500 words
    - Include examples

    Respond with JSON:
    {{...}}
    """
```

### 4. Add Parallel Execution

Run multiple agents in parallel using threading:

```python
from concurrent.futures import ThreadPoolExecutor

def run_workflow_parallel(self, transcript: str):
    workflow_context = {"transcript": transcript}

    # Step 1: Extract insights (must go first)
    insights_result = self.agent_tools["insight_extractor"].run(...)
    workflow_context["insights"] = insights_result["result"]

    # Steps 2-3: Run in parallel
    with ThreadPoolExecutor(max_workers=2) as executor:
        notes_future = executor.submit(
            self.agent_tools["note_taker"].run,
            "Create notes", workflow_context, 2
        )
        todos_future = executor.submit(
            self.agent_tools["todo_creator"].run,
            "Create todos", workflow_context, 2
        )

        notes_result = notes_future.result()
        todos_result = todos_future.result()
```

---

## Advanced Features

### 1. Add Memory Across Agents

```python
class ManagerAgent(BaseAgent):
    def __init__(self):
        super().__init__(...)
        self.shared_memory = {}  # Shared across all agents

    def run_workflow(self, transcript: str):
        workflow_context = {
            "transcript": transcript,
            "shared_memory": self.shared_memory  # Pass to all agents
        }

        # Agents can now read/write to shared memory
        insights_result = self.agent_tools["insight_extractor"].run(
            context=workflow_context
        )

        # Update shared memory
        self.shared_memory["insights"] = insights_result["result"]
```

### 2. Add Error Handling and Retry

```python
def run_workflow(self, transcript: str):
    max_retries = 2

    for attempt in range(max_retries):
        try:
            insights_result = self.agent_tools["insight_extractor"].run(...)

            if insights_result["success"]:
                break
            else:
                print(f"⚠️  Retry {attempt + 1}/{max_retries}")
        except Exception as e:
            print(f"❌ Error: {e}")
            if attempt == max_retries - 1:
                return {"error": str(e)}
```

### 3. Add Logging and Observability

```python
import logging
from datetime import datetime

class ManagerAgent(BaseAgent):
    def __init__(self):
        super().__init__(...)
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            filename=f'workflow_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("ManagerAgent")

    def run_workflow(self, transcript: str):
        self.logger.info("Starting workflow")

        insights_result = self.agent_tools["insight_extractor"].run(...)
        self.logger.info(f"Insights extracted: {len(insights_result.get('insights', []))}")
```

### 4. Add Human-in-the-Loop Approval

```python
def run_workflow(self, transcript: str):
    # Extract insights
    insights_result = self.agent_tools["insight_extractor"].run(...)

    # Show insights and ask for approval
    print("\n📋 Extracted Insights:")
    for i, insight in enumerate(insights_result.get("insights", []), 1):
        print(f"  {i}. {insight}")

    approval = input("\n✅ Approve these insights? (y/n): ")

    if approval.lower() != 'y':
        print("❌ Workflow cancelled")
        return

    # Continue with approved insights
    notes_result = self.agent_tools["note_taker"].run(...)
```

---

## Output Format

Results are saved to `workflow_results.json`:

```json
{
  "insights": [
    "Product launch scheduled for Q1 2024",
    "Engineering team is 90% complete",
    "Target market: mid-sized tech companies",
    "Beta launch planned for late January",
    "Full launch in February"
  ],
  "notes": {
    "summary": "Team met to finalize Q1 product launch strategy for AI-powered analytics dashboard...",
    "key_points": [
      "ML models trained and deployed",
      "2 weeks needed for auth and UI polish",
      "Soft launch with beta customers in January"
    ],
    "decisions": [
      "Target mid-sized tech companies",
      "Soft launch late January, full launch February"
    ],
    "next_steps": [
      "Complete authentication system",
      "Set up GitHub repository",
      "Create landing page and demo video"
    ]
  },
  "todos": [
    {
      "task": "Complete auth system and UI polish",
      "priority": "High",
      "assignee": "John"
    },
    {
      "task": "Set up GitHub repository with documentation",
      "priority": "High",
      "assignee": "John"
    },
    {
      "task": "Finalize beta customer list",
      "priority": "Medium",
      "assignee": "Maya"
    }
  ],
  "github": {
    "name": "ai-analytics-dashboard",
    "description": "AI-powered analytics dashboard for mid-sized tech companies",
    "readme_outline": [
      "Overview",
      "Features",
      "Installation",
      "API Documentation",
      "Contributing"
    ],
    "initial_files": [
      "README.md",
      "api_docs.md",
      "CONTRIBUTING.md",
      "setup.py"
    ]
  },
  "article": {
    "title": "Building Scalable ML Analytics: Our Journey to Production",
    "subtitle": "Lessons learned deploying AI-powered dashboards for enterprise clients",
    "sections": [
      {
        "heading": "The Challenge",
        "points": [
          "Need for real-time analytics",
          "Scaling ML models"
        ]
      },
      {
        "heading": "Our Architecture",
        "points": [
          "ML model design",
          "API structure"
        ]
      }
    ],
    "conclusion": "Our journey taught us the importance of...",
    "cta": "Follow us for more insights on building production ML systems"
  }
}
```

---

## Comparison: Single Agent vs Multi-Agent

### Single Agent (simple_agent.py)

```python
# One agent does everything
agent = SimpleAgent()
result = agent.run("Extract insights AND create notes AND create todos")

# Pros: Simple, fewer moving parts
# Cons: Limited by single context, can't specialize
```

### Multi-Agent (multi_agent_system.py)

```python
# Multiple specialized agents, coordinated by manager
manager = ManagerAgent()
results = manager.run_workflow(transcript)

# Pros: Specialization, modularity, parallel execution
# Cons: More complexity, coordination overhead
```

---

## When to Use Multi-Agent vs Single Agent

**Use Single Agent when:**
- Task is simple and straightforward
- No need for specialization
- Quick prototyping
- Limited context/steps

**Use Multi-Agent when:**
- Complex workflows with multiple distinct steps
- Different expertise needed for different tasks
- Want to run tasks in parallel
- Need modularity and easy extension

---

## Troubleshooting

### "Agent gets stuck in loop"

Reduce `max_iterations` or improve prompts:

```python
# In specialized agent
def _plan(self, context):
    prompt = f"""
    IMPORTANT: Respond with action "COMPLETE" once you have the result.
    Do not use "USE_TOOL" unless absolutely necessary.

    {context['goal']}
    """
```

### "JSON parsing errors"

Add better error handling:

```python
def _parse_json(self, text: str) -> Dict[str, Any]:
    try:
        # Try standard parsing
        return json.loads(text.strip())
    except json.JSONDecodeError:
        # Fallback: extract JSON object
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end > start:
            return json.loads(text[start:end])

        # Last resort: return error structure
        return {"action": "COMPLETE", "answer": "Error parsing response", "error": True}
```

### "Agents produce inconsistent results"

Lower temperature for more deterministic outputs:

```python
response = self.llm.chat.completions.create(
    model=self.model,
    messages=[...],
    temperature=0.1  # ← Lower = more consistent
)
```

---

## Next Steps

1. **Add Real Tool Integration**
   - Connect to actual GitHub API
   - Integrate with Medium API for publishing
   - Add file system operations

2. **Implement Parallel Execution**
   - Use `concurrent.futures`
   - Speed up workflow with parallel agents

3. **Add Agent Communication**
   - Let agents message each other
   - Implement feedback loops

4. **Build a Web Interface**
   - Flask/FastAPI backend
   - React frontend
   - Real-time progress updates

---

## Resources

- [Simple Agent (SPOAR)](./simple_agent.py) - The foundation
- [Groq Cloud Docs](https://console.groq.com/docs)
- [Multi-Agent Systems](https://en.wikipedia.org/wiki/Multi-agent_system)

---

Happy building with multi-agent systems! 🚀
