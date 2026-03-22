from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseNode(ABC):
    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            result = await self.execute(state)
            if not isinstance(result, dict):
                raise ValueError("Node execution must return a dict")
            return self._append_log(result, {
                "node": self.__class__.__name__,
                "status": "ok",
            })
        except Exception as exc:  # pragma: no cover - safety
            return self._append_log({"error": str(exc)}, {
                "node": self.__class__.__name__,
                "status": "error",
                "error": str(exc),
            })

    def _append_log(self, result: Dict[str, Any], log: Dict[str, Any]) -> Dict[str, Any]:
        logs: List[Dict[str, Any]] = list(result.get("logs", []))
        logs.append(log)
        result["logs"] = logs
        return result
