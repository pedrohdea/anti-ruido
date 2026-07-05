# Anti-Ruído — Documentação Técnica do Código

## Visão Geral

**Anti-Ruído** é um protótipo de sistema de separação de fala (speech separation) que:
1. Extrai o **perfil acústico** de uma pessoa a partir de uma amostra de voz (altura/pitch, timbre, intensidade)
2. Isola essa voz em áudio ruidoso usando processamento DSP clássico (sem GPU/IA)
3. Oferece dois controles de usuário — **tolerância** (corte de similaridade) e **gradiente** (profundidade de atenuação) — que permitem ajustar a separação em tempo real

O código está organizado em **duas camadas**: CLI/SDK Python (protótipo offline) e servidor web com app JavaScript (modo ao vivo).

---

## Estrutura do Projeto

```
prototype/
├── anti_ruido/              # Módulo Python (SDK)
│   ├── __init__.py
│   ├── profile.py           # Extração e armazenamento de perfil de voz
│   ├── separate.py          # Pipeline de separação (STFT → máscara → Wiener)
│   ├── analyze.py           # Exporta linha do tempo (timeline) para visualização
│   ├── mixer.py             # Utilitário: mistura voz + fundo com SNR controlado
│   ├── demo.py              # Demo sintética (gera voz + ruído, roda pipeline)
│   └── cli.py               # CLI (profile, separate, live, mix, demo, analyze)
├── app/                     # App web
│   ├── server.py            # Servidor Flask
│   ├── static/
│   │   ├── index.html       # Interface (gravação de perfil + modo ao vivo)
│   │   └── visualizador.js  # Timeline interativa (opcional)
│   └── data/                # Armazena perfis e áudio (JSON + MP3)
├── tests/                   # Suite de testes
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── Makefile                 # make → setup + server; make demo → CLI demo
```

---

## Módulos Principais

### 1. `profile.py` — Extração de Perfil de Voz

**Responsabilidade:** Analisar uma amostra de áudio (5–15s de fala limpa) e extrair as dimensões acústicas que identificam uma pessoa.

**Classe principal: `VoiceProfile`**

```python
@dataclass
class VoiceProfile:
    sample_rate: int
    # Altura (pitch)
    pitch_median_hz: float       # Mediana de F0
    pitch_p10_hz: float          # Percentil 10 (faixa baixa)
    pitch_p90_hz: float          # Percentil 90 (faixa alta)
    # Timbre
    mfcc_mean: list[float]       # 20 MFCCs médios
    mfcc_std: list[float]        # 20 desvios-padrão dos MFCCs
    spectral_centroid_hz: float  # "Brilho" do timbre (Hz)
    spectral_bandwidth_hz: float # Largura do espectro (Hz)
    # Intensidade e amplitude
    rms_dbfs: float              # RMS médio em dBFS
    peak_dbfs: float             # Pico em dBFS
    peak_amplitude: float        # Pico em amplitude linear
```

**Função principal: `extract_profile(wav_path: str | Path, sr: int = 22050) -> VoiceProfile`**

Fluxo interno:
1. **Carregamento:** Carrega o arquivo (WAV/MP3/FLAC/OGG) em 22.05 kHz mono, máximo 10s
2. **Voicing detection:** Remove silêncios (`librosa.effects.split`) para não contaminar o perfil com pausas
3. **Pitch (F0):** Usa `librosa.pyin` (robusto a ruído) para detectar altura vocal em 65 Hz–1 kHz
4. **Timbre (MFCC):** Extrai 20 coeficientes MFCC + estatísticas de centroide/largura espectral
5. **Intensidade:** Calcula RMS médio e pico em dBFS

**Saída:** JSON com `VoiceProfile.save(path)` — fica em `app/data/perfil.json` no app web.

```json
{
  "sample_rate": 22050,
  "pitch_median_hz": 180.5,
  "pitch_p10_hz": 140.2,
  "pitch_p90_hz": 225.8,
  "mfcc_mean": [-1200.3, 45.2, ...],
  "mfcc_std": [250.1, 120.5, ...],
  "spectral_centroid_hz": 3400.0,
  "spectral_bandwidth_hz": 2100.0,
  "rms_dbfs": -20.5,
  "peak_dbfs": -8.3,
  "peak_amplitude": 0.38
}
```

