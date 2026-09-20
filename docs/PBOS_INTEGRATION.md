# Integrasi PBOS ↔ LCH-OS

## Kontrak: Asset AI Creator (Blueprint)

PBOS mengirim blueprint via HTTP webhook (`POST /v1/genesis/ingest`) dengan header
`X-PBOS-Signature` (HMAC-SHA256, shared secret).

```json
{
  "blueprint_id": "pbos-creator-01J8Z",
  "version": 3,
  "creator_type": "live_creator",
  "niche": {
    "primary": "beauty_skincare",
    "sub": ["affiliate_tokopedia", "review_jujur"],
    "language": "id-ID",
    "tone": ["ramah", "ceria", "sedikit_cringe_sadar_diri"]
  },
  "persona": {
    "name": "Kak Rara",
    "age_persona": 24,
    "archetype": "kakak_pertemanan",
    "backstory": "Beauty enthusiast, jujur soal produk, suka ngobrol santai",
    "catchphrases": ["Bestiee~", "Jujur ya aku review"],
    "values": ["kejujuran_review", "no_hard_sell"]
  },
  "capability": {
    "live_hosting": true,
    "affiliate_selling": true,
    "content_clipper": false,
    "max_concurrent_sessions": 1
  },
  "voice": { "type": "cloned", "clone_consent_ref": "consent-123", "style": "energetic" },
  "avatar": { "type": "live2d", "rig_asset_ref": "s3://pbos-assets/rara-rig", "lip_sync": true },
  "policy": {
    "safe_topics": ["skincare", "makeup", "self_care"],
    "restricted_topics": ["klaim_medical"],
    "disclosure_text": "Aku AI host buatan tim kami — tapi obrolan tetap jujur!",
    "platforms": ["tiktok", "shopee"]
  },
  "monetization": {
    "affiliate_links": [{"platform": "tokopedia", "catalog_ref": "cat-77"}],
    "cta_style": "soft_sell"
  }
}
```

## API Surface LCH-OS (ringkasan)

| Method | Path | Fungsi |
|---|---|---|
| POST | `/v1/genesis/ingest` | Terima blueprint PBOS → validasi → registry |
| GET | `/v1/creators` | Daftar AI Creator tercompile |
| POST | `/v1/creators/{id}/compile` | Compile ulang blueprint → RuntimeBundle |
| POST | `/v1/sessions` | Mulai sesi live (creator_id, platform, akun, rundown) |
| GET | `/v1/sessions/{id}` | Status sesi + metrics |
| WS | `/v1/sessions/{id}/stream` | Telemetri real-time ke dashboard |
| POST | `/v1/sessions/{id}/control` | Perintah operator (pause/resume/stop/override bicara) |

## Error & Retry

- Ingest idempotent berdasarkan `blueprint_id + version`.
- Webhook PBOS: retry exponential backoff bila LCH-OS balas 5xx.
- Semua error normalisasi ke `LchError` (kode + pesan + retryable flag).
