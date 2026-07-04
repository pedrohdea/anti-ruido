# anti-ruido

Fone de ouvido B2C que identifica o ambiente ao redor, gera ruído branco adaptativo para mascarar o ruído de fundo e separa/isola a voz de quem está conversando com você — para permitir uma conversa clara em ambientes muito barulhentos (bares, restaurantes, eventos, transporte público, ruas).

Projeto em desenvolvimento no Startup Weekend. Este repositório está, por enquanto, focado em **validação de negócio** (não há ainda implementação técnica da solução).

- Documento vivo de validação (metodologias de startup, Lean Canvas, concorrência, SWOT, mercado, riscos etc.): [`docs/business-validation.md`](docs/business-validation.md)
- Site estático de divulgação e captação de interesse: [`site/`](site/) (landing page + explicação do produto + formulário de interesse)

## Site — desenvolvimento e publicação

O site é 100% estático (HTML/CSS, sem build). Para ver localmente:

```bash
cd site && python3 -m http.server 8000
# abra http://localhost:8000
```

O deploy é automático via GitHub Actions → **Cloudflare Pages** ([`.github/workflows/deploy-site.yml`](.github/workflows/deploy-site.yml)): todo push na branch `main` que tocar em `site/` publica uma nova versão (também dá para disparar manualmente na aba Actions).

Configuração única (uma vez só):

1. Crie o projeto no Cloudflare: dashboard → **Workers & Pages → Create → Pages → Direct Upload**, com o nome `anti-ruido` (ou `npx wrangler pages project create anti-ruido`).
2. Crie um API Token em **My Profile → API Tokens** com o template *"Edit Cloudflare Workers"* (ou permissão `Cloudflare Pages — Edit`).
3. No GitHub, em **Settings → Secrets and variables → Actions**, adicione:
   - `CLOUDFLARE_API_TOKEN` — o token criado acima
   - `CLOUDFLARE_ACCOUNT_ID` — visível na sidebar do dashboard do Cloudflare
4. Faça merge/push na `main`. O site sobe em `https://anti-ruido.pages.dev`.
