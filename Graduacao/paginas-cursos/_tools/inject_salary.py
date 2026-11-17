#!/usr/bin/env python3
"""Injeta a seção de salários (direção 02) nas cópias v1. Idempotente."""
import html as H
import json
import os
import re
import shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = json.load(open(os.path.join(ROOT, "_shared", "salarios.json"), encoding="utf-8"))
START, END = "<!-- phorte-salary:start -->", "<!-- phorte-salary:end -->"


def section(slug):
    c = DATA[slug]
    items = "".join(
        '<div class="phorte-salary__item"><strong class="phorte-salary__value">%s</strong>'
        '<span class="phorte-salary__label">Média Salarial</span>'
        '<span class="phorte-salary__role">%s</span></div>' % (H.escape(v), H.escape(r))
        for v, r in c["salaries"])
    return (
        '%s<section class="phorte-salary" id="%s-salarios" data-phorte-salary-section>'
        '<div class="phorte-salary__inner"><article class="phorte-salary__panel">'
        '<div class="phorte-salary__copy"><h2>%s</h2><p>%s</p></div>'
        '<div class="phorte-salary__list" aria-label="Médias salariais por ocupação">'
        '<h3 class="phorte-salary__list-title">Salários médios no Brasil</h3>%s</div>'
        '<p class="phorte-salary__source">%s</p></article></div></section>%s'
        % (START, slug, H.escape(c["title"]), H.escape(c["copy"]), items, H.escape(c["source"]), END))


def top_level_blocks(doc, root_marker='data-elementor-type="single-page"'):
    """Devolve [(inicio, fim)] dos <div> filhos diretos do container single-page."""
    i = doc.index(root_marker)
    root_start = doc.rfind("<div", 0, i)
    tag = re.compile(r"<(/?)div\b[^>]*?(/?)>", re.I)
    depth, blocks, cur = 0, [], None
    for m in tag.finditer(doc, root_start):
        if m.group(2):
            continue
        if m.group(1):
            depth -= 1
            if depth == 1 and cur is not None:
                blocks.append((cur, m.end()))
                cur = None
            if depth == 0:
                break
        else:
            depth += 1
            if depth == 2:
                cur = m.start()
    return blocks


# regra por curso: (modo, regex do título-âncora). "before"/"after" o bloco de seção que contém o título.
RULES = {
    "educacao-fisica": ("after", r"Saúde e Bem-Estar"),
    "administracao": ("before", r"Diferenciais\s+PHORTE"),
    "marketing": ("before", r"Diferenciais\s+PHORTE"),
    "processos-gerenciais": ("before", r"Diferenciais\s+PHORTE"),
    "recursos-humanos": ("before", r"Diferenciais\s+PHORTE"),
    "pedagogia": ("after", r"Onde o pedagogo pode atuar"),
    "traducao-e-interpretacao": ("before", r"Corpo docente"),
}
TAG = re.compile(r"<(/?)(div|section)\b[^>]*?(/?)>", re.I)


def section_block(doc, anchor_re, min_siblings=4):
    """Bloco (inicio, fim) mais alto, cujos irmãos sejam >= min_siblings, que contém o título."""
    m = re.search(anchor_re, doc)
    if not m:
        return None
    # pilha de elementos abertos até a posição do título
    stack = []  # [start, tag, n_children]
    for t in TAG.finditer(doc, 0, m.start()):
        if t.group(3):
            continue
        if t.group(1):
            if stack:
                stack.pop()
        else:
            if stack:
                stack[-1][2] += 1
            stack.append([t.start(), t.group(2).lower(), 0])
    # candidato: ancestral mais externo cujo pai tem muitos filhos
    def total_children(start):
        depth, n = 0, 0
        for t in TAG.finditer(doc, start):
            if t.group(3):
                continue
            if t.group(1):
                depth -= 1
                if depth == 0:
                    return n
            else:
                depth += 1
                if depth == 2:
                    n += 1
        return n

    cand = None
    for i, (st, tg, _n) in enumerate(stack):
        if i > 0 and total_children(stack[i - 1][0]) >= min_siblings:
            cand = i
            break
    if cand is None:
        return None
    start, tg = stack[cand][0], stack[cand][1]
    depth = 0
    for t in TAG.finditer(doc, start):
        if t.group(3):
            continue
        depth += -1 if t.group(1) else 1
        if depth == 0:
            return start, t.end()
    return None


def inject(slug):
    path = os.path.join(ROOT, slug, "v1", "index.html")
    doc = open(path, encoding="utf-8").read()
    doc = re.sub(re.escape(START) + ".*?" + re.escape(END), "", doc, flags=re.S)
    mode, anchor = RULES[slug]
    blk = section_block(doc, r">[^<]*" + anchor)
    if not blk:
        raise SystemExit("âncora não encontrada em %s: %s" % (slug, anchor))
    pos = blk[0] if mode == "before" else blk[1]
    doc = doc[:pos] + section(slug) + doc[pos:]
    if "salario-02.css" not in doc:
        doc = doc.replace('<link rel="stylesheet" href="assets/local.css">',
                          '<link rel="stylesheet" href="assets/local.css">\n<link rel="stylesheet" href="assets/salario-02.css">')
    open(path, "w", encoding="utf-8").write(doc)
    shutil.copy(os.path.join(ROOT, "_shared", "salario-02.css"), os.path.join(ROOT, slug, "v1", "assets", "salario-02.css"))
    print("%-28s %s '%s' (bloco %d chars)" % (slug, mode, anchor, blk[1] - blk[0]))


if __name__ == "__main__":
    for s in DATA:
        inject(s)