---

### 2. `separate.py` — Pipeline de Separação

**Responsabilidade:** Dado um áudio ruidoso e um perfil, isolar a voz-alvo usando processamento de espectro em tempo real (offline) ou blocos (ao vivo).

**Função principal: `separate(input_path, profile, output_path, tolerance=0.5, gradient=0.85, denoise=False) -> SeparationResult`**

**Pipeline DSP (4 passos):**

1. **STFT:** Transforma o áudio para o domínio da frequência (Short-Time Fourier Transform)
   - `N_FFT = 1024` (~46 ms de resolução temporal a 22.05 kHz)
   - `HOP = 256` (~12 ms entre quadros)

2. **Pontuação de Semelhança (`_frame_similarity`):**
   Para cada quadro (~12 ms), combina três sinais:
   
   a. **Timbre (60% peso):** Distância Mahalanobis simplificada dos MFCCs
      ```
      z = (MFCC_quadro - MFCC_média_perfil) / MFCC_desvio_perfil
      dist = sqrt(mean(z²))
      timbre_score = exp(-dist / 2.0)  # 1.0 = match perfeito, 0.0 = diferente
      ```
   
   b. **Altura (40% peso):** Pitch do quadro cai na faixa típica do perfil?
      ```
      se F0 em [pitch_p10 × 0.8, pitch_p90 × 1.2] → pitch_score = 1.0
      senão → pitch_score = 0.15 (ruído pode ter pitch acidental)
      se F0 não detectado → pitch_score = 0.35
      ```
   
   c. **Energia:** Silêncio nunca é "a voz"
      ```
      energy_gate = 1.0 se RMS > percentil_20, senão 0.0
      ```
   
   **Score final:** `score = (0.6 × timbre_score + 0.4 × pitch_score) × energy_gate`
   
   Suavização temporal: Aplica filtro 1D de ~8 quadros (~90 ms) para evitar "tremideira" na máscara.
   
   Normalização relativa (percentis 5–95 do próprio arquivo): Garante que "tolerância" signifique sempre "os X% de quadros mais parecidos", independente da escala absoluta.

3. **Máscara por Quadro (Sigmoide):**
   ```
   softness = 0.08
   frame_mask = 1.0 / (1.0 + exp(-(score - tolerance) / softness))
   ```
   - `score >> tolerance` → `frame_mask ≈ 1.0` (mantém)
   - `score << tolerance` → `frame_mask ≈ 0.0` (atenua)
   - Transição suave (sigmoide) → sem "cliques" audíveis no áudio

4. **Subtração de Wiener:**
   O espectro do ruído é estimado a partir dos 30% de quadros MENOS parecidos com a voz:
   ```
   noise_spectrum = mean(|STFT[quadros_ruidosos]|²)
   wiener_gain = max(1e-3, 1.0 - (1.0 + gradient) × noise_spectrum / (|STFT|² + eps))
   output_magnitude = |STFT| × wiener_gain × frame_mask
   ```
   
   Isso é o que dá ganho real contra ruído de multidão (validado em testes com áudio real: +1,4 dB de SI-SDR contra burburinho).

**Controles de Usuário:**

| Parâmetro | Intervalo | Efeito |
|---|---|---|
| `tolerance` | 0.0–1.0 | **Corte de similaridade.** 0.0 = permissivo (passa tudo); 1.0 = rigoroso (corta quase tudo). Recomendado: 0.3–0.8. |
| `gradient` | 0.0–1.0 | **Profundidade de atenuação.** 0.0 = deixa passar sem atenuar; 1.0 = silencia completamente. Controla suavidade da separação. Recomendado: 0.7–0.95. |
| `denoise` | bool | **Denoise estacionário (opt-in).** Remove zumbido/AC constante (ajuda contra ruído fixo) mas PIORA contra burburinho (validado: -1,6 dB). Use só para ruído constante. |

**Saída:**

```python
@dataclass
class SeparationResult:
    output_path: str        # Caminho do WAV resultante
    duration_s: float       # Duração em segundos
    frames_kept_pct: float  # % de quadros acima do limiar de máscara
    input_rms_dbfs: float   # RMS médio do entrada (dBFS)
    output_rms_dbfs: float  # RMS médio da saída (dBFS)
    tolerance: float        # Parâmetro usado
    gradient: float         # Parâmetro usado
```

