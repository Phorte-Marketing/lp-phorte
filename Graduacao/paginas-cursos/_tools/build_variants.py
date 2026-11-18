#!/usr/bin/env python3
"""Gera v2 e v3 de cada página de curso a partir do conteúdo extraído da v1.

v2 = "Editorial claro"  (fundo claro, hero centrado, faixas alternadas)
v3 = "Impacto Phorte"   (hero vermelho profundo, cards em destaque, salário logo após o hero)

Ambas usam o Design System Phorte (tokens, Poppins local) e a seção de salários direção 02.
Uso: python -I build_variants.py [slug ...]
"""
import glob
import html as H
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SLUGS = ["educacao-fisica", "administracao", "marketing", "pedagogia",
         "processos-gerenciais", "recursos-humanos", "traducao-e-interpretacao"]
NAMES = {"educacao-fisica": "Educação Física", "administracao": "Administração", "marketing": "Marketing",
         "pedagogia": "Pedagogia", "processos-gerenciais": "Processos Gerenciais",
         "recursos-humanos": "Recursos Humanos", "traducao-e-interpretacao": "Tradução e Interpretação"}
LIVE = {"traducao-e-interpretacao": "traducao-e-interpretacao-ingles-portugues"}
SALARY = json.load(open(os.path.join(ROOT, "_shared", "salarios.json"), encoding="utf-8"))

JUNK = re.compile(r"Powered by|GSheetConnector|^Enviar$|^▶$|Fazer Inscrição|^Pular para|^Quero me Inscrever$", re.I)
PRICE = re.compile(r"R\$\s?[\d.]+(?:,\d{2})?")
E = H.escape


# ----------------------------------------------------------------------------- modelo
def load(slug):
    return json.load(open(os.path.join(ROOT, slug, "content.json"), encoding="utf-8"))


def clean_heading(t):
    t = re.sub(r"([a-zà-ú])([A-ZÀ-Ú])", r"\1 \2", t)
    return re.sub(r"\s+", " ", t).strip()


def faculty_from_doc(slug):
    """Professores do listing do Jet Engine (cursos de gestão): nome, papel, bio, foto."""
    doc = open(os.path.join(ROOT, slug, "v1", "index.html"), encoding="utf-8").read()
    photos = dict(re.findall(r"jet-listing-dynamic-post-(\d+)[^{]*\{[^}]*?background-image:url\(([^)]+)\)", doc))
    out, seen = [], set()
    starts = [(m.start(), m.group(1)) for m in re.finditer(r'<div[^>]*jet-listing-grid__item[^>]*jet-listing-dynamic-post-(\d+)[^>]*>', doc)]
    for n, (pos, pid) in enumerate(starts):
        chunk = doc[pos:(starts[n + 1][0] if n + 1 < len(starts) else len(doc))]
        texts = [re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", t))).strip()
                 for t in re.findall(r'data-widget_type="text-editor\.default">(.*?)</div>', chunk, flags=re.S)]
        texts = [t for t in texts if t]
        if len(texts) < 3:
            continue
        name, role, bio = texts[0], texts[1], max(texts[2:], key=len)
        if len(name) > 50 or len(role) > 30:
            continue  # item do listing que não é professor
        if name in seen:
            continue
        seen.add(name)
        photo = photos.get(pid, "")
        out.append({"name": name, "role": role, "bio": bio, "photo": ("../v1/" + photo) if photo else ""})
    return out


def items_from_blocks(blocks):
    """Transforma a lista de blocos em estrutura: lead[], items[{title, paras, list}], list, buttons, images, faq."""
    lead, items, strays, buttons, images, faq = [], [], [], [], [], []
    cur = None
    i = 0
    blocks = [b for b in blocks if not (b.get("text") and JUNK.search(b["text"]))]
    while i < len(blocks):
        b = blocks[i]
        t, txt = b["t"], b.get("text", "")
        nxt = blocks[i + 1] if i + 1 < len(blocks) else None
        if t == "a":
            buttons.append(b)
        elif t == "img":
            images.append(b)
        elif t == "h3":
            cur = {"title": txt, "paras": [], "list": []}
            items.append(cur)
        elif t == "p" and txt.endswith("?+") and nxt and nxt["t"] == "p":
            faq.append({"q": txt[:-1], "a": nxt["text"]})
            i += 1
        elif (t == "p" and nxt and nxt["t"] == "li" and len(txt) < 100
              and (txt.endswith((":", "+")) or re.match(r"^(Módulo|Nível|Itinerário|\d+º|Eixo)", txt))):
            cur = {"title": txt.rstrip("+:").strip(), "paras": [], "list": []}
            items.append(cur)
        elif t == "p" and re.match(r"^\d+º\s*Semestre", txt):
            cur = {"title": txt, "paras": [], "list": []}
            items.append(cur)
        elif t == "li":
            (cur["list"] if cur else strays).append(txt)
        elif t == "p":
            (cur["paras"] if cur else lead).append(txt)
        i += 1
    return {"lead": lead, "items": items, "list": strays, "buttons": buttons, "images": images, "faq": faq}


