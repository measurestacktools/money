#!/usr/bin/env python3
"""Generate MeasureStack static site: 30 tool pages with unique SEO content."""
import os, json

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "/money"

CATS = {
 "concrete-masonry": ("Concrete & Masonry", "Slabs, bags, footings, block, brick, mortar and rebar — how much concrete and masonry do you need?"),
 "lumber-framing": ("Lumber & Framing", "Board feet, stud walls, plywood sheets and decking estimators."),
 "walls-paint": ("Walls, Paint & Insulation", "Drywall, paint, siding and insulation quantities."),
 "flooring-tile": ("Flooring & Tile", "Tile, laminate, carpet and grout estimators."),
 "roofing": ("Roofing & Gutters", "Shingles, metal panels, roof pitch and gutters."),
 "outdoor-earthwork": ("Outdoor & Earthwork", "Gravel, mulch, topsoil, pavers, fences, post holes and stairs."),
}

# slug: (cat, opportunity, title, desc, h1, intro, formula_html, example_html, faqs[(q,a)], related_slugs, inputs_html, compute_js)
T = {}
def tool(slug, cat, opp, title, desc, h1, intro, formula, example, faqs, related, inputs, js):
    T[slug] = dict(cat=cat, opp=opp, title=title, desc=desc, h1=h1, intro=intro,
                   formula=formula, example=example, faqs=faqs, related=related,
                   inputs=inputs, js=js)

U_TOGGLE = '''<div class="units" id="units" role="group" aria-label="Unit system">
<button type="button" data-u="imperial" aria-pressed="true">Feet / inches</button>
<button type="button" data-u="metric" aria-pressed="false">Metric</button></div>'''

def num_field(id_, label, imp, met, extra=""):
    return f'''<div class="field"><label for="{id_}">{label} (<span data-unit-label data-imp="{imp}" data-met="{met}">{imp}</span>)</label>
<input type="number" id="{id_}" inputmode="decimal" min="0" step="any" {extra}></div>'''

# ---------- 30 TOOLS ----------
tool("concrete-slab","concrete-masonry","HIGH",
 "Concrete Slab Calculator — Cubic Yards & Bags | MeasureStack",
 "How much concrete for a slab? Enter length, width and thickness to get cubic yards, cubic feet and estimated bags. Free, no signup.",
 "Concrete Slab Calculator",
 "Enter your slab size to get concrete volume in cubic yards and an estimated number of premix bags. Bag yield is editable because actual yield varies by product — check the bag.",
 "<p><strong>Volume</strong> = length × width × thickness (all converted to a consistent base unit internally, metres). <strong>Cubic yards</strong> = cubic metres ÷ 0.7646. <strong>Bags</strong> = volume ÷ editable yield per bag, rounded up, plus waste %.</p>",
 "<p>Example: 10 ft × 10 ft × 4 in = 33.3 cu ft (0.94 m³) → 1.23 yd³. At 0.60 cu ft per 80-lb bag: 33.3 ÷ 0.60 ≈ 55.6 bags; with 5% waste buy 59.</p>",
 [("How thick should a slab be?","4 in (100 mm) is typical for patios and walkways; 5–6 in for driveways. This tool does not design structural slabs — follow local code."),
  ("Why is bag yield editable?","Because 80-lb bags vary by mix and manufacturer (commonly ~0.60 cu ft but not universal). Check your bag and adjust."),
  ("How much waste should I add?","5–10% is common for slabs to cover spillage and uneven subgrade.")],
 ["concrete-bags","gravel-base","rebar-grid"],
 U_TOGGLE + num_field("L","Length","ft","m") + num_field("W","Width","ft","m") + num_field("Dp","Thickness","in","cm") +
 '''<div class="field"><label for="bag">Bag size</label><select id="bag"><option value="80">80 lb</option><option value="60">60 lb</option><option value="40">40 lb</option></select></div>
 <div class="field"><label for="yield">Yield per bag (cu ft) — check bag, editable</label><input type="number" id="yield" inputmode="decimal" min="0" step="any" value="0.60"></div>
 <div class="field"><label for="waste">Waste %</label><input type="number" id="waste" inputmode="decimal" min="0" step="any" value="5"></div>
 <div class="field"><label for="price">Price per bag (optional, your price)</label><input type="number" id="price" inputmode="decimal" min="0" step="any"></div>''',
 '''var u=unit;var L=Calc.lenToM(document.getElementById('L').value,unit==='metric'?'m':'ft');
 var W=Calc.lenToM(document.getElementById('W').value,unit==='metric'?'m':'ft');
 var D=Calc.lenToM(document.getElementById('Dp').value,unit==='metric'?'cm':'in');
 L=Calc.nonNeg(L,'Length');W=Calc.nonNeg(W,'Width');D=Calc.nonNeg(D,'Thickness');
 if(!(L>0&&W>0&&D>0))throw new Error('Enter length, width and thickness greater than zero.');
 var m3=L*W*D,yd3=m3/0.764554857984,cuft=m3*35.314666721;
 var y=Calc.nonNeg(document.getElementById('yield').value,'Yield');if(!(y>0))throw new Error('Yield must be greater than zero.');
 var w=Calc.nonNeg(document.getElementById('waste').value,'Waste');var bags=cuft/y,buy=Math.ceil(bags*(1+w/100)-1e-9);
 var p=document.getElementById('price').value,extra='';
 if(p!==''&&Number(p)>=0&&buy>0){extra='<br>Est. cost (at YOUR price): $'+Calc.fmt(buy*Number(p))+' — not a market price.'}
 return {html:'Volume: <strong>'+Calc.fmt(yd3)+' cu yd</strong> ('+Calc.fmt(cuft)+' cu ft / '+Calc.fmt(m3)+' m³)<br>Calculated bags: '+Calc.fmt(bags,1)+'<br><span class="buy">Buy: '+buy+' bags</span> (rounded up + '+w+'% waste)'+extra+
 '<br><span class="hint">Assumption: yield '+y+' cu ft/bag (editable). Actual yield varies — check bag.</span>'};''')

