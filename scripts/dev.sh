#!/usr/bin/env bash
# Bootstrap dev lokal: infra + api + worker + dashboard
set -e
docker compose -f infra/docker-compose.yml up -d postgres redis
cd apps/api && pip install -r requirements.txt && cd ../..
(cd apps/dashboard && npm install)
echo "Jalankan terpisah di 3 terminal:"
echo "  1) uvicorn lch_api.main:app --reload --port 8000   (dari root, PYTHONPATH=.)"
echo "  2) python -m packages.lch_live_engine.worker"
echo "  3) cd apps/dashboard && npm run dev"
