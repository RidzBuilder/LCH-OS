
from .mock import MockAdapter


class ShopeeAdapter(MockAdapter):
    """Stub adapter shopee — ganti dengan implementasi nyata.

    Referensi pola implementasi:
    - Event real-time: library ekosistem connector (cek ToS platform).
    - Stream keluar: RTMP/WebRTC ingest endpoint resmi.
    """
    platform = "shopee"
    account_ref = "shopee-account"
