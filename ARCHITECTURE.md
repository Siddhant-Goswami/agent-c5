# Multi-Agent System Architecture

This document explains the architecture of the multi-agent system.

---

## System Overview

```
┌───────────────────────────────────────────────────────────────────┐
│                         USER INPUT                                 │
│                    (Meeting Transcript)                            │
└────────────────────────────┬──────────────────────────────────────┘
                             │
                             ▼
┌───────────────────────────────────────────────────────────────────┐
│                       MANAGER AGENT                                │
│                    (Orchestrator)                                  │
│                                                                    │
│  Responsibilities:                                                 │
│  - Coordinate workflow                                             │
│  - Pass context between agents                                     │
│  - Aggregate results                                               │
│  - Handle errors                                                   │
└───────┬─────────┬──────────┬─────────┬─────────┬──────────────────┘
        │         │          │         │         │
        │         │          │         │         │
        ▼         ▼          ▼         ▼         ▼
    ┌────────┐ ┌──────┐  ┌──────┐  ┌──────┐  ┌────────┐
    │Insight │ │ Note │  │ Todo │  │GitHub│  │Article │
    │Extract │ │Taker │  │Create│  │Manage│  │Writer  │
    │  or    │ │      │  │  or  │  │  r   │  │        │
    └────────┘ └──────┘  └──────┘  └──────┘  └────────┘
        │         │          │         │         │
        ▼         ▼          ▼         ▼         ▼
    ┌────────────────────────────────────────────────┐
    │            WORKFLOW RESULTS                     │
    │                                                 │
    │  - insights: [...]                              │
    │  - notes: {...}                                 │
    │  - todos: [...]                                 │
    │  - github: {...}                                │
    │  - article: {...}                               │
    └────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Base Agent Class

The foundation for all agents.

```
┌─────────────────────────────────────────────────┐
│              BaseAgent                          │
├─────────────────────────────────────────────────┤
│ Attributes:                                     │
│  - name: str                                    │
│  - role: str                                    │
│  - llm: Groq                                    │
│  - model: str                                   │
│  - memory: List                                 │
├─────────────────────────────────────────────────┤
│ Methods:                                        │
│  + run(goal, context, max_iterations)           │
│  + _sense(context) → context                    │
│  + _plan(context) → plan                        │
│  + _act(plan) → result                          │
│  + _observe(plan, result) → observation         │
│  + _reflect(context, observation) → reflection  │
│  + _log_phase(phase, data)                      │
│  + _parse_json(text) → dict                     │
└─────────────────────────────────────────────────┘
```

**Key Responsibilities:**
- Implement SPOAR loop
- Handle LLM communication
- Parse JSON responses
- Log agent activities

---

### 2. Specialized Agents

Each inherits from `BaseAgent` and customizes `_plan()`.

#### InsightExtractorAgent

```
┌─────────────────────────────────────────┐
│      InsightExtractorAgent              │
├─────────────────────────────────────────┤
│ Inherits: BaseAgent                     │
│ Purpose: Extract key insights           │
├─────────────────────────────────────────┤
│ Input:                                  │
│  - transcript: str                      │
├─────────────────────────────────────────┤
│ Output:                                 │
│  {                                      │
│    "insights": [                        │
│      "Key insight 1",                   │
│      "Key insight 2",                   │
│      ...                                │
│    ]                                    │
│  }                                      │
└─────────────────────────────────────────┘
```

#### NoteTakerAgent

```
┌─────────────────────────────────────────┐
│          NoteTakerAgent                 │
├─────────────────────────────────────────┤
│ Inherits: BaseAgent                     │
│ Purpose: Create structured notes        │
├─────────────────────────────────────────┤
│ Input:                                  │
│  - transcript: str                      │
│  - insights: List[str]                  │
├─────────────────────────────────────────┤
│ Output:                                 │
│  {                                      │
│    "notes": {                           │
│      "summary": "...",                  │
│      "key_points": [...],               │
│      "decisions": [...],                │
│      "next_steps": [...]                │
│    }                                    │
│  }                                      │
└─────────────────────────────────────────┘
```

#### TodoCreatorAgent

```
┌─────────────────────────────────────────┐
│        TodoCreatorAgent                 │
├─────────────────────────────────────────┤
│ Inherits: BaseAgent                     │
│ Purpose: Generate actionable todos      │
├─────────────────────────────────────────┤
│ Input:                                  │
│  - notes: Dict                          │
├─────────────────────────────────────────┤
│ Output:                                 │
│  {                                      │
│    "todos": [                           │
│      {                                  │
│        "task": "...",                   │
│        "priority": "High/Med/Low",      │
│        "assignee": "..."                │
│      },                                 │
│      ...                                │
│    ]                                    │
│  }                                      │
└─────────────────────────────────────────┘
```

#### GitHubManagerAgent

```
┌─────────────────────────────────────────┐
│       GitHubManagerAgent                │
├─────────────────────────────────────────┤
│ Inherits: BaseAgent                     │
│ Purpose: Plan GitHub repository         │
├─────────────────────────────────────────┤
│ Input:                                  │
│  - notes: Dict                          │
├─────────────────────────────────────────┤
│ Output:                                 │
│  {                                      │
│    "repository": {                      │
│      "name": "...",                     │
│      "description": "...",              │
│      "readme_outline": [...],           │
│      "initial_files": [...]             │
│    }                                    │
│  }                                      │
└─────────────────────────────────────────┘
```

#### ArticleWriterAgent

```
┌─────────────────────────────────────────┐
│        ArticleWriterAgent               │
├─────────────────────────────────────────┤
│ Inherits: BaseAgent                     │
│ Purpose: Write Medium article outline   │
├─────────────────────────────────────────┤
│ Input:                                  │
│  - notes: Dict                          │
│  - insights: List[str]                  │
├─────────────────────────────────────────┤
│ Output:                                 │
│  {                                      │
│    "article": {                         │
│      "title": "...",                    │
│      "subtitle": "...",                 │
│      "sections": [...],                 │
│      "conclusion": "...",               │
│      "cta": "..."                       │
│    }                                    │
│  }                                      │
└─────────────────────────────────────────┘
```

---

### 3. Manager Agent

Orchestrates the entire workflow.

```
┌─────────────────────────────────────────────────┐
│              ManagerAgent                       │
├─────────────────────────────────────────────────┤
│ Inherits: BaseAgent                             │
│                                                 │
│ agent_tools: {                                  │
│   "insight_extractor": InsightExtractorAgent(), │
│   "note_taker": NoteTakerAgent(),               │
│   "todo_creator": TodoCreatorAgent(),           │
│   "github_manager": GitHubManagerAgent(),       │
│   "article_writer": ArticleWriterAgent()        │
│ }                                               │
│                                                 │
│ workflow_results: {}                            │
├─────────────────────────────────────────────────┤
│ Methods:                                        │
│  + run_workflow(transcript) → results           │
│  + save_results(output_file)                    │
└─────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

