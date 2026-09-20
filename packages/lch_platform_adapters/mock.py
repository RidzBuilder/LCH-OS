from __future__ import annotations
import asyncio
import uuid
from datetime import datetime
from typing import AsyncIterator

from packages.lch_core.models import LiveEvent, LiveEventType, LiveSession
from packages.lch_asset_pipeline.avatar import MediaFrame


class MockAdapter:
    """Adapter dummy untuk dev: generate komentar berkala, cetak media yang keluar."""

    platform = "mock"
    account_ref = "mock-account"

    async def authenticate(self, account):  # noqa: ANN001
        return None

    async def connect(self, session: LiveSession) -> None:
        print(f"[mock] connected session={session.id}")

    async def read_events(self) -> AsyncIterator[LiveEvent]:
        samples = [
            ("viewer1", "halo kak!"),
            ("viewer2", "harga produknya berapa?"),
            ("viewer3", "rose 1x"),
            ("viewer4", "bot kan?"),
            ("viewer5", "info link dong"),
        ]
        i = 0
        while True:
            await asyncio.sleep(3)
            name, text = samples[i % len(samples)]
            i += 1
            yield LiveEvent(
                id=str(uuid.uuid4()), session_id="mock",
                type=LiveEventType.COMMENT if "rose" not in text else LiveEventType.GIFT,
                viewer_id=name, viewer_name=name,
                payload={"text": text, "gift_name": "rose"} if "rose" in text else {"text": text},
                received_at=datetime.utcnow(),
            )

    async def send_stream(self, media: MediaFrame) -> None:
        print(f"[mock] streaming: {media.kind} {media.params or len(media.data)}b")

    async def publish_metadata(self, title: str, tags: list[str]) -> None:
        print(f"[mock] metadata: {title} {tags}")

    async def disconnect(self) -> None:
        print("[mock] disconnected")
