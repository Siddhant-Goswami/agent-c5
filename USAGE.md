# Usage Guide

Complete guide to using the multi-agent system with your own meeting transcripts.

---

## Quick Usage

### 1. Using the Provided Sample

The easiest way to get started:

```bash
python multi_agent_system.py
```

This will:
- Read `sample_transcript.txt` (provided)
- Process it through all 5 agents
- Generate `workflow_results.json`

### 2. Using Your Own Transcript

**Method 1: Edit the sample file**

```bash
# Open the file in your editor
nano sample_transcript.txt

# Or use any text editor
# Replace the content with your meeting transcript
# Save and run
python multi_agent_system.py
```

**Method 2: Programmatically**

```python
from multi_agent_system import ManagerAgent

# Your transcript
my_transcript = """
Your meeting content here...
"""

# Run workflow
manager = ManagerAgent()
results = manager.run_workflow(my_transcript)
manager.save_results("my_results.json")
```

---

## Input Format

### Recommended Transcript Format

For best results, structure your transcript like this:

```
Meeting: [Meeting Title]
Date: [Date]
Attendees: [Name (Role), Name (Role), ...]

[Name]: [What they said...]

[Name]: [Response...]

[Name]: [More discussion...]

Action Items:
- [Item 1]
- [Item 2]
```

### Example

```
Meeting: Product Review
Date: December 6, 2024
Attendees: Alice (CEO), Bob (CTO), Carol (Designer)

Alice: Let's review the new dashboard design.

Carol: I've updated the UI based on last week's feedback.
The new color scheme is more accessible.

Bob: The backend API is ready. We can integrate it this week.

Alice: Perfect! Let's target launch for next Friday.

Action Items:
- Carol: Finalize UI by Wednesday
- Bob: Complete API integration by Thursday
- Alice: Prepare launch announcement
```

---

## Output Files

### workflow_results.json

The main output file contains:

```json
{
  "insights": [
    "Key insight 1",
    "Key insight 2",
    ...
  ],
  "notes": {
    "summary": "Brief meeting summary...",
    "key_points": ["Point 1", "Point 2", ...],
    "decisions": ["Decision 1", ...],
    "next_steps": ["Step 1", ...]
  },
  "todos": [
    {
      "task": "Task description",
      "priority": "High/Medium/Low",
      "assignee": "Person name"
    },
    ...
  ],
  "github": {
    "name": "repository-name",
    "description": "Repo description",
    "readme_outline": ["Section 1", "Section 2", ...],
    "initial_files": ["file1.py", "file2.md", ...]
  },
  "article": {
    "title": "Article title",
    "subtitle": "Subtitle",
    "sections": [
      {
        "heading": "Section heading",
        "points": ["Point 1", "Point 2", ...]
      },
      ...
    ],
    "conclusion": "Conclusion text...",
    "cta": "Call to action..."
  }
}
```

---

## Advanced Usage

### Process Multiple Transcripts

Create a script to process multiple files:

```python
#!/usr/bin/env python3
import os
import glob
from multi_agent_system import ManagerAgent

# Initialize manager once
manager = ManagerAgent()

# Process all .txt files in a directory
for transcript_file in glob.glob("transcripts/*.txt"):
    print(f"\nProcessing {transcript_file}...")

    with open(transcript_file, "r") as f:
        transcript = f.read()

    # Run workflow
    results = manager.run_workflow(transcript)

    # Save with unique name
    output_file = transcript_file.replace(".txt", "_results.json")
    manager.save_results(output_file)

    print(f"✅ Saved to {output_file}")
```

### Custom Output Location

```python
from multi_agent_system import ManagerAgent

manager = ManagerAgent()

with open("sample_transcript.txt", "r") as f:
    transcript = f.read()

results = manager.run_workflow(transcript)

# Save to custom location
manager.save_results("outputs/meeting_2024_12_06.json")
```

### Extract Specific Results

```python
from multi_agent_system import ManagerAgent

manager = ManagerAgent()

with open("sample_transcript.txt", "r") as f:
    transcript = f.read()

results = manager.run_workflow(transcript)

# Get only insights
insights = results.get("insights", [])
print("Insights:", insights)

# Get only todos
todos = results.get("todos", [])
for todo in todos:
    print(f"- [{todo['priority']}] {todo['task']} ({todo['assignee']})")

# Get GitHub repo name
repo_name = results.get("github", {}).get("name", "N/A")
print(f"Repo: {repo_name}")
```

---

## Tips for Best Results

### 1. Provide Context

Include meeting metadata at the start:
- Meeting title/purpose
- Date
- Attendees with roles
- Any relevant background

### 2. Clear Speaker Attribution

Use consistent formatting:
```
Alice: I think we should...
Bob: I agree, and we could also...
```

Not:
```
Someone said something about...
We discussed...
```

### 3. Include Action Items

Explicitly mention action items in the discussion:
```
Sarah: Let's summarize action items:
- John: Complete feature by Friday
- Maya: Review documentation
```

### 4. Reasonable Length

**Optimal:** 200-2000 words
- Too short: May not generate meaningful insights
- Too long: May exceed context limits

If your transcript is very long, consider:
- Splitting into multiple meetings
- Summarizing less important sections
- Focusing on key discussion points

### 5. Structure Discussions

Group related topics:
```
Topic 1: Product Launch
Alice: ...
Bob: ...

Topic 2: Marketing Strategy
Carol: ...
David: ...
```

