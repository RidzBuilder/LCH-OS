from __future__ import annotations
import hashlib
from typing import Protocol

from packages.lch_core.config import get_settings


class TTSProvider(Protocol):
    async def synthesize(self, text: str, voice: str, style: str) -> bytes: ...


class ElevenLabsTTS:
    async def synthesize(self, text: str, voice: str, style: str) -> bytes:
        return b""


class LocalXTTS:
    async def synthesize(self, text: str, voice: str, style: str) -> bytes:
        return b""


def cache_key(text: str, voice: str, style: str) -> str:
    return hashlib.sha256(f"{voice}|{style}|{text}".encode()).hexdigest()


class TTSCache:
    """Cache audio per (voice, style, text) — kunci latency < 2.5s."""

    def __init__(self) -> None:
        self._store: dict[str, bytes] = {}

    async def get_or_create(self, provider: TTSProvider, text: str,
                            voice: str, style: str) -> bytes:
        key = cache_key(text, voice, style)
        if key not in self._store:
            self._store[key] = await provider.synthesize(text, voice, style)
        return self._store[key]


def default_provider() -> TTSProvider:
    return ElevenLabsTTS() if get_settings().tts_provider == "elevenlabs" else LocalXTTS()
