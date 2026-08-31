# Estratégias de Resposta a Riscos — Gerador de Senhas Seguras

Este documento define, para cada risco identificado em `identificacao.md` e analisado em `analise.md`, a estratégia de resposta adotada — evitar, mitigar, transferir ou aceitar — com justificativa explícita para cada escolha.

---

## Glossário de Estratégias

| Estratégia  | Definição                                                                                      |
|-------------|------------------------------------------------------------------------------------------------|
| **Evitar**  | Eliminar a causa raiz do risco, removendo a atividade que o gera ou alterando o plano.        |
| **Mitigar** | Reduzir a probabilidade de ocorrência e/ou o impacto caso o risco se materialize.            |
| **Transferir** | Deslocar o impacto financeiro ou operacional para um terceiro (seguro, SLA, fornecedor).  |
| **Aceitar** | Reconhecer o risco e não tomar ação proativa; pode ser ativa (com plano de contingência) ou passiva. |

---

## R01 — Exposição de dados em trânsito sem HTTPS

**Estratégia: Mitigar**

**Ações:**
1. Adicionar ao repositório um arquivo `nginx.conf` de referência configurando HTTPS com proxy reverso para o uvicorn.
2. Documentar em `docs/deploy.md` o processo de obtenção de certificado TLS gratuito com Let's Encrypt via Certbot.
3. Incluir verificação de protocolo no `server.js`: exibir aviso no console se o servidor detectar que está rodando em HTTP em modo de produção (`NODE_ENV=production`).

**Justificativa:** O risco não pode ser evitado (HTTPS é indispensável para qualquer aplicação pública) nem transferido (a responsabilidade de infraestrutura é do projeto). A mitigação via documentação e template de configuração reduz a probabilidade de um operador implantar a aplicação sem TLS. A aceitação passiva seria inaceitável dado que o produto central — a senha gerada — trafega na resposta HTTP.

---

## R02 — CORS permissivo em produção

**Estratégia: Mitigar**

**Ações:**
1. Alterar o valor padrão de `ALLOWED_ORIGINS` no `backend/.env.example` de `*` para um placeholder explícito como `https://meudominio.com`, forçando o operador a preencher conscientemente.
2. Adicionar uma verificação de inicialização em `main.py`: se `ALLOWED_ORIGINS == "*"` e a variável de ambiente `ENV` indicar produção, emitir um log de nível `WARNING` alertando sobre a configuração permissiva.

**Justificativa:** A correção de código já foi implementada (variável de ambiente configurável). A mitigação adicional via `.env.example` e warning de inicialização torna o risco operacional explícito e autodocumentado, sem necessidade de alterar a lógica de negócio. Evitar completamente (forçar origens específicas) prejudicaria o uso em desenvolvimento local.

---

## R03 — API sem rate limiting, sujeita a abuso

**Estratégia: Mitigar**

**Ações:**
1. Adicionar `slowapi` como dependência ao `pyproject.toml` e `requirements.txt`.
2. Implementar limite de 60 requisições/minuto por IP no endpoint `POST /api/gerar-senha`, retornando HTTP 429 com cabeçalho `Retry-After` quando excedido.
3. Registrar o evento de rate limit nos logs para facilitar identificação de padrões de abuso.

**Justificativa:** Evitar completamente implicaria tornar a API privada (autenticação), o que vai contra o objetivo do projeto. Transferir (uso de WAF de terceiros como Cloudflare) é uma opção válida em produção real, mas adiciona dependência externa. Mitigar via `slowapi` é a resposta proporcional ao tamanho do projeto: baixo custo de implementação, impacto direto no nível de risco mais crítico (9 → 3).

---

## R04 — Swagger UI exposto em produção

**Estratégia: Mitigar**

**Ações:**
1. Ler a variável de ambiente `ENV` em `main.py` e passar `docs_url=None, redoc_url=None` ao construtor do `FastAPI()` quando `ENV=production`.
2. Documentar a variável `ENV` no `backend/.env.example`.

