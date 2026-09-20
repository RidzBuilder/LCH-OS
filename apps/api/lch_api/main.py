from __future__ import annotations
import asyncio

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from packages.lch_core.config import get_settings
from packages.lch_core.events import EventBus
from packages.lch_core.errors import LchError
from packages.lch_genesis import ingestor
from packages.lch_genesis.compiler import compile_blueprint
from packages.lch_genesis.registry import registry
from .routers import creators, sessions
from .ws import ws_telemetry

app = FastAPI(title="LCH-OS API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

bus = EventBus()
app.state.bus = bus


@app.on_event("startup")
async def startup() -> None:
    app.state.bus_task = asyncio.create_task(bus.run())


@app.on_event("shutdown")
async def shutdown() -> None:
    app.state.bus_task.cancel()


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "env": get_settings().env}


@app.post("/v1/genesis/ingest", status_code=201)
async def genesis_ingest(request: Request) -> dict:
    raw = await request.body()
    sig = request.headers.get("X-PBOS-Signature", "")
    settings = get_settings()
    ingestor.verify_pbos_signature(raw, sig, settings.pbos_webhook_secret)
    bp = ingestor.parse_blueprint(raw)
    registry.save(bp)
    bundle = compile_blueprint(bp)
    return {
        "blueprint_id": bp.blueprint_id,
        "version": bp.version,
        "creator": bp.persona.name,
        "compiled": True,
        "platforms": bundle.behavior_limits["platforms"],
    }


@app.exception_handler(LchError)
async def lch_error_handler(request: Request, exc: LchError):  # noqa: ANN001
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=422,
        content={"error": exc.code, "message": exc.message},
    )


app.include_router(creators.router, prefix="/v1/creators", tags=["creators"])
app.include_router(sessions.router, prefix="/v1/sessions", tags=["sessions"])
app.include_router(ws_telemetry.router, prefix="/v1", tags=["telemetry"])