def normalize(slug):
    d = load(slug)
    name = NAMES[slug]
    secs = [s for s in d["sections"] if s["level"] != 0]
    h1 = next((s for s in secs if s["level"] == 1), None)
    body = [s for s in secs if s is not h1]
    model = {"slug": slug, "name": name, "title": d["title"], "badges": [], "bullets": [], "prices": [],
             "intro": [], "sections": [], "cta": "", "hero_img": ""}

    # --- hero
    model["h1"] = clean_heading(h1["heading"]) if h1 else name
    model["intro"] = [b["text"] for b in (h1["blocks"] if h1 else []) if b["t"] == "p" and not JUNK.search(b["text"])]
    # seções-curtas logo após o h1 (gestão): badges + bullets + preços + CTA
    idx = 0
    while idx < len(body):
        s = body[idx]
        if len(s["heading"]) <= 24 and "?" not in s["heading"] and slug in ("administracao", "marketing", "processos-gerenciais", "recursos-humanos"):
            if s["heading"].lower() != name.lower():
                model["badges"].append(s["heading"])
            for b in s["blocks"]:
                if b["t"] == "li":
                    model["bullets"].append(b["text"])
                elif b["t"] == "p" and PRICE.search(b["text"]):
                    model["prices"] += PRICE.findall(b["text"])
                elif b["t"] == "a" and "typechat" in b.get("href", "") and not model["cta"]:
                    model["cta"] = b["href"]
            idx += 1
        else:
            break
    body = body[idx:]

    # --- CTA / preço padrão para os demais
    allblocks = [b for s in d["sections"] for b in s["blocks"]]
    if not model["cta"]:
        link = next((b["href"] for b in allblocks if b["t"] == "a" and "typechat" in b.get("href", "")), "")
        model["cta"] = link or "https://faculdadephorte.edu.br/graduacao/%s/" % LIVE.get(slug, slug)
    if not model["prices"]:
        for b in allblocks:
            if b["t"] == "p" and PRICE.search(b["text"]):
                model["prices"] += PRICE.findall(b["text"])
                if len(model["prices"]) >= 2:
                    break
    model["prices"] = list(dict.fromkeys(model["prices"]))[:2]
    if not model["intro"] and body:
        first = body[0]["blocks"]
        model["intro"] = [b["text"] for b in first if b["t"] == "p" and len(b["text"]) > 60][:1]

    # --- seções: junta "Vamos iniciar o" + "Processo Seletivo?"; agrupa cards (empty-h2 + várias seções de 1 parágrafo)
    merged = []
    for s in body:
        if merged and merged[-1]["heading"].lower().endswith("iniciar o") and not merged[-1]["blocks"]:
            merged[-1] = {"heading": merged[-1]["heading"] + " " + s["heading"], "level": 2, "blocks": s["blocks"]}
        else:
            merged.append(dict(s))
    out, i = [], 0
    while i < len(merged):
        s = merged[i]
        card_run = []
        j = i + 1
        while j < len(merged) and len([b for b in merged[j]["blocks"] if b["t"] != "img"]) == 1 \
                and merged[j]["blocks"][-1]["t"] == "p" and merged[j]["heading"]:
            card_run.append(merged[j])
            j += 1
        if not s["blocks"] and len(card_run) >= 2 and s["heading"]:
            out.append({"kind": "cards", "title": s["heading"],
                        "items": [{"title": c["heading"], "text": next(b["text"] for b in c["blocks"] if b["t"] == "p")} for c in card_run]})
            i = j
            continue
        if s["heading"] and (s["blocks"] or s["heading"]):
            st = items_from_blocks(s["blocks"])
            if re.search(r"corpo docente|professores integrados", s["heading"], re.I) and slug in ("administracao", "marketing", "processos-gerenciais", "recursos-humanos"):
                out.append({"kind": "faculty", "title": s["heading"], "lead": [], "people": faculty_from_doc(slug)})
            elif re.search(r"Mais de 30 anos", s["heading"]):
                out.append({"kind": "band", "title": s["heading"]})
            elif st["faq"]:
                out.append({"kind": "faq", "title": s["heading"], "st": st})
            elif s["heading"] and not s["blocks"]:
                pass  # título solto sem conteúdo (ex.: "MATRICULAS ABERTAS!")
            else:
                out.append({"kind": "section", "title": s["heading"], "st": st})
        i += 1
    model["sections"] = out

    # --- imagem do hero
    pats = {"educacao-fisica": ["capa-video-edu-fisica-*.webp"], "pedagogia": ["hero-pedagogia-*.webp"],
            "traducao-e-interpretacao": ["livro-2-*.webp"]}.get(slug, ["curso-graduacao*895x1024*.webp", "arte-curso*895x1024*.webp", "*895x1024*.webp"])
    g = []
    for pat in pats:
        g = glob.glob(os.path.join(ROOT, slug, "v1", "assets", "img", pat))
        if g:
            break
    model["hero_img"] = ("../v1/assets/img/" + os.path.basename(g[0])) if g else ""
    return model


