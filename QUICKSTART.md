# Quick Start Guide

Get up and running with the multi-agent system in 5 minutes.

---

## Prerequisites

- Python 3.8 or higher
- A Groq Cloud API key ([Get one here](https://console.groq.com/keys))

---

## Installation

### Step 1: Clone or Download

```bash
# If you have the repository
cd agent-c5

# Or download the files directly
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `groq` - LLM provider
- `python-dotenv` - Environment variable management

### Step 3: Set Up API Key

```bash
# Create .env file
echo "GROQ_API_KEY=your-actual-api-key-here" > .env

# Replace 'your-actual-api-key-here' with your real API key
```

---

## Usage

### Option 1: Run Multi-Agent System (Recommended)

```bash
python multi_agent_system.py
```

This reads the meeting transcript from `sample_transcript.txt` and produces:
- Key insights
- Meeting notes
- Action items (todos)
- GitHub repository plan
- Medium article outline

**Input:** `sample_transcript.txt` (provided)
**Output:** `workflow_results.json`

**To use your own transcript:**
1. Edit `sample_transcript.txt` with your meeting content
2. Run `python multi_agent_system.py`
3. Check `workflow_results.json` for results

### Option 2: Run with Example Workflows

```bash
python example_workflow.py
```

Choose between:
1. Product Strategy Meeting
2. Technical Discussion

**Output:** `product_meeting_results.json` or `tech_meeting_results.json`

### Option 3: Run Simple Agent (Original)

```bash
python simple_agent.py
```

Runs the basic SPOAR agent with a simple calculation task.

---

## Customizing the Workflow

### Use Your Own Transcript

Edit `multi_agent_system.py` or `example_workflow.py`:

```python
# Your meeting transcript
my_transcript = """
Your actual meeting transcript here...
"""

# Run workflow
manager = ManagerAgent()
results = manager.run_workflow(my_transcript)
manager.save_results("my_results.json")
```

### Modify Agent Behavior

Edit the prompt in any agent's `_plan()` method:

```python
# In multi_agent_system.py, find the agent class:
class InsightExtractorAgent(BaseAgent):
    def _plan(self, context):
        prompt = f"""
        Modified instructions here...
        """
```

---

## Understanding the Output

### workflow_results.json Structure

```json
{
  "insights": [
    "Insight 1",
    "Insight 2"
  ],
  "notes": {
    "summary": "Meeting summary...",
    "key_points": ["Point 1", "Point 2"],
    "decisions": ["Decision 1"],
    "next_steps": ["Step 1"]
  },
  "todos": [
    {
      "task": "Complete feature X",
      "priority": "High",
      "assignee": "John"
    }
  ],
  "github": {
    "name": "repository-name",
    "description": "Repository description",
    "readme_outline": ["Section 1", "Section 2"],
    "initial_files": ["file1.py", "file2.md"]
  },
  "article": {
    "title": "Article Title",
    "subtitle": "Subtitle",
    "sections": [
      {
        "heading": "Section 1",
        "points": ["Point 1", "Point 2"]
      }
    ],
    "conclusion": "Conclusion text",
    "cta": "Call to action"
  }
}
```

---

## Troubleshooting

### "GROQ_API_KEY not found"

Make sure your `.env` file exists and contains:

```
GROQ_API_KEY=gsk_your_actual_key_here
```

Check the file:

```bash
cat .env
```

### "Module not found" errors

Install dependencies:

```bash
pip install -r requirements.txt
```

### "Rate limit exceeded"

You're making too many requests. Wait a few seconds and try again.

Groq Cloud has generous rate limits, but if you're testing repeatedly, add a delay:

```python
import time
time.sleep(2)  # Wait 2 seconds between runs
```

### JSON parsing errors

The LLM sometimes outputs invalid JSON. If this happens:

1. Check the logs to see what the LLM returned
2. Lower the temperature in the agent's `_plan()` method:

```python
response = self.llm.chat.completions.create(
    model=self.model,
    messages=[...],
    temperature=0.1  # Lower = more consistent
)
```

### Agent gets stuck in loop

Reduce `max_iterations` when running agents:

```python
result = agent.run(
    goal="Extract insights",
    context=workflow_context,
    max_iterations=2  # Reduced from 3
)
```

---

## Next Steps

1. **Read the Tutorial** - [TUTORIAL.md](./TUTORIAL.md) - Step-by-step guide
2. **Understand Architecture** - [ARCHITECTURE.md](./ARCHITECTURE.md) - System design
3. **Full Documentation** - [MULTI_AGENT_README.md](./MULTI_AGENT_README.md) - Complete reference

---

## Example Session

```bash
$ python multi_agent_system.py

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
📰 Article Title: Building Scalable ML Analytics

💡 Check 'workflow_results.json' for detailed output!
============================================================

💾 Results saved to workflow_results.json
```

---

## Tips for Best Results

### 1. Provide Detailed Transcripts

The more context in your transcript, the better the results:

**Good:**
```
Meeting: Product Launch Planning
Date: Dec 6, 2024
Attendees: Alice (PM), Bob (Eng), Carol (Marketing)

Alice: We need to launch by Q1. Bob, what's the engineering timeline?
Bob: We can deliver in 6 weeks if we focus on core features.
Carol: I need 2 weeks for marketing materials after engineering wraps.
...
```

**Less Good:**
```
We talked about launching the product.
```

### 2. Use Realistic Meeting Content

The agents work best with actual meeting discussions that include:
- Participants and roles
- Decisions made
- Action items mentioned
- Timelines discussed
- Problems and solutions

### 3. Adjust Agent Prompts for Your Domain

If you're in a specific industry (healthcare, finance, etc.), update the agent prompts to use domain-specific language.

### 4. Review and Refine Outputs

The agents provide a great starting point, but always review:
- Are the insights accurate?
- Are the todos actionable?
- Does the article outline make sense?

---

## Getting Help

- Check [TUTORIAL.md](./TUTORIAL.md) for detailed explanations
- Review [MULTI_AGENT_README.md](./MULTI_AGENT_README.md) for customization
- See [ARCHITECTURE.md](./ARCHITECTURE.md) to understand the system

---

Happy building! 🚀
