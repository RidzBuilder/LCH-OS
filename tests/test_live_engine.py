from packages.lch_core.models import LiveEvent, LiveEventType
from packages.lch_live_engine.queue import InteractionQueue


def test_queue_prioritizes_gifts():
    q = InteractionQueue()
    q.push(LiveEvent(id="c", session_id="s", type=LiveEventType.COMMENT,
                     viewer_id="v", viewer_name="V", payload={"text": "hai"}))
    q.push(LiveEvent(id="g", session_id="s", type=LiveEventType.GIFT,
                     viewer_id="v", viewer_name="V", payload={"text": "rose"}))
    first = q.pop()
    assert first.type == LiveEventType.GIFT
