#!/usr/bin/env python3
"""Build MeasureStack static site — full build. Run: python build_site.py"""
import os, json, re, html

ROOT = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(ROOT, "gen_part1.py"), encoding="utf-8").read())  # defines T, tool, CATS, U_TOGGLE, num_field

def nf(id_, label, imp, met):
    return num_field(id_, label, imp, met)

# ---- remaining 23 tools ----
tool("gravel-base","outdoor-earthwork","HIGH",
 "Gravel Calculator — Cubic Yards & Tons | MeasureStack",
 "How much gravel for a driveway or slab base? Enter area and depth to get cubic yards and tons (editable density).",
 "Gravel Calculator",
 "Gravel is sold by the cubic yard or ton. Enter area and compacted depth; density (tons per yard) is editable because stone varies.",
 "<p>Volume = area × depth (SI base). Yards = m³ ÷ 0.7646. Tons = yards × editable tons/yard (default 1.4).</p>",
 "<p>Example: 20 ft × 10 ft × 4 in = 2.47 yd³ → ≈3.5 tons at 1.4 tons/yd; order ~4 tons with waste.</p>",
 [("How many tons in a yard of gravel?","Commonly 1.3–1.5 tons depending on stone; default 1.4, editable."),
  ("Do I compact before or after measuring?","Enter final compacted depth and add 5–10% for compaction loss.")],
 ["concrete-slab","paver-calculator","topsoil-calculator"],
 U_TOGGLE + nf("GL","Length","ft","m") + nf("GW","Width","ft","m") + nf("GD","Depth","in","cm") + nf("GT","Tons per cubic yard (editable)","tons","tons"),
 '''var L=Calc.lenToM(document.getElementById('GL').value,'ft');var W=Calc.lenToM(document.getElementById('GW').value,'ft');var D=Calc.lenToM(document.getElementById('GD').value,'in');
 if(!(L>0&&W>0&&D>0))throw new Error('Enter length, width and depth.');
 var m3=L*W*D,yd3=m3/0.764554857984;var t=Number(document.getElementById('GT').value||1.4);if(!(t>0))throw new Error('Density must be positive.');
 var tons=yd3*t;return {html:'Volume: <strong>'+Calc.fmt(yd3)+' cu yd</strong> ('+Calc.fmt(m3)+' m³)<br><span class="buy">Order: '+Calc.fmt(tons)+' tons</span> (+5–10% compaction)'};''')

tool("mulch-coverage","outdoor-earthwork","HIGH",
 "Mulch Calculator — Yards & Bags | MeasureStack",
 "How much mulch for beds? Enter bed area and depth to get cubic yards and 2-cu-ft bags.",
 "Mulch Calculator",
 "Mulch depth is usually 2–4 inches. Get bulk yards plus bag count for top-ups.",
 "<p>Volume = area × depth. Yards = cu ft ÷ 27. Bags = cu ft ÷ editable bag size (default 2 cu ft).</p>",
 "<p>Example: 100 sq ft × 3 in = 25 cu ft = 0.93 yd³ → order 1 yard, or thirteen 2-cu-ft bags.</p>",
 [("How deep should mulch be?","2–4 in (5–10 cm); keep it off stems and trunks.")],
 ["topsoil-calculator","gravel-base","paver-calculator"],
 U_TOGGLE + nf("ML","Length","ft","m") + nf("MW","Width","ft","m") + nf("MD","Depth","in","cm"),
 '''var L=Calc.lenToM(document.getElementById('ML').value,'ft');var W=Calc.lenToM(document.getElementById('MW').value,'ft');var D=Calc.lenToM(document.getElementById('MD').value,'in');
 if(!(L>0&&W>0&&D>0))throw new Error('Enter bed size and depth.');
 var m3=L*W*D,cuft=m3*35.314666721,yd3=m3/0.764554857984;var bags=cuft/2;
 return {html:'Volume: <strong>'+Calc.fmt(yd3)+' cu yd</strong> ('+Calc.fmt(cuft)+' cu ft)<br><span class="buy">Buy: '+Math.ceil(yd3*1.05-1e-9)+' yd bulk or '+Math.ceil(bags-1e-9)+' × 2-cu-ft bags</span>'};''')

tool("topsoil-calculator","outdoor-earthwork","HIGH",
 "Topsoil Calculator — Cubic Yards | MeasureStack",
 "How much topsoil to raise a bed or level a lawn? Area × depth to cubic yards with waste.",
 "Topsoil Calculator",
 "Enter area and added depth to get bulk topsoil yards. Topsoil settles — add 10–20% for grading work.",
 "<p>Volume = area × depth → yards = m³ ÷ 0.7646, rounded up + settling allowance.</p>",
 "<p>Example: 200 sq ft × 6 in = 100 cu ft = 3.7 yd³; +15% settling → order 5 yards.</p>",
 [("Will topsoil settle?","Yes — fresh topsoil can settle 10–20%. Order extra and re-grade.")],
 ["mulch-coverage","gravel-base","paver-calculator"],
 U_TOGGLE + nf("TL","Length","ft","m") + nf("TW","Width","ft","m") + nf("TD","Depth","in","cm"),
 '''var L=Calc.lenToM(document.getElementById('TL').value,'ft');var W=Calc.lenToM(document.getElementById('TW').value,'ft');var D=Calc.lenToM(document.getElementById('TD').value,'in');
 if(!(L>0&&W>0&&D>0))throw new Error('Enter area and depth.');
 var m3=L*W*D,yd3=m3/0.764554857984;
 return {html:'Volume: '+Calc.fmt(yd3)+' cu yd<br><span class="buy">Order: '+Calc.fmt(Math.ceil(yd3*1.15-1e-9))+' yd</span> (+15% settling)'};''')