tool("concrete-bags","concrete-masonry","HIGH",
 "Concrete Bag Calculator — How Many Bags? | MeasureStack",
 "Know your volume in cubic feet or yards? Convert it to 40, 60 or 80-lb premix bags with editable yield. Fast jobsite math.",
 "Concrete Bag Calculator",
 "If you already know the volume (for example from the slab tool), convert it to bags here. Yield per bag is editable — never assume one universal number.",
 "<p><strong>Bags</strong> = volume ÷ editable yield per bag, rounded up, plus waste %.</p>",
 "<p>Example: 20 cu ft ÷ 0.60 cu ft per 80-lb bag = 33.3 → 34 bags; with 5% waste buy 35.</p>",
 [("What is the yield of an 80-lb bag?","Commonly about 0.60 cu ft, but it varies by product. This tool defaults to 0.60 and lets you change it."),
  ("40 vs 60 vs 80-lb bags?","Bigger bags mean fewer bags to carry and mix; the math is identical — volume divided by yield.")],
 ["concrete-slab","post-holes","fence-estimator"],
 U_TOGGLE + num_field("V","Volume","cu ft","m³") + '''<div class="field"><label for="vu">Volume unit</label><select id="vu"><option value="cuft">cubic feet</option><option value="yd3">cubic yards</option><option value="m3">cubic metres</option></select></div>
 <div class="field"><label for="yield2">Yield per bag (cu ft)</label><input type="number" id="yield2" inputmode="decimal" min="0" step="any" value="0.60"></div>
 <div class="field"><label for="waste2">Waste %</label><input type="number" id="waste2" inputmode="decimal" min="0" step="any" value="5"></div>''',
 '''var vu=document.getElementById('vu').value;var V=Calc.nonNeg(document.getElementById('V').value,'Volume');
 var cuft=V*(vu==='yd3'?27:(vu==='m3'?35.314666721:1));if(!(cuft>0))throw new Error('Enter a volume greater than zero.');
 var y=Calc.nonNeg(document.getElementById('yield2').value,'Yield');if(!(y>0))throw new Error('Yield must be greater than zero.');
 var w=Calc.nonNeg(document.getElementById('waste2').value,'Waste');var bags=cuft/y,buy=Math.ceil(bags*(1+w/100)-1e-9);
 return {html:'Calculated: '+Calc.fmt(bags,1)+' bags<br><span class="buy">Buy: '+buy+' bags</span> (rounded up + '+w+'% waste)'};''')

