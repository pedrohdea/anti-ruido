# Protótipo Anti-Ruído — separação de fala com perfil de voz

## App local (site offline) — ligar com `make`

```bash
cd prototype
make          # cria o venv, instala dependências e sobe o app
# abra http://localhost:8686 no navegador (permita o microfone)
```

Uma página, três passos:
1. **Gravar amostra de perfil (10s)** — grava do microfone e aprende a voz-alvo. A amostra é **sempre cortada em 10s no máximo**. Sem gravação, o app já inicia com a **voz padrão da demo**.
2. **Termômetro da voz (1-256)** — força do filtro, ajustável **durante** o modo ao vivo; em "Ajustes finos" dá para controlar tolerância e gradiente separadamente (múltiplos ajustes manuais).
3. **Ao vivo** — o microfone é filtrado com base no perfil e devolvido na saída de áudio (fones). Processamento em blocos de ~1s (medido: ~0,1s de CPU por bloco; latência total percebida ~1-2s). **Use fones de ouvido** para não realimentar o microfone.

Todos os áudios persistidos pelo app são salvos em **MP3** (`app/data/amostra-perfil.mp3`).

### Dependências

| Tipo | O quê |
|---|---|
| Sistema | `python3` (3.10+), `python3-venv`, `ffmpeg` — Ubuntu/Debian: `sudo apt install python3 python3-venv ffmpeg` · macOS: `brew install python ffmpeg` |
| Python (o `make` instala no venv) | `numpy`, `scipy`, `librosa`, `soundfile`, `noisereduce` (requirements.txt) + `flask` (servidor do app) |
| Opcional | `sounddevice` + `libportaudio2` (modo live do CLI, fora do app) · Docker (rodar o CLI em container) |
| Navegador | qualquer um moderno com microfone (MediaRecorder + Web Audio) |

---

Captura som (microfone ou arquivo WAV), aprende o **perfil da voz de uma pessoa**
(timbre, altura/pitch, intensidade, amplitude, decibéis) e **separa essa voz**
dos sons de ambiente/ruídos externos, com dois ajustes:

- **`--tolerance` (tolerância de corte, 0..1):** quão parecido com o perfil um
  trecho precisa ser para contar como "a voz". Baixo = permissivo (passa mais
  som); alto = rigoroso (corta mais).
- **`--gradient` (gradiente de atenuação, 0..1):** quão fundo atenuar o que foi
  cortado. `1.0` silencia; `0.5` reduz pela metade (soa mais natural).

## Ligar com um comando (Docker)

```bash
cd prototype
docker compose run --rm anti-ruido       # roda a demo completa (não precisa de microfone)
```

A demo sintetiza uma "voz" + ruído de bar, extrai o perfil, separa e imprime as
métricas (SNR antes/depois). Os arquivos ficam em `prototype/data/demo-out/`.

Com áudio real (coloque os WAVs em `prototype/data/`):

```bash
# 1. Perfil da pessoa (5-15s dela falando, o mais limpo possível)
docker compose run --rm anti-ruido profile /data/minha-voz.wav -o /data/perfil.json

# 2. Separar a voz num áudio ruidoso, com os ajustes
docker compose run --rm anti-ruido separate /data/bar.wav -p /data/perfil.json \
    -o /data/limpo.wav --tolerance 0.5 --gradient 0.85

# 3. Ao vivo, do microfone (Linux; o docker-compose já mapeia /dev/snd)
docker compose run --rm anti-ruido live -p /data/perfil.json -o /data/live.wav

# Extra: montar uma cena de teste mesclando fala + fundo com SNR controlado
docker compose run --rm anti-ruido mix /data/voz.wav /data/multidao.wav -o /data/cena.wav --snr 0
```

Para testar com áudio do YouTube (na sua máquina, fora do container):

```bash
pip install yt-dlp   # requer ffmpeg instalado
yt-dlp -x --audio-format wav --download-sections "*0-60" -o "data/multidao.%(ext)s" "URL_DO_VIDEO_DE_MULTIDAO"
yt-dlp -x --audio-format wav --download-sections "*1736-1796" -o "data/fala.%(ext)s" "URL_DO_VIDEO_DE_FALA"
docker compose run --rm anti-ruido mix /data/fala.wav /data/multidao.wav -o /data/cena.wav --snr 0
```

Sem Docker: `pip install -r requirements.txt && python -m anti_ruido.cli demo`.

## O que o perfil de voz captura

| Dimensão | Como é medida |
|---|---|
| Altura (pitch) | F0 mediano + faixa típica (percentis 10-90), via pYIN |
| Timbre | 20 MFCCs (média/desvio) + centroide e largura espectral |
| Intensidade | RMS médio em dBFS |
| Amplitude / decibéis | Pico absoluto e pico em dBFS |

## Como a separação funciona

1. STFT do áudio; para cada quadro (~12 ms), um escore de semelhança com o
   perfil (60% timbre, 40% pitch, com porta de energia — silêncio nunca é voz).
