# TMD 2026

Static WhatsApp preview page with an edge HTTP 307 redirect for visitors to the Google Form. WhatsApp and Meta preview crawlers receive HTTP 200 HTML with the poster metadata. The destination is the resolved Google Forms URL, avoiding the extra forms.gle redirect.

## Local preview
Run `python3 -m http.server 8080 --directory public`, then open http://localhost:8080.

## Deploy
Create a public GitHub repository named tmd2026 and push main. Import it into Vercel as tmd2026, preset Other, output public, no install/build commands. Assign tmd2026.vercel.app if available. Production must be publicly reachable.

## Updates
Replace the JPEG with a new versioned filename and update og:image, dimensions, and alt text in public/index.html. Keep 9:16 and under 300 KB. Update both the script and fallback link when changing the form. The root HTTP redirect must exclude WhatsApp/Meta preview crawlers. Keep the HTML fallback target and edge destination in sync; do not add a meta refresh.

## Verification
Check HTTP 307 for visitors and HTTP 200 with HTML metadata for WhatsApp/Meta preview User-Agents. Check the JPEG returns image/jpeg. Test immediate navigation in desktop/mobile browsers, fallback with JavaScript disabled, and Back without redirect loops. Paste the production URL into WhatsApp on a phone and verify the actual preview and destination. WhatsApp controls preview cropping. Form access may require Google login; do not submit test registrations.

## Contact route
`/cp_nadhief` returns a temporary HTTP 307 redirect to Nadhief on WhatsApp (+62 821-2665-7276), with the supplied message prefilled. The destination uses api.whatsapp.com/send directly because the wa.me intermediary was observed converting emoji to U+FFFD replacement characters. The user must press Send themselves. The route is configured in vercel.json and needs Vercel to test; Python's static server does not implement it.

## Poster v2
Source: source-assets/poster-tmd-2026-v2.png (original supplied PNG, preserved byte-for-byte). Preview: public/assets/poster-tmd-2026-v2.jpg, 1080×1920, 291,756 bytes; JPEG quality 82, optimized progressive, no chroma subsampling, no resizing/cropping. Versioned filename replaces v1 in the Open Graph tags. Existing WhatsApp messages may retain their cached preview; test a fresh share with ?v=2 if necessary.

`/cp_syifa` uses the same contact flow for Kak Syifa (+62 812-9775-8329), with the greeting changed to Kak Syifa and all emoji and line breaks preserved.

## Edge redirect verification
Run `python3 scripts/verify_routes.py https://tmd2026.vercel.app` after deployment. Python local static serving does not implement Vercel conditional routing. Root responses vary by User-Agent and are not browser-cached. The JavaScript and link fallback remain for requests that receive the metadata page.

## Referral links
Use `https://tmd2026.vercel.app/?ref=123456` to prefill only **Kode Referral (opsional)**. Codes must contain exactly six ASCII digits; leading zeroes such as `000123` are preserved. Missing or invalid codes open the ordinary blank form. The Google Forms field is `entry.1217740900`; update both routing and HTML if that field is recreated. WhatsApp/Meta previews and contact routes retain their existing behavior.

Run `node scripts/verify_fallback.cjs` for local fallback regression checks (Node.js standard library only). Full HTTP routing checks require a deployed URL: Vercel dev ignores query `has` conditions.
