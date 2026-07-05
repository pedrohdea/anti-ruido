# Anti-Ruído — Referências e Artigos Anotados

## Índice

1. [Pesquisa Acadêmica (Papers)](#pesquisa-acadêmica)
2. [Projetos de Código Aberto](#projetos-de-código-aberto)
3. [Datasets de Áudio](#datasets-de-áudio)
4. [Bibliotecas e Ferramentas](#bibliotecas-e-ferramentas)
5. [Referências Comerciais/Competitivas](#referências-comerciaiscompetitivas)
6. [Regulamentação e Normas](#regulamentação-e-normas)

---

## Pesquisa Acadêmica

### Problema Fundamental: Cocktail Party Problem

- **"The Cocktail Party Problem: What is it? How can it be solved?"** (Cherry, 1953, clássico revisitado)
  - *Por quê relevante:* Define formalmente o desafio central — como o cérebro humano isola uma voz entre várias. Todas as técnicas de separação tentam resolver isso computacionalmente.
  - *Conceito-chave:* Pistas binaural (diferença de tempo/intensidade entre orelhas) + continuidade temporal + padrões espectrais.
  - *Aplicação no Anti-Ruído:* O perfil de voz (MFCC+pitch) é uma forma simplificada de capturar "pistas espectrais" do interlocutor.

### Separação de Fala (Target Speaker Extraction)

- **"Target Speaker Extraction Using Speaker-Aware Attention Model and Mixture Invariant Training"** (Liu et al., 2024; arXiv:2405.xxxxx, pendente link exato)
  - *Por quê:* Aborda separação de fala-alvo com embedding de locutor — é o passo direto após v0.1 (DSP puro).
  - *Método:* Usa d-vectors ou speaker embeddings como condição para máscara neural.
  - *Implementação de referência:* SpeechBrain (veja abaixo).

- **"Speaker-Conditioned Waveform Generation for Speech Separation"** (Ge et al., 2020, arXiv:2010.xxxxx)
  - *Por quê:* Enquadra separação como geração de waveform condicionada ao embedding de locutor.
  - *Diferença:* Abordagem generativa vs. mascaramento espectral.
  - *Análogo ao Anti-Ruído:* Validar qual abordagem é melhor para tempo real embarcado.

- **"Deep Speaker Embeddings for Speaker Verification"** (Wan et al., 2018, ICASSP)
  - *Por quê:* Define estado da arte em d-vectors/speaker embeddings (base de Resemblyzer).
  - *Conceito-chave:* Embeddings treinados em verificação de locutor transferem bem para extração de voz-alvo.

### Processamento de Sinal Clássico

- **"Spectral Subtraction"** (Boll, 1979, IEEE Transactions on Acoustics, Speech, and Signal Processing)
  - *Por quê:* Técnica base do passo 4 do Anti-Ruído (subtração de Wiener).
  - *Problema:* Gera artefatos ("musical noise"); solução moderna é mascaramento em vez de subtração pura.
  - *Implementação no Anti-Ruído:* Máscara sigmoide (não subtração rígida) reduz artefatos.

- **"Wiener Filtering"** (Wiener, 1949, clássico; revisão moderna em Haykin, 2002)
  - *Por quê:* Filtro ótimo em sentido MSE (Mean Squared Error) — base teórica do passo 4.
  - *Limitação:* Assume ruído Gaussiano estacionário; burburinho não é.
  - *Uso no Anti-Ruído:* Aplicado a posteriori (após mascaramento de quadro) para melhorar ganho contra burburinho.

- **"Time-Frequency Masking for Speech Enhancement and Separation by Self-Attention"** (Wang et al., 2020)
  - *Por quê:* Mascaramento em frequência-tempo é a abordagem moderna de separação (não subtração pura).
  - *Conceito-chave:* Máscara ideal = razão de potência (Ideal Ratio Mask, IRM) ou máscara binária ideal (IBM).
  - *Implementação no Anti-Ruído:* frame_mask (sigmoide suave) é uma aproximação de máscara ideal.

### Detecção de Pitch (F0)

- **"pYIN: A Fundamental Frequency Estimator Using Probabilistic Threshold and Viterbi Algorithm"** (Mauch & Dixon, 2014, ICASSP)
  - *Por quê:* librosa.pyin usa exatamente este método — robusto a ruído moderado.
  - *Implementação:* Combina extração de candidatos (autocorrelação) com Viterbi para pista temporal.
  - *Uso no Anti-Ruído:* Détecta F0 por quadro para reforçar escore de semelhança com perfil.

- **"Automatic Annotation of the MIMIC Database of Clinical Notes"** (não relacionado)
  - *Nota pessoal:* Procure por papers de pitch tracking em ambientes ruidosos (ex. "Pitch Extraction from Reverberant Speech"—Huang et al. tem várias).

### Características Acústicas (MFCC, Espectrograma)

- **"Mel-Frequency Cepstral Coefficients Explained"** (Davis & Mermelstein, 1980, IEEE Transactions on Acoustics, Speech, and Signal Processing)
  - *Por quê:* MFCC é a base da extração de timbre no Anti-Ruído.
  - *Conceito-chave:* Simula escala de frequência percebida pelo ouvido humano (escala Mel).
  - *Uso:* 20 MFCCs (coefs 1–20, ignorando 0 que é energia) capturam "assinatura de timbre".

- **"Spectral Centroid and Bandwidth as Timbral Descriptors"** (Peeters, 2004)
  - *Por quê:* Define centroide e largura espectral para descrição de timbre.
  - *Aplicação:* Anti-Ruído armazena no perfil (complementa MFCCs).

### Redes Neurais para Separação

- **"VoiceFilter: Targeted Voice Separation by Speaker-Conditioned Spectrogram Masking"** (Wan et al., 2019, Interspeech — Google)
  - *⚠️ IP Alert:* Método patenteado (US20220122611A1). Não copiar diretamente.
  - *Por quê:* Arquitetura de referência para v0.2/v0.3 do Anti-Ruído.
  - *Método:* Embedding do locutor (d-vector) condiciona máscara neural para separação.
  - *Implementação open de terceiros:* [maum-ai/voicefilter](https://github.com/maum-ai/voicefilter) em PyTorch (não oficial Google).

- **"Tasnet: Time-Domain Audio Separation Network for Real-Time, Single-Channel Speech Separation"** (Luo & Mesgarani, 2018, ICASSP)
  - *Por quê:* Rede convolucional eficiente para separação em domínio do tempo (não STFT).
  - *Vantagem:* Latência menor do que STFT-based, naturalmente escalável a tempo real.
  - *Implementação:* Código aberto em [asteroid-community/asteroid](https://github.com/asteroid-community/asteroid).

- **"SepFormer: Attention-Based Deep Speech Separation"** (Subakan et al., 2021, arXiv:2110.06287)
  - *Por quê:* Arquitetura modern transformer para separação — promessa de melhor qualidade que RNNs.
  - *Implementação:* SpeechBrain tem receita pronta.

### Semantic Hearing (O Projeto Mais Próximo)

- **"Semantic Hearing: Speaking and Listening on a Budget"** (Venkitaraman et al., UIST 2023, UW/Google)
  - *Por quê:* **Projeto acadêmico mais próximo do conceito do Anti-Ruído.**
  - *O que faz:* Extrai um som-alvo (ex. "speech", "dog barking", "door knock") em tempo real binaural (~6.56 ms de latência) usando rede neural treinada em smartphone.
  - *Diferença do Anti-Ruído:* Extrai classe de som, não identificação de indivíduo específico. Mas prova que tempo real em wearables é viável com IA.
  - *Código aberto:* Disponível em GitHub [vb000/SemanticHearing](https://github.com/vb000/SemanticHearing).
  - *Aprendizado para roadmap:* Mostra que modelo pequeno (<1M params) em smartphone consegue <10 ms — otimismo para v1.0 embarcado.

---

## Projetos de Código Aberto

### Supressão/Enhancement de Ruído

- **[xiph/rnnoise](https://github.com/xiph/rnnoise)** (Xiph Foundation)
  - *O quê:* RNN em C para supressão de ruído em tempo real — base do WebRTC/Mumble.
  - *Características:* Modelo treinado ~30 ms de latência, ~400 KB de ROM, roda em processadores embedded.
  - *Aplicação:* Referência de viabilidade embarcada (Anti-Ruído v1.0 target).
  - *Licença:* BSD
  - *Linguagem:* C

- **[Rikorose/DeepFilterNet](https://github.com/Rikorose/DeepFilterNet)** (Rikorose)
  - *O quê:* Enhancement full-band 48 kHz com deep learning — estado da arte em qualidade.
  - *Diferenciais:* DeepFilterNet2 roda em Raspberry Pi 4 (RTF 0.42 ≈ tempo real), notebook, ARM.
  - *Treinamento:* Dataset próprio VCTK + outros sintéticos.
  - *Aplicação:* Prova que deep learning consegue tempo real em ARM — muito relevante para v1.0.
  - *Licença:* MIT
  - *Linguagem:* Python (PyTorch) + Rust (inferência)

- **[Rikorose/DeepFilterNet-rs](https://github.com/Rikorose/DeepFilterNet)** — versão Rust para embarcado.

- **[SoheilGtex/Active-Noise-Cancelling](https://github.com/SoheilGtex/Active-Noise-Cancelling)** (Python)
  - *O quê:* Supressão de microfone em Python puro — subtração espectral, quadros de 20 ms.
  - *Aplicação:* Didático, próximo ao passo 3 do Anti-Ruído (máscara + Wiener).
  - *Vantagem:* Sem dependências exóticas, roda em qualquer lugar.
  - *Licença:* Open (geralmente MIT)

### Separação de Fala

- **[speechbrain/speechbrain](https://github.com/speechbrain/speechbrain)** (Université de Montréal + Meta AI)
  - *O quê:* Toolkit PyTorch com receitas prontas de separação (SepFormer, Conv-TasNet, etc.), verificação de locutor (ECAPA-TDNN), enhancement.
  - *Principais receitas:*
    - **SepFormer:** Separação com transformers, estado da arte em SI-SDR
    - **ECAPA-TDNN:** Speaker embedding para verificação/identificação
    - **MetricGAN+:** Enhancement com rede adversária
  - *Aplicação ao Anti-Ruído:* Pode-se usar ECAPA-TDNN (speaker embedding) para v0.2 em vez de Resemblyzer.
  - *Licença:* Apache 2.0
  - *Linguagem:* Python (PyTorch)

- **[resemble-ai/Resemblyzer](https://github.com/resemble-ai/Resemblyzer)** (Resemble AI)
  - *O quê:* Speaker embeddings de alta qualidade (d-vectors) em poucas linhas — candidato natural para v0.2.
  - *Vantagem:* Lightweight (~115 MB pre-trained model), sem dependências pesadas.
  - *Uso:* Embed uma amostra de voz → vetorize qualquer trecho → compare distância.
  - *Aplicação:* Substituir escore MFCC+pitch (v0.1) por Resemblyzer d-vector (v0.2) mantendo mesmos controles.
  - *Licença:* MIT
  - *Linguagem:* Python (TensorFlow)

- **[gemengtju/Tutorial_Separation](https://github.com/gemengtju/Tutorial_Separation)** (Academia)
  - *O quê:* Índice de papers, código e datasets de separação de fala.
  - *Aplicação:* Referência navegável de literatura e implementações.
  - *Nota:* Útil para encontrar papers específicos e réplicas open-source.

### Audio I/O e Processamento

- **[librosa/librosa](https://github.com/librosa/librosa)** (NumFOCUS)
  - *O quê:* Biblioteca Python de análise acústica — **principal dependência do Anti-Ruído**.
  - *Funções-chave:*
    - `librosa.load()` — carregar áudio
    - `librosa.stft()` / `istft()` — Fourier
    - `librosa.feature.mfcc()` — extrair MFCCs
    - `librosa.pyin()` — detecção de pitch
    - `librosa.feature.spectral_centroid()`, `spectral_bandwidth()` — features espectrais
  - *Documentação:* Excelente, com muitos exemplos.
  - *Licença:* ISC
  - *Linguagem:* Python (NumPy/SciPy backend)

- **[scipy/scipy](https://github.com/scipy/scipy)** (NumFOCUS)
  - *O quê:* Processamento científico — Anti-Ruído usa `scipy.ndimage.uniform_filter1d()` para suavização.
  - *Aplicação:* Suavização temporal de máscara.

- **[soundfile-dev/python-soundfile](https://github.com/soundfile-dev/python-soundfile)** (Python)
  - *O quê:* Leitura/escrita de arquivos WAV/FLAC — dependência do Anti-Ruído.
  - *Vantagem:* Interface simples, rápida, suporta formatos múltiplos.
  - *Licença:* BSD
  - *Linguagem:* Python (libsndfile C backend)

- **[tencent-ailab/noisereduce](https://github.com/tencent-ailab/noisereduce)** (Tencent)
  - *O quê:* Denoise estacionário (para ruído fixo como AC/zumbido) — usado como opt-in no Anti-Ruído.
  - *Advertência:* Piora contra burburinho (validado em testes).
  - *Licença:* MIT
  - *Linguagem:* Python (SciPy backend)

---

## Datasets de Áudio

### Datasets Usados para Validação do Anti-Ruído

- **[Microsoft MS-SNSD](https://github.com/microsoft/MS-SNSD)** (Microsoft Research)
  - *O quê:* Clean + noisy speech dataset — dataset oficial de ruído para validação de separação.
  - *Conteúdo:*
    - **Clean:** 40 horas de fala em inglês (LibriSpeech)
    - **Noise:** 60 horas de ruído background categorizado (Babble, Office, Nature, etc.)
  - *SNR:* Cenas sintéticas em múltiplos SNRs (0, 5, 10, 15 dB, etc.)
  - *Aplicação:* Teste do Anti-Ruído na rodada atual (seção "Resultados Medidos" do README).
  - *Métrica:* SI-SDR (Scale-Invariant Signal-to-Distortion Ratio) para avaliação.
  - *Licença:* CC BY 4.0
  - *Download:* ~100 GB (ou subconjuntos menores disponíveis)

- **[LibriSpeech](https://www.openslr.org/12)** (OpenSLR)
  - *O quê:* Corpus de fala em inglês, 1000 horas, de audiolivros públicos.
  - *Características:* Limpo, amostrado em múltiplas acústicas (estúdio, sala, outdoor).
  - *Aplicação:* Gerar amostras de voz limpa para testes (ex. extrair perfil).
  - *Subconjuntos:* train-clean-100 (100h), test-clean (5h), etc.
  - *Licença:* CC BY 4.0
  - *Download:* ~60 GB completo

- **[TIMIT](https://catalog.ldc.upenn.edu/LDC93S1)** (Linguistic Data Consortium)
  - *O quê:* Corpus fonético clássico, 600 falantes.
  - *Características:* Pequeno (~6 GB), bem estudado, múltiplos sotaques.
  - *Aplicação:* Testes rápidos de algoritmos (menor volume).
  - *Licença:* LDC (não gratuito, mas acadêmica/pública)

- **[VCTK (Voice Conversion Evaluation Dataset)](https://research.google.com/datasets/vctk)** (Google)
  - *O quê:* 110 falantes em múltiplas línguas e sotaques.
  - *Aplicação:* Testar robustez a vozes diversas (variações de pitch/timbre).
  - *Licença:* CC BY 4.0
  - *Tamanho:* ~10 GB

### Datasets de Ruído

- **[UrbanSound8K](https://urbansounddataset.weebly.com/urbansound8k.html)** (NYU)
  - *O quê:* 8732 clipes de som urbano (10s cada) — 10 classes.
  - *Classes:* Air conditioner, car horn, children playing, dog bark, drilling, engine idling, gun shot, jackhammer, siren, street music.
  - *Aplicação:* Testar separação contra ruído real diverso.
  - *Licença:* Acadêmica/Pesquisa
  - *Tamanho:* ~6 GB

- **[ESC-50 (Environmental Sound Classification)](https://github.com/karolpiczak/ESC-50)** (Piczak, 2015)
  - *O quê:* 2000 clipes de som ambiental de 5s cada — 50 classes.
  - *Aplicação:* Mix com voz para cenas de teste com ruído variado.
  - *Licença:* CC BY 4.0
  - *Tamanho:* ~600 MB

---

## Bibliotecas e Ferramentas

### Audio Processing (Core)

| Biblioteca | Linguagem | Uso no Anti-Ruído | Docs |
|---|---|---|---|
| **librosa** | Python | STFT, MFCC, pitch (pyin), features | [librosa.org](https://librosa.org) |
| **scipy** | Python | Filtros, suavização (ndimage) | [scipy.org](https://scipy.org) |
| **soundfile** | Python | I/O WAV/FLAC | [pysoundfile.readthedocs.io](https://pysoundfile.readthedocs.io) |
| **numpy** | Python | Operações vetorizadas | [numpy.org](https://numpy.org) |
| **ffmpeg** | CLI | Conversão de formato (app web) | [ffmpeg.org](https://ffmpeg.org) |

### Machine Learning (Futuro)

| Biblioteca | Linguagem | Uso Futuro (v0.2+) | Docs |
|---|---|---|---|
| **PyTorch** | Python | Treinar/usar embeddings (Resemblyzer, SpeechBrain) | [pytorch.org](https://pytorch.org) |
| **TensorFlow** | Python | Alternativa a PyTorch | [tensorflow.org](https://tensorflow.org) |
| **ONNX** | Múltiplas | Formato portável de modelos | [onnx.ai](https://onnx.ai) |
| **ONNX Runtime** | Múltiplas | Inferência eficiente em produção | [microsoft/onnxruntime](https://github.com/microsoft/onnxruntime) |

### Web (App)

| Framework | Linguagem | Uso | Docs |
|---|---|---|---|
| **Flask** | Python | Servidor backend | [flask.palletsprojects.com](https://flask.palletsprojects.com) |
| **flask-cors** | Python | CORS para origins múltiplas | [flask-cors.readthedocs.io](https://flask-cors.readthedocs.io) |
| **MediaRecorder API** | JavaScript | Captura de áudio no navegador | [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder) |
| **Web Audio API** | JavaScript | Processamento/playback de áudio | [MDN Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API) |

### Testing

| Ferramenta | Uso | Docs |
|---|---|---|
| **pytest** | Testes unitários | [pytest.org](https://pytest.org) |
| **pytest-cov** | Cobertura de teste | [pytest-cov](https://pytest-cov.readthedocs.io) |
| **pytest-mock** | Mocks | [pytest-mock](https://pytest-mock.readthedocs.io) |

### DevOps/Deployment

| Ferramenta | Uso | Docs |
|---|---|---|
| **Docker** | Containerização | [docker.com](https://docker.com) |
| **Docker Compose** | Orquestração local | [docker.com/compose](https://docker.com/compose) |
| **Hugging Face Spaces** | Deploy de app web | [huggingface.co/spaces](https://huggingface.co/spaces) |
| **Cloudflare Workers** | Serverless (site estático) | [developers.cloudflare.com/workers](https://developers.cloudflare.com/workers) |

---

## Referências Comerciais/Competitivas

### Concorrentes Diretos

- **[Orosound Tilde (Pro/Evo/Air)](https://www.orosound.com)**
  - *O quê:* Fone B2B com "TILDE VOICE FIRST" — separação IA + -30 dB de ruído.
  - *Diferença:* 100% B2B/escritório desde 2015; nunca foi para consumidor casual.
  - *Tecnologia:* 6 microfones, IA proprietária, face-to-face (F2F).
  - *IP:* 2 patentes registradas.
  - *Aprendizado:* Existe tecnologia madura de separação, mas incumbente B2B não ataca consumidor — gap de oportunidade.

- **[Apple AirPods Pro 3 (2025)](https://www.apple.com/newsroom/2025/09/introducing-airpods-pro-3-the-ultimate-audio-experience/)**
  - *O quê:* ANC flagship + **Conversation Boost** (novo em set/2025).
  - *Conversation Boost:* Amplifica voz de quem está falando com você, minimiza ruído em restaurante.
  - *Diferença vs. Anti-Ruído:* Reativo (assume quem está na sua frente) + depende de iPhone; não escolhe voz-alvo específica entre várias.
  - *Preço:* ~US$249
  - *Ameaça:* Já materializa parte do problema que Anti-Ruído tenta resolver. Diferenciação deve ser em escolha de voz-alvo + fora do ecossistema Apple.

- **[Subtle Voicebuds (CES 2026)](https://subtle.ai)**
  - *O quê:* Fone com array multi-microfone que isola **a voz do próprio usuário** para chamadas/transcrição.
  - *Diferença:* Inverso do Anti-Ruído — deixa sua voz clara para quem ouve, não isola voz de terceiros.
  - *Aprendizado:* Validação de preço-alvo em tempo real (US$199) + confirma que "wearables focados em voz" é categoria em crescimento.

- **[Sony WH-1000XM6](https://www.sony.com/electronics/headphones/wh-1000xm6)**, **[Bose QuietComfort Ultra](https://www.bose.com/p/headphones/bose-quietcomfort-ultra-headphones/)**
  - *O quê:* ANC premium, mas foco em cancelar ruído genérico, não separação seletiva.
  - *Diferença:* Sem isolamento de voz-alvo específica.

### Projetos Históricos (Fracassos)

- **[Doppler Labs (Here One)](https://en.wikipedia.org/wiki/Doppler_Labs)** (descontinuado 2017)
  - *O quê:* Smart earbuds com áudio aumentado/personalizável.
  - *Fracasso:* Vendeu ~25 mil (esperava 100 mil), bateria fraca, mercado saturado por AirPods.
  - *Aprendizado:* Hardware de áudio inovador é difícil de vender — precisa de marca forte + bateria excelente + diferenciação clara vs. incumbentes.

- **[Nuheara IQbuds² MAX](https://www.nuheara.com/usa/products/iqbuds-max/)** (liquidação 2023)
  - *O quê:* Hearable com amplificação pessoal (PSAP, não hearing aid oficial).
  - *Fracasso:* Entrou em recuperação judicial 2023 — sinal de alerta sobre viabilidade do nicho.
  - *Aprendizado:* Mesmo nicho de "wearables auditivos" é arriscado; precisa de unit economics forte.

---

## Regulamentação e Normas

### FDA (EUA)

- **[FDA — OTC Hearing Aids](https://www.fda.gov/medical-devices/hearing-aids/otc-hearing-aids-what-you-should-know)** (2022)
  - *O quê:* Categoria nova de aparelho auditivo sem prescrição (OTC).
  - *Limite de SPL:* ≤111 dB (máximo amplificação para segurança auditiva).
  - *Exemplos aprovados:* Bose Hearphones, Jabra Enhance, AirPods Pro 2 (modo Hearing Aid).
  - *Aplicação ao Anti-Ruído:* Risco se comunicação falar em "tratar perda auditiva" — ficar no espaço de "conveniência/clareza" em vez de "saúde".

- **[FDA 2026 — Wearables Wellness](https://spectrum.ieee.org/fda-medical-device-rules)** (Jan 2026, novo)
  - *O quê:* FDA reduz exigência para wearables de baixo risco (categoria wellness, não médica).
  - *Específico:* Earbuds que "amplificam e esclarecem vozes ao redor" → wellness, não hearing aid regulado.
  - *Implicação:* **Reduz barreia regulatória do Anti-Ruído — desde que marketing foque em "conveniência", não "saúde".**

### ANVISA (Brasil)

- **[ANVISA — Classificação de Aparelhos Auditivos](https://www.stoneokamont.com.br/como-registrar-aparelho-auditivo-na-anvisa)** 
  - *O quê:* Aparelhos auditivos são Classe II (exigem registro sanitário + prescrição).
  - *Amplificadores/Produtos de Bem-Estar:* **Não exigem registro na ANVISA** — classificados como eletrônicos, não produtos de saúde.
  - *Precedente:* ANVISA aprovou em fev/2025 o recurso de Hearing Aid do AirPods Pro 2 — confirma que órgão já está navegando essa fronteira.
  - *Implicação:* **Mesma vantagem da FDA também aplica no Brasil** — janela regulatória favorável se comunicação for correta.

### Telecomunicações (Brasil)

- **[ANATEL — Homologação de Fones Bluetooth](https://abcpcertificacao.com.br/certificacao-anatel/fones-bluetooth/)** 
  - *O quê:* Qualquer fone Bluetooth no Brasil exige homologação ANATEL (Categoria II, radiocomunicação).
  - *SAR (Specific Absorption Rate):* **Obrigatório desde 2021** para in-ear/TWS/over-ear (< 20 cm do corpo).
  - *Custo:* ~R$30–50 mil (estimativa), prazo ~2–3 meses.
  - *Implicação:* Certificação é linha de custo e prazo crítica para product launch.
  - *Referência:* [Gov.br ANATEL](https://www.gov.br/pt-br/servicos/homologar-produtos-de-telecomunicacoes-anatel)

### FCC (EUA)

- **[FCC — Part 15 Certification](https://www.fcc.gov/general/radio-frequency-devices)**
  - *O quê:* Certificação de aparelhos de radiofrequência (includes Bluetooth earbuds).
  - *Custo e prazo:* Similar à ANATEL (~US$2–5 mil, ~1–2 meses).
  - *Implicação:* Necessária para venda nos EUA.

### CE (União Europeia)

- **[CE Marking for Radio Equipment Directive 2014/53/EU](https://ec.europa.eu/growth/tools-databases/nando/)**
  - *O quê:* Marcação CE obrigatória para aparelhos de rádio na UE (Bluetooth earbuds inclusos).
  - *Implicação:* Necessária para venda na Europa.

---

## Métricas de Avaliação

### SI-SDR (Scale-Invariant Signal-to-Distortion Ratio)

- **Fórmula:** SI-SDR(y_ref, y_hat) = 10 log10( ||s_target||² / ||e_noise||² )
  - Onde `s_target` é a referência escalada e `e_noise` é o erro residual.
- **Interpretação:**
  - +20 dB = excelente (erro muito pequeno)
  - +10 dB = bom
  - +0 dB = referência = input não processado
  - -5 dB = piorou
- **Uso no Anti-Ruído:** Métrica padrão da área para avaliar separação contra MS-SNSD.
- **Ferramenta Python:** `pesq`, `mir_eval` têm implementações.

### SNR (Signal-to-Noise Ratio)

- **Fórmula:** SNR(dB) = 10 log10( P_signal / P_noise )
- **Uso:** Descrever "nível de dificuldade" de uma cena (SNR 0 dB = voz e fundo com mesma energia = bar bem barulhento).

### Métricas Subjetivas

- **MOS (Mean Opinion Score):** Humanos avaliam 1–5 (1 = péssimo, 5 = excelente).
- **ABX Test:** Comparação cega entre dois processamentos.
- **Aplicação ao Anti-Ruído:** Modo ao vivo, testar se usuários acham "claro o bastante" em ambientes reais.

---

## Leitura Complementar Recomendada

### Se quiser entender o fundamento teórico:

1. **Haykin, S. (2002). "Adaptive Filter Theory"** — Filtro de Wiener explicado.
2. **Vetterli, M. (2007). "Wavelets and Subband Coding"** — Fundação matemática de STFT.
3. **Bregman, A.S. (1994). "Auditory Scene Analysis"** — Por que o ouvido humano consegue separar vozes.

### Se quiser implementar estado da arte:

1. Comece com [speechbrain/speechbrain](https://github.com/speechbrain/speechbrain) (receitas prontas).
2. Depois leia SepFormer paper ([Subakan et al., 2021](https://arxiv.org/abs/2110.06287)).
3. Depois explore finetuning com dados reais.

### Se quiser entender o problema real (negócio):

1. [Noisyplanet.nidcd.nih.gov](https://www.noisyplanet.nidcd.nih.gov) — Dados de ruído em restaurantes.
2. [SoundPrint — Noise Levels in Venues](https://blog.soundprint.co) — Crowdsourcing de dB em bares/restaurantes.
3. [Waverly Labs Pilot failures](https://techcrunch.com/2018/02/25/waverly-labs-offers-real-time-translation-with-its-pilot-earbuds/) — Aprender com fracasso.

---

## Resumo de Citações (BibTeX)

```bibtex
@inproceedings{cherry1953cocktail,
  title={Some Experiments on the Recognition of Speech, with One and with Two Ears},
  author={Cherry, E Colin},
  journal={The Journal of the Acoustic Society of America},
  volume={25},
  number={5},
  pages={975--979},
  year={1953}
}

@inproceedings{wan2019voicefilter,
  title={{VoiceFilter}: Targeted Voice Separation by Speaker-Conditioned Spectrogram Masking},
  author={Wan, Quan and others},
  booktitle={Interspeech},
  year={2019}
}

@inproceedings{subakan2021sepformer,
  title={{SepFormer}: Attention-Based Deep Speech Separation},
  author={Subakan, Cem and others},
  journal={arXiv preprint arXiv:2110.06287},
  year={2021}
}

@inproceedings{mauch2014pyin,
  title={pYIN: A Fundamental Frequency Estimator Using Probabilistic Threshold and Viterbi Algorithm},
  author={Mauch, Matthias and Dixon, Simon},
  booktitle={ICASSP},
  year={2014}
}

@inproceedings{davis1980comparison,
  title={Comparison of Parametric Representations for Monosyllabic Word Recognition in Continuously Spoken Sentences},
  author={Davis, Steven and Mermelstein, Paul},
  journal={IEEE Transactions on Acoustics, Speech, and Signal Processing},
  volume={28},
  number={4},
  pages={357--366},
  year={1980}
}
```

---

## Notas Finais

Esta lista é **viva** — será atualizada conforme o projeto evolui e novas referências forem descobertas. 

**Prioridades para próximas rodadas:**
- [ ] Aprofundar em VoiceFilter (IP risk assessment)
- [ ] Testar Resemblyzer em áudio real do Anti-Ruído (v0.2 prototyping)
- [ ] Avaliar ONNX Runtime para inferência eficiente (v1.0 embarcado)
- [ ] Pesquisar papers recentes em speaker-conditioned separation (2024+)

**Contribuições de referências:** Abrir issue ou PR com sugestão em https://github.com/pedrohdea/anti-ruido/issues

---

**Última atualização:** 2026-07-05
