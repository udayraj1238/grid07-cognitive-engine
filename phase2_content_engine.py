"""
Grid07 Cognitive Engine — Phase 2: Autonomous Content Engine (LangGraph)
========================================================================
When a bot is scheduled to create an original post, it doesn't just guess —
it researches real-world context using a structured LangGraph state machine.

LangGraph State Machine:
    ┌─────────────┐     ┌──────────────┐     ┌────────────┐
    │ decide_search│ ──→ │  web_search  │ ──→ │ draft_post │ ──→ END
    └─────────────┘     └──────────────┘     └────────────┘

Nodes:
    1. decide_search — LLM analyzes the bot's persona and decides a trending
                       topic + search query for today's post.
    2. web_search    — Executes mock_searxng_search tool to get real-world context.
    3. draft_post    — LLM uses persona + search results to generate a
                       280-character opinionated post as strict JSON.

Output Format (Pydantic-enforced):
    {"bot_id": "...", "topic": "...", "post_content": "..."}
"""

from typing import Optional
from typing_extensions import TypedDict

from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END

from config import GROQ_API_KEY, GROQ_MODEL, GROQ_TEMPERATURE, GROQ_MAX_TOKENS
from personas import ALL_BOTS, BotPersona
from tools.mock_search import mock_searxng_search
from utils.logging_config import (
    console,
    print_phase_header,
    print_success,
    print_info,
    print_error,
    print_subheader,
)
from rich.panel import Panel
from rich.syntax import Syntax
from rich import box
import json


# ─────────────────────────────────────────────
# Pydantic Model for Structured Output
# ─────────────────────────────────────────────

class BotPost(BaseModel):
    """
    Strict output schema for bot-generated posts.
    Enforced via LangChain's with_structured_output() to guarantee
    valid JSON output from the LLM every time.
    """
    bot_id: str = Field(
        description="The unique identifier of the bot generating the post (e.g., 'bot_a')"
    )
    topic: str = Field(
        description="The main topic or theme of the post (e.g., 'AI advancement')"
    )
    post_content: str = Field(
        description="The actual post text, maximum 280 characters, highly opinionated and in-character",
        max_length=280,
    )


class SearchDecision(BaseModel):
    """Schema for the search query decision node."""
    topic: str = Field(description="The trending topic the bot wants to post about today")
    search_query: str = Field(description="A concise search query to find recent news about this topic")


# ─────────────────────────────────────────────
# LangGraph State Definition
# ─────────────────────────────────────────────

class ContentEngineState(TypedDict):
    """State that flows through the LangGraph content generation pipeline."""
    bot_id: str
    persona: str                          # Bot's system prompt
    persona_text: str                     # Bot's persona description
    search_topic: Optional[str]           # Decided topic
    search_query: Optional[str]           # Formatted search query
    search_results: Optional[str]         # Raw search results from tool
    final_post: Optional[dict]            # The generated BotPost as dict


# ─────────────────────────────────────────────
# LangGraph Nodes
# ─────────────────────────────────────────────

def decide_search_node(state: ContentEngineState) -> dict:
    """
    Node 1: Decide Search
    
    The LLM analyzes the bot's persona and decides what trending topic
    it wants to post about today. It formats a search query to find
    relevant real-world context.
    """
    llm = ChatGroq(
        model=GROQ_MODEL,
        temperature=0.7,  # Slightly creative for topic selection
        api_key=GROQ_API_KEY,
    )
    structured_llm = llm.with_structured_output(SearchDecision)

    messages = [
        SystemMessage(content=state["persona"]),
        HumanMessage(content=(
            "You're about to create a post on Grid07. Based on your persona and interests, "
            "decide what trending topic you want to post about today. Pick something specific "
            "and current that aligns with your worldview. Return a topic and a search query "
            "to find recent news about it."
        )),
    ]

    result = structured_llm.invoke(messages)
    return {
        "search_topic": result.topic,
        "search_query": result.search_query,
    }


def web_search_node(state: ContentEngineState) -> dict:
    """
    Node 2: Web Search
    
    Executes the mock_searxng_search tool with the query decided
    in the previous node. No LLM call here — pure tool execution.
    """
    search_results = mock_searxng_search.invoke(state["search_query"])
    return {"search_results": search_results}


