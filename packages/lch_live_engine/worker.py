"""Worker entrypoint: konsumsi perintah session.control dari antrean (Redis/Celery).

MVP: CLI dev — jalankan sesi dummy dengan adapter MockAdapter.

Produksi:
    celery -A packages.lch_live_engine.worker worker -Q live -c 4
"""
from __future__ import annotations
import asyncio

from packages.lch_core.events import EventBus
from packages.lch_genesis.compiler import compile_blueprint
from packages.lch_genesis.registry import registry
from packages.lch_live_engine.session_loop import SessionLoop
from packages.lch_platform_adapters.mock import MockAdapter


async def main() -> None:
    bus = EventBus()
    consumer = asyncio.create_task(bus.run())

    bp = registry.get("demo-creator")  # seed: python scripts/seed_demo.py
    if bp is None:
        print("Jalankan dulu: python scripts/seed_demo.py")
        return
    loop = SessionLoop(compile_blueprint(bp), MockAdapter(), bus)
    await loop.run()


if __name__ == "__main__":
    asyncio.run(main())
