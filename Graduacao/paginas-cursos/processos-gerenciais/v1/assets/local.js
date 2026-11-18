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
    var facts = widget.classList.contains('elementor-element-28e351a6');
    function layout() {
      var p = bp();
      if (facts && window.innerWidth <= 1280) { track.querySelectorAll('.swiper-slide').forEach(function (sl) { sl.style.removeProperty('flex'); sl.style.removeProperty('width'); sl.style.removeProperty('margin-right'); }); return; }
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

// Carrosséis do Jet Engine (disciplinas e professores): o original rolava sozinho com setas; aqui rola por encaixe, com setas, pontos e teclado
// (sem rotação automática: movimento que o usuário não controla fere a WCAG 2.2.2). No WordPress o próprio Jet entrega as setas.
(function () {
  var L = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg>';
  var R = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>';
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.jet-listing-grid__slider').forEach(function (sl) {
    var track = sl.querySelector('.jet-listing-grid__items');
    if (!track || track.children.length < 2) return;
    var label = sl.querySelector('.elementor-element-743a018') ? 'Disciplinas do curso' : sl.querySelector('.elementor-element-d61b7e4') ? 'Corpo docente' : 'Carrossel';
    sl.setAttribute('role', 'region'); sl.setAttribute('aria-roledescription', 'carrossel'); sl.setAttribute('aria-label', label);
    track.setAttribute('tabindex', '0'); track.setAttribute('role', 'group'); track.setAttribute('aria-label', label + '. Use as setas do teclado para navegar.');
    var split = label === 'Corpo docente';
    var bar = document.createElement('div'); bar.className = 'ph-car' + (split ? ' ph-car--split' : '');
    bar.innerHTML = (split ? '<span class="ph-car__title" aria-hidden="true">Professores</span>' : '')
      + '<div class="ph-car__nav"><button type="button" class="ph-car__btn" data-d="-1" aria-label="Anterior">' + L + '</button><button type="button" class="ph-car__btn" data-d="1" aria-label="Próximo">' + R + '</button></div><div class="ph-car__dots" role="group" aria-label="Posição no carrossel"></div><span class="ph-car__status" aria-live="polite"></span>';
    sl.parentNode.insertBefore(bar, sl.nextSibling);
    var prev = bar.querySelector('[data-d="-1"]'), next = bar.querySelector('[data-d="1"]'), dots = bar.querySelector('.ph-car__dots'), st = bar.querySelector('.ph-car__status');
    function step() { return track.children[0].getBoundingClientRect().width; }
    function maxL() { return track.scrollWidth - track.clientWidth; }
    function pages() { return Math.max(1, Math.round(maxL() / step()) + 1); }
    function go(i) { track.scrollTo({ left: Math.min(i * step(), maxL()), behavior: reduce ? 'auto' : 'smooth' }); }
    function build() {
      var n = pages(); if (dots.children.length === n) return;
      dots.innerHTML = '';
      for (var i = 0; i < n; i++) (function (i) {
        var b = document.createElement('button'); b.type = 'button'; b.className = 'ph-car__dot';
        b.setAttribute('aria-label', 'Ir para a posição ' + (i + 1) + ' de ' + n); b.addEventListener('click', function () { go(i); }); dots.appendChild(b);
      })(i);
      dots.style.display = n > 1 ? 'flex' : 'none';
    }
    function update() {
      build(); var n = pages(), i = track.scrollLeft >= maxL() - 2 ? n - 1 : Math.round(track.scrollLeft / step());
      i = Math.max(0, Math.min(i, n - 1));
      prev.disabled = track.scrollLeft <= 2; next.disabled = track.scrollLeft >= maxL() - 2;
      [].forEach.call(dots.children, function (d, k) { if (k === i) d.setAttribute('aria-current', 'true'); else d.removeAttribute('aria-current'); });
      st.textContent = 'Posição ' + (i + 1) + ' de ' + n;
    }
    prev.addEventListener('click', function () { track.scrollBy({ left: -step(), behavior: reduce ? 'auto' : 'smooth' }); });
    next.addEventListener('click', function () { track.scrollBy({ left: step(), behavior: reduce ? 'auto' : 'smooth' }); });
    track.addEventListener('scroll', function () { window.requestAnimationFrame(update); }, { passive: true });
    track.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); next.click(); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); prev.click(); }
      else if (e.key === 'Home') { e.preventDefault(); go(0); }
      else if (e.key === 'End') { e.preventDefault(); go(pages() - 1); }
    });
    window.addEventListener('resize', update); update();
  });
})();

// Banner de matrículas: o bloco todo leva ao link do selo (o link continua sendo o destino de teclado e de leitor de tela)
(function () {
  var box = document.querySelector('.elementor-element-26c43c4e');
  var link = box && box.querySelector('a[href]');
  if (!link) return;
  box.addEventListener('click', function (e) { if (e.target.closest('a')) return; link.click(); });
})();

// Minibio dos professores: truncada em 4 linhas; um "Ver mais" abre as minibios de todos os cartões
(function () {
  document.querySelectorAll('.jet-listing-grid__items').forEach(function (track) {
    var bios = track.querySelectorAll('.elementor-element-e3ca74d.professor-bio');
    if (!bios.length) return;
    var items = [];
    bios.forEach(function (bio) {
      var b = document.createElement('button'); b.type = 'button'; b.className = 'ph-more'; b.textContent = 'Ver mais'; b.setAttribute('aria-expanded', 'false');
      bio.parentNode.insertBefore(b, bio.nextSibling); items.push({ bio: bio, b: b });
    });
    function measure() {
      var open = track.classList.contains('ph-bios-open');
      items.forEach(function (o) { o.b.style.visibility = (open || o.bio.scrollHeight > o.bio.clientHeight + 2) ? 'visible' : 'hidden'; });
    }
    function toggle() {
      var open = track.classList.toggle('ph-bios-open');
      items.forEach(function (o) { o.b.textContent = open ? 'Ver menos' : 'Ver mais'; o.b.setAttribute('aria-expanded', open); });
      measure();
    }
    items.forEach(function (o) { o.b.addEventListener('click', toggle); });
    measure(); window.addEventListener('resize', measure);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);
  });
})();

// Foto dos professores: o fundo do cartão (foto) vira um <img> de verdade na área da foto, com texto alternativo.
// Assim a foto não aparece por baixo do véu branco nos cantos arredondados e leitores de tela recebem o nome.
(function () {
  document.querySelectorAll('.elementor-element-d61b7e4').forEach(function (card) {
    var m = getComputedStyle(card).backgroundImage.match(/url\(["']?([^"')]+)["']?\)/);
    var area = card.querySelector('.elementor-element-f829ee6');
    if (!m || !area) return;
    var nameEl = card.querySelector('.elementor-element-eff8e2a');
    var img = document.createElement('img');
    img.src = m[1]; img.loading = 'lazy'; img.className = 'ph-prof-photo';
    img.alt = nameEl ? 'Foto de ' + nameEl.textContent.trim() : '';
    area.appendChild(img);
    card.classList.add('ph-photo');
  });
})();
