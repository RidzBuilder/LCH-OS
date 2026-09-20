from __future__ import annotations
import hmac, hashlib
from pydantic import ValidationError

from packages.lch_core.errors import LchError
from packages.lch_core.models import AssetCreatorBlueprint


def verify_pbos_signature(raw_body: bytes, signature: str, secret: str) -> None:
    expected = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise LchError("GENESIS_UNAUTHORIZED", "Signature PBOS tidak valid", retryable=False)


def parse_blueprint(raw_body: bytes) -> AssetCreatorBlueprint:
    try:
        return AssetCreatorBlueprint.model_validate_json(raw_body)
    except ValidationError as exc:
        raise LchError("GENESIS_INVALID_BLUEPRINT", f"Skema blueprint invalid: {exc}", retryable=False)