tool("paver-calculator","outdoor-earthwork","HIGH",
 "Paver Calculator — Pavers, Sand & Base | MeasureStack",
 "How many pavers for a patio? Enter patio and paver size to get paver count, joint sand and gravel base.",
 "Paver Calculator",
 "Counts pavers from net area plus cuts, and sizes the gravel base and sand bedding from the same footprint.",
 "<p>Pavers = patio area ÷ paver face area, +10% cuts. Base gravel = area × base depth → yards.</p>",
 "<p>Example: 12×12 ft patio with 4×8-in pavers (0.22 sq ft each): 144 ÷ 0.22 ≈ 648 → buy ~713.</p>",
 [("How much base under pavers?","Commonly 4–6 in compacted gravel + 1 in sand; follow manufacturer specs.")],
 ["gravel-base","concrete-slab","mulch-coverage"],
 U_TOGGLE + nf("PL","Patio length","ft","m") + nf("PW","Patio width","ft","m") + nf("VL","Paver length","in","cm") + nf("VW","Paver width","in","cm"),
 '''var L=Calc.lenToM(document.getElementById('PL').value,'ft');var W=Calc.lenToM(document.getElementById('PW').value,'ft');
 var vl=Calc.lenToM(document.getElementById('VL').value,'in');var vw=Calc.lenToM(document.getElementById('VW').value,'in');
 if(!(L>0&&W>0&&vl>0&&vw>0))throw new Error('Enter patio and paver sizes.');
 var A=L*W,pa=vl*vw,n=A/pa,buy=Math.ceil(n*1.10-1e-9);var baseYd=A*0.1016/0.764554857984;
 return {html:'Patio: '+Calc.fmt(Calc.m2ToSqFt(A))+' sq ft<br><span class="buy">Buy: '+buy+' pavers</span> (+10% cuts)<br>Gravel base (4 in): ≈ '+Calc.fmt(baseYd)+' yd³ + sand bedding ~'+Calc.fmt(A*0.0254/0.764554857984)+' yd³'};''')

tool("board-feet","lumber-framing","HIGH",
 "Board Feet Calculator — Lumber Volume & Cost | MeasureStack",
 "Convert lumber dimensions to board feet and estimate cost. Thickness × width × length ÷ 12, with optional price.",
 "Board Foot Calculator",
 "A board foot = 144 cubic inches. Enter thickness, width, length and piece count; add your price per board foot for cost.",
 "<p>BF per piece = T(in) × W(in) × L(ft) ÷ 12. Total = BF × count. Cost = total × your price.</p>",
 "<p>Example: ten 2×4×8 ft boards: 2×4×8/12 = 5.33 BF each → 53.3 BF total.</p>",
 [("Is a 2×4 really 2 by 4 inches?","No — nominal vs actual: a 2×4 is 1.5×3.5 in. Board feet use nominal sizes by convention; note this onitti your order."),
  ("What about metric?","Enter cm/mm and the tool converts to the board-foot equivalent.")],
 ["stud-wall","plywood-sheets","decking-estimator"],
 U_TOGGLE + nf("BT","Thickness","in","mm") + nf("BWd","Width","in","mm") + nf("BLn","Length","ft","m") + nf("BC","Piece count","count","count") + nf("BPp","Price per board foot (optional)","$","$"),
 '''var u2=unit;var tRaw=Number(document.getElementById('BT').value),wRaw=Number(document.getElementById('BWd').value),lRaw=Number(document.getElementById('BLn').value);
 var tIn=u2==='metric'?tRaw/25.4:tRaw,wIn=u2==='metric'?wRaw/25.4:wRaw,lFt=u2==='metric'?lRaw/0.3048:lRaw;
 if(!(tIn>0&&wIn>0&&lFt>0))throw new Error('Enter thickness, width and length.');
 var c=Number(document.getElementById('BC').value||1);if(!(c>0))throw new Error('Count must be positive.');
 var bf=tIn*wIn*lFt/12,tot=bf*c;var p=document.getElementById('BPp').value,ex='';
 if(p!==''&&Number(p)>=0)ex='<br>Est. cost (YOUR price): $'+Calc.fmt(tot*Number(p));
 return {html:'Per piece: <strong>'+Calc.fmt(bf)+' BF</strong><br>Total: <strong>'+Calc.fmt(tot)+' BF</strong> for '+c+' pcs'+ex};''')

