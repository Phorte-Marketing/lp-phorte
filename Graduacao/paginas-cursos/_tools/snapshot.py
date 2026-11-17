#!/usr/bin/env python3
"""Baixa as páginas de curso do site ao vivo e gera uma cópia HTML local (v1).

- remove header/navbar, popups, scripts e rastreadores;
- baixa CSS, imagens e fontes para ./<slug>/v1/assets;
- deixa um HTML estático que abre direto no navegador (file:// ou GitHub Pages).

Uso: python -I snapshot.py            (todas as páginas)
     python -I snapshot.py marketing  (uma página)
"""
import hashlib
import os
import re
import sys
import urllib.parse
import urllib.request

BASE = "https://faculdadephorte.edu.br"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UA = {"User-Agent": "Mozilla/5.0 (Phorte LP snapshot)"}

# slug local -> slug no site
COURSES = {
    "educacao-fisica": "educacao-fisica",
    "administracao": "administracao",
    "marketing": "marketing",
    "pedagogia": "pedagogia",
    "processos-gerenciais": "processos-gerenciais",
    "recursos-humanos": "recursos-humanos",
    "traducao-e-interpretacao": "traducao-e-interpretacao-ingles-portugues",
}

_cache = {}


def fetch(url):
    if url in _cache:
        return _cache[url]
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            data = r.read()
    except Exception as exc:  # noqa: BLE001
        print("  ! falhou", url, exc)
        data = None
    _cache[url] = data
    return data


def remove_balanced(html, open_re, tag):
    """Remove elementos <tag ...> que casam com open_re, respeitando aninhamento."""
    pat = re.compile(open_re)
    out, pos = [], 0
    while True:
        m = pat.search(html, pos)
        if not m:
            out.append(html[pos:])
            break
        out.append(html[pos:m.start()])
        depth, i = 0, m.start()
        tag_re = re.compile(r"<(/?)%s\b[^>]*?(/?)>" % tag, re.I)
        end = len(html)
        for t in tag_re.finditer(html, m.start()):
            if t.group(2):
                continue
            depth += -1 if t.group(1) else 1
            if depth == 0:
                end = t.end()
                break
        pos = end
    return "".join(out)


class Assets:
    def __init__(self, folder):
        self.folder = folder
        self.map = {}

    def save(self, url, kind):
        url = url.split("#")[0]
        if url in self.map:
            return self.map[url]
        data = fetch(url)
        if data is None:
            self.map[url] = None
            return None
        path = urllib.parse.urlparse(url).path
        name = os.path.basename(path) or "file"
        stem, ext = os.path.splitext(name)
        stem = re.sub(r"[^A-Za-z0-9._-]+", "-", stem)[:60]
        tag = hashlib.md5(url.encode()).hexdigest()[:6]
        rel = "assets/%s/%s-%s%s" % (kind, stem, tag, ext.lower() or "")
        full = os.path.join(self.folder, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "wb") as f:
            f.write(data)
        self.map[url] = rel
        return rel


def absolutize(u, base):
    u = u.strip().strip("'\"")
    if not u or u.startswith(("data:", "#", "javascript:", "mailto:", "tel:")):
        return None
    return urllib.parse.urljoin(base, u)


def rewrite_css(css, base, assets, rel_prefix):
    """Reescreve url(...) do CSS para arquivos locais."""

    def repl(m):
        raw = m.group(1)
        absu = absolutize(raw, base)
        if not absu:
            return m.group(0)
        ext = os.path.splitext(urllib.parse.urlparse(absu).path)[1].lower()
        kind = "fonts" if ext in (".woff", ".woff2", ".ttf", ".otf", ".eot") else "img"
        rel = assets.save(absu, kind)
        return "url(%s%s)" % (rel_prefix, rel) if rel else "url(%s)" % absu

    css = re.sub(r"url\(\s*([^)]+?)\s*\)", repl, css)
    css = re.sub(r"@charset[^;]*;", "", css)
    return css


