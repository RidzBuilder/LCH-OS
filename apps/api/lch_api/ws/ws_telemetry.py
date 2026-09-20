import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


@router.websocket("/sessions/{session_id}/stream")
async def telemetry(ws: WebSocket, session_id: str) -> None:
    """Telemetri real-time: live.event, live.utterance, persona.state, compliance.violation."""
    await ws.accept()
    queue: asyncio.Queue = asyncio.Queue()
    bus = ws.app.state.bus  # type: ignore[attr-defined]
    bus.subscribe("live.event", lambda p: queue.put(p))
    bus.subscribe("live.utterance", lambda p: queue.put(p))
    bus.subscribe("compliance.violation", lambda p: queue.put(p))
    try:
        while True:
            payload = await queue.get()
            await ws.send_text(json.dumps(payload, ensure_ascii=False, default=str))
    except WebSocketDisconnect:
        pass
