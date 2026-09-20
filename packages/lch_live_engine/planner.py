from __future__ import annotations
from packages.lch_core.models import LiveEvent


class ResponsePlanner:
    """Memutuskan: balas sekarang, gabung, tunda, atau abaikan."""

    def plan(self, event: LiveEvent) -> str:
        if event.type.value == "gift":
            return "react_gift"          # apresiasi + gimmick sesuai nilai gift
        if event.type.value == "follow":
            return "greet_follower"
        text = (event.payload.get("text") or "").lower()
        if len(text) < 2:
            return "ignore"
        return "reply"
