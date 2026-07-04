"""Exporta a linha do tempo de características do som para visualização.

Para cada instante (~46 ms), calcula o que o algoritmo "vê":
  - nível (RMS em dBFS)          -> intensidade naquele instante
  - pitch/F0 (Hz, ou null)       -> altura da voz detectada
  - centroide espectral (Hz)     -> "brilho" do timbre
  - semelhança com o perfil 0..1 -> o escore que decide o corte
  - ganho aplicado 0..1          -> o que a separação fez naquele instante

O JSON gerado alimenta o visualizador HTML (gráfico sincronizado ao áudio).
"""

from __future__ import annotations

import json
from pathlib import Path

import librosa
import numpy as np

from .profile import HOP, VoiceProfile, N_FFT
from .separate import _frame_similarity


def analyze_timeline(
    input_path: str | Path,
    profile: VoiceProfile,
    tolerance: float = 0.5,
    gradient: float = 0.85,
    stride: int = 4,
) -> dict:
    """Retorna dict com metadados + série temporal (1 ponto a cada `stride` quadros)."""
    y, sr = librosa.load(str(input_path), sr=profile.sample_rate, mono=True)
    score, f0 = _frame_similarity(y, sr, profile)

    rms = librosa.feature.rms(y=y, frame_length=N_FFT, hop_length=HOP)[0]
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr, n_fft=N_FFT, hop_length=HOP)[0]

    softness = 0.08
    frame_mask = 1.0 / (1.0 + np.exp(-(score - tolerance) / softness))
    gain = (1.0 - gradient) + gradient * frame_mask

    n = min(len(score), len(rms), len(centroid), len(gain))
    idx = np.arange(0, n, stride)

    def _f0(i: int) -> float | None:
        v = f0[i] if i < len(f0) else np.nan
        return None if np.isnan(v) else round(float(v), 1)

    points = [
        {
            "t": round(float(i * HOP / sr), 3),
            "db": round(float(20 * np.log10(max(rms[i], 1e-10))), 1),
            "f0": _f0(int(i)),
            "centroid": round(float(centroid[i]), 0),
            "score": round(float(score[i]), 3),
            "gain": round(float(gain[i]), 3),
        }
        for i in idx
    ]
    return {
        "duration_s": round(len(y) / sr, 2),
        "sample_rate": int(sr),
        "tolerance": tolerance,
        "gradient": gradient,
        "profile": {
            "pitch_median_hz": profile.pitch_median_hz,
            "pitch_p10_hz": profile.pitch_p10_hz,
            "pitch_p90_hz": profile.pitch_p90_hz,
            "spectral_centroid_hz": profile.spectral_centroid_hz,
        },
        "points": points,
    }


def save_timeline(data: dict, path: str | Path) -> None:
    Path(path).write_text(json.dumps(data, ensure_ascii=False))
