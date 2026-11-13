# Referral Prefill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Opening `https://tmd2026.vercel.app/?ref=123456` prefills only Kode Referral (opsional).

**Architecture:** Add a query-matching Vercel redirect ahead of the existing root redirect. Use Google Forms prefill parameter `entry.1217740900`, identified from the live form metadata. Keep the static HTML fallback consistent.

**Tech Stack:** Static HTML, Vercel routing JSON, Python smoke tests.

**Spec:** User request: six numeric digits from `?ref=XXXXXX`, only referral field populated, with testing.

## Global Constraints

- Accept exactly six ASCII digits; preserve leading zeroes.
- No new dependencies or form submissions.
- Preserve crawler poster previews and contact redirects.

## Review Focus

- Missing ref: existing form redirect without prefill.
- Invalid length/non-numeric ref: no prefill.
- Leading zeroes: preserved verbatim.
- Additional query parameters: referral still reaches its field.
- Crawler requests: continue serving poster metadata.

---

### Task 1: Route referral links and verify prefill

**Files:**
- Modify: `vercel.json` — insert referral-specific redirect first, sharing existing crawler exclusion.
- Modify: `public/index.html` — apply equivalent prefill to fallback anchor and client redirect.
- Modify: `scripts/verify_routes.py` — identify baseline/contact rules by source rather than position; add referral cases.
- Modify: `README.md` — document referral link format.

**Interfaces:**
- Consumes: URL query `ref`, matching `[0-9]{6}` only.
- Produces: Google Forms URL with `usp=pp_url&entry.1217740900=<ref>`; all other fields absent.

- [x] **Step 1: Add failing route cases.** Assert `123456` and `000123` map to `entry.1217740900` exactly; absent, empty, `12345`, `1234567`, `ABC123` do not prefill. Assert crawler requests with valid ref return HTML metadata. Keep existing contact and poster checks.
- [x] **Step 2: Run tests against current deployment.** `python3 scripts/verify_routes.py`; new valid-ref assertions must fail.
- [x] **Step 3: Add Vercel query condition.** Match `ref` with named capture `(?<referral>[0-9]{6})` anchored at both ends; interpolate `:referral` into only `entry.1217740900`. Preserve crawler exclusion. Update fallback using URLSearchParams and the same validation; update anchor before navigation.
- [x] **Step 4: Verify.** Validate JSON locally; run updated smoke tests against a Vercel preview. Open valid-ref link in browser and inspect actual referral input value `000123`, with other answer fields blank, without submitting. Run baseline/crawler/contact/poster checks; all assertions must pass.
- [x] **Step 5: Commit.** `git add vercel.json public/index.html scripts/verify_routes.py README.md` then `git commit -m "feat: prefill referral code from link"`.

Self-review: one task covers routing, fallback, documentation and tests; live field ID verified. Deployment and browser verification remain execution steps.

Execution: completed on `feat/referral-prefill`. See `VERIFICATION.md` for evidence and retained limitations. Used isolated testing deployment rather than changing original production.