def build(slug, site_slug):
    url = "%s/graduacao/%s/" % (BASE, site_slug)
    print("==", slug, url)
    html = fetch(url).decode("utf-8", "replace")
    out_dir = os.path.join(ROOT, slug, "v1")
    os.makedirs(out_dir, exist_ok=True)
    assets = Assets(out_dir)

    # 1) limpeza estrutural
    html = re.sub(r"<script\b.*?</script>", "", html, flags=re.S | re.I)
    html = re.sub(r"<noscript\b.*?</noscript>", "", html, flags=re.S | re.I)
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    html = remove_balanced(html, r"<header\b[^>]*elementor-location-header", "header")
    html = remove_balanced(html, r"<div\b[^>]*data-elementor-type=\"popup\"", "div")
    html = remove_balanced(html, r"<div\b[^>]*class=\"[^\"]*jet-popup[ \"]", "div")
    html = remove_balanced(html, r"<nav\b[^>]*jet-mobile-menu", "nav")
    html = remove_balanced(html, r"<iframe\b", "iframe")
    html = re.sub(r"<link\b[^>]*rel=['\"](?:preload|prefetch|dns-prefetch|preconnect|alternate|canonical|shortlink|https://api\.w\.org/|EditURI|manifest|icon|apple-touch-icon)['\"][^>]*>", "", html, flags=re.I)
    html = re.sub(r"<link\b[^>]*rel=['\"]stylesheet['\"][^>]*as=['\"]script['\"][^>]*>", "", html, flags=re.I)

    # 2) CSS: junta todos os <link stylesheet> em assets/site.css
    css_parts = []

    def css_link(m):
        tag = m.group(0)
        href = re.search(r"href=['\"]([^'\"]+)['\"]", tag)
        if not href:
            return ""
        absu = absolutize(href.group(1), url)
        if not absu:
            return ""
        data = fetch(absu)
        if data is None:
            return ""
        css = data.decode("utf-8", "replace")
        media = re.search(r"media=['\"]([^'\"]+)['\"]", tag)
        css = rewrite_css(css, absu, assets, "")
        if media and media.group(1) not in ("all", "screen"):
            css = "@media %s{%s}" % (media.group(1), css)
        css_parts.append("/* %s */\n%s" % (absu, css))
        return ""

    html = re.sub(r"<link\b[^>]*stylesheet[^>]*>", css_link, html, flags=re.I)

    # <style> inline: reescreve url() e mantém no head
    def style_block(m):
        return "<style>%s</style>" % rewrite_css(m.group(1), url, assets, "")

    html = re.sub(r"<style\b[^>]*>(.*?)</style>", style_block, html, flags=re.S | re.I)

    # url() de css/inline que apontam para ../ precisam estar em assets/ (css fica em assets/)
    css_all = "\n".join(css_parts)
    css_all = css_all.replace("url(assets/", "url(")  # site.css fica dentro de assets/
    os.makedirs(os.path.join(out_dir, "assets"), exist_ok=True)

    # 3) imagens em atributos
    def attr_repl(m):
        attr, quote, val = m.group(1), m.group(2), m.group(3)
        if attr in ("srcset", "data-srcset", "data-lazy-srcset"):
            parts = []
            for item in val.split(","):
                item = item.strip()
                if not item:
                    continue
                bits = item.split()
                absu = absolutize(bits[0], url)
                rel = assets.save(absu, "img") if absu else None
                if rel:
                    parts.append(" ".join([rel] + bits[1:]))
            return 'srcset=%s%s%s' % (quote, ", ".join(parts), quote) if parts else ""
        absu = absolutize(val, url)
        if not absu:
            return m.group(0)
        ext = os.path.splitext(urllib.parse.urlparse(absu).path)[1].lower()
        if ext not in (".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg", ".avif", ".ico"):
            return m.group(0)
        rel = assets.save(absu, "img")
        if not rel:
            return m.group(0)
        new_attr = "src" if attr.startswith("data-") else attr
        return "%s=%s%s%s" % (new_attr, quote, rel, quote)

    html = re.sub(
        r"\b(src|srcset|data-src|data-lazy-src|data-srcset|data-lazy-srcset|poster)=(['\"])(.*?)\2",
        attr_repl, html, flags=re.S)
    # background-image inline (ignora o que ja virou caminho local)
    def bg_repl(m):
        val = m.group(2)
        if val.startswith("assets/") or not re.search(r"\.(jpe?g|png|webp|gif|svg|avif)", val, re.I):
            return m.group(0)
        absu = absolutize(val, url)
        rel = assets.save(absu, "img") if absu else None
        return "url(%s)" % rel if rel else m.group(0)

    html = re.sub(r"url\(\s*(&quot;|['\"])?([^)'\"&]+?)(?:&quot;|['\"])?\s*\)", bg_repl, html)

    # 4) lazy-load / animações que dependem de JS
    html = re.sub(r"\sloading=(['\"])lazy\1", "", html)
    html = re.sub(r"\bdata-lazy-[a-z-]+=(['\"]).*?\1", "", html)
    html = html.replace("elementor-invisible", "")
    html = re.sub(r"\blazyload\b|\blazyloaded\b|\bno-lazyload\b", "", html)

    # 5) head final
    title = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    desc = re.search(r"<meta name=\"description\"[^>]*>", html)
    head = ['<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            "<title>%s [v1 · cópia local]</title>" % (title.group(1).strip() if title else slug)]
    if desc:
        head.append(desc.group(0))
    head.append('<meta name="robots" content="noindex">')
    head.append('<link rel="stylesheet" href="assets/site.css">')
    head.append('<link rel="stylesheet" href="assets/local.css">')

    body = re.search(r"<body\b[^>]*>(.*)</body>", html, flags=re.S)
    body_open = re.search(r"<body\b[^>]*>", html).group(0)
    inner = body.group(1) if body else html
    doc = '<!doctype html>\n<html lang="pt-BR">\n<head>\n%s\n</head>\n%s\n%s\n<script src="assets/local.js" defer></script>\n</body>\n</html>\n' % (
        "\n".join(head), body_open, inner)

    with open(os.path.join(out_dir, "assets", "site.css"), "w", encoding="utf-8") as f:
        f.write(css_all)
    shared = os.path.join(ROOT, "_shared")
    for src, dst in (("v1-local.css", "local.css"), ("v1-local.js", "local.js")):
        with open(os.path.join(shared, src), encoding="utf-8") as f_in, open(os.path.join(out_dir, "assets", dst), "w", encoding="utf-8") as f_out:
            f_out.write(f_in.read())
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(doc)
    print("   html %d KB, css %d KB, %d arquivos" % (len(doc) // 1024, len(css_all) // 1024, len([v for v in assets.map.values() if v])))


if __name__ == "__main__":
    wanted = sys.argv[1:] or list(COURSES)
    for s in wanted:
        build(s, COURSES[s])
