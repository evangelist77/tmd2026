# Verification — 2026-11-12

- PASS: supplied poster.jpeg copied byte-for-byte; JPEG 900×1600 (9:16), 173,938 bytes.
- PASS: local HTML and image return HTTP 200 with correct MIME types for browser and WhatsApp User-Agents.
- PASS: redirect script executed in Node VM with the exact intended form URL.
- PASS: production https://tmd2026.vercel.app/ returns HTTP 200 text/html containing static Open Graph tags and redirect script.
- PASS: production poster returns HTTP 200 image/jpeg and matches local source byte-for-byte. Tested normal and WhatsApp User-Agents, without authentication.
- PASS: opening production URL in native Chrome immediately navigated to the intended Google Form and displayed its TMD 2026 heading. No form response submitted.
- PASS: GitHub repository evangelist77/tmd2026 is PUBLIC, default branch main; Vercel reports GitHub connected and production deployment READY with requested alias.
- NOT VERIFIED: real WhatsApp phone preview, cropping and tap behavior; requires manual phone test.
- NOT VERIFIED: mobile browser viewport, JavaScript-disabled browser interaction and browser Back behavior. Fallback link exists in static HTML; redirect uses location.replace.

## Manual phone check
Paste https://tmd2026.vercel.app/ into WhatsApp, wait for preview, confirm correct poster and title. Send to your own chat and open the preview to confirm navigation to the form. WhatsApp controls image cropping. Google Form may require Google sign-in.