**Variante para Modo Ao Vivo: `filter_chunk(y: np.ndarray, sr: int, profile, tolerance=0.5, gradient=0.85) -> tuple[np.ndarray, dict]`**

- Versão otimizada para blocos de ~1s (não usa pyin, que é lento)
- Usa só MFCC + energia → processa 1s em dezenas de milissegundos
- Retorna: (áudio filtrado, métricas do bloco para a interface)

---

### 3. `analyze.py` — Timeline para Visualização

**Responsabilidade:** Exportar a "visão" do algoritmo sobre cada instante em JSON, para visualizador web sincronizado ao áudio.

**Função:** `analyze_timeline(input_path, profile, tolerance=0.5, gradient=0.85, stride=4) -> dict`

**Saída (JSON):**

```json
{
  "duration_s": 5.2,
  "sample_rate": 22050,
  "tolerance": 0.5,
  "gradient": 0.85,
  "profile": {
    "pitch_median_hz": 180.5,
    "pitch_p10_hz": 140.2,
    "pitch_p90_hz": 225.8,
    "spectral_centroid_hz": 3400.0
  },
  "points": [
    {
      "t": 0.0,
      "db": -25.3,
      "f0": 180.5,
      "centroid": 3420.0,
      "score": 0.87,
      "gain": 0.95
    },
    {
      "t": 0.05,
      "db": -24.8,
      "f0": 182.3,
      "centroid": 3410.0,
      "score": 0.91,
      "gain": 0.97
    },
    ...
  ]
}
```

Cada ponto = 1 quadro (multiplicado por `stride` para reduzir tamanho). Permite visualizar em tempo real:
- Nível (dB) do áudio
- Pitch detectado (Hz)
- "Brilho" espectral (centroide em Hz)
- Score de semelhança com o perfil (0–1)
- Ganho aplicado pela separação (0–1)

---

### 4. `mixer.py` — Utilitário de Teste

**Responsabilidade:** Misturar voz + ruído de fundo num arquivo único com SNR (Signal-to-Noise Ratio) controlado.

**Função:** `mix_files(voice_path, background_path, output_path, snr_db=0.0, sr=22050) -> dict`

**Parâmetro:** `snr_db`
- `0 dB` → voz e fundo com mesma energia (bar bem barulhento)
- `5 dB` → voz 5 dB acima do fundo (restaurante cheio, conversável)
- `-5 dB` → fundo mais alto que voz (show/balada, difícil)

Usado para montar cenas de teste realistas antes de rodar `separate()`.

---

### 5. `demo.py` — Protótipo Sintético

**Responsabilidade:** Gerar uma "voz" sintética (glotis + formantes) + ruído, rodar o pipeline e exibir métricas.

**Funções principais:**

- `_synth_voice(duration_s, f0_base, seed=None)` → gera uma voz sintética
- `_snsd_reference(name: str)` → carrega referência de ruído real (MS-SNSD dataset)
- `demo_pipeline()` → Executa o pipeline completo e imprime SI-SDR (Signal-to-Interference-plus-Noise Ratio)

Usado para validação rápida em CI/testes sem precisar de áudio real.

---

### 6. `cli.py` — Interface de Linha de Comando

**Responsabilidade:** Expor todos os comandos como CLI para uso offline.

**Comandos:**

```bash
python -m anti_ruido.cli profile <input.wav> [-o perfil.json]
  → Extrai perfil de voz e salva em JSON

python -m anti_ruido.cli separate <input.wav> -p perfil.json [-o output.wav] [--tolerance 0.5] [--gradient 0.85]
  → Separa a voz no áudio usando o perfil

python -m anti_ruido.cli live -p perfil.json [-o live.wav]
  → Captura do microfone em tempo real e filtra (requer sounddevice/PortAudio)

python -m anti_ruido.cli mix <voice.wav> <background.wav> [-o cena.wav] [--snr 0]
  → Mistura voz + fundo com SNR controlado

python -m anti_ruido.cli demo
  → Roda demo sintética, mostra métricas (sem microfone)

python -m anti_ruido.cli analyze <input.wav> -p perfil.json [-o timeline.json]
  → Exporta timeline para visualizador web
```

