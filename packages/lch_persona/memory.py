from __future__ import annotations
from collections import deque
from dataclasses import dataclass, field


@dataclass
class ViewerProfile:
    viewer_id: str
    name: str
    mentions: int = 0
    notes: list[str] = field(default_factory=list)  # "suka produk X", "pernah nanya harga"


class ShortTermMemory:
    """Buffer konteks sesi berjalan (ringkas)."""

    def __init__(self, max_items: int = 30) -> None:
        self.turns: deque[dict] = deque(maxlen=max_items)

    def add(self, role: str, content: str) -> None:
        self.turns.append({"role": role, "content": content})

    def as_messages(self) -> list[dict]:
        return list(self.turns)


class ViewerMemoryStore:
    """Long-term memory viewer. MVP in-memory; produksi: pgvector dengan embedding."""

    def __init__(self) -> None:
        self._viewers: dict[str, ViewerProfile] = {}

    def recall(self, viewer_id: str, name: str) -> ViewerProfile:
        v = self._viewers.setdefault(viewer_id, ViewerProfile(viewer_id=viewer_id, name=name))
        v.mentions += 1
        return v

    def note(self, viewer_id: str, fact: str) -> None:
        if viewer_id in self._viewers:
            self._viewers[viewer_id].notes.append(fact)
