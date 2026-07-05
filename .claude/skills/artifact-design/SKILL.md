---
name: artifact-design
description: Design guidance and fundamentals used for this project's visual work (site, one-pagers, dashboards). Salva no repositório para referência de qualquer sessão futura do Claude Code neste projeto — não é gerado automaticamente pelo produto Claude, é uma cópia local do skill nativo "artifact-design" usado para desenhar site/, DESIGN.md e os artifacts de pitch.
---

# Anti-Ruído — Registro do skill de design usado no projeto

Este arquivo é uma **cópia salva** do skill nativo `artifact-design` do Claude,
usado para tomar as decisões visuais do site (`site/`), do `site/DESIGN.md` e
dos one-pagers/artifacts de pitch deste projeto. Ele não existe como pacote de
arquivos no ambiente onde foi gerado (é servido inline pela plataforma) — foi
transcrito aqui para o time e para sessões futuras terem a mesma referência
sem depender do acesso ao skill original.

## Como foi aplicado neste projeto

- **Tratamento calibrado ao pedido**: o site (`index.html`, `demo.html`) recebeu
  tratamento editorial (é a peça que convence o visitante); `DESIGN.md` recebeu
  tratamento utilitário (documento de referência, sem "hero" nem floreio).
- **Sistema de design existente respeitado**: qualquer novo componente reusa os
  tokens de `site/styles.css` (`--bg`, `--voice`, `--serif`, `--sans`, `--mono`)
  em vez de introduzir cores/fontes soltas — ver `site/DESIGN.md` para a tabela
  completa de tokens.
- **Tema único, não dois temas**: o Anti-Ruído comprometeu-se deliberadamente
  com um único mundo visual (fundo escuro = ruído; acento âmbar = a voz
  escolhida) em vez de suportar light/dark — está documentado como escolha
  consciente em `DESIGN.md`, não omissão.
- **Evitar "cara de IA"**: por isso o corpo do texto usa Heebo (referência real
  do site vorrathwoodworks.com) em vez de Inter/Space Grotesk, e o site não
  usa emoji como marcador de seção nem cards com barra de acento arredondada
  genérica.

## Fundamentos (texto original do skill)

### Ler o pedido primeiro

Calibrar o tratamento, não se deve desenhar. Um documento merece o mesmo
cuidado que uma landing page — o que muda é o tratamento com que esse cuidado
é entregue.

Muitos pedidos pedem um tratamento mais utilitário: um plano, um memorando,
uma demo. Torne-o polido: inclua hierarquia tipográfica real, espaçamento
cuidadoso e uma paleta própria, mas evite exagerar no design. A maioria das
páginas não precisa de um hero gigante e chamativo. Mantenha floreios com
bom gosto e limitados.

Alguns pedidos pedem um tratamento editorial: uma landing page, um jogo, um
app ou ferramenta que a pessoa vai guardar ou compartilhar.

Na dúvida: uma página bem composta nunca é a escolha errada; uma identidade
visual exagerada às vezes é.

### Fundamentos para todo artifact

**Honre o que já existe.** Procure primeiro um sistema de design existente —
CLAUDE.md, um arquivo de tokens/tema, estilos de componentes já existentes.
Quando existir, aplique-o; tudo abaixo preenche lacunas e nunca sobrepõe.
Precedência: as palavras do usuário, depois o sistema existente do projeto,
depois suas escolhas.

**Ancore no assunto.** Se o assunto não estiver claro, defina-o: um assunto
concreto, seu público, e a tarefa única da página. O próprio mundo do
assunto — seus materiais, instrumentos, vocabulário — é de onde vêm escolhas
distintas. Construa sempre com conteúdo real, nunca lorem ipsum.

**Combine tipografias.** A tipografia carrega a página mesmo quando a página
não é sobre tipografia. Mantenha o texto corrido perto de 65 caracteres de
largura; defina uma escala tipográfica e mantenha-a; dê `text-wrap: balance`
aos títulos, espaço para respirar ao corpo do texto, e um toque de
letter-spacing aos rótulos em caixa alta.

