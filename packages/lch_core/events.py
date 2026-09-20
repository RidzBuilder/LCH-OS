from __future__ import annotations
import asyncio
import json
from typing import Any, AsyncIterator, Callable, Coroutine


Handler = Callable[[dict[str, Any]], Coroutine[Any, Any, None]]


class EventBus:
    """Event bus in-memory untuk dev/test.

    Produksi: ganti dengan Redis Streams (XADD/XREADGROUP); antarmuka sama.
    Topik: live.event, live.utterance, persona.state, compliance.violation,
    session.control, asset.ready
    """

    def __init__(self) -> None:
        self._topics: dict[str, list[Handler]] = {}
        self._queue: asyncio.Queue[tuple[str, dict[str, Any]]] = asyncio.Queue()

    def subscribe(self, topic: str, handler: Handler) -> None:
        self._topics.setdefault(topic, []).append(handler)

    async def publish(self, topic: str, payload: dict[str, Any]) -> None:
        await self._queue.put((topic, payload))

    async def run(self) -> None:  # background consumer loop
        while True:
            topic, payload = await self._queue.get()
            for handler in self._topics.get(topic, []):
                try:
                    await handler(payload)
                except Exception:  # jangan biarkan satu handler mematikan bus
                    pass


def encode(payload: dict) -> bytes:
    return json.dumps(payload, ensure_ascii=False, default=str).encode("utf-8")
