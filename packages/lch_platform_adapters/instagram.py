
from .mock import MockAdapter


class InstagramAdapter(MockAdapter):
    """Stub adapter instagram — ganti dengan implementasi nyata.

    Referensi pola implementasi:
    - Event real-time: library ekosistem connector (cek ToS platform).
    - Stream keluar: RTMP/WebRTC ingest endpoint resmi.
    """
    platform = "instagram"
    account_ref = "instagram-account"
