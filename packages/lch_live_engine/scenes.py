from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Scene:
    name: str
    duration_s: int
    prompt_hint: str = ""


@dataclass
class SceneManager:
    """Rundown konten sesi. Contoh rundown affiliate live."""
    scenes: list[Scene] = field(default_factory=lambda: [
        Scene("opening", 120, "Sapa viewers, perkenalkan diri + disclosure AI"),
        Scene("demo_produk", 900, "Jelaskan produk, demo pemakaian, jawab tanya_produk"),
        Scene("faq_cta", 600, "FAQ + CTA soft-sell affiliate link"),
        Scene("closing", 120, "Ucapkan terima kasih, teaser live berikutnya"),
    ])
    _idx: int = 0

    def current(self) -> Scene:
        return self.scenes[min(self._idx, len(self.scenes) - 1)]

    def advance(self) -> Scene:
        self._idx = min(self._idx + 1, len(self.scenes) - 1)
        return self.current()