**Código sugerido:**
```python
is_production = os.getenv("ENV", "development") == "production"
app = FastAPI(
    title="Gerador de Senhas Seguras",
    docs_url=None if is_production else "/docs",
    redoc_url=None if is_production else "/redoc",
)
```

**Justificativa:** A solução é trivial (< 5 linhas) e elimina o risco em produção sem prejudicar a experiência de desenvolvimento. Evitar completamente (remover a documentação em todos os ambientes) reduziria a utilidade do FastAPI no desenvolvimento. Aceitar seria negligente dado o esforço mínimo de implementação.

---

## R05 — Arquivos de servidor acessíveis pelo browser

**Estratégia: Mitigar**

**Ações:**
1. Criar a subpasta `frontend/public/` e mover `index.html`, `style.css`, `script.js` e `config.js` para ela.
2. Atualizar `server.js` para servir apenas `frontend/public/` com `express.static(path.join(__dirname, 'public'))`.

**Justificativa:** A mitigação é direta e já está descrita nos "Próximos Passos" do README. Aceitar passivamente seria razoável enquanto `server.js` não contém segredos, mas a reorganização de pastas é uma mudança de baixo risco e alto benefício que deve ser feita antes de qualquer deploy público.

---

## R06 — Commit acidental de variáveis de ambiente sensíveis

**Estratégia: Aceitar (ativa)**

**Ações do plano de contingência:**
1. Se ocorrer, revogar imediatamente quaisquer credenciais expostas (chaves de API, senhas).
2. Usar `git filter-repo` para remover o arquivo do histórico e fazer force-push.
3. Notificar qualquer colaborador que tenha clonado o repositório após o commit comprometido.

**Justificativa:** O `.gitignore` já mitiga preventivamente o risco principal. O risco residual (commit explícito do arquivo ou inclusão de credenciais em outros arquivos) é baixo e exigiria uma ação deliberadamente errada do desenvolvedor. Medidas adicionais como hooks de pre-commit (git-secrets, trufflehog) seriam desproporcionais ao projeto atual, mas devem ser reavaliadas se o projeto ganhar colaboradores ou dados sensíveis reais.

---

## R07 — Ausência de testes automatizados no frontend

**Estratégia: Mitigar**

**Ações:**
1. Configurar o Vitest como dependência de desenvolvimento no `frontend/package.json` para testes unitários da lógica em `script.js` (validação de critérios, parsing de resposta da API).
2. Adicionar ao menos um teste E2E com Playwright cobrindo o fluxo principal: preencher critérios → clicar em "Gerar" → verificar exibição da senha e do indicador de força.
3. Integrar a execução dos testes de frontend ao `make test` do Makefile.

**Justificativa:** O risco já tem nível Alto (6) e aumentará conforme features de frontend forem implementadas. Evitar (não adicionar features ao frontend) não é uma opção viável. Aceitar sem plano seria irresponsável dado que o risco se materializará com alta probabilidade a cada mudança no `script.js`.

---

## R08 — Sem pipeline de CI/CD configurado

**Estratégia: Mitigar**

**Ações:**
1. Criar `.github/workflows/ci.yml` com os jobs:
   - `test-backend`: `uv run pytest --cov`
   - `audit-backend`: `uv run pip-audit`
   - `audit-frontend`: `npm audit --audit-level=moderate`
2. Configurar o pipeline para rodar em todo push ao branch `main` e em pull requests.
3. Usar cache de dependências (uv cache, npm cache) para manter tempo de execução abaixo de 3 minutos.

**Justificativa:** O Makefile já centraliza todos os comandos necessários, tornando a criação do CI trivial. A ausência de CI é o multiplicador de risco mais importante do projeto: sem ele, R07 (sem testes de frontend), R09 (cobertura não monitorada) e R13 (dependências vulneráveis) nunca são verificados automaticamente. O custo de implementação é baixo; o benefício é sistêmico.

