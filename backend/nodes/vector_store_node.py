from __future__ import annotations

from typing import Any, Dict, List, Tuple

from openai import AsyncOpenAI
from pinecone import Pinecone

from core.config import settings
from nodes.base_node import BaseNode


def _tokenize(text: str) -> List[str]:
    return [t for t in text.lower().split() if t]


def _score(query_tokens: List[str], doc_tokens: List[str]) -> float:
    if not query_tokens or not doc_tokens:
        return 0.0
    query_set = set(query_tokens)
    doc_set = set(doc_tokens)
    return len(query_set & doc_set) / max(len(query_set), 1)


class VectorStoreNode(BaseNode):
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        query_key = self.config.get("query_key", "input")
        output_key = self.config.get("output_key", "vector_results")
        top_k = int(self.config.get("top_k", 3))

        query = str(state.get(query_key, ""))

        api_key = self.config.get("pinecone_api_key") or settings.pinecone_api_key
        index_name = self.config.get("pinecone_index") or settings.pinecone_index
        env = self.config.get("pinecone_env") or settings.pinecone_env
        openai_key = self.config.get("openai_api_key") or settings.openai_api_key

        if api_key and index_name and env and openai_key:
            client = AsyncOpenAI(api_key=openai_key)
            embed = await client.embeddings.create(
                model=self.config.get("embedding_model", "text-embedding-3-small"),
                input=query,
            )
            vector = embed.data[0].embedding

            pc = Pinecone(api_key=api_key, environment=env)
            index = pc.Index(index_name)
            query_result = index.query(vector=vector, top_k=top_k, include_metadata=True)

            matches = query_result.get("matches", [])
            results = [
                {
                    "id": match.get("id"),
                    "score": match.get("score"),
                    "metadata": match.get("metadata", {}),
                }
                for match in matches
            ]
            text_parts = [str(item.get("metadata", {}).get("text", "")) for item in results]
            return {
                output_key: results,
                "vector_results_text": "\n".join([t for t in text_parts if t]),
                "logs": [
                    {
                        "node": "VectorStoreNode",
                        "provider": "pinecone",
                        "count": len(results),
                    }
                ],
            }

        documents = self.config.get("documents") or []
        scored: List[Tuple[float, str]] = []
        query_tokens = _tokenize(query)

        for doc in documents:
            if isinstance(doc, dict):
                text = str(doc.get("text", ""))
            else:
                text = str(doc)
            score = _score(query_tokens, _tokenize(text))
            scored.append((score, text))

        scored.sort(key=lambda item: item[0], reverse=True)
        top_docs = scored[:top_k]
        results = [
            {"score": score, "text": text}
            for score, text in top_docs
            if text
        ]

        return {
            output_key: results,
            "vector_results_text": "\n".join([item["text"] for item in results]),
            "logs": [
                {
                    "node": "VectorStoreNode",
                    "provider": "in-memory",
                    "count": len(results),
                    "warning": "Pinecone not configured, using in-memory retrieval",
                }
            ],
        }