tool("stud-wall","lumber-framing","HIGH",
 "Stud Wall Calculator — Studs, Plates & Blocking | MeasureStack",
 "How many studs for a wall? Enter wall length with 16 or 24-in spacing to get studs, plates and fasteners.",
 "Stud Wall Calculator",
 "Counts studs at on-center spacing plus plates (top + bottom, double top) for a framing shopping list.",
 "<p>Studs = floor(length ÷ spacing) + 1 end stud + corners/openings allowance. Plates = 3 × length (sole + double top).</p>",
 "<p>Example: 12-ft wall at 16 in OC: 12×12/16 = 9 + 1 = 10 studs + 1 extra → buy 11–12.</p>",
 [("16 vs 24-in spacing?","16 in OC is standard for load-bearing; 24 in OC allowed for some non-bearing walls per code.")],
 ["board-feet","plywood-sheets","drywall-calculator"],
 U_TOGGLE + nf("WL","Wall length","ft","m") + '''<div class="field"><label for="OC">Stud spacing</label><select id="OC"><option value="16">16 in on-center</option><option value="24">24 in on-center</option></select></div>''' + nf("WO","Openings (doors/windows)","count","count"),
 '''var Lft=unit==='metric'?Number(document.getElementById('WL').value)/0.3048:Number(document.getElementById('WL').value);
 var oc=Number(document.getElementById('OC').value);var op=Number(document.getElementById('WO').value||0);
 if(!(Lft>0))throw new Error('Enter wall length.');
 var studs=Math.floor(Lft*12/oc)+1+Math.ceil(op*2)+1;var plateFt=Lft*3;
 return {html:'<span class="buy">Buy: '+studs+' studs</span> (incl. ends + openings)<br>Plates: '+Calc.fmt(plateFt)+' lin ft (sole + double top)<br>Nails ≈ '+Math.ceil(studs*8)+' (8/stud avg)'};''')

tool("plywood-sheets","lumber-framing","HIGH",
 "Plywood & Sheet Calculator — 4×8 Sheets | MeasureStack",
 "How many 4×8 sheets for a floor, wall or roof? Area ÷ 32 sq ft plus waste, with metric support.",
 "Plywood Sheet Calculator",
 "Sheathing sheets are 4×8 ft (32 sq ft / 2.98 m²). Enter area to get sheet count with cut waste.",
 "<p>Sheets = area ÷ 32 sq ft (or ÷ 2.98 m²), rounded up + waste %.</p>",
 "<p>Example: 256 sq ft floor ÷ 32 = 8 sheets; +10% → buy 9.</p>",
 [("What about windows and doors?","Enter net area after subtracting large openings.")],
 ["stud-wall","board-feet","drywall-calculator"],
 U_TOGGLE + nf("SA","Area length","ft","m") + nf("SB","Area width","ft","m") + nf("SW2","Waste %","%","%"),
 '''var L=Calc.lenToM(document.getElementById('SA').value,'ft');var W=Calc.lenToM(document.getElementById('SB').value,'ft');
 if(!(L>0&&W>0))throw new Error('Enter area dimensions.');
 var A=L*W,sheets=A/2.975, w=Number(document.getElementById('SW2').value||10);
 var buy=Math.ceil(sheets*(1+w/100)-1e-9);
 return {html:'Area: '+Calc.fmt(Calc.m2ToSqFt(A))+' sq ft<br><span class="buy">Buy: '+buy+' sheets (4×8)</span> (+'+w+'%)'};''')

tool("decking-estimator","lumber-framing","MEDIUM",
 "Decking Calculator — Boards & Screws | MeasureStack",
 "How many deck boards and screws? Deck size + board width gives boards, fasteners and joist hint.",
 "Decking Calculator",
 "Boards run along the length; count = deck width ÷ (board width + gap). Screws ≈ 2 per joist crossing.",
 "<p>Boards = ceil(deckWidth ÷ (boardW + gap)). Fasteners ≈ boards × joists × 2.</p>",
 "<p>Example: 12×16-ft deck, 5.5-in boards: 144 ÷ 5.75 ≈ 26 boards 16 ft long.</p>",
 [("What gap between boards?","About 1/8–1/4 in for drainage; wider for wet lumber that will shrink.")],
 ["board-feet","stud-wall","paint-coverage"],
 U_TOGGLE + nf("DL","Deck length (board direction)","ft","m") + nf("DWw","Deck width","ft","m") + nf("DB","Board width","in","mm"),
 '''var L=Calc.lenToM(document.getElementById('DL').value,'ft');var W=Calc.lenToM(document.getElementById('DWw').value,'ft');var b=Calc.lenToM(document.getElementById('DB').value,'in');
 if(!(L>0&&W>0&&b>0))throw new Error('Enter deck and board sizes.');
 var gap=0.006;var boards=Math.ceil(W/(b+gap)-1e-9);var joists=Math.floor(L/0.4064)+1;var screws=boards*joists*2;
 return {html:'<span class="buy">Buy: '+boards+' boards</span> ('+Calc.fmt(Calc.m2ToSqFt(L)/3.28084)+' ft long)<br>Joists ≈ '+joists+' at 16 in OC<br>Screws ≈ '+screws.toLocaleString()+' (2/joist/board) +5%'};''')

