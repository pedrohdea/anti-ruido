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

Configuração única (uma vez só) — o projeto Pages `anti-ruido` é criado automaticamente no 1º deploy, não precisa criar nada no dashboard:

1. No GitHub, em **Settings → Secrets and variables → Actions**, adicione os mesmos 2 secrets já usados no repo `rpg-de-mesa`:
   - `CLOUDFLARE_API_TOKEN` — token com permissão *"Cloudflare Pages: Edit"*
   - `CLOUDFLARE_ACCOUNT_ID` — ID da conta (dashboard → Workers & Pages)
2. Faça merge/push na `main` (ou rode o workflow manualmente na aba Actions). O site sobe em `https://anti-ruido.pages.dev`.