# ----------------------------------------------------------------------------- renderização comum
def slugify(t):
    t = re.sub(r"[^a-z0-9]+", "-", t.lower().encode("ascii", "ignore").decode() or "s")
    return t.strip("-") or "s"


def button(href, text, cls="btn"):
    return '<a class="%s" href="%s" target="_blank" rel="noopener">%s</a>' % (cls, E(href), E(text))


def render_items(items, cls="item"):
    """Fatos curtos viram faixa; títulos soltos viram rótulo; listas longas ocupam a largura toda."""
    facts, notes, labels, cards, wide = [], [], [], [], []
    for it in items:
        paras, lst = it["paras"], it["list"]
        if not paras and not lst:
            labels.append(it["title"])
        elif not lst and paras and len(paras[0]) <= 40:
            facts.append('<div class="fact"><span>%s</span><strong>%s</strong></div>' % (E(it["title"]), E(paras[0])))
            notes += paras[1:]
        elif len(lst) >= 6:
            wide.append('<article class="%s %s--wide"><h3>%s</h3>%s<ul class="checks checks--cols">%s</ul></article>' % (
                cls, cls, E(it["title"]), "".join("<p>%s</p>" % E(x) for x in paras), "".join("<li>%s</li>" % E(x) for x in lst)))
        else:
            body = "".join("<p>%s</p>" % E(x) for x in paras)
            if lst:
                body += '<ul class="checks">%s</ul>' % "".join("<li>%s</li>" % E(x) for x in lst)
            cards.append('<article class="%s"><h3>%s</h3>%s</article>' % (cls, E(it["title"]), body))
    out = ""
    if labels and facts:
        out += '<p class="eyebrow eyebrow--inline">%s</p>' % E(labels[0])
    if facts:
        out += '<div class="facts">%s</div>' % "".join(facts)
    out += "".join('<p class="note">%s</p>' % E(n) for n in notes)
    if cards:
        out += '<div class="items%s">%s</div>' % (" items--grid" if len(cards) >= 3 else "", "".join(cards))
    out += "".join(wide)
    return out


