# DESIGN.md — Sistema de Design do site Anti-Ruído

Este documento mapeia o sistema de design implementado em `site/styles.css` e
aplicado nas páginas `index.html`, `como-funciona.html`, `demo.html`,
`privacidade.html` e `termos.html`. Serve como referência única para manter
consistência visual ao adicionar novas páginas ou seções.

A metodologia de design usada para tomar essas decisões está salva em
[`.claude/skills/artifact-design/SKILL.md`](../.claude/skills/artifact-design/SKILL.md)
— vale ler antes de propor uma mudança visual grande.

## Referências de estilo pesquisadas

Pedido original: usar `meiwensee.com` e `vorrathwoodworks.com` como referência
de design, fontes e fundo. Rede liberada durante o desenvolvimento; a
renderização visual completa (screenshot) não foi possível — o Chromium via
proxy do ambiente sofreu `ERR_CONNECTION_RESET` em qualquer domínio externo,
uma limitação técnica do ambiente, não dos sites — mas o código-fonte
(HTML/CSS reais servidos pelos dois sites) foi obtido e analisado
diretamente.

**Achados reais (extraídos do HTML/CSS servido, não inferidos):**

| | meiwensee.com | vorrathwoodworks.com |
|---|---|---|
| Negócio | Designer multidisciplinar (LA) — identidade de marca, web, fotografia | Marcenaria artesanal ("Vorrath" = "estoque/despensa" em alemão) |
| Fonte(s) | **Inter** (única família, pesos 400/500/700 + itálicos) | **Sorts Mill Goudy** (serifada com itálico) + **Heebo** (sans, pesos 300-700) |
| Estrutura de seção | Alterna temas `dark-bold` e `white`/`white-bold` (alto contraste editorial) | Sem alternância de tema detectada — provavelmente fundo neutro único, deixando a fotografia de madeira carregar a cor |
| Cor real confirmada | `#faf9f6` (off-white quente) usado em texto sobre overlay de imagem | Não extraível via CSS estático (paleta aplicada via classes de tema, não em `:root`) |

**O que foi adotado no Anti-Ruído e por quê:**
- **Par tipográfico serifada+itálico / sans limpa** (o padrão dos dois sites, mais explícito no Vorrath Woodworks) — já era a lógica do sistema (Fraunces, que tem itálico nativo elegante). Adicionamos **Heebo** como fonte de corpo (`--sans`) no lugar da stack de sistema genérica, como referência direta ao Vorrath Woodworks — mais "desenhado", mantendo a stack de sistema como fallback de performance/offline.
- **Off-white quente, nunca branco puro** — já era a prática do sistema (`--text: #ece7db`); o `#faf9f6` do meiwensee confirma que é uma escolha comum em design editorial/artesanal, não uma peculiaridade nossa.

**O que foi considerado e conscientemente *não* adotado:**
- **Inter como fonte única** (meiwensee): é citada como o "rosto seguro" e clichê de design gerado por IA — evitamos deliberadamente por já termos um par tipográfico com mais personalidade (Fraunces + Heebo).
- **Alternância de temas claro/escuro por seção** (meiwensee): romperia a metáfora central do Anti-Ruído (fundo escuro = ruído do mundo; único acento quente = a voz). Copiar esse padrão sem necessidade narrativa enfraqueceria o conceito, não o reforçaria.

## Conceito central

**"O mundo é ruído; a voz escolhida é o único elemento quente."** Todo o
sistema visual deriva dessa ideia: um fundo escuro e frio (o caos sonoro ao
redor) contra o qual um único acento âmbar (a voz que se escolhe ouvir) se
destaca — nunca o contrário, nunca mais de um acento quente competindo por
atenção ao mesmo tempo.

## Cores

Definidas como custom properties em `:root` (`styles.css`), usadas sempre por
papel/função — nunca hex direto no HTML/CSS de página.

