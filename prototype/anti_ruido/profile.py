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
import logging
from dataclasses import asdict, dataclass, field
from pathlib import Path

import librosa
import numpy as np

logger = logging.getLogger(__name__)

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

    def log(self) -> None:
        logger.info("Voice profile extracted: sample_rate=%s", self.sample_rate)
        logger.info("Pitch: median=%.1f Hz p10=%.1f Hz p90=%.1f Hz", self.pitch_median_hz, self.pitch_p10_hz, self.pitch_p90_hz)
        logger.info("Spectral: centroid=%.1f Hz bandwidth=%.1f Hz", self.spectral_centroid_hz, self.spectral_bandwidth_hz)
        logger.info("MFCCs: mean[0]=%.3f std[0]=%.3f count=%d", self.mfcc_mean[0] if self.mfcc_mean else 0.0, self.mfcc_std[0] if self.mfcc_std else 0.0, len(self.mfcc_mean))
        logger.info("Volume: rms_dbfs=%.1f dBFS peak_dbfs=%.1f dBFS peak_amplitude=%.6f", self.rms_dbfs, self.peak_dbfs, self.peak_amplitude)

    def save(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(asdict(self), indent=2))

    @classmethod
    def load(cls, path: str | Path) -> "VoiceProfile":
        return cls(**json.loads(Path(path).read_text()))


def _dbfs(x: float) -> float:
    return float(20.0 * np.log10(max(x, 1e-10)))


MAX_PROFILE_SECONDS = 10.0  # amostra de perfil é SEMPRE cortada em 10s


def extract_profile(wav_path: str | Path, sr: int | None = 22050) -> VoiceProfile:
    """Extrai o perfil de voz de um arquivo WAV/MP3/FLAC/OGG com fala da pessoa.

    A amostra é limitada a MAX_PROFILE_SECONDS (10s) — o que passar disso é
    descartado, tanto para manter o perfil consistente quanto para a análise
    ser rápida.
    """
    logger.info("Loading audio file %s with target sr=%s", wav_path, sr)
    y, sr = librosa.load(str(wav_path), sr=sr, mono=True, duration=MAX_PROFILE_SECONDS)
    logger.info("Loaded audio: samples=%s sr=%s duration=%.2fs", len(y), sr, len(y) / sr)
    if len(y) < N_FFT * 4:
        logger.error("Audio too short: %s samples", len(y))
        raise ValueError("Amostra curta demais — grave pelo menos ~1s de fala.")

    # Considera só os trechos com energia (descarta silêncio da amostra),
    # para o perfil não ser contaminado pelas pausas.
    intervals = librosa.effects.split(y, top_db=35) # TODO, pode ser varivel/configuravel pelo usuário
    logger.info("Found %s voiced intervals", len(intervals))
    voiced = np.concatenate([y[a:b] for a, b in intervals]) if len(intervals) else y
    logger.info("Voiced audio total samples=%s duration=%.2fs", len(voiced), len(voiced) / sr)

    # Altura (F0) — pyin é robusto a ruído moderado; NaN = quadro sem pitch.
    fmin = librosa.note_to_hz("C2")
    fmax = librosa.note_to_hz("C6")
    logger.info("Extracting pitch with pyin (fmin=%.1f Hz fmax=%.1f Hz)", fmin, fmax)
    f0, _, _ = librosa.pyin(
        voiced,
        fmin=fmin,   # ~65 Hz — voz masculina grave # TODO: Isso não pdoe ser fixo. Use um default, mas adicione na aba de mais configurações.
        fmax=fmax,   # ~1 kHz — margem p/ voz aguda # TODO: Isso não pdoe ser fixo. Use um default, mas adicione na aba de mais configurações.
        sr=sr,
        frame_length=N_FFT * 2,
        hop_length=HOP,
    )
    logger.info("pyin pitch extraction produced %s frames", len(f0))
    f0 = f0[~np.isnan(f0)]
    logger.info("Valid pitch frames=%s", len(f0))
    if len(f0) == 0:
        logger.error("No pitch found in voiced audio")
        raise ValueError("Não encontrei pitch de fala na amostra — grave de novo, mais perto do microfone.")

    # Timbre
    mfcc = librosa.feature.mfcc(y=voiced, sr=sr, n_mfcc=N_MFCC, n_fft=N_FFT, hop_length=HOP)
    centroid = librosa.feature.spectral_centroid(y=voiced, sr=sr, n_fft=N_FFT, hop_length=HOP)
    bandwidth = librosa.feature.spectral_bandwidth(y=voiced, sr=sr, n_fft=N_FFT, hop_length=HOP)
    logger.info("Spectral feature frames: centroid=%s bandwidth=%s", centroid.shape[1], bandwidth.shape[1])

    # Intensidade / amplitude
    rms = librosa.feature.rms(y=voiced, frame_length=N_FFT, hop_length=HOP)
    logger.info("RMS frames=%s mean=%.6f", rms.shape[1], float(np.mean(rms)))

    profile = VoiceProfile(
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
    logger.info("Extracted voice profile from %s", wav_path)
    profile.log()
    return profile


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
