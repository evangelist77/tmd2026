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
