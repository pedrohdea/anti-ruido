"""Fixtures compartilhadas: áudio sintético curto (rápido de processar)."""

from __future__ import annotations

import sys
import tempfile
from functools import lru_cache
from pathlib import Path

import numpy as np
import soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from anti_ruido.demo import SR, _synth_ambient, _synth_voice  # noqa: E402


@lru_cache(maxsize=None)
def voice_wav(duration: float = 3.0, f0: float = 150.0, seed: int = 1) -> str:
    """WAV temporário com 'voz' sintética; cacheado por parâmetros."""
    y = _synth_voice(duration, f0_base=f0, seed=seed) * 0.8
    f = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(f.name, y, SR)
    return f.name


@lru_cache(maxsize=None)
def ambient_wav(duration: float = 3.0, seed: int = 3) -> str:
    y = _synth_ambient(duration, seed=seed) * 0.6
    f = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(f.name, y, SR)
    return f.name


@lru_cache(maxsize=None)
def mixed_wav(duration: float = 3.0) -> str:
    v = _synth_voice(duration, f0_base=150.0, seed=2) * 0.7
    a = _synth_ambient(duration, seed=3) * 0.5
    m = v + a
    m = m / (np.max(np.abs(m)) + 1e-9)
    f = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(f.name, m, SR)
    return f.name


@lru_cache(maxsize=None)
def default_profile():
    from anti_ruido.profile import extract_profile

    return extract_profile(voice_wav())
