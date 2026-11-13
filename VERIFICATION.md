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

## Referral prefill — 2026-11-13

- Original deployment: baseline 10/10 checks passed; new valid-ref check failed before implementation (no referral entry).
- Updated isolated Vercel test deployment: HTTP suite 22/22 passed, including six-digit codes, leading zeroes, extra query parameters, missing/invalid codes, trailing newline rejection, crawler previews, contacts, and poster bytes.
- `node scripts/verify_fallback.cjs`: 10/10 passed; confirmed the test fails against the original HTML.
- Browser: test deployment `/?ref=000123` opened the real Google Form; Kode Referral input contained `000123`, other visible text inputs were empty. No form was submitted.
- Fresh independent code review completed. Existing Vercel query passthrough retained: manually supplied Google `entry.*` parameters can prefill other answers. Duplicate `ref` keys are outside generated-link format and may differ between edge and fallback.
- Original production was not deployed. Isolated testing project is removed after verification with user authorization.

## Alphanumeric referrals and short links — 2026-11-13

- Before implementation: new alphanumeric expectations failed against both the old fallback script and production edge; `/AX2046?v=2` returned 404.
- Fallback now accepts exactly six ASCII letters/digits, preserving case and leading zeroes: 17/17 checks passed.
- Isolated Vercel preview: 53/53 HTTP checks passed, using authenticated access because preview deployment protection is enabled. Short links redirect to the root query form, preserving `v=2`; path code overrides conflicting `ref` query values.
- WhatsApp/Meta crawler checks passed for both `/?v=2&ref=AX2046` and `/AX2046?v=2`, serving v2 poster metadata. The poster asset response still matches the local v2 JPEG byte-for-byte; contact links remain intact.
- Existing query passthrough remains unchanged. Actual WhatsApp app cache/cropping and Google Form submission are not tested.
