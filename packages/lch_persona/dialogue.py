from __future__ import annotations
from typing import Protocol

from packages.lch_core.config import get_settings
from packages.lch_core.models import EmotionState, LiveEvent


class LLMClient(Protocol):
    async def chat(self, system: str, messages: list[dict], model: str) -> str: ...


class OpenAICompatLLM:
    async def chat(self, system: str, messages: list[dict], model: str) -> str:
        # Produksi: panggil AsyncOpenAI / AsyncAnthropic sesuai config.
        return "(stub LLM response)"


class DialogueEngine:
    def __init__(self, system_prompt: str, llm: LLMClient | None = None) -> None:
        self.system_prompt = system_prompt
        self.llm = llm or OpenAICompatLLM()

    async def reply(self, event: LiveEvent, context: list[dict],
                    emotion: EmotionState) -> str:
        mood = f"[suasana: {emotion.label}]"
        messages = context + [{"role": "user",
                               "content": f"{mood} {event.viewer_name}: {event.payload.get('text', '')}"}]
        return await self.llm.chat(self.system_prompt, messages,
                                   get_settings().default_llm_model)
