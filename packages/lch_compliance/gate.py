from __future__ import annotations
import re
import time
from dataclasses import dataclass

from packages.lch_genesis.compiler import RuntimeBundle


BANNED_PATTERNS = [
    r"obat (paling )?(ampuh|manjur)",      # klaim medis
    r"dijamin (sembuh|langsing)",
    r"investasi (pasti )?untung",
]


@dataclass
class Verdict:
    blocked: bool
    reason: str = ""
    redacted: str | None = None


class ComplianceGate:
    def __init__(self, bundle: RuntimeBundle) -> None:
        self.policy = bundle.blueprint.policy
        self._last_disclosure = 0.0

    def check_output(self, text: str) -> Verdict:
        for pattern in BANNED_PATTERNS:
            if re.search(pattern, text.lower()):
                return Verdict(blocked=True, reason=f"pola_terlarang:{pattern}")
        return Verdict(blocked=False)

    def disclosure_text(self) -> str:
        self._last_disclosure = time.monotonic()
        return self.policy.disclosure_text

    def need_periodic_disclosure(self, interval_minutes: int) -> bool:
        return (time.monotonic() - self._last_disclosure) >= interval_minutes * 60
