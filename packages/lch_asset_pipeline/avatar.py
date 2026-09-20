from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol

from packages.lch_core.models import EmotionState


@dataclass
class MediaFrame:
    """Satu frame/paket media siap stream (audio+video muxed atau instruksi avatar)."""
    kind: str
    data: bytes = b""
    params: dict | None = None
    duration_ms: int = 0


class AvatarRenderer(Protocol):
    async def render_speech(self, audio: bytes, emotion: EmotionState) -> MediaFrame: ...
    async def render_idle(self, emotion: EmotionState) -> MediaFrame: ...


class Live2DRenderer:
    """Mode 1: rig Live2D — kirim parameter (mulut, ekspresi) ke renderer lokal."""

    async def render_speech(self, audio: bytes, emotion: EmotionState) -> MediaFrame:
        return MediaFrame(kind="avatar_params",
                          params={"motion": "talk", "expression": emotion.label,
                                  "audio_len": len(audio)})

    async def render_idle(self, emotion: EmotionState) -> MediaFrame:
        return MediaFrame(kind="avatar_params",
                          params={"motion": "idle", "expression": emotion.label})


class TalkingHeadRenderer:
    """Mode 2: talking-head per kalimat (wav2lip-style) di GPU worker."""

    async def render_speech(self, audio: bytes, emotion: EmotionState) -> MediaFrame:
        return MediaFrame(kind="muxed_clip", data=audio, duration_ms=3000)


def build_renderer(avatar_type: str) -> AvatarRenderer:
    return TalkingHeadRenderer() if avatar_type == "talking_head" else Live2DRenderer()
