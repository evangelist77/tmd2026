# TMD 2026

Static WhatsApp preview page with immediate browser redirect to https://forms.gle/QzJoZCnaWvRLUD1t7.

## Local preview
Run `python3 -m http.server 8080 --directory public`, then open http://localhost:8080.

## Deploy
Create a public GitHub repository named tmd2026 and push main. Import it into Vercel as tmd2026, preset Other, output public, no install/build commands. Assign tmd2026.vercel.app if available. Production must be publicly reachable.

## Updates
Replace the JPEG with a new versioned filename and update og:image, dimensions, and alt text in public/index.html. Keep 9:16 and under 300 KB. Update both the script and fallback link when changing the form. Never add an HTTP redirect or meta refresh to the entry page.

## Verification
Check HTTP 200 and HTML metadata with curl using normal and WhatsApp User-Agents. Check the JPEG returns image/jpeg. Test immediate navigation in desktop/mobile browsers, fallback with JavaScript disabled, and Back without redirect loops. Paste the production URL into WhatsApp on a phone and verify the actual preview and destination. WhatsApp controls preview cropping. Form access may require Google login; do not submit test registrations.

## Contact route
`/cp_nadhief` returns a temporary HTTP 307 redirect to Nadhief on WhatsApp (+62 821-2665-7276), with the supplied message prefilled. The user must press Send themselves. The route is configured in vercel.json and needs Vercel to test; Python's static server does not implement it.

## Poster v2
Source: source-assets/poster-tmd-2026-v2.png (original supplied PNG, preserved byte-for-byte). Preview: public/assets/poster-tmd-2026-v2.jpg, 1080×1920, 291,756 bytes; JPEG quality 82, optimized progressive, no chroma subsampling, no resizing/cropping. Versioned filename replaces v1 in the Open Graph tags. Existing WhatsApp messages may retain their cached preview; test a fresh share with ?v=2 if necessary.