def render_section(sec, model, variant):
    sid = slugify(sec["title"])
    t = sec["kind"]
    if t == "cards":
        cards = "".join('<article class="card"><span class="card__n">%02d</span><h3>%s</h3><p>%s</p></article>'
                        % (i + 1, E(c["title"]), E(c["text"])) for i, c in enumerate(sec["items"]))
        return '<section class="sec sec--cards" id="%s"><div class="wrap"><h2>%s</h2><div class="cards">%s</div></div></section>' % (sid, E(sec["title"]), cards)
    if t == "faculty":
        ppl = "".join(
            '<article class="person">%s<div><h3>%s</h3><span>%s</span><p>%s</p></div></article>'
            % ('<img src="%s" alt="%s" loading="lazy">' % (E(p["photo"]), E(p["name"])) if p["photo"] else "",
               E(p["name"]), E(p["role"]), E(p["bio"][:420] + ("…" if len(p["bio"]) > 420 else ""))) for p in sec["people"])
        return '<section class="sec sec--faculty" id="%s"><div class="wrap"><h2>%s</h2><div class="people">%s</div></div></section>' % (sid, E(sec["title"]), ppl)
    if t == "band":
        return '<section class="band"><div class="wrap"><p>%s</p></div></section>' % E(sec["title"])
    if t == "faq":
        st = sec["st"]
        qa = "".join('<details><summary>%s</summary><p>%s</p></details>' % (E(x["q"]), E(x["a"])) for x in st["faq"])
        lead = "".join("<p class=\"lead\">%s</p>" % E(p) for p in st["lead"])
        btns = "".join(button(b["href"], b["text"], "btn btn--ghost") for b in st["buttons"][:1])
        return '<section class="sec sec--faq" id="%s"><div class="wrap wrap--narrow"><h2>%s</h2>%s%s%s</div></section>' % (sid, E(sec["title"]), lead, qa, btns)
    st = sec["st"]
    lead = "".join('<p class="lead">%s</p>' % E(p) for p in st["lead"])
    imgs = "".join('<img class="sec__img" src="../v1/%s" alt="%s" loading="lazy">' % (E(b["src"]), E(b.get("alt", "")))
                   for b in st["images"][:3] if not re.search(r"logo|icon|fa-", b["src"]))
    items = render_items(st["items"], "item")
    strays = '<ul class="checks checks--cols">%s</ul>' % "".join("<li>%s</li>" % E(x) for x in st["list"]) if st["list"] else ""
    btns = "".join(button(model["cta"] if b["href"].startswith("#") else b["href"], b["text"],
                          "btn" if i == 0 else "btn btn--ghost") for i, b in enumerate(st["buttons"][:2]))
    grid = items
    return ('<section class="sec" id="%s"><div class="wrap"><h2>%s</h2>%s%s%s%s%s</div></section>'
            % (sid, E(sec["title"]), lead, strays, grid, imgs, ('<div class="actions">%s</div>' % btns) if btns else ""))


def copy_html(t):
    """Destaca em negrito os valores em reais do texto ("R$ 5.085,50")."""
    return re.sub(r"(R\$\s?[\d.]+(?:,\d{2})?)", r'<strong class="phorte-salary__hl">\1</strong>', H.escape(t))


def title_html(t):
    """Sublinha o nome da profissão no título ("Quanto ganha um <u>administrador</u>?")."""
    m = re.match(r"^(Quanto ganha uma? )(.+?)(\?)$", t)
    if not m:
        return H.escape(t)
    return '%s<span class="phorte-salary__prof">%s</span>%s' % (H.escape(m.group(1)), H.escape(m.group(2)), m.group(3))


def salary_block(slug):
    c = SALARY[slug]
    items = "".join(
        '<div class="phorte-salary__item"><strong class="phorte-salary__value">%s</strong>'
        '<span class="phorte-salary__label">Média Salarial</span><span class="phorte-salary__role">%s</span></div>'
        % (E(v), E(r)) for v, r in c["salaries"])
    return ('<section class="phorte-salary" id="salarios" data-phorte-salary-section><div class="phorte-salary__inner">'
            '<article class="phorte-salary__panel"><div class="phorte-salary__copy"><h2>%s</h2><p>%s</p></div>'
            '<div class="phorte-salary__list" role="group" aria-label="Médias salariais por ocupação"><h3 class="phorte-salary__list-title">Salários médios no Brasil</h3>%s</div>'
            '<p class="phorte-salary__source">%s</p></article></div></section>'
            % (title_html(c["title"]), copy_html(c["copy"]), items, E(c["source"])))


def price_html(model):
    p = model["prices"]
    if not p:
        return ""
    if len(p) == 2:
        return '<p class="price"><s>%s</s> <strong>%s</strong><small>/mês</small></p>' % (E(p[0]), E(p[1]))
    return '<p class="price"><strong>%s</strong><small>/mês</small></p>' % E(p[0])


def footer_html():
    return ('<footer class="foot"><div class="wrap"><img src="../../_shared/logo-phorte.svg" alt="Faculdade Phorte" width="96">'
            '<p>Faculdade Phorte · Graduação | Pós-Graduação | MBA<br>Rua Rui Barbosa, 422 · Bela Vista · São Paulo – SP</p>'
            '<p class="foot__note">Protótipo local para avaliação · conteúdo copiado do site atual; valores e salários pendentes de validação.</p></div></footer>')


