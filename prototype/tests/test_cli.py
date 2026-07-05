import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from .helpers import ambient_wav, default_profile, mixed_wav, voice_wav
from anti_ruido.cli import main


def run_cli(*args: str) -> tuple[int, str]:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = main(list(args))
    return code, buf.getvalue()


class TestCLI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dir = Path(tempfile.mkdtemp())
        cls.perfil = cls.dir / "perfil.json"
        default_profile().save(cls.perfil)

    def test_profile(self):
        out = self.dir / "p.json"
        code, texto = run_cli("profile", voice_wav(), "-o", str(out))
        self.assertEqual(code, 0)
        self.assertIn("Perfil de voz", texto)
        self.assertTrue(out.exists())

    def test_separate(self):
        out = self.dir / "sep.wav"
        code, texto = run_cli("separate", mixed_wav(), "-p", str(self.perfil), "-o", str(out),
                              "-t", "0.5", "-g", "0.85")
        self.assertEqual(code, 0)
        self.assertTrue(out.exists())
        self.assertIn("tolerância de corte: 0.5", texto)

    def test_mix(self):
        out = self.dir / "cena.wav"
        code, texto = run_cli("mix", voice_wav(), ambient_wav(), "-o", str(out), "--snr", "3")
        self.assertEqual(code, 0)
        self.assertTrue(out.exists())
        self.assertIn("+3 dB", texto)

    def test_analyze(self):
        out = self.dir / "tl.json"
        code, texto = run_cli("analyze", mixed_wav(), "-p", str(self.perfil), "-o", str(out))
        self.assertEqual(code, 0)
        data = json.loads(out.read_text())
        self.assertIn("points", data)

    def test_comando_obrigatorio(self):
        with self.assertRaises(SystemExit):
            main([])


if __name__ == "__main__":
    unittest.main()
