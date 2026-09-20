from __future__ import annotations
import heapq
import itertools
import time
from packages.lch_core.models import LiveEvent, LiveEventType


PRIORITY = {
    LiveEventType.GIFT: 0,
    LiveEventType.FOLLOW: 1,
    LiveEventType.SHARE: 2,
    LiveEventType.COMMENT: 3,
    LiveEventType.JOIN: 4,
    LiveEventType.LIKE_BURST: 5,
}


class InteractionQueue:
    """Antrean event berprioritas: gift > follow > share > komentar."""

    def __init__(self) -> None:
        self._heap: list[tuple[int, int, LiveEvent]] = []
        self._counter = itertools.count()

    def push(self, event: LiveEvent) -> None:
        heapq.heappush(self._heap, (PRIORITY.get(event.type, 9), next(self._counter), event))

    def pop(self) -> LiveEvent | None:
        if not self._heap:
            return None
        return heapq.heappop(self._heap)[2]

    def __len__(self) -> int:
        return len(self._heap)
