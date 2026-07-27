# Matriz de Rastreabilidade

Liga cada requisito ao artefato que o descreve, ao código que o implementa, ao teste que o verifica e ao risco que o ameaça. A matriz existe para responder três perguntas de forma objetiva:

1. Todo requisito tem alguém que o verifica?
2. Toda linha de código relevante atende a algum requisito declarado?
3. Se um requisito mudar, o que precisa ser revisto junto?

---

## 1. Requisitos funcionais → artefatos → verificação

| Requisito | História | Caso de uso | Implementação | Verificação | Status |
|-----------|----------|-------------|---------------|-------------|--------|
| RF01 — tamanho 8–128 | HU01 | UC01 (2), UC06 | `models.py:7`, `index.html:39` | `test_comprimento_da_senha_na_resposta`, `test_payload_invalido_retorna_422` | ✅ |
| RF02 — maiúsculas | HU02 | UC01 (3, 7) | `generator.py:30-32` | `test_generator.py` (presença/ausência por tipo) | ✅ |
| RF03 — minúsculas | HU02 | UC01 (3, 7) | `generator.py:33-35` | `test_generator.py` | ✅ |
| RF04 — números | HU02 | UC01 (3, 7) | `generator.py:36-38` | `test_generator.py` | ✅ |
| RF05 — especiais | HU02 | UC01 (3, 7) | `generator.py:7,39-41` | `test_generator.py` (charset exclusivo) | ✅ |
| RF06 — uma senha por acionamento | HU04 | UC01 | `main.py:77-91` | `test_resposta_contem_campos_senha_e_forca` | ✅ |
| RF07 — copiar com um clique | HU07 | UC02 | `script.js:102-121` | ⚠️ apenas manual — sem teste de frontend ([R07](../riscos/identificacao.md)) | ✅ |
| RF08 — indicador de força | HU05 | UC01 (9), UC05 | `generator.py:10-17`, `script.js:43-49` | `test_calcular_forca`, `test_forca_retornada_pela_api` | ✅ |
| RF09 — bloqueio sem tipo selecionado | HU03 | UC01/A1, UC06 | `script.js:33-37`, `models.py:13-17` | `test_payload_invalido_retorna_422` (servidor) · manual (cliente) | ✅ |
| RF10 — informar falha ao usuário | HU06 | UC01/E1, UC01/E2 | `script.js:80-93` | ⚠️ sem teste · divergência em [LA03](lacunas-ambiguidades.md#la03--mensagem-de-erro-da-api-não-chega-ao-usuário) | ⚠️ |
| RF11 — endpoint de saúde | HU08 | UC03 | `main.py:57-64` | ⚠️ sem teste automatizado | ✅ |
| RF12 — geração em lote | HU10 | — | — | — | 📋 |
| RF13 — avaliar senha existente | HU11 | — | — | bloqueado por [LA06](lacunas-ambiguidades.md#la06--hu11-conflita-com-a-regra-de-não-trafegar-senha-em-uso) | 📋 |
| RF14 — excluir ambíguos | HU13 | — | — | — | 📋 |
| RF15 — exibir/ocultar senha | — | — | — | ver decisão D6 do [protótipo](prototipo.md#decisões-de-interface-registradas) | 📋 |

---

## 2. Regras de negócio → onde vivem

| Regra | Ponto de aplicação | Verificação | Consequência se removida |
|-------|-------------------|-------------|--------------------------|
| RN01 — ao menos um tipo | `models.py:13-17` + `script.js:33` | `test_payload_invalido_retorna_422` | `secrets.choice("")` lançaria exceção — erro 500 em vez de 422 |
| RN02 — tamanho [8, 128] | `models.py:7` + atributos do slider | `test_comprimento_da_senha_na_resposta` | Senhas triviais (tamanho 1) ou requisições de custo arbitrário |
| RN03 — um char de cada tipo | `generator.py:30-41` | `test_generator.py` | Senha poderia não conter um tipo pedido, sendo rejeitada pelo sistema de destino |
| RN04 — critérios padrão | `models.py:7-11` + HTML | `test_body_vazio_usa_valores_padrao` | Divergência silenciosa entre o que a tela mostra e o que a API assume |
| RN05 — conjunto de especiais | `generator.py:7` | teste de charset exclusivo | Reintrodução do bug de barra invertida corrigido na Fase 4 |
| RN06 — classificação de força | `generator.py:10-17` | `test_calcular_forca` (limites de cada faixa) | Indicador inconsistente com a documentação |
| RN07 — embaralhamento | `generator.py:46` | ⚠️ sem teste específico | Posição previsível dos caracteres garantidos por RN03 |
| RN08 — geração no servidor | Arquitetura | inspeção | Perda da garantia de CSPRNG (RNF01) |

---

## 3. Requisitos não funcionais → verificação

| RNF | Como é verificado hoje | Lacuna | Risco associado |
|-----|------------------------|--------|-----------------|
| RNF01 — CSPRNG no backend | Inspeção de código (`secrets`, nunca `random`) | Nenhuma verificação automatizada impede a troca | — |
| RNF02 — senha nunca logada | Inspeção de `main.py` | **Sem teste** — [LA04](lacunas-ambiguidades.md#la04--rnf02-e-rnf03-não-são-verificados-por-teste) | — |
| RNF03 — resposta < 500 ms (p95) | — | **Nunca medido** — [LA04](lacunas-ambiguidades.md#la04--rnf02-e-rnf03-não-são-verificados-por-teste) | — |
| RNF04 — CORS restrito | Log de inicialização | Padrão inseguro silencioso — [LA08](lacunas-ambiguidades.md#la08--padrão-inseguro-de-cors-não-falha-de-forma-visível) | [R02](../riscos/identificacao.md) |
| RNF05 — validação no servidor | `test_payload_invalido_retorna_422` | — | — |
| RNF06 — HTTPS em produção | — | Não implementado | [R01](../riscos/identificacao.md) |
| RNF07 — rate limiting | — | Sem limite definido — [LA10](lacunas-ambiguidades.md#la10--limites-de-uso-do-serviço-não-especificados) | [R03](../riscos/identificacao.md) |
| RNF08 — `/docs` fechado em produção | — | Não implementado | [R04](../riscos/identificacao.md) |
| RNF09 — sem injeção de HTML | Inspeção (`textContent`) | Sem teste de frontend | [R07](../riscos/identificacao.md) |
| RNF10 — stateless | Inspeção arquitetural | — | — |
| RNF11 — idioma pt-BR | Inspeção | — | — |
| RNF12 — anúncio a leitores de tela | Inspeção (`aria-live`, `role="alert"`) | Sem auditoria de acessibilidade | — |
| RNF13 — WCAG 2.1 AA | — | Não avaliado | — |
| RNF14 — responsividade | — | Deferido na elicitação | — |
| RNF15 — logging estruturado | Observação em execução | Sem teste | — |
| RNF16 — configuração externalizada | `config.js`, `ALLOWED_ORIGINS` | — | — |
| RNF17 — cobertura de testes do backend | `pytest --cov` | Sem threshold mínimo | [R09](../riscos/identificacao.md) |
| RNF18 — CHANGELOG mantido | Inspeção | Processo manual | — |
| RNF19 — `forca` como tipo fechado | — | Não implementado — [LA02](lacunas-ambiguidades.md#la02--o-campo-forca-é-string-livre-no-contrato) | — |

---

## 4. Cobertura reversa — código sem requisito declarado

Varredura no sentido inverso: trechos implementados que não correspondiam a nenhum requisito escrito antes desta elicitação.

| Trecho | O que faz | Situação |
|--------|-----------|----------|
| `main.py:50-53` — handler de validação | Padroniza a resposta 422 e registra a rejeição | Coberto agora por RF10 e RNF15; formato divergia da documentação ([LA03](lacunas-ambiguidades.md#la03--mensagem-de-erro-da-api-não-chega-ao-usuário)) |
| `main.py:67-74` — `_tipos_ativos` | Monta a lista de tipos para o log | Coberto agora por RNF15; comprova que a senha não é logada |
| `script.js:107-117` — fallback de cópia | Cópia em contexto não seguro | Coberto agora por UC02/E1; comportamento em falha não especificado ([LA05](lacunas-ambiguidades.md#la05--confirmação-de-cópia-não-é-verificada)) |
| `script.js:44` — `?? STRENGTH['fraca']` | Fallback de rótulo desconhecido | Comportamento indesejado, não requisito — origem de [LA02](lacunas-ambiguidades.md#la02--o-campo-forca-é-string-livre-no-contrato) |
| `generator.py:46` — embaralhamento | Evita posição previsível | Coberto agora por RN07; sem teste dedicado |

**Conclusão da varredura:** nenhum código implementado ficou sem requisito correspondente após esta revisão — mas cinco trechos existiam sem respaldo documental, todos originados de decisões tomadas durante a codificação e nunca reincorporadas à especificação. É a evidência mais direta de por que a elicitação precisou ser revisitada.

---

## 5. Impacto de mudança

Se algum destes requisitos for alterado, os itens da coluna direita precisam ser revistos na mesma mudança.

| Se mudar… | Revisar |
|-----------|---------|
| **RN02** (intervalo de tamanho) | `models.py`, atributos do slider, testes de fronteira, HU01, tabela de RN06 |
| **RN05** (conjunto de especiais) | `generator.py`, rótulo do checkbox, contrato documentado, teste de charset, HU02 |
| **RN06** (regra de força) | `generator.py`, `STRENGTH` no frontend, tabelas em README e `docs/fluxo-geracao.md`, exemplos de `EXEMPLOS.md`, HU05, UC05 |
| **Formato da resposta 422** | `main.py`, `script.js`, README, `docs/sequencia-api.md`, `EXEMPLOS.md`, teste de 422, HU06 |
| **RNF01** (geração no servidor) | Toda a arquitetura — invalida RN08, UC01 e a justificativa apresentada aos stakeholders |

> A linha de RN06 é a mais cara: a mesma regra está duplicada em **seis lugares**, três deles documentação. É um candidato natural a consolidação quando HU12 (entropia) for implementada.
