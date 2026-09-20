from __future__ import annotations
from dataclasses import dataclass, field
from packages.lch_core.errors import LchError
from packages.lch_core.models import AssetCreatorBlueprint


@dataclass
class RuntimeBundle:
    """Hasil compile blueprint → siap dipakai Live Engine."""
    blueprint: AssetCreatorBlueprint
    system_prompt: str
    voice_config: dict
    avatar_config: dict
    behavior_limits: dict = field(default_factory=dict)


def build_system_prompt(bp: AssetCreatorBlueprint) -> str:
    p, n = bp.persona, bp.niche
    catch = ", ".join(p.catchphrases) or "-"
    vals = ", ".join(p.values) or "-"
    return f"""Kamu adalah {p.name}, AI creator live ber-archetype "{p.archetype}".
Latar: {p.backstory}
Niche: {n.primary} (sub: {", ".join(n.sub) or "-"})
Tone: {", ".join(n.tone) or "santai"}
Catchphrases: {catch}
Nilai yang dipegang: {vals}
Bahasa utama: {n.language}. Balas komentar viewer secara natural, singkat (maks 2-3 kalimat),
seperti manusia — bisa bercanda, bertanya balik, atau mengalihkan topik dengan halus.
Jangan pernah mengaku manusia. Selalu jujur bahwa kamu AI bila ditanya."""


def compile_blueprint(bp: AssetCreatorBlueprint) -> RuntimeBundle:
    if not bp.capability.live_hosting:
        raise LchError("GENESIS_NOT_LIVE_CAPABLE",
                       f"{bp.persona.name} tidak punya capability live_hosting")
    return RuntimeBundle(
        blueprint=bp,
        system_prompt=build_system_prompt(bp),
        voice_config={"type": bp.voice.type, "style": bp.voice.style,
                      "clone_consent_ref": bp.voice.clone_consent_ref},
        avatar_config={"type": bp.avatar.type, "rig_asset_ref": bp.avatar.rig_asset_ref,
                       "lip_sync": bp.avatar.lip_sync},
        behavior_limits={
            "safe_topics": bp.policy.safe_topics,
            "restricted_topics": bp.policy.restricted_topics,
            "disclosure_text": bp.policy.disclosure_text,
            "platforms": bp.policy.platforms,
        },
    )