tool("footings-piers","concrete-masonry","MEDIUM",
 "Concrete Footing & Pier Calculator | MeasureStack",
 "Estimate concrete for strip footings and round piers. Length, width, depth or diameter — yards and bags with editable yield.",
 "Footing & Pier Calculator",
 "Choose strip footings (rectangular trench) or round piers, enter dimensions and count, and get volume plus bag estimates.",
 "<p>Strip: V = L × W × D. Round pier: V = π × (d/2)² × depth × count. Convert to yards; bags = V ÷ yield.</p>",
 "<p>Example: trench 20 ft × 12 in × 12 in = 20 cu ft = 0.74 yd³ → ~34 eighty-lb bags at 0.60 cu ft each.</p>",
 [("How deep should footings be?","Below local frost depth and per code — this tool estimates volume only, not structural design.")],
 ["concrete-slab","concrete-bags","rebar-grid"],
 U_TOGGLE + '''<div class="field"><label for="ft">Type</label><select id="ft"><option value="strip">Strip footing</option><option value="pier">Round piers</option></select></div>'''
 + num_field("FL","Length (strip) / depth (pier)","ft","m") + num_field("FW","Width / diameter","in","cm") + num_field("FD","Depth (strip only)","in","cm") + num_field("N","Count (piers; 1 for strip)","count","count"),
 '''var t=document.getElementById('ft').value;
 var m3;
 if(t==='strip'){var L=Calc.lenToM(document.getElementById('FL').value,'ft');var W=Calc.lenToM(document.getElementById('FW').value,'in');var D=Calc.lenToM(document.getElementById('FD').value,'in');
 L=Calc.nonNeg(L,'Length');W=Calc.nonNeg(W,'Width');D=Calc.nonNeg(D,'Depth');if(!(L>0&&W>0&&D>0))throw new Error('Enter all strip dimensions.');m3=L*W*D;}
 else{var Dp=Calc.lenToM(document.getElementById('FL').value,'ft');var Di=Calc.lenToM(document.getElementById('FW').value,'in');var N=Calc.nonNeg(document.getElementById('N').value,'Count');
 Dp=Calc.nonNeg(Dp,'Depth');Di=Calc.nonNeg(Di,'Diameter');if(!(Dp>0&&Di>0&&N>0))throw new Error('Enter depth, diameter and count.');m3=Math.PI*Math.pow(Di/2,2)*Dp*N;}
 var yd3=m3/0.764554857984,cuft=m3*35.314666721,bags=cuft/0.60,buy=Math.ceil(bags*1.05-1e-9);
 return {html:'Volume: <strong>'+Calc.fmt(yd3)+' cu yd</strong> ('+Calc.fmt(cuft)+' cu ft)<br>~'+Calc.fmt(bags,1)+' eighty-lb bags (0.60 cu ft — verify bag)<br><span class="buy">Buy: '+buy+' bags</span> (+5% waste)'};''')

