"""
Grid07 Cognitive Engine — Vector Store Utilities
=================================================
Manages the ChromaDB in-memory vector store for bot persona embeddings.
Uses cosine distance for similarity matching between posts and personas.

Key Design Decision:
    ChromaDB returns DISTANCE (not similarity). For cosine distance:
        similarity = 1 - distance
    A distance of 0 = perfect match (similarity 1.0)
    A distance of 2 = opposite (similarity -1.0)
"""

import chromadb
from personas import ALL_BOTS, BotPersona
from config import VECTOR_COLLECTION_NAME, VECTOR_DISTANCE_METRIC


class PersonaVectorStore:
    """
    In-memory vector store for bot persona matching.
    
    Uses ChromaDB's EphemeralClient (no disk persistence) with cosine distance
    to simulate the pgvector database described in the Grid07 architecture.
    """

    def __init__(self):
        """Initialize the in-memory ChromaDB client and load personas."""
        self.client = chromadb.EphemeralClient()

        # Delete existing collection if it exists (ensures clean state in tests)
        try:
            self.client.delete_collection(name=VECTOR_COLLECTION_NAME)
        except Exception:
            pass

        self.collection = self.client.create_collection(
            name=VECTOR_COLLECTION_NAME,
            metadata={"hnsw:space": VECTOR_DISTANCE_METRIC},
        )
        self._load_personas()

    def _load_personas(self):
        """Embed and store all bot personas in the vector collection."""
        self.collection.add(
            documents=[bot.persona_text for bot in ALL_BOTS],
            ids=[bot.bot_id for bot in ALL_BOTS],
            metadatas=[
                {
                    "name": bot.name,
                    "archetype": bot.archetype,
                    "emoji": bot.emoji,
                }
                for bot in ALL_BOTS
            ],
        )

    def query_similar_bots(
        self, post_content: str, n_results: int = 3
    ) -> list[dict]:
        """
        Query the vector store for bots whose persona is similar to the post.

        Args:
            post_content: The text of the incoming post.
            n_results: Number of results to return (default: all 3 bots).

        Returns:
            List of dicts with keys: bot_id, name, archetype, emoji,
            cosine_distance, cosine_similarity.
            Sorted by similarity (highest first).
        """
        results = self.collection.query(
            query_texts=[post_content],
            n_results=n_results,
            include=["distances", "metadatas", "documents"],
        )

        matches = []
        for i in range(len(results["ids"][0])):
            bot_id = results["ids"][0][i]
            distance = results["distances"][0][i]
            metadata = results["metadatas"][0][i]
            similarity = 1 - distance  # Convert cosine distance to similarity

            matches.append({
                "bot_id": bot_id,
                "name": metadata["name"],
                "archetype": metadata["archetype"],
                "emoji": metadata["emoji"],
                "cosine_distance": round(distance, 4),
                "cosine_similarity": round(similarity, 4),
                "persona_text": results["documents"][0][i],
            })

        # Sort by similarity (highest first)
        matches.sort(key=lambda x: x["cosine_similarity"], reverse=True)
        return matches
