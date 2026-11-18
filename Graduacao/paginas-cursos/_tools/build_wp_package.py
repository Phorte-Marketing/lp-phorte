# Gera os arquivos para o template do Elementor (um por curso): CSS, bloco de salário.
# Uso: python -I _tools/build_wp_package.py marketing 60913
import os, re, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
slug, tpl = sys.argv[1], sys.argv[2]
css = open(os.path.join(ROOT, slug, "v1", "assets", "local.css"), encoding="utf-8").read()
css = css.replace(".elementor-38681", ".elementor-" + tpl)
css = re.sub(r"@font-face\{[^}]*\}\n?", "", css)            # Poppins já vem do tema
css = re.sub(r'(background-image:url\()"img/([^"]+)"', r'\1"IMG_\2"', css)  # troca pelo upload do WordPress depois
sal = open(os.path.join(ROOT, "_shared", "salario-02.css"), encoding="utf-8").read()
html = open(os.path.join(ROOT, slug, "v1", "index.html"), encoding="utf-8").read()
a = html.index("<!-- phorte-salary:start -->"); b = html.index("<!-- phorte-salary:end -->") + len("<!-- phorte-salary:end -->")
out = os.path.join(ROOT, "_wp", slug); os.makedirs(out, exist_ok=True)
open(os.path.join(out, "custom.css"), "w", encoding="utf-8").write(css + "\n" + sal)
open(os.path.join(out, "salario.html"), "w", encoding="utf-8").write(html[a:b])
print(slug, tpl, len(css) + len(sal), "bytes de CSS;", b - a, "bytes de salário")
