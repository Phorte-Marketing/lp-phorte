#!/usr/bin/env python3
"""Aplica o Design System Phorte (tokens + acessibilidade) na v1, sem mudar a estrutura da página.
  1) _shared/v1-local.css  = ajustes locais existentes + bloco DS (tokens de phorte-tokens.css + regras de v1-ds.css)
  2) <curso>/v1/assets/local.css = o mesmo CSS + degradês corrigidos, gerados do site.css de cada curso
  3) <curso>/v1/index.html: só atributos de acessibilidade (aria-label, role, aria-level, id de destino do skip link)
Uso: python -I apply_v1_ds.py [slug ...]   (padrão: administracao)
"""
import os
import json
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SLUGS_ALL = ["educacao-fisica", "administracao", "marketing", "pedagogia", "processos-gerenciais", "recursos-humanos", "traducao-e-interpretacao"]
# Novo layout (DS + ajustes da v1): só os 4 cursos de gestão. Pedagogia, Educação Física e Tradução e Interpretação
# ficam FORA (decisão da empresa): recebem só o CSS base, sem o bloco DS-PHORTE.
SLUGS_DS = ["administracao", "marketing", "processos-gerenciais", "recursos-humanos"]
BEGIN = "/* ==== DS-PHORTE:INICIO"
END = "/* ==== DS-PHORTE:FIM ==== */"
LIGHT_END = "#F83C42"   # fim do degradê vinho (#571314 -> #F83C42): branco sobre ele = 3,7:1; o primário do DS dá 5,0:1
NL = "\n"


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def css_rules(css):
    """Percorre o CSS e devolve (pilha de @-regras, seletor, corpo) de cada regra simples."""
    i, stack, buf = 0, [], ""
    while i < len(css):
        c = css[i]
        if c == "{":
            head = buf.strip()
            if head.startswith("@"):
                stack.append(head)
                buf = ""
                i += 1
                continue
            j = css.index("}", i)
            yield list(stack), head, css[i + 1:j]
            buf, i = "", j + 1
            continue
        if c == "}":
            if stack:
                stack.pop()
            buf = ""
            i += 1
            continue
        buf += c
        i += 1


FLAT = {"#571314": "var(--ph-footer-red)", "#681718": "var(--ph-footer-red)", "#BB2D32": "var(--ph-primary-dark)"}


def gradient_overrides(slug):
    """Degradês vinho do site.css viram cor chapada do DS (texto com degradê vira cor sólida)."""
    site = os.path.join(ROOT, slug, "v1", "assets", "site.css")
    if not os.path.exists(site):
        return ""
    out, seen = [], set()
    for stack, head, body in css_rules(read(site)):
        for m in re.finditer(r"background-image:linear-gradient\([^,]+,\s*(#[0-9A-Fa-f]{6})[^)]*\)", body):
            first = m.group(1).upper()
            if first not in FLAT or "elementor-element-" not in head:
                continue
            if "premium-title" in head:
                decl = "background-image:none!important;-webkit-text-fill-color:var(--ph-footer-red)!important;color:var(--ph-footer-red)!important"
            else:
                decl = "background-image:none!important;background-color:%s!important" % FLAT[first]
            rule = "%s{%s}" % (head, decl)
            for media in reversed(stack):
                rule = "%s{%s}" % (media, rule)
            if rule not in seen:
                seen.add(rule)
                out.append(rule)
    if not out:
        return ""
    head = ("/* Degradês vinho do site.css convertidos em cor chapada (menos ruído, contraste estável)." + NL
            + "   Gerado por _tools/apply_v1_ds.py. No Elementor: tipo de fundo \"Clássico\" com a cor #7D1B1B ou #A81E1E. */" + NL)
    return NL + head + NL.join(out) + NL


def hero_bg(slug, assets_dir):
    """Fundo do hero: usa a imagem *-BG-*.webp que cada curso tem em assets/img."""
    img = os.path.join(assets_dir, "img")
    names = sorted(n for n in os.listdir(img) if "-BG-" in n and n.endswith(".webp")) if os.path.isdir(img) else []
    if not names:
        return ""
    return NL + '.elementor-element.elementor-element-4fc456d7:not(#ph){background-image:url("img/%s")}' % names[0] + NL