def draft_post_node(state: ContentEngineState) -> dict:
    """
    Node 3: Draft Post
    
    The LLM uses its persona (system prompt) combined with the search
    results (real-world context) to generate a highly opinionated,
    280-character post. Output is enforced as strict JSON via Pydantic.
    """
    llm = ChatGroq(
        model=GROQ_MODEL,
        temperature=0.9,  # Creative for post generation
        api_key=GROQ_API_KEY,
        max_tokens=GROQ_MAX_TOKENS,
    )
    structured_llm = llm.with_structured_output(BotPost)

    messages = [
        SystemMessage(content=state["persona"]),
        HumanMessage(content=(
            f"Based on the following recent news, write a highly opinionated post for Grid07.\n\n"
            f"TOPIC: {state['search_topic']}\n\n"
            f"RECENT NEWS CONTEXT:\n{state['search_results']}\n\n"
            f"RULES:\n"
            f"- Your post MUST be max 280 characters\n"
            f"- Be provocative, opinionated, and fully in-character\n"
            f"- Reference the real news to seem informed\n"
            f"- Your bot_id is: {state['bot_id']}\n"
            f"- The topic field should be a short label for the topic"
        )),
    ]

    result = structured_llm.invoke(messages)
    return {"final_post": result.model_dump()}


# ─────────────────────────────────────────────
# Build the LangGraph
# ─────────────────────────────────────────────

def build_content_engine_graph() -> StateGraph:
    """
    Construct and compile the LangGraph state machine for content generation.
    
    Graph structure:
        START → decide_search → web_search → draft_post → END
    """
    workflow = StateGraph(ContentEngineState)

    # Add nodes
    workflow.add_node("decide_search", decide_search_node)
    workflow.add_node("web_search", web_search_node)
    workflow.add_node("draft_post", draft_post_node)

    # Define edges (linear pipeline)
    workflow.set_entry_point("decide_search")
    workflow.add_edge("decide_search", "web_search")
    workflow.add_edge("web_search", "draft_post")
    workflow.add_edge("draft_post", END)

    return workflow.compile()


# ─────────────────────────────────────────────
# Phase 2 Demo Runner
# ─────────────────────────────────────────────

def run_phase2_demo():
    """
    Execute the full Phase 2 demonstration.

    Runs the LangGraph content engine for all 3 bots, displaying
    the state machine flow and generated posts with Rich formatting.
    """
    print_phase_header(
        2,
        "AUTONOMOUS CONTENT ENGINE",
        "LangGraph state machine generates persona-consistent posts using real-world context.",
    )

    # Validate API key
    if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
        print_error("GROQ_API_KEY not set! Please configure your .env file.")
        print_info("Get a free key at: https://console.groq.com")
        return False

    # Build the graph
    print_info("Building LangGraph state machine...")
    graph = build_content_engine_graph()
    print_success("Graph compiled successfully.")

    # Display graph structure
    print_info("Graph Node Structure: decide_search → web_search → draft_post → END\n")

    # Run for each bot
    for bot in ALL_BOTS:
        print_subheader(f"Generating Post for {bot.emoji} {bot.name} ({bot.archetype})")

        # Prepare initial state
        initial_state = {
            "bot_id": bot.bot_id,
            "persona": bot.system_prompt,
            "persona_text": bot.persona_text,
            "search_topic": None,
            "search_query": None,
            "search_results": None,
            "final_post": None,
        }

        try:
            # Execute the graph
            print_info("Running LangGraph pipeline...")
            final_state = graph.invoke(initial_state)

            # Display the flow
            console.print(f"\n  [dim]Step 1 — Topic Decided:[/dim] {final_state['search_topic']}")
            console.print(f"  [dim]Step 2 — Search Query:[/dim]  {final_state['search_query']}")
            console.print(f"  [dim]Step 3 — Search Results:[/dim]")
            for line in final_state["search_results"].split("\n"):
                console.print(f"    [dim]{line}[/dim]")

            # Display the final post as formatted JSON
            post_json = json.dumps(final_state["final_post"], indent=2)
            console.print()
            console.print(Panel(
                Syntax(post_json, "json", theme="monokai", word_wrap=True),
                title=f"[bold green]✓ Generated Post — {bot.emoji} {bot.name}[/bold green]",
                border_style="green",
                box=box.ROUNDED,
                padding=(1, 2),
            ))

            # Validate constraints
            post_content = final_state["final_post"]["post_content"]
            char_count = len(post_content)
            if char_count <= 280:
                print_success(f"Character count: {char_count}/280 ✓")
            else:
                print_error(f"Character count: {char_count}/280 — EXCEEDS LIMIT")

            print_success("JSON schema validated via Pydantic ✓\n")

        except Exception as e:
            print_error(f"Error generating post for {bot.name}: {e}")
            console.print_exception()

    return True


# ─────────────────────────────────────────────
# Direct execution
# ─────────────────────────────────────────────
if __name__ == "__main__":
    run_phase2_demo()