---

### 7. `app/server.py` — Servidor Web (Flask)

**Responsabilidade:** Expor o pipeline via HTTP para a interface JavaScript do navegador.

**Rotas principais:**

| Rota | Método | Função |
|---|---|---|
| `/` | GET | Serve `index.html` (app web) |
| `/api/profile/extract` | POST | Recebe blob de áudio (WebM/MP3), extrai perfil e carrega globalmente |
| `/api/profile/get` | GET | Retorna o perfil carregado (JSON) |
| `/api/process/block` | POST | Recebe bloco de ~1s, processa com `filter_chunk()`, retorna áudio filtrado + métricas |
| `/api/timeline` | POST | Recebe áudio, retorna `analyze_timeline()` completo |
| `/api/download/profile` | GET | Download do perfil em MP3 |

**Fluxo de uso no app web:**

1. Usuário grava 10s de voz (navegador registra em WebM/Opus via `MediaRecorder`)
2. JS envia POST `/api/profile/extract` (blob de áudio)
3. Server: converte para WAV (ffmpeg) → `extract_profile()` → salva em JSON
4. Modo AO VIVO:
   - Navegador captura microfone continuamente em chunks de ~1s
   - Cada chunk → POST `/api/process/block`
   - Server filtra com `filter_chunk()` → retorna áudio processado + métricas em header `X-Metrics`
   - JS reproduz áudio nos fones (com latência ~1-2s total = captura + processamento + playback)

---

## Constantes Globais

```python
from anti_ruido.profile import N_FFT, HOP, N_MFCC

N_FFT = 1024           # Tamanho da janela STFT (~46 ms a 22.05 kHz)
HOP = 256              # Hop entre quadros (~12 ms)
N_MFCC = 20            # Número de coeficientes MFCC para timbre

# Em profile.py:
MAX_PROFILE_SECONDS = 10.0  # Amostra de perfil sempre cortada em 10s
SR = 22050             # Taxa de amostragem padrão (app web)
```

---

## Fluxos de Uso

### Fluxo 1: CLI Offline (Desenvolvimento/Validação)

```bash
# 1. Extrair perfil
python -m anti_ruido.cli profile minha-voz.wav -o perfil.json

# 2. Misturar voz + fundo para teste
python -m anti_ruido.cli mix fala-limpa.wav multidao.wav -o teste.wav --snr 0

# 3. Separar
python -m anti_ruido.cli separate teste.wav -p perfil.json -o resultado.wav --tolerance 0.6 --gradient 0.8

# 4. Exportar timeline para visualizar
python -m anti_ruido.cli analyze teste.wav -p perfil.json -o timeline.json
```

### Fluxo 2: App Web (Modo Interativo)

```
Browser (index.html)
  ↓ [MediaRecorder + Web Audio API]
  ↓ grava microfone em WebM/Opus
  ↓ POST /api/profile/extract (blob)
  ↓
Server (Flask)
  ↓ ffmpeg: WebM → WAV
  ↓ extract_profile()
  ↓ save JSON + convert to MP3
  ↓
Browser: Modo AO VIVO ativado, "Termômetro" aparece
  ↓ captura microfone continuamente (chunks ~1s)
  ↓ POST /api/process/block (cada chunk + tolerance + gradient)
  ↓
Server: filter_chunk() → áudio processado
  ↓ return audio stream + X-Metrics header
  ↓
Browser: reproduz em fones, atualiza interface com métricas
```

---

## Testes

Localização: `tests/`

**Suite de testes:**
- `test_profile.py` → Extração de perfil (roundtrip JSON, validação de ranges)
- `test_separate.py` → Separação (dimensões de entrada/saída, clipping)
- `test_mixer.py` → Mistura (SNR real vs. teórico)
- `test_demo.py` → Demo sintética (pipeline completo)
- `test_app.py` → Endpoints Flask (upload, processing, CORS)
- `test_cli.py` → CLI (parsing de args, integração)

**Executar:**
```bash
pytest                          # roda todas
pytest tests/test_separate.py   # teste específico
pytest -v --tb=short           # verbose + traceback resumido
```