---

## R09 — Cobertura de testes não monitorada

**Estratégia: Aceitar (ativa)**

**Ações:**
1. Definir `fail_under = 80` na seção `[tool.pytest.ini_options]` ou `[tool.coverage.report]` do `pyproject.toml`.
2. Revisar a cobertura a cada nova feature adicionada ao backend.

**Justificativa:** O risco atual é Baixo (2) e o backend já possui alta cobertura. Investir em ferramentas de monitoramento contínuo de cobertura (Codecov, Coveralls) seria desproporcional ao tamanho do projeto. A aceitação ativa com threshold mínimo configurado é a resposta adequada.

---

## R10 — Escopo crescente não gerenciado (feature creep)

**Estratégia: Mitigar**

**Ações:**
1. Organizar os 16 itens de backlog em categorias de prioridade (Must/Should/Could) no `CHANGELOG.md` ou em um `BACKLOG.md` dedicado.
2. Adotar a regra de "um item em andamento por vez": nenhuma nova feature começa antes da anterior ser concluída e testada.
3. Revisar o backlog a cada versão liberada, marcando itens concluídos e ajustando prioridades.

**Justificativa:** Evitar completamente implicaria congelar o backlog, o que vai contra a natureza evolutiva do projeto. Aceitar sem estrutura resultaria em fragmentação do esforço. A mitigação via priorização explícita é de baixo custo e mantém o projeto evoluindo de forma controlada.

---

## R11 — Conhecimento concentrado em um único desenvolvedor

**Estratégia: Mitigar**

**Ações:**
1. Criar `docs/runbook.md` com procedimentos operacionais: como iniciar/parar serviços, como fazer deploy, como reverter uma versão, como responder a incidentes comuns.
2. Garantir que o `CHANGELOG.md` registre não apenas "o que mudou" mas também "por que mudou", preservando o raciocínio das decisões.
3. A longo prazo: convidar um segundo colaborador para code review, mesmo que informal.

**Justificativa:** Evitar (distribuir o conhecimento a múltiplos colaboradores) não é viável no contexto de um projeto solo de pós-graduação. Transferir (terceirizar a operação) seria desproporcional. A mitigação via documentação operacional reduz o impacto de uma eventual indisponibilidade do desenvolvedor e é a resposta mais custo-efetiva.

---

## R12 — Ausência de ambiente de homologação

**Estratégia: Mitigar**

**Ações:**
1. Implementar R16 (containerização com Docker) primeiro: com `docker-compose.yml`, o ambiente de homologação pode ser criado em qualquer máquina com um único comando.
2. Definir um processo de deploy em dois estágios: branch `main` → homologação (validação manual) → produção.

**Justificativa:** Criar um servidor de homologação dedicado seria desproporcional ao tamanho do projeto. A containerização (R16) resolve indiretamente R12: um `docker-compose.yml` é, na prática, um ambiente de homologação reproduzível. As duas ações são interdependentes e devem ser tratadas juntas.

---

## R13 — Dependências desatualizadas com vulnerabilidades

**Estratégia: Mitigar**

**Ações:**
1. Incluir `pip-audit` e `npm audit` no pipeline de CI (R08), falhando o build em vulnerabilidades de severidade alta ou crítica.
2. Configurar alertas automáticos do GitHub Dependabot para criar pull requests de atualização de dependências.
3. Seguir o calendário de atualização definido em `docs/gestao-dependencias.md`: patches a cada 2 semanas, minors mensalmente, majors com avaliação manual.

**Justificativa:** Evitar dependências externas não é viável — FastAPI, Pydantic e Express são parte central da arquitetura. Transferir (uso de distribuições corporativas com suporte de segurança) seria desproporcional. A mitigação via Dependabot + CI é a prática padrão da indústria e tem custo próximo de zero.

---

## R14 — Incompatibilidade de licenças

