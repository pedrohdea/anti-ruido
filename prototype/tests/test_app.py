"""Testes do servidor do app local (Flask test client — sem rede/microfone)."""

import importlib.util
import io
import json
import sys
import unittest
from pathlib import Path

import numpy as np
import soundfile as sf

from .helpers import SR, mixed_wav, voice_wav

APP_PATH = Path(__file__).resolve().parents[1] / "app" / "server.py"


def _load_server():
    spec = importlib.util.spec_from_file_location("anti_ruido_app_server", APP_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)  # roda _ensure_default_profile()
    return mod


class TestAppServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = _load_server()
        cls.client = cls.server.app.test_client()

    def _wav_bytes(self, path: str) -> bytes:
        y, sr = sf.read(path)
        buf = io.BytesIO()
        sf.write(buf, y, sr, format="WAV")
        return buf.getvalue()

    def test_pagina_principal(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"anti-", r.data)

    def test_perfil_padrao_existe(self):
        r = self.client.get("/api/profile")
        self.assertEqual(r.status_code, 200)
        j = r.get_json()
        self.assertIn("Perfil de voz", j["descricao"])
        self.assertEqual(j["max_seconds"], 10.0)

    def test_gravar_perfil_e_persistir_mp3(self):
        r = self.client.post("/api/profile", data=self._wav_bytes(voice_wav(seed=5)))
        self.assertEqual(r.status_code, 200)
        self.assertIn("Perfil de voz", r.get_json()["descricao"])
        self.assertTrue(self.server.SAMPLE_MP3.exists())          # amostra em MP3
        self.assertTrue(str(self.server.SAMPLE_MP3).endswith(".mp3"))

    def test_perfil_sem_audio_retorna_400(self):
        r = self.client.post("/api/profile", data=b"")
        self.assertEqual(r.status_code, 400)

    def test_perfil_audio_invalido(self):
        r = self.client.post("/api/profile", data=b"nao sou audio")
        self.assertIn(r.status_code, (422, 500))

    def test_reset_para_voz_padrao(self):
        r = self.client.post("/api/profile/default")
        self.assertEqual(r.status_code, 200)

    def test_filter_com_termometro(self):
        r = self.client.post("/api/filter?thermo=128", data=self._wav_bytes(mixed_wav()))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.mimetype, "audio/wav")
        met = json.loads(r.headers["X-Metrics"])
        for k in ("score", "gain", "db", "kept_pct", "tolerance", "gradient"):
            self.assertIn(k, met)
        y, sr = sf.read(io.BytesIO(r.data))
        self.assertEqual(sr, SR)
        self.assertGreater(len(y), 0)

    def test_filter_ajuste_fino_sobrepoe_termometro(self):
        r = self.client.post("/api/filter?thermo=128&tolerance=0.9&gradient=1.0",
                             data=self._wav_bytes(mixed_wav()))
        met = json.loads(r.headers["X-Metrics"])
        self.assertEqual(met["tolerance"], 0.9)
        self.assertEqual(met["gradient"], 1.0)

    def test_termometro_monotonico(self):
        """Termômetro maior -> ganho médio menor (filtro mais forte)."""
        data = self._wav_bytes(mixed_wav())
        gains = []
        for th in (1, 128, 256):
            r = self.client.post(f"/api/filter?thermo={th}", data=data)
            gains.append(json.loads(r.headers["X-Metrics"])["gain"])
        self.assertGreater(gains[0], gains[1])
        self.assertGreater(gains[1], gains[2])

    def test_thermo_to_params_limites(self):
        f = self.server._thermo_to_params
        t1, g1 = f(1)
        t256, g256 = f(256)
        self.assertAlmostEqual(t1, 0.15, places=2)
        self.assertAlmostEqual(g1, 0.40, places=2)
        self.assertAlmostEqual(t256, 0.85, places=2)
        self.assertAlmostEqual(g256, 1.00, places=2)
        # fora da faixa é grampeado, nunca explode
        self.assertEqual(f(-10), f(1))
        self.assertEqual(f(9999), f(256))


if __name__ == "__main__":
    unittest.main()
