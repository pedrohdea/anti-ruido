"""Demo de ponta a ponta sem microfone: sintetiza uma "voz" (fonte harmônica
com contorno de pitch e envelope de sílabas), mistura com ruído de ambiente
(babble + zumbido + ruído largo), e roda o pipeline perfil -> separação.

Serve para (1) testar o pipeline em qualquer máquina/CI e (2) demonstrar o
efeito dos controles de tolerância e gradiente com métricas objetivas (SNR).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import soundfile as sf

from .profile import describe, extract_profile
from .separate import separate

SR = 22050


def _synth_voice(duration: float, f0_base: float, seed: int) -> np.ndarray:
    """Fonte glotal simplificada: harmônicos com vibrato + envelope de sílabas."""
    rng = np.random.default_rng(seed)
    t = np.arange(int(duration * SR)) / SR
    # contorno de pitch: base + deriva lenta + vibrato
    f0 = f0_base * (1 + 0.06 * np.sin(2 * np.pi * 0.35 * t) + 0.02 * np.sin(2 * np.pi * 5.5 * t))
    phase = 2 * np.pi * np.cumsum(f0) / SR
    y = np.zeros_like(t)
    for h, gain in enumerate([1.0, 0.62, 0.42, 0.28, 0.18, 0.11, 0.06], start=1):
        y += gain * np.sin(h * phase)
    # "formantes" fixos dão identidade de timbre à voz sintética
    for fc, g in [(500, 0.35), (1500, 0.22), (2500, 0.12)]:
        y += g * np.sin(2 * np.pi * fc * t + 0.7 * np.sin(phase))
    # envelope de sílabas (~4/s) com pausas
    syllables = 0.5 * (1 + np.sign(np.sin(2 * np.pi * 3.8 * t + rng.uniform(0, 6.28))))
    pauses = (np.sin(2 * np.pi * 0.22 * t + rng.uniform(0, 6.28)) > -0.55).astype(float)
    env = np.convolve(syllables * pauses, np.ones(1024) / 1024, mode="same")
    y *= env
    return y / (np.max(np.abs(y)) + 1e-9)


def _synth_ambient(duration: float, seed: int) -> np.ndarray:
    """Ruído de bar: burburinho (ruído filtrado modulado), zumbido 60 Hz e chiado."""
    rng = np.random.default_rng(seed)
    n = int(duration * SR)
    t = np.arange(n) / SR
    white = rng.standard_normal(n)
    # burburinho: passa-banda grosseiro via diferenças acumuladas + modulação lenta
    babble = np.convolve(white, np.ones(64) / 64, mode="same")
    babble *= 0.6 * (1 + 0.5 * np.sin(2 * np.pi * 0.9 * t + 1.3))
    hum = 0.25 * np.sin(2 * np.pi * 60 * t) + 0.12 * np.sin(2 * np.pi * 120 * t)
    hiss = 0.18 * white
    amb = babble + hum + hiss
    return amb / (np.max(np.abs(amb)) + 1e-9)


def _snr_db(signal: np.ndarray, noise: np.ndarray) -> float:
    ps = float(np.mean(signal**2))
    pn = float(np.mean(noise**2)) + 1e-12
    return 10 * np.log10(ps / pn)


def run_demo(workdir: Path, tolerance: float = 0.5, gradient: float = 0.85) -> int:
    workdir.mkdir(parents=True, exist_ok=True)

    # 1) amostra limpa da "pessoa" (para o perfil) — voz A, pitch ~150 Hz
    voice_sample = _synth_voice(6.0, f0_base=150.0, seed=1)
    sample_path = workdir / "amostra-voz.wav"
    sf.write(sample_path, voice_sample * 0.8, SR)

    # 2) cena ruidosa: a mesma voz A falando + ambiente de bar por cima
    voice_scene = _synth_voice(8.0, f0_base=150.0, seed=2) * 0.7
    ambient = _synth_ambient(8.0, seed=3) * 0.55
    mix = voice_scene + ambient
    mix = mix / (np.max(np.abs(mix)) + 1e-9)
    mix_path = workdir / "cena-ruidosa.wav"
    sf.write(mix_path, mix, SR)

    # 3) perfil
    prof = extract_profile(sample_path)
    prof_path = workdir / "perfil.json"
    prof.save(prof_path)
    print(describe(prof))

    # 4) separação
    out_path = workdir / "cena-separada.wav"
    res = separate(mix_path, prof, out_path, tolerance=tolerance, gradient=gradient)

    # 5) métrica objetiva: SNR aproximado antes/depois.
    #    Reprocessa voz e ruído isolados com a MESMA máscara não é trivial aqui;
    #    usamos a aproximação padrão de demo: energia na banda da voz vs fora dela.
    snr_before = _snr_db(voice_scene, ambient)
    y_out, _ = sf.read(out_path)
    resid = y_out[: len(ambient)] - voice_scene[: len(y_out)] * (np.std(y_out) / (np.std(voice_scene) + 1e-9))
    snr_after = _snr_db(voice_scene[: len(y_out)], resid)

    print(f"\nArquivos em {workdir}/:")
    print(f"  amostra-voz.wav    (entrada do perfil)")
    print(f"  cena-ruidosa.wav   (voz + bar simulado)  SNR ~{snr_before:.1f} dB")
    print(f"  cena-separada.wav  (resultado)           SNR ~{snr_after:.1f} dB")
    print(f"  quadros mantidos como voz: {res.frames_kept_pct:.0f}% | tolerância {tolerance} | gradiente {gradient}")
    if snr_after <= snr_before:
        print("\nAVISO: o SNR não melhorou — ajuste tolerance/gradient ou revise o pipeline.")
        return 1
    print("\nDemo OK — o SNR melhorou com a separação.")
    return 0