def page(model, variant, body):
    title = "%s — Faculdade Phorte [v%d]" % (model["name"], variant)
    return ('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n<meta name="robots" content="noindex">\n'
            '<title>%s</title>\n<link rel="stylesheet" href="../../_shared/base.css">\n'
            '<link rel="stylesheet" href="../../_shared/salario-02.css">\n<link rel="stylesheet" href="../../_shared/v%d.css">\n'
            '</head>\n<body class="v%d">\n%s\n</body>\n</html>\n' % (E(title), variant, variant, body))


def hero_badges(model):
    return "".join("<span class=\"chip\">%s</span>" % E(b) for b in model["badges"])


def bullets(model):
    return '<ul class="hero__bullets">%s</ul>' % "".join("<li>%s</li>" % E(b) for b in model["bullets"]) if model["bullets"] else ""


# ----------------------------------------------------------------------------- v2 — Editorial claro
def render_v2(m):
    intro = "".join("<p>%s</p>" % E(p) for p in m["intro"][:2])
    hero = ('<header class="hero"><div class="wrap hero__grid"><div class="hero__copy"><p class="eyebrow">Graduação · Faculdade Phorte</p>'
            '<h1>%s</h1>%s<div class="chips">%s</div>%s%s<div class="actions">%s</div></div>%s</div></header>'
            % (E(m["h1"]), intro, hero_badges(m), bullets(m), price_html(m), button(m["cta"], "Quero me inscrever"),
               ('<figure class="hero__fig"><img src="%s" alt="%s"></figure>' % (E(m["hero_img"]), E(m["name"]))) if m["hero_img"] else ""))
    secs, placed = [], False
    # salário depois da seção de "impacto/atuação/mercado" ou, na falta, ao meio
    target = next((i for i, s in enumerate(m["sections"]) if re.search(r"impacto|atuar|carreira|profiss", s["title"], re.I)), None)
    if target is None:
        target = max(0, len(m["sections"]) // 2 - 1)
    for i, s in enumerate(m["sections"]):
        secs.append(render_section(s, m, 2))
        if i == target:
            secs.append(salary_block(m["slug"]))
            placed = True
    if not placed:
        secs.append(salary_block(m["slug"]))
    cta = ('<section class="cta"><div class="wrap"><h2>Comece sua graduação em %s</h2><p>Faça o vestibular simplificado e garanta sua vaga.</p>%s</div></section>'
           % (E(m["name"]), button(m["cta"], "Fazer inscrição")))
    return page(m, 2, "<main>%s%s%s</main>%s" % (hero, "".join(secs), cta, footer_html()))


# ----------------------------------------------------------------------------- v3 — Impacto Phorte
def render_v3(m):
    intro = "".join("<p>%s</p>" % E(p) for p in m["intro"][:1])
    stat = ""
    if m["prices"]:
        stat = '<div class="hero__panel">%s%s%s</div>' % (price_html(m), bullets(m), button(m["cta"], "Quero me inscrever"))
    else:
        stat = '<div class="hero__panel">%s%s</div>' % (bullets(m), button(m["cta"], "Quero me inscrever"))
    hero = ('<header class="hero"><div class="wrap hero__grid"><div class="hero__copy"><div class="chips">%s</div><h1>%s</h1>%s</div>%s</div></header>'
            % (hero_badges(m), E(m["h1"]), intro, stat))
    secs = [render_section(s, m, 3) for s in m["sections"]]
    # v3 abre com o salário logo após o hero (argumento de mercado primeiro)
    cta = ('<section class="cta"><div class="wrap"><div><h2>Sua vaga em %s está aberta</h2><p>Vestibular simplificado, 100%% online.</p></div>%s</div></section>'
           % (E(m["name"]), button(m["cta"], "Fazer inscrição")))
    return page(m, 3, "<main>%s%s%s%s</main>%s" % (hero, salary_block(m["slug"]), "".join(secs), cta, footer_html()))


# ----------------------------------------------------------------------------- v4 — Refinada
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿️]")
DROP_V4 = re.compile(r"^(VAGAS ABERTAS|Ainda ficou com|Oferta exclusiva$|Comece sua gradua|MATRICULAS)", re.I)
NAV_KEYS = re.compile(r"por que|impacto|atuar|diferenciais|docente|professores|matriz|trajet|estrutura|oferta|kit|d[uú]vidas|escolher", re.I)


