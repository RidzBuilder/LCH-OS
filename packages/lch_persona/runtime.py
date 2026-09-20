from __future__ import annotations
from packages.lch_genesis.compiler import RuntimeBundle
from packages.lch_core.models import LiveEvent
from .dialogue import DialogueEngine
from .emotion import EmotionEngine
from .intents import classify_intent
from .memory import ShortTermMemory, ViewerMemoryStore
from .proactive import ProactiveEngine
from packages.lch_core.models import EmotionState


class PersonaRuntime:
    """Gabungan seluruh komponen otak untuk satu sesi live."""

    def __init__(self, bundle: RuntimeBundle) -> None:
        self.bundle = bundle
        self.dialogue = DialogueEngine(bundle.system_prompt)
        self.emotion = EmotionEngine()
        self.emotion_state = EmotionState()
        self.stm = ShortTermMemory()
        self.viewers = ViewerMemoryStore()
        self.proactive = ProactiveEngine()

    async def handle_event(self, event: LiveEvent) -> tuple[str, str]:
        """→ (intent, teks respons) atau ('ignored','') bila spam."""
        intent = classify_intent(event)
        if intent == "spam":
            return intent, ""
        self.viewers.recall(event.viewer_id, event.viewer_name)
        self.emotion_state = self.emotion.update(self.emotion_state, event.type)
        self.stm.add("user", f"{event.viewer_name}: {event.payload.get('text', '')}")
        text = await self.dialogue.reply(event, self.stm.as_messages(), self.emotion_state)
        self.stm.add("assistant", text)
        self.proactive.mark_activity()
        return intent, text

    def idle_hook(self, niche: str = "") -> str | None:
        hook = self.proactive.poke()
        return hook.format(niche=niche) if hook else None
