# Anti-Ruído — Documento Vivo de Validação de Negócio

> **Status do loop de pesquisa:** Próxima rodada: **3** (Personas + Jobs To Be Done) · Rodadas concluídas: 2/54 · Prazo do loop: até 2026-07-04 ~11:00 UTC (08:00 BRT)
> Este documento é atualizado automaticamente a cada rodada (~10 min) durante o Startup Weekend. Cada rodada foca em um ângulo/metodologia diferente — ver seção "Metodologia deste documento" no final.

## Resumo executivo (one-liner)

**Anti-Ruído** é um fone de ouvido de consumo (B2C) que usa cancelamento de ruído adaptativo (ANC) combinado com **extração seletiva de voz** (isolar a voz de quem está na sua frente, mesmo em ambientes muito barulhentos) para permitir conversas claras em bares, restaurantes, eventos, transporte público e ruas — algo que hoje só existe de forma parcial (Apple, reativo ao próprio usuário) ou fora do alcance do consumidor casual (Orosound, B2B/corporativo).

*(Este resumo será revisado nas últimas rodadas do loop, à medida que a validação avança.)*

## Changelog

- **Rodada 1** (Lean Canvas + concorrência direta de hardware): documento criado; Lean Canvas preenchido; panorama competitivo com 8 concorrentes/referências mapeados; estado da arte tecnológico inicial mapeado; README atualizado com o escopo real do produto.
- **Rodada 2** (SWOT + PESTEL): preenchido SWOT e PESTEL. Achado importante: a FDA emitiu em 6/jan/2026 nova orientação que **facilita o enquadramento de earbuds que "amplificam e esclarecem vozes ao redor" como dispositivo de bem-estar (wellness)**, não como aparelho auditivo médico — reduz o risco regulatório identificado na rodada 1. Também mapeado: mercado de vida noturna/eventos ao vivo e dados de perda auditiva induzida por ruído em jovens.

## 1. Problema e evidência

**Problema central:** em ambientes com ruído ambiente alto (>75-85 dB — nível típico de bares, restaurantes lotados, shows, estações de transporte), a inteligibilidade da fala cai drasticamente mesmo para quem tem audição normal. As pessoas recorrem a gritar, aproximar o rosto, usar leitura labial informal ou simplesmente desistir da conversa.

**Casos de uso concretos (hipóteses a validar com entrevistas reais pós-evento):**
- Bar/balada: conversar com um amigo específico em meio à música alta e outras conversas.
- Restaurante lotado: conversa de trabalho ou encontro em ambiente com ruído de talheres, outras mesas, cozinha.
- Transporte público (metrô, ônibus, aeroporto): entender ligações ou conversas presenciais com ruído mecânico constante.
- Eventos/shows/feiras: conversar perto do palco ou em corredores lotados.
- Rua/trânsito: pedestres conversando perto de tráfego intenso.