| Token | Hex | Papel |
|---|---|---|
| `--bg` | `#0f1217` | Fundo base — quase-preto azulado, não preto puro (reduz halo/fadiga visual) |
| `--bg-raised` | `#161b23` | Superfícies elevadas: cards, stats, footer-cols, diálogo |
| `--bg-sunken` | `#0a0d11` | Superfícies "afundadas": aviso de honestidade, offline banner |
| `--text` | `#ece7db` | Texto principal — off-white quente, não branco puro (mesmo motivo do `--bg`) |
| `--text-muted` | `#9a948a` | Texto secundário/legendas — contraste reduzido mas ainda acessível |
| `--voice` | `#e8a33d` | **O único acento quente do sistema.** CTAs primários, ênfases, ícones ativos |
| `--voice-strong` | `#f5c069` | Hover/estado ativo do acento; links |
| `--voice-deep` | `#8a5a10` | Reservado para textos sobre fundo âmbar quando necessário |
| `--noise` | `#4a5262` | Cinza-azulado frio — rótulos de "categoria" nos cards de comparação |
| `--border` | `rgba(236,231,219,.12)` | Divisores e bordas padrão, sutis |
| `--border-strong` | `rgba(232,163,61,.45)` | Bordas de destaque (card "ours", cta-band, diálogo) |

Cor semântica adicional (fora da paleta principal, usada com parcimônia):
- **WhatsApp:** `#3fae63` / hover `#4dc476` — verde reconhecível da marca, usado *só* no botão de WhatsApp, sempre acompanhado do texto "Chamar no WhatsApp" (nunca só a cor/ícone).

**Regra de ouro:** um único acento quente (`--voice`) por vez. Se uma seção
precisar de uma segunda cor de destaque, ela deve ser neutra/fria (como
`--noise`) ou semântica e rotulada (como o verde do WhatsApp), nunca uma
segunda cor "quente" competindo com `--voice`.

## Tipografia

Três famílias, cada uma com um papel fixo — nunca misturadas fora do papel:

| Papel | Família | Uso |
|---|---|---|
| Display | `"Fraunces"` (serif, itálico disponível) → `Georgia` → serif do sistema | H1/H2, números de destaque (`.stat .num`), números dos passos (`.step .n`), títulos de diálogo |
| Corpo | `"Heebo"` (Google Fonts, pesos 300-700) → stack de sistema como fallback | Parágrafos, navegação, botões, listas |
| Técnico/rótulo | `ui-monospace, "SF Mono", Menlo...` | Eyebrows (rótulos acima de títulos), tags de categoria, cabeçalhos de coluna do footer |

Fraunces e Heebo são carregados via Google Fonts (`<link>` no `<head>` de cada página, junto com `preconnect`); a stack de sistema em `--sans` garante texto legível mesmo se a rede/fonte falhar.

Escala tipográfica (`clamp()` fluido, sem breakpoints fixos de font-size):
- H1: `clamp(2.4rem, 6vw, 4.2rem)`, peso 500, `line-height: 1.08`
- H2: `clamp(1.6rem, 3.4vw, 2.3rem)`, peso 500
- Corpo (lede): `clamp(1.1rem, 2vw, 1.3rem)`
- Corpo padrão: `1.0625rem` / `line-height: 1.65` (espaçamento generoso — ver seção de acessibilidade)
- Eyebrow/mono: `0.75rem`, `letter-spacing: 0.14em`, uppercase

`text-wrap: balance` em H1/H2 e `text-wrap: pretty` na lede — quebras de linha
sempre visualmente equilibradas, nunca uma palavra órfã sozinha.

## Layout e espaçamento

- Container único: `.wrap` (`max-width: 1040px`, padding lateral `1.5rem`); `.narrow` (`720px`) para prosa longa (FAQ, "como funciona").
- Seções (`section`) sempre com `border-top` sutil (`--border`) em vez de sombra — separação limpa, sem ruído visual adicional.
- Grids responsivos via `auto-fit`/`minmax()` (stats, compare, footer-grid) — nunca breakpoints manuais por número de colunas fixo, exceto o footer (4→2→1 colunas, definido explicitamente para legibilidade).
- Cards (`.stat`, `.compare .card`, `.demo-card`) sempre: `--bg-raised` + `1px solid --border` + `border-radius: 10-16px`. Nunca sombra (`box-shadow`) — o sistema usa apenas borda + diferença de superfície para indicar elevação, o que é mais estável visualmente sob zoom/temas variados.

## Componentes