**Estratégia: Aceitar (passiva)**

**Justificativa:** As dependências atuais (FastAPI/MIT, Uvicorn/BSD-3, Pydantic/MIT, Express/MIT, Python/PSF) são todas compatíveis com a licença MIT do projeto. O risco só se tornará relevante se novas dependências com licenças restritivas (GPL, LGPL, AGPL) forem adicionadas ou se o projeto for distribuído comercialmente. A reavaliação deve ocorrer a cada nova dependência adicionada.

---

## R15 — Sem monitoramento de disponibilidade em produção

**Estratégia: Mitigar**

**Ações:**
1. Configurar monitoramento gratuito via UptimeRobot ou BetterUptime apontando para `GET /health`.
2. Configurar alertas por e-mail em caso de indisponibilidade.
3. Definir SLO informal: disponibilidade-alvo de 99% em horário comercial.

**Justificativa:** O endpoint `/health` já existe — a implementação do monitoramento é configuração, não código. Aceitar passivamente (sem monitoramento) significaria descobrir falhas apenas quando usuários reportassem, o que é inaceitável para qualquer serviço público. O custo da mitigação é zero (ferramentas gratuitas disponíveis).

---

## R16 — Ausência de containerização

**Estratégia: Mitigar**

**Ações:**
1. Criar `backend/Dockerfile` com build em múltiplos estágios (builder + runtime), usando imagem base `python:3.12-slim`.
2. Criar `frontend/Dockerfile` usando `node:lts-alpine` com apenas as dependências de produção.
3. Criar `docker-compose.yml` na raiz orquestrando backend e frontend com variáveis de ambiente configuráveis.
4. Atualizar o `Makefile` com `make docker-up` e `make docker-down`.

**Justificativa:** Evitar (desenvolver sem dependências externas) eliminaria os benefícios das stacks escolhidas. A containerização é o padrão da indústria para garantir reprodutibilidade de ambiente e é pré-requisito para R12 (homologação) e para deploy escalável. O esforço de implementação é médio, mas o retorno é sistêmico.

---

## Mapa de Respostas

| ID  | Risco                                        | Nível | Estratégia   | Prazo Sugerido |
|-----|----------------------------------------------|-------|--------------|----------------|
| R01 | Sem HTTPS em produção                        | 9     | Mitigar      | Antes do 1º deploy público |
| R03 | API sem rate limiting                        | 9     | Mitigar      | Antes do 1º deploy público |
| R11 | Conhecimento concentrado em 1 desenvolvedor  | 9     | Mitigar      | Contínuo       |
| R07 | Sem testes no frontend                       | 6     | Mitigar      | Próxima iteração |
| R08 | Sem pipeline CI/CD                           | 6     | Mitigar      | Próxima iteração |
| R10 | Escopo crescente não gerenciado              | 6     | Mitigar      | Imediato       |
| R12 | Ausência de ambiente de homologação          | 6     | Mitigar      | Com R16        |
| R13 | Dependências com vulnerabilidades            | 6     | Mitigar      | Com R08 (CI)   |
| R15 | Sem monitoramento de disponibilidade         | 6     | Mitigar      | Antes do 1º deploy público |
| R16 | Ausência de containerização                  | 6     | Mitigar      | Próxima iteração |
| R02 | CORS permissivo em produção                  | 4     | Mitigar      | Antes do 1º deploy público |
| R04 | Swagger UI exposto em produção               | 3     | Mitigar      | Antes do 1º deploy público |
| R05 | Arquivos de servidor acessíveis              | 3     | Mitigar      | Próxima iteração |
| R06 | Commit acidental de .env                     | 2     | Aceitar (ativa) | Contingência  |
| R09 | Cobertura não monitorada                     | 2     | Aceitar (ativa) | Com R08 (CI) |
| R14 | Incompatibilidade de licenças                | 2     | Aceitar (passiva) | Revisar a cada nova dependência |
