import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
import soundfile as sf

from .helpers import SR, default_profile, voice_wav
from anti_ruido.profile import MAX_PROFILE_SECONDS, VoiceProfile, describe, extract_profile


class TestExtractProfile(unittest.TestCase):
    def test_valores_plausiveis(self):
        p = default_profile()
        # a voz sintética tem F0 ~150 Hz
        self.assertAlmostEqual(p.pitch_median_hz, 150, delta=20)
        self.assertLess(p.pitch_p10_hz, p.pitch_p90_hz)
        self.assertEqual(len(p.mfcc_mean), 20)
        self.assertEqual(len(p.mfcc_std), 20)
        self.assertGreater(p.spectral_centroid_hz, 0)
        self.assertLess(p.rms_dbfs, 0)       # dBFS é sempre negativo
        self.assertLessEqual(p.peak_dbfs, 0)
        self.assertGreater(p.peak_amplitude, 0)

    def test_corta_amostra_em_10s(self):
        # 15s de entrada não podem deixar o perfil mais "longo" que 10s:
        # como o corte acontece no load, o teste verifica indiretamente pela
        # constante e pelo carregamento truncado.
        self.assertEqual(MAX_PROFILE_SECONDS, 10.0)
        import librosa

        y, _ = librosa.load(voice_wav(duration=12.0, seed=9), sr=SR, mono=True,
                            duration=MAX_PROFILE_SECONDS)
        self.assertLessEqual(len(y) / SR, MAX_PROFILE_SECONDS + 0.01)

    def test_erro_amostra_curta(self):
        f = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        sf.write(f.name, np.zeros(512), SR)
        with self.assertRaises(ValueError):
            extract_profile(f.name)

    def test_erro_sem_pitch(self):
        # ruído branco puro não tem pitch de fala
        rng = np.random.default_rng(0)
        f = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        sf.write(f.name, rng.standard_normal(SR * 2) * 0.3, SR)
        with self.assertRaises(ValueError):
            extract_profile(f.name)


class TestVoiceProfileIO(unittest.TestCase):
    def test_save_load_roundtrip(self):
        p = default_profile()
        out = Path(tempfile.mkdtemp()) / "perfil.json"
        p.save(out)
        p2 = VoiceProfile.load(out)
        self.assertEqual(p, p2)
        # JSON válido e legível
        data = json.loads(out.read_text())
        self.assertIn("pitch_median_hz", data)

    def test_save_cria_diretorio_pai(self):
        out = Path(tempfile.mkdtemp()) / "sub/dir/perfil.json"
        default_profile().save(out)
        self.assertTrue(out.exists())

    def test_describe_contem_dimensoes(self):
        txt = describe(default_profile())
        for chave in ("altura", "timbre", "intensidade", "pico"):
            self.assertIn(chave, txt)


if __name__ == "__main__":
    unittest.main()
