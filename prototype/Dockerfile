FROM python:3.12-slim

# libsndfile: leitura/escrita de WAV (soundfile)
# libportaudio2: captura de microfone (sounddevice, modo live)
RUN apt-get update && apt-get install -y --no-install-recommends \
        libsndfile1 libportaudio2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt sounddevice

COPY anti_ruido/ anti_ruido/
ENV PYTHONPATH=/app

# Volume de trabalho para trocar áudios/perfis com o host
VOLUME ["/data"]
WORKDIR /data

ENTRYPOINT ["python", "-m", "anti_ruido.cli"]
CMD ["demo", "--workdir", "/data/demo-out"]
