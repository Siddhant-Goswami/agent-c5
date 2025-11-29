#!/usr/bin/env python3
"""
=============================================================================
SIMPLE AI AGENT BOILERPLATE
=============================================================================

A minimal, educational implementation of an autonomous AI agent.
This single file demonstrates all core concepts needed to build AI agents:

1. LLM Integration - Using OpenAI for reasoning
2. Tools - Functions the agent can call to interact with the world
3. Memory - Storing context and conversation history
4. Agent Loop - SENSE → PLAN → ACT → OBSERVE → REFLECT cycle
5. Logging - Observability into agent execution

Author: AI Learning Coach Team
Purpose: Teaching students how to build AI agents from scratch

Usage:
    python simple_agent.py

Requirements:
    pip install openai python-dotenv
"""

# =============================================================================
# SECTION 1: IMPORTS AND CONFIGURATION
# =============================================================================

import os
import json
import time
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Callable
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()


@dataclass
class AgentConfig:
    """
    Configuration for the agent.
    
    Attributes:
        model: The LLM model to use (default: gpt-4o-mini for cost efficiency)
        max_iterations: Maximum reasoning loops before stopping
        temperature: LLM creativity (0=deterministic, 1=creative)
        verbose: Whether to print detailed logs
    """
    model: str = "gpt-4o-mini"
    max_iterations: int = 5
    temperature: float = 0.3
    verbose: bool = True


# =============================================================================
# SECTION 2: MEMORY AND CONTEXT STORE
# =============================================================================

class MemoryStore:
    """
    Simple in-memory storage for agent context and conversation history.
    
    In production, you would replace this with a database or vector store.
    This class demonstrates the concept of agent memory:
    - Short-term: Current conversation context
    - Long-term: Stored facts and user preferences
    """
    
    def __init__(self):
        # Short-term memory: Current session context
        self.context: Dict[str, Any] = {}
        
        # Long-term memory: Persistent facts (simulated)
        self.facts: List[Dict[str, Any]] = []
        
        # Conversation history for this session
        self.conversation_history: List[Dict[str, str]] = []
        
        # User preferences
        self.user_preferences: Dict[str, Any] = {
            "name": "Student",
            "learning_level": "intermediate",
            "interests": ["AI", "Machine Learning", "Python"],
        }
    
    def store_fact(self, fact: str, source: str = "agent") -> Dict[str, Any]:
        """Store a new fact in long-term memory."""
        fact_entry = {
            "id": len(self.facts) + 1,
            "content": fact,
            "source": source,
            "timestamp": datetime.now().isoformat(),
        }
        self.facts.append(fact_entry)
        return fact_entry
    
    def search_facts(self, query: str) -> List[Dict[str, Any]]:
        """
        Simple keyword search through stored facts.
        
        In production, you would use vector similarity search here.
        This is a simplified version for teaching purposes.
        """
        query_lower = query.lower()
        results = []
        for fact in self.facts:
            if query_lower in fact["content"].lower():
                results.append(fact)
        return results
    
    def add_to_conversation(self, role: str, content: str):
        """Add a message to conversation history."""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
        })
    
    def get_recent_context(self, n: int = 5) -> str:
        """Get the last n conversation turns as context."""
        recent = self.conversation_history[-n:] if self.conversation_history else []
        return "\n".join([f"{m['role']}: {m['content']}" for m in recent])
    
    def update_context(self, key: str, value: Any):
        """Update the current session context."""
        self.context[key] = value
    
    def get_context(self) -> Dict[str, Any]:
        """Get the full current context."""
        return {
            "session_context": self.context,
            "user_preferences": self.user_preferences,
            "facts_count": len(self.facts),
        }


# =============================================================================
# SECTION 3: KNOWLEDGE BASE (Mock Retrieval)
# =============================================================================