2. Máscara por quadro: abaixo da **tolerância**, o quadro é atenuado pela
   profundidade do **gradiente** (transição sigmoide, sem cliques).
3. Subtração de Wiener: o espectro do ruído é estimado dos 30% de quadros
   menos parecidos com a voz e subtraído da cena inteira.
4. `--denoise` (opcional): redução extra de ruído **estacionário** — ajuda
   com zumbido/ar-condicionado; **piora contra burburinho** (medido, abaixo).

## Resultados medidos com áudio real

Cena de teste: fala real (LibriSpeech via MS-SNSD, `clean_test/clnsp1.wav`)
mesclada com **burburinho real de multidão** (`noise_train/Babble_1.wav` do
[microsoft/MS-SNSD](https://github.com/microsoft/MS-SNSD)) no mesmo volume
(SNR 0 dB — "bar bem barulhento"). Perfil extraído de outro trecho da mesma
pessoa. Métrica: SI-SDR (padrão da área) contra a voz limpa de referência.

| Variante | SI-SDR | vs. cena |
|---|---|---|
| Cena com multidão (entrada) | −0,05 dB | — |
| Máscara de quadro + banda (v0.1 inicial) | −0,25 dB | ~0 |
| Pente harmônico no pitch-alvo | −1,77 dB | **piorou** (estimar o pitch-alvo dentro da mistura é o próprio problema difícil) |
| **Máscara de quadro + Wiener (atual)** | **+1,34 dB** | **+1,4 dB** |
| Atual + denoise estacionário | −1,66 dB | piorou (por isso `--denoise` é opt-in) |

**Leitura honesta:** +1,4 dB contra burburinho é ganho real mas modesto —
burburinho *é fala*, o pior caso da categoria. É exatamente por isso que o
roadmap v0.2/v0.3 troca o escore DSP por embedding/máscara neurais. Contra
ruído estacionário (demo sintética: voz + zumbido + chiado), o pipeline
melhora o SNR em ~19 dB.

**Limite conhecido:** com DSP clássico a separação é aproximada — suficiente
para demonstrar o conceito e os controles. Para vozes muito parecidas ou
burburinho denso, o escore deve ser trocado por um embedding neural
(mantendo os mesmos controles). Caminho de upgrade abaixo.

## Projetos de referência pesquisados (GitHub)

**Supressão de ruído / speech enhancement em tempo real:**
- [xiph/rnnoise](https://github.com/xiph/rnnoise) — RNN em C, tempo real, o clássico da categoria (base do noise suppression do WebRTC/Mumble).
- [Rikorose/DeepFilterNet](https://github.com/Rikorose/DeepFilterNet) — enhancement full-band 48 kHz; o DeepFilterNet2 roda em tempo real até num Raspberry Pi 4 (RTF 0.42) — referência de viabilidade embarcada.
- [SoheilGtex/Active-Noise-Cancelling](https://github.com/SoheilGtex/Active-Noise-Cancelling) — supressão de microfone em Python puro (subtração espectral, quadros de 20 ms) — didático, próximo do nosso passo 3.
- Tópicos úteis: [noise-suppression](https://github.com/topics/noise-suppression), [speech-denoising](https://github.com/topics/speech-denoising).

**Separação por identidade de voz (o nosso diferencial):**
- [maum-ai/voicefilter](https://github.com/maum-ai/voicefilter) — implementação PyTorch (não oficial) do VoiceFilter do Google: separa a voz-alvo condicionada num embedding do locutor. É a arquitetura de referência do que o produto quer fazer. *(Atenção IP: o método do Google é patenteado — US20220122611A1; ver docs/business-validation.md, seção 13.)*
- [resemble-ai/Resemblyzer](https://github.com/resemble-ai/Resemblyzer) — embedding de voz (d-vector) em poucas linhas; candidato natural para substituir nosso escore MFCC/pitch.
- [speechbrain/speechbrain](https://github.com/speechbrain/speechbrain) — toolkit PyTorch com receitas prontas de separação (SepFormer), verificação de locutor (ECAPA-TDNN) e enhancement.
- [vb000/SemanticHearing](https://github.com/vb000/SemanticHearing) — o projeto acadêmico (UW/UIST 2023) mais próximo do produto: extração binaural de som-alvo em tempo real (6,56 ms), código aberto.
- [gemengtju/Tutorial_Separation](https://github.com/gemengtju/Tutorial_Separation) — mapa de papers/códigos/datasets de separação e extração de locutor.

**Roadmap de evolução do protótipo:**
1. **v0.1 (este código):** perfil DSP (MFCC+pitch) + máscara espectral ajustável — prova os controles de produto (tolerância/gradiente) sem GPU.
2. **v0.2:** trocar o escore de semelhança por embedding do Resemblyzer (mesmos controles, muito mais robusto a vozes parecidas).
3. **v0.3:** máscara neural tipo VoiceFilter/SepFormer (SpeechBrain) com o embedding como condição — qualidade de produto.
4. **v1.0:** portar para tempo real embarcado — o DeepFilterNet2 no Raspberry Pi mostra que o orçamento computacional fecha.
