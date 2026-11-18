/* Faculdade Phorte · páginas de curso (gestão) · v1 design system. Roda sobre o template do Elementor; não altera a estrutura. */
(function () {
  var ICONS = __ICONS__;
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
      sw.params.speed = (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) ? 0 : 650;
      var label = $('.elementor-element-743a018', sl) ? 'Disciplinas do curso' : $('.elementor-element-d61b7e4', sl) ? 'Corpo docente' : 'Carrossel', split = label === 'Corpo docente';
      sl.setAttribute('role', 'region'); sl.setAttribute('aria-roledescription', 'carrossel'); sl.setAttribute('aria-label', label);
      sw.params.breakpoints = { 0: { slidesPerView: 1, slidesPerGroup: 1 }, 768: { slidesPerView: 2, slidesPerGroup: 2 }, 1025: { slidesPerView: 3, slidesPerGroup: 3 } };
      sw.currentBreakpoint = false; if (sw.setBreakpoint) sw.setBreakpoint(); sw.update();
      var bar = document.createElement('div'); bar.className = 'ph-car' + (split ? ' ph-car--split' : '');
      bar.innerHTML = (split ? '<span class="ph-car__title" aria-hidden="true">Professores</span>' : '') +
        '<div class="ph-car__nav"><button type="button" class="ph-car__btn" data-d="-1" aria-label="Anterior">' + Larr + '</button><button type="button" class="ph-car__btn" data-d="1" aria-label="Próximo">' + Rarr + '</button></div><div class="ph-car__dots"></div><span class="ph-car__status" role="status" aria-live="polite"></span>';
      sl.parentNode.insertBefore(bar, sl.nextSibling);
      var dots = $('.ph-car__dots', bar), st = $('.ph-car__status', bar);
      function real() { return sw.slides.filter(function (s) { return !s.classList.contains('swiper-slide-duplicate'); }).length; }
      function per() { return Math.max(1, +sw.params.slidesPerView || 1); }
      function pages() { return Math.max(1, Math.ceil(real() / per())); }
      function cur() { return Math.min(pages() - 1, Math.floor((sw.realIndex || 0) / per())); }
      function build() {
        var n = pages(); if (dots.children.length === n) return; dots.innerHTML = '';
        for (var i = 0; i < n; i++) (function (i) { var b = document.createElement('button'); b.type = 'button'; b.className = 'ph-car__dot'; b.setAttribute('aria-label', 'Ir para a posição ' + (i + 1) + ' de ' + n); b.addEventListener('click', function () { sw.slideToLoop(i * per()); }); dots.appendChild(b); })(i);
        dots.style.display = n > 1 ? 'flex' : 'none';
      }
      function update() { build(); var i = cur(), n = pages(); [].forEach.call(dots.children, function (d, k) { if (k === i) d.setAttribute('aria-current', 'true'); else d.removeAttribute('aria-current'); }); st.textContent = 'Posição ' + (i + 1) + ' de ' + n; }
      $('[data-d="-1"]', bar).addEventListener('click', function () { sw.slidePrev(); });
      $('[data-d="1"]', bar).addEventListener('click', function () { sw.slideNext(); });
      sl.setAttribute('tabindex', '0');
      sl.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') { e.preventDefault(); sw.slideNext(); } else if (e.key === 'ArrowLeft') { e.preventDefault(); sw.slidePrev(); } });
      sw.on('slideChange', update); sw.on('breakpoint', function () { build(); update(); }); sw.on('resize', update); update();
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

  function run() { icons(); attrs(); sliders(); bios(); photos(); }
  function start() { banner(); run(); [600, 1500, 3000].forEach(function (t) { setTimeout(run, t); }); }
  if (document.readyState === 'complete') start(); else window.addEventListener('load', start);
})();
