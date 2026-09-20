
from .mock import MockAdapter


class YoutubeAdapter(MockAdapter):
    """Stub adapter youtube — ganti dengan implementasi nyata.

    Referensi pola implementasi:
    - Event real-time: library ekosistem connector (cek ToS platform).
    - Stream keluar: RTMP/WebRTC ingest endpoint resmi.
    """
    platform = "youtube"
    account_ref = "youtube-account"
