#!/usr/bin/env python3
"""Render home, categories, guides, static pages, sitemap, robots."""
import os, json

ROOT = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(ROOT, "build_tools_data.py"), encoding="utf-8").read())

SITE_CANON = "https://measurestacktools.github.io/money"
BASE = "/money"

def head(title, desc, canon, depth):
    a = "../" * depth + "assets/"
    return ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
      "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
      "<title>" + title + "</title>\n<meta name=\"description\" content=\"" + desc + "\">\n"
      "<link rel=\"canonical\" href=\"" + canon + "\">\n"
      "<link rel=\"icon\" href=\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%230f5fd0'/%3E%3Ctext x='32' y='44' font-size='36' text-anchor='middle' fill='white' font-family='sans-serif' font-weight='bold'%3EM%3C/text%3E%3C/svg%3E\">\n"
      "<link rel=\"stylesheet\" href=\"" + a + "css/main.css\">\n</head>")

def header(depth):
    return ("<body>\n<a class=\"skip\" href=\"#main\">Skip to content</a>\n"
      "<header class=\"top\"><div class=\"nav\">\n"
      "<a class=\"brand\" href=\"" + BASE + "/\"><span data-brand>MeasureStack</span> <small>material estimators</small></a>\n"
      "<nav aria-label=\"Main\"><a href=\"" + BASE + "/\">Home</a><a href=\"" + BASE + "/guides/\">Guides</a><a href=\"" + BASE + "/about/\">About</a></nav>\n"
      "</div></header>\n<main id=\"main\">")

def footer(depth):
    a = "../" * depth + "assets/"
    return ("</main>\n<footer class=\"site\"><div class=\"inner\">\n"
      "<p><strong><span data-brand>MeasureStack</span></strong> — fast jobsite material estimators. Estimates only; verify with manufacturer specs and local code.</p>\n"
      "<p><a href=\"" + BASE + "/about/\">About</a> · <a href=\"" + BASE + "/privacy/\">Privacy</a> · <a href=\"" + BASE + "/contact/\">Contact</a> · <a href=\"" + BASE + "/sitemap.xml\">Sitemap</a></p>\n"
      "</div></footer>\n<script src=\"" + a + "js/site-config.js\"></script>\n</body>\n</html>")

def write(path, content):
    p = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(content)

POPULAR = ["concrete-slab", "gravel-base", "paint-coverage", "tile-estimator", "board-feet", "roof-shingles"]
def tool_link(s):
    return "<li><a href=\"" + BASE + "/" + T[s]["cat"] + "/" + s + "/\">" + T[s]["h1"] + "</a></li>"

# ---------- HOME ----------
pop = "".join(tool_link(s) for s in POPULAR)
cats = "".join("<a class=\"cat-card\" href=\"" + BASE + "/" + c + "/\"><h3>" + n + "</h3><p>" + d + "</p></a>" for c, (n, d) in CATS.items())
home = (head("MeasureStack — How Much Material Do I Need? Free Estimators",
  "Free construction material estimators: concrete, gravel, lumber, drywall, paint, tile, roofing and more. Imperial + metric, no signup.",
  SITE_CANON + "/", 0) + header(0)
  + "<section class=\"hero\"><h1>How much material do you need?</h1>\n"
  + "<p>Fast estimators for DIYers, homeowners, builders and trades — concrete, lumber, paint, tile, roofing and outdoor materials. Imperial and metric.</p>\n"
  + "<div class=\"searchbox\" role=\"search\"><input id=\"q\" type=\"text\" placeholder=\"What do you need to calculate? Try 'cement', 'patio', 'paint walls'…\" aria-label=\"Search estimators\"><button type=\"button\" onclick=\"document.getElementById('q').focus()\">Search</button></div>\n"
  + "<div id=\"qr\" aria-live=\"polite\"></div></section>\n"
  + "<section class=\"card\"><h2>Popular estimators</h2><ul class=\"linklist\">" + pop + "</ul></section>\n"
  + "<section><h2>Browse by category</h2><div class=\"grid\">" + cats + "</div></section>\n"
  + "<section class=\"card\"><h2>Building a slab? Follow the flow</h2><p>Concrete Slab → Concrete Bags → Rebar Grid → Gravel Base. Each tool links to the next — no dead ends.</p></section>\n"
  + "<section class=\"card\"><h2>Guides</h2><ul><li><a href=\"" + BASE + "/guides/how-much-concrete/\">How much concrete do I need?</a></li>"
  + "<li><a href=\"" + BASE + "/guides/square-footage/\">How to calculate square footage</a></li>"
  + "<li><a href=\"" + BASE + "/guides/waste-factor/\">How to add material waste</a></li></ul></section>\n"
  + "<section class=\"card\"><h2>Why trust these numbers?</h2><p>Every tool shows its formula, states its product assumptions (bag yields, coverage rates) as editable inputs, rounds purchase quantities up, and never uses scraped store prices — cost estimates use only YOUR price.</p></section>\n"
  + '<script src="assets/js/search.js"></script>\n' + footer(0))
