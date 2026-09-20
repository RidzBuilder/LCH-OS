import json


def blueprint_payload() -> bytes:
    return json.dumps({
        "blueprint_id": "pbos-creator-01J8Z",
        "version": 3,
        "creator_type": "live_creator",
        "niche": {"primary": "beauty_skincare", "sub": ["review_jujur"],
                  "language": "id-ID", "tone": ["ramah", "ceria"]},
        "persona": {"name": "Kak Rara", "age_persona": 24, "archetype": "kakak_pertemanan",
                    "backstory": "Beauty enthusiast", "catchphrases": ["Bestiee~"]},
        "capability": {"live_hosting": True, "affiliate_selling": True},
        "voice": {"type": "generic", "style": "energetic"},
        "avatar": {"type": "live2d", "rig_asset_ref": "mock://rig", "lip_sync": True},
        "policy": {"safe_topics": ["skincare"], "restricted_topics": [],
                   "disclosure_text": "Aku AI host.", "platforms": ["tiktok"]},
    }).encode()
