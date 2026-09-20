
from .mock import MockAdapter


class TiktokAdapter(MockAdapter):
    """Stub adapter tiktok — ganti dengan implementasi nyata.

    Referensi pola implementasi:
    - Event real-time: library ekosistem connector (cek ToS platform).
    - Stream keluar: RTMP/WebRTC ingest endpoint resmi.
    """
    platform = "tiktok"
    account_ref = "tiktok-account"
