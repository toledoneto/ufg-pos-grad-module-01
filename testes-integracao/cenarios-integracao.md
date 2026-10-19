# Cenários de Integração — Frontend ↔ Backend

> Artefato gerado pelo **Prompt 01** (tipo *"Cenários de integração + contrato de API"*) — ver [PROMPTS.md](../PROMPTS.md#módulo-13-testes-de-software-automatizados-com-inteligência-artificial-generativa-c13-es-t1).
> Testes automatizados: [backend/tests/integracao/test_contrato_frontend_backend.py](../backend/tests/integracao/test_contrato_frontend_backend.py) e [backend/tests/integracao/test_fluxo_http_real.py](../backend/tests/integracao/test_fluxo_http_real.py).

## 1. Contrato implícito extraído do frontend

O frontend não compartilha tipos com o backend: o contrato existe apenas no JavaScript. A LLM leu `script.js`, `config.js` e `index.html` e extraiu:

| Item | Onde está no frontend | Valor esperado pelo frontend | Onde está no backend | Situação |
|------|----------------------|------------------------------|----------------------|----------|
| URL e método | `config.js` → `API_URL`; `script.js` → `fetch(..., {method: 'POST'})` | `POST /api/gerar-senha` | `main.py` → `@app.post("/api/gerar-senha")` | ✅ Coincide |
| Campos do payload | `script.js` → `const payload` | `tamanho`, `maiusculas`, `minusculas`, `numeros`, `especiais` | `models.py` → `SenhaRequest` | ✅ Coincide |
| Limites do tamanho | `index.html` → `<input type="range" min="8" max="128">` | 8 a 128 | `Field(ge=8, le=128)` | ✅ Coincide |
| Valor inicial | `index.html` → `value="16"` | 16 | `tamanho = 16` | ✅ Coincide |
| Campos lidos da resposta | `script.js` → `data.senha`, `data.forca` | `senha`, `forca` | `SenhaResponse` | ✅ Coincide |
| Níveis de força exibidos | `script.js` → `STRENGTH` | `fraca`, `média`, `forte`, `muito forte` | `calcular_forca()` | ✅ Coincide (nível desconhecido cairia em silêncio no fallback `fraca`) |
| Tratamento de erro | `script.js` → `await resp.json()` **antes** de `if (!resp.ok)` | Toda resposta de erro precisa ser JSON | `validation_exception_handler` | ❌ **Defeito** — ver [casos-de-erro.md](casos-de-erro.md#defeitos-encontrados) |
| CORS | navegador em `http://localhost:3000` | Preflight `POST` + `Content-Type` liberado | `CORSMiddleware` + `ALLOWED_ORIGINS` | ✅ Coincide |

### Divergência com a documentação

O contrato publicado no [README.md](../README.md#contrato-da-api) mostra o erro 422 como:

```json
{ "detail": "Pelo menos um tipo de caractere deve ser selecionado." }
```

O formato real do FastAPI é uma **lista de objetos**:

```json
{ "detail": [ { "type": "value_error", "loc": ["body"], "msg": "Value error, Pelo menos um tipo de caractere deve ser selecionado.", "input": { "...": "..." } } ] }
```

O frontend atual não lê `detail`, então isso não quebra a interface hoje, mas qualquer cliente novo escrito a partir do README trataria o erro errado. **Recomendação:** corrigir o README.

## 2. Cenários de integração

| ID | Objetivo | Componentes integrados | Pré-condição | Passos | Resultado esperado | Teste automatizado |
|----|----------|------------------------|--------------|--------|--------------------|--------------------|
| CI-01 | A rota que o frontend chama existe | `config.js` ↔ rotas FastAPI | — | Extrair o caminho de `API_URL` e procurar nas rotas `POST` do app | Caminho presente como `POST` | `test_rota_configurada_no_frontend_existe_no_backend_como_post` |
| CI-02 | Payload do frontend = modelo do backend | `script.js` ↔ `SenhaRequest` | — | Extrair chaves de `const payload` e comparar com `model_fields` | Conjuntos idênticos (nem campo a mais, nem a menos) | `test_payload_do_frontend_tem_exatamente_os_campos_do_senha_request` |
| CI-03 | Slider não permite valores que o backend rejeita | `index.html` ↔ `Field(ge, le)` | — | Ler `min`/`max` do slider e as restrições do Pydantic | `(8, 128)` nos dois lados | `test_limites_do_slider_coincidem_com_a_validacao_do_backend` |
| CI-04 | Padrão do slider = padrão da API | `index.html` ↔ `SenhaRequest.tamanho` | — | Ler `value` do slider e o *default* do modelo | Ambos 16 | `test_valor_inicial_do_slider_coincide_com_o_padrao_do_backend` |
| CI-05 | Frontend só lê campos que a API devolve | `script.js` ↔ `SenhaResponse` | — | Extrair todos os `data.<campo>` | Subconjunto de `{senha, forca}` | `test_frontend_le_apenas_campos_presentes_na_resposta` |
| CI-06 | Todo nível de força tem exibição | `calcular_forca` ↔ `STRENGTH` | — | Calcular força para todo tamanho 8–128 × 1–4 tipos | Todos os níveis existem em `STRENGTH` | `test_todo_nivel_de_forca_do_backend_tem_exibicao_no_frontend` |
| CI-07 | OpenAPI publica o contrato real | FastAPI ↔ `/openapi.json` | — | Gerar o schema e verificar respostas, campos obrigatórios e limites | `200`/`422` declarados; `senha`, `forca` obrigatórios; `minimum=8`, `maximum=128` | `test_openapi_publica_o_contrato_consumido_pelo_frontend` |
| CI-08 | Health check sobre HTTP real | uvicorn ↔ `/health` | API em processo separado | `GET /health` | `200`, `status=ok`, `version=1.0.0` | `test_health_check_disponivel_sobre_http` |
| CI-09 | Fluxo feliz ponta a ponta para cada nível de força | uvicorn → CORS → Pydantic → gerador → serialização | API em processo separado | `POST` com o mesmo payload que o frontend monta e `Origin: http://localhost:3000` | `200`, `application/json`, comprimento correto, força esperada | `test_fluxo_feliz_com_payload_identico_ao_do_frontend` (4 casos) |
| CI-10 | Especiais (`"`, `\`, `'`…) sobrevivem ao JSON | gerador ↔ serialização ↔ cliente | API em processo separado | Gerar 128 chars só de especiais | Todos os caracteres no charset; comprimento 128 | `test_caracteres_especiais_sobrevivem_a_serializacao_json` |
| CI-11 | Preflight do navegador é aceito | navegador ↔ `CORSMiddleware` | API em processo separado | `OPTIONS` com `Access-Control-Request-Method: POST` e `-Headers: Content-Type` | `200`, `POST` e `Content-Type` permitidos | `test_preflight_cors_do_navegador_e_aceito` |
| CI-12 | Erro 422 também carrega CORS | `CORSMiddleware` ↔ handler de erro | API em processo separado | `POST` inválido com `Origin` | `422` com `Access-Control-Allow-Origin` (senão o navegador esconde o erro) | `test_resposta_de_erro_422_tambem_carrega_cabecalho_cors` |
| CI-13 | Preflight rejeita método/cabeçalho não permitidos | navegador ↔ `CORSMiddleware` | API em processo separado | `OPTIONS` pedindo `PUT`; depois `POST` + `Authorization` | `400` com motivo | `test_preflight_rejeita_metodo_ou_cabecalho_nao_permitido` (2 casos) |
| CI-14 | `ALLOWED_ORIGINS` restrito aceita o frontend | variável de ambiente ↔ `CORSMiddleware` | API com `ALLOWED_ORIGINS=http://localhost:3000` | `POST` com essa origem | `200`, `Access-Control-Allow-Origin: http://localhost:3000` | `test_cors_restrito_aceita_a_origem_do_frontend` |
| CI-15 | `ALLOWED_ORIGINS` restrito bloqueia outras origens | variável de ambiente ↔ `CORSMiddleware` | API com `ALLOWED_ORIGINS=http://localhost:3000` | `POST` e `OPTIONS` com origem desconhecida | Sem cabeçalho CORS no `POST`; `400` no preflight | `test_cors_restrito_nao_libera_origem_desconhecida` |

## 3. Resultado da execução

```
tests/integracao/test_contrato_frontend_backend.py .......               [ 7 passed ]
tests/integracao/test_fluxo_http_real.py ............                    [12 passed ]
```

Todos os 19 testes dos cenários CI-01 a CI-15 passaram. O único defeito de integração do contrato (tratamento de erro) aparece nos casos de erro do Prompt 02.
