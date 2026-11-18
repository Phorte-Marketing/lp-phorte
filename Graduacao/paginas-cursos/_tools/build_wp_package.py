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
# "Conheça o curso" em grade (até 1280px): o Swiper duplica os slides para o loop; os clones ficam escondidos
css += "\n@media (max-width:1280px){.elementor-element-28e351a6 .swiper-slide-duplicate{display:none!important}}\n"
# cartões de disciplinas e professores com a mesma altura dentro do carrossel
css += ("\n.jet-listing-grid__slider .swiper-wrapper{align-items:stretch}\n"
        ".jet-listing-grid__slider .swiper-slide.jet-listing-grid__item{height:auto;display:flex}\n"
        ".jet-listing-grid__slider .swiper-slide.jet-listing-grid__item>.elementor{display:flex;flex:1;min-width:0}\n"
        ".jet-listing-grid__slider .swiper-slide.jet-listing-grid__item>.elementor>.elementor-element-743a018{flex:1}\n")
# causa do corte na borda de baixo: o equal-columns do Jet põe height:100% no cartão, e o cartão de disciplinas tem margin-top:37px;
# 100% + 37px estoura o slide e o overflow:hidden do Swiper corta o fim da caixa. Com height:auto o cartão estica (stretch) já descontando a margem.
css += ("\n.jet-listing-grid__slider .jet-listing-grid__item.jet-equal-columns>.elementor>:is(.elementor-element-743a018,.elementor-element-d61b7e4):not(#ph){height:auto!important;align-self:stretch}\n"
        ".jet-listing-grid__slider .swiper-slide.jet-listing-grid__item{box-sizing:border-box}\n")
# sem salto no carregamento: o carrossel só aparece depois de o JS montar (fim do loop, 3/2/1 por vista, barra); se o JS falhar, aparece em 4s.
# o espaço da barra (setas e pontos) já fica reservado, para o conteúdo de baixo não pular quando a barra entra.
css += ("\n.jet-listing-grid__slider:not([data-ph-car]){opacity:0;animation:ph-car-reveal 0s linear 4s forwards}\n"
        "@keyframes ph-car-reveal{to{opacity:1}}\n"
        ".jet-listing-grid__slider:not([data-ph-car]):has(.elementor-element-743a018){margin-bottom:calc(20px + var(--ph-alvo-toque,2.75rem))}\n"
        ".jet-listing-grid__slider:not([data-ph-car]):has(.elementor-element-d61b7e4){margin-bottom:calc(1.25rem + 1.5rem + 3rem)}\n"   # + o botão "Ver mais" (3rem) que o JS põe nos cartões
        "@media (prefers-reduced-motion:no-preference){.jet-listing-grid__slider[data-ph-car]{animation:ph-car-in .25s ease-out}@keyframes ph-car-in{from{opacity:0}}}\n"
        # foco do teclado: o foco fica no próprio carrossel (tabindex=0)
        ".jet-listing-grid__slider[data-ph-car]:focus-visible{outline:var(--ph-largura-foco,3px) solid var(--ph-ring,#1A1A1A);outline-offset:var(--ph-afastamento-foco,2px)}\n"
        ".jet-listing-grid__slider .swiper-wrapper{touch-action:pan-y pinch-zoom}\n"
        # o Swiper põe cada slide em camada própria (translateZ+backface-hidden): em posição fracionada a borda de 1px sai borrada/mais escura
        ".jet-listing-grid__slider.swiper-backface-hidden .swiper-slide{transform:none;backface-visibility:visible}\n")
# número do cartão vindo do JS (posição real da disciplina), em vez do contador por posição no HTML
css += "\n.elementor-element-743a018[data-ph-n]::after{content:attr(data-ph-n)}\n"
# troca dos carrosséis do Jet: desaceleração suave (a duração vem do JS; movimento reduzido zera)
css += "\n.jet-listing-grid__slider .swiper-wrapper{transition-timing-function:cubic-bezier(.25,.8,.25,1)!important}\n@media (prefers-reduced-motion:reduce){.jet-listing-grid__slider .swiper-wrapper{transition-duration:0ms!important}}\n"
# barra inferior "Faça sua inscrição" (popup 34612 "Rodapé Inscreva-se"): padrão antigo, não entra no layout novo
css += "\n/* popup 34612 (barra inferior) fora do layout novo */\n#elementor-popup-modal-34612,.elementor-popup-modal:has(.elementor-element-5748245){display:none!important}\n"

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