---

## Performance e Limites Conhecidos

### Latência (Modo Ao Vivo)

- **Captura:** ~50 ms (chunk de ~1s com processamento em tempo real)
- **Processamento:** ~100–200 ms por bloco (filter_chunk sem pyin)
- **Playback:** ~50 ms
- **Total percebido:** ~1–2s (protótipo web; produto embarcado seria <20 ms)

### Qualidade de Separação

**Teste com áudio real** (LibriSpeech + MS-SNSD Babble, SNR 0 dB):

| Variante | SI-SDR (dB) | vs. entrada |
|---|---|---|
| Entrada (sem processamento) | −0.05 | — |
| Máscara de quadro apenas | −0.25 | ~0 (piora marginal) |
| Pente harmônico no pitch | −1.77 | **piora** (pitch é ambíguo em mistura) |
| **Máscara de quadro + Wiener (atual)** | **+1.34** | **+1.4 (melhora real)** |
| Máscara + Wiener + denoise | −1.66 | **piora** (denoise não ajuda contra burburinho) |

**Interpretação:** +1,4 dB é ganho modesto mas real contra o pior caso (fala com fala). É suficiente para demonstrar o conceito dos controles, mas inadequado para produção — a solução é trocar o escore DSP por embedding neural (roadmap v0.2).

### Limitações Conhecidas

1. **Vozes muito parecidas:** DSP puro não consegue diferenciar bem; solução: embedding neural (Resemblyzer).
2. **Burburinho denso:** Ruído com muita fala sobreposta é o "cocktail party problem" clássico; DSP não resolve perfeitamente.
3. **Compatibilidade de amostra:** Perfil deve ser de áudio limpo (~5–15s); amostra ruidosa ou silenciosa degrada o resultado.
4. **Taxa de amostragem:** Fixo em 22.05 kHz; entrada em outra taxa é ressampled automaticamente (reduz qualidade se muito diferente).

---

## Dependências

**Sistema:**
- `python3` (3.10+)
- `ffmpeg` (conversão de áudio)
- `libportaudio2` (opcional, modo live no CLI)

**Python (requirements.txt):**
- `numpy` — cálculos vetorizados
- `scipy` — processamento de sinal
- `librosa` — análise acústica (MFCC, pitch, STFT, etc.)
- `soundfile` — leitura/escrita de WAV
- `noisereduce` — denoise estacionário (opt-in)
- `flask` — servidor web
- `flask-cors` — CORS para app web

**Desenvolvimento:**
- `pytest` — testes
- `pytest-cov` — cobertura
- `black` — formatação
- `mypy` — type checking

---

## Roadmap Futuro (v0.2+)

**v0.1 (atual):** Perfil DSP (MFCC+pitch) + máscara espectral → prova dos controles sem GPU

**v0.2:** Trocar escore DSP por embedding (Resemblyzer) → robusto a vozes parecidas, mantém controles

**v0.3:** Máscara neural (VoiceFilter/SepFormer) com embedding como condição → qualidade de produto

**v1.0:** Porta para embarcado (Raspberry Pi/ARM) → tempo real <20 ms, bateria otimizada

---

## Como Contribuir

1. Abrir issue em https://github.com/pedrohdea/anti-ruido
2. Fazer fork + branch: `git checkout -b feature/seu-nome`
3. Desenvolver + testes: `pytest`
4. Commit + PR com descrição clara

**Orientações de código:**
- Type hints em todas as funções públicas
- Docstrings em PT-BR (formato Google)
- Sem magic numbers — definir constantes com nome
- Log com `logging` (não `print`)

---

## Referências e Documentação Adicional

Ver [REFERENCES.md](REFERENCES.md) para:
- Papers acadêmicos (target speaker extraction, cocktail party problem)
- Projetos de código aberto (Semantic Hearing, DeepFilterNet, rnnoise)
- Bases de dados de áudio (MS-SNSD, LibriSpeech, TIMIT)
- Documentação de bibliotecas (librosa, scipy.signal, etc.)

---

## Licença

[Ver LICENSE](LICENSE)

---

**Última atualização:** 2026-07-05
**Versão do código:** 0.1.0
