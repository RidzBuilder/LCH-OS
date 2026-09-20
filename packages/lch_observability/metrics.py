"""Metrics Prometheus sederhana. Produksi: gunakan prometheus_client."""
from collections import defaultdict


class Metrics:
    def __init__(self) -> None:
        self.counters: dict[str, int] = defaultdict(int)

    def inc(self, name: str, amount: int = 1) -> None:
        self.counters[name] += amount

    def snapshot(self) -> dict[str, int]:
        return dict(self.counters)


metrics = Metrics()
