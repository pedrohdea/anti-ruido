---
title: Anti-Ruído API
emoji: 🎧
colorFrom: yellow
colorTo: gray
sdk: docker
app_port: 7860
pinned: false
---

# Anti-Ruído — backend da demo pública

API Flask que alimenta a aba **Demo** do site do Anti-Ruído (fone com seleção
de voz — projeto de Startup Weekend). Endpoints:

- `GET /api/health` — status
- `GET /api/profile` — perfil de voz atual (padrão: voz sintética da demo)
- `POST /api/profile` — grava um novo perfil (áudio de até 10s)
- `POST /api/filter?thermo=1..256` — filtra um bloco de áudio e devolve WAV

Código-fonte: repositório `pedrohdea/anti-ruido`, diretório `prototype/`.
Este Space é gerado por `deploy/hf-space/deploy-hf.sh`.
