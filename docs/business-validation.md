# Anti-Ruído — Documento Vivo de Validação de Negócio

> **Status do loop de pesquisa:** Próxima rodada: **31** (síntese e revisão cruzada) · Rodadas concluídas: 30/54 · Execução: a pedido do usuário, as 54 rodadas estão sendo executadas em sequência (sem esperar os 10 min entre cada uma); ao final, uma rodada extra de reavaliação/melhorias será feita.
> Este documento é atualizado automaticamente a cada rodada (~10 min) durante o Startup Weekend. Cada rodada foca em um ângulo/metodologia diferente — ver seção "Metodologia deste documento" no final.

## Resumo executivo (one-liner)

**Anti-Ruído** é um fone de ouvido de consumo (B2C) que usa cancelamento de ruído adaptativo (ANC) combinado com **extração seletiva de voz** (isolar a voz de quem está na sua frente, mesmo em ambientes muito barulhentos) para permitir conversas claras em bares, restaurantes, eventos, transporte público e ruas — algo que hoje só existe de forma parcial (Apple, reativo ao próprio usuário) ou fora do alcance do consumidor casual (Orosound, B2B/corporativo).

*(Este resumo será revisado nas últimas rodadas do loop, à medida que a validação avança.)*

## Changelog

- **Rodada 1** (Lean Canvas + concorrência direta de hardware): documento criado; Lean Canvas preenchido; panorama competitivo com 8 concorrentes/referências mapeados; estado da arte tecnológico inicial mapeado; README atualizado com o escopo real do produto.
- **Rodada 2** (SWOT + PESTEL): preenchido SWOT e PESTEL. Achado importante: a FDA emitiu em 6/jan/2026 nova orientação que **facilita o enquadramento de earbuds que "amplificam e esclarecem vozes ao redor" como dispositivo de bem-estar (wellness)**, não como aparelho auditivo médico — reduz o risco regulatório identificado na rodada 1. Também mapeado: mercado de vida noturna/eventos ao vivo e dados de perda auditiva induzida por ruído em jovens.
- **Rodadas 3-10** (personas/JTBD, pricing, riscos técnicos/IP, VPC, Blue Ocean, Porter, AARRR, mercado adjacente, OKRs/pitch — executadas em sequência a pedido do usuário): definidas 3 personas (frequentador de eventos, profissional viajante, mercado adjacente de perda auditiva leve); JTBD funcional/emocional/social; pricing com sweet spot sugerido US$150-250; achado de risco de IP adicional (patente Google US20220122611A1) mas também campo de pesquisa acadêmica aberta ativa; achado estratégico importante — chipset Qualcomm Snapdragon S7 já comoditiza "background voice rejection" e "context-aware ANC" em silício, baixando barreira técnica de entrada para qualquer concorrente; Blue Ocean Canvas com grade ERRC; AARRR completo com North Star Metric candidata; OKRs de validação para o evento; pitch de 60s e estrutura do pitch de 5min (rascunho).
- **Rodadas 11-20** (teardown competitivo detalhado, modelagem financeira, fundraising, cap table, legal, supply chain, certificações): teardown do Orosound (fundada 2015, 2 patentes, ~US$5,4-39,5M captados conforme a fonte, 100% B2B — confirma gap de 10 anos sem entrar no consumidor); estrutura de custos com BOM estimado ilustrativamente em US$35-70 (a validar com ODM real); fundraising com comparáveis reais (xMEMS, Mira, Hearvana) e alerta de que "connected hearables" recebem só 2,77% do capital de wearables; diretrizes gerais de cap table e legal/societário; supply chain via ODMs de referência Qualcomm QCC; certificação ANATEL **obrigatória** no Brasil (Categoria II + SAR obrigatório desde 2021) adicionada como novo risco regulatório-técnico.
- **Rodadas 21-30** (marca, marketing, lançamento, parcerias, equipe, cultura, métricas híbridas, expansão internacional, ESG, sensibilidade de mercado): estratégia de lançamento comparando crowdfunding/pré-venda/varejo; casos reais de parceria de marcas de fone com vida noturna/artistas (Skullcandy x Budweiser, Sony x Olivia Rodrigo, Bose x NFL) como modelo de canal; mercado brasileiro de wearables (US$1,57B em 2024 → US$4,90B em 2033) sugerindo Brasil como mercado de lançamento inicial plausível; novas leis de e-waste/right-to-repair nos EUA (2025-2026) relevantes para design do produto; análise de sensibilidade confirmando que o cenário de incumbentes copiarem via firmware é plausível no curto-médio prazo.

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

| Perfil do cliente | Proposta de valor |
|---|---|
| **Dores:** gritar/repetir em ambientes barulhentos; cansaço social; sensação de exclusão da conversa; ANC atual cancela ruído mas não resolve isso; estigma de parecer "antissocial" usando fone em grupo | **Aliviadores de dor:** extração seletiva da voz de uma pessoa-alvo + ruído branco adaptado ao ambiente elimina a necessidade de gritar/repetir; ativação simples ("modo conversa") reduz fricção |
| **Ganhos desejados:** conversar com clareza sem esforço; sentir-se presente socialmente; ser percebido como preparado/tecnológico | **Criadores de ganho:** modo social dedicado com ativação rápida (ex. toque duplo/gesto), app simples para calibrar perfil de voz/ambiente |
| **Jobs:** funcional (entender/ser entendido), emocional (sentir-se conectado), social (não parecer isolado) — ver seção 4 | **Produtos/serviços:** fone com ANC + microfones direcionais + extração seletiva de voz + app companion *(conceito, não construído neste evento)* |

