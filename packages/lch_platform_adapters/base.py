from __future__ import annotations
from dataclasses import dataclass
from typing import AsyncIterator, Protocol

from packages.lch_core.models import LiveEvent, LiveSession
from packages.lch_asset_pipeline.avatar import MediaFrame


@dataclass
class PlatformAccount:
    platform: str
    account_ref: str              # user_id / handle / stream key vault ref
    credentials_ref: str          # vault ref, JANGAN plaintext di repo


@dataclass
class AuthSession:
    access_token: str
    expires_at: float


class BasePlatformAdapter(Protocol):
    platform: str
    account_ref: str

    async def authenticate(self, account: PlatformAccount) -> AuthSession: ...
    async def connect(self, session: LiveSession) -> None: ...
    async def read_events(self) -> AsyncIterator[LiveEvent]: ...
    async def send_stream(self, media: MediaFrame) -> None: ...
    async def publish_metadata(self, title: str, tags: list[str]) -> None: ...
    async def disconnect(self) -> None: ...
