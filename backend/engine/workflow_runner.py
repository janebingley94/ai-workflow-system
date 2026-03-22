from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict

from core.redis import get_redis
from engine.flow_parser import FlowParser


class WorkflowRunner:
    def __init__(self) -> None:
        self.parser = FlowParser()

    async def run(self, execution_id: str, flow_config: dict, input_payload: Any) -> None:
        redis = get_redis()
        channel = f"execution:{execution_id}"

        try:
            compiled = self.parser.parse(flow_config)
            initial_state = self._build_initial_state(input_payload)
            await self._publish(redis, channel, {"type": "start", "timestamp": self._now_iso()})

            result = await compiled.ainvoke(initial_state)
            await self._publish(
                redis,
                channel,
                {
                    "type": "done",
                    "timestamp": self._now_iso(),
                    "output": result,
                },
            )
        except Exception as exc:  # pragma: no cover
            await self._publish(
                redis,
                channel,
                {
                    "type": "error",
                    "timestamp": self._now_iso(),
                    "error": str(exc),
                },
            )
        finally:
            await redis.close()

    def _build_initial_state(self, input_payload: Any) -> Dict[str, Any]:
        if isinstance(input_payload, dict):
            return input_payload
        return {"input": input_payload}

    async def _publish(self, redis, channel: str, message: Dict[str, Any]) -> None:
        await redis.publish(channel, json.dumps(message))

    def _now_iso(self) -> str:
        return datetime.utcnow().isoformat() + "Z"


async def run_workflow_in_background(execution_id: str, flow_config: dict, input_payload: Any) -> None:
    runner = WorkflowRunner()
    await runner.run(execution_id, flow_config, input_payload)
