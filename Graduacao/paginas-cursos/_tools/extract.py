#!/usr/bin/env python3
"""Extrai o conteúdo de cada v1 (sem a seção de salários) em <slug>/content.json.

Formato: {"slug", "title", "sections": [{"heading", "level", "blocks": [...]}]}
bloco = {"t": "p"|"li"|"h3"|"a"|"img", "text"?, "href"?, "src"?, "alt"?}
"""
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SLUGS = ["educacao-fisica", "administracao", "marketing", "pedagogia",
         "processos-gerenciais", "recursos-humanos", "traducao-e-interpretacao"]
SKIP_CLASS = re.compile(r"phorte-salary|swiper-pagination|elementor-swiper-button")


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.sections = [{"heading": "", "level": 0, "blocks": []}]
        self.buf, self.tag, self.href = [], None, None
        self.skip_depth = 0
        self.stack = []
        self.in_body = False
        self.seen_text = set()

    # --- helpers
    def flush(self):
        text = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        self.buf = []
        tag = self.tag
        self.tag = None
        if not text or not tag:
            return
        if tag in ("h1", "h2"):
            self.sections.append({"heading": text, "level": int(tag[1]), "blocks": []})
            return
        key = (tag, text)
        blocks = self.sections[-1]["blocks"]
        if blocks and blocks[-1].get("text") == text:
            return  # duplicado consecutivo (swiper/duplicatas do Elementor)
        blocks.append({"t": tag, "text": text})

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class", "") or ""
        if tag == "footer" or (a.get("data-elementor-type") == "footer"):
            self.in_body = False
            self.stop = True
        if tag == "div" and a.get("data-elementor-type") in ("single-page", "single-post"):
            self.in_body = True
        if not self.in_body:
            return
        if self.skip_depth:
            if tag in ("div", "section", "article"):
                self.skip_depth += 1
            return
        if SKIP_CLASS.search(cls) and tag in ("div", "section", "article"):
            self.skip_depth = 1
            return
        if tag in ("h1", "h2", "h3", "h4", "p", "li", "button"):
            self.flush()
            self.tag = "li" if tag == "li" else ("h3" if tag in ("h3", "h4") else ("p" if tag in ("p", "button") else tag))
        elif tag == "a":
            self.href = a.get("href")
        elif tag == "img":
            src = a.get("src") or ""
            if src and not src.startswith("data:"):
                self.flush()
                self.sections[-1]["blocks"].append({"t": "img", "src": src, "alt": a.get("alt", "")})
        elif tag == "br":
            self.buf.append(" ")

    def handle_endtag(self, tag):
        if not self.in_body:
            return
        if self.skip_depth:
            if tag in ("div", "section", "article"):
                self.skip_depth -= 1
            return
        if tag in ("h1", "h2", "h3", "h4", "p", "li", "button"):
            self.flush()
        elif tag == "a" and self.href:
            href, self.href = self.href, None
            text = re.sub(r"\s+", " ", "".join(self.abuf)).strip()
            self.abuf = []
            if href and href != "#" and not href.startswith("javascript") and text:
                self.sections[-1]["blocks"].append({"t": "a", "href": href, "text": text})

    abuf = []

    def handle_data(self, data):
        if not self.in_body or self.skip_depth:
            return
        if self.tag:
            self.buf.append(data)
        if self.href is not None:
            self.abuf.append(data)


def run(slug):
    doc = open(os.path.join(ROOT, slug, "v1", "index.html"), encoding="utf-8").read()
    doc = re.sub(r"<!-- phorte-salary:start -->.*?<!-- phorte-salary:end -->", "", doc, flags=re.S)
    p = P()
    p.feed(doc)
    p.flush()
    secs = [s for s in p.sections if s["heading"] or s["blocks"]]
    title = re.search(r"<title>(.*?)</title>", doc, re.S).group(1).replace(" [v1 · cópia local]", "").strip()
    out = {"slug": slug, "title": html.unescape(title), "sections": secs}
    with open(os.path.join(ROOT, slug, "content.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("%-26s %2d seções, %3d blocos" % (slug, len(secs), sum(len(s["blocks"]) for s in secs)))


if __name__ == "__main__":
    for s in (sys.argv[1:] or SLUGS):
        run(s)
