import tempfile
import unittest
from pathlib import Path

import numpy as np
import soundfile as sf

from .helpers import SR, ambient_wav, voice_wav
from anti_ruido.mixer import mix_files


class TestMixer(unittest.TestCase):
    def _mix(self, snr, voice_dur=3.0, bg_dur=3.0):
        out = Path(tempfile.mkdtemp()) / "cena.wav"
        info = mix_files(voice_wav(duration=voice_dur), ambient_wav(duration=bg_dur), out, snr_db=snr)
        y, sr = sf.read(str(out))
        return out, info, y, sr

    def test_snr_solicitado_e_atingido(self):
        """A energia relativa voz/fundo na mescla deve refletir o SNR pedido.

        O guard anti-clipping pode reescalar a mescla inteira; por isso o
        fator de escala da voz é estimado por projeção (alpha), em vez de
        assumir escala 1.
        """
        import librosa

        v, _ = librosa.load(voice_wav(), sr=SR, mono=True)
        for snr in (-5.0, 0.0, 5.0):
            out, info, y, sr = self._mix(snr)
            n = min(len(v), len(y))
            alpha = float(np.dot(y[:n], v[:n]) / (np.dot(v[:n], v[:n]) + 1e-12))
            bg = y[:n] - alpha * v[:n]
            p_v = np.mean((alpha * v[:n]) ** 2)
            p_b = np.mean(bg**2) + 1e-12
            snr_medido = 10 * np.log10(p_v / p_b)
            self.assertAlmostEqual(snr_medido, snr, delta=1.0)

    def test_fundo_curto_e_repetido_em_loop(self):
        out, info, y, sr = self._mix(0.0, voice_dur=4.0, bg_dur=1.0)
        self.assertAlmostEqual(info["duration_s"], 4.0, delta=0.1)
        self.assertAlmostEqual(len(y) / sr, 4.0, delta=0.1)

    def test_fundo_longo_e_cortado(self):
        out, info, y, sr = self._mix(0.0, voice_dur=2.0, bg_dur=5.0)
        self.assertAlmostEqual(len(y) / sr, 2.0, delta=0.1)

    def test_sem_clipping(self):
        out, info, y, sr = self._mix(-10.0)  # fundo bem mais alto força o guard
        self.assertLessEqual(float(np.max(np.abs(y))), 0.99)


if __name__ == "__main__":
    unittest.main()
