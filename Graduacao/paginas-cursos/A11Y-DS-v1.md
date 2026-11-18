# v1 · Design System Phorte e acessibilidade (Administração)

Escopo: melhorias pontuais na v1, **sem mudar a estrutura** da página (a v1 será publicada no WordPress/Elementor). Tudo é CSS e atributos de acessibilidade; nenhum bloco foi movido, criado ou removido.

Fonte dos tokens: <https://phorte-design-system.vercel.app> (cores, tipografia, espaçamento, efeitos e a página de Acessibilidade). Critérios de auditoria: skill `accessibility` (WCAG 2.2) de `Agents e Skills Globais/skills-landing-page-review`, aplicados com axe-core 4.10.2 e medições de contraste próprias.

## Regras do Design System que guiaram a revisão

| Regra do DS | Valor |
|---|---|
| Fonte | Poppins, só 5 pesos: 400, 500, 600, 700, 900 (300 vale 400; 800 vale 900); 700 e 900 com tracking -0,01em e entrelinha 1,35 |
| Contraste | texto >= 4,5:1; limite de controle >= 3:1 |
| Alvo de toque | 44 × 44px (`--spacing-alvo-toque`); mínimo WCAG 2.5.8 é 24px |
| Foco | contorno de 2px, recuo de 2px, cor `#7D1B1B` (`#FAFAFA` sobre fundo escuro); contorno, não só sombra, para o modo de alto contraste |
| Fonte mínima | 12px |
| Movimento | respeitar `prefers-reduced-motion` |
| Primário | `#D42B2B` (5,0:1 com branco); `#A81E1E` (7,3:1); `#E64242` é cor de marca, não serve de fundo de texto (4,0:1) |

Os tokens usados estão em `_shared/phorte-tokens.css`, com prefixo `--ph-` para não colidir com o tema.

## Antes e depois (axe, Administração v1, desktop)

| Verificação | Antes | Depois |
|---|---|---|
| Contraste de cor (reprovado) | 20 trechos | 0 |
| Alvo de toque menor que 24px | 12 links | 0 |
| Link sem nome acessível | 2 | 0 |
| Skip link sem destino | 1 | 0 |
| Landmark duplicado (2 carrosséis "Carrossel") | 1 | 0 |
| Uso de `aria-label` sem papel | 1 | 0 |
| Falta de `main` / conteúdo fora de landmarks | 1 + 60 | 1 + 60 (ver "Fora do alcance da v1") |

## O que mudou

**CSS** (`_shared/v1-ds.css`, copiado para `<curso>/v1/assets/local.css` por `_tools/apply_v1_ds.py`)

1. Cores globais do Kit: o vermelho `#E64242` passa a `#D42B2B` e o texto padrão `#7A7A7A` (4,3:1) passa a `#595959` (7,0:1). Isso corrige de uma vez o cartão de preço, os ícones e os parágrafos da seção "Como funciona".
2. Degradês vinho (`#571314` a `#F83C42`): o fim claro vira `#D42B2B`. Branco sobre `#F83C42` dava 3,7:1.
3. Cartão de inscrição: chip da turma sem texto branco sobre laranja (1,4:1) e botão "Fazer Inscrição" branco com texto `#A81E1E`; mesma estrutura e tamanho.
4. Cartões de professores: o véu escuro sobre a foto agora já está em 88% quando o texto começa.
5. Legenda do e-MEC sobre fundo escuro: `#C7C7C7` (8,2:1).
6. Foco visível em todos os controles, com anel inverso sobre fundo vermelho ou escuro.
7. Poppins: as caixas de fato do curso (Bacharelado, 8 Semestres...) estavam em Roboto; pesos 300 e 800 mapeados para 400 e 900.
8. Alvos de 44px nas listas de links e no rodapé; texto do rodapé com no mínimo 12px (estava entre 8 e 11px).
9. Entrelinha de 1,625 nos textos corridos e `prefers-reduced-motion`.

**Atributos** (`apply_v1_ds.py`, idempotente)

- Chips "Turma 2027.1" e "EAD • Presencial": `role="presentation"` (eram títulos H2).
- 9 títulos de cartão (impacto e diferenciais): `aria-level="3"` (estavam como H2 dentro de seções H2).
- Links só com imagem: `aria-label` no selo do vestibular e no selo do e-MEC.
- Carrosséis com rótulos distintos ("Dados do curso", "Diferenciais Phorte").
- Destino do skip link: `id="content"` na raiz da página.
- Bloco de salário: `role="group"` na lista de valores.

## Como levar para o Elementor

