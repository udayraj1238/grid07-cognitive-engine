<div align="center">

<!-- Animated Header -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:06B6D4,50:0EA5E9,100:3B82F6&height=220&section=header&text=Grid07%20Cognitive%20Engine&fontSize=42&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=AI%20Routing%20%7C%20LangGraph%20%7C%20RAG%20%7C%20Prompt%20Defense&descSize=16&descAlignY=55&descAlign=50" width="100%"/>

<!-- Typing SVG -->
<a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=0EA5E9&center=true&vCenter=true&width=650&lines=Vector+Semantic+Query+Routing;Multi-Agent+LangGraph+Orchestration;RAG+Combat+Engine;Multi-Layered+Prompt+Injection+Defense" alt="Typing SVG" /></a>

<br/>

<!-- Badges -->
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" />
<img src="https://img.shields.io/badge/LangGraph-FF6F00?style=for-the-badge&logo=graphql&logoColor=white" />
<img src="https://img.shields.io/badge/RAG-8B5CF6?style=for-the-badge&logo=elasticsearch&logoColor=white" />

</div>

---

<div align="center">
<h2>🎯 What It Does</h2>
<p><i>An intelligent AI backend that routes queries through semantic vectors, orchestrates multi-step reasoning, and retrieves context-aware responses — all secured against prompt injection attacks.</i></p>
</div>

---

<div align="center">
<h2>🏗️ Three-Phase Architecture</h2>
</div>

```mermaid
graph TD
    A["💬 User Query"] --> B["🛡️ Prompt Injection Shield"]
    
    B --> C["Phase 1: Router"]
    
    subgraph P1["🔵 Phase 1 — Semantic Router"]
        C --> C1["Vector Embedding"]
        C1 --> C2["Cosine Similarity"]
        C2 --> C3["Intent Classification"]
    end
    
    C3 --> D["Phase 2: Content Engine"]
    
    subgraph P2["🟣 Phase 2 — Content Engine"]
        D --> D1["LangGraph State Machine"]
        D1 --> D2["Multi-Agent Workflow"]
        D2 --> D3["Conditional Branching"]
    end
    
    D3 --> E["Phase 3: Combat Engine"]
    
    subgraph P3["🔴 Phase 3 — RAG Combat"]
        E --> E1["Vector DB Retrieval"]
        E1 --> E2["Context Injection"]
        E2 --> E3["Grounded Generation"]
    end
    
    E3 --> F["✅ Secure Response"]
    
    style A fill:#F59E0B,stroke:#F59E0B,color:#fff
    style B fill:#EF4444,stroke:#EF4444,color:#fff
    style C fill:#3B82F6,stroke:#3B82F6,color:#fff
    style C1 fill:#60A5FA,stroke:#60A5FA,color:#fff
    style C2 fill:#60A5FA,stroke:#60A5FA,color:#fff
    style C3 fill:#60A5FA,stroke:#60A5FA,color:#fff
    style D fill:#8B5CF6,stroke:#8B5CF6,color:#fff
    style D1 fill:#A78BFA,stroke:#A78BFA,color:#fff
    style D2 fill:#A78BFA,stroke:#A78BFA,color:#fff
    style D3 fill:#A78BFA,stroke:#A78BFA,color:#fff
    style E fill:#EF4444,stroke:#EF4444,color:#fff
    style E1 fill:#F87171,stroke:#F87171,color:#fff
    style E2 fill:#F87171,stroke:#F87171,color:#fff
    style E3 fill:#F87171,stroke:#F87171,color:#fff
    style F fill:#10B981,stroke:#10B981,color:#fff
```

---

<div align="center">
<h2>✨ Key Features</h2>
</div>

<table>
<tr>
<td align="center" width="25%">
<img src="https://img.shields.io/badge/🔵-Vector_Router-3B82F6?style=for-the-badge&labelColor=1a1a2e" /><br/><br/>
Semantic similarity-based query routing to specialized agent nodes
</td>
<td align="center" width="25%">
<img src="https://img.shields.io/badge/🟣-LangGraph-8B5CF6?style=for-the-badge&labelColor=1a1a2e" /><br/><br/>
Stateful multi-agent workflows with conditional branching
</td>
<td align="center" width="25%">
<img src="https://img.shields.io/badge/🔴-RAG_Engine-EF4444?style=for-the-badge&labelColor=1a1a2e" /><br/><br/>
Vector DB retrieval for context-grounded generation
</td>
<td align="center" width="25%">
<img src="https://img.shields.io/badge/🛡️-Defense-F59E0B?style=for-the-badge&labelColor=1a1a2e" /><br/><br/>
Multi-layered prompt injection protection
</td>
</tr>
</table>

---

<div align="center">
<h2>📁 Project Structure</h2>
</div>

```
grid07-cognitive-engine/
├── 🚀 main.py                    # Entry point
├── ⚙️ config.py                  # Configuration
├── 🎭 personas.py                # Agent persona definitions
├── 🔵 phase1_router.py           # Semantic vector routing
├── 🟣 phase2_content_engine.py   # Content generation engine
├── 🔴 phase3_combat_engine.py    # RAG combat engine
├── 📋 requirements.txt
├── 🧪 tests/                     # Test suite
├── 🔧 tools/                     # Utility tools
└── 📦 utils/                     # Helper functions
```

---

<div align="center">
<h2>🚀 Quick Start</h2>
</div>

```bash
git clone https://github.com/udayraj1238/grid07-cognitive-engine.git
cd grid07-cognitive-engine
pip install -r requirements.txt
cp .env.example .env  # Add your API keys
python main.py
```

---

<div align="center">

<h2>🤝 Contact</h2>
<a href="https://www.linkedin.com/in/uday6002/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" /></a>
<a href="https://udayraj1238.vercel.app"><img src="https://img.shields.io/badge/Portfolio-000000?style=for-the-badge&logo=vercel&logoColor=white" /></a>
<a href="mailto:rajuday6002@gmail.com"><img src="https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white" /></a>

</div>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:06B6D4,50:0EA5E9,100:3B82F6&height=120&section=footer" width="100%"/>
