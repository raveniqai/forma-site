(function () {
  var menu = document.querySelector('.guide-menu');
  if (menu && window.matchMedia('(max-width: 52rem)').matches) menu.removeAttribute('open');
  var box = document.getElementById('guide-search'), out = document.getElementById('guide-results');
  if (!box || !out) return;
  var index = null;
  function load(cb) {
    if (index) return cb();
    fetch(box.dataset.index).then(function (r) { return r.json(); }).then(function (j) { index = j; cb(); });
  }
  function run() {
    var q = box.value.trim().toLowerCase();
    out.textContent = '';
    if (q.length < 2) return;
    var words = q.split(/\s+/);
    var hits = index.map(function (p) {
      var score = 0;
      words.forEach(function (w) {
        if (p.title.toLowerCase().indexOf(w) >= 0) score += 5;
        if (p.summary.toLowerCase().indexOf(w) >= 0) score += 2;
        if (p.text.indexOf(w) >= 0) score += 1; else score -= 100;
      });
      return { p: p, score: score };
    }).filter(function (h) { return h.score > 0; }).sort(function (a, b) { return b.score - a.score; }).slice(0, 12);
    if (!hits.length) { var li = document.createElement('li'); li.textContent = 'Nothing found. Try another word.'; out.appendChild(li); return; }
    hits.forEach(function (h) {
      var li = document.createElement('li'), a = document.createElement('a'), sm = document.createElement('span');
      a.href = box.dataset.root + h.p.url; a.textContent = h.p.title; sm.textContent = ' ' + h.p.summary; sm.className = 'small';
      li.appendChild(a); li.appendChild(sm); out.appendChild(li);
    });
  }
  box.addEventListener('input', function () { load(run); });
})();
