/* Faculdade Phorte · páginas de curso (gestão) · v1 design system. Roda sobre o template do Elementor; não altera a estrutura. */
(function () {
  var ICONS = {"graduation-cap": "<path d=\"M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z\"/><path d=\"M22 10v6\"/><path d=\"M6 12.5V16a6 3 0 0 0 12 0v-3.5\"/>", "calendar-clock": "<path d=\"M16 14v2.2l1.6 1\"/><path d=\"M16 2v4\"/><path d=\"M21 7.5V6a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h3.5\"/><path d=\"M3 10h5\"/><path d=\"M8 2v4\"/><circle cx=\"16\" cy=\"16\" r=\"6\"/>", "moon": "<path d=\"M20.985 12.486a9 9 0 1 1-9.473-9.472c.405-.022.617.46.402.803a6 6 0 0 0 8.268 8.268c.344-.215.825-.004.803.401\"/>", "map-pin": "<path d=\"M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0\"/><circle cx=\"12\" cy=\"10\" r=\"3\"/>", "monitor-play": "<path d=\"M15.033 9.44a.647.647 0 0 1 0 1.12l-4.065 2.352a.645.645 0 0 1-.968-.56V7.648a.645.645 0 0 1 .967-.56z\"/><path d=\"M12 17v4\"/><path d=\"M8 21h8\"/><rect x=\"2\" y=\"3\" width=\"20\" height=\"14\" rx=\"2\"/>", "building-2": "<path d=\"M10 12h4\"/><path d=\"M10 8h4\"/><path d=\"M14 21v-3a2 2 0 0 0-4 0v3\"/><path d=\"M6 10H4a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-2\"/><path d=\"M6 21V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v16\"/>", "leaf": "<path d=\"M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z\"/><path d=\"M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12\"/>", "piggy-bank": "<path d=\"M11 17h3v2a1 1 0 0 0 1 1h2a1 1 0 0 0 1-1v-3a3.16 3.16 0 0 0 2-2h1a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1h-1a5 5 0 0 0-2-4V3a4 4 0 0 0-3.2 1.6l-.3.4H11a6 6 0 0 0-6 6v1a5 5 0 0 0 2 4v3a1 1 0 0 0 1 1h2a1 1 0 0 0 1-1z\"/><path d=\"M16 10h.01\"/><path d=\"M2 8v1a2 2 0 0 0 2 2h1\"/>", "megaphone": "<path d=\"M11 6a13 13 0 0 0 8.4-2.8A1 1 0 0 1 21 4v12a1 1 0 0 1-1.6.8A13 13 0 0 0 11 14H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2z\"/><path d=\"M6 14a12 12 0 0 0 2.4 7.2 2 2 0 0 0 3.2-2.4A8 8 0 0 1 10 14\"/><path d=\"M8 6v8\"/>", "users": "<path d=\"M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2\"/><path d=\"M16 3.128a4 4 0 0 1 0 7.744\"/><path d=\"M22 21v-2a4 4 0 0 0-3-3.87\"/><circle cx=\"9\" cy=\"7\" r=\"4\"/>", "briefcase-business": "<path d=\"M12 12h.01\"/><path d=\"M16 6V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2\"/><path d=\"M22 13a18.15 18.15 0 0 1-20 0\"/><rect width=\"20\" height=\"14\" x=\"2\" y=\"6\" rx=\"2\"/>", "trending-up": "<path d=\"M16 7h6v6\"/><path d=\"m22 7-8.5 8.5-5-5L2 17\"/>", "lightbulb": "<path d=\"M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5\"/><path d=\"M9 18h6\"/><path d=\"M10 22h4\"/>", "rocket": "<path d=\"M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5\"/><path d=\"M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09\"/><path d=\"M9 12a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.4 22.4 0 0 1-4 2z\"/><path d=\"M9 12H4s.55-3.03 2-4c1.62-1.08 5 .05 5 .05\"/>", "sprout": "<path d=\"M14 9.536V7a4 4 0 0 1 4-4h1.5a.5.5 0 0 1 .5.5V5a4 4 0 0 1-4 4 4 4 0 0 0-4 4c0 2 1 3 1 5a5 5 0 0 1-1 3\"/><path d=\"M4 9a5 5 0 0 1 8 4 5 5 0 0 1-8-4\"/><path d=\"M5 21h14\"/>", "banknote": "<rect width=\"20\" height=\"12\" x=\"2\" y=\"6\" rx=\"2\"/><circle cx=\"12\" cy=\"12\" r=\"2\"/><path d=\"M6 12h.01M18 12h.01\"/>", "handshake": "<path d=\"m11 17 2 2a1 1 0 1 0 3-3\"/><path d=\"m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4\"/><path d=\"m21 3 1 11h-2\"/><path d=\"M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3\"/><path d=\"M3 4h8\"/>"};
  var FACT = {"179b3cc5":"graduation-cap","1405263e":"calendar-clock","1aeabeb0":"moon","59778430":"map-pin","f5315d0":"monitor-play"};
  var MATRIX = {"Organização Empresarial":"building-2","Sustentabilidade Empresarial":"leaf","Finanças":"piggy-bank","Marketing e Cadeia de Suprimentos":"megaphone","Gestão de Pessoas e Processos":"users","Gestão de Negócio":"briefcase-business","Gestão de Mercado":"trending-up","Gestão Contemporânea":"lightbulb","Gestão de Marketing":"megaphone","Marketing e Empreendedorismo":"rocket","Administração do Capital Humano":"users","Desenvolvimento das Pessoas":"sprout"};
  var FALLBACK = ["building-2","leaf","piggy-bank","megaphone","users","briefcase-business","trending-up","lightbulb"];
  var IMPACT = {"Group-233.":"banknote","Group-232-1.":"briefcase-business","Group-234-1.":"trending-up","Group-230-1.":"handshake"};
  function svg(name, cls) { return '<svg aria-hidden="true" class="' + cls + '" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" data-lucide="' + name + '">' + ICONS[name] + '</svg>'; }
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return [].slice.call((r || document).querySelectorAll(s)); }
  function el(id) { return $('.elementor-element-' + id); }

  function icons() {
    Object.keys(FACT).forEach(function (id) {
      $$('.elementor-element-' + id).forEach(function (w) {   /* inclui os clones que o Swiper cria para o loop */
        $$('svg, i', w).forEach(function (s) { if (!s.classList.contains('ph-lucide') && s.closest('.elementor-icon')) s.outerHTML = svg(FACT[id], 'e-font-icon-svg ph-lucide'); });
      });
    });
    $$('.elementor-element-743a018').forEach(function (card, i) {
      var old = $('svg.e-far-caret-square-right', card); if (!old) return;
      var t = $('.jet-listing-dynamic-field__content', card), title = t ? t.textContent.trim() : '';
      old.outerHTML = svg(MATRIX[title] || FALLBACK[i % FALLBACK.length], 'e-font-icon-svg ph-lucide');
    });
    $$('.elementor-widget-image img').forEach(function (img) {
      var m = Object.keys(IMPACT).filter(function (k) { return (img.getAttribute('src') || '').indexOf(k) > -1; })[0];
      if (!m || img.parentNode.querySelector('.ph-impact-ic')) return;
      img.insertAdjacentHTML('beforebegin', svg(IMPACT[m], 'ph-impact-ic'));
    });
  }

  function attrs() {
    function set(id, sel, a) { var w = el(id); var t = w && (sel ? $(sel, w) : w); if (t) Object.keys(a).forEach(function (k) { t.setAttribute(k, a[k]); }); }
    ['10b58e26', 'b7c34b0'].forEach(function (id) { set(id, 'h2', { role: 'presentation' }); });
    ['2dfb46', '11e08b6b', '506643e6', '1fa888a0', '77603471', '48a0b3df', '3bcaaae7', '5d3b04f5', '8148694'].forEach(function (id) { set(id, 'h2', { 'aria-level': '3' }); });
    set('42a79f6f', 'a', { 'aria-label': 'Fazer o Vestibular Simplificado da Faculdade Phorte' });
    var emec = $('a[href*="emec.mec.gov.br"]'); if (emec && !emec.getAttribute('aria-label')) emec.setAttribute('aria-label', 'Consultar o cadastro da Faculdade Phorte no e-MEC');
    set('28e351a6', '.swiper', { 'aria-label': 'Dados do curso' });
    set('807c9b9', '.swiper', { 'aria-label': 'Diferenciais Phorte' });
    var main = $('[data-elementor-type="single-page"]'); if (main && !main.id) { main.id = 'content'; main.setAttribute('tabindex', '-1'); }
    var news = el('53d5c0d1'); if (news) { var im = $('img', news); if (im && !im.getAttribute('alt')) im.setAttribute('alt', 'Reportagem do jornal O Globo, caderno Economia: no Brasil, quem tem diploma ganha mais que o dobro do trabalhador com ensino médio'); }
  }

  /* Carrosséis do Jet (disciplinas e professores): Swiper real; sem rotação automática (WCAG 2.2.2), 3/2/1 por vez, setas, pontos e teclado */
  var Larr = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg>', Rarr = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>';
  function sliders() {
    $$('.jet-listing-grid__slider').forEach(function (sl) {
      var sw = sl.swiper; if (!sw || sl.getAttribute('data-ph-car')) return;
      sl.setAttribute('data-ph-car', '1');
      if (sw.autoplay && sw.autoplay.running) sw.autoplay.stop();
      sw.params.autoplay = false;
      sw.params.speed = (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) ? 0 : 300;
      /* rolagem finita: sem loop (o carrossel não volta do último ao primeiro; volta pelo caminho contrário) */
      if (sw.params.loop && sw.loopDestroy) { sw.loopDestroy(); }
      sw.params.loop = false; sw.params.rewind = false;
      var label = $('.elementor-element-743a018', sl) ? 'Disciplinas do curso' : $('.elementor-element-d61b7e4', sl) ? 'Corpo docente' : 'Carrossel', split = label === 'Corpo docente';
      sl.setAttribute('role', 'region'); sl.setAttribute('aria-roledescription', 'carrossel'); sl.setAttribute('aria-label', label);
      /* o Jet pode vir com centerMode: o 1º cartão fica no meio (vazio à esquerda) e as posições não batem com setas/pontos */
      sw.params.centeredSlides = false; sw.params.centeredSlidesBounds = false; sw.params.centerInsufficientSlides = false;
      sw.params.roundLengths = true;   /* larguras inteiras: bordas de 1px não ficam borradas/mais escuras em posições fracionadas */
      sw.params.slidesPerGroup = 1;   /* as setas andam 1 cartão por vez, não o grupo inteiro */
      sw.params.breakpoints = { 0: { slidesPerView: 1, slidesPerGroup: 1 }, 768: { slidesPerView: 2, slidesPerGroup: 1 }, 1025: { slidesPerView: 3, slidesPerGroup: 1 } };
      sw.currentBreakpoint = false; if (sw.setBreakpoint) sw.setBreakpoint(); sw.update(); sw.slideTo(0, 0);
      var bar = document.createElement('div'); bar.className = 'ph-car' + (split ? ' ph-car--split' : '');
      bar.innerHTML = (split ? '<span class="ph-car__title" aria-hidden="true">Professores</span>' : '') +
        '<div class="ph-car__nav"><button type="button" class="ph-car__btn" data-d="-1" aria-label="Anterior">' + Larr + '</button><button type="button" class="ph-car__btn" data-d="1" aria-label="Próximo">' + Rarr + '</button></div><div class="ph-car__dots"></div><span class="ph-car__status" role="status" aria-live="polite"></span>';
      sl.parentNode.insertBefore(bar, sl.nextSibling);
      var dots = $('.ph-car__dots', bar), st = $('.ph-car__status', bar);
      var prevB = $('[data-d="-1"]', bar), nextB = $('[data-d="1"]', bar);
      function per() { return Math.max(1, +sw.params.slidesPerView || 1); }
      function pages() { return Math.max(1, sw.slides.length - per() + 1); }   /* uma posição por cartão */
      function cur() { return Math.max(0, Math.min(pages() - 1, sw.activeIndex)); }
      function build() {
        var n = pages(); if (dots.children.length === n) return; dots.innerHTML = '';
        for (var i = 0; i < n; i++) (function (i) { var b = document.createElement('button'); b.type = 'button'; b.className = 'ph-car__dot'; b.setAttribute('aria-label', 'Ir para a posição ' + (i + 1) + ' de ' + n); b.addEventListener('click', function () { sw.slideTo(i); }); dots.appendChild(b); })(i);
        dots.style.display = n > 1 ? 'flex' : 'none';
      }
      function update() {
        build(); var i = cur(), n = pages();
        [].forEach.call(dots.children, function (d, k) { if (k === i) d.setAttribute('aria-current', 'true'); else d.removeAttribute('aria-current'); });
        prevB.disabled = i <= 0; nextB.disabled = i >= n - 1;   /* sem volta do último para o primeiro */
        st.textContent = 'Posição ' + (i + 1) + ' de ' + n;
      }
      $('[data-d="-1"]', bar).addEventListener('click', function () { sw.slidePrev(); });
      $('[data-d="1"]', bar).addEventListener('click', function () { sw.slideNext(); });
      sl.setAttribute('tabindex', '0');
      sl.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') { e.preventDefault(); sw.slideNext(); } else if (e.key === 'ArrowLeft') { e.preventDefault(); sw.slidePrev(); } });
      sw.on('loopFix', function () { numbering(); }); sw.on('slideChangeTransitionEnd', function () { numbering(); });
      sw.on('slideChange', update); sw.on('breakpoint', function () { build(); update(); }); sw.on('resize', update); update();
      /* o foco num botão de um cartão fora da vista faria o navegador rolar o overflow:hidden do carrossel (cartões cortados/deslocados): traz o cartão para a vista */
      sl.addEventListener('scroll', function () { if (sl.scrollLeft) sl.scrollLeft = 0; });
      sl.addEventListener('focusin', function (e) {
        var s = e.target.closest && e.target.closest('.swiper-slide'); if (!s) return;
        var k = sw.slides.indexOf(s); if (k < 0) return;
        var a = sw.activeIndex; if (k < a || k >= a + per()) sw.slideTo(k < a ? k : Math.min(k - per() + 1, pages() - 1), 0);
        if (sl.scrollLeft) sl.scrollLeft = 0;
      });
      /* o Swiper guarda tamanhos antes das fontes/imagens/layout final: recalcula quando eles chegam e quando o tamanho muda */
      var refresh = function () { if (sl.swiper) { sw.update(); update(); } };
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(refresh);
      $$('img', sl).forEach(function (im) { if (!im.complete) im.addEventListener('load', refresh); });
      window.addEventListener('resize', function () { clearTimeout(sl._phT); sl._phT = setTimeout(refresh, 120); });
      window.addEventListener('orientationchange', function () { setTimeout(refresh, 300); });
      /* as setas nativas do Jet saem: os controles acima as substituem */
      $$('.jet-listing-grid__slider-icon', sl.parentNode).forEach(function (a) { a.style.display = 'none'; });
    });
  }

  /* banner de matrículas inteiro clicável */
  function banner() { var box = el('26c43c4e'), link = box && $('a[href]', box); if (link) box.addEventListener('click', function (e) { if (!e.target.closest('a')) link.click(); }); }

  /* minibio dos professores: 4 linhas e um "Ver mais" que abre todas */
  function bios() {
    $$('.jet-listing-grid__items').forEach(function (track) {
      var list = $$('.elementor-element-e3ca74d.professor-bio', track); if (!list.length || track.getAttribute('data-ph-bios')) return; track.setAttribute('data-ph-bios', '1');
      var items = list.map(function (bio) { if (bio.nextSibling && bio.nextSibling.className === 'ph-more') return null; var b = document.createElement('button'); b.type = 'button'; b.className = 'ph-more'; b.textContent = 'Ver mais'; b.setAttribute('aria-expanded', 'false'); bio.parentNode.insertBefore(b, bio.nextSibling); return { bio: bio, b: b }; }).filter(Boolean);
      var scope = track.closest('.jet-listing-grid__slider') || track;
      function measure() { var open = scope.classList.contains('ph-bios-open'); items.forEach(function (o) { o.b.style.visibility = (open || o.bio.scrollHeight > o.bio.clientHeight + 2) ? 'visible' : 'hidden'; }); }
      function toggle() { var open = scope.classList.toggle('ph-bios-open'); $$('.ph-more', scope).forEach(function (b) { b.textContent = open ? 'Ver menos' : 'Ver mais'; b.setAttribute('aria-expanded', open); }); measure(); }
      items.forEach(function (o) { o.b.addEventListener('click', toggle); }); measure(); window.addEventListener('resize', measure);
    });
  }

  /* a foto vem de um CSS dinâmico do Jet (por post); se o navegador não a aplicou, lê a URL direto das regras */
  var CSS_TEXT = null;
  function photoUrl(card) {
    var m = getComputedStyle(card).backgroundImage.match(/url\(["']?([^"')]+)["']?\)/);
    if (m) return m[1];
    var item = card.closest('.jet-listing-grid__item'), id = item && (item.className.match(/jet-listing-dynamic-post-(\d+)/) || [])[1];
    if (!id) return null;
    if (CSS_TEXT === null) CSS_TEXT = [].slice.call(document.querySelectorAll('style')).map(function (x) { return x.textContent; }).join('\n');
    var r = CSS_TEXT.match(new RegExp('jet-listing-dynamic-post-' + id + '[^{}]*elementor-element-d61b7e4[^{}]*\\{background-image:url\\("([^"]+)"\\)'));
    return r ? r[1] : null;
  }
  function photos() {
    $$('.elementor-element-d61b7e4').forEach(function (card) {
      if (card.classList.contains('ph-photo')) return;
      var u = photoUrl(card), area = $('.elementor-element-f829ee6', card); if (!u || !area) return;
      var n = $('.elementor-element-eff8e2a', card), img = document.createElement('img');
      img.src = u; img.loading = 'lazy'; img.className = 'ph-prof-photo'; img.alt = n ? 'Foto de ' + n.textContent.trim() : ''; area.appendChild(img); card.classList.add('ph-photo');
    });
  }

  /* número do cartão = posição real da disciplina (data-swiper-slide-index), não a posição no HTML: o Swiper cria cópias para o loop e as reordena */
  function numbering() {
    $$('.jet-listing-grid__slider .swiper-slide').forEach(function (s) {
      var c = $('.elementor-element-743a018', s), i = s.getAttribute('data-swiper-slide-index');
      if (i === null) i = [].indexOf.call(s.parentNode.children, s);   /* sem loop não há atributo: vale a ordem */
      if (c) { var n = +i + 1; c.setAttribute('data-ph-n', (n < 10 ? '0' : '') + n); }
    });
  }
  function run() { icons(); attrs(); sliders(); numbering(); bios(); photos(); }
  /* repete a cada 250ms até os carrosséis do Jet existirem e estarem montados (o Swiper do Jet pode iniciar depois do load).
     O grid pode vir por lazy-load (AJAX, quando a seção entra na tela, a qualquer momento): um observador religa a busca quando o DOM muda. */
  var iv = null, tries = 0;
  function kick() {
    tries = 0; if (iv) return;
    iv = setInterval(function () {
      run(); tries++;
      var pend = $$('.jet-listing-grid__slider').some(function (s) { return !s.getAttribute('data-ph-car'); });
      if ((!pend && tries > 12) || tries > 48) { clearInterval(iv); iv = null; }
    }, 250);
  }
  function start() {
    banner(); run(); kick();
    if (window.MutationObserver) new MutationObserver(function (ms) {
      if (iv) return;
      for (var i = 0; i < ms.length; i++) for (var j = 0; j < ms[i].addedNodes.length; j++) {
        var n = ms[i].addedNodes[j];
        if (n.nodeType === 1 && (n.matches('.jet-listing-grid__slider, .jet-listing-grid__items') || n.querySelector('.jet-listing-grid__slider'))) { kick(); return; }
      }
    }).observe(document.body, { childList: true, subtree: true });
  }
  if (document.readyState === 'complete') start(); else window.addEventListener('load', start);
})();