---

## Common Use Cases

### 1. Team Standup

```
Meeting: Daily Standup
Date: December 6, 2024
Team: Engineering

Alice: Yesterday I finished the login feature. Today I'll start on password reset.
Bob: I'm still working on the API. Should be done today.
Carol: I need help with the database schema. Can someone review?

Blockers:
- Carol needs DB schema review
```

**Output:** Quick insights, clear todos with owners

### 2. Strategy Session

```
Meeting: Q1 Planning
Date: December 6, 2024
Leadership Team

Discussion of Q1 priorities, resource allocation, and key initiatives...
[Full discussion]

Decisions:
- Focus on feature X
- Hire 2 engineers
- Launch by March
```

**Output:** Strategic insights, high-level todos, article outline

### 3. Technical Review

```
Meeting: Architecture Review
Date: December 6, 2024
Engineering Team

Review of new microservices architecture...
[Technical discussion]

Decisions:
- Use Kubernetes
- Implement API gateway
- Migration plan over 6 weeks
```

**Output:** Technical insights, implementation todos, detailed GitHub plan

### 4. Client Meeting

```
Meeting: Client Onboarding
Date: December 6, 2024
Client: Acme Corp

Discussion of requirements, timeline, deliverables...
[Full discussion]

Next steps:
- Send proposal by Friday
- Schedule demo next week
- Prepare contract
```

**Output:** Client insights, follow-up todos, project plan

---

## Troubleshooting

### Issue: No insights extracted

**Cause:** Transcript too short or lacks substance

**Solution:**
- Add more context
- Include actual discussion points
- Mention specific decisions or action items

### Issue: Todos are generic

**Cause:** Action items not explicitly mentioned

**Solution:**
- Include a clear "Action Items" or "Next Steps" section
- Mention specific assignees
- Include deadlines when possible

### Issue: GitHub plan is off-topic

**Cause:** Meeting doesn't discuss technical projects

**Solution:**
- This is normal for non-technical meetings
- The agent does its best to infer a relevant repo
- You can ignore this section if not applicable

### Issue: Article outline doesn't match meeting

**Cause:** Agent interprets content creatively

**Solution:**
- This is expected - the agent creates content about the topics
- Review and adjust the outline as needed
- The goal is to provide a starting point

---

## Integration Examples

### Save to Notion

```python
import requests
from multi_agent_system import ManagerAgent

manager = ManagerAgent()
results = manager.run_workflow(transcript)

# Post to Notion API
notion_api_url = "https://api.notion.com/v1/pages"
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

data = {
    "parent": {"database_id": DATABASE_ID},
    "properties": {
        "Name": {"title": [{"text": {"content": "Meeting Notes"}}]},
        "Summary": {"rich_text": [{"text": {"content": results["notes"]["summary"]}}]}
    }
}

response = requests.post(notion_api_url, headers=headers, json=data)
```

### Email Summary

```python
import smtplib
from email.mime.text import MIMEText
from multi_agent_system import ManagerAgent

manager = ManagerAgent()
results = manager.run_workflow(transcript)

# Create email
body = f"""
Meeting Summary:
{results['notes']['summary']}

Key Points:
{chr(10).join(f"- {p}" for p in results['notes']['key_points'])}

Action Items:
{chr(10).join(f"- [{t['priority']}] {t['task']} ({t['assignee']})" for t in results['todos'])}
"""

msg = MIMEText(body)
msg['Subject'] = 'Meeting Summary'
msg['From'] = 'bot@company.com'
msg['To'] = 'team@company.com'

# Send email
smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.starttls()
smtp.login(username, password)
smtp.send_message(msg)
smtp.quit()
```

### Export to Markdown

```python
from multi_agent_system import ManagerAgent

manager = ManagerAgent()
results = manager.run_workflow(transcript)

# Generate markdown
markdown = f"""# Meeting Notes

## Summary
{results['notes']['summary']}

## Key Points
{chr(10).join(f"- {p}" for p in results['notes']['key_points'])}

## Decisions
{chr(10).join(f"- {d}" for d in results['notes']['decisions'])}

## Action Items
{chr(10).join(f"- [{t['priority']}] {t['task']} - *{t['assignee']}*" for t in results['todos'])}

## GitHub Repository
**Name:** {results['github']['name']}

**Description:** {results['github']['description']}

## Article Outline
**Title:** {results['article']['title']}

**Subtitle:** {results['article']['subtitle']}
"""

with open("meeting_notes.md", "w") as f:
    f.write(markdown)
```

---

## Best Practices

1. **Consistent Format:** Use the same transcript format for all meetings
2. **Clear Attribution:** Always attribute statements to specific people
3. **Action Items:** Explicitly list action items with owners
4. **Regular Processing:** Process transcripts shortly after meetings while they're fresh
5. **Review Output:** Always review AI-generated content before sharing
6. **Archive Results:** Keep all `workflow_results.json` files for reference
7. **Iterate:** Adjust your transcript format based on output quality

---

## Next Steps

Once you're comfortable with basic usage:

1. **Customize Agents** - Modify prompts for your specific needs
2. **Add New Agents** - Create specialized agents for your workflow
3. **Automate** - Set up automated processing of recorded meetings
4. **Integrate** - Connect to your existing tools (Slack, Notion, etc.)

See [MULTI_AGENT_README.md](./MULTI_AGENT_README.md) for customization details.

---

Happy meeting processing! 🚀
