# Protótipo Anti-Ruído — separação de fala com perfil de voz

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
2. Máscara tempo-frequência: quadros abaixo da **tolerância** são atenuados
   pela profundidade do **gradiente** (transição sigmoide, sem cliques); bins
   fora da banda útil da voz também são atenuados.
3. Redução final de ruído estacionário (spectral gating, via `noisereduce`).

**Limite conhecido:** com DSP clássico a separação é aproximada — suficiente
para demonstrar o conceito e os controles. Para vozes muito parecidas ou
burburinho denso, o passo 2 deve ser trocado por um embedding neural
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