write("index.html", home)

# ---------- CATEGORY PAGES ----------
for c, (n, dsc) in CATS.items():
    tools = "".join(tool_link(s) for s, v in sorted(T.items()) if v["cat"] == c)
    other = "".join("<li><a href=\"" + BASE + "/" + cc + "/\">" + nn + "</a></li>" for cc, (nn, dd) in CATS.items() if cc != c)
    pg = (head(n + " Estimators | MeasureStack", dsc + " Free estimators, imperial + metric.",
      SITE_CANON + "/" + c + "/", 1) + header(1)
      + "<nav class=\"breadcrumb\" aria-label=\"Breadcrumb\"><a href=\"" + BASE + "/\">Home</a> › " + n + "</nav>\n"
      + "<h1>" + n + "</h1>\n<p>" + dsc + "</p>\n"
      + "<section class=\"card\"><h2>Estimators in this category</h2><ul class=\"linklist\">" + tools + "</ul></section>\n"
      + "<section class=\"card\"><h2>Other categories</h2><ul>" + other + "</ul></section>\n" + footer(1))
    write(c + "/index.html", pg)

# ---------- GUIDES ----------
GUIDES = {
 "how-much-concrete": ("How Much Concrete Do I Need? (Slabs, Footings, Holes)",
   "Volume-first method for slabs, footings and post holes, plus bag math with editable yields.",
   "<p>Step 1: compute volume (slab: L×W×T; footing trench: L×W×D; round hole: πr²h). Step 2: convert to cubic yards (÷27 from cu ft). Step 3: bags = volume ÷ yield per bag (check the bag — commonly 0.60 cu ft for 80-lb but varies). Step 4: add 5–10% waste.</p><p>Try: <a href=\"" + BASE + "/concrete-masonry/concrete-slab/\">Concrete Slab Calculator</a> · <a href=\"" + BASE + "/concrete-masonry/concrete-bags/\">Bag Calculator</a> · <a href=\"" + BASE + "/outdoor-earthwork/post-holes/\">Post Hole Calculator</a>.</p>"),
 "square-footage": ("How to Calculate Square Footage for Materials",
   "Measure length × width per rectangle, subtract openings, add waste. Works in feet or metres.",
   "<p>Break rooms into rectangles, multiply, sum, subtract doors/windows, then add waste (paint 10%, tile 10–15%, flooring 10%). Use the same unit throughout, then convert if needed (1 sq ft = 0.0929 m²).</p><p>Try: <a href=\"" + BASE + "/walls-paint/paint-coverage/\">Paint Calculator</a> · <a href=\"" + BASE + "/flooring-tile/tile-estimator/\">Tile Calculator</a>.</p>"),
 "waste-factor": ("How to Add Material Waste (5%? 10%? 15%?)",
   "Rule-of-thumb waste rates by material and when to raise them.",
   "<p>Slabs/gravel 5–10%, block/brick 5–7%, tile 10% grid / 15% diagonal, flooring 10%, shingles 5–10% + starter/ridge, cuts and patterns push higher. Order quantity = calculated × (1 + waste%), rounded up.</p><p>Every MeasureStack tool applies this transparently and shows both exact and buy quantities.</p>"),
 "concrete-volume-method": ("How to Calculate Concrete Volume (Method Guide)",
   "The volume-first method behind all our concrete tools, with unit conversions.",
   "<p>Always reduce to consistent units first (we compute in metres internally): slab V=L×W×T; strip footing V=L×W×D; pier V=πr²h×count. Convert: m³→yd³ ÷0.7646; m³→cu ft ×35.31. Then divide by your bag's stated yield.</p><p>Try: <a href=\"" + BASE + "/concrete-masonry/footings-piers/\">Footing Calculator</a>.</p>"),
 "estimating-quantities": ("How to Estimate Construction Material Quantities",
   "A 5-step workflow: measure → net area/volume → product coverage → waste → buy list with your prices.",
   "<p>1) Measure net dimensions. 2) Subtract openings. 3) Divide by product coverage (editable). 4) Add waste and round up. 5) Multiply by YOUR unit price for cost. Never trust a price you didn't enter — stores change prices; the math doesn't.</p><p>Start: <a href=\"" + BASE + "/\">all estimators</a>.</p>"),
}
write("guides/index.html", head("Guides — How to Estimate Materials | MeasureStack",
  "Practical guides: concrete volume, square footage, waste factors and estimating workflow.", SITE_CANON + "/guides/", 1)
  + header(1) + "<h1>Guides</h1><p>Short, practical guides that support the calculators — no filler.</p><ul>"
  + "".join("<li><a href=\"" + BASE + "/guides/" + g + "/\">" + t + "</a></li>" for g, (t, dd, bb) in GUIDES.items())
  + "</ul>" + footer(1))
