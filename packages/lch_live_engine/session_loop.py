from __future__ import annotations
import asyncio
import uuid
from datetime import datetime
from typing import AsyncIterator

from packages.lch_core.events import EventBus
from packages.lch_core.models import LiveEvent, LiveSession, SessionState, Utterance
from packages.lch_genesis.compiler import RuntimeBundle
from packages.lch_persona.runtime import PersonaRuntime
from packages.lch_live_engine.queue import InteractionQueue
from packages.lch_live_engine.planner import ResponsePlanner
from packages.lch_live_engine.scenes import SceneManager
from packages.lch_asset_pipeline.pipeline import AssetPipeline
from packages.lch_platform_adapters.base import BasePlatformAdapter
from packages.lch_compliance.gate import ComplianceGate


class SessionLoop:
    """Jantung satu sesi live. Satu instance = satu sesi = satu thread event."""

    def __init__(self, bundle: RuntimeBundle, adapter: BasePlatformAdapter,
                 bus: EventBus, asset_pipeline: AssetPipeline | None = None) -> None:
        self.session = LiveSession(
            id=str(uuid.uuid4()),
            creator_id=bundle.blueprint.blueprint_id,
            platform=adapter.platform,
            account_ref=adapter.account_ref,
            title=f"{bundle.blueprint.persona.name} Live",
        )
        self.persona = PersonaRuntime(bundle)
        self.adapter = adapter
        self.bus = bus
        self.pipeline = asset_pipeline or AssetPipeline(bundle)
        self.compliance = ComplianceGate(bundle)
        self.queue = InteractionQueue()
        self.planner = ResponsePlanner()
        self.scenes = SceneManager()
        self._stop = asyncio.Event()

    async def run(self) -> None:
        await self._transition(SessionState.WARMING)
        await self.adapter.connect(self.session)
        await self.bus.publish("session.control",
                               {"session_id": self.session.id, "cmd": "start"})

        # Buka disclosure wajib di awal sesi
        disclosure = self.compliance.disclosure_text()
        await self._speak(disclosure, intent="disclosure")

        await self._transition(SessionState.LIVE)
        reader = asyncio.create_task(self._pump_events())
        idle = asyncio.create_task(self._idle_watcher())
        try:
            while not self._stop.is_set():
                event = self.queue.pop()
                if event is None:
                    await asyncio.sleep(0.1)
                    continue
                await self._handle(event)
        finally:
            idle.cancel()
            reader.cancel()
            await self.adapter.disconnect()
            await self._transition(SessionState.ENDED)

    # ---- internals ----
    async def _pump_events(self) -> None:
        async for event in self.adapter.read_events():
            if self._stop.is_set():
                break
            await self.bus.publish("live.event", event.model_dump())
            self.queue.push(event)

    async def _handle(self, event: LiveEvent) -> None:
        action = self.planner.plan(event)
        if action == "ignore":
            return
        intent, text = await self.persona.handle_event(event)
        if not text:
            return
        await self._speak(text, intent=intent)

    async def _speak(self, text: str, intent: str) -> None:
        verdict = self.compliance.check_output(text)
        if verdict.blocked:
            await self.bus.publish("compliance.violation",
                                   {"session_id": self.session.id, "reason": verdict.reason,
                                    "original": text})
            if verdict.redacted:
                text = verdict.redacted
            else:
                return
        utterance = Utterance(session_id=self.session.id, text=text, intent=intent,
                              emotion=self.persona.emotion_state)
        media = await self.pipeline.render(text, self.persona.emotion_state)
        await self.adapter.send_stream(media)
        await self.bus.publish("live.utterance", utterance.model_dump())

    async def _idle_watcher(self) -> None:
        niche = self.persona.bundle.blueprint.niche.primary
        while True:
            await asyncio.sleep(5)
            hook = self.persona.idle_hook(niche)
            if hook and self.session.state == SessionState.LIVE:
                await self._speak(hook, intent="proactive")

    async def _transition(self, state: SessionState) -> None:
        self.session.state = state
        if state == SessionState.LIVE:
            self.session.started_at = datetime.utcnow()
        await self.bus.publish("persona.state",
                               {"session_id": self.session.id, "state": state.value})

    # ---- kontrol operator ----
    def pause(self) -> None:
        self.session.state = SessionState.PAUSED

    def resume(self) -> None:
        self.session.state = SessionState.LIVE

    def stop(self) -> None:
        self._stop.set()