### Sequential Workflow

```
INPUT: Meeting Transcript
│
▼
┌──────────────────────────────┐
│ STEP 1: Extract Insights     │
│ Agent: InsightExtractorAgent │
└──────────┬───────────────────┘
           │ insights: List[str]
           ▼
┌──────────────────────────────┐
│ STEP 2: Create Notes         │
│ Agent: NoteTakerAgent        │
│ Input: transcript + insights │
└──────────┬───────────────────┘
           │ notes: Dict
           ▼
┌──────────────────────────────┐
│ STEP 3: Create Todos         │
│ Agent: TodoCreatorAgent      │
│ Input: notes                 │
└──────────┬───────────────────┘
           │ todos: List[Dict]
           ▼
┌──────────────────────────────┐
│ STEP 4: Plan GitHub Repo     │
│ Agent: GitHubManagerAgent    │
│ Input: notes                 │
└──────────┬───────────────────┘
           │ github: Dict
           ▼
┌──────────────────────────────┐
│ STEP 5: Write Article        │
│ Agent: ArticleWriterAgent    │
│ Input: notes + insights      │
└──────────┬───────────────────┘
           │ article: Dict
           ▼
OUTPUT: workflow_results.json
```

---

## SPOAR Loop (Per Agent)

Each agent follows this pattern:

```
┌──────────────────────────────────────────────┐
│                 AGENT ITERATION              │
├──────────────────────────────────────────────┤
│                                              │
│  1. SENSE                                    │
│     ├─ Gather context                        │
│     ├─ Check goal                            │
│     └─ Review previous actions               │
│         │                                    │
│         ▼                                    │
│  2. PLAN                                     │
│     ├─ Build prompt                          │
│     ├─ Call LLM (GPT OSS 120B)               │
│     └─ Parse JSON response                   │
│         │                                    │
│         ▼                                    │
│  3. ACT                                      │
│     └─ Execute planned action                │
│         │                                    │
│         ▼                                    │
│  4. OBSERVE                                  │
│     ├─ Record action taken                   │
│     ├─ Record result                         │
│     └─ Check success/failure                 │
│         │                                    │
│         ▼                                    │
│  5. REFLECT                                  │
│     ├─ Evaluate progress                     │
│     └─ Decide next steps                     │
│         │                                    │
│         ▼                                    │
│  ┌──────────────────┐                       │
│  │ Complete?        │                       │
│  └────┬────────┬────┘                       │
│       │ No     │ Yes                        │
│       │        └─► Return Result            │
│       └─► Next Iteration                    │
└──────────────────────────────────────────────┘
```

---

## Context Object Structure

The context flows through the workflow:

### Initial Context

```python
{
  "transcript": "Full meeting transcript text..."
}
```

