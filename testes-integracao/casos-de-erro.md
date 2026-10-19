# Casos de Erro e Dados de Teste — Integração

> Artefato gerado pelo **Prompt 02** (tipo *"Casos de erro + dados de teste"*) — ver [PROMPTS.md](../PROMPTS.md#módulo-13-testes-de-software-automatizados-com-inteligência-artificial-generativa-c13-es-t1).
> Dados: [backend/tests/integracao/dados/casos_erro.json](../backend/tests/integracao/dados/casos_erro.json) · Teste: [backend/tests/integracao/test_casos_erro_orientado_a_dados.py](../backend/tests/integracao/test_casos_erro_orientado_a_dados.py)

## Por que orientado a dados

Os casos ficam em um JSON separado do código de teste. Para adicionar um caso novo basta incluir uma entrada no arquivo, sem escrever Python. O mesmo arquivo pode ser importado no Postman ou no Insomnia. O corpo é guardado como **string bruta**, o que permite enviar JSON inválido e `Content-Type` arbitrário, coisas que um `json=` do cliente HTTP não conseguiria representar.

Cada caso é enviado para a **API real** (uvicorn em processo separado) e validado contra três regras:

1. o status HTTP é o esperado;
2. o `Content-Type` é `application/json`. É um requisito do consumidor: o frontend faz `await resp.json()` antes de checar `resp.ok`;
3. o corpo tem `detail`. Nos erros de validação, `detail` é uma lista de objetos com `type`, `loc` e `msg`, e contém o `type` esperado.

## Casos de erro

| ID | Descrição | Requisição | Esperado | Observado | Situação |
|----|-----------|------------|----------|-----------|----------|
| CE-01 | JSON malformado (truncado) | `POST` `application/json` `{"tamanho":` | 422 `json_invalid` | 422 `json_invalid` | ✅ |
| CE-02 | Requisição sem corpo | `POST` sem corpo | 422 `missing` | 422 `missing` | ✅ |
| CE-03 | Corpo é array | `[16, true]` | 422 `model_attributes_type` | 422 `model_attributes_type` | ✅ |
| CE-04 | JSON com `Content-Type: text/plain` | `{"tamanho": 16}` | 422 `model_attributes_type` (JSON) | **500 `Internal Server Error` (texto puro)** | ❌ Defeito D-01 |
| CE-05 | Formulário HTML | `tamanho=16&maiusculas=true` | 422 `model_attributes_type` (JSON) | **500 `Internal Server Error` (texto puro)** | ❌ Defeito D-01 |
| CE-06 | Nenhum tipo selecionado (regra de negócio RN) | todos `false` | 422 `value_error` (JSON) | **500 `Internal Server Error` (texto puro)** | ❌ Defeito D-01 |
| CE-07 | Tamanho 7 | `{"tamanho":7}` | 422 `greater_than_equal` | 422 `greater_than_equal` | ✅ |
| CE-08 | Tamanho 129 | `{"tamanho":129}` | 422 `less_than_equal` | 422 `less_than_equal` | ✅ |
| CE-09 | Tamanho negativo | `{"tamanho":-16}` | 422 `greater_than_equal` | 422 `greater_than_equal` | ✅ |
| CE-10 | Tamanho 10^30 | `{"tamanho":1e30 inteiro}` | 422 `less_than_equal` | 422 `less_than_equal` | ✅ |
| CE-11 | Tamanho fracionário | `{"tamanho":16.5}` | 422 `int_from_float` | 422 `int_from_float` | ✅ |
| CE-12 | Tamanho `null` | `{"tamanho":null}` | 422 `int_type` | 422 `int_type` | ✅ |
| CE-13 | Tamanho texto | `{"tamanho":"dezesseis"}` | 422 `int_parsing` | 422 `int_parsing` | ✅ |
| CE-14 | Booleano `2` | `{"numeros":2}` | 422 `bool_parsing` | 422 `bool_parsing` | ✅ |
| CE-15 | Booleano `"sim"` | `{"especiais":"sim"}` | 422 `bool_parsing` | 422 `bool_parsing` | ✅ |
| CE-16 | Método errado | `GET /api/gerar-senha` | 405 JSON | 405 `{"detail":"Method Not Allowed"}` | ✅ |
| CE-17 | Rota com erro de digitação | `POST /api/gerar_senha` | 404 JSON | 404 `{"detail":"Not Found"}` | ✅ |

## Valores de fronteira válidos

| ID | Descrição | Corpo | Esperado | Situação |
|----|-----------|-------|----------|----------|
| CF-01 | Mínimo | `{"tamanho":8}` | 200, senha com 8 chars | ✅ |
| CF-02 | Máximo | `{"tamanho":128}` | 200, senha com 128 chars | ✅ |
| CF-03 | Corpo vazio | `{}` | 200, padrão de 16 chars | ✅ |
| CF-04 | Campo desconhecido | `{"tamanho":12,"historico":true}` | 200, campo ignorado | ✅ |

## Coerções a decidir (não são defeitos)

O Pydantic, em modo *lax* (padrão), converte alguns tipos automaticamente. O frontend nunca envia esses valores, mas um cliente de terceiros pode enviar. Os testes registram o comportamento atual e ficam como **decisão pendente do time**:

| ID | Corpo | Comportamento atual | Se adotar `strict=True` |
|----|-------|---------------------|-------------------------|
| CC-01 | `{"tamanho":"16"}` | 200 (string vira int) | 422 `int_type` |
| CC-02 | `{"tamanho":16.0}` | 200 (float inteiro vira int) | 422 `int_type` |
| CC-03 | `{"numeros":"true"}` | 200 (string vira bool) | 422 `bool_type` |
| CC-04 | `{"numeros":1}` | 200 (1 vira `true`) | 422 `bool_type` |

## Defeitos encontrados

### D-01 — Handler de validação quebra com 500 quando o erro contém objetos não serializáveis

- **Onde:** [backend/main.py:53](../backend/main.py#L53) → `JSONResponse(status_code=422, content={"detail": exc.errors()})`
- **Causa:** `exc.errors()` pode conter objetos Python que não são JSON:
  - no `model_validator` (CE-06), `ctx.error` é a instância de `ValueError`;
  - em `text/plain` e formulário (CE-04, CE-05), `input` é `bytes`.

  O `json.dumps` do Starlette lança `TypeError`, e o cliente recebe `500 Internal Server Error` em **texto puro**, sem cabeçalho CORS.
- **Impacto na integração:** o cenário mais comum de erro de negócio, **nenhum tipo selecionado**, retorna 500 em vez de 422. Como a resposta não é JSON, o `resp.json()` do frontend lança exceção, cai no `catch`, e o usuário lê *"Não foi possível conectar ao servidor"*, uma mensagem falsa. Hoje o frontend desabilita o botão quando nenhum checkbox está marcado, o que esconde o defeito na interface, mas qualquer outro cliente (Postman, integração de terceiros) o encontra.
- **Detecção:** os testes unitários existentes `test_payload_invalido_retorna_422[payload0-nenhum tipo selecionado]` e `test_resposta_422_contem_campo_detail` em `tests/test_api.py` **já falhavam** com as versões atuais das dependências (FastAPI 0.136.1 / Pydantic 2.13.3 / Starlette 1.0.0). Os testes de integração confirmaram o defeito sobre HTTP real e encontraram dois gatilhos novos (CE-04 e CE-05).
- **Correção sugerida** (uma linha, validada numa cópia do projeto: 134/134 testes passando):

  ```python
  from fastapi.encoders import jsonable_encoder
  ...
  return JSONResponse(status_code=422, content={"detail": jsonable_encoder(exc.errors())})
  ```

- **Decisão:** o código da aplicação **não foi alterado** neste exercício. Os testes continuam afirmando o comportamento correto e permanecem vermelhos até a correção ser aplicada.

## Resultado da execução

```
tests/integracao/test_casos_erro_orientado_a_dados.py ...FFF............ .......
FAILED ...[CE-04 Corpo JSON enviado com Content-Type text/plain]          assert 500 == 422
FAILED ...[CE-05 Formulário HTML (application/x-www-form-urlencoded)]     assert 500 == 422
FAILED ...[CE-06 Nenhum tipo de caractere selecionado (regra de negócio)] assert 500 == 422
========================= 3 failed, 22 passed =========================
```
