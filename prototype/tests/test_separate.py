import tempfile
import unittest
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf

from .helpers import SR, default_profile, mixed_wav
from anti_ruido.separate import filter_chunk, separate


class TestSeparate(unittest.TestCase):
    def test_gera_saida_valida(self):
        out = Path(tempfile.mkdtemp()) / "saida.wav"
        res = separate(mixed_wav(), default_profile(), out)
        self.assertTrue(out.exists())
        info = sf.info(str(out))
        self.assertEqual(info.samplerate, SR)
        self.assertAlmostEqual(info.duration, 3.0, delta=0.1)
        self.assertGreaterEqual(res.frames_kept_pct, 0)
        self.assertLessEqual(res.frames_kept_pct, 100)

    def test_parametros_invalidos(self):
        out = Path(tempfile.mkdtemp()) / "x.wav"
        with self.assertRaises(ValueError):
            separate(mixed_wav(), default_profile(), out, tolerance=1.5)
        with self.assertRaises(ValueError):
            separate(mixed_wav(), default_profile(), out, gradient=-0.1)

    def test_tolerancia_monotonica(self):
        """Tolerância maior deve manter MENOS quadros como voz."""
        d = Path(tempfile.mkdtemp())
        kept = []
        for t in (0.2, 0.5, 0.8):
            res = separate(mixed_wav(), default_profile(), d / f"t{t}.wav", tolerance=t)
            kept.append(res.frames_kept_pct)
        self.assertGreaterEqual(kept[0], kept[1])
        self.assertGreaterEqual(kept[1], kept[2])

    def test_gradiente_atenua_mais(self):
        """Gradiente maior deve resultar em saída com menos energia."""
        d = Path(tempfile.mkdtemp())
        r_soft = separate(mixed_wav(), default_profile(), d / "soft.wav", gradient=0.3)
        r_hard = separate(mixed_wav(), default_profile(), d / "hard.wav", gradient=1.0)
        self.assertLess(r_hard.output_rms_dbfs, r_soft.output_rms_dbfs)

    def test_sem_clipping(self):
        out = Path(tempfile.mkdtemp()) / "clip.wav"
        separate(mixed_wav(), default_profile(), out, gradient=0.2)
        y, _ = sf.read(str(out))
        self.assertLessEqual(float(np.max(np.abs(y))), 1.0)


class TestFilterChunk(unittest.TestCase):
    def _chunk(self, seconds=1.0):
        y, _ = librosa.load(mixed_wav(), sr=SR, mono=True, duration=seconds)
        return y

    def test_saida_mesmo_tamanho_e_metricas(self):
        y = self._chunk()
        out, met = filter_chunk(y, SR, default_profile())
        self.assertEqual(len(out), len(y))
        for k in ("score", "gain", "db", "kept_pct"):
            self.assertIn(k, met)
        self.assertGreaterEqual(met["score"], 0.0)
        self.assertLessEqual(met["score"], 1.0)

    def test_entrada_minuscula_passa_direto(self):
        y = np.zeros(100, dtype=np.float32)
        out, met = filter_chunk(y, SR, default_profile())
        self.assertEqual(len(out), 100)
        self.assertIn("gain", met)

    def test_gradiente_controla_atenuacao(self):
        y = self._chunk()
        out_soft, _ = filter_chunk(y, SR, default_profile(), gradient=0.3)
        out_hard, _ = filter_chunk(y, SR, default_profile(), gradient=1.0)
        self.assertLess(float(np.sqrt(np.mean(out_hard**2))),
                        float(np.sqrt(np.mean(out_soft**2))))

    def test_rapido_o_bastante_para_tempo_real(self):
        """1s de áudio precisa processar em bem menos de 1s (folga: 0,8s)."""
        import time

        y = self._chunk()
        filter_chunk(y, SR, default_profile())  # aquecimento (caches numba/librosa)
        t0 = time.monotonic()
        filter_chunk(y, SR, default_profile())
        self.assertLess(time.monotonic() - t0, 0.8)


if __name__ == "__main__":
    unittest.main()
