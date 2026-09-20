#!/usr/bin/env python3
"""Final SEO safety scan for branding/indexing task."""
import os, re, json

ROOT = os.path.dirname(os.path.abspath(__file__))
PROD = "https://measurestacktools.github.io/money"
fails, notes = [], []

def pages():
    out = []
    for dp, dn, fn in os.walk(ROOT):
        if ".git" in dp: continue
        for f in fn:
            if f in ("index.html", "404.html"):
                out.append(os.path.join(dp, f))
    return out

P = pages()
indexable = [p for p in P if not p.endswith("404.html")]
print("pages:", len(P), "indexable:", len(indexable))

# 1. banned strings in HTML pages
for p in P:
    t = open(p, encoding="utf-8").read()
    rel = os.path.relpath(p, ROOT)
    for pat in ["USERNAME", "rayanbaig796-crypto", "localhost", "127.0.0.1",
                "/money/money/", "BuildEstimate", "data:image/svg+xml"]:
        if pat in t:
            fails.append(f"BANNED '{pat}': {rel}")
    # http:// only allowed inside svg namespace / ld+json contexts? check non-namespace
    for m in re.finditer(r"http://(?!www\.w3\.org)[^\s\"']*", t):
        fails.append(f"HTTP URL: {rel} -> {m.group(0)[:80]}")

# 2. one canonical per indexable page, matching production URL structure
cans = {}
for p in indexable:
    t = open(p, encoding="utf-8").read()
    rel = os.path.relpath(p, ROOT)
    found = re.findall(r'<link rel="canonical" href="([^"]+)"', t)
    if len(found) != 1:
        fails.append(f"CANONICAL COUNT {len(found)}: {rel}")
        continue
    c = found[0]
    cans.setdefault(c, []).append(rel)
    if not c.startswith(PROD):
        fails.append(f"CANONICAL DOMAIN: {rel} -> {c}")
    # expected path from file location
    d = os.path.dirname(rel).replace("\\", "/")
    exp = PROD + "/" if d in (".", "") else PROD + "/" + d + "/"
    if c != exp and not (rel == "404.html"):
        fails.append(f"CANONICAL MISMATCH: {rel} has {c} want {exp}")
for c, v in cans.items():
    if len(v) > 1:
        fails.append(f"DUP CANONICAL {c}: {v}")

# 3. sitemap vs canonicals
sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
locs = re.findall(r"<loc>(.*?)</loc>", sm)
if "404" in sm or "localhost" in sm or "USERNAME" in sm or "rayanbaig796-crypto" in sm:
    fails.append("SITEMAP contains 404/localhost/USERNAME/old-user")
if len(locs) != len(set(locs)):
    fails.append("SITEMAP duplicates")
if set(locs) != set(cans.keys()):
    fails.append(f"SITEMAP/CANONICAL SET MISMATCH: sitemap={len(locs)} canonicals={len(cans)} "
                 + f"only-sitemap={set(locs)-set(cans)} only-canon={set(cans)-set(locs)}")

# 4. robots
rb = open(os.path.join(ROOT, "robots.txt"), encoding="utf-8").read()
if PROD + "/sitemap.xml" not in rb:
    fails.append("ROBOTS sitemap ref wrong: " + rb.strip().replace("\n", " | "))

# 5. favicon/logo/og refs resolve to files
for p in P:
    t = open(p, encoding="utf-8").read()
    rel = os.path.relpath(p, ROOT)
    depth = 0 if os.path.dirname(rel) in (".", "") else (1 if rel.count(os.sep) == 1 else 2)
    for m in re.finditer(r'(?:href|src)="(\.\./(?:assets/[^"]+))"', t):
        target = os.path.normpath(os.path.join(os.path.dirname(p), m.group(1)))
        if not os.path.isfile(target):
            fails.append(f"BROKEN ASSET: {rel} -> {m.group(1)}")
    if '<meta property="og:image" content="' + PROD + '/assets/img/og-image.png">' not in t:
        fails.append(f"OG IMAGE TAG: {rel}")
    ogurl = re.search(r'<meta property="og:url" content="([^"]+)"', t)
    can = re.search(r'<link rel="canonical" href="([^"]+)"', t)
    if ogurl and can and ogurl.group(1) != can.group(1):
        fails.append(f"OGURL/CANON MISMATCH: {rel}")

# 6. JSON-LD valid on all pages; org logo absolute on home
for p in P:
    t = open(p, encoding="utf-8").read()
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        try:
            json.loads(m.group(1))
        except Exception as e:
            fails.append(f"BAD JSON-LD {os.path.relpath(p, ROOT)}: {e}")
home = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
for need in ['"@type":"Organization"', '"name":"MeasureStack"',
             '"logo":"' + PROD + '/assets/img/icon-512.png"',
             '"@type":"WebSite"']:
    if need not in home:
        fails.append("ORG SCHEMA missing: " + need[:50])

# 7. noindex check
for p in P:
    if "noindex" in open(p, encoding="utf-8").read().lower():
        fails.append("NOINDEX: " + os.path.relpath(p, ROOT))

print("FAILURES:", len(fails))
for f in fails:
    print(" -", f)
