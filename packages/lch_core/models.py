from __future__ import annotations
import enum
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field


# ---------- Blueprint dari PBOS ----------
class CreatorType(str, enum.Enum):
    CONTENT_CREATOR = "content_creator"
    AFFILIATE_CREATOR = "affiliate_creator"
    LIVE_CREATOR = "live_creator"


class Niche(BaseModel):
    primary: str
    sub: list[str] = Field(default_factory=list)
    language: str = "id-ID"
    tone: list[str] = Field(default_factory=list)


class PersonaProfile(BaseModel):
    name: str
    age_persona: int = 25
    archetype: str = "teman_ngobrol"
    backstory: str = ""
    catchphrases: list[str] = Field(default_factory=list)
    values: list[str] = Field(default_factory=list)


class Capability(BaseModel):
    live_hosting: bool = True
    affiliate_selling: bool = False
    content_clipper: bool = False
    max_concurrent_sessions: int = 1


class VoiceSpec(BaseModel):
    type: str = "generic"                 # generic | cloned
    clone_consent_ref: Optional[str] = None
    style: str = "natural"


class AvatarSpec(BaseModel):
    type: str = "live2d"                  # live2d | talking_head | video_presence
    rig_asset_ref: Optional[str] = None
    lip_sync: bool = True


class PolicySpec(BaseModel):
    safe_topics: list[str] = Field(default_factory=list)
    restricted_topics: list[str] = Field(default_factory=list)
    disclosure_text: str = "Aku AI host. Konten ini dihasilkan AI."
    platforms: list[str] = Field(default_factory=list)


class AssetCreatorBlueprint(BaseModel):
    blueprint_id: str
    version: int
    creator_type: CreatorType
    niche: Niche
    persona: PersonaProfile
    capability: Capability = Field(default_factory=Capability)
    voice: VoiceSpec = Field(default_factory=VoiceSpec)
    avatar: AvatarSpec = Field(default_factory=AvatarSpec)
    policy: PolicySpec = Field(default_factory=PolicySpec)
    monetization: dict[str, Any] = Field(default_factory=dict)


# ---------- Runtime ----------
class EmotionState(BaseModel):
    valence: float = 0.0      # -1 .. 1
    arousal: float = 0.5      #  0 .. 1
    label: str = "netral"


class LiveEventType(str, enum.Enum):
    COMMENT = "comment"
    GIFT = "gift"
    FOLLOW = "follow"
    SHARE = "share"
    LIKE_BURST = "like_burst"
    JOIN = "join"


class LiveEvent(BaseModel):
    id: str
    session_id: str
    type: LiveEventType
    viewer_id: str
    viewer_name: str
    payload: dict[str, Any] = Field(default_factory=dict)  # text, gift_name, value, dll
    received_at: datetime = Field(default_factory=datetime.utcnow)


class Utterance(BaseModel):
    session_id: str
    text: str
    emotion: EmotionState = Field(default_factory=EmotionState)
    intent: str = "chat"
    tts_audio_ref: Optional[str] = None
    avatar_clip_ref: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SessionState(str, enum.Enum):
    CREATED = "created"
    WARMING = "warming"
    LIVE = "live"
    INTERACTING = "interacting"
    PAUSED = "paused"
    COOLDOWN = "cooldown"
    ENDED = "ended"


class LiveSession(BaseModel):
    id: str
    creator_id: str
    platform: str
    account_ref: str
    title: str
    state: SessionState = SessionState.CREATED
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    metadata: dict[str, Any] = Field(default_factory=dict)
