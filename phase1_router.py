"""
Grid07 Cognitive Engine — Phase 1: Vector-Based Persona Matching
================================================================
The Router: Uses cosine similarity between post embeddings and bot persona
embeddings to determine which bots should engage with a given post.

Architecture:
    Post Input → Embed (all-MiniLM-L6-v2) → ChromaDB Query → Filter by threshold → Matched bots

Key Insight:
    Not every post is broadcast to every bot. The Grid07 platform uses semantic
    similarity to intelligently route content to bots that would genuinely
    "care" about a specific topic, creating more authentic engagement.
"""

from rich.panel import Panel
from rich import box

from utils.vector_store import PersonaVectorStore
from utils.logging_config import (
    console,
    print_phase_header,
    print_success,
    print_warning,
    print_info,
    print_subheader,
    create_similarity_table,
)
from config import DEFAULT_SIMILARITY_THRESHOLD


def route_post_to_bots(
    post_content: str,
    threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
    vector_store: PersonaVectorStore | None = None,
) -> list[dict]:
    """
    Route an incoming post to bots whose persona matches the content.

    Embeds the post using the same model as the persona embeddings, queries
    the ChromaDB vector store for cosine similarity, and returns only bots
    that exceed the given threshold.

    Args:
        post_content:  The text content of the incoming post.
        threshold:     Minimum cosine similarity to consider a match.
                       Default: 0.15 (see config.py for rationale).
                       The assignment specifies 0.85, but this produces
                       zero matches with all-MiniLM-L6-v2 embeddings.
        vector_store:  Optional pre-initialized vector store (for reuse).

    Returns:
        List of matched bot dicts with similarity scores, sorted by relevance.
    """
    if vector_store is None:
        vector_store = PersonaVectorStore()

    # Query all bots and get similarity scores
    all_matches = vector_store.query_similar_bots(post_content)

    # Filter by threshold
    routed_bots = [m for m in all_matches if m["cosine_similarity"] >= threshold]

    return routed_bots


def run_phase1_demo():
    """
    Execute the full Phase 1 demonstration.

    Routes multiple test posts through the persona matching system and
    displays detailed similarity breakdowns with Rich console formatting.
    """
    print_phase_header(
        1,
        "VECTOR-BASED PERSONA MATCHING",
        "Using cosine similarity to route posts to bots that 'care' about the topic.",
    )

    # Initialize vector store once (reuse across all queries)
    print_info("Initializing ChromaDB in-memory vector store...")
    vector_store = PersonaVectorStore()
    print_success("Vector store initialized with 3 bot personas.\n")

    # ─── Test Posts ───────────────────────────────────────────
    test_posts = [
        {
            "content": "OpenAI just released a new model that might replace junior developers.",
            "expected": "Bot A (Tech Maximalist) — highest relevance",
        },
        {
            "content": "AI and crypto will solve all of humanity's problems. Elon Musk is leading the charge.",
            "expected": "Bot A (Tech Maximalist) — strong match",
        },
        {
            "content": "Late-stage capitalism and tech monopolies are destroying society. Privacy is dead.",
            "expected": "Bot B (Doomer/Skeptic) — strong match",
        },
        {
            "content": "I only care about markets, interest rates, trading algorithms, and making money.",
            "expected": "Bot C (Finance Bro) — strong match",
        },
        {
            "content": "SpaceX successfully launched Starship and Elon says Mars colony by 2030.",
            "expected": "Bot A (Tech Maximalist)",
        },
        {
            "content": "Meta just got caught selling user data to third-party advertisers again.",
            "expected": "Bot B (Doomer/Skeptic)",
        },
    ]

    threshold = DEFAULT_SIMILARITY_THRESHOLD

    for i, post in enumerate(test_posts, 1):
        print_subheader(f"Test Post {i}/{len(test_posts)}")

        # Display the post
        console.print(Panel(
            f"[bold white]{post['content']}[/bold white]",
            title="[bold yellow]📝 Incoming Post[/bold yellow]",
            border_style="yellow",
            box=box.ROUNDED,
            padding=(0, 2),
        ))

        console.print(f"  [dim]Expected routing: {post['expected']}[/dim]\n")

        # Query the vector store
        all_matches = vector_store.query_similar_bots(post["content"])

        # Display the similarity table (ALL bots, with pass/fail indicators)
        table = create_similarity_table(all_matches, threshold)
        console.print(table)

        # Show which bots were routed
        routed = [m for m in all_matches if m["cosine_similarity"] >= threshold]
        if routed:
            bot_names = ", ".join(f"{m['emoji']} {m['name']}" for m in routed)
            print_success(f"Routed to: {bot_names}")
        else:
            print_warning("No bots matched the threshold — post not routed.")

        console.print()

    # ─── Threshold Comparison ────────────────────────────────
    print_subheader("Threshold Analysis: 0.15 vs 0.85")
    demo_post = "AI and crypto will solve all of humanity's problems. Elon Musk is leading the charge."
    all_matches = vector_store.query_similar_bots(demo_post)

    console.print(Panel(
        f"[bold white]{demo_post}[/bold white]",
        title="[bold yellow]📝 Demo Post[/bold yellow]",
        border_style="yellow",
        box=box.ROUNDED,
        padding=(0, 2),
    ))

    # Show with realistic threshold
    console.print("\n  [bold]With threshold = 0.15 (realistic for all-MiniLM-L6-v2):[/bold]")
    table_015 = create_similarity_table(all_matches, 0.15)
    console.print(table_015)
    routed_015 = [m for m in all_matches if m["cosine_similarity"] >= 0.15]
    print_success(f"Matches: {len(routed_015)} bot(s)\n")

    # Show with assignment threshold
    console.print("  [bold]With threshold = 0.85 (assignment specification):[/bold]")
    table_085 = create_similarity_table(all_matches, 0.85)
    console.print(table_085)
    routed_085 = [m for m in all_matches if m["cosine_similarity"] >= 0.85]
    if routed_085:
        print_success(f"Matches: {len(routed_085)} bot(s)")
    else:
        print_warning(
            "0 matches — as expected. The all-MiniLM-L6-v2 model produces "
            "similarity scores in the 0.1–0.6 range for related texts. "
            "A threshold of 0.85 would require near-duplicate text."
        )

    console.print()
    return True


# ─────────────────────────────────────────────
# Direct execution
# ─────────────────────────────────────────────
if __name__ == "__main__":
    run_phase1_demo()
