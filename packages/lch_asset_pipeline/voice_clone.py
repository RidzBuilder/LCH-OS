from __future__ import annotations
from packages.lch_core.errors import LchError


def request_voice_clone(consent_ref: str | None, sample_audio_ref: str) -> str:
    """Onboarding clone suara. WAJIB consent_ref valid (bukti persetujuan pemilik suara).

    Produksi: submit job ke provider (ElevenLabs VoiceLab / Azure Custom NN),
    simpan voice_id ke registry, tandai consent_ref.
    """
    if not consent_ref:
        raise LchError("VOICE_CLONE_NO_CONSENT",
                       "Clone suara tanpa consent_ref — dilarang compliance.", retryable=False)
    return f"voice_{consent_ref}"
