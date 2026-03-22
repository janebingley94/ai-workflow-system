from __future__ import annotations

from typing import Any, Dict

from openai import AsyncOpenAI

from core.config import settings
from nodes.base_node import BaseNode


class LLMNode(BaseNode):
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        input_key = self.config.get("input_key", "input")
        output_key = self.config.get("output_key", "llm_output")
        model = self.config.get("model", "gpt-4o-mini")
        system_prompt = self.config.get("system_prompt", "You are a helpful assistant.")
        temperature = float(self.config.get("temperature", 0.7))
        max_tokens = self.config.get("max_tokens")

        user_input = state.get(input_key, "")
        api_key = self.config.get("openai_api_key") or settings.openai_api_key

        if not api_key:
            fallback = f"[LLM fallback] {user_input}".strip()
            return {
                output_key: fallback,
                "logs": [
                    {
                        "node": "LLMNode",
                        "warning": "OPENAI_API_KEY not configured, using fallback",
                    }
                ],
            }

        client = AsyncOpenAI(api_key=api_key)

        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": str(user_input)},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        content = response.choices[0].message.content or ""
        return {
            output_key: content,
            "logs": [
                {
                    "node": "LLMNode",
                    "model": model,
                    "preview": content[:120],
                }
            ],
        }
