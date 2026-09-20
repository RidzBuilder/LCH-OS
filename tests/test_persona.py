from packages.lch_core.models import EmotionState, LiveEvent, LiveEventType
from packages.lch_persona.emotion import EmotionEngine
from packages.lch_persona.intents import classify_intent


def ev(text: str, etype: LiveEventType = LiveEventType.COMMENT) -> LiveEvent:
    return LiveEvent(id="1", session_id="s", type=etype, viewer_id="v",
                     viewer_name="Viewer", payload={"text": text})


def test_intent_classification():
    assert classify_intent(ev("harga berapa kak?")) == "tanya_produk"
    assert classify_intent(ev("halo kak")) == "sapaan"
    assert classify_intent(ev("cek profil bit.ly/xx")) == "spam"
    assert classify_intent(ev("kamu bot ya")) == "troll"


def test_emotion_reacts_to_gift():
    eng = EmotionEngine()
    state = eng.update(EmotionState(), LiveEventType.GIFT)
    assert state.valence > 0.3
    assert state.label == "senang"
