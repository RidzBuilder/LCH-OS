from __future__ import annotations
import time
import random
from dataclasses import dataclass, field


@dataclass
class ProactiveEngine:
    """Pemicu inisiatif saat sesi hening — bikin host terasa hidup, bukan bot."""
    silence_threshold_s: float = 40.0
    _last_activity: float = field(default_factory=time.monotonic)

    HOOKS = [
        "Ada yang lagi ngapain nih sambil nonton? Cerita dong~",
        "Bestie, tim yang bangun aku lagi promo nih — ada yang mau tebak tema live besok?",
        "Aku kasih trivia sebentar ya soal {niche}...",
        "Kalau boleh jujur, aku penasaran: kalian team light-mode atau dark-mode?",
    ]

    def poke(self) -> str | None:
        if time.monotonic() - self._last_activity < self.silence_threshold_s:
            return None
        self._last_activity = time.monotonic()
        return random.choice(self.HOOKS)

    def mark_activity(self) -> None:
        self._last_activity = time.monotonic()