for g, (t, dd, bb) in GUIDES.items():
    write("guides/" + g + "/index.html", head(t + " | MeasureStack", dd, SITE_CANON + "/guides/" + g + "/", 2)
      + header(2) + "<nav class=\"breadcrumb\" aria-label=\"Breadcrumb\"><a href=\"" + BASE + "/\">Home</a> › <a href=\"" + BASE + "/guides/\">Guides</a> › " + t + "</nav>\n"
      + "<h1>" + t + "</h1>\n<p>" + dd + "</p>\n<section class=\"card\">" + bb + "</section>\n" + footer(2))

# ---------- ABOUT / PRIVACY / CONTACT / 404 ----------
write("about/index.html", head("About MeasureStack — What This Site Is", "MeasureStack (working name) provides free static material estimators. No accounts, no scraped prices, assumptions shown.",
  SITE_CANON + "/about/", 1) + header(1) + "<h1>About MeasureStack</h1>"
  "<section class=\"card\"><p><strong>MeasureStack</strong> is a temporary working brand for a free, static collection of construction material estimators. Audience: DIYers, homeowners, builders, contractors, tradespeople and renovators asking “how much material do I need?”</p>"
  "<p>Principles: calculations run 100% in your browser; product assumptions (bag yields, coverage) are editable and stated; purchase quantities round up; cost estimates use only prices you enter; no scraped store prices; no accounts; no external APIs.</p>"
  "<p>Estimates only — verify with manufacturer specs and local building code. Structural work (footings, stairs, roofs) needs professional design where code requires it.</p></section>" + footer(1))
write("privacy/index.html", head("Privacy — MeasureStack", "Privacy: no accounts, no analytics by default, unit preference stored locally on your device only.",
  SITE_CANON + "/privacy/", 1) + header(1) + "<h1>Privacy</h1>"
  "<section class=\"card\"><p>No accounts. No server-side tracking. The only stored item is your unit preference (imperial/metric), kept in your browser's local storage — and the site works if storage is unavailable (it simply defaults to imperial). No data leaves your device for calculations.</p></section>" + footer(1))
write("contact/index.html", head("Contact — MeasureStack", "Contact the MeasureStack maintainer: corrections to formulas and assumptions welcome.",
  SITE_CANON + "/contact/", 1) + header(1) + "<h1>Contact</h1>"
  "<section class=\"card\"><p>Found a formula error or a bad default assumption? Open an issue on the GitHub repository (<code>money</code>) with the page URL, your inputs, expected vs actual result, and the manufacturer spec that disagrees. No account on this site is needed.</p></section>" + footer(1))
write("404.html", head("Page not found — MeasureStack", "The page you requested does not exist. Browse estimators instead.",
  SITE_CANON + "/404.html", 0) + header(0) + "<h1>Page not found</h1><p><a href=\"" + BASE + "/\">Back to all estimators</a></p>" + footer(0))

# ---------- robots + sitemap (static) ----------
open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write("User-agent: *\nAllow: /\n\nSitemap: " + SITE_CANON + "/sitemap.xml\n")
urls = [SITE_CANON + "/"]
for c in CATS: urls.append(SITE_CANON + "/" + c + "/")
for s, v in T.items(): urls.append(SITE_CANON + "/" + v["cat"] + "/" + s + "/")
urls += [SITE_CANON + "/guides/", SITE_CANON + "/about/", SITE_CANON + "/privacy/", SITE_CANON + "/contact/"]
for g in GUIDES: urls.append(SITE_CANON + "/guides/" + g + "/")
sm = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n"
for u in urls: sm += "  <url><loc>" + u + "</loc></url>\n"
sm += "</urlset>\n"
open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(sm)
print("pages done. sitemap urls:", len(urls))