| Item | Onde no Elementor |
|---|---|
| Cores globais | Configurações do site > Cores globais: trocar "E64242" por `#D42B2B` e a cor de Texto por `#595959` |
| Degradês vinho | em cada container: segunda cor do degradê = `#D42B2B` |
| Chip da turma e botão | widget > Estilo: chip com fundo `#FBEAEA` e texto `#A81E1E`; botão com fundo branco e texto `#A81E1E`, altura mínima 44px |
| Fonte | Configurações do site > Tipografia global: Poppins, pesos 400, 500, 600, 700 e 900 |
| Foco, alvos, 12px, véu dos professores | CSS personalizado da página (cole o conteúdo do bloco `DS-PHORTE` de `v1-local.css`) |
| Títulos | nos widgets de título dos cartões, usar a tag H3; nos chips, trocar o widget por "Texto" |
| Imagens-link | campo "Link" > texto alternativo / rótulo; imagens decorativas com alt vazio |

## Fora do alcance da v1 (precisa do tema ou do template)

- Falta um `<main>` e os landmarks: na v1 local o cabeçalho foi removido, e no site o tema Hello Elementor fornece `header`, `main` e `footer`.
- IDs duplicados do acordeão (`e-n-accordion-item-*`) vêm da listagem de professores do Jet Engine, repetida por card.
- O rodapé é o template global 31347: os ajustes de 12px e alvo de toque valem para o site todo e devem ser feitos nesse template.
- O contraste de texto sobre as fotos dos professores e sobre o banner do vestibular foi medido por amostragem de pixels (mínimo de 4,0:1 no título de 45px e 5,7:1 no subtítulo), não pelo axe.
- Falta uma passada com leitor de tela (NVDA/VoiceOver), como o próprio DS exige antes de dar uma peça por pronta.

## Comandos

```bash
python -I _tools/apply_v1_ds.py administracao   # CSS + atributos (idempotente)
python -I _tools/apply_v1_ds.py                  # mesmo comando; padrão é a Administração
```

---

## Segunda rodada: menos ruído, tipografia e ícones

Arquivos: `_shared/v1-ds-ui.css` (regras), `_shared/lucide-icons.json` (ícones), `_tools/apply_v1_ds.py` (aplica CSS, converte degradês do `site.css` e troca os ícones).

**Degradês viram cor chapada.** Nenhum degradê sobrou na página (fora a faixa de imagem do banner). Mapa de cores: painéis do hero, "Por que estudar" e título gradiente em `#7D1B1B`; cartões de impacto em `#A81E1E`; faixa de diferenciais em `#F4F6F9`; botões de vestibular em `#D42B2B` com texto branco (5,0:1). O véu degradê das fotos de professores virou uma base escura chapada (foto em cima, texto embaixo). O bloco de salário também ficou chapado.

**Sombras do DS.** `0 0 10px` a 50% de preto foi trocado por três níveis: repouso (cartões), hover (imagens e botões) e flutuante (cartão de inscrição). O hero deixou de projetar sombra sobre a próxima seção e ganhou uma linha de 1px.

**Escala tipográfica (DS).** Títulos de seção em um único tamanho (30px no celular a 36px no desktop, peso 700); título principal 36 a 48px; títulos de cartão 20px; corpo 16px com entrelinha 1,625; apoio 14px; rótulos 12px. Antes havia 13, 14, 15, 17, 18, 19 e 24px em texto corrido, e títulos de 36 a 62px.

**"Conheça o curso".** Caixas de fato claras com rótulo pequeno em caixa alta e valor em 18px. O texto da modalidade virou uma coluna de leitura de 46rem: subtítulo vermelho, lista de pontos com ícone de check, trechos de apoio com filete cinza e os avisos (Presencial e "Veja só") em destaque rosa. O ponto solto "." do editor deixou de aparecer.

**Ícones Lucide** (instalado em `Daily/node_modules/lucide` v1.8, trocados dentro dos widgets de ícone que já existiam):

| Cartão | Ícone |
|---|---|
| Organização Empresarial | `building-2` |
| Sustentabilidade Empresarial | `leaf` |
| Finanças | `piggy-bank` |
| Marketing e Cadeia de Suprimentos | `megaphone` |
| Gestão de Pessoas e Processos | `users` |
| Gestão de Negócio | `briefcase-business` |
| Gestão de Mercado | `trending-up` |
| Gestão Contemporânea | `lightbulb` |

As caixas de fato também usam Lucide (`graduation-cap`, `calendar-clock`, `moon`, `map-pin`, `monitor-play`). No Elementor: Widget de ícone > Biblioteca > Enviar SVG, com os arquivos do Lucide (traço `currentColor`, 1,75px).

