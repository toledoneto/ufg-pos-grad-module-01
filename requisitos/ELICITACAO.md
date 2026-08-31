# Elicitação de Requisitos com Apoio de IA Generativa

**Projeto:** Gerador de Senhas Seguras
**Baseline analisada:** 1.0.0
**Responsável:** Toledo Neto
**Data:** Julho de 2026
**Ferramenta de IA:** Claude Opus 5, via Claude Code

---

## 1. Objetivo e natureza desta atividade

Este documento registra a **elicitação e especificação de requisitos** do Gerador de Senhas Seguras, conduzida com apoio de IA generativa, e justifica a escolha dos artefatos produzidos.

Há uma particularidade que precisa ficar explícita, porque muda o significado do que foi feito: **o produto já estava implementado quando esta elicitação ocorreu**. A Fase 1 original (documentada no [README](../README.md#fase-1--levantamento-de-requisitos)) produziu oito requisitos funcionais, três não funcionais e três regras de negócio — suficientes para começar a codificar, insuficientes como especificação.

Isso configura uma **elicitação retrospectiva com projeção de incremento**, e não uma elicitação inicial. Ela tem três produtos distintos:

| Produto | O que é |
|---------|---------|
| **Especificação da baseline** | O que a versão 1.0.0 de fato faz — reconstruído a partir de código, testes e documentação, não a partir de intenção |
| **Divergências** | Onde documentação, código e expectativa discordam entre si |
| **Requisitos do próximo incremento** | O que o backlog e a análise de riscos implicam, formulado como requisito verificável antes de virar código |

Essa é a situação mais comum em manutenção de software real: a especificação precisa ser reconstruída, e a reconstrução vale mais pelo que revela de inconsistência do que pelo que confirma. Dez divergências foram encontradas — registradas em [lacunas-ambiguidades.md](lacunas-ambiguidades.md).

---

## 2. Técnicas de elicitação empregadas

Sem acesso a usuários reais — restrição do contexto acadêmico —, as técnicas foram escolhidas entre as que operam sobre artefatos existentes:

| Técnica | Como foi aplicada | O que produziu |
|---------|-------------------|----------------|
| **Análise de documentos** | Leitura do README, `docs/`, `CHANGELOG.md`, `riscos/` e `comunicacao/` | Recuperação dos requisitos originais e das decisões de escopo |
| **Engenharia reversa de requisitos** | Leitura de `main.py`, `generator.py`, `models.py`, `script.js` e da suíte de testes | RN04–RN08 e RF09–RF11, que existiam em código mas em nenhum documento |
| **Análise de inconsistência cruzada** | Confronto documentação × implementação × testes, item a item | LA01–LA10; a mais grave (LA03) só aparece nesse cruzamento |
| **Derivação a partir de riscos** | Cada risco de `riscos/identificacao.md` foi lido como requisito ausente | RNF06, RNF07, RNF08, RNF13 |
| **Prototipagem de baixa fidelidade** | Wireframe textual dos seis estados da interface | Confirmação do fluxo e das decisões D1–D6 |
| **Questionamento adversarial assistido por IA** | Solicitação explícita à IA de que criticasse a especificação em vez de completá-la | LA01, LA02, LA06 e LA09 |
| **Análise de personas** | Distinção entre usuário final, operador e monitoramento | Ator "operador de infraestrutura" (LA07), UC04, HU09 |

A técnica que mais rendeu foi a **análise de inconsistência cruzada**. Documentos isolados são internamente coerentes — é no confronto entre eles que a divergência aparece.

---

## 3. Artefatos produzidos e por que estes

A escolha dos artefatos partiu de três características do projeto, não de um checklist genérico:

- **Domínio simples, poucas entidades.** Não há modelo de dados (o sistema é stateless), não há workflow multi-ator, não há máquina de estados de negócio. Artefatos estruturais tradicionais teriam pouco a representar.
- **Complexidade concentrada em regras e qualidade.** O que é difícil aqui é a regra de composição, a classificação de força e as propriedades não funcionais (não persistir, não logar, gerar com CSPRNG). É onde a especificação precisa ser precisa.
- **Produto já implementado.** Artefatos precisam ser verificáveis contra código existente, ou não passam de ficção retroativa.

### 3.1 Artefatos escolhidos

| Artefato | Por que é adequado a **este** projeto |
|----------|--------------------------------------|
| **[Especificação de requisitos](especificacao-requisitos.md)** — RF, RN, RNF com IDs, origem, critério de verificação e status | O projeto já tinha IDs em uso no README, em testes e na análise de riscos. Preservá-los mantém a rastreabilidade histórica; acrescentar *critério de verificação* transforma frases como "a API deve responder rápido" em algo testável. A separação explícita entre RF, RN e RNF importa aqui porque **as regras de negócio são o núcleo do produto** — RN03 e RN06 concentram quase toda a complexidade lógica |
| **[Histórias de usuário com critérios em Gherkin](historias-de-usuario.md)** | O produto tem funcionalidades pequenas, independentes e priorizáveis — formato natural para história. O Gherkin foi escolhido em vez de critérios em prosa porque quase todo critério aqui é uma **tabela de decisão**: tamanho × tipos → força, combinação de checkboxes → habilitação do botão. `Esquema do Cenário` com exemplos expressa isso de forma direta e espelha a estrutura de `@pytest.mark.parametrize` já usada na suíte |
| **[Casos de uso expandidos](casos-de-uso.md)** | Histórias descrevem bem o caminho feliz e mal os fluxos de exceção. Neste produto os desvios são onde mora o risco: backend fora do ar, origem bloqueada por CORS, validação recusada, cópia sem API de clipboard. O formato expandido (Cockburn) obriga a enumerar exceções e a declarar **garantia mínima** — foi assim que a promessa "nada é armazenado mesmo em falha" virou requisito verificável |
| **[Lacunas e ambiguidades](lacunas-ambiguidades.md)** | O artefato mais valioso desta atividade e o que justifica o uso de IA. Registra dez divergências entre documentação, código e expectativa, cada uma classificada, avaliada e encerrada com um encaminhamento — em vez de virar conhecimento tácito do único desenvolvedor (risco [R11](../riscos/identificacao.md)) |
| **[Protótipo de baixa fidelidade](prototipo.md)** | A interface é uma tela única; o que precisava ser validado era **comportamento entre estados**, não estética. Um wireframe textual com diagrama de estados responde a isso e é versionável em Git junto do código. Protótipo de alta fidelidade custaria mais e discutiria a coisa errada |
| **[Matriz de rastreabilidade](matriz-rastreabilidade.md)** | Fecha o ciclo: requisito → história → caso de uso → código → teste → risco. Foi ela que expôs os cinco trechos de código sem requisito declarado e as três propriedades verificadas apenas por inspeção humana. Também dá a tabela de impacto de mudança, que mostra RN06 duplicada em seis lugares |

### 3.2 Artefatos deliberadamente descartados

Registrar o que **não** se produz é parte da justificativa — a escolha só é defensável se as alternativas foram consideradas.

| Artefato | Por que foi descartado |
|----------|----------------------|
| **Modelo entidade-relacionamento / diagrama de classes** | Não há persistência nem hierarquia de domínio. Duas classes Pydantic (`SenhaRequest`, `SenhaResponse`) são o modelo inteiro, e o contrato da API já as descreve melhor do que um diagrama descreveria |
| **BPMN / diagrama de atividades de negócio** | Não existe processo organizacional, aprovação ou múltiplos papéis em sequência. O [diagrama de fluxo](../docs/fluxo-geracao.md) da Fase 2 já cobre o algoritmo com precisão suficiente |
| **Especificação IEEE 830 / ISO 29148 completa** | O modelo prevê seções — evolução do produto, migração, suposições de interoperabilidade — que seriam preenchidas com "não se aplica". Adotou-se a **estrutura de qualidade da ISO/IEC 25010** para classificar os RNF, sem importar o template inteiro |
| **Diagrama de máquina de estados do domínio** | Não há entidade com ciclo de vida; a senha nasce e morre na mesma requisição. O único estado relevante é o **da interface**, e ele está no protótipo |
| **Protótipo navegável de alta fidelidade** | Custo desproporcional para uma tela cujo layout já está implementado. Serviria para vender a ideia, não para especificar |
| **Backlog formal com estimativas em story points** | A priorização MoSCoW resolve o que é necessário aqui. Estimar velocidade de uma equipe de uma pessoa produziria número sem lastro |
| **Casos de uso para cada interação de tela** | Explicado em [4.2](#42-o-que-foi-modificado) — foi exatamente a sugestão da IA que precisou ser corrigida |

---

## 4. Como a IA generativa apoiou a atividade

A IA foi usada como **analista de requisitos júnior incansável**: rápida para varrer, gerar hipóteses e produzir texto estruturado; sem autoridade para decidir. Toda decisão de escopo, classificação de severidade e encaminhamento foi humana.

### 4.1 Onde a contribuição foi real

**Varredura cruzada em escala.** A tarefa mais produtiva — confrontar cada afirmação do README com o código correspondente — é mecânica, tediosa e propensa a desatenção humana. A IA leu os quatro arquivos de código, os três de teste, o README de 674 linhas e os seis documentos auxiliares em uma passagem, e apontou onde documentação e implementação divergiam. Foi assim que [LA03](lacunas-ambiguidades.md#la03--mensagem-de-erro-da-api-não-chega-ao-usuário) apareceu: o contrato documentado promete `{"detail": "<string>"}`, o handler em `main.py:53` devolve `{"detail": [lista de erros]}`. A divergência estava lá desde a Fase 5 e nenhuma leitura anterior a tinha pego.

**Crítica adversarial sob demanda.** O prompt mais útil de toda a atividade não pedia produção, pedia contestação: *"aja como um analista cético; aponte onde a especificação está errada, não onde está incompleta"*. Isso rendeu [LA01](lacunas-ambiguidades.md#la01--força-não-mede-entropia) (uma senha de 128 minúsculas é classificada "fraca" enquanto tem entropia muito maior que uma "muito forte" de 16) e [LA02](lacunas-ambiguidades.md#la02--o-campo-forca-é-string-livre-no-contrato) (mudar o rótulo `"média"` no backend faria o frontend exibir "Fraca" para toda senha, silenciosamente). Nenhuma das duas é bug em execução — são falhas de especificação que só aparecem quando alguém pergunta "e se?".

**Detecção de conflito entre requisitos.** Ao cruzar o backlog do README com os RNF, a IA identificou que "avaliar senha existente" contradiz a premissa que sustenta toda a arquitetura: o produto se justifica porque a senha nasce no servidor e nunca é armazenada — enviar uma senha *em uso* inverte isso ([LA06](lacunas-ambiguidades.md#la06--hu11-conflita-com-a-regra-de-não-trafegar-senha-em-uso)). É o tipo de contradição que só se percebe lendo dois documentos ao mesmo tempo.

**Preenchimento estruturado de formato.** Casos de uso expandidos e cenários Gherkin têm forma rígida e repetitiva. A IA produziu o rascunho completo dos seis casos de uso e dos conjuntos de critérios das histórias; a revisão humana corrigiu conteúdo, não estrutura. Ganho de tempo direto, sem perda de qualidade.

**Vocabulário de qualidade.** Os RNF originais eram três. A IA propôs a classificação por ISO/IEC 25010, o que expôs categorias inteiras nunca consideradas — acessibilidade, operabilidade, manutenibilidade. Nem tudo foi aceito (ver 4.3), mas a estrutura tornou visível o que faltava.

### 4.2 O que foi modificado

Casos em que a sugestão da IA foi aproveitada **depois de correção humana**:

| Sugestão original da IA | Correção aplicada | Motivo |
|------------------------|-------------------|--------|
| Reaproveitar os oito casos de uso do [diagrama da Fase 2](../docs/casos-de-uso.md) — *"Selecionar maiúsculas"*, *"Selecionar minúsculas"*, *"Selecionar números"*, *"Selecionar especiais"* | Reagrupados em quatro casos de uso orientados a objetivo (UC01–UC04) mais duas subfunções (UC05, UC06); as seleções viraram **passos** do UC01 | Marcar uma caixa de seleção não é objetivo de ator: ninguém abre a aplicação para "selecionar maiúsculas". Caso de uso precisa ter valor observável ao término. A IA reproduziu o erro do documento original em vez de questioná-lo — modelos tendem a tratar o artefato existente como correto |
| Escrever uma especificação nova, com numeração própria | Preservados os IDs RF01–RF08, RNF01–RNF03 e RN01–RN03 do README; novos itens continuam a partir dali | Os IDs originais são citados na análise de riscos e na comunicação a stakeholders. Renumerar quebraria rastreabilidade sem ganho algum |
| Critérios de aceitação em prosa ("o sistema deve exibir a força correta") | Reescritos em Gherkin, com `Esquema do Cenário` e tabelas de exemplo | Prosa não é verificável. A regra de força é uma tabela de decisão e precisa ser expressa como tabela — inclusive as linhas contraintuitivas, como `1 tipo / 128 caracteres → Fraca` |
| Marcar RN06 (classificação de força) como **defeito** a corrigir | Reclassificada como **limitação conhecida e aceita** na 1.0.0, com correção projetada para 1.1 (HU12) | A regra faz o que foi especificado; o problema é o nome "força" prometer mais do que a métrica entrega. Chamar de defeito distorceria o histórico e sugeriria correção emergencial onde cabe evolução planejada |
| Ator "Administrador do sistema", com permissões e autenticação | Substituído por "Operador de infraestrutura", sem interface própria e sem autenticação | Não existe painel administrativo nem conta de usuário no produto. A IA importou um ator de sistemas típicos; o ator real configura variáveis de ambiente e nada mais |
| Trocar a heurística de força por entropia já na especificação da baseline | Registrada como HU12 no incremento 1.1, com a limitação documentada no glossário e no critério de HU05 | Especificação de baseline descreve o que **existe**. Misturar o desejado com o implementado é o erro que originou boa parte das divergências encontradas |
| Afirmar "57 testes" ao descrever a cobertura em [LA04](lacunas-ambiguidades.md#la04--rnf02-e-rnf03-não-são-verificados-por-teste) | Substituído por descrição qualitativa das camadas cobertas | O número vem do README. A contagem direta encontra 45 funções de teste, que se expandem via `parametrize` — os dois números podem estar certos, mas nenhum foi verificado em execução nesta atividade. Requisito não se apoia em número não conferido |

### 4.3 O que foi descartado

Sugestões recusadas por inteiro, com o motivo:

| Sugestão descartada | Motivo |
|--------------------|--------|
| **Requisitos de autenticação, contas e "senhas favoritas"** | Escopo inventado. Contradiz frontalmente a decisão fundadora do projeto de não persistir nada. A IA propôs por analogia com gerenciadores de senha — produtos diferentes |
| **Bateria completa de RNF da ISO/IEC 25010** (portabilidade entre SOs, compatibilidade com navegadores legados, recuperação de desastre, backup, escalabilidade horizontal) | Requisito que ninguém vai verificar é ruído: dilui a especificação e cria falsa sensação de rigor. Foram mantidos apenas os RNF com critério de verificação plausível neste contexto. Backup, em particular, é absurdo em um sistema que por definição não guarda dado |
| **Diagrama de classes UML do backend** | Duas classes Pydantic e três funções. O diagrama teria menos informação que o próprio arquivo `models.py`, com custo de manutenção adicional |
| **Estimativas em story points e velocidade de sprint** | Equipe de uma pessoa, sem histórico de iterações. Número sem lastro empírico é decoração |
| **Personas ficcionais detalhadas** ("Ana, 34 anos, analista financeira que esquece senhas") | Persona só tem valor quando informada por pesquisa com usuários. Inventada, vira ficção que confere autoridade indevida a preferências do próprio autor. A distinção entre usuário final e operador — essa sim, derivável dos requisitos — foi mantida |
| **Reescrever as tabelas de requisitos da Fase 1 no README** | O README é registro histórico do processo em cinco fases. Sobrescrevê-lo apagaria a evolução que esta atividade justamente documenta. A especificação nova referencia o README e declara-se como fonte de verdade — sem reescrever o passado |
| **Marcar todos os itens de `riscos/` como requisitos obrigatórios** | Risco identificado não é requisito aprovado. RNF06–RNF08 foram derivados dos riscos, mas entram como **backlog condicionado à publicação em ambiente público** — não como pendência da 1.0.0, que nunca previu deploy público |
| **Gerar automaticamente o código das correções apontadas** | Fora do escopo desta atividade. A elicitação identifica e especifica; a correção é decisão de priorização que passa pelo CHANGELOG e por nova rodada de testes |

### 4.4 Limitações observadas no uso da IA

Registro honesto, por ser tão instrutivo quanto os acertos:

1. **A IA tende a confiar no documento.** Diante de README e código em conflito, a primeira resposta reproduziu o README — inclusive o contrato 422 incorreto. Só ao ser instruída a *verificar cada afirmação contra o código-fonte* ela encontrou a divergência. A postura padrão do modelo é completar coerentemente, não duvidar.
2. **Fluência é indistinguível de correção.** Requisitos inventados (autenticação, backup) vieram redigidos com a mesma segurança dos corretos. Nada no texto sinaliza qual é qual — a triagem é inteiramente humana e não pode ser delegada.
3. **Viés de completude.** Pedir "os requisitos não funcionais deste sistema" produz a lista canônica de RNF de qualquer sistema. A pergunta útil não é "o que falta?", e sim "o que aqui é verificável e por quem?".
4. **Números precisam ser conferidos.** A contagem de testes ilustrou bem: a IA repetiu um valor documentado sem conferir, e a conferência deu resultado diferente. Toda quantidade citada foi ou verificada, ou substituída por descrição qualitativa.
5. **Reprodução de erro herdado.** Quando o artefato existente contém um erro conceitual — os oito "casos de uso" que eram interações de tela —, o modelo o propaga em vez de corrigi-lo, porque o trata como contexto autoritativo.

**Conclusão operacional:** a IA acelerou fortemente a *varredura* e a *redação estruturada*, e foi genuinamente útil na *geração de hipóteses adversariais*. Não substituiu, em nenhum momento, o julgamento sobre o que é escopo, o que é severidade e o que é decisão de produto. O padrão que funcionou foi: **IA propõe amplamente, humano verifica contra o código e decide** — com a verificação contra a fonte primária sendo a etapa não negociável.

---

## 5. Estratégia de prompts

Os prompts que produziram resultado útil seguiram quatro padrões. Registrados aqui porque a qualidade do artefato dependeu mais da formulação da pergunta do que da capacidade do modelo.

| Padrão | Formulação usada | Resultado |
|--------|-----------------|-----------|
| **Verificação contra fonte primária** | *"Para cada afirmação do README sobre o comportamento da API, localize a linha de código correspondente e diga se confere"* | LA03 — a divergência do 422 |
| **Adversarial** | *"Aja como um analista cético revisando esta especificação. Não a complete: aponte onde ela está errada, ambígua ou não verificável"* | LA01, LA02, LA05, LA09 |
| **Cruzamento de artefatos** | *"Confronte o backlog do README com os requisitos não funcionais e aponte contradições"* | LA06 — conflito entre HU11 e RNF02 |
| **Restrição explícita de escopo** | *"Não proponha requisitos que este produto não tem. Se um requisito não puder ser verificado com o que existe no repositório, marque-o como não verificável em vez de incluí-lo"* | Redução drástica de RNF inventados |

O padrão que **não** funcionou: perguntas abertas do tipo *"quais requisitos faltam neste sistema?"*. Elas produzem a lista genérica de qualquer sistema web e exigem mais esforço de triagem do que teriam economizado.

---

## 6. Resultado consolidado

| Métrica | Antes (Fase 1 original) | Depois desta elicitação |
|---------|------------------------|------------------------|
| Requisitos funcionais | 8 | 15 (11 na baseline, 4 no backlog) |
| Requisitos não funcionais | 3 | 19, agrupados por característica de qualidade |
| Regras de negócio | 3 | 8 |
| Requisitos com critério de verificação | 0 | 100 % dos requisitos da baseline |
| Histórias de usuário | — | 13, em 5 épicos, priorizadas por MoSCoW |
| Casos de uso especificados | 8 interações de tela, sem fluxo | 4 casos de uso + 2 subfunções, com exceções |
| Divergências documentadas | — | 10, classificadas e encaminhadas |
| Questões em aberto | — | 5, com dependência e item bloqueado |
| Código sem requisito declarado | 5 trechos | 0 |

O ganho mais relevante não é quantitativo. É que **três propriedades que sustentam a proposta do produto — não persistir, não logar e responder rápido — estavam afirmadas na documentação e não verificadas por nada**. Depois desta elicitação, duas continuam sem teste automatizado, mas isso agora é uma lacuna rastreada com encaminhamento ([LA04](lacunas-ambiguidades.md#la04--rnf02-e-rnf03-não-são-verificados-por-teste)), e não uma suposição silenciosa.

---

## 7. Índice dos artefatos

| Artefato | Conteúdo |
|----------|----------|
| [especificacao-requisitos.md](especificacao-requisitos.md) | RF, RN e RNF com origem, critério de verificação, status, glossário e premissas |
| [historias-de-usuario.md](historias-de-usuario.md) | 13 histórias em 5 épicos, com critérios de aceitação em Gherkin |
| [casos-de-uso.md](casos-de-uso.md) | UC01–UC06 expandidos, com fluxos alternativos, exceções e diagrama revisado |
| [lacunas-ambiguidades.md](lacunas-ambiguidades.md) | LA01–LA10 classificadas por tipo e severidade + 5 questões em aberto |
| [prototipo.md](prototipo.md) | Wireframes dos 6 estados, diagrama de estados e decisões de interface |
| [matriz-rastreabilidade.md](matriz-rastreabilidade.md) | Requisito ↔ história ↔ caso de uso ↔ código ↔ teste ↔ risco, e impacto de mudança |

**Documentos do projeto referenciados:** [README.md](../README.md) · [docs/](../docs/) · [riscos/](../riscos/) · [comunicacao/status-stackholders.md](../comunicacao/status-stackholders.md) · [PROMPTS.md](../PROMPTS.md) · [CHANGELOG.md](../CHANGELOG.md)
