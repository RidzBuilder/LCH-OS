# Roadmap LCH-OS

## Fase 0 — Fondasi (repo ini)
- [x] Struktur monorepo + domain model + event bus + config
- [x] Genesis ingestor + compiler (blueprint → RuntimeBundle)
- [x] Persona runtime (dialogue, memori, emosi, proaktif)
- [x] Live engine state machine + interaction queue + scene/rundown
- [x] Asset pipeline interfaces (TTS, voice clone, avatar, mixer)
- [x] Platform adapter stubs (TikTok/YouTube/Instagram/Twitch/Shopee)
- [x] Compliance gate + observability scaffolding
- [x] Dashboard skeleton + API + docker-compose

## Fase 1 — MVP Satu Platform
- [ ] Adapter TikTok LIVE full (event read + stream send) via ekosistem connector
- [ ] TTS provider nyata (ElevenLabs/Azure) + avatar Live2D renderer
- [ ] Sesi live end-to-end di staging account, 1 AI creator, 1 jam
- [ ] Dashboard monitoring real-time (event feed, latency, violation)

## Fase 2 — Human-likeness
- [ ] Long-term memory viewer + greeting ulang viewer lama
- [ ] Emosi visual di avatar (ekspresi) terikat state emosi persona
- [ ] Proactive engine v2 (trivia, poll, challenge komentar)
- [ ] Latency < 2.5s (TTS cache + predictive rendering)

## Fase 3 — Skala & Multi-Platform
- [ ] Multi-akun multi-platform scheduler
- [ ] Affiliate engine: katalog produk, deep-link, tracking konversi
- [ ] Clipper otomatis (highlight → short video) untuk creator content
- [ ] Evaluasi kualitas persona (scorecard dari recording + metrik engagement)

## Fase 4 — Ekosistem Universe
- [ ] Marketplace creator: PBOS genesis → LCH-OS compile → sewa host live
- [ ] API publik (tiered), webhook event untuk third-party
- [ ] Self-healing: auto-recovery adapter, failover stream
