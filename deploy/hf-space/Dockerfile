# Backend da aba Demo do Anti-Ruído — Hugging Face Space (sdk: docker)
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        libsndfile1 ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# usuário não-root (exigência/boa prática dos Spaces)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH" \
    HOME=/home/user \
    NUMBA_CACHE_DIR=/tmp/numba

WORKDIR /home/user/app
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt flask flask-cors gunicorn

COPY --chown=user anti_ruido/ anti_ruido/
COPY --chown=user app/ app/

EXPOSE 7860
# 1 worker (o perfil é estado em memória/disco compartilhado) + threads p/ blocos concorrentes
CMD ["gunicorn", "--chdir", "app", "--bind", "0.0.0.0:7860", "--workers", "1", "--threads", "8", "--timeout", "120", "server:app"]
