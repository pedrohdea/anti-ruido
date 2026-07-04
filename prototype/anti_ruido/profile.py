"""Perfil de voz: extrai a "assinatura" acústica de uma pessoa a partir de
uma amostra de áudio (poucos segundos falando, o mais limpo possível).

O perfil captura as dimensões pedidas no conceito do produto:
  - altura (pitch/F0 mediano e faixa, em Hz)
  - timbre (média e desvio dos MFCCs + centroide/largura espectral)
  - intensidade (RMS médio, em dBFS)
  - amplitude (pico absoluto)
  - decibéis (nível médio e de pico, em dBFS)

O perfil é salvo em JSON e usado por separate.py para decidir, quadro a
quadro, o quanto do áudio se parece com a voz-alvo.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

import librosa
import numpy as np

# Janela de análise padrão (~46 ms a 22.05 kHz) — curta o bastante para
# acompanhar a fala, longa o bastante para estimar pitch com estabilidade.
N_FFT = 1024
HOP = 256
N_MFCC = 20


@dataclass
class VoiceProfile:
    sample_rate: int
    # altura
    pitch_median_hz: float
    pitch_p10_hz: float
    pitch_p90_hz: float
    # timbre
    mfcc_mean: list[float] = field(default_factory=list)
    mfcc_std: list[float] = field(default_factory=list)
    spectral_centroid_hz: float = 0.0
    spectral_bandwidth_hz: float = 0.0
    # intensidade / decibéis / amplitude
    rms_dbfs: float = 0.0
    peak_dbfs: float = 0.0
    peak_amplitude: float = 0.0

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(asdict(self), indent=2))

    @classmethod
    def load(cls, path: str | Path) -> "VoiceProfile":
        return cls(**json.loads(Path(path).read_text()))


def _dbfs(x: float) -> float:
    return float(20.0 * np.log10(max(x, 1e-10)))


def extract_profile(wav_path: str | Path, sr: int | None = 22050) -> VoiceProfile:
    """Extrai o perfil de voz de um arquivo WAV/FLAC/OGG com fala da pessoa."""
    y, sr = librosa.load(str(wav_path), sr=sr, mono=True)
    if len(y) < N_FFT * 4:
        raise ValueError("Amostra curta demais — grave pelo menos ~1s de fala.")

    # Considera só os trechos com energia (descarta silêncio da amostra),
    # para o perfil não ser contaminado pelas pausas.
    intervals = librosa.effects.split(y, top_db=35)
    voiced = np.concatenate([y[a:b] for a, b in intervals]) if len(intervals) else y

    # Altura (F0) — pyin é robusto a ruído moderado; NaN = quadro sem pitch.
    f0, _, _ = librosa.pyin(
        voiced,
        fmin=librosa.note_to_hz("C2"),   # ~65 Hz — voz masculina grave
        fmax=librosa.note_to_hz("C6"),   # ~1 kHz — margem p/ voz aguda
        sr=sr,
        frame_length=N_FFT * 2,
        hop_length=HOP,
    )
    f0 = f0[~np.isnan(f0)]
    if len(f0) == 0:
        raise ValueError("Não encontrei pitch de fala na amostra — grave de novo, mais perto do microfone.")

    # Timbre
    mfcc = librosa.feature.mfcc(y=voiced, sr=sr, n_mfcc=N_MFCC, n_fft=N_FFT, hop_length=HOP)
    centroid = librosa.feature.spectral_centroid(y=voiced, sr=sr, n_fft=N_FFT, hop_length=HOP)
    bandwidth = librosa.feature.spectral_bandwidth(y=voiced, sr=sr, n_fft=N_FFT, hop_length=HOP)

    # Intensidade / amplitude
    rms = librosa.feature.rms(y=voiced, frame_length=N_FFT, hop_length=HOP)

    return VoiceProfile(
        sample_rate=int(sr),
        pitch_median_hz=float(np.median(f0)),
        pitch_p10_hz=float(np.percentile(f0, 10)),
        pitch_p90_hz=float(np.percentile(f0, 90)),
        mfcc_mean=np.mean(mfcc, axis=1).tolist(),
        mfcc_std=(np.std(mfcc, axis=1) + 1e-8).tolist(),
        spectral_centroid_hz=float(np.mean(centroid)),
        spectral_bandwidth_hz=float(np.mean(bandwidth)),
        rms_dbfs=_dbfs(float(np.mean(rms))),
        peak_dbfs=_dbfs(float(np.max(np.abs(voiced)))),
        peak_amplitude=float(np.max(np.abs(voiced))),
    )


def describe(profile: VoiceProfile) -> str:
    """Resumo legível do perfil (para o terminal)."""
    return (
        f"Perfil de voz\n"
        f"  altura (pitch):   mediana {profile.pitch_median_hz:.0f} Hz "
        f"(faixa típica {profile.pitch_p10_hz:.0f}–{profile.pitch_p90_hz:.0f} Hz)\n"
        f"  timbre:           centroide {profile.spectral_centroid_hz:.0f} Hz, "
        f"largura {profile.spectral_bandwidth_hz:.0f} Hz, {len(profile.mfcc_mean)} MFCCs\n"
        f"  intensidade:      {profile.rms_dbfs:.1f} dBFS RMS\n"
        f"  pico:             {profile.peak_dbfs:.1f} dBFS (amplitude {profile.peak_amplitude:.3f})"
    )