tool("drywall-calculator","walls-paint","HIGH",
 "Drywall Calculator — Sheets, Screws & Mud | MeasureStack",
 "How many drywall sheets, screws and joint compound for a room? Walls + ceiling with openings subtracted.",
 "Drywall Calculator",
 "Sheets from net area ÷ 32 sq ft; screws ≈ 32 per sheet; mud ≈ 1 gallon per 100 sq ft (editable).",
 "<p>Sheets = ceil(netArea ÷ 32) + waste. Screws ≈ sheets × 32. Compound ≈ netArea ÷ 100 gal.</p>",
 "<p>Example: 12×12×8-ft room: walls 2×(12+12)×8 = 384 sq ft + ceiling 144 = 528 − 60 openings = 468 → 468 ÷ 32 = 14.6 sheets; +10% → buy 17.</p>",
 [("4×8 or 4×12 sheets?","4×12 covers faster with fewer seams where it fits through doors and stairs.")],
 ["paint-coverage","insulation-batts","plywood-sheets"],
 U_TOGGLE + nf("RL2","Room length","ft","m") + nf("RW2","Room width","ft","m") + nf("RH2","Ceiling height","ft","m") + nf("RO2","Openings area","sq ft","m²"),
 '''var L=Calc.lenToM(document.getElementById('RL2').value,'ft');var W=Calc.lenToM(document.getElementById('RW2').value,'ft');var H=Calc.lenToM(document.getElementById('RH2').value,'ft');
 if(!(L>0&&W>0&&H>0))throw new Error('Enter room dimensions.');
 var wallM2=2*(L+W)*H,totM2=wallM2+L*W;var op=unit==='metric'?Number(document.getElementById('RO2').value||0):Number(document.getElementById('RO2').value||0)*0.09290304;
 var net=Math.max(0,totM2-op);var sqft=net/0.09290304;var sheets=net/2.975;var buy=Math.ceil(sheets*1.10-1e-9);
 return {html:'Net area: '+Calc.fmt(sqft)+' sq ft<br><span class="buy">Buy: '+buy+' sheets (4×8)</span> (+10%)<br>Screws ≈ '+(buy*32).toLocaleString()+'<br>Joint compound ≈ '+Calc.fmt(sqft/100)+' gal (verify product coverage)'};''')

tool("paint-coverage","walls-paint","HIGH",
 "Paint Calculator — Gallons & Primer | MeasureStack",
 "How much paint for walls and ceiling? Net area ÷ editable coverage per gallon, 1–2 coats plus primer option.",
 "Paint Calculator",
 "Coverage varies by paint and surface (default 350 sq ft/gal, editable). Subtract openings; add coats and waste.",
 "<p>Gallons = netArea × coats ÷ editable coverage, rounded up + waste.</p>",
 "<p>Example: 468 sq ft net × 2 coats ÷ 350 = 2.7 gal → buy 3.</p>",
 [("Do I need primer?","On bare drywall, patches or dramatic color changes — roughly the same quantity as one coat.")],
 ["drywall-calculator","siding-estimator","insulation-batts"],
 U_TOGGLE + nf("PA","Wall area","sq ft","m²") + nf("PC","Coats","count","count") + nf("PV","Coverage per gallon (editable)","sq ft/gal","m²/L"),
 '''var aRaw=Number(document.getElementById('PA').value);var A=unit==='metric'?aRaw:aRaw*0.09290304;
 var coats=Number(document.getElementById('PC').value||2);var covRaw=Number(document.getElementById('PV').value|| (unit==='metric'?9:350));
 var cov=unit==='metric'?covRaw:covRaw*0.09290304;
 if(!(A>0&&coats>0&&cov>0))throw new Error('Enter area, coats and coverage.');
 var gal=A*coats/cov;var liters=gal;var disp=unit==='metric'?Calc.fmt(liters)+' L':Calc.fmt(A/0.09290304*coats/covRaw)+' gal';
 return {html:'Paint needed: '+Calc.fmt(gal,2)+' L equivalent<br><span class="buy">Buy: '+disp+'</span> (rounded up +10% rec.)<br><span class="hint">Coverage '+covRaw+' is an editable assumption — check your paint.</span>'};''')

tool("siding-estimator","walls-paint","MEDIUM",
 "Siding Calculator — Squares & Panels | MeasureStack",
 "How much siding? Net wall area → squares (100 sq ft) plus panels and waste for laps and cuts.",
 "Siding Calculator",
 "One square = 100 sq ft. Vinyl panels vary — count from area with 10–15% cut waste.",
 "<p>Squares = netArea ÷ 100. Panels ≈ squares × panels-per-square (product-specific; default 2 per sq for 12-ft D4).</p>",
 "<p>Example: 1,200 sq ft net = 12 squares; +10% → 13.2 → order 14 squares equivalent.</p>",
 [("Should I include gables?","Yes — measure gable triangles (½×base×height) and add them.")],
 ["paint-coverage","insulation-batts","drywall-calculator"],
 U_TOGGLE + nf("SL2","Wall area","sq ft","m²") + nf("SO2","Openings","sq ft","m²"),
 '''var aRaw=Number(document.getElementById('SL2').value),oRaw=Number(document.getElementById('SO2').value||0);
 var A=unit==='metric'?aRaw:aRaw*0.09290304,O=unit==='metric'?oRaw:oRaw*0.09290304;var net=Math.max(0,A-O);
 if(!(net>0))throw new Error('Enter wall area.');
 var sq=net/9.290304;sq=net/0.09290304/100;
 return {html:'Net: '+Calc.fmt(net/0.09290304)+' sq ft ('+Calc.fmt(net)+' m²)<br><span class="buy">Order: '+Calc.fmt(Math.ceil(sq*1.10-1e-9))+' squares</span> (+10% cuts)<br><span class="hint">Confirm panels-per-square for your product.</span>'};''')