def build_css():
    p = os.path.join(ROOT, "_shared", "v1-local.css")
    css = read(p)
    if BEGIN in css:
        css = css[:css.index(BEGIN)].rstrip() + NL
    block = (BEGIN + " — Design System Phorte na v1 (só CSS; fonte: _shared/phorte-tokens.css + _shared/v1-ds.css + _shared/v1-ds-ui.css) ==== */" + NL
             + read(os.path.join(ROOT, "_shared", "phorte-tokens.css")) + NL + read(os.path.join(ROOT, "_shared", "v1-ds.css")) + NL + read(os.path.join(ROOT, "_shared", "v1-ds-ui.css")) + NL + END + NL)
    with open(p, "w", encoding="utf-8") as f:
        f.write(css + NL + block)
    for s in SLUGS_ALL:
        d = os.path.join(ROOT, s, "v1", "assets")
        if os.path.isdir(d):
            with open(os.path.join(d, "local.css"), "w", encoding="utf-8") as f:
                f.write(css + NL + block + gradient_overrides(s) + hero_bg(s, d) if s in SLUGS_DS else css + NL)


# ---- atributos de acessibilidade (por data-id do Elementor; o modelo é o mesmo nos 4 cursos de gestão)
def add_attr_to_tag(html, data_id, tag, attrs):
    """Acrescenta atributos à primeira <tag> dentro do elemento com data-id; ignora os que já existem."""
    i = html.find('data-id="%s"' % data_id)
    if i < 0:
        return html, False
    j = html.find("<%s" % tag, i)
    if j < 0:
        return html, False
    k = html.find(">", j)
    opening = html[j:k]
    add = "".join(' %s="%s"' % (a, v) for a, v in attrs if not re.search(r"\s%s=" % re.escape(a), opening))
    return (html[:k] + add + html[k:]) if add else html, True


MATRIX_ICONS = {"Organização Empresarial": "building-2", "Sustentabilidade Empresarial": "leaf", "Finanças": "piggy-bank",
                "Marketing e Cadeia de Suprimentos": "megaphone", "Gestão de Pessoas e Processos": "users",
                "Gestão de Negócio": "briefcase-business", "Gestão de Marketing": "megaphone", "Marketing e Empreendedorismo": "rocket",
                "Administração do Capital Humano": "users", "Desenvolvimento das Pessoas": "sprout", "Gestão de Mercado": "trending-up", "Gestão Contemporânea": "lightbulb"}
MATRIX_FALLBACK = ["building-2", "leaf", "piggy-bank", "megaphone", "users", "briefcase-business", "trending-up", "lightbulb"]
FACT_ICONS = {"179b3cc5": "graduation-cap", "1405263e": "calendar-clock", "1aeabeb0": "moon", "59778430": "map-pin", "f5315d0": "monitor-play"}


def lucide_svg(name, icons):
    return ('<svg aria-hidden="true" class="e-font-icon-svg ph-lucide" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" '
            'data-lucide="%s">%s</svg>' % (name, icons[name]))


def patch_icons(h, log):
    """Troca os ícones FontAwesome por ícones Lucide, dentro dos próprios widgets de ícone (mesma estrutura)."""
    icons = json.loads(read(os.path.join(ROOT, "_shared", "lucide-icons.json")))
    # caixas de fato do curso
    for did, name in FACT_ICONS.items():
        i = h.find('data-id="%s"' % did)
        j = h.find("<svg", i) if i >= 0 else -1
        if j >= 0 and "ph-lucide" not in h[j:h.find(">", j)]:
            k = h.find("</svg>", j) + len("</svg>")
            h = h[:j] + lucide_svg(name, icons) + h[k:]
            log.append("ok ícone Lucide %s (fato do curso)" % name)
    # cartões de disciplinas: um ícone por cartão, escolhido pelo título que vem logo depois
    pat = re.compile(r'<svg aria-hidden="true" class="e-font-icon-svg e-far-caret-square-right".*?</svg>', re.S)
    pos, n = 0, 0
    while True:
        m = pat.search(h, pos)
        if not m:
            break
        t = re.search(r'jet-listing-dynamic-field__content"[^>]*>\s*([^<]+?)\s*<', h[m.end():m.end() + 3000])
        title = t.group(1).strip() if t else ""
        name = MATRIX_ICONS.get(title) or MATRIX_FALLBACK[n % len(MATRIX_FALLBACK)]  # título novo: ícone pela ordem do cartão
        svg = lucide_svg(name, icons)
        h = h[:m.start()] + svg + h[m.end():]
        pos = m.start() + len(svg)
        n += 1
    log.append("ok %d ícones Lucide nas disciplinas" % n)
    return h



