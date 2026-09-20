# Deployment

## Lokal (dev)
Lihat README.md Quick Start.

## Staging/Produksi
1. Isi `infra/env/.env.production` (secret dari vault, BUKAN di repo).
2. `docker compose -f infra/docker-compose.yml --env-file infra/env/.env.production up -d`
3. Migrasi DB: `PYTHONPATH=. alembic upgrade head` (alembic: TODO Fase 1).
4. GPU worker (render avatar): node terpisah dengan NVIDIA runtime,
   Dockerfile.worker di-extend base `nvidia/cuda` + dependensi render.

## Checklist sebelum Go Live produksi
- [ ] PBOS webhook secret rotated
- [ ] Kredensial platform di vault (bukan env plaintext)
- [ ] Compliance strict mode ON + disclosure text terverifikasi
- [ ] Consent voice clone tervalidasi
- [ ] Adapter platform sesuai ToS terbaru
- [ ] Monitoring + alert (Prometheus/Grafana) aktif
