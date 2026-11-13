"""Smoke-test deployed edge routing without following contacts or submitting forms."""
import json
import sys
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args):
        return None


def fetch(path, user_agent):
    request = Request(base + path, headers={"User-Agent": user_agent})
    try:
        response = opener.open(request, timeout=30)
    except HTTPError as response_error:
        response = response_error
    with response:
        return response.code, response.headers, response.read()


base = (sys.argv[1] if len(sys.argv) > 1 else "https://tmd2026.vercel.app").rstrip("/")
opener = build_opener(NoRedirect)
project = Path(__file__).resolve().parent.parent
config = json.loads((project / "vercel.json").read_text())
form = urlsplit(next(route["destination"] for route in config["redirects"] if route["source"] == "/" and not route.get("has")))
for user_agent in ["Mozilla/5.0 Chrome/130.0", "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) Mobile/15E148", "curl/8.0"]:
    status, headers, _ = fetch("/", user_agent)
    location = urlsplit(headers.get("Location", ""))
    assert status == 307 and location == form, (user_agent, status, location)
    print("PASS: immediate form redirect", user_agent)
for user_agent in ["WhatsApp/2.24.5 A", "facebookexternalhit/1.1", "meta-externalagent/1.1", "meta-externalfetcher/1.1"]:
    status, headers, body = fetch("/?v=2", user_agent)
    assert status == 200 and "text/html" in headers.get("Content-Type", "")
    assert b'og:image' in body and b'poster-tmd-2026-v2.jpg' in body
    print("PASS: poster metadata accessible", user_agent)
for route in (route for route in config["redirects"] if route["source"].startswith("/cp_")):
    status, headers, _ = fetch(route["source"], "Mozilla/5.0")
    actual, expected = urlsplit(headers.get("Location", "")), urlsplit(route["destination"])
    assert status == 307
    assert (actual.netloc, actual.path, parse_qs(actual.query)) == (expected.netloc, expected.path, parse_qs(expected.query))
    assert "\ufffd" not in parse_qs(actual.query)["text"][0]
    print("PASS: contact template intact", route["source"])
status, headers, body = fetch("/assets/poster-tmd-2026-v2.jpg", "WhatsApp/2.24")
assert status == 200 and "image/jpeg" in headers.get("Content-Type", "")
assert body == (project / "public/assets/poster-tmd-2026-v2.jpg").read_bytes()
print("PASS: poster asset intact")

for query, expected in [
    ("ref=123456", "123456"), ("ref=000123", "000123"),
    ("v=2&ref=654321", "654321"), ("", None), ("ref=", None),
    ("ref=12345", None), ("ref=1234567", None), ("ref=ABC123", "ABC123"),
    ("ref=AX2046", "AX2046"), ("v=2&ref=ax2046", "ax2046"),
    ("ref=ABCDEF", "ABCDEF"), ("ref=AX204", None),
    ("ref=AX20467", None), ("ref=AX-046", None), ("ref=%C3%89X2046", None),
    ("ref=%20123456", None), ("ref=123456%0A", None),
]:
    status, headers, _ = fetch("/?" + query, "Mozilla/5.0")
    location = urlsplit(headers.get("Location", ""))
    answers = {key: value for key, value in parse_qs(location.query).items() if key.startswith("entry.")}
    assert status == 307 and (location.netloc, location.path) == (form.netloc, form.path)
    assert answers == ({"entry.1217740900": [expected]} if expected else {}), (query, answers)
    print("PASS: referral", query or "absent")
for user_agent in ["WhatsApp/2.24.5 A", "facebookexternalhit/1.1"]:
    for path in ["/?ref=000123", "/?v=2&ref=AX2046"]:
        status, _, body = fetch(path, user_agent)
        assert status == 200 and b'og:image' in body and b'poster-tmd-2026-v2.jpg' in body
        print("PASS: referral poster v2 preview", path, user_agent)

for path, expected, version in [
    ("/AX2046", "AX2046", None), ("/AX2046?v=2", "AX2046", "2"),
    ("/ax2046?v=2", "ax2046", "2"), ("/000123", "000123", None),
    ("/ABCDEF", "ABCDEF", None), ("/AX2046?ref=ZZ9999&v=2", "AX2046", "2"),
]:
    for user_agent in ["Mozilla/5.0", "WhatsApp/2.24.5 A", "facebookexternalhit/1.1"]:
        status, headers, _ = fetch(path, user_agent)
        location = urlsplit(headers.get("Location", ""))
        query = parse_qs(location.query)
        assert status == 307 and location.path == "/", (path, status, location)
        assert query.get("ref") == [expected], (path, query)
        assert query.get("v") == ([version] if version else None), (path, query)
        root_path = location.path + "?" + location.query
        status, headers, body = fetch(root_path, user_agent)
        if user_agent == "Mozilla/5.0":
            target = urlsplit(headers.get("Location", ""))
            answers = {key: value for key, value in parse_qs(target.query).items() if key.startswith("entry.")}
            assert status == 307 and (target.netloc, target.path) == (form.netloc, form.path)
            assert answers == {"entry.1217740900": [expected]}, (path, answers)
        else:
            assert status == 200 and b'poster-tmd-2026-v2.jpg' in body
        print("PASS: short referral and v2", path, user_agent)
for path in ["/AX204", "/AX20467", "/AX-046", "/AX2046/extra"]:
    status, _, _ = fetch(path, "Mozilla/5.0")
    assert status == 404, (path, status)
    print("PASS: invalid short referral", path)