tool("insulation-batts","walls-paint","MEDIUM",
 "Insulation Calculator — Batts & Rolls | MeasureStack",
 "How many insulation batts? Cavity area ÷ batt coverage with joist/stud spacing note.",
 "Insulation Calculator",
 "Coverage per batt varies by product — enter your batt's coverage (sq ft) to get count with cut waste.",
 "<p>Batts = netArea ÷ editable coverage per batt, rounded up + waste.</p>",
 "<p>Example: 500 sq ft attic ÷ 48 sq ft/batt ≈ 10.4 → buy 12.</p>",
 [("What R-value do I need?","Per local energy code and climate zone — this tool counts batts only.")],
 ["drywall-calculator","siding-estimator","paint-coverage"],
 U_TOGGLE + nf("IA","Area","sq ft","m²") + nf("IB","Coverage per batt/pack (sq ft)","sq ft","sq ft"),
 '''var aRaw=Number(document.getElementById('IA').value);var A=unit==='metric'?aRaw:aRaw*0.09290304;
 var cov=Number(document.getElementById('IB').value||48);if(!(A>0&&cov>0))throw new Error('Enter area and batt coverage.');
 var Asq=unit==='metric'?aRaw/0.09290304:aRaw;var n=Asq/cov;return {html:'<span class="buy">Buy: '+Math.ceil(n*1.10-1e-9)+' batts/packs</span> (+10% cuts)<br><span class="hint">Verify coverage and R-value on your product.</span>'};''')

tool("tile-estimator","flooring-tile","HIGH",
 "Tile Calculator — Tiles & Grout | MeasureStack",
 "How many tiles and how much grout? Floor/wall area + tile size → tiles with cut waste and grout estimate.",
 "Tile Calculator",
 "Tile count from area ÷ tile face area; grout in pounds is an editable assumption (default 0.5 lb/sq ft).",
 "<p>Tiles = area ÷ tileArea + waste (10% straight, 15% diagonal). Grout ≈ area × editable lb/sq ft.</p>",
 "<p>Example: 100 sq ft with 12×12-in tile: 100 tiles +10% → 110; grout ≈ 50 lb.</p>",
 [("Straight vs diagonal layout?","Diagonal uses ~15% waste vs ~10% for grid, due to triangle cuts.")],
 ["grout-calculator","laminate-flooring","paint-coverage"],
 U_TOGGLE + nf("TA","Area length","ft","m") + nf("TB","Area width","ft","m") + nf("TT","Tile length","in","cm") + nf("TWt","Tile width","in","cm") + '''<div class="field"><label for="TL2">Layout</label><select id="TL2"><option value="10">Straight (+10%)</option><option value="15">Diagonal (+15%)</option></select></div>''',
 '''var L=Calc.lenToM(document.getElementById('TA').value,'ft');var W=Calc.lenToM(document.getElementById('TB').value,'ft');
 var tl=Calc.lenToM(document.getElementById('TT').value,'in');var tw=Calc.lenToM(document.getElementById('TWt').value,'in');
 if(!(L>0&&W>0&&tl>0&&tw>0))throw new Error('Enter area and tile sizes.');
 var n=(L*W)/(tl*tw);var w=Number(document.getElementById('TL2').value);var buy=Math.ceil(n*(1+w/100)-1e-9);
 var sqft=(L*W)/0.09290304;
 return {html:'Tiles exact: '+Calc.fmt(n,1)+'<br><span class="buy">Buy: '+buy+' tiles</span> (+'+w+'%)<br>Grout ≈ '+Calc.fmt(sqft*0.5)+' lb (0.5 lb/sq ft editable assumption — verify product)'};''')

tool("grout-calculator","flooring-tile","MEDIUM",
 "Grout Calculator — Pounds & Bags | MeasureStack",
 "How much grout? From tile area with editable coverage — verify against manufacturer charts.",
 "Grout Calculator",
 "Grout use depends on tile size, joint width and depth. Default 0.5 lb/sq ft is a planning figure — confirm on the bag chart.",
 "<p>Grout lb = area × editable lb per sq ft. Bags = lb ÷ bag size, rounded up.</p>",
 "<p>Example: 100 sq ft × 0.5 = 50 lb → two 25-lb bags.</p>",
 [("Why is this only an estimate?","Wide joints and small tiles use much more grout; always check the coverage chart.")],
 ["tile-estimator","laminate-flooring","mortar-mix"],
 U_TOGGLE + nf("GA","Tile area","sq ft","m²") + nf("GC","Grout per sq ft in lb (editable)","lb","lb"),
 '''var aRaw=Number(document.getElementById('GA').value);var A=unit==='metric'?aRaw:aRaw*0.09290304;
 var c=Number(document.getElementById('GC').value||0.5);if(!(A>0&&c>0))throw new Error('Enter area and grout rate.');
 var lb=A/c* c;A=A/0.09290304;lb=A*c;
 return {html:'Grout: <strong>'+Calc.fmt(lb)+' lb</strong><br><span class="buy">Buy: '+Math.ceil(lb/25-1e-9)+' × 25-lb bags</span><br><span class="hint">Verify with manufacturer chart for your joint size.</span>'};''')

