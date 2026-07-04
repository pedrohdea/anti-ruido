"""CLI do protótipo Anti-Ruído.

Comandos:
  profile   grava/analisa a amostra de voz e salva o perfil JSON
  separate  processa um WAV separando a voz do perfil (gradiente/tolerância)
  live      captura do microfone e processa em blocos (requer sounddevice)
  demo      gera um áudio sintético (voz + ruído), roda o pipeline e mostra métricas
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .profile import VoiceProfile, describe, extract_profile
from .separate import separate


def _cmd_profile(args: argparse.Namespace) -> int:
    prof = extract_profile(args.input)
    prof.save(args.output)
    print(describe(prof))
    print(f"\nPerfil salvo em {args.output}")
    return 0


def _cmd_separate(args: argparse.Namespace) -> int:
    prof = VoiceProfile.load(args.profile)
    res = separate(
        args.input,
        prof,
        args.output,
        tolerance=args.tolerance,
        gradient=args.gradient,
        denoise=not args.no_denoise,
    )
    print(f"OK: {res.output_path}")
    print(f"  duração: {res.duration_s:.1f}s | quadros mantidos como voz: {res.frames_kept_pct:.0f}%")
    print(f"  nível RMS: {res.input_rms_dbfs:.1f} dBFS -> {res.output_rms_dbfs:.1f} dBFS")
    print(f"  tolerância de corte: {res.tolerance} | gradiente de atenuação: {res.gradient}")
    return 0


def _cmd_live(args: argparse.Namespace) -> int:
    try:
        import sounddevice as sd  # import tardio: só o modo live precisa
    except OSError as e:  # PortAudio ausente
        print(f"Modo live indisponível: {e}\nInstale PortAudio (libportaudio2) ou rode via Docker com --device /dev/snd.", file=sys.stderr)
        return 2

    import numpy as np

    prof = VoiceProfile.load(args.profile)
    sr = prof.sample_rate
    block = int(sr * args.block_seconds)
    print(f"Capturando do microfone a {sr} Hz em blocos de {args.block_seconds}s — Ctrl+C para parar.")
    chunks: list[np.ndarray] = []
    try:
        with sd.InputStream(samplerate=sr, channels=1, dtype="float32") as stream:
            while True:
                audio, _ = stream.read(block)
                chunks.append(audio[:, 0].copy())
    except KeyboardInterrupt:
        pass

    if not chunks:
        print("Nada gravado.")
        return 1

    import soundfile as sf

    raw = np.concatenate(chunks)
    raw_path = Path(args.output).with_suffix(".raw.wav")
    sf.write(raw_path, raw, sr)
    res = separate(raw_path, prof, args.output, tolerance=args.tolerance, gradient=args.gradient)
    print(f"Bruto: {raw_path}\nSeparado: {res.output_path}")
    return 0


def _cmd_demo(args: argparse.Namespace) -> int:
    from .demo import run_demo

    return run_demo(Path(args.workdir), tolerance=args.tolerance, gradient=args.gradient)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="anti-ruido", description="Protótipo de separação de fala com perfil de voz.")
    p.add_argument("--version", action="version", version=f"anti-ruido {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    sp = sub.add_parser("profile", help="extrai o perfil de voz de uma amostra")
    sp.add_argument("input", help="WAV com ~5-15s da pessoa falando")
    sp.add_argument("-o", "--output", default="perfil.json")
    sp.set_defaults(fn=_cmd_profile)

    ss = sub.add_parser("separate", help="separa a voz do perfil num áudio")
    ss.add_argument("input", help="WAV de entrada (ambiente ruidoso)")
    ss.add_argument("-p", "--profile", required=True, help="perfil JSON gerado pelo comando profile")
    ss.add_argument("-o", "--output", default="saida.wav")
    ss.add_argument("-t", "--tolerance", type=float, default=0.5, help="corte de semelhança 0..1 (padrão 0.5)")
    ss.add_argument("-g", "--gradient", type=float, default=0.85, help="profundidade de atenuação 0..1 (padrão 0.85)")
    ss.add_argument("--no-denoise", action="store_true", help="desliga a redução de ruído estacionário final")
    ss.set_defaults(fn=_cmd_separate)

    sl = sub.add_parser("live", help="captura do microfone e processa")
    sl.add_argument("-p", "--profile", required=True)
    sl.add_argument("-o", "--output", default="saida-live.wav")
    sl.add_argument("-t", "--tolerance", type=float, default=0.5)
    sl.add_argument("-g", "--gradient", type=float, default=0.85)
    sl.add_argument("--block-seconds", type=float, default=1.0)
    sl.set_defaults(fn=_cmd_live)

    sd_ = sub.add_parser("demo", help="gera áudio sintético e roda o pipeline completo")
    sd_.add_argument("--workdir", default="demo-out")
    sd_.add_argument("-t", "--tolerance", type=float, default=0.5)
    sd_.add_argument("-g", "--gradient", type=float, default=0.85)
    sd_.set_defaults(fn=_cmd_demo)

    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
