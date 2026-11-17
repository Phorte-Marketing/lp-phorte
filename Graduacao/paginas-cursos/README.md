# Páginas de curso — Graduação (v1, v2, v3)

Sete cursos: Educação Física, Administração, Marketing, Pedagogia, Processos Gerenciais, Recursos Humanos, Tradução e Interpretação.

| Versão | O que é | Caminho |
|---|---|---|
| v1 | Cópia estática da página do site atual, sem header/navbar/popups/scripts, com CSS, imagens e fontes locais | `<curso>/v1/index.html` |
| v2 | Editorial claro | `<curso>/v2/index.html` |
| v3 | Impacto Phorte | `<curso>/v3/index.html` |

A seção de salários (direção 02 · Destaque de mercado, aprovada) está nas três versões. Dados em `_shared/salarios.json`, estilo em `_shared/salario-02.css`, origem no [protótipo](../prototipo-salarios/index.html).

## Como regenerar

```bash
python -I _tools/snapshot.py        # baixa as 7 páginas do site -> v1 (sobrescreve v1)
python -I _tools/inject_salary.py   # injeta a seção de salários na v1
python -I _tools/extract.py         # extrai o conteúdo da v1 -> <curso>/content.json
python -I _tools/build_variants.py  # gera v2 e v3
```

## Limites conhecidos

- v1 não executa o JS do WordPress/Elementor: carrosséis rolam por scroll horizontal, contadores mostram o valor final, animações e lottie foram removidos.
- v2/v3 são geradas a partir do conteúdo extraído; páginas com estrutura própria (Educação Física, Pedagogia, Tradução) usam renderização genérica e merecem revisão editorial.
- Preços, links de inscrição e dados salariais vêm do site atual e do protótipo; confirmar antes de publicar.
- Formulários (GSheetConnector), pop-ups e rastreadores não foram copiados.
- Para subir ao site: a v1 não é adequada (CSS do Elementor de ~1,5 MB); v2/v3 foram pensadas para virar template.
