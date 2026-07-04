"""Gera o visualizador HTML autocontido (áudio + timeline embutidos).

Uso:
  python viewer/build_viewer.py --before mescla.mp3 --after filtrada.mp3 \
      --timeline timeline.json -o visualizador.html
"""

from __future__ import annotations

import argparse
import base64
from pathlib import Path

TEMPLATE = Path(__file__).parent / "template.html"


def build(before_mp3: Path, after_mp3: Path, timeline_json: Path, out: Path) -> None:
    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("__TIMELINE__", timeline_json.read_text(encoding="utf-8"))
    html = html.replace("__AUDIO_BEFORE__", base64.b64encode(before_mp3.read_bytes()).decode())
    html = html.replace("__AUDIO_AFTER__", base64.b64encode(after_mp3.read_bytes()).decode())
    out.write_text(html, encoding="utf-8")
    print(f"OK: {out} ({out.stat().st_size/1e6:.1f} MB)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", required=True, type=Path)
    ap.add_argument("--after", required=True, type=Path)
    ap.add_argument("--timeline", required=True, type=Path)
    ap.add_argument("-o", "--output", default=Path("visualizador.html"), type=Path)
    a = ap.parse_args()
    build(a.before, a.after, a.timeline, a.output)
