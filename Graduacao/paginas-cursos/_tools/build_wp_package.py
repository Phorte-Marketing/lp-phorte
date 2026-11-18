# Gera os arquivos para o template do Elementor (um por curso): CSS, JS e bloco de salário.
# Uso: python -I _tools/build_wp_package.py marketing 60913 [pages]
#   pages = usa as imagens publicadas no GitHub Pages (revisão); sem isso deixa IMG_<arquivo> para trocar pelo upload do WordPress.
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PAGES = "https://srbunnie.github.io/lp-phorte/Graduacao/paginas-cursos/%s/v1/assets/img/"
slug, tpl = sys.argv[1], sys.argv[2]
pages = len(sys.argv) > 3 and sys.argv[3] == "pages"

css = open(os.path.join(ROOT, slug, "v1", "assets", "local.css"), encoding="utf-8").read()
css = css.replace(".elementor-38681", ".elementor-" + tpl)
css = re.sub(r"@font-face\{[^}]*\}\n?", "", css)  # Poppins já vem do tema
# fora: regras que só simulavam o Elementor/Jet na cópia local (o site de verdade já roda o Swiper)
drop = [r"^\.swiper[^\n]*$", r"^\.elementor-swiper-button\{cursor[^\n]*$",
        r"^\.jet-listing-grid__slider \.jet-listing-grid__items\{overflow-x[^\n]*$",
        r"^\.jet-listing-grid__slider \.jet-listing-grid__items::-webkit[^\n]*$",
        r"^\.jet-listing-grid__slider \.jet-listing-grid__item\{scroll-snap[^\n]*$",
        r"^\s*\.jet-listing-grid__slider \.jet-listing-grid__items>\.jet-listing-grid__item\{flex:0 0[^\n]*$"]
for d in drop:
    css = re.sub(d + "\n?", "", css, flags=re.M)
repl = (PAGES % slug) if pages else "IMG_"
css = re.sub(r'(background-image:url\()"img/([^"]+)"', lambda m: '%s"%s%s"' % (m.group(1), repl, m.group(2)), css)
css += "\n" + open(os.path.join(ROOT, "_shared", "salario-02.css"), encoding="utf-8").read()

html = open(os.path.join(ROOT, slug, "v1", "index.html"), encoding="utf-8").read()
a = html.index("<!-- phorte-salary:start -->") + len("<!-- phorte-salary:start -->")
b = html.index("<!-- phorte-salary:end -->")

icons = json.load(open(os.path.join(ROOT, "_shared", "lucide-icons.json"), encoding="utf-8"))
need = ["graduation-cap", "calendar-clock", "moon", "map-pin", "monitor-play", "building-2", "leaf", "piggy-bank", "megaphone", "users",
        "briefcase-business", "trending-up", "lightbulb", "rocket", "sprout", "banknote", "handshake"]
js = open(os.path.join(ROOT, "_wp", "wp.src.js"), encoding="utf-8").read().replace("__ICONS__", json.dumps({k: icons[k] for k in need}, ensure_ascii=False))

out = os.path.join(ROOT, "_wp", slug)
os.makedirs(out, exist_ok=True)
open(os.path.join(out, "custom.css"), "w", encoding="utf-8").write(css)
open(os.path.join(out, "salario.html"), "w", encoding="utf-8").write(html[a:b])
open(os.path.join(ROOT, "_wp", "wp.js"), "w", encoding="utf-8").write(js)
print(slug, tpl, len(css), "bytes de CSS;", len(js), "bytes de JS;", b - a, "bytes de salário")
