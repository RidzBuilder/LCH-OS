from __future__ import annotations
from packages.lch_core.models import AssetCreatorBlueprint


class CreatorRegistry:
    """Registry blueprint & runtime bundle. MVP: in-memory; produksi: tabel Postgres."""

    def __init__(self) -> None:
        self._blueprints: dict[str, AssetCreatorBlueprint] = {}

    def save(self, bp: AssetCreatorBlueprint) -> None:
        key = f"{bp.blueprint_id}@v{bp.version}"
        self._blueprints[key] = bp

    def get(self, blueprint_id: str, version: int | None = None) -> AssetCreatorBlueprint | None:
        if version is not None:
            return self._blueprints.get(f"{blueprint_id}@v{version}")
        candidates = [k for k in self._blueprints if k.startswith(f"{blueprint_id}@")]
        if not candidates:
            return None
        latest = max(candidates, key=lambda k: int(k.split("@v")[1]))
        return self._blueprints[latest]

    def list(self) -> list[AssetCreatorBlueprint]:
        return list(self._blueprints.values())


registry = CreatorRegistry()
