"""Servidor local do app Anti-Ruído (offline, roda com `make`).

Uma página, três funções:
  - gravar amostra de perfil (máx. 10s; padrão = voz da demo)
  - modo AO VIVO: microfone -> filtro (perfil + termômetro) -> fones
  - termômetro 1-256 e ajustes finos (tolerância/gradiente), mudáveis ao vivo

Todos os áudios persistidos em MP3 (via ffmpeg). O processamento ao vivo é
feito em blocos de ~1s (latência ~1-2s — protótipo, não produto embarcado).
"""

from __future__ import annotations

import io
import json
import logging
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf
from flask import Flask, jsonify, request, send_file

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from anti_ruido.profile import MAX_PROFILE_SECONDS, VoiceProfile, describe, extract_profile  # noqa: E402
from anti_ruido.separate import filter_chunk  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("anti-ruido.app")

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
PROFILE_PATH = DATA_DIR / "perfil.json"
SAMPLE_MP3 = DATA_DIR / "amostra-perfil.mp3"
SR = 22050

app = Flask(__name__, static_folder=str(APP_DIR / "static"), static_url_path="")

_profile: VoiceProfile | None = None


def _ffmpeg_to_wav(blob: bytes, max_seconds: float | None = None) -> np.ndarray:
    """Converte qualquer contêiner (webm/opus do navegador, mp3, wav) p/ mono 22.05k."""
    args = ["ffmpeg", "-loglevel", "error", "-i", "pipe:0"]
    if max_seconds:
        args += ["-t", str(max_seconds)]
    args += ["-ac", "1", "-ar", str(SR), "-f", "wav", "pipe:1"]
    out = subprocess.run(args, input=blob, capture_output=True, check=True).stdout
    y, _ = sf.read(io.BytesIO(out), dtype="float32")
    return np.asarray(y)


def _wav_to_mp3_file(y: np.ndarray, path: Path) -> None:
    buf = io.BytesIO()
    sf.write(buf, y, SR, format="WAV")
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", "pipe:0", "-b:a", "128k", str(path)],
        input=buf.getvalue(), capture_output=True, check=True,
    )


def _ensure_default_profile() -> None:
    """Perfil padrão = a voz sintética da demo (sempre disponível, sem microfone)."""
    global _profile
    if PROFILE_PATH.exists():
        _profile = VoiceProfile.load(PROFILE_PATH)
        logger.info("Perfil existente carregado de %s", PROFILE_PATH)
        return
    from anti_ruido.demo import _synth_voice

    logger.info("Gerando perfil padrão (voz da demo)…")
    y = _synth_voice(8.0, f0_base=150.0, seed=1) * 0.8
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        sf.write(f.name, y, SR)
        _profile = extract_profile(f.name)
    _profile.save(PROFILE_PATH)
    _wav_to_mp3_file(y, SAMPLE_MP3)
    logger.info("Perfil padrão salvo em %s", PROFILE_PATH)


def _thermo_to_params(thermo: int) -> tuple[float, float]:
    """Termômetro 1-256 -> (tolerance, gradient). 1 = filtro mínimo; 256 = máximo."""
    t01 = (max(1, min(256, thermo)) - 1) / 255.0
    return 0.15 + 0.70 * t01, 0.40 + 0.60 * t01


@app.get("/")
def index():
    return app.send_static_file("index.html")


@app.get("/api/profile")
def get_profile():
    assert _profile is not None
    return jsonify({
        "descricao": describe(_profile),
        "pitch_median_hz": _profile.pitch_median_hz,
        "amostra_mp3": SAMPLE_MP3.exists(),
        "max_seconds": MAX_PROFILE_SECONDS,
    })


@app.post("/api/profile")
def set_profile():
    global _profile
    blob = request.get_data()
    if not blob:
        return jsonify({"erro": "sem áudio"}), 400
    y = _ffmpeg_to_wav(blob, max_seconds=MAX_PROFILE_SECONDS)  # corta em 10s
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        sf.write(f.name, y, SR)
        try:
            _profile = extract_profile(f.name)
        except ValueError as e:
            return jsonify({"erro": str(e)}), 422
    _profile.save(PROFILE_PATH)
    _wav_to_mp3_file(y, SAMPLE_MP3)  # amostra persistida em MP3
    logger.info("Novo perfil gravado (%.1fs de áudio)", len(y) / SR)
    return jsonify({"descricao": describe(_profile)})


@app.post("/api/profile/default")
def reset_profile():
    PROFILE_PATH.unlink(missing_ok=True)
    SAMPLE_MP3.unlink(missing_ok=True)
    _ensure_default_profile()
    assert _profile is not None
    return jsonify({"descricao": describe(_profile)})


@app.post("/api/filter")
def filter_live():
    """Recebe um bloco de áudio do microfone, devolve o bloco filtrado (WAV).

    Parâmetros de query, ajustáveis a cada bloco (ao vivo):
      thermo=1..256  (termômetro; define tolerance+gradient)
      tolerance=0..1, gradient=0..1 (ajuste fino manual — sobrepõem o termômetro)
    Métricas do bloco vão no cabeçalho X-Metrics (JSON).
    """
    assert _profile is not None
    blob = request.get_data()
    if not blob:
        return jsonify({"erro": "sem áudio"}), 400
    thermo = request.args.get("thermo", type=int)
    tolerance = request.args.get("tolerance", type=float)
    gradient = request.args.get("gradient", type=float)
    if thermo is not None and (tolerance is None or gradient is None):
        t_tol, t_grad = _thermo_to_params(thermo)
        tolerance = t_tol if tolerance is None else tolerance
        gradient = t_grad if gradient is None else gradient
    tolerance = 0.5 if tolerance is None else min(1.0, max(0.0, tolerance))
    gradient = 0.85 if gradient is None else min(1.0, max(0.0, gradient))

    try:
        y = _ffmpeg_to_wav(blob)
    except subprocess.CalledProcessError:
        return jsonify({"erro": "áudio inválido"}), 422
    out, metrics = filter_chunk(y, SR, _profile, tolerance=tolerance, gradient=gradient)

    buf = io.BytesIO()
    sf.write(buf, out, SR, format="WAV")
    buf.seek(0)
    resp = send_file(buf, mimetype="audio/wav")
    resp.headers["X-Metrics"] = json.dumps({**metrics, "tolerance": tolerance, "gradient": gradient})
    return resp


_ensure_default_profile()

if __name__ == "__main__":
    print("\nAnti-Ruído app: http://localhost:8686  (Ctrl+C para parar)\n")
    app.run(host="127.0.0.1", port=8686, debug=False)
