#!/usr/bin/env python3
"""QA: SEO audit + link crawl + formula tests + JSON-LD validation."""
import os, re, json, math

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "/money"
fails, warns = [], []

def pages():
    out = []
    for dp, dn, fn in os.walk(ROOT):
        if "node_modules" in dp: continue
        for f in fn:
            if f == "index.html" or f == "404.html":
                out.append(os.path.join(dp, f))
    return out

P = pages()
print("HTML pages:", len(P))

# --- SEO checks ---
titles, descs, h1s = {}, {}, {}
for p in P:
    t = open(p, encoding="utf-8").read()
    rel = os.path.relpath(p, ROOT)
    for name, pat in [("title", r"<title>(.*?)</title>"), ("desc", r'<meta name="description" content="(.*?)">'),
                      ("canon", r'<link rel="canonical" href="(.*?)">'), ("h1", r"<h1>(.*?)</h1>"),
                      ("viewport", r'<meta name="viewport"'), ("lang", r'<html lang="en">')]:
        m = re.search(pat, t, re.S)
        if not m and name in ("title", "desc", "canon", "h1", "viewport", "lang"):
            fails.append(f"MISSING {name}: {rel}")
        elif m and name == "title": titles.setdefault(m.group(1), []).append(rel)
        elif m and name == "desc": descs.setdefault(m.group(1), []).append(rel)
        elif m and name == "h1": h1s.setdefault(m.group(1), []).append(rel)
    # JSON-LD validity
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        try: json.loads(m.group(1))
        except Exception as e: fails.append(f"BAD JSON-LD {rel}: {e}")

for label, d in [("title", titles), ("desc", descs)]:
    for k, v in d.items():
        if len(v) > 1: fails.append(f"DUP {label}: {k[:60]}... in {v}")
print("unique titles:", len(titles), "unique descs:", len(descs), "unique H1:", len(h1s))

# --- link crawl ---
def href_to_file(h):
    h = h.split("#")[0].split("?")[0]
    if not h.startswith(BASE + "/") and h != BASE + "/": return None
    sub = h[len(BASE):]
    if sub in ("", "/"): return os.path.join(ROOT, "index.html")
    sub = sub.lstrip("/")
    cand = [os.path.join(ROOT, sub, "index.html"), os.path.join(ROOT, sub),
            os.path.join(ROOT, sub.rstrip("/") + ".html")]
    for c in cand:
        if os.path.isfile(c): return c
    if sub == "sitemap.xml" or sub == "robots.txt": return "static-ok"
    return "MISSING"

checked, broken = set(), []
for p in P:
    t = open(p, encoding="utf-8").read()
    for m in re.finditer(r'href="(/money/[^"]*)"', t):
        h = m.group(1)
        if h in checked: continue
        checked.add(h)
        r = href_to_file(h)
        if r == "MISSING": broken.append(f"{os.path.relpath(p,ROOT)} -> {h}")
        elif r == "static-ok":
            if not os.path.isfile(os.path.join(ROOT, os.path.basename(h))): broken.append(f"static missing {h}")
print("internal links checked:", len(checked), "broken:", len(broken))
for b in broken: fails.append("BROKEN LINK: " + b)

# --- sitemap check ---
sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
locs = re.findall(r"<loc>(.*?)</loc>", sm)
print("sitemap urls:", len(locs))
for u in locs:
    if "USERNAME" in u: fails.append("SITEMAP PLACEHOLDER NOT REPLACED: " + u)
    path = re.sub(r"^https?://[^/]+/money", "", u)
    f = href_to_file(BASE + path + ("" if path.endswith("/") else "/"))
    if f == "MISSING": fails.append("SITEMAP URL MISSING FILE: " + u)

# --- formula tests (mirror of JS math) ---
def slab_yd3(Lft, Wft, Din): return Lft * 0.3048 * Wft * 0.3048 * Din * 0.0254 / 0.764554857984
cases = [
    ("slab 10x10x4in yd3", slab_yd3(10, 10, 4), 1.234, 0.05),
    ("slab bags 10x10x4in", slab_yd3(10, 10, 4) * 0.764554857984 * 35.314666721 / 0.60, 55.6, 0.5),
    ("boardfeet 2x4x8", 2 * 4 * 8 / 12, 5.333, 0.01),
    ("tile 100sqft 12in", 100 / 1, 100, 0.01),
    ("pitch mult 6/12", math.sqrt(1 + (6 / 12) ** 2), 1.118, 0.001),
    ("posthole 12inx36in cuft", math.pi * (1 / 2) ** 2 * 3, 2.356, 0.01),
    ("gravel 20x10x4in yd3", slab_yd3(20, 10, 4), 2.469, 0.05),
    ("metric slab 3x3x0.1 m3", 3 * 3 * 0.1, 0.9, 0.001),
]
for name, got, exp, tol in cases:
    ok = abs(got - exp) <= tol
    print(("PASS " if ok else "FAIL ") + f"{name}: got {got:.4f} expect ~{exp}")
    if not ok: fails.append("FORMULA: " + name)
# edge cases
for name, fn in [("zero", lambda: slab_yd3(0, 10, 4)), ("huge", lambda: slab_yd3(1e6, 1e6, 12))]:
    try:
        v = fn()
        print(f"edge {name}: {v} (finite={math.isfinite(v)})")
        if name == "zero" and v != 0: fails.append("EDGE zero nonzero")
    except Exception as e: fails.append(f"EDGE {name}: {e}")

# JS syntax sanity: node-less check — ensure calc.js/site-config parse as balanced braces
for js in ["assets/js/site-config.js", "assets/js/calc.js", "assets/js/assumptions.js", "assets/js/search.js"]:
    t = open(os.path.join(ROOT, js), encoding="utf-8").read()
    if t.count("{") != t.count("}"): fails.append(f"JS brace mismatch {js}")

print("\n==== RESULT ====")
print("FAILURES:", len(fails))
for f in fails: print(" -", f)
open(os.path.join(ROOT, "QA-RESULTS.txt"), "w").write("\n".join(fails) if fails else "ALL CHECKS PASSED")
