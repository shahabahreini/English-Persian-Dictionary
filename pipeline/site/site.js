/* Device picker (tabs with deep links) and copy buttons. The page is fully usable without this script. */
(function () {
  var root = document.documentElement;
  root.classList.remove('no-js'); root.classList.add('js');
  var tabs = [].slice.call(document.querySelectorAll('[role=tab]'));
  var panels = [].slice.call(document.querySelectorAll('[role=tabpanel]'));
  if (tabs.length) {
    var ids = tabs.map(function (t) { return t.getAttribute('data-panel'); });
    var show = function (id, focus, push) {
      if (ids.indexOf(id) < 0) id = ids[0];
      tabs.forEach(function (t) {
        var on = t.getAttribute('data-panel') === id;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
        if (on && focus) t.focus();
      });
      panels.forEach(function (p) { p.hidden = p.id !== id; });
      if (push) { try { history.replaceState(null, '', '#' + id); } catch (e) {} }
    };
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function (e) { e.preventDefault(); show(t.getAttribute('data-panel'), false, true); });
      t.addEventListener('keydown', function (e) {
        var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (root.dir === 'rtl') d = -d;
        if (e.key === 'ArrowDown') d = 1; if (e.key === 'ArrowUp') d = -1;
        if (!d) return;
        e.preventDefault();
        show(ids[(i + d + ids.length) % ids.length], true, true);
      });
    });
    var h = (location.hash || '').slice(1);
    show(ids.indexOf(h) >= 0 ? h : ids[0], false, false);
    window.addEventListener('hashchange', function () {
      var x = (location.hash || '').slice(1);
      if (ids.indexOf(x) >= 0) show(x, false, false);
    });
  }
  if (navigator.clipboard) {
    [].forEach.call(document.querySelectorAll('.copy'), function (b) {
      b.hidden = false;
      b.addEventListener('click', function () {
        navigator.clipboard.writeText(b.getAttribute('data-copy')).then(function () {
          var old = b.textContent; b.textContent = b.getAttribute('data-done'); setTimeout(function () { b.textContent = old; }, 1400);
        });
      });
    });
  }
})();
