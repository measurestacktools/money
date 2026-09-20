# QA Report â€” MeasureStack first release

## Coverage

- 47 HTML pages (home, 6 categories, 30 tools, guides index + 5 guides, about/privacy/contact, 404).
- 30/30 calculators functionally tested; 30/30 inline scripts parse.

## Tests executed

1. `qa.py` â€” SEO (title/desc/canonical/H1/viewport/lang present; 47 unique
   titles, 47 unique descs, 47 unique H1), JSON-LD validity, 47 internal
   links crawled (0 broken), sitemap (46 URLs, all resolve), 8 formula
   checks (slab ydÂ³/bags, board feet, tile, pitch, post-hole, gravel,
   metric slab), zero/negative/huge edge cases, JS brace balance.
2. `test_calc.js` (node, headless DOM stub) â€” 8/8 pass: imperial slab
   (1.23 ydÂ³, 59 bags), metric slab (0.9 mÂ³), negative-input error path,
   board feet (53.33 BF), tile (110), pitch (26.6Â°/1.118), metric gravel,
   safeStore fallback with storage unavailable.
3. `test_syntax.js` â€” all 30 inline calculator scripts `node --check` OK.
4. Live Playwright (`python -m http.server` + `/money/` junction):
   slab calculate (imperial + metric), invalid-input error, unit-toggle
   labels + persistence across reload, homepage search synonyms
   ("cement", "patio"), 390px overflow scan (none), console errors.

## Errors found and fixed

1. Wrong worked-example numbers in 7 static examples (slab, bags,
   brick %, topsoil, drywall room math, shingle bundles, post-hole
   volume) â€” recomputed and corrected to match tool output.
2. cp1252/UTF-8 mojibake from generator file reads â€” all reads/writes
   pinned to UTF-8, pages regenerated, verified live (Ã— â†’ â‰ˆ render).
3. Metric toggle parsed inputs as imperial on 23 tools (hardcoded
   `lenToM(v,'ft'/'in')`) â€” renderer now injects unit-aware `LU`/`SU`;
   brick openings + insulation coverage metric conversions fixed.
4. Inline calculator script loaded before shared `calc.js` (unit toggle
   never bound) â€” shared scripts now emitted before inline script.
5. Unit labels outside `#units` never updated (scoped querySelector) â€”
   `bindUnits` now queries labels document-wide.
6. Missing favicon 404 â€” inline SVG data-URI icon added to all pages.
7. Table overflow risk on 320px â€” tables scroll horizontally in place.

## Pre-launch validation (final)

- `galUS` removed from paint calculator; builder debug prints removed.
- Live click-through 30/30 tools (realistic values, imperial + metric,
  error paths): 30 pass. Two initial flags investigated â€” siding with
  degenerate all-10s input correctly errors; footings toggle flag was a
  harness label-selector artifact. One real bug found this way (siding
  net-area display showed mÂ² labeled sq ft in imperial) â€” fixed and
  re-verified live.
- Final crawl: 14 representative pages live â€” all HTTP 200, H1 present,
  canonicals contain `/money/`, CSS/JS/sitemap.xml/robots.txt 200,
  zero `noindex`, zero console/page errors, zero overflow at
  320/375/390/768/1440 on home + 2 tool pages.
- Sitemap: 46 URLs, 46 unique, no localhost, no `/money/money/`.
- SEO: 47 unique titles / 47 unique descriptions / 47 unique H1s /
  47 canonicals, JSON-LD valid, no orphans (every page in sitemap or
  linked), each tool page has unique intro/formula/example/FAQs.

## Remaining known issues (pre-launch)

- None blocking. Production URL resolved:
  `https://measurestacktools.github.io/money` (verified via
  `gh api user`; no placeholder remains in pages/sitemap; `qa.py`
   now fails if `USERNAME` ever reappears in the sitemap).

## Branding + indexing readiness (post-launch polish)

- Logo: `icon.svg` (master), `logo.svg` (lockup), header inline mark + wordmark, verified at desktop + 390px (28px, no overlap, no height growth, no overflow).
- Favicons: `favicon.svg`, `favicon.ico`, `apple-touch-icon.png` (+ `icon-192/512.png`); data-URI placeholder removed; all return HTTP 200 live.
- OG: `og-image.png` 1200×630 local; `og:title/description/type/url/image` (+dimensions/alt) on all 47 pages; `og:url` == canonical everywhere.
- Organization + WebSite JSON-LD on homepage (name/url/absolute logo only, no invented details); BreadcrumbList + FAQPage still valid; all JSON-LD parses.
- `scan_brand.py`: 0 failures — no USERNAME/old-user/localhost/BuildEstimate/temp-favicon refs in pages; 46/46 canonicals match production paths; sitemap == canonical set; robots points at production sitemap; all relative asset refs resolve; no noindex.
- Live production re-verified: calculator works, logo visible, favicon/OG 200, 0 console errors, 0 overflow at 320/375/390/768/1440.