## 4. Jobs To Be Done

- **Funcional:** "Quando estou num ambiente muito barulhento, quero entender e ser entendido por uma pessoa específica, para não precisar gritar ou repetir."
- **Emocional:** "Quero me sentir presente/conectado socialmente mesmo em ambientes caóticos, sem a frustração e o constrangimento de pedir para repetir várias vezes."
- **Social:** "Quero parecer preparado e tecnológico usando o fone em público, não 'antissocial' — hoje há estigma de usar fone em contexto social; o produto precisa reverter isso (é uma ferramenta *para* conversar, não para se isolar)."

## 5. Personas e segmentação

| Persona | Perfil | Evidência |
|---|---|---|
| **Frequentador de eventos/shows (early adopter primário)** | Gen Z/Millennial urbano, prioriza "economia da experiência", já gasta em áudio premium | Gen Z gastou US$2.100+ em música ao vivo em 2 anos; mercado de música ao vivo nos EUA crescendo 6,45% a.a. (rodada 2) |
| **Profissional urbano/viajante** | Compra TWS premium (>US$200), valoriza produtividade e clareza em viagens, aeroportos, transporte | Segmento >US$200 nos EUA já vale US$15,42B (37,8% share), crescendo 30,9% CAGR — maior sinal de disposição a pagar por áudio premium |
| **Mercado adjacente: perda auditiva leve não diagnosticada** | Adultos que evitam ambientes ruidosos silenciosamente, sem se identificar como "usuário de aparelho auditivo" | Nos EUA, ~28,8 milhões de adultos se beneficiariam de aparelho auditivo, mas só 16% dos que precisam (20-69 anos) realmente usam um; ~25,4 milhões de pessoas com 12+ anos têm perda auditiva leve (NIDCD) — grande público subatendido, mas requer cuidado regulatório (ver seção 13) |

