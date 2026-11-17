/* Cópia local v1: comportamento mínimo no lugar do JS do WordPress/Elementor. */
(function () {
  function bp() {
    var w = window.innerWidth;
    return w <= 767 ? 'mobile' : w <= 1024 ? 'tablet' : 'desktop';
  }

  function settingsOf(widget) {
    try { return JSON.parse(widget.getAttribute('data-settings') || '{}'); } catch (e) { return {}; }
  }

  function pick(s, key, point, fallback) {
    var v = point === 'desktop' ? s[key] : (s[key + '_' + point] || s[key]);
    var n = parseFloat(v);
    return isNaN(n) ? fallback : n;
  }

  function spacing(s, point) {
    var o = point === 'desktop' ? s.image_spacing_custom : (s['image_spacing_custom_' + point] || s.image_spacing_custom);
    var n = o && parseFloat(o.size);
    return isNaN(n) ? 16 : n;
  }

  // Carrosséis: n slides por vista conforme o breakpoint + botões anterior/próximo
  document.querySelectorAll('.elementor-widget-n-carousel, .elementor-widget-nested-carousel').forEach(function (widget) {
    var track = widget.querySelector('.swiper-wrapper');
    if (!track) return;
    var s = settingsOf(widget);
    function layout() {
      var p = bp();
      var n = pick(s, 'slides_to_show', p, 1);
      var gap = spacing(s, p);
      track.style.setProperty('--phorte-swiper-gap', gap + 'px');
      track.querySelectorAll('.swiper-slide').forEach(function (sl) {
        sl.style.setProperty('flex', '0 0 calc((100% - ' + gap * (n - 1) + 'px) / ' + n + ')', 'important');
        sl.style.setProperty('width', 'auto', 'important');
        sl.style.setProperty('margin-right', '0', 'important');
      });
    }
    layout();
    window.addEventListener('resize', layout);
    widget.querySelectorAll('.elementor-swiper-button-next').forEach(function (b) {
      b.addEventListener('click', function () { track.scrollBy({ left: track.clientWidth * 0.8, behavior: 'smooth' }); });
    });
    widget.querySelectorAll('.elementor-swiper-button-prev').forEach(function (b) {
      b.addEventListener('click', function () { track.scrollBy({ left: -track.clientWidth * 0.8, behavior: 'smooth' }); });
    });
  });

  // Contadores: mostram o valor final
  document.querySelectorAll('.elementor-counter-number').forEach(function (n) {
    var to = n.getAttribute('data-to-value');
    if (to) n.textContent = to;
  });

  // Âncoras vazias não devem rolar para o topo
  document.querySelectorAll('a[href="#"]').forEach(function (a) { a.addEventListener('click', function (e) { e.preventDefault(); }); });
})();
