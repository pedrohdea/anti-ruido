"""Separação de fala: atenua tudo que não se parece com a voz do perfil.

Pipeline (DSP clássico, sem GPU — roda em qualquer máquina):

  1. STFT do áudio de entrada.
  2. Pontuação de "semelhança com a voz-alvo" por quadro (~12 ms):
     combina timbre (distância de Mahalanobis simplificada nos MFCCs),
     altura (o pitch do quadro cai na faixa do perfil?) e presença de
     energia de fala.
  3. Máscara tempo-frequência: quadros parecidos com a voz mantêm o
     espectro; quadros diferentes são atenuados. Dentro de cada quadro,
     bins fora da banda útil da voz também são atenuados.
  4. Os dois controles do produto:
       - tolerance (0..1): o CORTE — quão parecido com o perfil um quadro
         precisa ser para contar como "a voz". Baixo = deixa passar mais
         (mais permissivo); alto = corta mais (mais rigoroso).
       - gradient (0..1): o GRADIENTE — quão fundo atenuar o que foi
         cortado. 1.0 = silencia; 0.5 = reduz pela metade (mais natural).
  5. Redução de ruído estacionário residual (spectral gating, noisereduce).

Limite conhecido (documentado no estudo de viabilidade): com DSP clássico a
separação é aproximada — para vozes muito parecidas ou ruído com fala densa,
o caminho é trocar o passo 2 por um embedding neural (Resemblyzer/VoiceFilter),
mantendo exatamente os mesmos controles de tolerância e gradiente.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import librosa
import noisereduce as nr
import numpy as np
import soundfile as sf
from scipy.ndimage import uniform_filter1d

from .profile import HOP, N_FFT, N_MFCC, VoiceProfile


@dataclass
class SeparationResult:
    output_path: str
    duration_s: float
    frames_kept_pct: float
    input_rms_dbfs: float
    output_rms_dbfs: float
    tolerance: float
    gradient: float


def _frame_similarity(y: np.ndarray, sr: int, profile: VoiceProfile) -> np.ndarray:
    """Pontuação 0..1 por quadro: quão parecido o quadro é com a voz-alvo."""
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=N_MFCC, n_fft=N_FFT, hop_length=HOP)
    mean = np.asarray(profile.mfcc_mean)[:, None]
    std = np.asarray(profile.mfcc_std)[:, None]

    # Timbre: distância normalizada ao perfil -> escore que decai suavemente.
    # (ignora o MFCC 0, que é energia/volume — volume não é identidade)
    z = (mfcc[1:] - mean[1:]) / std[1:]
    dist = np.sqrt(np.mean(z**2, axis=0))
    timbre_score = np.exp(-dist / 2.0)

    # Altura: pitch do quadro dentro da faixa típica do perfil (com folga de 20%).
    f0, _, _ = librosa.pyin(
        y,
        fmin=max(50.0, profile.pitch_p10_hz * 0.6),
        fmax=min(1100.0, profile.pitch_p90_hz * 1.8),
        sr=sr,
        frame_length=N_FFT * 2,
        hop_length=HOP,
    )
    lo, hi = profile.pitch_p10_hz * 0.8, profile.pitch_p90_hz * 1.2
    pitch_score = np.where(np.isnan(f0), 0.35, np.where((f0 >= lo) & (f0 <= hi), 1.0, 0.15))
    pitch_score = pitch_score[: timbre_score.shape[0]]
    if len(pitch_score) < len(timbre_score):
        pitch_score = np.pad(pitch_score, (0, len(timbre_score) - len(pitch_score)), constant_values=0.35)

    # Presença de energia: silêncio nunca é "a voz".
    rms = librosa.feature.rms(y=y, frame_length=N_FFT, hop_length=HOP)[0]
    energy_gate = (rms > np.percentile(rms, 20)).astype(float)

    score = (0.6 * timbre_score + 0.4 * pitch_score) * energy_gate
    # Suaviza no tempo (~8 quadros ≈ 90 ms) para a máscara não "tremer".
    score = uniform_filter1d(score, size=8)

    # Normalização relativa (percentis 5-95 do próprio arquivo): faz a
    # tolerância significar sempre "os X% de quadros mais parecidos com a
    # voz", independente da escala absoluta das distâncias — sem isso, uma
    # amostra de perfil muito limpa (desvio pequeno) derruba todos os
    # escores para perto de zero e nada passa do corte.
    lo_s, hi_s = np.percentile(score, 5), np.percentile(score, 95)
    if hi_s - lo_s > 1e-8:
        score = np.clip((score - lo_s) / (hi_s - lo_s), 0.0, 1.0)
    return score


def separate(
    input_path: str | Path,
    profile: VoiceProfile,
    output_path: str | Path,
    tolerance: float = 0.5,
    gradient: float = 0.85,
    denoise: bool = True,
) -> SeparationResult:
    """Separa a voz do perfil no áudio de entrada e grava o resultado.

    tolerance: 0..1 — corte de semelhança (alto = mais rigoroso, corta mais)
    gradient:  0..1 — profundidade da atenuação do que foi cortado
    """
    if not 0.0 <= tolerance <= 1.0 or not 0.0 <= gradient <= 1.0:
        raise ValueError("tolerance e gradient devem estar entre 0 e 1")

    y, sr = librosa.load(str(input_path), sr=profile.sample_rate, mono=True)
    score = _frame_similarity(y, sr, profile)

    # Máscara por quadro com transição suave em volta do corte (sigmoide):
    # score >> tolerance -> 1 (mantém); score << tolerance -> atenua por `gradient`.
    softness = 0.08
    frame_mask = 1.0 / (1.0 + np.exp(-(score - tolerance) / softness))
    frame_gain = 1.0 - gradient * (1.0 - frame_mask)

    stft = librosa.stft(y, n_fft=N_FFT, hop_length=HOP)
    n_frames = stft.shape[1]
    if len(frame_gain) < n_frames:
        frame_gain = np.pad(frame_gain, (0, n_frames - len(frame_gain)), constant_values=frame_gain[-1])
    frame_gain = frame_gain[:n_frames]

    # Banda útil da voz (com folga): fora dela, aplica a atenuação cheia.
    freqs = librosa.fft_frequencies(sr=sr, n_fft=N_FFT)
    lo = max(60.0, profile.pitch_p10_hz * 0.7)
    hi = min(sr / 2.0, profile.spectral_centroid_hz + 2.5 * profile.spectral_bandwidth_hz)
    band = ((freqs >= lo) & (freqs <= hi)).astype(float)
    bin_gain = band[:, None] * frame_gain[None, :] + (1.0 - band[:, None]) * (1.0 - gradient)

    y_out = librosa.istft(stft * bin_gain, hop_length=HOP, length=len(y))

    if denoise:
        # Remove o ruído estacionário residual (ex.: zumbido, ar-condicionado).
        y_out = nr.reduce_noise(y=y_out, sr=sr, prop_decrease=min(gradient, 0.9), stationary=True)

    y_out = np.clip(y_out, -1.0, 1.0)
    sf.write(str(output_path), y_out, sr)

    def dbfs(x: np.ndarray) -> float:
        return float(20 * np.log10(max(np.sqrt(np.mean(x**2)), 1e-10)))

    return SeparationResult(
        output_path=str(output_path),
        duration_s=len(y) / sr,
        frames_kept_pct=float(100.0 * np.mean(frame_mask > 0.5)),
        input_rms_dbfs=dbfs(y),
        output_rms_dbfs=dbfs(y_out),
        tolerance=tolerance,
        gradient=gradient,
    )