Fontes desta rodada: [Grand View Research – TWS Earbuds Market](https://www.grandviewresearch.com/industry-analysis/true-wireless-stereo-earbuds-market-report), [Grand View Research – OTC Hearing Aids Market](https://www.grandviewresearch.com/industry-analysis/over-the-counter-hearing-aids-market-report), [The Hearing Review – OTC Hearing Aid Market to Hit $1.16B by 2030](https://hearingreview.com/hearing-products/hearing-aids/otc/otc-hearing-aid-market-to-hit-1-16-billion-by-2030).

**Dimensionamento macro do mercado adjacente (rodada 9, sem virar foco do produto):** globalmente, a OMS estima que **1,5 bilhão de pessoas** vivem com algum grau de perda auditiva, projeção de **2,5 bilhões até 2050**. O mercado de aparelhos auditivos vale US$9,27B (2025) → US$15,11B (2033, CAGR 6,3%); o nicho específico de OTC (sem receita médica) vale US$437,4M (2025) → US$884,1M (2034, CAGR 8,1%). Esses números mostram um mercado adjacente grande e crescente, mas hoje **dimensionado como categoria médica/assistiva**, não como "conveniência social" — reforça que o Anti-Ruído deve se manter posicionado como produto de consumo/conveniência (ver seção 13, risco regulatório) mesmo que parte da demanda futura venha de pessoas com perda auditiva leve não diagnosticada. Fontes: [SkyQuest – Hearing Aid Market](https://www.skyquestt.com/report/hearing-aid-market), [Fortune Business Insights – Hearing Aids Market](https://www.fortunebusinessinsights.com/industry-reports/hearing-aids-market-101573), [GM Insights – OTC Hearing Aids Market](https://www.gminsights.com/industry-analysis/otc-hearing-aids-market).

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

**Teardown — Orosound (rodada 11):** fundada em 2015 em Paris por Eric Benhaim (especialista em IA/processamento de sinal) e Pierre Guiu (veterano de marcas de áudio da Ásia/Europa). Detém **2 patentes** sobre a tecnologia "TILDE VOICE FIRST" (cancelamento de ruído seletivo e direcional), premiada inclusive pelo Ministério da Pesquisa francês. Captação de recursos relatada varia por fonte — Crunchbase indica ~US$5,42M, PitchBook indica ~US$39,5M para a "Orosound Labs" — **discrepância a esclarecer**, mas em qualquer leitura confirma que é uma empresa de porte pequeno/médio, focada 100% em B2B (escritórios/contact centers), sem sinal de intenção de entrar no consumidor casual. Isso reforça a leitura de "gap" para o Anti-Ruído: a tecnologia mais próxima existe, tem 10 anos de maturação e proteção de patente, mas nunca foi endereçada ao consumidor final. Fontes: [Orosound – About Us](https://www.orosound.com/about-us/), [Crunchbase – Orosound](https://www.crunchbase.com/organization/orosound), [PitchBook – Orosound Labs](https://pitchbook.com/profiles/company/125681-14).

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

- **Rivalidade entre concorrentes:** alta — Apple, Sony e Bose dominam com marca, escala e distribuição; Orosound ocupa o nicho tecnicamente mais próximo mas só em B2B.
- **Ameaça de novos entrantes:** moderada-alta. Achado importante desta rodada: os fornecedores de chipset de áudio já estão comoditizando parte da tecnologia-chave — o **Qualcomm Snapdragon S7** (chip de áudio) já inclui NPU dedicado e oferece recursos de IA como **"background voice rejection" e "context-aware ANC"** como funcionalidade de silício pronta para qualquer fabricante licenciar. Isso baixa a barreira de entrada para concorrentes genéricos, mas também significa que o Anti-Ruído poderia **construir sobre esse chipset em vez de desenvolver o algoritmo do zero** — acelerando o roadmap técnico, ao custo de menor diferenciação defensável (ver "Unfair Advantage", seção 2).
- **Poder de barganha dos fornecedores:** moderado — chipsets Bluetooth/ANC têm múltiplos fornecedores (Qualcomm QCC/Snapdragon, Airoha, Bestechnic/BES, Jieli) e ODMs consolidados (ex. KiSB para Qualcomm QCC), reduzindo dependência de um único fornecedor, mas os chips com NPU dedicado para IA (Snapdragon S7) ainda são um diferencial mais restrito.
- **Poder de barganha dos compradores:** alto — baixo custo de troca entre marcas de fone, muitas alternativas disponíveis.
- **Ameaça de produtos substitutos:** alta — apps de isolamento de voz em smartphone (Krisp, mas não em tempo real "ao vivo" fisicamente), aproximar-se fisicamente, gritar, leitura labial (todos substitutos "gratuitos" existentes).

Fontes desta rodada: [Sonun – Most Common Headphone Chips](https://www.sonun.com/most-common-headphone-chips/), [Qualcomm – QCC30xx Series Bluetooth Audio SoCs](https://www.qualcomm.com/products/internet-of-things/consumer/audio/qcc30xx-series), [SoundGuys – Qualcomm Snapdragon S7 audio chip](https://www.soundguys.com/qualcomm-xpan-wifi-earbuds-102360/).

## 11. Blue Ocean Strategy Canvas

**Eixos da curva de valor:** preço, marca/confiança, isolamento seletivo de voz-alvo, foco social/casual (vs. profissional), simplicidade de ativação.

- **Apple/Sony/Bose:** altos em preço e marca, médios em ANC genérico, **baixos** em isolamento seletivo de voz de terceiros.
- **Orosound:** **alto** em isolamento seletivo de voz, mas **baixo** em foco casual/social (100% B2B) — não compete pela atenção do consumidor comum.
- **Anti-Ruído (proposta):** cria uma curva nova, alta em isolamento seletivo de voz-alvo *e* em foco social/casual, preço médio-alto (não ultra-premium), simplicidade de ativação como diferencial central.

**Grade ERRC (Eliminate-Reduce-Raise-Create):**
- **Eliminar:** recursos corporativos/de frota da Orosound (gestão centralizada, integração com softwares de call center) — irrelevantes para o consumidor casual.
- **Reduzir:** preço frente ao ultra-premium (Bose/Sony ~US$400+).
- **Elevar:** isolamento seletivo de voz-alvo para uso social casual; simplicidade de ativação ("modo conversa" em 1 gesto).
- **Criar:** categoria de "fone social" pensado explicitamente para bares/eventos/shows, não para escritório nem genericamente para "todo dia".

## 12. Modelo de receita e pricing

Referências de preço (rodada 1): AirPods Pro ~US$250; Bose QC Ultra ~US$430; Sony XM6 ~US$400+; Jabra Enhance (hearing aid OTC) US$995-1995; faixa sub-US$50 é o segmento de ANC que mais cresce (~21%+ CAGR) — sinaliza pressão de comoditização de preço na entrada.

**Segmentação de preço no mercado de TWS (rodada 4):** o segmento US$51-100 é hoje o maior por volume; o segmento US$100-199 já responde por 51,3% do valor de mercado (crescendo 31,7% a.a.); o segmento premium >US$200 nos EUA vale US$15,42B (37,8% share) e cresce **30,9% a.a.** — o crescimento mais rápido está no premium, não no genérico. Isso sugere um "sweet spot" de lançamento em torno de **US$150-250**: acima do genérico (evita comoditização), mas abaixo do super-premium (Bose/Sony ~US$400+), competindo diretamente com o preço do AirPods Pro.

**Benchmarks de crowdfunding (rodada 4):** earbuds com diferencial de IA/tradução conseguem tração em crowdfunding nessa faixa — Timekettle WT2 Plus (tradução offline) US$239,99; Morph InfiniConnect atingiu 1600% da meta; Buddie (assistente IA open-source) usa "preço de custo" para adoção inicial. Sinal de que uma proposta de valor clara e diferenciada consegue validar disposição a pagar via pré-venda, sem depender de varejo tradicional.

*Modelagem financeira detalhada (projeção 3-5 anos, cenários) — Rodada 14. Willingness-to-pay aprofundada — Rodada 37.*

Fontes desta rodada: [Grand View Research – TWS Earbuds Market Report](https://www.grandviewresearch.com/industry-analysis/true-wireless-stereo-earbuds-market-report), [Kickstarter – Buddie AI Earbuds](https://www.kickstarter.com/projects/buddieai/buddie-the-discrete-ai-earbuds-assistant), [Liliputing – TDM Neo hybrid headphones Kickstarter](https://liliputing.com/tdm-neo-hybrid-headphones-and-speaker-launch-on-kickstarter-for-189-and-up/).

## 12.1 Estrutura de custos, fundraising, legal, supply chain e certificações (Fase B, rodadas 14-20)

**Estrutura de custos e modelagem financeira (rodadas 14-15):** o custo de materiais (BOM) de eletrônicos de consumo como earbuds normalmente fica entre **US$10-50**, sendo que o BOM responde por 50-70% do custo total de fabricação — o resto é montagem, controle de qualidade, embalagem e logística. Como referência de margem no setor de áudio premium: fones Beats de US$200 no varejo tiveram BOM estimado em ~US$18 (caso público, ilustra a margem típica de marca/design em áudio de consumo). Para o Anti-Ruído — que precisa de array de microfones adicional e um chipset com NPU dedicado (ex. Snapdragon S7, seção 10) — o BOM estimado deve ficar **acima da média de TWS genérico**, plausivelmente na faixa de US$35-70 (estimativa ilustrativa para o pitch, não cotação real de fornecedor — validar com ODM antes de qualquer compromisso financeiro). Cenários de receita (otimista/base/pessimista) dependem de validação de preço (seção 12) e taxa de conversão de pré-venda — a modelar com dados reais após entrevistas (seção 16), não estimados sem evidência nesta rodada.

**Fundraising (rodada 16):** rounds pre-seed em 2025-2026 tipicamente levantam **US$250K-1,5M** (até US$2M para times "quentes" ou deep-tech/IA). Comparáveis diretos no espaço de áudio/hearables: xMEMS (componentes MEMS de áudio) levantou US$21M em Series D; Mira (AR glasses) US$6,6M seed; Hearvana (wearable de áudio para saúde) US$6M pre-seed. Sinal de alerta: "hearables conectados" respondem por 12,5% das rodadas de wearables mas **só 2,77% do capital**, sugerindo que investidores financiam validação, não escala, nesse subsegmento específico — relevante para calibrar expectativa de captação. Mediana de seed para wearables early-stage: ~US$2M.

**Cap table (rodada 17 — prática geral de mercado, não dado desta pesquisa específica):** para 2-3 cofundadores em estágio pre-seed, a prática comum é split relativamente equilibrado ajustado por contribuição/risco assumido, reservando 10-20% em pool de opções (ESOP) para contratações futuras, evitando que um único fundador fique com participação esmagadoramente majoritária antes da primeira rodada institucional.

**Legal/societário (rodada 18):** no Brasil, startups de hardware tipicamente constituem-se como Sociedade Limitada (LTDA) ou, com plano de captação institucional, Sociedade Anônima (S.A.) ou LTDA com acordo de quotistas equivalente a shareholders agreement. Proteção de IP relevante: registro de patente no INPI (Brasil) além de eventual depósito internacional (PCT), NDA com fabricantes/ODMs antes de compartilhar especificações técnicas. *(Pesquisa jurídica aprofundada real fica fora do escopo deste evento — recomenda-se consultoria jurídica especializada antes de qualquer desenvolvimento.)*

**Cadeia de suprimentos e manufatura (rodada 19):** ODMs consolidados já atendem earbuds com chipset Qualcomm QCC (ex. KiSB, citado na seção 10) — reduz o tempo de lançamento por reaproveitar referência de design existente ("reference design"). MOQs (quantidade mínima de pedido) para hardware customizado tipicamente são da ordem de milhares de unidades por lote — a validar com cotação real de ODM antes do roadmap pós-evento.

**Certificações e compliance (rodada 20):** no Brasil, a homologação da ANATEL é **obrigatória** para qualquer fone Bluetooth (classificado como Categoria II — radiocomunicação de radiação restrita), regida pela Resolução ANATEL nº 715/2019 (alterada pela nº 780/2025) e pela Resolução nº 680/2017. Desde o Ato ANATEL nº 1.630/2021, o **ensaio de SAR (Specific Absorption Rate) é obrigatório** para fones in-ear/TWS/over-ear usados a menos de 20cm do corpo. Mercados internacionais (FCC nos EUA, CE na União Europeia) têm exigências análogas — pendente pesquisa detalhada em rodada futura. Combinado com o risco regulatório de "dispositivo médico" (seção 13), o produto precisa navegar **certificação de telecomunicações (ANATEL/FCC/CE)** E manter-se fora da categoria de dispositivo médico.

Fontes desta seção: [TechSpot – Beats headphones BOM cost](https://www.techspot.com/news/61060-200-beats-headphones-actually-cost-18-make.html), [AGS Devices – BOM Cost 2025](https://www.agsdevices.com/bom-cost/), [Growth List – Audio Startups 2026 Funded Companies](https://growthlist.co/audio-startups/), [New Market Pitch – Wearable Technology Startup Funding 2025-2026](https://newmarketpitch.com/blogs/news/werarable-funding-analysis), [Startups.com – Pre-seed Funding 2025](https://www.startups.com/lexicon/pre-seed-funding), [ABCP – Certificação e Homologação ANATEL de Fones Bluetooth](https://abcpcertificacao.com.br/certificacao-anatel/fones-bluetooth/), [Gov.br ANATEL – Homologar produtos de telecomunicações](https://www.gov.br/pt-br/servicos/homologar-produtos-de-telecomunicacoes-anatel).

## 13. Riscos

**Riscos identificados na rodada 1 (aprofundamento de mitigação na rodada 32):**

- **Técnico**: extrair voz-alvo em tempo real com baixa latência e baixo consumo de energia num chip de earbud (não num laptop) é território de pesquisa, não tecnologia "de prateleira" pronta — maior incerteza técnica do projeto.
- **Regulatório**: a FDA oficializou em 2022 a categoria de **OTC Hearing Aids** (Bose, Jabra e o recurso "Hearing Aid" do AirPods Pro 2 já certificados). Qualquer alegação de "melhorar audição" (não só cancelar ruído) pode enquadrar o produto como dispositivo médico regulado, com exigências técnicas (ex.: limite de 111 dB SPL) e de rotulagem. Fonte: [FDA – OTC Hearing Aids](https://www.fda.gov/medical-devices/hearing-aids/otc-hearing-aids-what-you-should-know), [Federal Register 2022](https://www.federalregister.gov/documents/2022/08/17/2022-17230/medical-devices-ear-nose-and-throat-devices-establishing-over-the-counter-hearing-aids). **Atualização (rodada 2, jan/2026):** a FDA publicou nova diretriz que trata earbuds que "amplificam e esclarecem vozes ao redor" como dispositivo de bem-estar (wellness), não aparelho auditivo regulado — **reduz esse risco**, desde que o marketing evite alegações de "tratar perda auditiva". Fonte: [IEEE Spectrum](https://spectrum.ieee.org/fda-medical-device-rules), [STAT News](https://www.statnews.com/2026/01/06/fda-pulls-back-oversight-ai-enabled-devices-wearables/). Ainda pendente: equivalente da ANVISA no Brasil.
- **Mercado**: dois precedentes diretos de fracasso comercial em hearables "inteligentes" — **Doppler Labs** (levantou US$50M+, fechou em 2017) e **Nuheara** (liquidação em 2023). Ambos mostram que hardware de áudio "smart" tem histórico de dificuldade de tração e unit economics.
- **Propriedade intelectual**: já existe pelo menos uma patente registrada (US 10923136) em técnica de extração de fala-alvo supervisionada — o espaço de IP não está vazio. **Aprofundamento (rodada 5):** há também a patente **US20220122611A1** (Google) — "Targeted voice separation by speaker conditioned on spectrogram masking" — confirmando que players grandes (Google) já depositaram IP nessa área específica. Ao mesmo tempo, a pesquisa acadêmica em *target speaker extraction* está muito ativa em 2025 (técnicas como USEF-TSE sem necessidade de embedding de locutor, uso de encoders self-supervised como WavLM/wav2vec 2.0, modelos de difusão) — **o campo é ao mesmo tempo bem patenteado por incumbentes E muito pesquisado abertamente**, o que sugere que construir sobre pesquisa acadêmica aberta (ex. papers arXiv, não as patentes) é o caminho mais seguro para evitar violação de IP, mas exige assessoria jurídica de patentes antes de qualquer desenvolvimento real.
- **Regulatório-técnico (rodada 20)**: no Brasil, homologação ANATEL é obrigatória para qualquer fone Bluetooth (Categoria II), incluindo ensaio de SAR obrigatório desde 2021 para in-ear/TWS — processo e custo a orçar antes de qualquer produção real (ver seção 12.1).
- **Competitivo**: Apple, Sony e Bose têm recursos (Adaptive Audio, Conversation Awareness, Adaptive NC Optimizer) que já endereçam parte do problema e poderiam estender via **atualização de firmware** para competir diretamente, sem precisar de novo hardware — barreira de entrada baixa para incumbentes reagirem. **Aprofundamento (rodada 7):** o chipset Qualcomm Snapdragon S7 já oferece "background voice rejection" e "context-aware ANC" como recurso de silício pronto para qualquer fabricante — isso significa que a barreira técnica para um concorrente genérico oferecer algo parecido está caindo rapidamente (ver Porter's Five Forces, seção 10).

## 13.1 Go-to-market, organização e expansão (Fase C, rodadas 21-30)

**Marca e posicionamento (rodada 21):** o nome "Anti-Ruído" comunica bem a categoria (ANC) mas não diferencia o ângulo social/conversa — a validar no evento se um nome que remeta a "conversa"/"clareza" (em vez de só "silêncio") comunica melhor a proposta única (ouvir uma pessoa específica, não só bloquear ruído).

**Estratégia de lançamento (rodada 23):** três caminhos plausíveis, cada um com trade-off:
1. **Crowdfunding** (Kickstarter/Indiegogo) — valida demanda e financia produção inicial, mas exige protótipo funcional demonstrável (risco, já que a solução técnica não foi construída neste evento).
2. **Pré-venda direta (landing page + D2C)** — mais rápido de testar, mas sem o efeito de prova social do crowdfunding.
3. **Varejo tradicional** — inviável nesta fase (exige escala e certificação já concluída, seção 12.1).
Recomendação preliminar: pré-venda direta para validar interesse/preço agora, crowdfunding como funding gate seguinte, uma vez com protótipo.

**Parcerias estratégicas (rodada 24):** casos reais de marcas de fone que já usam parcerias com vida noturna/eventos/artistas para atingir o público-alvo do Anti-Ruído: **Skullcandy x Budweiser** (fone em edição limitada, "clash de mundos" música + socialização, mirando jovens); **Sony LinkBuds S x Olivia Rodrigo** (parceria com artista Grammy para atingir Gen Z/millennials); **Bose x NFL** (patrocínio oficial de som). Esses casos confirmam que parcerias com marcas de bebida/eventos/artistas são um canal validado no setor — plausível para o Anti-Ruído: parcerias com casas de show, festivais de porte médio ("tier-two", que dão mais liberdade criativa a patrocinadores) e talvez marcas de bebida.

**Equipe e organização (rodada 25 — diretriz geral, não pesquisa específica desta rodada):** papéis-chave que faltam hoje: engenharia de hardware/acústica, ML/processamento de sinal (extração de voz), design industrial, e growth/marketing. Para um Startup Weekend, o time formado no evento deve mapear quais dessas competências já existem entre os participantes e quais precisam ser buscadas logo após.

**Cultura e valores (rodada 26):** a proposta de valor do produto é fundamentalmente sobre *conexão humana* em meio ao caos — sugere-se que a cultura da empresa espelhe isso: foco em usabilidade/simplicidade acima de especificações técnicas, e comunicação de marca que celebre "estar presente", não "se isolar" (reverte o estigma atual de fones em contexto social, JTBD social da seção 4).

**Métricas híbridas hardware+app (rodada 27):** se houver componente de assinatura de app (seção 12), as métricas de receita recorrente (MRR, churn) devem ser acompanhadas separadamente das métricas de venda de hardware (seção 14) — modelo "razor + blade" clássico de hearables com app companion.

**Expansão internacional (rodada 28):** o mercado brasileiro de wearables está avaliado em **US$1,57 bilhão (2024) → US$4,90 bilhões (2033, CAGR 13,5%)**, com o Brasil liderando a adoção de wearables na América Latina por população e urbanização. Isso é relevante porque o fundador está no Brasil — sugere que o Brasil pode ser mercado de lançamento inicial plausível antes de expansão para EUA/Europa (onde a concorrência e o preço médio de TWS premium são mais altos, seção 12).

**Sustentabilidade/ESG (rodada 29):** regulação de e-waste está se expandindo rapidamente — a Califórnia aprovou em 2025/2026 lei (SB 1215) que adiciona produtos com bateria embutida (incluindo fones sem fio) ao programa de reciclagem de eletrônicos, com taxa de descarte cobrada na compra; leis de "right-to-repair" também estão se expandindo para wearables em múltiplos estados dos EUA. Isso sinaliza que o design do produto deve considerar reparabilidade/reciclagem de bateria desde o início, tanto por compliance futuro quanto por posicionamento de marca.

**Análise de sensibilidade de mercado (rodada 30):** o principal cenário de risco (já mapeado nas seções 10 e 13) é a Apple/Sony/Bose lançarem via firmware um recurso de "isolar 1 voz específica" — dado que o chipset Qualcomm Snapdragon S7 já comoditiza parte disso (seção 10), esse cenário é **plausível no curto-médio prazo**. Mitigação estratégica: velocidade de execução + foco de marca 100% social/casual (que incumbentes não priorizam) + construir uma comunidade/marca antes que o recurso vire commodity.

Fontes desta seção: [Buzzincontent – Headphone brands marketing](https://www.buzzincontent.com/story/how-headphone-brands-are-amping-up-their-marketing-game-through-quirky-branded-content/), [PT Engine – Bose Marketing/NFL](https://www.ptengine.com/blog/digital-marketing/bose-marketing-7-emotional-marketing-campaigns-that-every-marketer-can-learn-from/), [Amazon Ads – Sony LinkBuds S case study](https://advertising.amazon.com/library/case-studies/sony-interactive-audio-ads), [Event Marketer – Tier-two music festival sponsorships](https://www.eventmarketer.com/article/brands-investing-tier-two-music-festival-sponsorships/), [Market Data Forecast – Brazil Wearable Technology Market](https://www.imarcgroup.com/brazil-wearable-technology-market), [Waste Dive – New 2026 recycling/battery EPR laws](https://www.wastedive.com/news/new-laws-2026-battery-epr-waste-recycling-organics-landfill-policy/808714/), [ERI – Electronics disposal rules to watch in 2026](https://eridirect.com/blog/2026/01/new-year-new-compliance-risks-electronics-disposal-rules-to-watch-in-2026/).

## 14. Métricas-chave / North Star Metric / AARRR

**North Star Metric (candidata):** número de "conversas bem-sucedidas em ambiente ruidoso" por usuário por semana (proxy: sessões em que o usuário ativa o "modo conversa" e reporta sucesso subjetivo de entendimento).

- **Acquisition:** crowdfunding (ver seção 12) + micro-influenciadores (10-100 mil seguidores têm engajamento de 3-8% vs. 1-2% de mega-influenciadores, e CPM 60-80% menor) + parcerias com casas de show/eventos.
- **Activation:** primeiro "momento aha" = conseguir isolar a voz de 1 pessoa com sucesso perceptível em ambiente ruidoso real, dentro de segundos de configuração inicial.
- **Retention:** uso recorrente associado a hábitos sociais (sair para bares/eventos/viagens) — testar se vira parte do "kit de saída" do usuário.
- **Revenue:** venda de hardware (seção 12) + possível assinatura de app para perfis de voz/ambiente personalizados.
- **Referral:** o próprio produto tem gatilho social embutido — demonstrar "experimenta isso" a um amigo em ambiente ruidoso é um momento natural de indicação.

**Nota sobre CAC:** custos de aquisição em D2C subiram 60-80% desde 2021 (mudanças de privacidade do iOS, saturação de plataformas); a meta saudável de LTV:CAC é de pelo menos 3:1 (marcas D2C premium alcançam 4-6:1) — referência para o roadmap de validação pós-evento (seção 16).

Fontes desta rodada: [MarketingCharts – D2C Brands Top Customer Acquisition Channels](https://www.marketingcharts.com/charts/d2c-brands-top-customer-acquisition-channels), [Storyboard18 – D2C influencer marketing budgets](https://www.storyboard18.com/brand-marketing/54-of-d2c-brands-spend-up-to-25-of-marketing-budgets-on-influencers-85597.htm).

## 15. OKRs de validação

**Objetivo 1 — Validar que o problema é real e que as pessoas pagariam por uma solução**
- KR1: Coletar N manifestações de interesse/pré-cadastro (landing page ou lista) durante o evento.
- KR2: Confirmar disposição a pagar em conversas informais com pelo menos 15-20 pessoas no perfil de persona (seção 5) durante o Startup Weekend.
- KR3: Obter validação qualitativa de pelo menos 1 mentor/especialista técnico do evento sobre a viabilidade da extração de voz em restrição de energia/DSP de um earbud.

**Objetivo 2 — Confirmar diferenciação real vs. concorrência**
- KR1: Mapear e confirmar (feito nas rodadas 1, 6 e 11) que nenhum concorrente direto atende ao caso de uso "escolher 1 voz específica em ambiente social casual".
- KR2: Testar a reação de pelo menos 10 pessoas ao pitch de 60s (abaixo) e registrar objeções recorrentes.

## 16. Roadmap de validação pós-evento

*Pendente — Rodada 38.*

## 17. Pitch de 60s e pitch de 5min

**Pitch de 60s (versão rascunho, rodada 10 — sem slides, formato oficial de sexta-feira):**

> "Você já tentou conversar num show, bar ou aeroporto lotado e teve que gritar, ou simplesmente desistiu? Nós somos o Anti-Ruído: um fone que aprende o ruído do ambiente ao seu redor e isola a voz de quem está falando com você, para você ouvir com clareza mesmo no caos. Hoje, Apple, Sony e Bose cancelam ruído — mas nenhum deles deixa você escolher ouvir uma pessoa específica em um ambiente social. A Orosound resolve algo parecido, mas só para escritórios corporativos. Ninguém resolveu isso para quem está numa balada, um show ou um bar. Queremos validar essa ideia com vocês esse fim de semana. Quem aqui já perdeu uma conversa importante porque o lugar estava barulhento demais?"

**Estrutura do pitch de 5min (domingo, alinhado aos 3 critérios de julgamento):**
1. Abertura com o problema + evidência (seção 1) — 45s
2. Demonstração conceitual do produto (mockup/wireframe, já que a solução técnica não foi construída neste evento) — 60s
3. Panorama competitivo e diferenciação (Blue Ocean, seção 11) — 60s
4. Modelo de negócio (Lean Canvas + pricing, seções 2 e 12) — 45s
5. Evidência de validação coletada no evento (OKRs, seção 15) — 45s
6. Pedido/próximos passos (roadmap, seção 16) — 15s

*(Refinado nas rodadas 42 e 54, após mais evidência coletada.)*

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

**Rodadas 3-10:**
- [Grand View Research – TWS Earbuds Market Report](https://www.grandviewresearch.com/industry-analysis/true-wireless-stereo-earbuds-market-report)
- [Grand View Research – OTC Hearing Aids Market Report](https://www.grandviewresearch.com/industry-analysis/over-the-counter-hearing-aids-market-report)
- [The Hearing Review – OTC Hearing Aid Market to Hit $1.16B by 2030](https://hearingreview.com/hearing-products/hearing-aids/otc/otc-hearing-aid-market-to-hit-1-16-billion-by-2030)
- [SkyQuest – Hearing Aid Market](https://www.skyquestt.com/report/hearing-aid-market)
- [Fortune Business Insights – Hearing Aids Market](https://www.fortunebusinessinsights.com/industry-reports/hearing-aids-market-101573)
- [GM Insights – OTC Hearing Aids Market](https://www.gminsights.com/industry-analysis/otc-hearing-aids-market)
- [Kickstarter – Buddie AI Earbuds Assistant](https://www.kickstarter.com/projects/buddieai/buddie-the-discrete-ai-earbuds-assistant)
- [Liliputing – TDM Neo hybrid headphones Kickstarter](https://liliputing.com/tdm-neo-hybrid-headphones-and-speaker-launch-on-kickstarter-for-189-and-up/)
- [Emergent Mind – Target Speaker Extraction Overview](https://www.emergentmind.com/topics/target-speaker-extraction-tse)
- [Google Patents – US20220122611A1 Targeted voice separation](https://patents.google.com/patent/US20220122611A1/en)
- [Sonun – Most Common Headphone Chips](https://www.sonun.com/most-common-headphone-chips/)
- [Qualcomm – QCC30xx Series Bluetooth Audio SoCs](https://www.qualcomm.com/products/internet-of-things/consumer/audio/qcc30xx-series)
- [SoundGuys – Qualcomm Snapdragon S7 audio chip](https://www.soundguys.com/qualcomm-xpan-wifi-earbuds-102360/)
- [MarketingCharts – D2C Brands Top Customer Acquisition Channels](https://www.marketingcharts.com/charts/d2c-brands-top-customer-acquisition-channels)
- [Storyboard18 – D2C influencer marketing budgets](https://www.storyboard18.com/brand-marketing/54-of-d2c-brands-spend-up-to-25-of-marketing-budgets-on-influencers-85597.htm)

**Rodadas 11-20:**
- [Orosound – About Us](https://www.orosound.com/about-us/)
- [Crunchbase – Orosound](https://www.crunchbase.com/organization/orosound)
- [PitchBook – Orosound Labs](https://pitchbook.com/profiles/company/125681-14)
- [TechSpot – $200 Beats headphones cost $18 to make](https://www.techspot.com/news/61060-200-beats-headphones-actually-cost-18-make.html)
- [AGS Devices – BOM Cost in 2025](https://www.agsdevices.com/bom-cost/)
- [Growth List – Audio Startups 2026](https://growthlist.co/audio-startups/)
- [New Market Pitch – Wearable Technology Startup Funding 2025-2026](https://newmarketpitch.com/blogs/news/werarable-funding-analysis)
- [Startups.com – Pre-seed Funding 2025](https://www.startups.com/lexicon/pre-seed-funding)
- [ABCP – Certificação e Homologação ANATEL de Fones Bluetooth](https://abcpcertificacao.com.br/certificacao-anatel/fones-bluetooth/)
- [Gov.br ANATEL – Homologar produtos de telecomunicações](https://www.gov.br/pt-br/servicos/homologar-produtos-de-telecomunicacoes-anatel)

**Rodadas 21-30:**
- [Buzzincontent – Headphone brands marketing](https://www.buzzincontent.com/story/how-headphone-brands-are-amping-up-their-marketing-game-through-quirky-branded-content/)
- [PT Engine – Bose Marketing/NFL campaigns](https://www.ptengine.com/blog/digital-marketing/bose-marketing-7-emotional-marketing-campaigns-that-every-marketer-can-learn-from/)
- [Amazon Ads – Sony LinkBuds S case study](https://advertising.amazon.com/library/case-studies/sony-interactive-audio-ads)
- [Event Marketer – Tier-two music festival sponsorships](https://www.eventmarketer.com/article/brands-investing-tier-two-music-festival-sponsorships/)
- [IMARC Group – Brazil Wearable Technology Market](https://www.imarcgroup.com/brazil-wearable-technology-market)
- [Waste Dive – New 2026 recycling/battery EPR laws](https://www.wastedive.com/news/new-laws-2026-battery-epr-waste-recycling-organics-landfill-policy/808714/)
- [ERI – Electronics disposal rules to watch in 2026](https://eridirect.com/blog/2026/01/new-year-new-compliance-risks-electronics-disposal-rules-to-watch-in-2026/)

---

## Metodologia deste documento

Este documento é mantido por um loop automatizado de pesquisa (~10 min por rodada, ~54 rodadas ao longo de ~9h), rodando durante o Startup Weekend, com o objetivo de aplicar metodologias reais de criação/validação de startup (Lean Canvas, SWOT, PESTEL, Porter's Five Forces, Blue Ocean Strategy, Value Proposition Canvas, Jobs To Be Done, AARRR, OKRs) à ideia do fone Anti-Ruído, e mapear tudo que for encontrável por pesquisa sobre concorrência, tecnologia, mercado, regulação e riscos — sem ainda construir a solução técnica. Cada rodada pesquisa fontes novas e reais (citadas inline e na seção 19), atualiza apenas as seções do seu ângulo, e evita repetir buscas já feitas. Fases do loop:

- **Fase A (rodadas 1-10)**: fundamentos de validação (Lean Canvas, SWOT/PESTEL, personas/JTBD, pricing, riscos técnicos/IP, VPC/Blue Ocean, Porter, AARRR, mercado adjacente, OKRs/pitch).
- **Fase B (rodadas 11-20)**: teardown competitivo e finanças aprofundadas.
- **Fase C (rodadas 21-30)**: go-to-market e organização.
- **Fase D (rodadas 31-42)**: síntese, mitigação de risco e consolidação.
- **Fase E (rodadas 43-54)**: polimento final e reforço das seções mais fracas.
