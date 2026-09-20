import pytest

from packages.lch_core.errors import LchError
from packages.lch_core.models import CreatorType, Niche, PersonaProfile
from packages.lch_genesis.compiler import compile_blueprint
from packages.lch_genesis.ingestor import parse_blueprint, verify_pbos_signature
from tests.fixtures import blueprint_payload


def test_parse_valid_blueprint():
    bp = parse_blueprint(blueprint_payload())
    assert bp.persona.name == "Kak Rara"
    assert bp.creator_type == CreatorType.LIVE_CREATOR


def test_parse_invalid_blueprint():
    with pytest.raises(LchError) as exc:
        parse_blueprint(b'{"blueprint_id": "x"}')
    assert exc.value.code == "GENESIS_INVALID_BLUEPRINT"


def test_signature_verify_ok():
    import hashlib, hmac
    body = blueprint_payload()
    sig = hmac.new(b"secret", body, hashlib.sha256).hexdigest()
    verify_pbos_signature(body, sig, "secret")  # tidak raise


def test_signature_verify_fail():
    with pytest.raises(LchError):
        verify_pbos_signature(b"{}", "bad", "secret")


def test_compile_builds_runtime_bundle():
    bp = parse_blueprint(blueprint_payload())
    bundle = compile_blueprint(bp)
    assert "Kak Rara" in bundle.system_prompt
    assert bundle.voice_config["style"] == "energetic"