tool("block-wall","concrete-masonry","MEDIUM",
 "Concrete Block Calculator — Blocks & Mortar | MeasureStack",
 "How many concrete blocks and how much mortar for a wall? Enter wall size; get blocks, mortar bags and waste allowance.",
 "Concrete Block Calculator",
 "Standard 16×8-in blocks cover about 0.89 sq ft each in a wall (with mortar joint) — an assumption you can adjust. Get block count plus mortar.",
 "<p>Wall area = L × H. Blocks = area ÷ editable coverage per block, rounded up + waste. Mortar ≈ 0.15 cu ft per block (editable).</p>",
 "<p>Example: 20 ft × 4 ft = 80 sq ft ÷ 0.89 ≈ 90 blocks; +5% → buy 95.</p>",
 [("Do I subtract windows and doors?","Yes — enter net wall area after subtracting openings for best accuracy."),
  ("How much mortar per block?","Roughly 0.1–0.2 cu ft per standard block depending on joint; default 0.15, editable.")],
 ["brick-wall","mortar-mix","rebar-grid"],
 U_TOGGLE + num_field("BL","Wall length","ft","m") + num_field("BH","Wall height","ft","m") + num_field("COV","Coverage per block (sq ft)","sq ft","sq ft") + num_field("BW","Waste %","%","%"),
 '''var L=Calc.lenToM(document.getElementById('BL').value,'ft');var H=Calc.lenToM(document.getElementById('BH').value,'ft');
 var A=L*H/0.09290304;L=Calc.nonNeg(L,'L');H=Calc.nonNeg(H,'H');if(!(L>0&&H>0))throw new Error('Enter wall length and height.');
 var cov=document.getElementById('COV').value===''?'0.89':document.getElementById('COV').value;cov=Number(cov);if(!(cov>0))throw new Error('Coverage must be positive.');
 var w=document.getElementById('BW').value===''?'5':document.getElementById('BW').value;w=Number(w);
 var n=A/cov,buy=Math.ceil(n*(1+w/100)-1e-9);var mortarCuFt=n*0.15,mortarBags=mortarCuFt/0.60;
 return {html:'Wall area: '+Calc.fmt(A)+' sq ft<br>Calculated: '+Calc.fmt(n,1)+' blocks<br><span class="buy">Buy: '+buy+' blocks</span> (+'+w+'%)<br>Mortar ≈ '+Calc.fmt(mortarCuFt)+' cu ft (~'+Calc.fmt(mortarBags,1)+' 80-lb bags at 0.60 cu ft — verify product)'};''')

tool("brick-wall","concrete-masonry","MEDIUM",
 "Brick Calculator — Bricks & Mortar | MeasureStack",
 "Estimate bricks for a wall with openings subtracted. Uses editable bricks-per-sq-ft (default 6.5 for standard running bond).",
 "Brick Calculator",
 "Enter net wall area to get brick count plus mortar estimate. Bricks-per-sq-ft varies by brick size and joint — adjust the default.",
 "<p>Bricks = net area × editable bricks-per-sq-ft, rounded up + waste.</p>",
 "<p>Example: 100 sq ft × 6.5 = 650 bricks; +7% cuts → buy 696.</p>",
 [("What about soldier courses and patterns?","Patterns change consumption — add extra waste (10–15%) for cuts and patterns.")],
 ["block-wall","mortar-mix","siding-estimator"],
 U_TOGGLE + num_field("RL","Wall length","ft","m") + num_field("RH","Wall height","ft","m") + num_field("OP","Openings area","sq ft","m²") + num_field("BP","Bricks per sq ft (editable)","each","each"),
 '''var L=Calc.lenToM(document.getElementById('RL').value,'ft');var H=Calc.lenToM(document.getElementById('RH').value,'ft');
 if(!(L>0&&H>0))throw new Error('Enter wall dimensions.');
 var A=L*H/0.09290304;var opRaw=Number(document.getElementById('OP').value||0);var op=unit==='metric'?opRaw/0.09290304:opRaw;var net=Math.max(0,A-op);
 var bp=document.getElementById('BP').value===''?'6.5':document.getElementById('BP').value;bp=Number(bp);if(!(bp>0))throw new Error('Bricks per sq ft must be positive.');
 var n=net*bp,buy=Math.ceil(n*1.07-1e-9);
 return {html:'Net area: '+Calc.fmt(net)+' sq ft<br><span class="buy">Buy: '+buy+' bricks</span> (+7% cuts/waste)<br><span class="hint">Assumes '+bp+' bricks/sq ft — verify for your brick size.</span>'};''')

