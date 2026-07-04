import tempfile
import unittest
from pathlib import Path

from anti_ruido.demo import run_demo


class TestDemo(unittest.TestCase):
    def test_demo_completa_melhora_snr(self):
        """A demo é o teste de regressão de ponta a ponta: retorna 0 apenas
        quando o SNR da cena melhora após a separação."""
        workdir = Path(tempfile.mkdtemp())
        self.assertEqual(run_demo(workdir), 0)
        for nome in ("amostra-voz.wav", "cena-ruidosa.wav", "cena-separada.wav", "perfil.json"):
            self.assertTrue((workdir / nome).exists(), nome)


if __name__ == "__main__":
    unittest.main()
