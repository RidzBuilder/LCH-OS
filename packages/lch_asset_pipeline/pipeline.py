from __future__ import annotations
from packages.lch_genesis.compiler import RuntimeBundle
from packages.lch_core.models import EmotionState
from .avatar import MediaFrame, build_renderer
from .mixer import StreamMixer
from .tts import TTSCache, default_provider


class AssetPipeline:
    """Teks + emosi → media siap stream (TTS → avatar → mix)."""

    def __init__(self, bundle: RuntimeBundle) -> None:
        self.voice_cfg = bundle.voice_config
        self.renderer = build_renderer(bundle.avatar_config["type"])
        self.tts = TTSCache()
        self.provider = default_provider()
        self.mixer = StreamMixer()

    async def render(self, text: str, emotion: EmotionState) -> MediaFrame:
        voice = self.voice_cfg.get("clone_consent_ref") or "default"
        style = self.voice_cfg.get("style", "natural")
        audio = await self.tts.get_or_create(self.provider, text, voice, style)
        frame = await self.renderer.render_speech(audio, emotion)
        return await self.mixer.push(frame)
