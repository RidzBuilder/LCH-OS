from packages.lch_core.models import EmotionState, LiveEventType


class EmotionEngine:
    """State emosi sederhana: valence (-1..1), arousal (0..1). Dipengaruhi event."""

    def update(self, state: EmotionState, event_type: LiveEventType,
               sentiment: float = 0.0) -> EmotionState:
        if event_type == LiveEventType.GIFT:
            state.valence = min(1.0, state.valence + 0.35)
            state.arousal = min(1.0, state.arousal + 0.3)
        elif event_type == LiveEventType.FOLLOW:
            state.valence = min(1.0, state.valence + 0.15)
        elif event_type == LiveEventType.COMMENT:
            state.valence = max(-1.0, min(1.0, state.valence + sentiment * 0.2))
        state.label = self._label(state)
        return state

    @staticmethod
    def _label(s: EmotionState) -> str:
        if s.valence > 0.4:
            return "senang"
        if s.valence < -0.3:
            return "sedih" if s.arousal < 0.5 else "kesal"
        return "netral"
