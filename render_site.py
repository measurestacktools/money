#!/usr/bin/env python3
"""Render all MeasureStack HTML pages. Run: python render_site.py"""
import os, json

ROOT = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(ROOT, "build_tools_data.py"), encoding="utf-8").read())

SITE_CANON = "https://rayanbaig796-crypto.github.io/money"
BASE = "/money"
ASSET = lambda depth: ("../" * depth + "assets/")

HEAD = lambda title, desc, canon, depth: f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%230f5fd0'/%3E%3Ctext x='32' y='44' font-size='36' text-anchor='middle' fill='white' font-family='sans-serif' font-weight='bold'%3EM%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="{ASSET(depth)}css/main.css">
</head>"""

HEADER = lambda depth: f"""<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="nav">
<a class="brand" href="{BASE}/"><span data-brand>MeasureStack</span> <small>material estimators</small></a>
<nav aria-label="Main"><a href="{BASE}/">Home</a><a href="{BASE}/guides/">Guides</a><a href="{BASE}/about/">About</a></nav>
</div></header>
<main id="main">"""

FOOTER = lambda depth, scripts=True: f"""</main>
<footer class="site"><div class="inner">
<p><strong><span data-brand>MeasureStack</span></strong> — fast jobsite material estimators. Estimates only; verify with manufacturer specs and local code.</p>
<p><a href="{BASE}/about/">About</a> · <a href="{BASE}/privacy/">Privacy</a> · <a href="{BASE}/contact/">Contact</a> · <a href="{BASE}/sitemap.xml">Sitemap</a></p>
</div></footer>
""" + (f"""<script src="{ASSET(depth)}js/site-config.js"></script>
<script src="{ASSET(depth)}js/assumptions.js"></script>
<script src="{ASSET(depth)}js/calc.js"></script>
""" if scripts else "") + """</body>
</html>"""
SHARED = lambda depth: (f"""<script src="{ASSET(depth)}js/site-config.js"></script>
<script src="{ASSET(depth)}js/assumptions.js"></script>
<script src="{ASSET(depth)}js/calc.js"></script>
""")

def tool_url(slug):
    cat = T[slug]["cat"]
    return f"{BASE}/{cat}/{slug}/"

def render_tool(slug, d):
    depth = 2
    canon = f"{SITE_CANON}/{d['cat']}/{slug}/"
    cat_name = CATS[d["cat"]][0]
    related = "".join(f'<li><a href="{tool_url(r)}">{T[r]["h1"]}</a></li>' for r in d["related"] if r in T)
    faqs = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in d["faqs"])
    faq_schema = ""
    if faqs:
        items = ",".join('{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}' % (json.dumps(q), json.dumps(a)) for q, a in d["faqs"])
        faq_schema = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}</script>' % items
    breadcrumb_schema = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"%s/"},{"@type":"ListItem","position":2,"name":"%s","item":"%s/%s/"},{"@type":"ListItem","position":3,"name":"%s"}]}</script>' % (SITE_CANON, cat_name, SITE_CANON, d["cat"], d["h1"])
    js_raw = d['js'].replace(",'ft')", ",LU)").replace(',"ft")', ",LU)").replace(",'in')", ",SU)").replace(',"in")', ",SU)")
    js_wrap = "var LU=unit==='metric'?'m':'ft',SU=unit==='metric'?'cm':'in';var __R=(function(){" + js_raw + "})()"
    scr = ("<scr" + "ipt>(function(){var unit=window.Calc?Calc.unitSystem('imperial'):'imperial';"
           "if(window.Calc){unit=Calc.bindUnits('units',function(u){unit=u;});}"
           "document.getElementById('f').addEventListener('submit',function(e){e.preventDefault();"
           "try{@@JS@@}catch(err){Calc.show(document.getElementById('r'),'Error: '+err.message,true);return;}"
           "Calc.show(document.getElementById('r'),__R.html,false);});})();</scr" + "ipt>").replace("@@JS@@", js_wrap)
    body = (HEAD(d['title'], d['desc'], canon, depth) + HEADER(depth)
        + '<nav class="breadcrumb" aria-label="Breadcrumb"><a href="' + BASE + '/">Home</a> › <a href="' + BASE + '/' + d['cat'] + '/">' + cat_name + '</a> › ' + d['h1'] + '</nav>\n'
        + "<h1>" + d['h1'] + "</h1>\n<p>" + d['intro'] + "</p>\n"
        + '<section class="card" aria-label="Calculator">\n<form class="calc" id="f" novalidate>\n' + d['inputs']
        + '\n<div><button class="primary" type="submit">Calculate</button></div>\n</form>\n'
        + '<div class="result" id="r" aria-live="polite"><span class="hint">Enter your measurements and press Calculate.</span></div>\n'
        + '<p class="hint">Actual product yields vary — check the manufacturer\'s specs. Estimated cost (if shown) uses YOUR price, not a market price.</p>\n</section>\n'
        + '<section class="card"><h2>Formula</h2>' + d['formula'] + '</section>\n'
        + '<section class="card"><h2>Worked example</h2>' + d['example'] + '</section>\n'
        + '<section class="card"><h2>Questions</h2>' + faqs + '</section>\n'
        + '<section class="card"><h2>Related estimators</h2><ul>' + related + '</ul>\n'
        + '<p><a href="' + BASE + '/' + d['cat'] + '/">' + cat_name + ' estimators</a> · <a href="' + BASE + '/">All estimators</a></p></section>\n'
        + faq_schema + "\n" + breadcrumb_schema + "\n" + SHARED(depth) + scr + "\n" + FOOTER(depth, False))
    out = os.path.join(ROOT, d["cat"], slug, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(body)

for slug, d in T.items():
    render_tool(slug, d)

# ---- search index ----
idx = [dict(slug=s, title=v["h1"], cat=v["cat"], url=f"{BASE}/{v['cat']}/{s}/",
            keys=(v["h1"] + " " + v["title"] + " " + v["cat"]).lower()) for s, v in T.items()]
syn = {"cement": "concrete", "boards": "lumber board feet", "patio": "paver concrete slab",
       "paint walls": "paint drywall", "roof": "shingle metal pitch gutter", "dirt": "topsoil gravel",
       "fence posts": "fence post holes concrete"}
open(os.path.join(ROOT, "assets", "js", "search-index.json"), "w", encoding="utf-8").write(json.dumps({"tools": idx, "synonyms": syn}, indent=1))

open(os.path.join(ROOT, "assets", "js", "search.js"), "w", encoding="utf-8").write("""(function(){var box=document.getElementById('q'),res=document.getElementById('qr');if(!box)return;
fetch('BASE_PLACEHOLDERassets/js/search-index.json'.replace('BASE_PLACEHOLDER',window.SITE?window.SITE.BASE_PATH:'/money/')).then(function(r){return r.json()}).then(function(ix){
function go(){var q=box.value.toLowerCase().trim();if(q.length<2){res.innerHTML='';return;}
for(var k in ix.synonyms){if(q.indexOf(k)>-1)q+=' '+ix.synonyms[k];}
var words=q.split(/\\s+/);var out=ix.tools.map(function(t){var s=0;words.forEach(function(w){if(t.keys.indexOf(w)>-1)s++;});return{s:s,t:t};}).filter(function(x){return x.s>0}).sort(function(a,b){return b.s-a.s}).slice(0,8);
res.innerHTML=out.length?'<ul>'+out.map(function(x){return '<li><a href="'+x.t.url+'">'+x.t.title+'</a></li>'}).join('')+'</ul>':'<p class="hint">No match — browse categories below.</p>';}
box.addEventListener('input',go);});})();""".replace("BASE_PLACEHOLDER", BASE + "/"))

print("tools rendered:", len(T))
