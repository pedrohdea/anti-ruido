# anti-ruido

Fone de ouvido B2C que identifica o ambiente ao redor, gera ruído branco adaptativo para mascarar o ruído de fundo e separa/isola a voz de quem está conversando com você — para permitir uma conversa clara em ambientes muito barulhentos (bares, restaurantes, eventos, transporte público, ruas).

Projeto em desenvolvimento no Startup Weekend. Este repositório está, por enquanto, focado em **validação de negócio** (não há ainda implementação técnica da solução).

- Documento vivo de validação (metodologias de startup, Lean Canvas, concorrência, SWOT, mercado, riscos etc.): [`docs/business-validation.md`](docs/business-validation.md)
- Planilha de métricas de startup (CAC, LTV, churn, runway, k-factor etc. + detecção de Inflection/Tipping/Turning Point): [`docs/planilha-metricas-startup.xlsx`](docs/planilha-metricas-startup.xlsx) (abrir no Google Sheets ou Excel)
- Site estático de divulgação e captação de interesse: [`site/`](site/) (landing page + explicação do produto + formulário de interesse)
- Protótipo de separação de fala com perfil de voz (timbre/pitch/intensidade) e ajustes de gradiente/tolerância: [`prototype/`](prototype/) — liga com um comando via Docker (`cd prototype && docker compose run --rm anti-ruido`)

## Site — desenvolvimento e publicação

O site é 100% estático (HTML/CSS, sem build). Para ver localmente:

```bash
cd site && python3 -m http.server 8000
# abra http://localhost:8000
```

O deploy é automático via **integração Git do Cloudflare (Workers Builds)**: o repositório está conectado ao projeto `anti-ruido` no Cloudflare, e cada push dispara um build/deploy — o bot `cloudflare-workers-and-pages` comenta o status direto no PR, com link para os logs. A configuração de build (diretório `site/` como assets estáticos) fica no dashboard do Cloudflare em **Workers & Pages → anti-ruido → Settings → Build**. A URL pública aparece no mesmo painel (domínio `*.workers.dev`, com opção de domínio próprio).

*(Um workflow de deploy via GitHub Actions + wrangler existiu aqui, mas foi removido quando a integração Git foi conectada — dois caminhos de deploy para o mesmo projeto só gerariam confusão. Se um dia a integração for desligada, o workflow pode ser recuperado do histórico do git: `git log --diff-filter=D -- .github/workflows/deploy-site.yml`.)*