def pretty_title(t):
    t = EMOJI.sub("", t).strip()
    t = re.sub(r"[A-ZÀ-Ú]{3,}(?: [A-ZÀ-Ú]{3,})*", lambda m: m.group(0).title(), t)
    return re.sub(r"\s+", " ", t).strip()


def v4_model(m):
    """Refina o modelo comum: título/subtítulo, fatos do hero, seções limpas e sem duplicatas."""
    slug, d = m["slug"], load(m["slug"])
    h1, sub = pretty_title(m["h1"]), ""
    mm = re.search(r"\s+(Forma[çc][ãa]o .+)$", h1)
    if mm:
        h1, sub = h1[:mm.start()], mm.group(1)
    facts = []
    if m["badges"]:
        facts.append(("Turma", re.sub(r"^Turma\s*", "", m["badges"][0])))
        if len(m["badges"]) > 1:
            facts.append(("Modalidade", m["badges"][1]))
    secs, seen = [], set()
    for s in m["sections"]:
        s = dict(s, title=pretty_title(s["title"]))
        key = re.sub(r"\W+", "", s["title"].lower())
        if DROP_V4.search(s["title"]) and not (slug == "educacao-fisica" and s["title"].startswith("Oferta exclusiva!")):
            continue
        if key in seen:
            continue
        seen.add(key)
        if s.get("st"):
            bs, sb = set(), []
            for b in s["st"]["buttons"]:
                if b["text"].strip().lower() not in bs:
                    bs.add(b["text"].strip().lower())
                    sb.append(b)
            s["st"] = dict(s["st"], buttons=sb)
        secs.append(s)
    if slug == "educacao-fisica":
        facts = [("Duração", "8 semestres (4 anos)"), ("Modalidade", "Presencial 3 dias + online 2 dias"),
                 ("Certificado", "Bacharelado"), ("Período", "Noturno")]
        flat = [b for s in d["sections"] for b in s["blocks"]]
        for s in secs:  # restos de botões/rótulos do carrossel original
            st = s.get("st")
            if st:
                st["items"] = [it for it in st["items"] if it["list"] or not it["paras"] or len(it["paras"][0]) > 40]
                st["lead"] = [p for p in st["lead"] if not re.match(r"^(Quero ser avisado|APRENDA COM)", p, re.I)]
                st["buttons"] = [b for b in st["buttons"] if not re.search(r"avisado", b["text"], re.I)]
        for s in secs:
            if s["title"].startswith("Oferta exclusiva"):
                lead = s["st"]["lead"]
                s.update(kind="cards", title="Kit de boas-vindas para os 20 primeiros matriculados",
                         lead=[lead[0]] if lead else [],
                         items=[{"title": lead[i], "text": lead[i + 1]} for i in range(1, 6, 2) if i + 1 < len(lead)])
        mec = next((b["text"] for b in flat if b["t"] == "p" and b["text"].startswith("Sim, o curso de Educação Física")), "")
        if mec:
            secs.append({"kind": "faq", "title": "Dúvidas frequentes", "st": {
                "lead": [], "buttons": [], "faq": [{"q": "O curso é autorizado pelo MEC?", "a": mec}]}})
    if m["prices"]:
        facts.append(("Mensalidade", "a partir de " + m["prices"][-1]))
    return dict(m, h1=h1, sub=sub, facts=facts, sections=secs)


def short_label(t):
    t = re.sub(r"[?!.]+$", "", t)
    t = re.sub(r"^(Conheça nosso |Por que estudar |Qual o |Uma |Como funciona a )", "", t, flags=re.I)
    t = t[:1].upper() + t[1:]
    return t if len(t) <= 26 else t[:25].rsplit(" ", 1)[0] + "…"


