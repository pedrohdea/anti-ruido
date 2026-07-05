#!/usr/bin/env bash
# Deploy do backend da demo no Hugging Face Spaces.
# Uso: HF_TOKEN=hf_xxx ./deploy-hf.sh <usuario-hf> [nome-do-space]
set -euo pipefail

HF_USER="${1:?uso: HF_TOKEN=hf_xxx ./deploy-hf.sh <usuario-hf> [nome-do-space]}"
SPACE_NAME="${2:-anti-ruido}"
: "${HF_TOKEN:?defina HF_TOKEN com um token de ESCRITA do Hugging Face}"

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

# 1) cria o Space (idempotente) via API
python3 - <<PY
from huggingface_hub import HfApi
api = HfApi(token="${HF_TOKEN}")
api.create_repo("${HF_USER}/${SPACE_NAME}", repo_type="space", space_sdk="docker", exist_ok=True)
print("Space ok:", "${HF_USER}/${SPACE_NAME}")
PY

# 2) monta o conteúdo do Space: Dockerfile + README + código do app
cp "$ROOT/deploy/hf-space/Dockerfile" "$STAGE/Dockerfile"
cp "$ROOT/deploy/hf-space/README-space.md" "$STAGE/README.md"
cp "$ROOT/prototype/requirements.txt" "$STAGE/requirements.txt"
cp -r "$ROOT/prototype/anti_ruido" "$STAGE/anti_ruido"
mkdir -p "$STAGE/app"
cp "$ROOT/prototype/app/server.py" "$STAGE/app/server.py"
cp -r "$ROOT/prototype/app/static" "$STAGE/app/static"
find "$STAGE" -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true

# 3) push
cd "$STAGE"
git init -q -b main
git add -A
git -c user.email=deploy@anti-ruido -c user.name=anti-ruido-deploy commit -qm "deploy"
git push -q -f "https://${HF_USER}:${HF_TOKEN}@huggingface.co/spaces/${HF_USER}/${SPACE_NAME}" main

echo
echo "Enviado. Acompanhe o build em: https://huggingface.co/spaces/${HF_USER}/${SPACE_NAME}"
echo "URL da API quando ficar verde:  https://${HF_USER}-${SPACE_NAME}.hf.space/api/health"
