from __future__ import annotations

from typing import Any, Dict

import httpx

from nodes.base_node import BaseNode


class HTTPNode(BaseNode):
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        method = str(self.config.get("method", "GET")).upper()
        url = str(self.config.get("url", ""))
        headers = self.config.get("headers") or {}
        params = self.config.get("params") or {}
        body = self.config.get("body")
        timeout = float(self.config.get("timeout", 15))
        output_key = self.config.get("output_key", "http_response")

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=body,
            )

        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            payload: Any = response.json()
        else:
            payload = response.text

        if isinstance(payload, str) and len(payload) > 2000:
            payload = payload[:2000] + "..."

        return {
            output_key: {
                "status": response.status_code,
                "data": payload,
            },
            "logs": [
                {
                    "node": "HTTPNode",
                    "status": response.status_code,
                    "url": url,
                }
            ],
        }
