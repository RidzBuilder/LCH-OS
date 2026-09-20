
from .mock import MockAdapter


class TwitchAdapter(MockAdapter):
    """Stub adapter twitch — ganti dengan implementasi nyata.

    Referensi pola implementasi:
    - Event real-time: library ekosistem connector (cek ToS platform).
    - Stream keluar: RTMP/WebRTC ingest endpoint resmi.
    """
    platform = "twitch"
    account_ref = "twitch-account"