tool("laminate-flooring","flooring-tile","HIGH",
 "Laminate & Vinyl Floor Calculator | MeasureStack",
 "How many boxes of laminate or vinyl plank? Room area + box coverage → boxes with stagger waste.",
 "Laminate Floor Calculator",
 "Box coverage varies (commonly ~20 sq ft) — enter your box coverage. Stagger waste ~10%.",
 "<p>Boxes = ceil(area ÷ editable box coverage × (1 + waste)).</p>",
 "<p>Example: 200 sq ft ÷ 20 sq ft/box = 10 +10% → 11 boxes.</p>",
 [("Do I need underlayment?","Many laminates need it — order room area +10%; some vinyl has attached pad.")],
 ["tile-estimator","carpet-estimator","paint-coverage"],
 U_TOGGLE + nf("LA","Room length","ft","m") + nf("LB","Room width","ft","m") + nf("LC","Box coverage (sq ft, editable)","sq ft","sq ft"),
 '''var L=Calc.lenToM(document.getElementById('LA').value,'ft');var W=Calc.lenToM(document.getElementById('LB').value,'ft');
 if(!(L>0&&W>0))throw new Error('Enter room size.');
 var sqft=(L*W)/0.09290304;var cov=Number(document.getElementById('LC').value||20);if(!(cov>0))throw new Error('Box coverage must be positive.');
 var boxes=Math.ceil(sqft/cov*1.10-1e-9);
 return {html:'Room: '+Calc.fmt(sqft)+' sq ft<br><span class="buy">Buy: '+boxes+' boxes</span> (+10%)<br>Underlayment ≈ '+Calc.fmt(Math.ceil(sqft*1.10))+' sq ft'};''')

tool("carpet-estimator","flooring-tile","MEDIUM",
 "Carpet Calculator — Sq Yards & Rolls | MeasureStack",
 "How much carpet and pad? Room area → square yards with seam and waste allowance.",
 "Carpet Calculator",
 "Carpet is sold by the square yard (9 sq ft). Rolls are 12 ft wide — seams planned separately.",
 "<p>Sq yd = sq ft ÷ 9. Order +10% (rooms) to +15% (stairs/patterns).</p>",
 "<p>Example: 12×12-ft room = 144 sq ft = 16 sq yd → order ~18.</p>",
 [("What about stairs?","Measure each tread+riser and add 15–20%; patterns need matching allowance.")],
 ["laminate-flooring","tile-estimator","paint-coverage"],
 U_TOGGLE + nf("CA","Room length","ft","m") + nf("CB","Room width","ft","m"),
 '''var L=Calc.lenToM(document.getElementById('CA').value,'ft');var W=Calc.lenToM(document.getElementById('CB').value,'ft');
 if(!(L>0&&W>0))throw new Error('Enter room size.');
 var sqft=(L*W)/0.09290304,sy=sqft/9;
 return {html:'Room: '+Calc.fmt(sqft)+' sq ft = '+Calc.fmt(sy)+' sq yd<br><span class="buy">Order: '+Calc.fmt(Math.ceil(sy*1.10-1e-9))+' sq yd</span> (+10%)<br>Pad: same quantity'};''')

tool("roof-shingles","roofing","HIGH",
 "Roofing Shingle Calculator — Squares & Bundles | MeasureStack",
 "How many shingles? Roof area with pitch multiplier → squares, bundles, felt and nails.",
 "Roof Shingle Calculator",
 "A square = 100 sq ft. Bundles per square vary (default 3, editable). Pitch increases true area.",
 "<p>TrueArea = footprint × pitchMultiplier. Squares = area ÷ 100. Bundles = squares × editable bundles/square.</p>",
 "<p>Example: 1,500 sq ft footprint at 6/12 (×1.118) = 1,677 → 16.8 squares → 53 bundles at 3/square +5% + starter/ridge.</p>",
 [("What is a roofing square?","100 sq ft of roofed area — 17 squares ≈ 1,700 sq ft."),
  ("Do bundles per square vary?","Yes — typically 3–4 depending on shingle type. Check the wrapper.")],
 ["metal-roofing","roof-pitch","gutter-calculator"],
 U_TOGGLE + nf("RA","Roof footprint length","ft","m") + nf("RB","Roof footprint width","ft","m") + nf("RP","Pitch (rise per 12 run)","/12","/12") + nf("RBu","Bundles per square (editable)","count","count"),
 '''var L=Calc.lenToM(document.getElementById('RA').value,'ft');var W=Calc.lenToM(document.getElementById('RB').value,'ft');
 var p=Number(document.getElementById('RP').value||6);if(!(L>0&&W>0))throw new Error('Enter roof footprint.');
 var mult=Math.sqrt(1+Math.pow(p/12,2));var sqft=(L*W)/0.09290304*mult;var sq=sqft/100;
 var b=Number(document.getElementById('RBu').value||3);var bundles=Math.ceil(sq*b*1.05-1e-9);
 return {html:'True roof area ≈ '+Calc.fmt(sqft)+' sq ft ('+Calc.fmt(sq)+' squares, pitch ×'+Calc.fmt(mult,3)+')<br><span class="buy">Buy: '+bundles+' bundles</span> (+5%) + starter + ridge<br>Felt ≈ '+Calc.fmt(Math.ceil(sqft/400))+' rolls · Nails ≈ '+Calc.fmt(Math.ceil(sq*320/7200))+' boxes (verify product)'};''')

