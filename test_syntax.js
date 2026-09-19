// Syntax-check every tool page's inline calculator script with node --check.
const fs = require('fs');
const path = require('path');
const ROOT = __dirname;
const { execSync } = require('child_process');

const idx = JSON.parse(fs.readFileSync(path.join(ROOT, 'assets/js/search-index.json'), 'utf8'));
let bad = 0;
for (const t of idx.tools) {
  const rel = t.url.replace('/money/', '');
  const html = fs.readFileSync(path.join(ROOT, rel, 'index.html'), 'utf8');
  const start = html.indexOf('(function(){var unit=');
  const tail = "Calc.show(document.getElementById('r'),__R.html,false);});})();";
  const end = html.indexOf(tail);
  if (start < 0 || end < 0) { console.log('MISSING SCRIPT ' + t.url); bad++; continue; }
  const js = html.slice(start, end + tail.length);
  const tmp = path.join(ROOT, '_tmp_check.js');
  fs.writeFileSync(tmp, 'var document,window,localStorage;\n' + js);
  try { execSync('node --check ' + tmp, { stdio: 'pipe' }); }
  catch (e) { console.log('SYNTAX FAIL ' + t.url); bad++; }
}
try { fs.unlinkSync(path.join(ROOT, '_tmp_check.js')); } catch (e) {}
console.log(bad === 0 ? 'ALL ' + idx.tools.length + ' INLINE SCRIPTS PARSE OK' : bad + ' FAILURES');
process.exit(bad ? 1 : 0);
