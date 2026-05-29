# Grid07 Cognitive Engine

> AI Cognitive Engine featuring **vector-based semantic routing**, **LangGraph multi-agent orchestration**, and a **RAG combat engine** with multi-layered prompt injection defense.

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white" />
</p>

---

## What It Does

Grid07 Cognitive Engine is an intelligent AI backend that routes user queries through semantic vector matching, orchestrates multi-step reasoning using LangGraph state machines, and retrieves context-aware responses through a RAG (Retrieval-Augmented Generation) pipeline -- all secured with multi-layered prompt injection defense.

---

## Architecture

`
  User Query
       |
       v
  +----------------------------+
  |  Prompt Injection Shield   |
  |  Multi-layered defense     |
  +-------------+--------------+
                |
                v
  +----------------------------+
  |  Vector Semantic Router    |
  |  Query classification      |
  |  Intent detection          |
  +-------------+--------------+
                |
                v
  +----------------------------+
  |  LangGraph Orchestrator    |
  |  Multi-agent state graph   |
  |  Conditional routing       |
  +-------------+--------------+
                |
                v
  +----------------------------+
  |  RAG Combat Engine         |
  |  Vector DB retrieval       |
  |  Context-aware generation  |
  +-------------+--------------+
                |
                v
  +----------------------------+
  |  Response Output           |
  +----------------------------+
`

---

## Key Features

- **Vector Routing** -- Semantic similarity-based query routing to specialized agent nodes
- **LangGraph Orchestration** -- Stateful multi-agent workflows with conditional branching
- **RAG Pipeline** -- Context retrieval from vector databases for grounded responses
- **Prompt Injection Defense** -- Multi-layered security against adversarial prompt attacks
- **Modular Design** -- Easily extensible agent nodes and routing logic
- **Three-Phase Architecture** -- Router -> Content Engine -> Combat Engine pipeline

---

## Project Structure

`
grid07-cognitive-engine/
|-- main.py                    # Entry point
|-- config.py                  # Configuration
|-- personas.py                # Agent persona definitions
|-- phase1_router.py           # Semantic vector routing
|-- phase2_content_engine.py   # Content generation engine
|-- phase3_combat_engine.py    # RAG combat engine
|-- requirements.txt           # Dependencies
|-- tests/                     # Test suite
|-- tools/                     # Utility tools
|-- utils/                     # Helper functions
`

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python |
| LLM Framework | LangChain, LangGraph |
| Vector Database | Vector embeddings for semantic search |
| Security | Multi-layered prompt injection defense |

---

## Getting Started

`ash
git clone https://github.com/udayraj1238/grid07-cognitive-engine.git
cd grid07-cognitive-engine
pip install -r requirements.txt
cp .env.example .env  # Add your API keys
python main.py
`

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

## Contact

**Uday Raj** -- [LinkedIn](https://www.linkedin.com/in/uday6002/) | [Portfolio](https://udayraj1238.vercel.app) | [Email](mailto:rajuday6002@gmail.com)