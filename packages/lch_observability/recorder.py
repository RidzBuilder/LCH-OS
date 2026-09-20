"""Rekam ringkasan sesi (utterance + event penting) untuk evaluasi persona."""
from __future__ import annotations
import json
from pathlib import Path


class SessionRecorder:
    def __init__(self, out_dir: str = "var/recordings") -> None:
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def append(self, session_id: str, record: dict) -> None:
        path = self.out_dir / f"{session_id}.jsonl"
        line = json.dumps(record, ensure_ascii=False, default=str) + chr(10)
        with path.open("a", encoding="utf-8") as f:
            f.write(line)