tool("metal-roofing","roofing","MEDIUM",
 "Metal Roof Panel Calculator | MeasureStack",
 "How many metal panels and screws? Roof length ÷ editable panel coverage width.",
 "Metal Roof Calculator",
 "Panels are sold by coverage width (default 36-in/0.91-m coverage, editable) and cut to length.",
 "<p>Panels = ceil(slopeWidth ÷ coverageWidth). Screws ≈ panels × length × 2 per foot + trim.</p>",
 "<p>Example: 30-ft eave ÷ 3-ft coverage = 10 panels per slope.</p>",
 [("How much overlap?","Side lap per profile; end lap per manufacturer — add 5–10% trim waste.")],
 ["roof-shingles","roof-pitch","gutter-calculator"],
 U_TOGGLE + nf("MA","Eave width (per slope)","ft","m") + nf("MB","Slope length (eave→ridge)","ft","m") + nf("MC","Panel coverage width (in, editable)","in","mm"),
 '''var W=Calc.lenToM(document.getElementById('MA').value,'ft');var S=Calc.lenToM(document.getElementById('MB').value,'ft');
 var cRaw=Number(document.getElementById('MC').value||(unit==='metric'?914:36));var cM=unit==='metric'?cRaw/1000:cRaw*0.0254;
 if(!(W>0&&S>0&&cM>0))throw new Error('Enter widths and coverage.');
 var panels=Math.ceil(W/cM-1e-9);var screws=Math.ceil(panels*(S/0.3048)*2*1.05);
 return {html:'<span class="buy">Buy: '+panels+' panels per slope</span> (cut to '+Calc.fmt(S/0.3048)+' ft)<br>Screws ≈ '+screws.toLocaleString()+' + trim/flashing per plan'};''')

tool("roof-pitch","roofing","MEDIUM",
 "Roof Pitch Calculator — Angle & Multiplier | MeasureStack",
 "Convert roof rise and run to pitch, angle and area multiplier for shingle and sheathing math.",
 "Roof Pitch Calculator",
 "Pitch = rise per 12-in run. Angle = arctan(rise/run). Multiplier = √(1+(pitch/12)²).",
 "<p>Angle° = atan(rise/run). Area multiplier = hypotenuse ÷ run.</p>",
 "<p>Example: 6/12 → 26.6° → multiplier 1.118.</p>",
 [("Why does pitch matter for materials?","Steeper roofs have more true area than their footprint — multiply footprint by the multiplier.")],
 ["roof-shingles","metal-roofing","plywood-sheets"],
 nf("PA2","Rise","in","cm") + nf("PB2","Run","in","cm"),
 '''var r=Number(document.getElementById('PA2').value),rn=Number(document.getElementById('PB2').value);
 if(!(r>=0&&rn>0))throw new Error('Enter rise and run.');
 var pitch=r/rn*12,ang=Math.atan(r/rn)*180/Math.PI,mult=Math.sqrt(1+Math.pow(r/rn,2));
 return {html:'Pitch: <strong>'+Calc.fmt(pitch,1)+' / 12</strong><br>Angle: '+Calc.fmt(ang,1)+'°<br>Area multiplier: ×'+Calc.fmt(mult,3)};''')

tool("gutter-calculator","roofing","MEDIUM",
 "Gutter Calculator — Length & Downspouts | MeasureStack",
 "How much gutter and how many downspouts? Eave length → gutter feet, hangers and downspouts.",
 "Gutter Calculator",
 "Gutter = eave length + waste. Hangers every ~2 ft. Downspouts roughly every 30–40 ft per eave.",
 "<p>Gutter ft = eaves total × (1+waste). Downspouts = ceil(eave ÷ 35) per run (planning rule).</p>",
 "<p>Example: 60-ft eave → 63 ft gutter (+5%), 2 downspouts, ~30 hangers.</p>",
 [("What size gutters?","5-in K-style suits most homes; 6-in for steep/large roofs — confirm with local practice.")],
 ["roof-shingles","metal-roofing","roof-pitch"],
 U_TOGGLE + nf("GE","Eave length (one run)","ft","m") + nf("GN","Number of eave runs","count","count"),
 '''var e=Calc.lenToM(document.getElementById('GE').value,'ft');var n=Number(document.getElementById('GN').value||1);
 if(!(e>0&&n>0))throw new Error('Enter eave length and runs.');
 var totFt=e/0.3048*n;var gutter=Math.ceil(totFt*1.05);var ds=Math.ceil(e/0.3048/35)*n;var hang=Math.ceil(totFt/2);
 return {html:'Gutter: <strong>'+Calc.fmt(gutter)+' lin ft</strong><br>Downspouts ≈ '+ds+'<br>Hangers ≈ '+hang+' (every ~2 ft)'};''')

