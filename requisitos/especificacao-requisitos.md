# Especificação de Requisitos — Gerador de Senhas Seguras

**Versão do documento:** 1.0
**Baseline do produto:** 1.0.0
**Responsável:** Toledo Neto
**Data:** Julho de 2026

Este documento consolida os requisitos elicitados para o Gerador de Senhas Seguras. Ele refina e substitui, como fonte de verdade, a tabela resumida da *Fase 1* do [README.md](../README.md): os requisitos originais foram mantidos com os mesmos identificadores, mas receberam critério de verificação, origem e status.

A justificativa da escolha dos artefatos e o registro do uso de IA generativa estão em [ELICITACAO.md](ELICITACAO.md).

---

## 1. Escopo e contexto

### 1.1 Objetivo do produto

Permitir que qualquer pessoa gere uma senha aleatória de qualidade criptográfica, configurando tamanho e composição de caracteres, sem instalar software e sem que a senha seja armazenada em qualquer ponto do sistema.

### 1.2 Fora de escopo (baseline 1.0.0)

| Item | Motivo da exclusão |
|------|--------------------|
| Autenticação e contas de usuário | O produto não guarda estado; não há dado a proteger por sessão |
| Persistência ou histórico de senhas | Decisão de projeto: armazenar senha contradiz a proposta do produto |
| Geração em lote | Deferido para incremento futuro (ver [README — Próximos Passos](../README.md#próximos-passos)) |
| Interface responsiva / mobile | Deferido explicitamente na elicitação original |
| Internacionalização | Público-alvo definido como pt-BR |

### 1.3 Atores e partes interessadas

| Ator | Tipo | Interesse |
|------|------|-----------|
| **Usuário final** | Primário, humano | Obter uma senha forte rapidamente e copiá-la |
| **Operador de infraestrutura** | Secundário, humano | Publicar e manter a aplicação (CORS, portas, TLS, monitoramento) |
| **Sistema de monitoramento** | Secundário, sistema | Consultar `GET /health` periodicamente |
| Orientadores / avaliadores | Interessado, não-ator | Avaliar o processo de engenharia e a rastreabilidade |

> O **operador de infraestrutura** não estava previsto na elicitação original. Ele foi identificado durante esta revisão porque os requisitos RNF06, RNF08 e RNF09 só podem ser satisfeitos por alguém que configure o ambiente — ver [LA07](lacunas-ambiguidades.md#la07--ator-operador-não-declarado-na-especificação).

### 1.4 Glossário

| Termo | Definição adotada neste projeto |
|-------|--------------------------------|
| **Critério** | Parâmetro de entrada informado pelo usuário: tamanho e os quatro tipos de caractere |
| **Tipo de caractere** | Uma das quatro classes: maiúsculas (A–Z), minúsculas (a–z), números (0–9), especiais |
| **Charset** | União dos conjuntos de caracteres dos tipos ativos, usada como alfabeto de sorteio |
| **Força** | Rótulo qualitativo (`fraca`, `média`, `forte`, `muito forte`) derivado de tamanho e quantidade de tipos — **não** é entropia |
| **Entropia** | Medida em bits do espaço de busca da senha: `log₂(|charset| ^ tamanho)`. Não implementada na baseline |
| **CSPRNG** | Gerador pseudoaleatório criptograficamente seguro; no projeto, o módulo `secrets` do Python |
| **Stateless** | O backend não mantém nem persiste dado algum entre requisições |

---

## 2. Requisitos funcionais

Legenda de status: ✅ implementado na 1.0.0 · 📋 backlog · ⚠️ implementado com divergência.

| ID | Requisito | Prioridade | Origem | Verificação | Status |
|----|-----------|-----------|--------|-------------|--------|
| **RF01** | O usuário define o tamanho da senha, entre 8 e 128 caracteres | Must | Elicitação inicial | Slider em `index.html:39`; validação em `models.py:7`; teste `test_comprimento_da_senha_na_resposta` | ✅ |
| **RF02** | O usuário pode incluir ou excluir letras maiúsculas (A–Z) | Must | Elicitação inicial | `chkUppercase`; `generator.py:30` | ✅ |
| **RF03** | O usuário pode incluir ou excluir letras minúsculas (a–z) | Must | Elicitação inicial | `chkLowercase`; `generator.py:33` | ✅ |
| **RF04** | O usuário pode incluir ou excluir números (0–9) | Must | Elicitação inicial | `chkNumbers`; `generator.py:36` | ✅ |
| **RF05** | O usuário pode incluir ou excluir caracteres especiais do conjunto definido em RN05 | Must | Elicitação inicial | `chkSpecials`; `generator.py:39` | ✅ |
| **RF06** | O sistema gera **uma** senha por acionamento, a partir dos critérios vigentes | Must | Elicitação inicial | `POST /api/gerar-senha` | ✅ |
| **RF07** | O usuário pode copiar a senha exibida para a área de transferência com um clique | Should | Elicitação inicial | `script.js:102-121` | ✅ |
| **RF08** | O sistema exibe o indicador de força da senha recém-gerada | Should | Elicitação inicial | `exibirForca()`; `calcular_forca()` | ✅ |
| **RF09** | O sistema impede o acionamento da geração enquanto nenhum tipo de caractere estiver selecionado, informando o motivo | Must | Derivado de RN01 nesta revisão | `validarCriterios()` em `script.js:33-37` | ✅ |
| **RF10** | O sistema informa ao usuário quando não for possível concluir a geração (backend indisponível ou requisição rejeitada) | Must | Derivado do fluxo de exceção do UC01 | `script.js:80-93` | ⚠️ mensagem genérica — ver [LA03](lacunas-ambiguidades.md#la03--mensagem-de-erro-da-api-não-chega-ao-usuário) |
| **RF11** | O sistema expõe endpoint de verificação de saúde com status, versão e timestamp | Could | Fase 5 — Manutenção | `GET /health` em `main.py:57` | ✅ |
| **RF12** | O usuário pode gerar múltiplas senhas em uma única solicitação | Won't (1.0) / Should (1.1) | Backlog — README | — | 📋 |
| **RF13** | O usuário pode submeter uma senha própria e receber a avaliação de força | Won't (1.0) / Could (1.1) | Backlog — README | — | 📋 |
| **RF14** | O usuário pode excluir caracteres ambíguos (`0`/`O`, `1`/`l`/`I`) do charset | Won't (1.0) / Could (1.1) | Backlog — README | — | 📋 |
| **RF15** | O usuário pode alternar entre exibir e ocultar a senha na tela | Won't (1.0) / Could (1.1) | Backlog — README | — | 📋 |

---

## 3. Regras de negócio

| ID | Regra | Onde é aplicada | Status |
|----|-------|-----------------|--------|
| **RN01** | Pelo menos um tipo de caractere deve estar selecionado. Requisição sem nenhum tipo é rejeitada | `models.py:13-17` (backend) e `script.js:33` (frontend) | ✅ |
| **RN02** | O tamanho da senha deve estar no intervalo fechado [8, 128] | `models.py:7` (`ge=8, le=128`) e `min`/`max` do slider | ✅ |
| **RN03** | A senha gerada contém **ao menos um** caractere de cada tipo selecionado | `generator.py:30-41` (lista `garantidos`) | ✅ |
| **RN04** | Os critérios padrão, quando não informados, são: tamanho 16, maiúsculas e minúsculas ativas, números e especiais inativos | `models.py:7-11`; espelhado no HTML | ✅ |
| **RN05** | O conjunto de caracteres especiais é exatamente `` !@#$%^&*()_+-=[]{}|;':",.<>?/ `` — sem barra invertida e sem espaço | `generator.py:7` | ✅ |
| **RN06** | A força é classificada por tamanho **e** quantidade de tipos ativos, na primeira regra satisfeita de cima para baixo: muito forte (≥4 tipos e ≥16), forte (≥3 e ≥12), média (≥2 e ≥10), fraca (demais casos) | `generator.py:10-17` | ✅ |
| **RN07** | A senha é embaralhada após a montagem, de modo que a posição dos caracteres garantidos por RN03 não seja previsível | `generator.py:46` | ✅ |
| **RN08** | A geração é sempre feita no servidor; o cliente nunca produz a senha | Arquitetura — `script.js` só consome a API | ✅ |

### 3.1 Nota sobre RN03 × RN06

RN03 (garantir um de cada tipo) reduz marginalmente a entropia real em relação a um sorteio uniforme puro, porque fixa a composição da senha. A perda é irrelevante para os tamanhos praticados (≥ 8) e o ganho de usabilidade é alto — muitos sistemas exigem composição mínima. **Decisão:** manter RN03; registrar o trade-off. Ver [LA01](lacunas-ambiguidades.md#la01--força-não-mede-entropia).

---

## 4. Requisitos não funcionais

Organizados pelas características de qualidade da ISO/IEC 25010. Os RNF01–RNF03 originais foram preservados com os mesmos IDs e ganharam critério de aceitação mensurável.

### 4.1 Segurança

| ID | Requisito | Critério de verificação | Status |
|----|-----------|------------------------|--------|
| **RNF01** | A geração da senha ocorre exclusivamente no backend, usando CSPRNG do sistema operacional | Código usa `secrets`, nunca `random`; verificável por inspeção e por `grep` no repositório | ✅ |
| **RNF02** | A senha gerada nunca é persistida, cacheada ou registrada em log | Nenhuma escrita em disco/BD; nenhum `logger` recebe a senha como argumento | ⚠️ atendido no código, **sem teste automatizado** — ver [LA04](lacunas-ambiguidades.md#la04--rnf02-e-rnf03-não-são-verificados-por-teste) |
| **RNF04** | A API aceita requisições apenas das origens declaradas em `ALLOWED_ORIGINS` | Middleware CORS em `main.py:38-43`; verificação manual por requisição cross-origin | ✅ (código) / ⚠️ padrão `*` — risco [R02](../riscos/analise.md) |
| **RNF05** | Toda entrada é validada no servidor antes do processamento, retornando HTTP 422 em caso de violação | Modelos Pydantic; testes `test_payload_invalido_retorna_422` | ✅ |
| **RNF06** | Em produção, o tráfego entre cliente e servidor deve ocorrer sobre HTTPS/TLS | Certificado válido no endpoint público | 📋 risco [R01](../riscos/identificacao.md) |
| **RNF07** | A API deve limitar a taxa de requisições por origem em ambiente público | Limite configurável por IP/minuto; retorno HTTP 429 ao exceder | 📋 risco [R03](../riscos/identificacao.md) |
| **RNF08** | A documentação interativa (`/docs`) não deve estar acessível em produção | `docs_url=None` quando `ENV=production` | 📋 risco [R04](../riscos/identificacao.md) |
| **RNF09** | A senha exibida é inserida no DOM sem interpretação de HTML | Uso de `textContent` em `script.js:86` | ✅ |

### 4.2 Desempenho e eficiência

| ID | Requisito | Critério de verificação | Status |
|----|-----------|------------------------|--------|
| **RNF03** | O endpoint `POST /api/gerar-senha` responde em menos de 500 ms no percentil 95, para tamanho ≤ 128, em máquina local, desconsiderando latência de rede | Medição com 100 requisições sequenciais; p95 < 500 ms | ⚠️ não medido — ver [LA04](lacunas-ambiguidades.md#la04--rnf02-e-rnf03-não-são-verificados-por-teste) |
| **RNF10** | O backend é stateless: nenhuma requisição depende de estado deixado por outra | Reinício do processo entre requisições não altera comportamento | ✅ |

### 4.3 Usabilidade e acessibilidade

| ID | Requisito | Critério de verificação | Status |
|----|-----------|------------------------|--------|
| **RNF11** | A aplicação usa idioma pt-BR em toda a interface e nas mensagens ao usuário | Inspeção da interface; `lang="pt-BR"` no HTML | ✅ |
| **RNF12** | Mudanças de estado relevantes (força, erro) são anunciadas a leitores de tela | `aria-live="polite"` na linha de força; `role="alert"` na mensagem de erro | ✅ parcial |
| **RNF13** | A interface deve ser operável integralmente por teclado e atender contraste mínimo 4.5:1 (WCAG 2.1 AA) | Auditoria com axe/Lighthouse | 📋 backlog |
| **RNF14** | O layout deve se adaptar a telas de 320 px a 1920 px de largura | Inspeção em breakpoints | 📋 deferido na elicitação original |

### 4.4 Manutenibilidade e operação

| ID | Requisito | Critério de verificação | Status |
|----|-----------|------------------------|--------|
| **RNF15** | O backend registra início de aplicação, cada geração (sem a senha) e cada rejeição de validação | Logs observados em `main.py:45,80,90,52` | ✅ |
| **RNF16** | Endereço do backend e origens permitidas são configuráveis sem alteração de código-fonte | `frontend/config.js` e variável `ALLOWED_ORIGINS` | ✅ |
| **RNF17** | A suíte de testes do backend cobre lógica de geração, modelos e API | `pytest --cov`; 57 testes na baseline | ✅ |
| **RNF18** | Toda alteração relevante é registrada no CHANGELOG segundo *Keep a Changelog* | Inspeção do [CHANGELOG.md](../CHANGELOG.md) | ✅ |

---

## 5. Requisitos de interface externa

### 5.1 Contrato da API

O contrato completo está em [docs/sequencia-api.md](../docs/sequencia-api.md). Dois pontos de atenção levantados nesta elicitação:

1. O campo `forca` é tipado como `str` livre em `models.py:22`. Como o frontend faz *lookup* por string exata — incluindo o acento de `"média"` — qualquer mudança de rótulo no backend quebra o indicador silenciosamente. **Requisito derivado (RNF19):** o campo `forca` deve ser um tipo enumerado fechado, e o frontend deve degradar de forma segura para valor desconhecido. Status: 📋 — hoje há apenas o *fallback* `?? STRENGTH['fraca']`, que exibe rótulo incorreto em vez de sinalizar o desconhecido.
2. O corpo da resposta 422 documentado (`{"detail": "mensagem"}`) **não corresponde** ao implementado (`{"detail": [lista de erros Pydantic]}`). Ver [LA03](lacunas-ambiguidades.md#la03--mensagem-de-erro-da-api-não-chega-ao-usuário).

### 5.2 Variáveis de ambiente

| Variável | Componente | Padrão | Requisito relacionado |
|----------|-----------|--------|----------------------|
| `ALLOWED_ORIGINS` | backend | `*` | RNF04 |
| `PORT` | backend | `8000` | RNF16 |
| `PORT` | frontend | `3000` | RNF16 |

---

## 6. Premissas e restrições

| Tipo | Item |
|------|------|
| Premissa | O usuário confia no servidor que hospeda a aplicação — a senha é gerada remotamente por decisão de projeto (RNF01) |
| Premissa | O ambiente de execução dispõe de fonte de entropia adequada para o módulo `secrets` |
| Premissa | Uso individual e esporádico; não há requisito de concorrência elevada na baseline |
| Restrição | Stack fixada na elicitação: Python/FastAPI no backend; HTML, CSS e JS sem framework no frontend |
| Restrição | Sem banco de dados — imposta pela regra de não persistência |
| Restrição | Projeto conduzido por um único desenvolvedor (risco [R11](../riscos/identificacao.md)) |

---

## 7. Documentos relacionados

| Documento | Conteúdo |
|-----------|----------|
| [ELICITACAO.md](ELICITACAO.md) | Processo de elicitação, escolha dos artefatos e uso de IA generativa |
| [historias-de-usuario.md](historias-de-usuario.md) | Histórias de usuário e critérios de aceitação em Gherkin |
| [casos-de-uso.md](casos-de-uso.md) | Casos de uso expandidos com fluxos alternativos e de exceção |
| [lacunas-ambiguidades.md](lacunas-ambiguidades.md) | Lacunas, ambiguidades e questões em aberto |
| [prototipo.md](prototipo.md) | Protótipo de baixa fidelidade e estados da interface |
| [matriz-rastreabilidade.md](matriz-rastreabilidade.md) | Rastreabilidade requisito ↔ artefato ↔ código ↔ teste ↔ risco |
