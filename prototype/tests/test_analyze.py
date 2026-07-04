import json
import tempfile
import unittest
from pathlib import Path

from .helpers import default_profile, mixed_wav
from anti_ruido.analyze import analyze_timeline, save_timeline


class TestAnalyze(unittest.TestCase):
    def test_estrutura_da_timeline(self):
        data = analyze_timeline(mixed_wav(), default_profile(), tolerance=0.5, gradient=0.85)
        self.assertAlmostEqual(data["duration_s"], 3.0, delta=0.1)
        self.assertEqual(data["tolerance"], 0.5)
        self.assertEqual(data["gradient"], 0.85)
        self.assertIn("pitch_median_hz", data["profile"])
        self.assertGreater(len(data["points"]), 10)

        p = data["points"][len(data["points"]) // 2]
        for k in ("t", "db", "f0", "centroid", "score", "gain"):
            self.assertIn(k, p)
        self.assertGreaterEqual(p["score"], 0.0)
        self.assertLessEqual(p["score"], 1.0)
        self.assertGreaterEqual(p["gain"], 0.0)
        self.assertLessEqual(p["gain"], 1.0)

    def test_tempos_crescentes(self):
        data = analyze_timeline(mixed_wav(), default_profile())
        ts = [p["t"] for p in data["points"]]
        self.assertEqual(ts, sorted(ts))
        self.assertLessEqual(ts[-1], data["duration_s"] + 0.1)

    def test_save_gera_json_valido(self):
        data = analyze_timeline(mixed_wav(), default_profile())
        out = Path(tempfile.mkdtemp()) / "timeline.json"
        save_timeline(data, out)
        recarregado = json.loads(out.read_text())
        self.assertEqual(len(recarregado["points"]), len(data["points"]))


if __name__ == "__main__":
    unittest.main()
