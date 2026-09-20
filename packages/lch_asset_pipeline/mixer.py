from __future__ import annotations
from .avatar import MediaFrame


class StreamMixer:
    """Mux audio+video lalu kirim ke ingest point (RTMP/WebRTC) via adapter."""

    async def push(self, frame: MediaFrame) -> MediaFrame:
        # Produksi: ffmpeg mux ke rtmp://..., atau WebRTC track.
        return frame
