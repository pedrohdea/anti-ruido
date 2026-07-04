"""Mescla dois áudios (voz + fundo) num arquivo só, com SNR controlado.

Serve para montar cenas de teste realistas: pegue qualquer gravação de fala
e qualquer ruído de fundo (multidão, bar, rua) e produza o WAV "cena ruidosa"
que o comando `separate` vai tentar limpar.
"""

from __future__ import annotations

from pathlib import Path

import librosa
import numpy as np
import soundfile as sf


def mix_files(
    voice_path: str | Path,
    background_path: str | Path,
    output_path: str | Path,
    snr_db: float = 0.0,
    sr: int = 22050,
) -> dict:
    """Mistura voz + fundo no SNR pedido (dB de voz acima do fundo).

    snr_db = 0  -> voz e fundo com a mesma energia (bar bem barulhento)
    snr_db = 5  -> voz 5 dB acima do fundo (restaurante cheio)
    snr_db = -5 -> fundo mais alto que a voz (show/balada)
    """
    voice, _ = librosa.load(str(voice_path), sr=sr, mono=True)
    bg, _ = librosa.load(str(background_path), sr=sr, mono=True)

    # Fundo cobre a voz inteira: repete (loop) se for curto, corta se for longo.
    if len(bg) < len(voice):
        bg = np.tile(bg, int(np.ceil(len(voice) / len(bg))))
    bg = bg[: len(voice)]

    p_voice = float(np.mean(voice**2)) + 1e-12
    p_bg = float(np.mean(bg**2)) + 1e-12
    # ganho do fundo para atingir o SNR desejado
    target_p_bg = p_voice / (10 ** (snr_db / 10))
    bg = bg * np.sqrt(target_p_bg / p_bg)

    mix = voice + bg
    peak = float(np.max(np.abs(mix)))
    if peak > 0.99:  # evita clipping mantendo a proporção
        mix, voice, bg = mix / peak * 0.98, voice / peak * 0.98, bg / peak * 0.98

    sf.write(str(output_path), mix, sr)
    return {
        "output": str(output_path),
        "duration_s": round(len(mix) / sr, 1),
        "snr_db": snr_db,
        "sample_rate": sr,
    }
