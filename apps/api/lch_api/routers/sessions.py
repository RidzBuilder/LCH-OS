import uuid
from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter()
_sessions: dict[str, dict] = {}


class SessionCreate(BaseModel):
    blueprint_id: str
    platform: str
    account_ref: str
    title: str = "LCH Live Session"


@router.post("", status_code=201)
async def create_session(body: SessionCreate, request: Request) -> dict:
    session_id = str(uuid.uuid4())
    _sessions[session_id] = {**body.model_dump(), "id": session_id, "state": "created"}
    await request.app.state.bus.publish(
        "session.control", {"session_id": session_id, "cmd": "start", **body.model_dump()})
    return _sessions[session_id]


@router.get("/{session_id}")
async def get_session(session_id: str) -> dict:
    return _sessions.get(session_id, {"error": "NOT_FOUND"})


class SessionControl(BaseModel):
    cmd: str


@router.post("/{session_id}/control")
async def control_session(session_id: str, body: SessionControl, request: Request) -> dict:
    await request.app.state.bus.publish(
        "session.control", {"session_id": session_id, "cmd": body.cmd})
    if session_id in _sessions:
        _sessions[session_id]["state"] = body.cmd + "d"
    return {"session_id": session_id, "cmd": body.cmd, "ok": True}