**Escolha neutros, não use por padrão.** Um cinza médio puro soa não
pensado; um cinza com leve viés de matiz em direção ao acento da página soa
escolhido. Branco puro e quase-preto são fundos válidos quando combinam com
o assunto — o importante é que o neutro tenha sido escolhido, não herdado.

**Projete os dois temas** (quando aplicável). A página renderiza no tema do
usuário: `prefers-color-scheme` carrega a preferência do SO. O padrão robusto
é em nível de token: defina a paleta como custom properties em `:root`,
redefina os tokens sob `@media (prefers-color-scheme: dark)` — estilize
componentes através dos tokens, nunca diretamente dentro do media query.
Um design que se compromete deliberadamente com um único mundo visual pode
permanecer em tema único — torne isso uma escolha, não uma omissão.

**Deixe o layout cuidar do espaçamento.** Disponha grupos de irmãos com flex
ou grid e `gap`, não margens por elemento que colapsam ou dobram
silenciosamente. Conteúdo largo — tabelas, código, diagramas — recebe
`overflow-x: auto` no próprio container.

**Evite design "gerado por IA".** Os padrões que mais aparecem: cream quente
(#F4F1EA) com serifada display e acento terracota; quase-preto com um único
verde-ácido ou vermelho pipocando; réguas finas estilo jornal com colunas
densas; hero gradiente roxo-azul sobre branco; Inter ou Space Grotesk como
fonte "segura"; emoji como marcador de seção; tudo centralizado;
`rounded-lg` em tudo; barra de acento em cards arredondados. Onde o usuário
define uma direção visual, siga-a exatamente. Onde nada for especificado,
não gaste essa liberdade em um desses padrões.

**Construa de forma limpa.** Atenção a elementos sobrepostos, colisões de
cascata CSS, fallbacks silenciosos de fonte. Feche toda tag não-vazia, use
aspas duplas em atributos, dê foco de teclado visível, respeite
`prefers-reduced-motion`.

**Regras de CSS.** Cuidado com especificidade de seletores — é fácil gerar
classes que se cancelam mutuamente.

**Escrevendo o texto.** Palavras são material de design, não decoração.
Escreva do lado da tela do usuário — nomeie as coisas pelo que as pessoas
reconhecem, não por como o sistema é construído. Voz ativa; um controle diz
exatamente o que acontece ("Publicar", depois um toast "Publicado").

**Estrutura é informação.** Numeração, eyebrows, divisores, rótulos devem
codificar algo verdadeiro sobre o conteúdo, não decorá-lo. Marcadores
numerados (01/02/03) só fazem sentido se o conteúdo for de fato uma
sequência real.

**Quando é uma interface, não um documento.** Um dashboard é escaneado e
operado, não lido de cima a baixo — a informação de estado (chip, pill,
faixa de severidade) importa tanto quanto o número.

### Processo

Antes de escrever código, esboce um plano de design compacto — um sistema de
tokens com cor, tipo e layout:
- **Cor**: descreva a paleta como 4-6 valores hex nomeados.
- **Tipo**: tipografias para 2+ papéis — uma face de display com
  personalidade usada com moderação, uma face de corpo complementar, e uma
  face utilitária para legendas/dados se necessário.
- **Layout**: um conceito de layout em uma ou duas frases.

Depois construa, seguindo o plano.

### Quando o pedido é editorial

A postura muda: o cliente já rejeitou propostas que pareciam templates, e
está pagando por um ponto de vista distinto. Faça escolhas opinativas, e
corra um risco estético real onde isso servir ao trabalho.

- **O hero é uma tese**: abra com a coisa mais característica do mundo do
  assunto.
- **A tipografia carrega a personalidade da página.**
- **Aproveite o movimento deliberadamente** — nem toda página precisa de
  animação; excesso de animação contribui para a sensação de "gerado por IA".
- **Combine complexidade com a visão**: direções maximalistas precisam de
  execução elaborada; direções mínimas precisam de precisão em espaçamento,
  tipo e detalhe.
- **Gaste sua ousadia em um só lugar**; mantenha tudo ao redor quieto.