**Evidência indireta já encontrada (pesquisa secundária, rodada 1):**
- A Apple considerou o problema relevante o suficiente para lançar **Conversation Awareness** (abaixa mídia e realça vozes quando o usuário fala) e **Adaptive Audio** nos AirPods Pro — sinal de que grandes players já validaram que "conversar com fone no ouvido em ambiente ruidoso" é uma dor real de mercado. Fonte: [Apple Support – Adaptive Audio](https://support.apple.com/en-us/104979), [Apple Newsroom 2023](https://www.apple.com/newsroom/2023/06/airpods-redefine-the-personal-audio-experience/).
- A Waverly Labs documentou publicamente que seu tradutor Pilot **falha em ambientes ruidosos como bares/cafeterias** porque a captação de voz é atrapalhada por outras pessoas falando — evidência de que o problema específico (isolar 1 voz-alvo em ambiente com múltiplas fontes sonoras) ainda não está resolvido de forma satisfatória. Fonte: [TechCrunch](https://techcrunch.com/2018/02/25/waverly-labs-offers-real-time-translation-with-its-pilot-earbuds/), [Wareable](https://www.wareable.com/hearables/waverly-labs-pilot-review).
- Existe literatura acadêmica de décadas sobre o **"cocktail party problem"** (como o cérebro humano isola uma voz entre várias) — o fato de ser um problema de pesquisa ativo e batizado confirma que é um problema real e difícil, não trivial. Ver seção 9 (Tecnologia).

*(Validação direta com usuários — entrevistas, pesquisa de campo — está fora do escopo deste evento por falta de tempo; ver seção 18, Roadmap pós-evento.)*

## 2. Lean Canvas

Formato oficial usado no Startup Weekend / Techstars Entrepreneur's Toolkit (Ash Maurya). Fonte: [Techstars Entrepreneur's Toolkit – Lean Canvas](https://toolkit.techstars.com/build-your-lean-canvas).

| Bloco | Conteúdo |
|---|---|
| **Customer Segments** | Jovens adultos urbanos (18-35) que frequentam bares, baladas, restaurantes e eventos com frequência; viajantes/passageiros de transporte público; secundariamente, pessoas com perda auditiva leve não diagnosticada (mercado adjacente, ver seção 7 e rodada 9) |
| **Problem** | 1) Difícil conversar em ambientes ruidosos (bares, restaurantes, eventos, transporte); 2) Soluções atuais de ANC cancelam ruído mas não "trazem" a voz do interlocutor de forma seletiva e sob controle do usuário; 3) Alternativas existentes (Apple, Orosound) são reativas/genéricas ou voltadas a B2B, não a um consumidor casual que escolhe uma pessoa específica para ouvir |
| **Unique Value Proposition** | "Converse com clareza em qualquer lugar, por mais barulhento que seja" — um fone que deixa você escolher literalmente **ouvir uma pessoa específica** acima do caos sonoro ao redor, algo que hoje nenhum produto de consumo massificado faz de forma dedicada e simples |
| **Solution** | Fone com ANC + microfones direcionais/beamforming + processamento (on-device ou app) de extração seletiva de voz + geração de ruído branco adaptativo ao nível/perfil espectral do ambiente *(não será construído neste evento — apenas conceito a validar)* |
| **Channels** | Pré-venda via crowdfunding (Kickstarter/Indiegogo — padrão de mercado para hearables, ver rodada 4), redes sociais/influenciadores de tecnologia e vida noturna, parcerias com casas de eventos (ver rodada 24), D2C via e-commerce próprio |
| **Revenue Streams** | Venda de hardware (preço-alvo a validar na rodada 4/37, referências de mercado entre US$150-300 — abaixo de Bose/Sony premium, acima da faixa sub-US$50 genérica); possível add-on de assinatura de app para perfis de voz/ambientes personalizados (a validar) |
| **Cost Structure** | P&D (algoritmos de ML para extração de voz, ou licenciamento de tecnologia existente), fabricação (ODM/OEM de earbuds), certificações regulatórias (ver rodada 20), marketing de lançamento, suporte |
| **Key Metrics** | Taxa de sucesso de isolamento de voz-alvo em teste subjetivo; intenção de compra pré-venda (%); CAC e conversão de campanha de crowdfunding; NPS pós-uso em ambiente ruidoso real |
| **Unfair Advantage** | A definir — hoje **nenhuma vantagem defensável comprovada ainda existe** (ponto crítico de risco, ver seção 15). Candidatos a explorar: foco explícito em B2C casual/social (gap deixado por Orosound, que é B2B), possível parceria com pesquisa acadêmica aberta (ex.: técnicas tipo "Semantic Hearing" da U. Washington, código aberto), ou velocidade de execução/marca antes de incumbentes reagirem |

## 3. Value Proposition Canvas

*Pendente — Rodada 6.*

## 4. Jobs To Be Done

*Pendente — Rodada 3.*

## 5. Personas e segmentação

*Pendente — Rodada 3.*

## 6. Panorama competitivo

