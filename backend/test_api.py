"""
test_api.py – Quick integration test using urllib (no httpx needed).
Run via: python test_api.py  (with server running separately)
Or: python -c "exec(open('test_api.py').read())" for inline.
"""
import json
import urllib.request
import urllib.error
import sys

BASE = "http://localhost:8001"
PASS = 0
FAIL = 0

def test(label, method, path, body=None, expect_status=200, check=None):
    global PASS, FAIL
    url = BASE + path
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method)
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        resp = urllib.request.urlopen(req)
        status = resp.status
        result = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        status = e.code
        result = json.loads(e.read().decode()) if e.read else {}
    except Exception as e:
        print(f"  FAIL  {label} — Exception: {e}")
        FAIL += 1
        return

    ok = status == expect_status
    if ok and check:
        ok = check(result)
    tag = "PASS" if ok else "FAIL"
    if not ok:
        FAIL += 1
        print(f"  {tag}  {label} — got status={status}, body={json.dumps(result)[:200]}")
    else:
        PASS += 1
        print(f"  {tag}  {label}")
    return result


# ─── Tests ────────────────────────────────────────────────────────────────────

print("=== HEALTH ===")
test("Health check returns ok",
     "GET", "/api/health",
     check=lambda r: r["status"] == "ok" and r["faq_count"] == 44)

print("\n=== CATEGORIES ===")
test("Returns 10 categories",
     "GET", "/api/categories",
     check=lambda r: len(r["categories"]) == 10)

print("\n=== FAQS ===")
test("All FAQs (44)",
     "GET", "/api/faqs",
     check=lambda r: r["total"] == 44)

test("Filter by fees",
     "GET", "/api/faqs?category=fees",
     check=lambda r: r["total"] == 4 and all(f["category"] == "fees" for f in r["faqs"]))

test("Filter case-insensitive FEES",
     "GET", "/api/faqs?category=FEES",
     check=lambda r: r["total"] == 4)

test("Non-existent category",
     "GET", "/api/faqs?category=nonexistent",
     check=lambda r: r["total"] == 0)

print("\n=== CHAT – POSITIVE ===")
test("Exact FAQ question",
     "POST", "/api/chat",
     body={"message": "What is the tuition fee?"},
     check=lambda r: r["intent"] == "tuition_fee" and r["category"] == "fees" and r["confidence"] >= 0.9)

test("Paraphrased question",
     "POST", "/api/chat",
     body={"message": "how to apply for admission"},
     check=lambda r: r["intent"] == "admission_process" and r["category"] == "admissions")

test("Single keyword: hostel",
     "POST", "/api/chat",
     body={"message": "hostel"},
     check=lambda r: r["category"] == "hostel")

test("Fallback – gibberish",
     "POST", "/api/chat",
     body={"message": "xyzzy blargh foobaz"},
     check=lambda r: r["intent"] is None and "sorry" in r["reply"].lower())

test("Fallback – off topic",
     "POST", "/api/chat",
     body={"message": "How do I cook pasta?"},
     check=lambda r: r["intent"] is None)

test("Confidence between 0 and 1",
     "POST", "/api/chat",
     body={"message": "What are the library timings?"},
     check=lambda r: r["confidence"] is not None and 0 <= r["confidence"] <= 1)

print("\n=== CHAT - INPUT VALIDATION ===")
test("Empty message -> 422",
     "POST", "/api/chat",
     body={"message": ""},
     expect_status=422)

test("Whitespace-only -> 422",
     "POST", "/api/chat",
     body={"message": "   "},
     expect_status=422)

test("Missing field -> 422",
     "POST", "/api/chat",
     body={},
     expect_status=422)

test("Emojis only -> fallback",
     "POST", "/api/chat",
     body={"message": "😀🎓📚"},
     check=lambda r: r.get("intent") is None)

test("Special chars only -> fallback",
     "POST", "/api/chat",
     body={"message": "@#$%^&*()!"},
     check=lambda r: r.get("intent") is None)

print("\n=== CHAT - SECURITY ===")
test("SQL injection -> no crash",
     "POST", "/api/chat",
     body={"message": "'; DROP TABLE faqs; --"},
     check=lambda r: "reply" in r)

test("XSS payload -> no crash",
     "POST", "/api/chat",
     body={"message": "<script>alert(1)</script>"},
     check=lambda r: "reply" in r)

test("Path traversal -> no crash",
     "POST", "/api/chat",
     body={"message": "../../etc/passwd"},
     check=lambda r: "reply" in r)

print("\n=== HISTORY ===")
test("History returns records",
     "GET", "/api/history",
     check=lambda r: r["total"] > 0)

test("History limit=2",
     "GET", "/api/history?limit=2",
     check=lambda r: len(r["history"]) <= 2)

test("History limit=0 -> 422",
     "GET", "/api/history?limit=0",
     expect_status=422)

test("History limit=abc -> 422",
     "GET", "/api/history?limit=abc",
     expect_status=422)

print("\n=== ROOT ===")
test("Root endpoint",
     "GET", "/",
     check=lambda r: "message" in r)

print(f"\n{'='*50}")
print(f"RESULTS:  {PASS} passed,  {FAIL} failed,  {PASS+FAIL} total")
if FAIL > 0:
    sys.exit(1)
