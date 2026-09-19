# QA Report — MeasureStack first release

## Coverage

- 47 HTML pages (home, 6 categories, 30 tools, guides index + 5 guides, about/privacy/contact, 404).
- 30/30 calculators functionally tested; 30/30 inline scripts parse.

## Tests executed

1. `qa.py` — SEO (title/desc/canonical/H1/viewport/lang present; 47 unique
   titles, 47 unique descs, 47 unique H1), JSON-LD validity, 47 internal
   links crawled (0 broken), sitemap (46 URLs, all resolve), 8 formula
   checks (slab yd³/bags, board feet, tile, pitch, post-hole, gravel,
   metric slab), zero/negative/huge edge cases, JS brace balance.
2. `test_calc.js` (node, headless DOM stub) — 8/8 pass: imperial slab
   (1.23 yd³, 59 bags), metric slab (0.9 m³), negative-input error path,
   board feet (53.33 BF), tile (110), pitch (26.6°/1.118), metric gravel,
   safeStore fallback with storage unavailable.
3. `test_syntax.js` — all 30 inline calculator scripts `node --check` OK.
4. Live Playwright (`python -m http.server` + `/money/` junction):
   slab calculate (imperial + metric), invalid-input error, unit-toggle
   labels + persistence across reload, homepage search synonyms
   ("cement", "patio"), 390px overflow scan (none), console errors.

## Errors found and fixed

1. Wrong worked-example numbers in 7 static examples (slab, bags,
   brick %, topsoil, drywall room math, shingle bundles, post-hole
   volume) — recomputed and corrected to match tool output.
2. cp1252/UTF-8 mojibake from generator file reads — all reads/writes
   pinned to UTF-8, pages regenerated, verified live (× → ≈ render).
3. Metric toggle parsed inputs as imperial on 23 tools (hardcoded
   `lenToM(v,'ft'/'in')`) — renderer now injects unit-aware `LU`/`SU`;
   brick openings + insulation coverage metric conversions fixed.
4. Inline calculator script loaded before shared `calc.js` (unit toggle
   never bound) — shared scripts now emitted before inline script.
5. Unit labels outside `#units` never updated (scoped querySelector) —
   `bindUnits` now queries labels document-wide.
6. Missing favicon 404 — inline SVG data-URI icon added to all pages.
7. Table overflow risk on 320px — tables scroll horizontally in place.

## Pre-launch validation (final)

- `galUS` removed from paint calculator; builder debug prints removed.
- Live click-through 30/30 tools (realistic values, imperial + metric,
  error paths): 30 pass. Two initial flags investigated — siding with
  degenerate all-10s input correctly errors; footings toggle flag was a
  harness label-selector artifact. One real bug found this way (siding
  net-area display showed m² labeled sq ft in imperial) — fixed and
  re-verified live.
- Final crawl: 14 representative pages live — all HTTP 200, H1 present,
  canonicals contain `/money/`, CSS/JS/sitemap.xml/robots.txt 200,
  zero `noindex`, zero console/page errors, zero overflow at
  320/375/390/768/1440 on home + 2 tool pages.
- Sitemap: 46 URLs, 46 unique, no localhost, no `/money/money/`.
- SEO: 47 unique titles / 47 unique descriptions / 47 unique H1s /
  47 canonicals, JSON-LD valid, no orphans (every page in sitemap or
  linked), each tool page has unique intro/formula/example/FAQs.

## Remaining known issues (pre-launch)

- None blocking. Production URL resolved:
  `https://rayanbaig796-crypto.github.io/money` (verified via
  `gh api user`; no placeholder remains in pages/sitemap; `qa.py`
  now fails if `USERNAME` ever reappears in the sitemap).
