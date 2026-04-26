"""
Grid07 Cognitive Engine — Mock SearXNG Search Tool
===================================================
Simulates a real-time news search engine (SearXNG) for the LangGraph
content engine. Returns hardcoded but realistic news headlines based
on keyword matching in the query.

In production, this would be replaced with actual SearXNG API calls
or a similar meta-search engine integration.
"""

from langchain_core.tools import tool


# ─────────────────────────────────────────────
# News headline database organized by topic
# ─────────────────────────────────────────────
NEWS_DATABASE = {
    "crypto": [
        "Bitcoin hits new all-time high amid regulatory ETF approvals — Bloomberg",
        "Ethereum Layer 2 solutions process 10x more transactions than mainnet — CoinDesk",
        "SEC approves three new spot crypto ETFs, institutional adoption surges — Reuters",
    ],
    "ai": [
        "OpenAI releases GPT-5 with PhD-level reasoning capabilities — TechCrunch",
        "Google DeepMind's Gemini 2.0 achieves human-level code generation — The Verge",
        "EU passes comprehensive AI Act, mandates transparency for all foundation models — Politico",
        "AI-generated code now accounts for 40% of new GitHub commits — Ars Technica",
    ],
    "elon": [
        "SpaceX Starship completes first successful orbital refueling mission — Space.com",
        "Tesla's Full Self-Driving achieves Level 4 autonomy approval in three US states — CNBC",
        "Neuralink receives FDA approval for second-generation brain implant — Wired",
    ],
    "space": [
        "NASA's Artemis III mission lands humans on the Moon for the first time since 1972 — NASA.gov",
        "SpaceX Starship completes first successful orbital refueling mission — Space.com",
        "Blue Origin launches first commercial space station module — The Verge",
    ],
    "privacy": [
        "Meta fined €2.3 billion for illegal data transfers under GDPR — TechCrunch",
        "Signal reports 300% growth as users flee WhatsApp over policy changes — Ars Technica",
        "California passes landmark data broker regulation bill — The Guardian",
    ],
    "environment": [
        "Global carbon emissions hit record high despite renewable energy growth — BBC",
        "Amazon rainforest reaches critical tipping point, scientists warn — Nature",
        "Major oil company caught greenwashing carbon offset programs — ProPublica",
    ],
    "market": [
        "S&P 500 breaks 6000 for the first time on strong earnings reports — CNBC",
        "Federal Reserve signals potential rate cut amid cooling inflation data — Bloomberg",
        "NVIDIA surpasses Apple as world's most valuable company at $4T market cap — Reuters",
    ],
    "trading": [
        "Algorithmic trading firms now account for 70% of daily market volume — Financial Times",
        "New SEC regulations target high-frequency trading latency arbitrage — WSJ",
        "Renaissance Technologies posts 40% returns using quantum computing signals — Bloomberg",
    ],
    "interest": [
        "Federal Reserve signals potential rate cut amid cooling inflation data — Bloomberg",
        "10-year Treasury yield drops to 3.2%, bond market rallies — CNBC",
        "Bank of Japan ends negative interest rate policy after 8 years — Reuters",
    ],
    "regulation": [
        "EU passes comprehensive AI Act, mandates transparency for all foundation models — Politico",
        "SEC cracks down on unregistered crypto exchanges, files 12 lawsuits — Reuters",
        "FTC proposes ban on non-compete clauses for tech workers — The Verge",
    ],
    "social media": [
        "TikTok faces potential US ban as Supreme Court upholds divestiture law — NYT",
        "Teen mental health crisis linked to social media, Surgeon General declares — WaPo",
        "Bluesky reaches 100 million users, challenges X/Twitter dominance — Wired",
    ],
    "capitalism": [
        "Top 1% now own more wealth than bottom 50% combined, Oxfam reports — The Guardian",
        "Tech layoffs reach 300,000 in 2025 despite record corporate profits — Business Insider",
        "Amazon warehouse workers unionize in 15 new locations — NPR",
    ],
    "ev": [
        "Tesla Model 3 battery retains 93% capacity after 200,000 miles in fleet study — Electrek",
        "China's BYD overtakes Tesla in global EV sales for first time — Bloomberg",
        "Solid-state EV batteries promise 500-mile range by 2026, Toyota announces — Reuters",
    ],
    "developer": [
        "AI-generated code now accounts for 40% of new GitHub commits — Ars Technica",
        "Stack Overflow traffic drops 35% as developers shift to AI coding assistants — The Verge",
        "Devin AI autonomously completes real software engineering tasks at 14% success rate — SWE-bench",
    ],
}

# Default fallback headlines for unmatched queries
DEFAULT_HEADLINES = [
    "Global markets show mixed signals as geopolitical tensions escalate — Reuters",
    "Tech sector continues to lead job market recovery in Q1 2025 — Bureau of Labor Statistics",
    "Climate change accelerates faster than predicted, IPCC report warns — Nature",
]


@tool
def mock_searxng_search(query: str) -> str:
    """
    Search for recent news and headlines related to the given query.
    
    This tool simulates a SearXNG meta-search engine that aggregates results
    from multiple news sources. Use it to find current events, trending topics,
    and recent developments relevant to your area of interest.

    Args:
        query: A search query string describing what news to look for.
              Example: "latest AI developments" or "crypto market trends"

    Returns:
        A formatted string containing relevant news headlines with sources.
    """
    query_lower = query.lower()
    matched_headlines = []

    # Match keywords in the query against our news database
    for keyword, headlines in NEWS_DATABASE.items():
        if keyword in query_lower:
            matched_headlines.extend(headlines)

    # Deduplicate while preserving order
    seen = set()
    unique_headlines = []
    for h in matched_headlines:
        if h not in seen:
            seen.add(h)
            unique_headlines.append(h)

    # Fallback to default if no keywords matched
    if not unique_headlines:
        unique_headlines = DEFAULT_HEADLINES

    # Format the results
    results = [f"  {i+1}. {headline}" for i, headline in enumerate(unique_headlines[:5])]
    return f"Search results for '{query}':\n" + "\n".join(results)