**HeroUI v3** não foi usado: são componentes React e esta página é Elementor. As cores, raios e sombras seguem os tokens do DS, que é a fonte comum.

Também foi corrigida a rolagem lateral no celular, causada pelo selo do MEC no hero (`overflow-x:clip` no wrapper da página).

### Cartões de disciplinas e carrossel (terceira rodada)

- **Carrossel de volta:** na cópia local os dois carrosséis do Jet Engine (disciplinas, 8 cartões; professores, 7) mostravam só 3 itens e escondiam o resto, porque o JS do WordPress foi removido. Agora rolam com encaixe, setas de 44px, pontos com área de toque de 24px, teclado (setas, Home e End) e rótulos (`Disciplinas do curso`, `Corpo docente`). Sem rotação automática: o original girava a cada 5s e pausar só no hover não cumpre a WCAG 2.2.2. No WordPress o Jet entrega as setas nativamente; configure "Setas: ligado" e use os mesmos tokens.
- **Cartão:** alinhado à esquerda, azulejo de ícone Lucide de 48px, número 01 a 08 no canto, título em 20px, lista com marcadores do DS e o item repetido "Gestão em Ação" como selo rosa no rodapé (todos os selos ficam na mesma linha porque os cartões têm a mesma altura).
- **Controles:** `_shared/v1-local.js` (JS) e bloco 7 de `_shared/v1-ds-ui.css`.

### Quarta rodada: banner, impacto, botão, professores, "30 anos" e processo seletivo

- **Rodapé removido** da v1 (o WordPress já tem o seu). Feito em `apply_v1_ds.py`; os outros cursos ainda têm o rodapé.
- **Banner "Matrículas abertas":** o bloco inteiro é clicável. `local.js` repassa o clique do bloco ao link do selo, que continua sendo o destino do teclado e dos leitores de tela (nome acessível definido). No Elementor: Contêiner > Link.
- **Impacto na carreira:** cartões à esquerda com ícones Lucide (`banknote`, `briefcase-business`, `trending-up`, `handshake`) no lugar das imagens PNG, texto alinhado à esquerda; a notícia do O Globo ocupa a coluna da direita em largura total, com borda e sombra, e ganhou texto alternativo (antes `alt=""`).
- **Botão do vestibular:** virou uma faixa de chamada rosa clara com botão grande (56px, 20px de fonte) e seta.
- **Professores:** padrão da v6: cartão branco, foto em cima, nome, cargo, minibio de 14px, botão "Ver mais" (real, com `aria-expanded`), título "Professores" e setas no canto superior direito, pontos embaixo.
- **"Mais de 30 anos":** faixa cinza clara, título vermelho em peso 900, texto cinza, números 85% e 90% em vermelho e rótulo em destaque, imagem com cantos arredondados e sombra flutuante.
- **"Vamos iniciar o Processo Seletivo?":** cartão vinho centralizado com título branco, texto e os dois botões lado a lado (primário branco com seta, secundário vazado); no celular os botões empilham.

### Rodada final: refinamentos e responsivo (tablet até 1024px, celular até 767px)

- **Dados do curso:** até 1280px os 5 dados ficam todos visíveis em grade (não há mais carrossel escondendo itens); acima disso continuam em linha, sem setas.
- **Disciplinas e professores:** 3 por vez no desktop, 2 no tablet e 1 no celular, com setas e pontos.
- **Diferenciais:** cartões na largura toda no celular e setas centralizadas abaixo, fora do texto. Todas as setas do Elementor viraram botões de 44px com contorno.
- **Banner de matrículas:** no celular o selo entra no fluxo abaixo do texto, sem invadir o título da seção seguinte; o selo do MEC do hero fica dentro da tela.
- **Impacto:** os 4 cartões em 4 colunas, 2 no tablet e 1 no celular, com margem lateral.
- **"Por que estudar":** painéis na largura toda no celular.
- **"30 anos":** números lado a lado e com respiro do texto.
- **Textos de apoio** centralizados em largura de leitura; palavras longas quebram em vez de vazar (WCAG 1.4.12).
- **Poppins** também nos rótulos e valores das caixas de fato (estavam em Roboto).

Verificação (axe, 5 larguras): 320, 375, 820, 1280 e 1440px sem violações (exceto landmarks, que dependem do tema), sem rolagem lateral, sem texto abaixo de 12px e com 100% do texto em Poppins. Reflow a 320px com espaçamento de texto forçado (WCAG 1.4.12) sem rolagem lateral. Pendente: passada com leitor de tela e teste em aparelho real.


---

## Decisões de design e guia para as próximas páginas (registrado em 18/11/2026)