tool("fence-estimator","outdoor-earthwork","HIGH",
 "Fence Calculator — Pickets, Posts & Concrete | MeasureStack",
 "How much fence? Linear feet + picket width → pickets, rails, posts and concrete bags per post.",
 "Fence Calculator",
 "Pickets = length ÷ (picket width + gap). Posts every 6–8 ft. Concrete ≈ 1 bag per post (editable by hole size).",
 "<p>Pickets = ceil(L ÷ (w+gap)) + waste. Posts = ceil(L ÷ spacing) + 1.</p>",
 "<p>Example: 100-ft fence, 5.5-in pickets: 1200 ÷ 5.75 ≈ 209 pickets +10% → 230.</p>",
 [("How deep are posts?","Commonly 1/3 of post in ground below frost line — check local code.")],
 ["post-holes","concrete-bags","gravel-base"],
 U_TOGGLE + nf("FL2","Fence length","ft","m") + nf("PW3","Picket width","in","mm") + nf("PS","Post spacing","ft","m"),
 '''var L=Calc.lenToM(document.getElementById('FL2').value,'ft');var pw=Calc.lenToM(document.getElementById('PW3').value,'in');
 var sp=Calc.lenToM(document.getElementById('PS').value,'ft');if(!sp||sp<=0)sp=2.4384;
 if(!(L>0&&pw>0))throw new Error('Enter fence length and picket width.');
 var pickets=Math.ceil(L/(pw+0.006)-1e-9);var buy=Math.ceil(pickets*1.10-1e-9);
 var posts=Math.ceil(L/sp)+1;var rails=Math.ceil(L/0.3048/16)*2;
 return {html:'<span class="buy">Buy: '+buy+' pickets</span> (+10%)<br>Posts: '+posts+' (every '+Calc.fmt(sp/0.3048)+' ft)<br>Rails: ≈ '+rails+' × 16-ft rails<br>Concrete: ≈ '+posts+' bags (1/post — verify hole size in post-hole tool)'};''')

tool("post-holes","outdoor-earthwork","MEDIUM",
 "Post Hole Calculator — Concrete per Hole | MeasureStack",
 "How much concrete per post hole? Diameter × depth × count → cubic feet, yards and bags.",
 "Post Hole Calculator",
 "Cylinder volume per hole: π × (d/2)² × depth × count, minus nothing (post displacement ignored = built-in buffer).",
 "<p>V = πr²h × count → bags = V ÷ yield, rounded up.</p>",
 "<p>Example: ten 12-in × 36-in holes: 10 × 2.36 cu ft ≈ 23.6 cu ft → ~40 eighty-lb bags; +5% → buy 42.</p>",
 [("Should I subtract the post?","No — ignoring it adds a small safety buffer for spillage.")],
 ["fence-estimator","concrete-bags","gravel-base"],
 U_TOGGLE + nf("HD","Hole diameter","in","cm") + nf("HH","Hole depth","in","cm") + nf("HN","Number of holes","count","count"),
 '''var d=Calc.lenToM(document.getElementById('HD').value,'in');var h=Calc.lenToM(document.getElementById('HH').value,'in');
 var n=Number(document.getElementById('HN').value);if(!(d>0&&h>0&&n>0))throw new Error('Enter diameter, depth and count.');
 var m3=Math.PI*Math.pow(d/2,2)*h*n,cuft=m3*35.314666721;var bags=cuft/0.60;
 return {html:'Volume: '+Calc.fmt(cuft)+' cu ft ('+Calc.fmt(m3/0.764554857984)+' yd³)<br><span class="buy">Buy: '+Math.ceil(bags*1.05-1e-9)+' eighty-lb bags</span> (0.60 cu ft editable — verify bag)'};''')

tool("stair-stringer","outdoor-earthwork","MEDIUM",
 "Stair Stringer Calculator — Rise, Run & Steps | MeasureStack",
 "How many steps and how long a stringer? Total rise ÷ target riser height → steps, tread depth and stringer length.",
 "Stair Calculator",
 "Steps = ceil(totalRise ÷ maxRiser). Actual riser = totalRise ÷ steps. Run = steps × tread depth.",
 "<p>Comfort rule: riser 7–7.5 in, tread 10–11 in; check code for max riser/min tread.</p>",
 "<p>Example: 36-in rise ÷ 7.5 = 4.8 → 5 steps × 7.2-in risers; run 5 × 11 = 55 in.</p>",
 [("What is code for stairs?","Commonly max ~7.75-in riser, min ~10-in tread — verify local code; this is planning math.")],
 ["board-feet","plywood-sheets","decking-estimator"],
 U_TOGGLE + nf("TR","Total rise (deck to ground)","in","cm") + nf("MR","Max riser height","in","mm"),
 '''var rise=unit==='metric'?Number(document.getElementById('TR').value)/2.54:Number(document.getElementById('TR').value);
 var mx=unit==='metric'?Number(document.getElementById('MR').value)/25.4:Number(document.getElementById('MR').value);
 if(!(mx>0))mx=7.5;if(!(rise>0))throw new Error('Enter total rise.');
 var steps=Math.ceil(rise/mx-1e-9);var actual=rise/steps;var run=steps*11;
  return {html:'Steps: <strong>'+steps+'</strong> × '+Calc.fmt(actual,2)+'-in risers<br>Total run ≈ '+Calc.fmt(run)+' in ('+Calc.fmt(run/12)+' ft)<br>Stringer ≈ '+Calc.fmt(Math.sqrt(rise*rise+run*run)/12)+' ft long'};''')