### After InsightExtractor

```python
{
  "transcript": "Full meeting transcript text...",
  "insights": [
    "Insight 1",
    "Insight 2",
    ...
  ]
}
```

### After NoteTaker

```python
{
  "transcript": "...",
  "insights": [...],
  "notes": {
    "summary": "Meeting summary...",
    "key_points": ["Point 1", "Point 2", ...],
    "decisions": ["Decision 1", ...],
    "next_steps": ["Step 1", ...]
  }
}
```

### Final Context (After All Agents)

```python
{
  "transcript": "...",
  "insights": [...],
  "notes": {...},
  "todos": [...],
  "github": {...},
  "article": {...}
}
```

---

## Error Handling Flow

```
Agent Execution
│
├─ Success
│  └─► Continue to next agent
│
└─ Failure
   ├─► Log error
   ├─► Return partial results
   └─► Continue workflow (graceful degradation)
```

---

## Extension Points

### 1. Add New Agent

```python
# Step 1: Create agent class
class NewAgent(BaseAgent):
    def __init__(self):
        super().__init__("NewAgent", "New agent purpose")

    def _plan(self, context):
        # Custom planning logic
        pass

# Step 2: Register with manager
class ManagerAgent(BaseAgent):
    def __init__(self):
        # ...
        self.agent_tools["new_agent"] = NewAgent()

# Step 3: Add to workflow
def run_workflow(self, transcript):
    # ...
    new_result = self.agent_tools["new_agent"].run(...)
```

### 2. Modify Workflow Order

Simply reorder the steps in `run_workflow()`:

```python
def run_workflow(self, transcript):
    # Changed order
    sentiment = self.agent_tools["sentiment_analyzer"].run(...)
    insights = self.agent_tools["insight_extractor"].run(...)
    notes = self.agent_tools["note_taker"].run(...)
    # ...
```

### 3. Add Parallel Execution

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=3) as executor:
    future1 = executor.submit(agent1.run, ...)
    future2 = executor.submit(agent2.run, ...)
    result1 = future1.result()
    result2 = future2.result()
```

### 4. Add Conditional Logic

```python
if "technical" in transcript.lower():
    article = self.agent_tools["technical_writer"].run(...)
else:
    article = self.agent_tools["general_writer"].run(...)
```

---

## Performance Considerations

### Sequential Execution

- Current implementation: ~15-30 seconds for full workflow
- 5 agents × (2-5 seconds per agent)
- Sequential = sum of all agent times

### Parallel Execution (Potential)

- Independent agents can run in parallel
- Could reduce to ~10-15 seconds
- Requires ThreadPoolExecutor or async/await

### Optimization Strategies

1. **Reduce max_iterations** - Fewer SPOAR loops per agent
2. **Optimize prompts** - Clearer instructions = faster completion
3. **Parallel independent agents** - Run TodoCreator and GitHubManager simultaneously
4. **Cache results** - Reuse insights across multiple workflows
5. **Stream outputs** - Show results as they complete

---

## Security Considerations

1. **API Key Management**
   - Stored in `.env` file
   - Never committed to git
   - Loaded via python-dotenv

2. **Input Validation**
   - Validate transcript length
   - Sanitize user inputs
   - Check for malicious content

3. **Output Sanitization**
   - Parse JSON safely
   - Handle LLM hallucinations
   - Validate agent outputs

4. **Error Handling**
   - Never expose API keys in errors
   - Log errors securely
   - Fail gracefully

---

## Testing Architecture

```
┌────────────────────────────────────────┐
│          Testing Pyramid               │
├────────────────────────────────────────┤
│                                        │
│         E2E Tests                      │
│       (Full Workflow)                  │
│      /              \                  │
│     /                \                 │
│    /  Integration     \                │
│   /   Tests (Multi-   \                │
│  /    Agent Workflow)  \               │
│ /                       \              │
│/  Unit Tests (Individual \             │
│   Agents, Functions)      \            │
└────────────────────────────────────────┘
```

### Test Levels

1. **Unit Tests** - Test individual agents
2. **Integration Tests** - Test agent interactions
3. **E2E Tests** - Test complete workflow

---

## Deployment Architecture (Future)

```
┌─────────────────────────────────────────┐
│           Web Interface                 │
│         (React Frontend)                │
└──────────────┬──────────────────────────┘
               │ HTTP/REST
               ▼
┌─────────────────────────────────────────┐
│        API Server                       │
│      (Flask/FastAPI)                    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Multi-Agent System                 │
│       (ManagerAgent)                    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│         LLM Provider                    │
│        (Groq Cloud)                     │
└─────────────────────────────────────────┘
```

---

This architecture enables:
- **Modularity** - Easy to add/remove agents
- **Scalability** - Can run agents in parallel
- **Maintainability** - Clear separation of concerns
- **Extensibility** - Simple to customize and extend