| Concorrente | Categoria | Tecnologia relevante | Preço aprox. | Gap / oportunidade |
|---|---|---|---|---|
| **Apple AirPods Pro 2/3, AirPods Max 2** | Consumer ANC premium | "Adaptive Audio" (mistura dinâmica Transparency/ANC) + "Conversation Awareness" (abaixa mídia e realça vozes quando **o próprio usuário** fala) | ~US$250 (Pro) | Reativo à fala do próprio usuário, não permite escolher/isolar a voz de **outra pessoa** específica |
| **Sony WH-1000XM6** | Consumer ANC premium | Processador QN3, 12 microfones, "Adaptive NC Optimizer" ajusta ao ambiente continuamente | ~US$400+ | Foco em cancelar ruído, não em isolar voz de terceiros |
| **Bose QuietComfort Ultra (2ª gen)** | Consumer ANC premium | Modo "Aware" deixa ruído/conversas entrarem, sem separação seletiva | ~US$430 | Sem isolamento seletivo de voz-alvo |
| **Orosound Tilde (Pro/Evo/Air)** | B2B office/contact center | "TILDE VOICE FIRST" — separação de voz por IA (>1M parâmetros) + recurso "F2F" (face-to-face) prioriza voz de quem está à frente, -30dB de ruído, até 6 microfones dedicados a voz | Enterprise (não divulgado ao consumidor) | **Concorrente tecnicamente mais próximo** — mas 100% posicionado B2B/escritório, não para uso social/casual. Gap: ninguém leva essa tecnologia para o consumidor em bares/eventos |
| **Nuheara IQbuds² MAX** | Hearable / PSAP (amplificação pessoal, não hearing aid oficial) | Ear ID (calibração via app), ANC + amplificação personalizada para ambientes difíceis | — | **Empresa entrou em liquidação/recuperação judicial em 2023** — sinal de alerta sobre dificuldade de viabilidade comercial no nicho |
| **Jabra Enhance (Select 500/700)** | Hearing aid OTC | "SoundScape" para clareza de fala + cancelamento de ruído | US$995–1995/par | Referência de preço para dispositivo "premium hearing", mas é categoria médica regulada (ver seção 15) |
| **Waverly Labs Pilot** | Tradutor em tempo real | Captação de voz via earbuds | — | Falha documentada em ambientes ruidosos (bares/cafés) — validação de que o problema não está resolvido nem por quem tentou algo adjacente |
| **Doppler Labs (Here One)** — descontinuado | Smart earbuds "hearables" | Áudio aumentado/personalizável | Levantou US$50M+ | **Caso de fracasso**: vendeu só ~25 mil unidades (esperava 100 mil+), bateria fraca, mercado saturado por AirPods/Galaxy Buds, fechou em 2017 sem conseguir Série C — lição de risco de mercado (ver seção 15) |
| **Krisp.ai "Voice Isolation"** (software, não hardware) | App/SDK para chamadas | Remove ruído de fundo E outras vozes, mantém só o falante, deep learning local, integra Zoom/Meet/Teams | Assinatura de app | Prova que a tecnologia de "isolar 1 voz entre várias" já funciona bem em laptop/celular — a incógnita é rodar isso em tempo real, baixa latência, num chip pequeno de earbud com bateria limitada |

**Leitura estratégica (rascunho, a refinar na rodada 6 com Blue Ocean Canvas):** o único concorrente que já resolve tecnicamente um problema parecido (Orosound) deliberadamente não vai para o consumidor casual. Os grandes de consumo (Apple/Sony/Bose) resolvem parcialmente (reativo ao próprio usuário, não seletivo a terceiros). Isso sugere um espaço não disputado (*"ruído branco adaptativo + escolha de voz-alvo, para uso social casual"*) — mas o histórico de Doppler Labs/Nuheara mostra que esse nicho já teve tentativas fracassadas, o que exige cuidado extra em unit economics e proposta de valor muito clara (ver riscos, seção 15).

## 7. Tecnologia existente / estado da arte

*(Mapeamento do que já existe — sem entrar em como construir a solução neste evento.)*

