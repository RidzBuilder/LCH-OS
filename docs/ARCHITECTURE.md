# LCH-OS — Arsitektur Fundamental

## 1. Prinsip Desain

1. **PBOS = Genesis, LCH-OS = Eksekusi.** PBOS tidak pernah live; ia menghasilkan *blueprint*.
   LCH-OS mem-materialisasi blueprint menjadi runtime host live.
2. **Human-like by design, bukan sekadar bot.** Setiap respons melewati pipeline:
   *perception → emosi → memori → niat → dialogue → suara → avatar → aksi* — mirip loop kognitif manusia.
3. **Adapter-agnostic.** Semua platform live (TikTok, YT, IG, Twitch, Shopee…) diakses lewat
   antarmuka `BasePlatformAdapter`. Engine inti tidak tahu detail platform.
4. **Compliance as a gate, bukan afterthought.** Output melewati `ComplianceGate` sebelum dirender.
5. **Event-driven & observable.** Semua kejadian adalah event di `EventBus`; terekam untuk evaluasi.

## 2. Modul

### 2.1 lch_core
- `models.py`: `AssetCreatorBlueprint`, `PersonaProfile`, `LiveSession`, `LiveEvent`, `Utterance`, dll.
- `events.py`: `EventBus` (Redis Streams / in-memory dev), topik: `live.event`, `live.utterance`,
  `persona.state`, `compliance.violation`, `session.control`.
- `config.py`: Pydantic Settings (env-based, multi-environment).
- Pola: semua antarmuka pakai `Protocol` (structural typing) → mudah di-mock untuk test.

### 2.2 lch_genesis
- `ingestor.py`: menerima blueprint PBOS → validasi skema (Pydantic) → normalisasi → registry.
- `compiler.py`: meng-compile blueprint menjadi `RuntimeBundle`:
  - persona prompt + policy,
  - konfigurasi suara (voice_id, style),
  - preset avatar (rig Live2D / video loop / talking-head),
  - batas perilaku (safe-topics, disclosure text, jam tayang).
- `registry.py`: CRUD katalog AI Creator (versi blueprint, status compile).

### 2.3 lch_persona (Otak)
- `dialogue.py`: LLM client (pluggable: OpenAI/Anthropic/local) dengan system prompt hasil compile.
- `memory.py`: short-term (buffer sesi) + long-term (viewer store; produksi pgvector) — ingat viewer,
  running joke, topik yang pernah dibahas.
- `emotion.py`: state emosi (valence/arousal) dipengaruhi event (gift, sentiment komentar).
- `proactive.py`: pemicu inisiatif — "sudah 40 detik hening → ajak ngobrol / trivia / teasing".
- `intents.py`: klasifikasi niat komentar (tanya_produk, sapaan, pujian, spam, troll, ngobrol).

### 2.4 lch_live_engine (Jantung)
Loop sesi (`session_loop.py`), state machine:
```
CREATED → WARMING → LIVE → INTERACTING ⇄ PAUSED → COOLDOWN → ENDED
```
- Event masuk (komentar, gift, follow, share) dari adapter → `InteractionQueue`
  (prioritas: gift > follow > komentar).
- `ResponsePlanner`: memilih strategi (balas langsung, tunda, abaikan spam, trigger gimmick gift).
- Latency budget: komentar→suara keluar target < 2.5 detik (TTS caching + avatar predictive idle).
- `SceneManager`: rundown konten (mis. sesi affiliate: intro → demo produk → FAQ → CTA → closing).

### 2.5 lch_asset_pipeline
- `tts.py`: interface `TTSProvider` (ElevenLabs, Azure, local XTTS); cache per (text, voice, style).
- `voice_clone.py`: onboarding clone suara (consent-verified) → voice_id.
- `avatar.py`: tiga mode render:
  1. **Live2D/VTuber rig** (parameter WebSocket → renderer),
  2. **Talking-head** (wav2lip-style, per kalimat → animasi),
  3. **Video-presence** (avatar 3D / sprite + lip-sync).
- `mixer.py`: mux audio+video, kirim ke ingest point (RTMP/WebRTC) platform.
- Proses berat berjalan async di worker dengan antrean Redis.

### 2.6 lch_platform_adapters
`BasePlatformAdapter` (interface):
```python
class BasePlatformAdapter(Protocol):
    async def authenticate(self, account: PlatformAccount) -> AuthSession: ...
    async def connect(self, session: LiveSession) -> ConnectionHandle: ...
    async def read_events(self) -> AsyncIterator[LiveEvent]: ...      # komentar/gift/follow
    async def send_stream(self, media: MediaFrame | MediaClip) -> None: ...
    async def publish_metadata(self, title: str, tags: list[str]) -> None: ...
    async def disconnect(self) -> None: ...
```
Implementasi stub + pola: `tiktok`, `youtube`, `instagram`, `twitch`, `shopee`.
Catatan: gunakan API resmi/partner bila tersedia; untuk event real-time gunakan
library ekosistem (mis. TikTok Live Connector) — sesuaikan dengan ToS platform.

### 2.7 Compliance & Safety (lintas modul)
- `moderation.py`: filter input (spam/toxic) & output (klaim berbahaya, kata terlarang platform).
- `disclosure.py`: sisipkan disclosure "AI host" berkala & watermark/metadata labeling.
- `policy.py`: aturan per-niche & per-platform (jam tayang, larangan konten, batas interaksi).
- Setiap pelanggaran → event `compliance.violation` + tindakan (redaksi, ganti topik, pause, stop).

### 2.8 lch_observability
- Structured logging (JSON), trace per sesi (`session_id` di semua log).
- Metrics Prometheus: event rate, response latency, violation count, uptime sesi.
- `recorder.py`: rekaman ringkasan sesi untuk evaluasi kualitas persona.

## 3. Alur Data End-to-End (satu komentar)

```
Viewer komentar di TikTok
  → TikTokAdapter.read_events() → LiveEvent(comment)
  → EventBus "live.event"
  → LiveEngine: moderasi input → intent classify → prioritas queue
  → PersonaRuntime: memori viewer + emosi + konteks rundown → draft utterance
  → ComplianceGate: moderasi output → (lolos)
  → TTS (cache?) → Avatar render (lip-sync) → MediaFrame
  → TikTokAdapter.send_stream() → tayang
  → EventBus "live.utterance" (tersimpan untuk analitik)
```

## 4. Deployment Topology

- `api` (FastAPI): REST + WebSocket dashboard.
- `worker` (Python): live-engine + asset pipeline (GPU untuk avatar/render).
- `postgres` (+pgvector), `redis` (queue + event bus dev), `nginx` (reverse proxy).
- Multi-akun multi-platform: satu worker pool, sesi dijadwalkan orchestrator.
- Skala horizontal: worker stateless, state sesi di Redis/DB.
