import re
from packages.lch_core.models import LiveEvent


def classify_intent(event: LiveEvent) -> str:
    text = (event.payload.get("text") or "").lower()
    if event.type.value != "comment":
        return event.type.value
    rules = [
        ("tanya_produk", r"(harga|berapa|ready|stock|stok|link|checkout|beli)"),
        ("sapaan", r"^(halo|hai|hello|hei|pagi|siang|sore|malam)"),
        ("pujian", r"(cantik|keren|bagus|love|mau|cute)"),
        ("spam", r"(spam|cek profil|wa\s*me|bit\.ly)"),
        ("troll", r"(bot|robot|bukan manusia|ai kan)"),
    ]
    for label, pattern in rules:
        if re.search(pattern, text):
            return label
    return "ngobrol"
