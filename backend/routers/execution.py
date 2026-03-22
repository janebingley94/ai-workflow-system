from __future__ import annotations

import json
from typing import AsyncGenerator

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from core.redis import get_redis

router = APIRouter(prefix="/execution", tags=["execution"])


@router.get("/{execution_id}/stream")
async def stream_execution(execution_id: str) -> StreamingResponse:
    redis = get_redis()
    channel = f"execution:{execution_id}"

    async def event_stream() -> AsyncGenerator[bytes, None]:
        pubsub = redis.pubsub()
        await pubsub.subscribe(channel)
        try:
            async for message in pubsub.listen():
                if message.get("type") != "message":
                    continue
                data = message.get("data")
                if data is None:
                    continue
                yield f"data: {data}\n\n".encode()
                try:
                    payload = json.loads(data)
                except json.JSONDecodeError:
                    payload = {}
                if payload.get("type") in {"done", "error"}:
                    break
        finally:
            await pubsub.unsubscribe(channel)
            await pubsub.close()
            await redis.close()

    try:
        return StreamingResponse(event_stream(), media_type="text/event-stream")
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc))
