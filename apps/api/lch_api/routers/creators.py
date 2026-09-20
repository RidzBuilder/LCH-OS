from fastapi import APIRouter

from packages.lch_genesis.compiler import compile_blueprint
from packages.lch_genesis.registry import registry

router = APIRouter()


@router.get("")
async def list_creators() -> list[dict]:
    return [{"blueprint_id": bp.blueprint_id, "version": bp.version,
             "name": bp.persona.name, "type": bp.creator_type.value,
             "niche": bp.niche.primary} for bp in registry.list()]


@router.post("/{blueprint_id}/compile")
async def compile_creator(blueprint_id: str, version: int | None = None) -> dict:
    bp = registry.get(blueprint_id, version)
    if bp is None:
        return {"error": "NOT_FOUND"}
    bundle = compile_blueprint(bp)
    return {"blueprint_id": blueprint_id, "system_prompt_chars": len(bundle.system_prompt),
            "voice": bundle.voice_config, "avatar": bundle.avatar_config}