### Escopo (decisão da empresa)
| Página | Novo layout? |
|---|---|
| Administração (modelo, concluída localmente) | Sim |
| Marketing, Processos Gerenciais, Recursos Humanos | Sim — aplicar o mesmo conjunto |
| Pedagogia, Educação Física, Tradução e Interpretação (Inglês/Português) | **Não** — ficam como estão |

`_tools/apply_v1_ds.py` tem a lista `SLUGS_DS`; só esses 4 cursos recebem o bloco DS-PHORTE no `local.css`. Os 3 fora do escopo recebem apenas o CSS base.

### Regras de design adotadas
1. **Só CSS e atributos.** Nenhuma mudança estrutural no HTML do Elementor, exceto: rodapé removido (o site já tem), ícones Lucide inline nos widgets existentes, `id="content"` para o skip-link, atributos ARIA.
2. **Design System Phorte, só Poppins.** Tokens em `_shared/phorte-tokens.css`. Vinho `#7D1B1B` (fundos fortes), vermelho `#D42B2B`/`#A81E1E`, bordas `#8C8C8C` em controles.
3. **Sem degradês.** Cores chapadas. Fundos de imagem só se já forem claros (hero) e sem camada de overlay.
4. **Sombras:** só onde ajudam (cartões flutuantes, foto da notícia, hover). Repouso: borda 1px.
5. **Coluna única de 1140px** (`--ph-coluna`), margem lateral fluida `clamp(1rem,4vw,2.5rem)` (`--ph-margem`). Toda seção parte da mesma borda esquerda (141px a 1440px). Exceção intencional: cartão "Vamos iniciar o Processo Seletivo?" (56rem, centralizado). Cuidado com `padding-left:80px` herdado do Elementor em colunas.
6. **Títulos nunca quebram no meio da palavra** (`overflow-wrap:normal`; só parágrafos, listas e links quebram). Nome do curso e H1 com fonte fluida (`clamp`).
7. **Alturas iguais** em cartões de uma mesma linha (disciplinas, professores, impacto, diferenciais).
8. **Carrosséis:** setas de 44px com contorno e ícone na cor do texto (`#1A1A1A`; o Elementor deixava `fill` cinza claro, por isso usar `:not(#ph)` + `fill:currentColor`), pontos de 24px de área de toque, sem barra de rolagem. Desktop 3 por vez, tablet 2, celular 1.
9. **Professores:** minibio truncada em 4 linhas, um "Ver mais" abre todos; foto como `<img>` injetada (sem cantos escuros).
10. **Banner de matrículas inteiro clicável** (local.js repassa o clique ao link do selo).
11. **Impacto:** título centralizado, notícia acima, 4 cartões lado a lado (2 no tablet, 1 no celular).
12. **Botão do vestibular:** faixa rosa clara com botão vermelho e seta (opções A/B/C em `administracao/v1/cta-opcoes.html`; escolha final ainda pendente).
13. **Responsivo:** tablet ≤1024px, celular ≤767px; "Por que estudar" empilha; selos entram no fluxo no celular.
14. **Acessibilidade:** WCAG 2.2 AA, axe sem violações em 320/375/820/1280/1440 (exceto landmarks do tema), alvo mínimo 24px, foco visível, skip-link.

### Roteiro para aplicar em Marketing, Processos Gerenciais e RH
1. `python -I _tools/apply_v1_ds.py marketing processos-gerenciais recursos-humanos` (gera `assets/local.css` e aplica os patches de HTML).
2. Copiar `_shared/v1-local.js` e `_shared/salario-02.css` para `<curso>/v1/assets/`.
3. Fundo do hero: o script usa automaticamente a imagem `*-BG-*.webp` da pasta `assets/img` de cada curso.
4. Verificar em 1440/1280/1024/820/375px: bordas alinhadas, sem rolagem horizontal, nome do curso sem quebra, setas visíveis, axe.
5. Pendências gerais: escolher o botão do vestibular e confirmar o link `https://typechat.phorte.org.br/vestibular-simplificado` (hoje `href="#"`); passada com leitor de tela; teste em aparelho real; migração para o WordPress/Elementor (tabela acima).

### Observações de conteúdo
- "Gestão em Ação" repetido: é disciplina de verdade, aparece em 8 semestres (um cartão por semestre). Sem erro; se confundir, destacar o semestre no cartão.

**Status (18/11/2026):** layout aplicado localmente em Marketing, Processos Gerenciais e RH (passos 1–3 feitos; verificado em 1440/1024/375px: sem rolagem horizontal, bordas alinhadas, setas escuras, fundo do hero presente). Falta conferência visual página a página e a passada com leitor de tela.
