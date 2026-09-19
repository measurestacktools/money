// Headless functional test of calculators using node with a minimal DOM stub.
const fs = require('fs');
const path = require('path');
const ROOT = __dirname;

let pass = 0, fail = 0;
function ok(name, cond, extra) {
  if (cond) { pass++; console.log('PASS ' + name); }
  else { fail++; console.log('FAIL ' + name + (extra ? ' :: ' + extra : '')); }
}

// minimal DOM stub
function stubEl(values, k) {
  return {
    value: values[k] !== undefined ? values[k] : '',
    innerHTML: '',
    dataset: {},
    setAttribute() {},
    classList: { add() {}, remove() {} },
    querySelectorAll: () => [],
    addEventListener(ev, cb) { this.__cb = cb; },
  };
}
function makeDoc(values) {
  const els = {};
  const handler = {
    get(t, id) { if (!(id in els)) els[id] = stubEl(values, id); return els[id]; },
  };
  const byId = new Proxy({}, handler);
  return {
    getElementById: (id) => byId[id],
    querySelectorAll: () => [],
    addEventListener() {},
    __els: els,
  };
}

const calcSrc = fs.readFileSync(path.join(ROOT, 'assets/js/calc.js'), 'utf8');
const cfgSrc = fs.readFileSync(path.join(ROOT, 'assets/js/site-config.js'), 'utf8');

function runTool(slug, values, unit) {
  const html = fs.readFileSync(path.join(ROOT, values.__cat, slug, 'index.html'), 'utf8');
  const start = html.indexOf('(function(){var unit=');
  const tail = "Calc.show(document.getElementById('r'),__R.html,false);});})();";
  const end = html.indexOf(tail);
  if (start < 0 || end < 0) return { error: 'inline script not found' };
  const snippet = html.slice(start, end + tail.length);
  const document = makeDoc(values);
  const localStorage = { _s: {}, getItem(k) { return k in this._s ? this._s[k] : null; }, setItem(k, v) { this._s[k] = v; } };
  if (unit === 'metric') localStorage.setItem('ms-units', 'metric');
  const window = {};
  const script = `
    var document = arguments[0], localStorage = arguments[1], window = arguments[2];
    var unit = ${JSON.stringify(unit)};
    ${cfgSrc};
    ${calcSrc};
    var Calc = window.Calc || globalThis.Calc;
    ${snippet}
    return document.getElementById('r').innerHTML;
  `;
  // emulate browser-ish globals
  global.window = window;
  try {
    const wrapped = new Function('document', 'localStorage', 'window', script);
    wrapped(document, localStorage, window);
    const cb = document.__els['f'] && document.__els['f'].__cb;
    if (!cb) return { error: 'submit handler not registered' };
    cb({ preventDefault() {} });
    return { html: document.__els['r'].innerHTML };
  } catch (e) { return { error: String(e) }; }
  finally { delete global.window; }
}

// 1. slab imperial normal
let r = runTool('concrete-slab', { __cat: 'concrete-masonry', L: '10', W: '10', Dp: '4', bag: '80', yield: '0.60', waste: '5', price: '' }, 'imperial');
ok('slab imp 10x10x4 -> 1.23 yd, 59 bags', !r.error && r.html.includes('1.23') && r.html.includes('59 bags'), r.error || r.html);
// 2. slab metric: 3x3m x10cm = 0.9 m3
r = runTool('concrete-slab', { __cat: 'concrete-masonry', L: '3', W: '3', Dp: '10', bag: '80', yield: '0.60', waste: '5', price: '' }, 'metric');
ok('slab metric 3x3x0.1 -> 0.9 m3', !r.error && r.html.includes('0.9'), r.error || r.html);
// 3. slab negative -> error message path (Calc.show error). Our harness: snippet throws -> caught by page try/catch which calls Calc.show(...,true). Check no exception escapes.
r = runTool('concrete-slab', { __cat: 'concrete-masonry', L: '-5', W: '10', Dp: '4', bag: '80', yield: '0.60', waste: '5', price: '' }, 'imperial');
ok('slab negative handled (no crash)', !r.error, r.error);
// 4. board feet
r = runTool('board-feet', { __cat: 'lumber-framing', BT: '2', BWd: '4', BLn: '8', BC: '10', BPp: '' }, 'imperial');
ok('boardfeet 2x4x8x10 -> 53.33 BF', !r.error && r.html.includes('53.33'), r.error || r.html);
// 5. tile
r = runTool('tile-estimator', { __cat: 'flooring-tile', TA: '10', TB: '10', TT: '12', TWt: '12', TL2: '10' }, 'imperial');
ok('tile 100sqft 12in -> 110 tiles', !r.error && r.html.includes('110 tiles'), r.error || r.html);
// 6. pitch
r = runTool('roof-pitch', { __cat: 'roofing', PA2: '6', PB2: '12' }, 'imperial');
ok('pitch 6/12 -> 26.6 deg, 1.118', !r.error && r.html.includes('26.6') && r.html.includes('1.118'), r.error || r.html);
// 7. gravel metric
r = runTool('gravel-base', { __cat: 'outdoor-earthwork', GL: '6', GW: '3', GD: '10', GT: '1.4' }, 'metric');
ok('gravel metric no crash + tons shown', !r.error && r.html.includes('tons'), r.error || r.html);
// 8. localStorage unavailable (safeStore fallback)
try {
  const document = makeDoc({ L: '10' });
  const badStore = new Proxy({}, { get() { throw new Error('denied'); } });
  const fn = new Function('document', 'localStorage', 'window', cfgSrc + '; return window.safeStore.get("x","fb");');
  ok('safeStore fallback without localStorage', fn(document, badStore, {}) === 'fb');
} catch (e) { ok('safeStore fallback without localStorage', false, String(e)); }

console.log(`\nTOTAL pass=${pass} fail=${fail}`);
process.exit(fail ? 1 : 0);
