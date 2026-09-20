# LCH-OS — Live Creator Hub Operating System

> **Universe AI Agent** yang mengeksekusi **Asset AI Creator Live** (hasil genesis dari PBOS)
> menjadi host live interaktif yang berperilaku *seperti human creator*, lintas platform.

LCH-OS adalah lapisan operasional (execution & orchestration) di atas **PBOS (Persona Blueprint Operating System)**.
PBOS bertugas sebagai *genesis*: menciptakan blueprint AI Creator berdasarkan tipe
(`content_creator`, `affiliate_creator`, `live_creator`) dan niche-nya.
LCH-OS mengambil blueprint tersebut, membangun seluruh aset runtime (otak persona, suara, avatar,
memori, perilaku interaktif), lalu menjalankannya sebagai **live host** di TikTok Live, YouTube Live,
Instagram Live, Twitch, Shopee Live, dll.

## Arsitektur Singkat

```
PBOS (Genesis) → Asset AI Creator (blueprint JSON) → LCH-OS:
  Genesis Ingestor → Persona Runtime → Live Engine → Platform Adapters
  Asset Pipeline (TTS/voice-clone/avatar) • Compliance & Safety • Observability
  Orchestrator (FastAPI + worker) • Dashboard (React)
```

## Struktur Monorepo

```
lch-os/
├── apps/
│   ├── api/                 # REST/WS API utama (FastAPI)
│   └── dashboard/           # UI operator (React + Vite + TS)
├── packages/
│   ├── lch_core/            # Domain model, event bus, config, errors
│   ├── lch_genesis/         # Ingest & validasi Asset AI Creator dari PBOS
│   ├── lch_persona/         # Otak persona: LLM dialogue, memori, emosi, proaktif
│   ├── lch_live_engine/     # Loop sesi live: event→respons→render→stream
│   ├── lch_asset_pipeline/  # TTS/voice-clone, avatar, lip-sync, rendering
│   ├── lch_platform_adapters/ # TikTok, YouTube, Instagram, Twitch, Shopee, dll
│   └── lch_observability/   # Logging, metrics, recording sesi
├── infra/                   # docker-compose, env, nginx
├── scripts/                 # Bootstrap, seed, dev helper
└── docs/                    # Arsitektur detail, integrasi PBOS, compliance
```

## Quick Start (Local Dev)

```bash
# 1. Prasyarat: Docker, Docker Compose, Python 3.11+, Node 20+
cp infra/env/.env.example infra/env/.env.development

# 2. Jalankan infrastruktur (Postgres, Redis)
docker compose -f infra/docker-compose.yml up -d postgres redis

# 3. Jalankan API
cd apps/api && python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn lch_api.main:app --reload --port 8000

# 4. Jalankan worker live engine
python -m packages.lch_live_engine.worker

# 5. Jalankan dashboard
cd apps/dashboard && npm install && npm run dev
```

Dashboard: http://localhost:5173 • API docs: http://localhost:8000/docs

## Cara Kerja Singkat

1. **Genesis**: kirim Asset AI Creator dari PBOS ke `POST /v1/genesis/ingest`.
2. **Compile**: LCH-OS meng-compile blueprint menjadi runtime bundle (persona brain + voice + avatar preset).
3. **Go Live**: operator memanggil `POST /v1/sessions` → Live Engine membangun loop interaktif:
   `komentar/gift/follow masuk → persona memproses (emosi+memori+niat) → jawaban + aksi
   → TTS → avatar/lip-sync → dikirim ke platform via adapter`.
4. **Supervisi**: dashboard memantau sesi real-time; Compliance Layer memoderasi output sebelum tayang.

## Status

Fondasi arsitektur (scaffold production-ready). Lihat `docs/ROADMAP.md` untuk tahapan implementasi penuh.

## Lisensi & Compliance

Penggunaan live AI host harus tunduk pada Terms of Service masing-masing platform.
Selalu aktifkan disclosure AI & labeling sesuai regulasi (lihat `docs/COMPLIANCE.md`).
