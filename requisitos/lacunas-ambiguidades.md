# Lacunas, Ambiguidades e Questões em Aberto

Resultado da análise crítica dos requisitos existentes contra o código implementado, a documentação da Fase 1 e a análise de riscos. Cada item é classificado, avaliado quanto ao impacto e encerrado com um **encaminhamento**: corrigir agora, corrigir no próximo incremento ou aceitar com registro.

**Classificação usada:**

| Tipo | Significado |
|------|-------------|
| **Lacuna** | Requisito necessário que nunca foi declarado |
| **Ambiguidade** | Requisito declarado que admite mais de uma leitura |
| **Inconsistência** | Documentação e implementação discordam entre si |
| **Conflito** | Dois requisitos não podem ser satisfeitos simultaneamente |

**Severidade:** Alta (compromete o propósito do produto ou induz o usuário ao erro) · Média (afeta manutenção ou confiabilidade) · Baixa (cosmética ou de baixo alcance).

---

## Resumo

| ID | Item | Tipo | Severidade | Encaminhamento |
|----|------|------|-----------|----------------|
| [LA01](#la01--força-não-mede-entropia) | Indicador de força ignora o tamanho do alfabeto | Ambiguidade | Alta | Aceitar na 1.0 · corrigir na 1.1 (HU12) |
| [LA02](#la02--o-campo-forca-é-string-livre-no-contrato) | `forca` é `str` livre, acoplando frontend a rótulos | Lacuna | Média | Corrigir na 1.1 (RNF19) |
| [LA03](#la03--mensagem-de-erro-da-api-não-chega-ao-usuário) | 422 documentado difere do implementado; motivo não chega ao usuário | Inconsistência | Alta | Corrigir a documentação agora · melhorar a mensagem na 1.1 |
| [LA04](#la04--rnf02-e-rnf03-não-são-verificados-por-teste) | RNF02 e RNF03 sem verificação automatizada | Lacuna | Alta | Corrigir na 1.1 |
| [LA05](#la05--confirmação-de-cópia-não-é-verificada) | "Copiado!" é exibido mesmo se a cópia falhar | Lacuna | Média | Corrigir na 1.1 |
| [LA06](#la06--hu11-conflita-com-a-regra-de-não-trafegar-senha-em-uso) | Avaliar senha existente contradiz RNF02 | Conflito | Alta | Decidir antes de aceitar HU11 no escopo |
| [LA07](#la07--ator-operador-não-declarado-na-especificação) | Operador de infraestrutura não era ator reconhecido | Lacuna | Média | **Corrigido** nesta elicitação |
| [LA08](#la08--padrão-inseguro-de-cors-não-falha-de-forma-visível) | Padrão `*` de CORS sobe sem alerta | Lacuna | Média | Corrigir na 1.1 |
| [LA09](#la09--fronteira-do-rnf02-não-está-declarada) | Alcance de "senha nunca armazenada" não delimitado | Ambiguidade | Média | **Corrigido** nesta elicitação |
| [LA10](#la10--limites-de-uso-do-serviço-não-especificados) | Sem requisito de volume, concorrência ou limite de uso | Lacuna | Média | Corrigir junto com RNF07 |

---

## LA01 — Força não mede entropia

**Onde:** RN06 · `generator.py:10-17` · tabela "Cálculo de Força da Senha" no README.

**O problema.** A classificação combina apenas *quantidade de tipos* e *tamanho*. Uma senha de 128 caracteres composta somente por minúsculas é rotulada **"fraca"**, embora seu espaço de busca (26¹²⁸, cerca de 601 bits) seja ordens de magnitude maior que o de uma senha de 16 caracteres com os quatro tipos (cerca de 104 bits) rotulada **"muito forte"**.

O termo "força", na interface, sugere ao usuário uma medida de resistência a ataque. O que o sistema entrega é uma medida de *conformidade com políticas de composição* — que é útil, mas é outra coisa.

**Por que passou despercebido.** A regra foi elicitada como heurística de usabilidade, não como medida criptográfica, e a documentação nunca explicitou essa diferença.

**Impacto.** O usuário pode aumentar desnecessariamente a complexidade da senha — piorando a memorização e a digitação — para escapar de um rótulo que não reflete risco real.

**Encaminhamento.** Aceitar na 1.0.0, com a limitação registrada na especificação (seção 1.4, verbete *Força*) e no critério de aceitação de HU05. Substituir por entropia em bits na 1.1 (HU12), mantendo os rótulos qualitativos como faixas derivadas do valor calculado.

---

## LA02 — O campo `forca` é string livre no contrato

**Onde:** `models.py:22` (`forca: str`) · `script.js:18-23`.

**O problema.** O frontend indexa um dicionário pela string exata devolvida pela API, incluindo o acento de `"média"`. Não há tipo enumerado no contrato que impeça o backend de devolver outro rótulo. Se alguém traduzir, capitalizar ou remover o acento no servidor, o frontend cai no *fallback* `?? STRENGTH['fraca']` — e passa a exibir **"Fraca" para qualquer senha**, silenciosamente, sem erro em log nem em console.

**Impacto.** Falha silenciosa que apresenta informação incorreta ao usuário justamente no ponto em que ele avalia a segurança da senha. É o pior tipo de degradação: parece funcionar.

**Encaminhamento.** Registrado como **RNF19** na especificação. Duas ações na 1.1: tipar `forca` como enumeração fechada no Pydantic, e fazer o frontend exibir estado indefinido — em vez de "Fraca" — quando receber valor fora do conjunto conhecido.

---

## LA03 — Mensagem de erro da API não chega ao usuário

**Onde:** `main.py:50-53` · `script.js:80-84` · README (contrato da API) · [docs/sequencia-api.md](../docs/sequencia-api.md).

**Duas discrepâncias encadeadas:**

1. **Documentação × implementação.** O README e o diagrama de sequência documentam a resposta 422 como `{"detail": "Pelo menos um tipo de caractere deve ser selecionado."}` — uma string. O handler implementado devolve `{"detail": exc.errors()}`, que é a **lista de objetos de erro do Pydantic**. Quem integrar com a API a partir da documentação vai tratar o campo errado.
2. **Implementação × usuário.** Mesmo tendo o motivo em mãos, o frontend descarta a resposta e exibe sempre o mesmo texto: *"Erro ao gerar a senha. Verifique os critérios e tente novamente."* O usuário não distingue "tamanho fora do intervalo" de "nenhum tipo selecionado".

**Por que passou despercebido.** O tratamento de erro global foi adicionado na Fase 5 (logging), depois que o contrato havia sido documentado na Fase 2. Nenhum teste compara documentação e resposta real — `test_resposta_422_contem_campo_detail` verifica apenas a **presença** do campo, não seu formato.

**Impacto.** Alto para integradores da API; médio para o usuário final, que consegue se recuperar por tentativa e erro.

**Encaminhamento.**
- **Agora:** corrigir o contrato documentado no README e em `docs/sequencia-api.md` para refletir o formato real.
- **1.1:** decidir entre normalizar a resposta 422 para `{"detail": "<mensagem legível>"}` — mais simples de consumir — ou manter o formato Pydantic e fazer o frontend traduzir os erros. Recomendação: normalizar, porque a API tem um único consumidor conhecido e o formato Pydantic vaza detalhes de implementação.

---

## LA04 — RNF02 e RNF03 não são verificados por teste

**Onde:** `backend/tests/` — a suíte cobre geração, modelos e API, mas nenhum teste toca log ou tempo de resposta.

**O problema.** Dois requisitos não funcionais críticos são afirmados na documentação e respeitados no código, mas **nada impede que uma alteração futura os viole sem que ninguém perceba**:

- **RNF02 (senha nunca logada).** Hoje `main.py` registra tamanho, tipos e força — nunca a senha. Um `logger.info("Senha gerada: %s", senha)` adicionado em depuração e esquecido no commit passaria por toda a suíte de testes.
- **RNF03 (resposta < 500 ms).** Nunca foi medido. O requisito nem sequer definia condição de medição — qual percentil, sob qual carga, com ou sem latência de rede.

**Impacto.** Alto. RNF02 é o requisito que sustenta a promessa central do produto; sua violação seria invisível.

**Encaminhamento.**
- RNF03 foi reescrito na especificação com condição mensurável (p95, tamanho ≤ 128, máquina local, sem latência de rede).
- **1.1:** adicionar teste com `caplog` que gere uma senha e afirme que a string gerada não aparece em nenhum registro capturado; adicionar teste de tempo de resposta na suíte ou no CI.

---

## LA05 — Confirmação de cópia não é verificada

**Onde:** `script.js:102-121`.

**O problema.** O bloco `catch` cobre a falha de `navigator.clipboard`, mas o mecanismo alternativo (`document.execCommand('copy')`) não tem seu retorno verificado, e o rótulo "Copiado!" é aplicado incondicionalmente depois dele. Se ambos os caminhos falharem, o usuário recebe confirmação de uma cópia que não ocorreu — e cola conteúdo antigo no formulário de destino.

Nenhum requisito da baseline definia o que fazer quando a cópia falha; a HU07 previa apenas o caminho feliz e o alternativo.

**Impacto.** Médio, e depende do ambiente: no caminho de uso previsto (HTTP em `localhost`) `navigator.clipboard` funciona.

**Encaminhamento.** 1.1 — verificar o retorno do mecanismo alternativo e exibir orientação de cópia manual em caso de falha. Critério de aceitação a acrescentar em HU07.

---

## LA06 — HU11 conflita com a regra de não trafegar senha em uso

**Onde:** RF13 / HU11 (backlog) × RNF01, RNF02.

**O conflito.** Toda a arquitetura se apoia em uma decisão: gerar no servidor é seguro porque a senha nasce lá, trafega uma única vez e nunca é armazenada. A funcionalidade "avaliar senha existente" inverte isso — o usuário enviaria ao servidor uma senha **já em uso**, possivelmente a de seu banco ou e-mail. Sem TLS (RNF06 ainda em aberto), ela trafegaria em texto claro; e a requisição atravessaria o mesmo handler que hoje registra logs de validação.

O risco não é hipotético: ele contradiz diretamente a justificativa apresentada aos stakeholders em [comunicacao/status-stackholders.md](../comunicacao/status-stackholders.md).

**Encaminhamento.** Não aceitar HU11 no escopo enquanto não houver decisão explícita entre duas alternativas:

| Alternativa | Consequência |
|-------------|--------------|
| **Avaliar no cliente** (JavaScript, senha nunca sai do navegador) | Preserva RNF02 integralmente; abre exceção controlada a RNF01, que passa a valer apenas para *geração* |
| **Avaliar no servidor sob TLS obrigatório** | Exige RNF06 implementado, log auditado e declaração explícita ao usuário |

**Recomendação:** avaliar no cliente. Cálculo de entropia não exige aleatoriedade criptográfica e, portanto, não precisa do servidor — o motivo que justificava RNF01 não se aplica a esta operação.

---

## LA07 — Ator operador não declarado na especificação

**Onde:** [docs/casos-de-uso.md](../docs/casos-de-uso.md) — diagrama original com um único ator.

**O problema.** Os requisitos de CORS, portas, TLS, rate limiting e documentação em produção pressupõem alguém que configure o ambiente. Esse ator não existia em nenhum artefato: os requisitos estavam escritos como propriedades do sistema, sem responsável. Consequência prática — nenhum artefato descrevia *o procedimento de publicação*, o que reaparece na análise de riscos como [R12](../riscos/identificacao.md) (ausência de homologação) e [R11](../riscos/identificacao.md) (conhecimento concentrado).

**Encaminhamento.** **Corrigido nesta elicitação:** ator declarado na especificação (seção 1.3), com UC04 e HU09 próprios.

---

## LA08 — Padrão inseguro de CORS não falha de forma visível

**Onde:** `main.py:24-28`.

**O problema.** Quando `ALLOWED_ORIGINS` não está definida, a aplicação assume `*` e sobe normalmente, registrando `CORS permitido para: ['*']` em nível INFO — indistinguível de qualquer outra linha de inicialização. O padrão inseguro é também o caminho de menor esforço, e nada sinaliza que uma decisão de segurança foi tomada por omissão.

Faltava um requisito descrevendo o comportamento esperado do sistema **em produção sem configuração**.

**Encaminhamento.** 1.1 — introduzir variável `ENV`; quando `ENV=production` e `ALLOWED_ORIGINS` ausente, registrar em nível WARNING (ou recusar a inicialização). Requisito a acrescentar como refinamento de RNF04. Mitiga o risco [R02](../riscos/analise.md).

---

## LA09 — Fronteira do RNF02 não está declarada

**Onde:** RNF02 — "a senha nunca é armazenada ou logada no servidor".

**A ambiguidade.** O enunciado pode ser lido como garantia absoluta de que a senha não persiste em lugar algum. Isso é falso e inevitavelmente falso: após a geração, a senha existe no DOM da página, no histórico de rede do navegador enquanto a aba estiver aberta e — se o usuário acionar UC02 — na área de transferência do sistema operacional, onde permanece após o fechamento da página e pode ser lida por outros aplicativos.

**Impacto.** Não é um defeito de implementação, é um limite de responsabilidade não documentado. Um leitor da documentação pode assumir uma garantia que o produto não pode oferecer.

**Encaminhamento.** **Corrigido nesta elicitação:** RNF02 delimitado como garantia do *sistema* (servidor), com a fronteira registrada na pós-condição de [UC02](casos-de-uso.md#uc02--copiar-senha-gerada) e nas premissas da especificação.

---

## LA10 — Limites de uso do serviço não especificados

**Onde:** ausente em todos os artefatos da Fase 1.

**O problema.** Nenhum requisito responde: quantos usuários simultâneos o serviço deve suportar? Quantas requisições por minuto uma origem pode fazer? Qual o tamanho máximo de um lote quando HU10 for implementada? A ausência é o que torna o risco [R03](../riscos/identificacao.md) (abuso da API) inevitável — não há critério contra o qual verificar uma proteção.

A premissa implícita de "uso individual e esporádico" foi assumida por todos, mas nunca escrita.

**Encaminhamento.** A premissa foi tornada explícita na especificação (seção 6). O requisito quantitativo — limite por IP/minuto e teto de lote — deve ser definido junto com RNF07, antes de qualquer publicação em ambiente público, e antes de aceitar HU10 no escopo.

---

## Questões em aberto para decisão

Itens que dependem de decisão do responsável pelo produto e que não podem ser resolvidos por análise técnica:

| # | Questão | Depende de | Bloqueia |
|---|---------|-----------|----------|
| Q1 | O indicador de força deve exibir o valor em bits, ou manter apenas o rótulo qualitativo? | Perfil do público-alvo | HU12 |
| Q2 | A avaliação de senha existente será feita no cliente ou no servidor? | Aceitação do risco de LA06 | HU11 |
| Q3 | Qual o limite aceitável de requisições por IP por minuto? | Expectativa de volume | RNF07, HU10 |
| Q4 | A resposta 422 será normalizada para mensagem legível ou manterá o formato Pydantic? | Existência de outros consumidores da API | LA03 |
| Q5 | Acessibilidade WCAG 2.1 AA é requisito de aceite ou melhoria opcional? | Contexto de uso e obrigações do projeto | RNF13 |
