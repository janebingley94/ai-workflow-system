from __future__ import annotations

from typing import Any, Dict

import httpx

from core.config import settings
from nodes.base_node import BaseNode


class SearchNode(BaseNode):
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        query_key = self.config.get("query_key", "input")
        output_key = self.config.get("output_key", "search_results")
        num_results = int(self.config.get("num_results", 5))

        query = state.get(query_key, "")
        api_key = self.config.get("tavily_api_key") or settings.tavily_api_key

        if not api_key:
            fallback = [
                {
                    "title": f"Fallback result {i+1}",
                    "url": "https://example.com",
                    "content": f"Result for '{query}' (fallback)",
                }
                for i in range(num_results)
            ]
            return {
                output_key: fallback,
                "logs": [
                    {
                        "node": "SearchNode",
                        "warning": "TAVILY_API_KEY not configured, using fallback",
                    }
                ],
            }

        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": api_key,
                    "query": str(query),
                    "max_results": num_results,
                },
            )
            response.raise_for_status()
            data = response.json()

        results = data.get("results", [])
        return {
            output_key: results,
            "logs": [
                {
                    "node": "SearchNode",
                    "count": len(results),
                }
            ],
        }