def load_knowledge_base() -> List[Dict[str, Any]]:
    """
    Load the knowledge base for retrieval.
    
    In production, this would be a vector database with embeddings.
    For teaching, we use a simple JSON file with pre-defined content.
    """
    kb_path = os.path.join(os.path.dirname(__file__), "sample_knowledge_base.json")
    
    if os.path.exists(kb_path):
        with open(kb_path, "r") as f:
            return json.load(f)
    
    # Fallback: Return built-in sample data
    return [
        {
            "id": 1,
            "title": "What is an AI Agent?",
            "content": "An AI agent is a system that can perceive its environment, make decisions, and take actions to achieve goals. Unlike simple chatbots, agents can use tools, maintain memory, and reason through multi-step problems.",
            "tags": ["agents", "basics", "AI"],
        },
        {
            "id": 2,
            "title": "The Agent Loop",
            "content": "The core of an AI agent is the reasoning loop: SENSE (gather information), PLAN (decide what to do), ACT (execute actions), OBSERVE (see results), REFLECT (evaluate progress). This cycle repeats until the goal is achieved.",
            "tags": ["agents", "loop", "reasoning"],
        },
        {
            "id": 3,
            "title": "Tools in AI Agents",
            "content": "Tools are functions that agents can call to interact with the world. Examples include: search engines, calculators, APIs, databases. The LLM decides which tool to use based on the task.",
            "tags": ["tools", "agents", "functions"],
        },
        {
            "id": 4,
            "title": "RAG - Retrieval Augmented Generation",
            "content": "RAG combines retrieval systems with LLMs. First, relevant documents are retrieved from a knowledge base. Then, these documents are provided as context to the LLM for generating accurate responses.",
            "tags": ["RAG", "retrieval", "generation"],
        },
        {
            "id": 5,
            "title": "Agent Memory Systems",
            "content": "Agents use memory to maintain context across interactions. Short-term memory holds current conversation state. Long-term memory stores facts, preferences, and learned information that persists across sessions.",
            "tags": ["memory", "agents", "context"],
        },
    ]


