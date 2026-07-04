"""CLI do protótipo Anti-Ruído.

Comandos:
  profile   grava/analisa a amostra de voz e salva o perfil JSON
  separate  processa um WAV separando a voz do perfil (gradiente/tolerância)
  live      captura do microfone e processa em blocos (requer sounddevice)
  demo      gera um áudio sintético (voz + ruído), roda o pipeline e mostra métricas
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from . import __version__
from .profile import VoiceProfile, describe, extract_profile
from .separate import separate

logger = logging.getLogger(__name__)


def _cmd_profile(args: argparse.Namespace) -> int:
    logger.info("Running profile command input=%s output=%s", args.input, args.output)
    logger.debug("profile command args=%s", vars(args))
    prof = extract_profile(args.input)
    prof.save(args.output)
    print(describe(prof))
    print(f"\nPerfil salvo em {args.output}")
    return 0


def _cmd_separate(args: argparse.Namespace) -> int:
    logger.info("Running separate command input=%s profile=%s output=%s tolerance=%s gradient=%s denoise=%s",
                args.input, args.profile, args.output, args.tolerance, args.gradient, args.denoise)
    prof = VoiceProfile.load(args.profile)
    res = separate(
        args.input,
        prof,
        args.output,
        tolerance=args.tolerance,
        gradient=args.gradient,
        denoise=args.denoise,
    )
    print(f"OK: {res.output_path}")
    print(f"  duração: {res.duration_s:.1f}s | quadros mantidos como voz: {res.frames_kept_pct:.0f}%")
    print(f"  nível RMS: {res.input_rms_dbfs:.1f} dBFS -> {res.output_rms_dbfs:.1f} dBFS")
    print(f"  tolerância de corte: {res.tolerance} | gradiente de atenuação: {res.gradient}")
    return 0


def _cmd_live(args: argparse.Namespace) -> int:
    logger.info("Running live command profile=%s output=%s block_seconds=%s tolerance=%s gradient=%s",
                args.profile, args.output, args.block_seconds, args.tolerance, args.gradient)
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


def _cmd_mix(args: argparse.Namespace) -> int:
    logger.info("Running mix command voice=%s background=%s output=%s snr=%s", args.voice, args.background, args.output, args.snr)
    from .mixer import mix_files

    info = mix_files(args.voice, args.background, args.output, snr_db=args.snr)
    print(f"OK: {info['output']} ({info['duration_s']}s, voz {info['snr_db']:+.0f} dB sobre o fundo)")
    return 0


def _cmd_analyze(args: argparse.Namespace) -> int:
    from .analyze import analyze_timeline, save_timeline

    prof = VoiceProfile.load(args.profile)
    data = analyze_timeline(args.input, prof, tolerance=args.tolerance, gradient=args.gradient)
    save_timeline(data, args.output)
    print(f"OK: {args.output} ({len(data['points'])} pontos, {data['duration_s']}s)")
    return 0


def _cmd_demo(args: argparse.Namespace) -> int:
    logger.info("Running demo command workdir=%s tolerance=%s gradient=%s", args.workdir, args.tolerance, args.gradient)
    from .demo import run_demo

    return run_demo(Path(args.workdir), tolerance=args.tolerance, gradient=args.gradient)


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
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
    ss.add_argument("--denoise", action="store_true", help="redução extra de ruído ESTACIONÁRIO (zumbido/ar-condicionado); piora contra burburinho")
    ss.set_defaults(fn=_cmd_separate)

    sl = sub.add_parser("live", help="captura do microfone e processa")
    sl.add_argument("-p", "--profile", required=True)
    sl.add_argument("-o", "--output", default="saida-live.wav")
    sl.add_argument("-t", "--tolerance", type=float, default=0.5)
    sl.add_argument("-g", "--gradient", type=float, default=0.85)
    sl.add_argument("--block-seconds", type=float, default=1.0)
    sl.set_defaults(fn=_cmd_live)

    sa = sub.add_parser("analyze", help="exporta linha do tempo de características (JSON p/ visualizador)")
    sa.add_argument("input", help="WAV/MP3 a analisar")
    sa.add_argument("-p", "--profile", required=True)
    sa.add_argument("-o", "--output", default="timeline.json")
    sa.add_argument("-t", "--tolerance", type=float, default=0.5)
    sa.add_argument("-g", "--gradient", type=float, default=0.85)
    sa.set_defaults(fn=_cmd_analyze)

    sm = sub.add_parser("mix", help="mescla voz + fundo num WAV de teste com SNR controlado")
    sm.add_argument("voice", help="WAV com a fala a preservar")
    sm.add_argument("background", help="WAV com o ruído de fundo (multidão, bar...)")
    sm.add_argument("-o", "--output", default="cena.wav")
    sm.add_argument("--snr", type=float, default=0.0, help="dB da voz acima do fundo (padrão 0 = mesma energia)")
    sm.set_defaults(fn=_cmd_mix)

    sd_ = sub.add_parser("demo", help="gera áudio sintético e roda o pipeline completo")
    sd_.add_argument("--workdir", default="demo-out")
    sd_.add_argument("-t", "--tolerance", type=float, default=0.5)
    sd_.add_argument("-g", "--gradient", type=float, default=0.85)
    sd_.set_defaults(fn=_cmd_demo)

    args = p.parse_args(argv)
    logger.info("CLI started with argv=%s", argv if argv is not None else sys.argv[1:])
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
