(function(){var box=document.getElementById('q'),res=document.getElementById('qr');if(!box)return;
fetch('/money/assets/js/search-index.json'.replace('/money/',window.SITE?window.SITE.BASE_PATH:'/money/')).then(function(r){return r.json()}).then(function(ix){
function go(){var q=box.value.toLowerCase().trim();if(q.length<2){res.innerHTML='';return;}
for(var k in ix.synonyms){if(q.indexOf(k)>-1)q+=' '+ix.synonyms[k];}
var words=q.split(/\s+/);var out=ix.tools.map(function(t){var s=0;words.forEach(function(w){if(t.keys.indexOf(w)>-1)s++;});return{s:s,t:t};}).filter(function(x){return x.s>0}).sort(function(a,b){return b.s-a.s}).slice(0,8);
res.innerHTML=out.length?'<ul>'+out.map(function(x){return '<li><a href="'+x.t.url+'">'+x.t.title+'</a></li>'}).join('')+'</ul>':'<p class="hint">No match — browse categories below.</p>';}
box.addEventListener('input',go);});})();