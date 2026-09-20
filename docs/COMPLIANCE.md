# Compliance & Safety — Live AI Creator

## Wajib
1. **Disclosure AI**: setiap sesi live harus menyatakan diri sebagai AI host di awal dan berkala
   (setiap 10-15 menit + label metadata stream). Template dari blueprint `policy.disclosure_text`.
2. **Consent suara**: voice clone HANYA dengan `clone_consent_ref` valid. Tanpa consent → TTS generik.
3. **ToS Platform**: setiap adapter memuat flag fitur berdasarkan aturan platform terbaru;
   nonaktifkan fitur (mis. auto-reply DM) bila melanggar.
4. **Moderasi dua arah**: input komentar & output utterance sama-sama difilter.
5. **Larangan umum**: klaim medis, janji hasil investasi, konten dewasa, politik sensitif,
   impersonation manusia nyata, data pribadi viewer.

## Mekanisme di Kode
- `compliance/gate.py` = satu-satunya jalur output ke stream. Tidak ada bypass.
- Pelanggaran level: `WARN` (redaksi) → `BLOCK` (skip utterance) → `PAUSE` (jeda sesi) → `KILL` (stop).
- Log audit immutable (`compliance.violation`) dengan hash rantai.

## Catatan Hukum (ringkas, bukan nasihat hukum)
- Indonesia: UU ITE, aturan label konten AI, hak cipta suara/wajah.
- Selalu review kebijakan terbaru tiap platform sebelum produksi.