- **ANC ativo tradicional**: cancelamento de ruído de baixa frequência via microfones feedforward/feedback — commodity hoje, presente até em fones sub-US$50.
- **"Adaptive Transparency" / modos híbridos**: Apple e Sony já ajustam dinamicamente entre ANC e transparência conforme o ambiente muda.
- **Beamforming multi-microfone**: usado pela Orosound (até 6 mics dedicados a voz) para captar direcionalmente a voz de quem está à frente.
- **Target Speaker Extraction / "Cocktail Party Problem"**: linha de pesquisa estabelecida que distingue *blind speech separation* (separar todas as vozes sem saber quantas existem) de *target speaker extraction* (usar uma amostra de referência da voz-alvo para extraí-la). Já existe patente registrada nessa área (US 10923136, prioridade 2018) — sinaliza espaço de propriedade intelectual já ocupado, risco a mapear na rodada 5. Fonte: [ResearchGate](https://www.researchgate.net/publication/266462837_Target_speech_extraction_in_cocktail_party_by_combining_beamforming_and_blind_source_separation).
- **"Semantic Hearing" (Universidade de Washington, UIST 2023)**: rede neural (transformer) que extrai binauralmente um som-alvo dentre 20 classes (incluindo "speech") em tempo real, rodando em 6.56ms num smartphone conectado a fones binaurais — código aberto disponível. É o projeto acadêmico mais próximo conceitualmente da ideia. Fontes: [Paper (UIST 2023)](https://dl.acm.org/doi/10.1145/3586183.3606779), [GitHub](https://github.com/vb000/SemanticHearing), [UW News](https://www.washington.edu/news/2023/11/09/ai-noise-canceling-headphones/).
- **ClearBuds**: fones binaurais wireless com "learning-based speech enhancement" (arXiv 2206.13611) — outra referência acadêmica relevante.
- **Krisp.ai Voice Isolation**: já citado na seção 6 — prova de conceito em software (laptop/celular) de isolar 1 voz entre várias.

**Pergunta em aberto para rodadas futuras (5 e 35):** qual a viabilidade de rodar um modelo do tipo "Semantic Hearing"/"target speaker extraction" **on-device**, dentro do orçamento de energia e DSP de um earbud (não um smartphone), com latência aceitável para conversação (<20ms) — hoje a demonstração mais avançada roda no smartphone, não no próprio fone.

## 8. SWOT

| | |
|---|---|
| **Forças (Strengths)** | Posicionamento claramente diferenciado de todos os concorrentes mapeados (B2C casual/social, nenhum incumbente ocupa esse espaço hoje); existe prova acadêmica de conceito tecnicamente próximo e aberta (Semantic Hearing/UW, código no GitHub); Krisp.ai já prova que "isolar 1 voz entre várias" funciona bem em software, reduzindo a incerteza de que o problema é solucionável em algum dispositivo |
| **Fraquezas (Weaknesses)** | Nenhuma vantagem defensável (Unfair Advantage) comprovada ainda (canvas, seção 2); nenhum protótipo ou validação técnica de extração de voz rodando *on-device* em earbud (hoje só demonstrado em smartphone); zero histórico de marca/confiança no nicho de áudio |
| **Oportunidades (Opportunities)** | FDA (EUA) publicou em 6/jan/2026 nova diretriz que trata earbuds que "amplificam e esclarecem vozes ao redor" como dispositivo de bem-estar, não aparelho auditivo regulado — **reduz risco regulatório** de forma relevante; mercado de hearables crescendo (US$55,8B em 2025 → US$62,2B em 2026 → US$107,1B em 2031, CAGR 11,47%); mercado de música ao vivo nos EUA em forte crescimento (US$18,51B em 2025 → US$19,7B em 2026, CAGR 6,45%) com Gen Z gastando US$2.100+ em 2 anos em shows — público dispensado a pagar por experiências, público-alvo plausível |
| **Ameaças (Threats)** | Jovens <25 anos respondem por só ~8,1% do gasto em bares/baladas (tendência de beber menos) — pode estreitar o público-alvo ideal para frequentadores de eventos/shows em vez do "jovem de balada" genérico; incumbentes (Apple/Sony/Bose) podem estender recursos parecidos via firmware sem novo hardware; ~1 em cada 5 adultos de 20-29 anos já apresenta dano auditivo induzido por ruído — pode ser vento a favor (ângulo de proteção auditiva) ou ameaça (se o produto for lido como alegação de saúde, reabre risco regulatório) |

Fontes desta rodada: [Bars & Nightclubs Market 2025-2026](https://www.mmcginvest.com/post/u-s-bars-nightclubs-industry-market-trends-valuations-outlook-for-investors), [US Live Music Market – Mordor Intelligence](https://www.mordorintelligence.com/industry-reports/united-states-live-music-market), [NIHL statistics – Nagish](https://nagish.com/post/noise-induced-hearing-loss-statistics), [CDC MMWR – Noise-Induced Hearing Loss Among Adults](https://www.cdc.gov/mmwr/volumes/66/wr/mm6605e3.htm).

## 9. PESTEL

| Fator | Achado |
|---|---|
| **Político** | FDA (EUA) emitiu em 6/jan/2026 novas diretrizes que reduzem a exigência regulatória para wearables/dispositivos de "wellness" de baixo risco, incluindo esclarecimento específico sobre earbuds que amplificam/esclarecem vozes — tendência política favorável nos EUA. Equivalente brasileiro (ANVISA) ainda não pesquisado — pendente para rodada futura. |
| **Econômico** | Mercado global de bares/baladas ~US$78-105B (2025-2026); música ao vivo nos EUA ~US$18,5-19,7B (2025-2026), crescendo 6,45% a.a.; mercado de hearables ~US$62,2B (2026) crescendo 11,47% a.a. até 2031 |
| **Social** | Cultura de "economia da experiência" pós-pandemia impulsiona gasto em eventos ao vivo, mesmo com jovens <25 bebendo/frequentando bares menos; consciência sobre perda auditiva induzida por ruído entre jovens ainda é baixa apesar de ~1 em 5 (20-29 anos) já ter dano mensurável |
| **Tecnológico** | Convergência de processamento de áudio avançado + IA + sensores biométricos está transformando hearables de "acessório de áudio simples" em "plataforma de computação vestível multifuncional" (Mordor Intelligence) — tendência favorável ao conceito do produto |
| **Ambiental** | Pendente — a aprofundar na rodada 29 (sustentabilidade/ESG: baterias, e-waste de eletrônicos vestíveis) |
| **Legal** | A nova diretriz da FDA (jan/2026) é o fator legal mais relevante encontrado até agora: ajuda a diferenciar produtos "wellness" (não regulados) de aparelhos auditivos convencionais regulados — favorece diretamente o posicionamento do Anti-Ruído como produto de conveniência/comunicação, não como dispositivo médico, desde que a comunicação de marketing evite alegações de "tratar perda auditiva" |

Fontes desta rodada: [IEEE Spectrum – FDA 2026 Update for Wearables](https://spectrum.ieee.org/fda-medical-device-rules), [ConsumerAffairs – FDA relaxes rules for wearable health devices](https://www.consumeraffairs.com/news/fda-relaxes-rules-for-wearable-health-devices-010726.html), [STAT News – FDA pulls back oversight of AI-enabled devices/wearables](https://www.statnews.com/2026/01/06/fda-pulls-back-oversight-ai-enabled-devices-wearables/), [Mordor Intelligence – Hearables Market 2026-2031](https://www.mordorintelligence.com/industry-reports/hearables-market).

## 10. Porter's Five Forces

*Pendente — Rodada 7.*

## 11. Blue Ocean Strategy Canvas

*Pendente — Rodada 6.*

## 12. Modelo de receita e pricing

*Pendente — Rodada 4 (aprofundado na rodada 37).*

Referências de preço já coletadas (rodada 1): AirPods Pro ~US$250; Bose QC Ultra ~US$430; Sony XM6 ~US$400+; Jabra Enhance (hearing aid OTC) US$995-1995; faixa sub-US$50 é o segmento de ANC que mais cresce (~21%+ CAGR) — sinaliza pressão de comoditização de preço na entrada.

## 13. Riscos

**Riscos identificados na rodada 1 (aprofundamento de mitigação na rodada 32):**

- **Técnico**: extrair voz-alvo em tempo real com baixa latência e baixo consumo de energia num chip de earbud (não num laptop) é território de pesquisa, não tecnologia "de prateleira" pronta — maior incerteza técnica do projeto.
- **Regulatório**: a FDA oficializou em 2022 a categoria de **OTC Hearing Aids** (Bose, Jabra e o recurso "Hearing Aid" do AirPods Pro 2 já certificados). Qualquer alegação de "melhorar audição" (não só cancelar ruído) pode enquadrar o produto como dispositivo médico regulado, com exigências técnicas (ex.: limite de 111 dB SPL) e de rotulagem. Fonte: [FDA – OTC Hearing Aids](https://www.fda.gov/medical-devices/hearing-aids/otc-hearing-aids-what-you-should-know), [Federal Register 2022](https://www.federalregister.gov/documents/2022/08/17/2022-17230/medical-devices-ear-nose-and-throat-devices-establishing-over-the-counter-hearing-aids). **Atualização (rodada 2, jan/2026):** a FDA publicou nova diretriz que trata earbuds que "amplificam e esclarecem vozes ao redor" como dispositivo de bem-estar (wellness), não aparelho auditivo regulado — **reduz esse risco**, desde que o marketing evite alegações de "tratar perda auditiva". Fonte: [IEEE Spectrum](https://spectrum.ieee.org/fda-medical-device-rules), [STAT News](https://www.statnews.com/2026/01/06/fda-pulls-back-oversight-ai-enabled-devices-wearables/). Ainda pendente: equivalente da ANVISA no Brasil.
- **Mercado**: dois precedentes diretos de fracasso comercial em hearables "inteligentes" — **Doppler Labs** (levantou US$50M+, fechou em 2017) e **Nuheara** (liquidação em 2023). Ambos mostram que hardware de áudio "smart" tem histórico de dificuldade de tração e unit economics.
- **Propriedade intelectual**: já existe pelo menos uma patente registrada (US 10923136) em técnica de extração de fala-alvo supervisionada — o espaço de IP não está vazio; aprofundar busca de patentes na rodada 5.
- **Competitivo**: Apple, Sony e Bose têm recursos (Adaptive Audio, Conversation Awareness, Adaptive NC Optimizer) que já endereçam parte do problema e poderiam estender via **atualização de firmware** para competir diretamente, sem precisar de novo hardware — barreira de entrada baixa para incumbentes reagirem (aprofundar na rodada 7 e 30).

## 14. Métricas-chave / North Star Metric / AARRR

*Pendente — Rodada 8.*

## 15. OKRs de validação

*Pendente — Rodada 10.*

## 16. Roadmap de validação pós-evento

*Pendente — Rodada 38.*

## 17. Pitch de 60s e pitch de 5min

*Pendente — Rodada 10 (refinado na rodada 42/54).*

## 18. Resumo de requisitos para sucesso

*Pendente — consolidado na rodada 42.*

## 19. Log de fontes (Rodada 1)

- [Techstars Entrepreneur's Toolkit – Lean Canvas](https://toolkit.techstars.com/build-your-lean-canvas)
- [The Ultimate Guide to Winning Startup Weekend](https://medium.com/code-without-code/the-ultimate-guide-to-winning-startup-weekend-6a6a92ec23b2)
- [Techstars – How pitches work](https://www.techstars.com/communities/startup-weekend/facilitate-a-startup-weekend/event-logistics/how-pitches-work)
- [What is it with the Startup Weekend Pitch?](https://www.venturecentre.io/blog/post/55973/what-is-it-with-the-startup-weekend-pitch/)
- [Apple Support – Adaptive Audio](https://support.apple.com/en-us/104979)
- [Apple Newsroom 2023](https://www.apple.com/newsroom/2023/06/airpods-redefine-the-personal-audio-experience/)
- [SoundGuys – Sony WH-1000XM6 vs Bose QC Ultra](https://www.soundguys.com/sony-wh-1000xm6-vs-bose-quietcomfort-ultra-heavyweights-137869/)
- [What Hi-Fi – Sony vs Bose comparativo](https://www.whathifi.com/headphones/wireless-headphones/sony-wh-1000xm6-vs-bose-quietcomfort-ultra-headphones-2nd-gen-which-flagship-wireless-over-ears-are-best)
- [Orosound Tilde Pro](https://www.orosound.com/office-headphones-tilde-pro-2/)
- [Orosound Tilde Air](https://www.orosound.com/tilde-earphones/)
- [Nuheara IQbuds² MAX](https://www.nuheara.com/usa/products/iqbuds-max/)
- [HearingTracker – Nuheara review](https://www.hearingtracker.com/hearing-aids/nuheara-iqbuds-max)
- [Jabra Enhance](https://www.jabraenhance.com/)
- [NCOA – Jabra Enhance review](https://www.ncoa.org/product-resources/hearing-aids/jabra-enhance-review/)
- [TechCrunch – Waverly Labs Pilot](https://techcrunch.com/2018/02/25/waverly-labs-offers-real-time-translation-with-its-pilot-earbuds/)
- [Wareable – Waverly Labs Pilot review](https://www.wareable.com/hearables/waverly-labs-pilot-review)
- [TechCrunch – Doppler Labs shuts down](https://techcrunch.com/2017/11/01/smart-earbuds-startup-doppler-labs-shuts-down-after-raising-50m/)
- [Wareable – Why Doppler Labs shut down](https://www.wareable.com/hearables/why-doppler-labs-shut-down-interview-932)
- [Krisp.ai – Voice Isolation](https://krisp.ai/noise-cancellation/)
- [Krisp.ai – Voice Isolation docs](https://help.krisp.ai/hc/en-us/articles/5356050927644-Voice-Isolation-with-Krisp)
- [Semantic Hearing paper (UIST 2023)](https://dl.acm.org/doi/10.1145/3586183.3606779)
- [Semantic Hearing GitHub](https://github.com/vb000/SemanticHearing)
- [UW News – AI noise-canceling headphones](https://www.washington.edu/news/2023/11/09/ai-noise-canceling-headphones/)
- [Target speech extraction research](https://www.researchgate.net/publication/266462837_Target_speech_extraction_in_cocktail_party_by_combining_beamforming_and_blind_source_separation)
- [Patente USPTO 10923136](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10923136)
- [FDA – OTC Hearing Aids](https://www.fda.gov/medical-devices/hearing-aids/otc-hearing-aids-what-you-should-know)
- [Federal Register – Final Rule 2022](https://www.federalregister.gov/documents/2022/08/17/2022-17230/medical-devices-ear-nose-and-throat-devices-establishing-over-the-counter-hearing-aids)
- [Mordor Intelligence – Hearables Market](https://www.mordorintelligence.com/industry-reports/hearables-market)
- [Research and Markets – ANC Headphones Market](https://www.researchandmarkets.com/report/global-active-noise-cancelling-headphone-market)

**Rodada 2:**
- [Nagish – Noise-Induced Hearing Loss Statistics](https://nagish.com/post/noise-induced-hearing-loss-statistics)
- [CDC MMWR – Noise-Induced Hearing Loss Among Adults 2011-2012](https://www.cdc.gov/mmwr/volumes/66/wr/mm6605e3.htm)
- [MDPI – NIHL Awareness in Young Adults 18-30, Greece](https://www.mdpi.com/2039-4349/15/6/171)
- [MMCG – US Bars & Nightclubs Industry 2025](https://www.mmcginvest.com/post/u-s-bars-nightclubs-industry-market-trends-valuations-outlook-for-investors)
- [Mordor Intelligence – US Live Music Market](https://www.mordorintelligence.com/industry-reports/united-states-live-music-market)
- [Coherent Market Insights – US Live Events Market](https://www.coherentmarketinsights.com/industry-reports/us-live-events-market)
- [IEEE Spectrum – What the FDA's 2026 Update Means for Wearables](https://spectrum.ieee.org/fda-medical-device-rules)
- [ConsumerAffairs – FDA relaxes rules for wearable health devices](https://www.consumeraffairs.com/news/fda-relaxes-rules-for-wearable-health-devices-010726.html)
- [STAT News – FDA pulls back oversight of AI-enabled devices/wearables](https://www.statnews.com/2026/01/06/fda-pulls-back-oversight-ai-enabled-devices-wearables/)
- [Mordor Intelligence – Hearables Market 2026-2031](https://www.mordorintelligence.com/industry-reports/hearables-market)

---

## Metodologia deste documento

Este documento é mantido por um loop automatizado de pesquisa (~10 min por rodada, ~54 rodadas ao longo de ~9h), rodando durante o Startup Weekend, com o objetivo de aplicar metodologias reais de criação/validação de startup (Lean Canvas, SWOT, PESTEL, Porter's Five Forces, Blue Ocean Strategy, Value Proposition Canvas, Jobs To Be Done, AARRR, OKRs) à ideia do fone Anti-Ruído, e mapear tudo que for encontrável por pesquisa sobre concorrência, tecnologia, mercado, regulação e riscos — sem ainda construir a solução técnica. Cada rodada pesquisa fontes novas e reais (citadas inline e na seção 19), atualiza apenas as seções do seu ângulo, e evita repetir buscas já feitas. Fases do loop:

- **Fase A (rodadas 1-10)**: fundamentos de validação (Lean Canvas, SWOT/PESTEL, personas/JTBD, pricing, riscos técnicos/IP, VPC/Blue Ocean, Porter, AARRR, mercado adjacente, OKRs/pitch).
- **Fase B (rodadas 11-20)**: teardown competitivo e finanças aprofundadas.
- **Fase C (rodadas 21-30)**: go-to-market e organização.
- **Fase D (rodadas 31-42)**: síntese, mitigação de risco e consolidação.
- **Fase E (rodadas 43-54)**: polimento final e reforço das seções mais fracas.