def render_v4(m0):
    m = v4_model(m0)
    intro = "".join("<p>%s</p>" % E(p) for p in m["intro"][:2])
    chips = hero_badges(m)
    price = ""
    if m["prices"]:
        old = '<s>%s</s>' % E(m["prices"][0]) if len(m["prices"]) == 2 else ""
        price = ('<div class="hero__price"><span>Mensalidade a partir de</span><p>%s<strong>%s</strong></p></div>'
                 % (old, E(m["prices"][-1])))
    fig = ('<figure class="hero__fig"><img src="%s" alt="%s">%s</figure>' % (E(m["hero_img"]), E(m["name"]), price)) \
        if m["hero_img"] else ('<div class="hero__fig hero__fig--plain">%s</div>' % price)
    hero = ('<header class="hero"><div class="wrap hero__grid"><div class="hero__copy"><p class="eyebrow">Graduação · Faculdade Phorte</p>'
            '<h1>%s</h1>%s%s<div class="chips">%s</div>%s<div class="actions">%s%s</div></div>%s</div></header>'
            % (E(m["h1"]), ('<p class="hero__sub">%s</p>' % E(m["sub"])) if m["sub"] else "", intro, chips, bullets(m),
               button(m["cta"], "Quero me inscrever"), '<a class="btn btn--ghost" href="#salarios">Quanto ganha na área</a>', fig))
    facts = ('<div class="wrap"><dl class="strip">%s</dl></div>' % "".join(
        "<div><dt>%s</dt><dd>%s</dd></div>" % (E(k), E(v)) for k, v in m["facts"])) if m["facts"] else ""
    target = next((i for i, s in enumerate(m["sections"]) if re.search(r"impacto|atuar", s["title"], re.I)), None)
    if target is None:
        target = min(1, len(m["sections"]) - 1)
    body, nav, placed = [], [], False
    for i, s in enumerate(m["sections"]):
        if s["kind"] == "cards" and s.get("lead"):
            html = render_section(dict(s, kind="cards"), m, 4).replace(
                '<div class="cards">', "".join('<p class="lead">%s</p>' % E(p) for p in s["lead"]) + '<div class="cards">', 1)
        else:
            html = render_section(s, m, 4)
        body.append(html)
        if NAV_KEYS.search(s["title"]) and s["kind"] != "band" and len(nav) < 5:
            nav.append((slugify(s["title"]), short_label(s["title"])))
        if i == target:
            body.append(salary_block(m["slug"]))
            nav.append(("salarios", "Salários"))
            placed = True
    if not placed:
        body.append(salary_block(m["slug"]))
        nav.append(("salarios", "Salários"))
    nav_html = '<nav class="subnav" aria-label="Nesta página"><div class="wrap">%s</div></nav>' % "".join(
        '<a href="#%s">%s</a>' % (E(a), E(b)) for a, b in nav)
    cta = ('<section class="cta"><div class="wrap cta__card"><div><h2>Sua vaga em %s está aberta</h2>'
           '<p>Vestibular simplificado, 100%% online. Garanta sua vaga%s.</p></div>%s</div></section>'
           % (E(m["name"]), (" a partir de " + E(m["prices"][-1]) + "/mês") if m["prices"] else "", button(m["cta"], "Fazer inscrição")))
    sticky = ('<div class="stickybar"><div><small>%s</small><strong>%s</strong></div>%s</div>'
              % (E(m["name"]), E(("a partir de " + m["prices"][-1]) if m["prices"] else "Vagas abertas"), button(m["cta"], "Inscrever-se")))
    js = ('<script>(function(){var l=[].slice.call(document.querySelectorAll(".subnav a"));if(!("IntersectionObserver"in window))return;'
          'var o=new IntersectionObserver(function(e){e.forEach(function(x){if(x.isIntersecting){l.forEach(function(a){a.classList.toggle("is-on",a.getAttribute("href")==="#"+x.target.id)})}})},{rootMargin:"-40% 0px -55% 0px"});'
          'l.forEach(function(a){var t=document.getElementById(a.getAttribute("href").slice(1));if(t)o.observe(t)})})();</script>')
    return page(m, 4, "%s%s<main>%s%s</main>%s%s%s" % (hero, facts, nav_html, "".join(body), cta, footer_html(), sticky) + js)


def run(slug):
    m = normalize(slug)
    for v, fn in ((2, render_v2), (3, render_v3), (4, render_v4)):
        d = os.path.join(ROOT, slug, "v%d" % v)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(fn(m))
    print("%-26s hero=%s cta=%s seções=%d professores=%d" % (
        slug, bool(m["hero_img"]), "typechat" in m["cta"], len(m["sections"]),
        sum(len(s.get("people", [])) for s in m["sections"])))


if __name__ == "__main__":
    for s in (sys.argv[1:] or SLUGS):
        run(s)