IMPACT_ICONS = {"Group-233-": "banknote", "Group-232-1-": "briefcase-business", "Group-234-1-": "trending-up", "Group-230-1-": "handshake"}
NEWS_ALT = ("Reportagem do jornal O Globo, caderno Economia: no Brasil, quem tem diploma ganha mais que o dobro do trabalhador com ensino médio; "
            "o país tem a maior taxa de empregabilidade e retorno salarial para quem concluiu faculdade, na comparação com países da OCDE.")


def patch_blocks(h, log):
    """Rodapé do site removido (o WordPress já tem o seu), ícones Lucide no impacto e texto alternativo da notícia."""
    n0 = len(h)
    h = re.sub(r"<footer[^>]*elementor-location-footer[^>]*>.*?</footer>", "", h, count=1, flags=re.S)
    log.append("ok rodapé removido" if len(h) < n0 else "-- rodapé já removido")
    icons = json.loads(read(os.path.join(ROOT, "_shared", "lucide-icons.json")))
    for key, name in IMPACT_ICONS.items():
        m = re.search(r"<img[^>]*assets/img/%s[^>]*>" % re.escape(key), h)
        if m:
            svg = ('<svg class="ph-impact-ic" aria-hidden="true" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" data-lucide="%s">%s</svg>'
                   % (name, icons[name]))
            h = h[:m.start()] + svg + h[m.end():]
            log.append("ok ícone Lucide %s (impacto)" % name)
    m = re.search(r'(<img[^>]*assets/img/ganha-o-dobro-8c7140\.png[^>]*?)alt=""', h)
    if m:
        h = h[:m.start()] + m.group(1) + 'alt="%s"' % NEWS_ALT + h[m.end():]
        log.append("ok texto alternativo da notícia")
    return h


def patch_html(slug):
    p = os.path.join(ROOT, slug, "v1", "index.html")
    h = read(p)
    log = []

    def do(data_id, tag, attrs, what):
        nonlocal h
        h, ok = add_attr_to_tag(h, data_id, tag, attrs)
        log.append(("ok " if ok else "-- ") + what)

    # chips do hero: informação (turma, modalidade), não títulos
    for did, what in (("10b58e26", "chip da turma"), ("b7c34b0", "chip da modalidade")):
        h = h.replace('role="paragraph"', 'role="presentation"')
        do(did, "h2", [("role", "presentation")], what + " deixa de ser título")
    # títulos de cartão dentro de seções H2 passam a nível 3
    for did in ["2dfb46", "11e08b6b", "506643e6", "1fa888a0", "77603471", "48a0b3df", "3bcaaae7", "5d3b04f5", "8148694"]:
        do(did, "h2", [("aria-level", "3")], "título de cartão %s vira nível 3" % did)
    # links só com imagem precisam de nome acessível
    do("42a79f6f", "a", [("aria-label", "Fazer o Vestibular Simplificado da Faculdade Phorte")], "link do selo do vestibular")
    if 'aria-label="Consultar o cadastro' not in h:
        h = re.sub(r'(<figure class="wp-caption">\s*<a href="https://emec\.mec\.gov\.br[^"]*")(>)',
                   r'\1 aria-label="Consultar o cadastro da Faculdade Phorte no e-MEC"\2', h, count=1)
    log.append("ok link do e-MEC")
    # carrosséis com rótulos distintos
    for did, label in (("28e351a6", "Dados do curso"), ("807c9b9", "Diferenciais Phorte")):
        i = h.find('data-id="%s"' % did)
        m = re.compile(r'aria-label="Carrossel"').search(h, i) if i >= 0 else None
        if m and m.start() - i < 4000:
            h = h[:m.start()] + 'aria-label="%s"' % label + h[m.end():]
            log.append("ok carrossel %s -> %s" % (did, label))
    h = patch_icons(h, log)
    h = patch_blocks(h, log)
    # destino do skip link "#content"
    if 'id="content"' not in h:
        h = h.replace('<div data-elementor-type="single-page"', '<div id="content" tabindex="-1" data-elementor-type="single-page"', 1)
        log.append("ok destino do skip link (#content)")
    with open(p, "w", encoding="utf-8") as f:
        f.write(h)
    return log


if __name__ == "__main__":
    build_css()
    for s in (sys.argv[1:] or ["administracao"]):
        print(s)
        for line in patch_html(s):
            print("  ", line)