tool("mortar-mix","concrete-masonry","MEDIUM",
 "Mortar Calculator — Bags for Block & Brick | MeasureStack",
 "How much mortar? Enter blocks/bricks or volume; get cubic feet and bag count with editable bag yield.",
 "Mortar Calculator",
 "Convert masonry units or a target volume into mortar bags. Yield per bag is editable because products differ.",
 "<p>From units: mortar cu ft = units × editable cu ft per unit. Bags = cu ft ÷ editable yield, rounded up.</p>",
 "<p>Example: 100 blocks × 0.15 cu ft = 15 cu ft ÷ 0.60 = 25 eighty-lb bags.</p>",
 [("Does mortar type matter?","Yes — Type N/S/M and pre-mixed vs site-mixed change yield. Check the bag.")],
 ["block-wall","brick-wall","concrete-bags"],
 num_field("MU","Masonry units (0 to use volume instead)","count","count") + num_field("MV","Or mortar volume","cu ft","m³") + num_field("MY","Yield per 80-lb bag (cu ft, editable)","cu ft","cu ft"),
 '''var u=Number(document.getElementById('MU').value||0);var cuft;
 if(u>0){cuft=u*0.15;}else{var v=Number(document.getElementById('MV').value);if(!(v>0))throw new Error('Enter units or a volume.');cuft=v;}
 var y=Number(document.getElementById('MY').value||0.60);if(!(y>0))throw new Error('Yield must be positive.');
 var bags=cuft/y,buy=Math.ceil(bags*1.05-1e-9);
 return {html:'Mortar: '+Calc.fmt(cuft)+' cu ft<br><span class="buy">Buy: '+buy+' bags</span> (+5%)<br><span class="hint">0.15 cu ft/unit and '+y+' cu ft/bag are editable assumptions.</span>'};''')

tool("rebar-grid","concrete-masonry","MEDIUM",
 "Rebar Calculator — Grid for Slabs | MeasureStack",
 "How much rebar for a slab? Enter slab size and bar spacing to get linear feet, pieces and estimated weight.",
 "Rebar Calculator",
 "Rebar forms a grid: bars each way = dimension ÷ spacing + 1. Weight uses standard bar weights (#3 = 0.376 lb/ft, #4 = 0.668 lb/ft).",
 "<p>Bars_x = floor(L/spacing)+1; total length = bars_x×W + bars_y×L. Weight = length × lb/ft.</p>",
 "<p>Example: 20×20 ft slab at 18-in spacing → 14 bars each way → 560 ft of #4 ≈ 374 lb.</p>",
 [("What size rebar for a slab?"," commonly #3 or #4; spacing per plans/code. This tool estimates quantity only, not structural design.")],
 ["concrete-slab","footings-piers","gravel-base"],
 U_TOGGLE + num_field("SL","Slab length","ft","m") + num_field("SW","Slab width","ft","m") + num_field("SP","Bar spacing","in","cm") + '''<div class="field"><label for="BS">Bar size</label><select id="BS"><option value="0.376">#3 (3/8 in)</option><option value="0.668" selected>#4 (1/2 in)</option><option value="1.043">#5 (5/8 in)</option></select></div>''',
 '''var L=Calc.lenToM(document.getElementById('SL').value,'ft')/0.3048;var W=Calc.lenToM(document.getElementById('SW').value,'ft')/0.3048;
 var sp=unit==='metric'?Calc.lenToM(document.getElementById('SP').value,'cm')/0.0254:Number(document.getElementById('SP').value);
 if(!(L>0&&W>0&&sp>0))throw new Error('Enter slab size and spacing.');
 var bx=Math.floor(L*12/sp)+1,by=Math.floor(W*12/sp)+1;var totalFt=bx*W+by*L;var wt=Number(document.getElementById('BS').value);
 var pcs20=Math.ceil(totalFt/20-1e-9);
  return {html:'Grid: '+bx+' × '+by+' bars<br>Total: <strong>'+Calc.fmt(totalFt)+' lin ft</strong> (≈ '+Calc.fmt(totalFt*0.3048)+' m)<br>Weight ≈ '+Calc.fmt(totalFt*wt)+' lb<br><span class="buy">Buy: '+pcs20+' × 20-ft sticks</span> (+order 5–10% lap/waste)'};''')