def search_knowledge(query: str, knowledge_base: List[Dict[str, Any]], top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Simple keyword-based search through the knowledge base.
    
    In production, you would use:
    - Vector embeddings (OpenAI, Sentence Transformers)
    - Similarity search (cosine similarity, dot product)
    - Vector databases (Pinecone, Weaviate, Supabase pgvector)
    
    This simplified version demonstrates the concept of retrieval.
    """
    query_words = set(query.lower().split())
    scored_results = []
    
    for item in knowledge_base:
        # Calculate simple relevance score based on word overlap
        content_words = set(item["content"].lower().split())
        title_words = set(item["title"].lower().split())
        tag_words = set(tag.lower() for tag in item.get("tags", []))
        
        # Score: matches in title (weight 3) + content (weight 1) + tags (weight 2)
        title_matches = len(query_words & title_words) * 3
        content_matches = len(query_words & content_words)
        tag_matches = len(query_words & tag_words) * 2
        
        score = title_matches + content_matches + tag_matches
        
        if score > 0:
            scored_results.append({**item, "relevance_score": score})
    
    # Sort by score and return top_k results
    scored_results.sort(key=lambda x: x["relevance_score"], reverse=True)
    return scored_results[:top_k]


# =============================================================================
# SECTION 4: TOOLS DEFINITION
# =============================================================================

# Global knowledge base (loaded once)
KNOWLEDGE_BASE = load_knowledge_base()


class ToolRegistry:
    """
    Registry of tools available to the agent.
    
    Tools are the "hands" of the agent - they allow it to take actions
    beyond just generating text. Each tool has:
    - name: Unique identifier
    - description: What the tool does (shown to LLM)
    - parameters: What inputs it accepts
    - function: The actual Python function to execute
    """
    
    def __init__(self, memory: MemoryStore):
        self.memory = memory
        self.tools: Dict[str, Dict[str, Any]] = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register the built-in tools."""
        
        # Tool 1: Search Knowledge Base
        self.register_tool(
            name="search_knowledge",
            description="Search the knowledge base for information about a topic. Use this to find relevant content before answering questions.",
            parameters={
                "query": {
                    "type": "string",
                    "description": "The search query to find relevant information",
                }
            },
            function=self._search_knowledge,
        )
        
        # Tool 2: Get User Context
        self.register_tool(
            name="get_user_context",
            description="Get information about the current user including their preferences, learning level, and interests.",
            parameters={},
            function=self._get_user_context,
        )
        
        # Tool 3: Store Memory
        self.register_tool(
            name="store_memory",
            description="Store an important fact or piece of information for future reference.",
            parameters={
                "fact": {
                    "type": "string",
                    "description": "The fact or information to remember",
                }
            },
            function=self._store_memory,
        )
        
        # Tool 4: Recall Memories
        self.register_tool(
            name="recall_memories",
            description="Search through stored memories and facts to find relevant information.",
            parameters={
                "query": {
                    "type": "string",
                    "description": "What to search for in memories",
                }
            },
            function=self._recall_memories,
        )
    
    def register_tool(
        self,
        name: str,
        description: str,
        parameters: Dict[str, Any],
        function: Callable,
    ):
        """Register a new tool."""
        self.tools[name] = {
            "name": name,
            "description": description,
            "parameters": parameters,
            "function": function,
        }
    
    def _search_knowledge(self, query: str) -> Dict[str, Any]:
        """Execute knowledge base search."""
        results = search_knowledge(query, KNOWLEDGE_BASE)
        return {
            "success": True,
            "results": results,
            "count": len(results),
        }
    
    def _get_user_context(self) -> Dict[str, Any]:
        """Get user context from memory."""
        context = self.memory.get_context()
        return {
            "success": True,
            "user": self.memory.user_preferences,
            "context": context,
        }
    
    def _store_memory(self, fact: str) -> Dict[str, Any]:
        """Store a fact in memory."""
        stored = self.memory.store_fact(fact)
        return {
            "success": True,
            "stored": stored,
            "message": f"Stored fact with id {stored['id']}",
        }
    
    def _recall_memories(self, query: str) -> Dict[str, Any]:
        """Search through stored memories."""
        results = self.memory.search_facts(query)
        return {
            "success": True,
            "memories": results,
            "count": len(results),
        }
    
    def execute(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool by name with given arguments.
        
        Returns the tool's output or an error dictionary.
        """
        if tool_name not in self.tools:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}",
                "available_tools": list(self.tools.keys()),
            }
        
        tool = self.tools[tool_name]
        try:
            # Call the tool function with provided arguments
            result = tool["function"](**args)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "tool": tool_name,
            }
    
    def get_tools_for_prompt(self) -> str:
        """Format tool descriptions for the LLM prompt."""
        lines = ["Available Tools:"]
        for name, tool in self.tools.items():
            lines.append(f"\n### {name}")
            lines.append(f"Description: {tool['description']}")
            if tool["parameters"]:
                lines.append("Parameters:")
                for param_name, param_info in tool["parameters"].items():
                    lines.append(f"  - {param_name} ({param_info['type']}): {param_info['description']}")
            else:
                lines.append("Parameters: None")
        return "\n".join(lines)


# =============================================================================
# SECTION 5: LOGGING AND OBSERVABILITY
# =============================================================================

class AgentLogger:
    """
    Simple logger for agent execution.
    
    Provides visibility into the agent's reasoning process.
    Each phase (SENSE, PLAN, ACT, OBSERVE, REFLECT) is logged
    with timestamps and relevant data.
    """
    
    # Phase indicators with emojis for visual clarity
    PHASE_ICONS = {
        "SENSE": "👁️ ",
        "PLAN": "🧠",
        "ACT": "⚡",
        "OBSERVE": "📊",
        "REFLECT": "💭",
        "COMPLETE": "✅",
        "ERROR": "❌",
    }
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.logs: List[Dict[str, Any]] = []
        self.start_time: Optional[float] = None
    
    def start_session(self, goal: str):
        """Mark the start of an agent session."""
        self.start_time = time.time()
        self.logs = []
        self._log("START", {"goal": goal})
        if self.verbose:
            print("\n" + "=" * 60)
            print(f"🚀 AGENT SESSION STARTED")
            print(f"📎 Goal: {goal}")
            print("=" * 60)
    
    def log_phase(self, phase: str, data: Dict[str, Any], iteration: int = 0):
        """Log a phase execution."""
        self._log(phase, data, iteration)
        
        if self.verbose:
            icon = self.PHASE_ICONS.get(phase, "  ")
            print(f"\n{icon} [{phase}] Iteration {iteration}")
            print("-" * 40)
            for key, value in data.items():
                if isinstance(value, dict):
                    print(f"  {key}: {json.dumps(value, indent=4)[:200]}...")
                elif isinstance(value, str) and len(value) > 100:
                    print(f"  {key}: {value[:100]}...")
                else:
                    print(f"  {key}: {value}")
    
    def _log(self, phase: str, data: Dict[str, Any], iteration: int = 0):
        """Internal logging."""
        self.logs.append({
            "timestamp": datetime.now().isoformat(),
            "phase": phase,
            "iteration": iteration,
            "data": data,
        })
    
    def complete(self, result: Dict[str, Any]):
        """Mark session as complete."""
        elapsed = time.time() - self.start_time if self.start_time else 0
        self._log("COMPLETE", {"result": result, "elapsed_seconds": elapsed})
        
        if self.verbose:
            print("\n" + "=" * 60)
            print(f"✅ AGENT SESSION COMPLETED")
            print(f"⏱️  Total time: {elapsed:.2f} seconds")
            print(f"📝 Iterations: {len([l for l in self.logs if l['phase'] in ['PLAN', 'ACT']])}")
            print("=" * 60)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the session."""
        return {
            "total_logs": len(self.logs),
            "phases": [log["phase"] for log in self.logs],
            "elapsed": time.time() - self.start_time if self.start_time else 0,
        }


# =============================================================================
# SECTION 6: THE AGENT - CORE REASONING LOOP
# =============================================================================

class SimpleAgent:
    """
    The main AI Agent class.
    
    This implements the core agent loop:
    
    1. SENSE   - Gather context about the current state
    2. PLAN    - Use LLM to decide what action to take
    3. ACT     - Execute the chosen tool/action
    4. OBSERVE - Record and analyze the result
    5. REFLECT - Evaluate progress toward the goal
    
    The loop continues until the goal is achieved or max iterations reached.
    """
    
    def __init__(self, config: AgentConfig = None):
        """Initialize the agent with configuration."""
        self.config = config or AgentConfig()
        
        # Initialize components
        self.memory = MemoryStore()
        self.tools = ToolRegistry(self.memory)
        self.logger = AgentLogger(verbose=self.config.verbose)
        
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.llm = OpenAI(api_key=api_key)
        
        # System prompt that defines the agent's behavior
        self.system_prompt = """You are an intelligent AI assistant agent. You help users by:
1. Understanding their questions thoroughly
2. Using available tools to gather information
3. Providing accurate, helpful responses

You work in a loop: SENSE → PLAN → ACT → OBSERVE → REFLECT

When planning, you MUST respond with valid JSON in this exact format:
{
    "action_type": "TOOL_CALL" | "COMPLETE",
    "tool": "tool_name_here",
    "args": {"arg1": "value1"},
    "reasoning": "Why you chose this action"
}

Action Types:
- TOOL_CALL: Use a tool to gather information or take action
- COMPLETE: Goal is achieved, provide final answer

IMPORTANT: Only return JSON, no other text."""
    
    def run(self, goal: str) -> Dict[str, Any]:
        """
        Main entry point - run the agent with a goal.
        
        Args:
            goal: Natural language description of what the user wants
            
        Returns:
            Dictionary with the final result and execution metadata
        """
        self.logger.start_session(goal)
        
        # Store goal in context
        self.memory.update_context("current_goal", goal)
        self.memory.add_to_conversation("user", goal)
        
        iteration = 0
        context = {}
        
        try:
            while iteration < self.config.max_iterations:
                iteration += 1
                
                # ============== SENSE ==============
                # Gather current context and state
                if iteration == 1:
                    context = self._sense(goal, iteration)
                
                # ============== PLAN ==============
                # Decide what action to take
                plan = self._plan(goal, context, iteration)
                
                # Check if we should complete
                if plan.get("action_type") == "COMPLETE":
                    result = {
                        "status": "completed",
                        "answer": plan.get("answer", plan.get("reasoning", "")),
                        "iterations": iteration,
                    }
                    self.memory.add_to_conversation("assistant", result["answer"])
                    self.logger.complete(result)
                    return result
                
                # ============== ACT ==============
                # Execute the planned action
                action_result = self._act(plan, iteration)
                
                # ============== OBSERVE ==============
                # Record what happened
                self._observe(plan, action_result, iteration)
                
                # Update context with result
                context["last_action"] = plan
                context["last_result"] = action_result
                
                # ============== REFLECT ==============
                # Evaluate progress
                reflection = self._reflect(goal, plan, action_result, context, iteration)
                context["last_reflection"] = reflection
            
            # Max iterations reached
            result = {
                "status": "max_iterations",
                "answer": "I wasn't able to fully complete your request within the iteration limit. Here's what I found: " + json.dumps(context.get("last_result", {})),
                "iterations": iteration,
            }
            self.logger.complete(result)
            return result
            
        except Exception as e:
            result = {
                "status": "error",
                "error": str(e),
                "iterations": iteration,
            }
            self.logger.log_phase("ERROR", {"error": str(e)}, iteration)
            return result
    
    def _sense(self, goal: str, iteration: int) -> Dict[str, Any]:
        """
        SENSE Phase: Gather context about current state.
        
        This phase collects all relevant information before planning.
        """
        # Get user context
        user_context = self.tools.execute("get_user_context", {})
        
        context = {
            "goal": goal,
            "user": user_context.get("user", {}),
            "recent_conversation": self.memory.get_recent_context(),
            "available_tools": list(self.tools.tools.keys()),
        }
        
        self.logger.log_phase("SENSE", {
            "gathered_context": "user preferences, conversation history",
            "user_level": context["user"].get("learning_level", "unknown"),
        }, iteration)
        
        return context
    
    def _plan(self, goal: str, context: Dict[str, Any], iteration: int) -> Dict[str, Any]:
        """
        PLAN Phase: Use LLM to decide next action.
        
        The LLM receives:
        - The current goal
        - Available tools and their descriptions
        - Current context (user info, previous results)
        - History of actions taken
        
        It responds with a JSON plan specifying what to do next.
        """
        # Build the planning prompt
        tools_description = self.tools.get_tools_for_prompt()
        
        planning_prompt = f"""## Current Goal
{goal}

## User Context
- Name: {context.get('user', {}).get('name', 'Unknown')}
- Level: {context.get('user', {}).get('learning_level', 'intermediate')}
- Interests: {context.get('user', {}).get('interests', [])}

## {tools_description}

## Previous Actions This Session
{json.dumps(context.get('last_action', 'None - this is the first action'), indent=2)}

## Last Result
{json.dumps(context.get('last_result', 'None yet'), indent=2)[:500]}

## Last Reflection
{context.get('last_reflection', 'None yet')}

## Your Task
Decide the NEXT action to take. If you have enough information to answer the goal, use action_type "COMPLETE" and include an "answer" field.

Respond with ONLY valid JSON:
{{"action_type": "TOOL_CALL" | "COMPLETE", "tool": "tool_name", "args": {{}}, "reasoning": "why", "answer": "only if COMPLETE"}}"""
        
        # Call LLM for planning
        response = self.llm.chat.completions.create(
            model=self.config.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": planning_prompt},
            ],
            temperature=self.config.temperature,
            max_tokens=500,
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Parse the JSON response
        plan = self._parse_json_response(response_text)
        
        self.logger.log_phase("PLAN", {
            "action_type": plan.get("action_type"),
            "tool": plan.get("tool", "N/A"),
            "reasoning": plan.get("reasoning", "")[:100],
        }, iteration)
        
        return plan
    
    def _act(self, plan: Dict[str, Any], iteration: int) -> Dict[str, Any]:
        """
        ACT Phase: Execute the planned action.
        
        This phase takes the plan from the LLM and executes it.
        For TOOL_CALL actions, it runs the specified tool with arguments.
        """
        action_type = plan.get("action_type")
        
        if action_type != "TOOL_CALL":
            return {"skipped": True, "reason": f"Action type is {action_type}"}
        
        tool_name = plan.get("tool")
        args = plan.get("args", {})
        
        # Execute the tool
        result = self.tools.execute(tool_name, args)
        
        self.logger.log_phase("ACT", {
            "tool": tool_name,
            "args": args,
            "success": result.get("success", False),
        }, iteration)
        
        return result
    
    def _observe(self, plan: Dict[str, Any], result: Dict[str, Any], iteration: int):
        """
        OBSERVE Phase: Record and analyze the result.
        
        This phase logs what happened after executing an action.
        It helps build context for future planning.
        """
        observation = {
            "action_taken": plan.get("tool", plan.get("action_type")),
            "success": result.get("success", "unknown"),
            "result_summary": self._summarize_result(result),
        }
        
        self.logger.log_phase("OBSERVE", observation, iteration)
    
    def _reflect(
        self,
        goal: str,
        plan: Dict[str, Any],
        result: Dict[str, Any],
        context: Dict[str, Any],
        iteration: int,
    ) -> str:
        """
        REFLECT Phase: Evaluate progress toward the goal.
        
        The LLM reflects on what happened and determines if:
        - The goal has been achieved
        - More actions are needed
        - A different approach should be tried
        """
        reflection_prompt = f"""## Goal
{goal}

## Action Taken
Tool: {plan.get('tool', 'N/A')}
Reasoning: {plan.get('reasoning', 'N/A')}

## Result
{json.dumps(self._summarize_result(result), indent=2)}

## Task
Provide a brief (2-3 sentences) reflection on:
1. Did this action help progress toward the goal?
2. What should be done next?

Be concise and actionable."""
        
        response = self.llm.chat.completions.create(
            model=self.config.model,
            messages=[
                {"role": "system", "content": "You are reflecting on an AI agent's progress. Be brief and actionable."},
                {"role": "user", "content": reflection_prompt},
            ],
            temperature=self.config.temperature,
            max_tokens=150,
        )
        
        reflection = response.choices[0].message.content.strip()
        
        self.logger.log_phase("REFLECT", {
            "reflection": reflection,
        }, iteration)
        
        return reflection
    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """Parse JSON from LLM response, handling markdown code blocks."""
        # Remove markdown code blocks if present
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]
        
        try:
            return json.loads(response_text.strip())
        except json.JSONDecodeError:
            # Fallback: try to extract JSON object
            import re
            match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if match:
                return json.loads(match.group())
            raise ValueError(f"Could not parse JSON from: {response_text[:200]}")
    
    def _summarize_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Create a brief summary of a result for logging."""
        summary = {"success": result.get("success", "unknown")}
        
        if "results" in result:
            summary["results_count"] = len(result["results"])
            if result["results"]:
                summary["first_result"] = {
                    "title": result["results"][0].get("title", "N/A"),
                    "preview": result["results"][0].get("content", "")[:100],
                }
        
        if "error" in result:
            summary["error"] = result["error"]
        
        if "memories" in result:
            summary["memories_found"] = len(result["memories"])
        
        return summary


# =============================================================================
# SECTION 7: MAIN ENTRY POINT AND EXAMPLES
# =============================================================================

def main():
    """
    Main function demonstrating agent usage.
    
    Run this script directly to see the agent in action:
        python simple_agent.py
    """
    print("\n" + "=" * 60)
    print("🤖 SIMPLE AI AGENT DEMO")
    print("=" * 60)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ Error: OPENAI_API_KEY not found!")
        print("Please create a .env file with your OpenAI API key:")
        print("  OPENAI_API_KEY=sk-your-key-here")
        return
    
    # Create agent with default config
    config = AgentConfig(
        model="gpt-4o-mini",
        max_iterations=5,
        temperature=0.3,
        verbose=True,
    )
    
    agent = SimpleAgent(config)
    
    # Example goals to test
    example_goals = [
        "What is an AI agent and how does the agent loop work?",
        # "Explain RAG to me like I'm a beginner",
        # "What tools can AI agents use?",
    ]
    
    # Run the agent with the first example
    goal = example_goals[0]
    print(f"\n📝 Running agent with goal: '{goal}'")
    
    result = agent.run(goal)
    
    # Display final result
    print("\n" + "=" * 60)
    print("📋 FINAL RESULT")
    print("=" * 60)
    print(f"\nStatus: {result.get('status')}")
    print(f"Iterations: {result.get('iterations')}")
    print(f"\nAnswer:\n{result.get('answer', result.get('error', 'No answer'))}")


if __name__ == "__main__":
    main()