- **Botões** (`.btn`): pílula (`border-radius: 999px`), 3 variantes — `.btn` (primário, âmbar), `.btn.ghost` (secundário, contorno), `.btn.call`/`.btn.whatsapp` (ação semântica). Todos com `:hover` sutil (não dependem de cor para affordance — têm padding generoso e cursor pointer).
- **Faixa de CTA** (`.cta-band`, `.contact-band`): fundo em gradiente suave do acento sobre `--bg-raised`, borda `--border-strong`. Reservada para no máximo 1-2 por página — nunca empilhar mais de duas faixas de destaque seguidas.
- **FAQ** (`.faq details`): usa `<details>/<summary>` nativo — acessível por teclado e leitor de tela sem JavaScript.
- **Diálogo de cookies** (`dialog#cookieDialog`): `<dialog>` nativo (`showModal()`) — foco automático, `Esc` fecha, `::backdrop` nativo. Preferido a um modal em `<div>` construído do zero porque já entrega semântica e trap de foco corretos.
- **Footer**: grid de 4 colunas (marca/navegar/contato/endereço) + barra inferior com copyright e links legais separados por `|` (política de privacidade · termos de uso · gerenciar cookies). Estrutura idêntica em todas as páginas — muda apenas qual link de navegação fica ausente/presente.
- **Páginas "em construção"** (`.wip-box`): borda tracejada (`border: 1px dashed`), para diferenciar visualmente de conteúdo "pronto" — sinaliza honestamente que é provisório sem precisar de texto extra dizendo isso.

## Movimento e animação

- `html { scroll-behavior: smooth }`, mas com fallback: `@media (prefers-reduced-motion: reduce)` força `scroll-behavior: auto` **e** reduz qualquer `animation`/`transition` do site para ~0 — regra global, não precisa ser lembrada por componente novo.
- A única animação decorativa é a onda do hero (`#wave`, canvas), que já é **removida inteiramente** (não só desacelerada) quando `prefers-reduced-motion: reduce` está ativo.
- Nenhum autoplay de áudio/vídeo em lugar nenhum do site — os players (guiado e ao vivo) sempre exigem clique explícito do usuário.
- Nenhum carrossel, contador regressivo ambíguo ou conteúdo que se move/atualiza sozinho fora do controle do usuário (a única contagem regressiva, "gravando 10s", é uma ação que o próprio usuário iniciou clicando).

## Acessibilidade e design neurodivergente-friendly

Princípios aplicados deliberadamente, não apenas WCAG mínimo:

1. **Sem preto/branco puros.** `--bg` e `--text` são levemente dessaturados e quentes — reduz o contraste "estroboscópico" entre fundo e texto que pode ser desconfortável para hipersensibilidade visual.
2. **Um único acento de cor.** Reduz carga de decisão visual: em qualquer tela, há no máximo uma cor "quente" chamando atenção por vez (ver regra de ouro em Cores).
3. **Estrutura previsível.** A navegação (Início · Como funciona · Demo) mantém sempre a mesma ordem e os mesmos rótulos em todas as páginas; o footer segue a mesma estrutura de 4 colunas em todo lugar. Nada muda de posição entre páginas.
4. **Nunca só cor para significar estado.** Estado ativo de navegação usa cor **e** sublinhado (`aria-current="page"` + `border-bottom`); o botão de WhatsApp usa cor **e** ícone **e** texto explícito.
5. **Sem movimento inesperado.** Ver seção "Movimento e animação" acima — tudo é opt-in (clique do usuário) ou desacelerado/removido por padrão de acessibilidade do sistema operacional.
6. **Linguagem direta e literal.** Frases curtas, uma ideia por vez, sem metáforas obscuras nos textos de interface (títulos podem ser mais poéticos; botões e status nunca são).
7. **`skip-link`** ("Pular para o conteúdo") em todas as páginas — para quem navega por teclado/leitor de tela evitar repetir o menu a cada página.
8. **Foco sempre visível**: `a:focus-visible, button:focus-visible` com contorno de 2px na cor de acento — nunca `outline: none` sem substituto.
9. **Espaçamento generoso**: `line-height: 1.65` no corpo do texto, `gap` consistente entre elementos de grid (nunca margin colapsando de forma imprevisível).
10. **Zero imagens de banco/stock.** Todo elemento visual é gerado em CSS/Canvas (a onda do hero, os ícones são emoji ou glifos tipográficos) — sem fotografia genérica de terceiros, que tende a introduzir ruído visual e licenciamento incerto.

## Como estender

Ao criar uma nova página ou seção:
1. Reutilize `.wrap` como container e siga a hierarquia H1 (só 1 por página) → H2 → H3.
2. Novas cores de destaque só entram na paleta com justificativa (nova cor semântica rotulada, nunca uma segunda cor "decorativa").
3. Copie o footer completo (marca + 3 colunas + barra legal + diálogo de cookies + `footer.js`) de `demo.html` — é a versão mais recente/completa.
4. Rode o teste manual de `prefers-reduced-motion` (DevTools → Rendering → Emulate CSS media → `prefers-reduced-motion: reduce`) antes de adicionar qualquer animação nova.
