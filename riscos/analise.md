# Análise de Riscos — Gerador de Senhas Seguras

Este documento analisa cada risco identificado em `identificacao.md`, avaliando probabilidade de ocorrência, impacto potencial, nível de risco resultante e os fatores condicionantes que determinam essas classificações.

---

## Escala de Avaliação

| Dimensão     | Baixo (1)                                    | Médio (2)                                      | Alto (3)                                         |
|--------------|----------------------------------------------|------------------------------------------------|--------------------------------------------------|
| Probabilidade | Improvável dado o contexto atual             | Possível; já houve situação semelhante         | Provável ou já em andamento                     |
| Impacto       | Inconveniência pontual, fácil de reverter   | Degradação visível, correção custosa           | Perda de dados, indisponibilidade ou dano legal |

**Nível de Risco = Probabilidade × Impacto**

| Faixa  | Classificação |
|--------|---------------|
| 1–2    | Baixo         |
| 3–4    | Médio         |
| 6–9    | Alto          |

---

## R01 — Exposição de dados em trânsito sem HTTPS

| Dimensão          | Valor | Justificativa                                                                                   |
|-------------------|-------|-------------------------------------------------------------------------------------------------|
| **Probabilidade** | Alta (3) | Não existe configuração de TLS no projeto. Qualquer deploy em servidor público ocorre em HTTP. |
| **Impacto**       | Alto (3) | A senha gerada — o produto principal — trafega em texto claro. Interceptação compromete diretamente a segurança do usuário. |
| **Nível**         | **Alto (9)** | — |

**Fatores condicionantes:**
- Ausência de `Dockerfile`, Nginx ou qualquer configuração de proxy reverso no repositório.
- O projeto não documenta um processo de deploy em produção; a configuração de TLS ficaria a cargo do operador sem referência.
- A natureza da aplicação (geração de senhas) amplifica o impacto: o dado interceptado é exatamente o que o usuário confia ao sistema.

---

## R02 — CORS permissivo em produção

| Dimensão          | Valor | Justificativa                                                                                      |
|-------------------|-------|----------------------------------------------------------------------------------------------------|
| **Probabilidade** | Média (2) | O `.env.example` documenta o valor padrão como `*`. Um operador desatento manterá esse padrão. |
| **Impacto**       | Médio (2) | Permite que sites maliciosos façam requisições à API em nome do usuário (CSRF). O impacto é limitado porque o backend é stateless e não há dados pessoais armazenados. |
| **Nível**         | **Médio (4)** | — |

**Fatores condicionantes:**
- A correção já está implementada no código (`ALLOWED_ORIGINS` configurável via variável de ambiente); o risco é operacional, não de código.
- O impacto é moderado porque a API não autentica usuários nem armazena estado — o pior cenário é uso indevido da capacidade computacional do servidor.
- O risco sobe para Alto se rate limiting não for implementado (R03), pois CORS permissivo + sem rate limit = API aberta ao mundo.

---

## R03 — API sem rate limiting, sujeita a abuso

| Dimensão          | Valor | Justificativa                                                                                        |
|-------------------|-------|------------------------------------------------------------------------------------------------------|
| **Probabilidade** | Alta (3) | Não há nenhum mecanismo de controle implementado. Em ambiente público, scrapers e bots atingem APIs sem proteção com frequência. |
| **Impacto**       | Alto (3) | Sobrecarga do servidor pode tornar a aplicação indisponível para usuários legítimos. Em escala extrema, eleva custo de infraestrutura ou derruba o processo. |
| **Nível**         | **Alto (9)** | — |

**Fatores condicionantes:**
- O backend é stateless e não exige autenticação, tornando cada endpoint trivialmente acessível.
- A geração de senha com `secrets.choice()` é leve em CPU, mas volume extremo de requisições pode saturar a conexão de rede ou o worker do uvicorn.
- A falta de CI/CD (R08) significa que `slowapi` (mencionado nos próximos passos) não será cobrado automaticamente pelo pipeline.

---

## R04 — Swagger UI exposto em produção

| Dimensão          | Valor | Justificativa                                                                                           |
|-------------------|-------|---------------------------------------------------------------------------------------------------------|
| **Probabilidade** | Alta (3) | O FastAPI habilita `/docs` por padrão. Sem configuração explícita (`docs_url=None`), a interface estará disponível. |
| **Impacto**       | Baixo (1) | A API é pública e sem autenticação. O Swagger expõe informações já visíveis para quem fizer uma requisição. O risco real é de reconhecimento facilitado para atacantes. |
| **Nível**         | **Médio (3)** | — |

**Fatores condicionantes:**
- O impacto seria maior se a API tivesse endpoints administrativos ou exigisse autenticação — neste projeto, os danos são limitados.
- Crawlers e scanners de segurança indexam `/docs` ativamente, aumentando a superfície de exposição.
- A correção é trivial (uma linha de código) e está documentada nos "Próximos Passos".

---

## R05 — Arquivos de servidor acessíveis pelo browser

| Dimensão          | Valor | Justificativa                                                                                                |
|-------------------|-------|--------------------------------------------------------------------------------------------------------------|
| **Probabilidade** | Alta (3) | O `server.js` serve toda a pasta `frontend/` sem restrição. O comportamento atual já expõe os arquivos. |
| **Impacto**       | Baixo (1) | `server.js` e `package.json` não contêm segredos. Expõem versões de dependências e estrutura de código, úteis para reconhecimento, mas sem dados sensíveis. |
| **Nível**         | **Médio (3)** | — |

**Fatores condicionantes:**
- Se variáveis de ambiente forem incorporadas no código do frontend (antipadrão), o impacto subiria imediatamente para Alto.
- A correção (mover estáticos para `public/`) está planejada, mas não implementada.

---

## R06 — Commit acidental de variáveis de ambiente sensíveis

| Dimensão          | Valor | Justificativa                                                                                         |
|-------------------|-------|-------------------------------------------------------------------------------------------------------|
| **Probabilidade** | Baixa (1) | O `.gitignore` já protege `.env`. O risco é residual e exige uma ação equivocada explícita do desenvolvedor. |
| **Impacto**       | Médio (2) | Em produção futura com chaves de API, banco de dados ou serviços de e-mail, a exposição de `.env` seria crítica. No estado atual, o impacto é limitado a configurações de CORS e porta. |
| **Nível**         | **Baixo (2)** | — |

**Fatores condicionantes:**
- O risco aumenta à medida que o projeto evolui e mais variáveis sensíveis são adicionadas ao `.env`.
- O uso de `git add .` ou `git add -A` em vez de staging seletivo é o vetor mais comum.

---

## R07 — Ausência de testes automatizados no frontend

| Dimensão          | Valor | Justificativa                                                                                                 |
|-------------------|-------|---------------------------------------------------------------------------------------------------------------|
| **Probabilidade** | Alta (3) | O frontend não tem nenhum teste. Qualquer alteração em `script.js` já opera sem cobertura automatizada. |
| **Impacto**       | Médio (2) | Regressões no frontend são visíveis ao usuário (erro ao copiar senha, indicador de força errado), mas não comprometem a segurança da geração. |
| **Nível**         | **Alto (6)** | — |

**Fatores condicionantes:**
- As features planejadas (histórico de sessão, modo escuro, avaliação de senha existente) aumentarão a complexidade do `script.js`, elevando a probabilidade de regressão.
- Testes E2E com Playwright estão listados nos "Próximos Passos", mas sem prazo ou prioridade definida.

---

## R08 — Sem pipeline de CI/CD configurado

| Dimensão          | Valor | Justificativa                                                                                                     |
|-------------------|-------|-------------------------------------------------------------------------------------------------------------------|
| **Probabilidade** | Alta (3) | Não existe nenhum arquivo de CI no repositório (`.github/workflows/`, `.gitlab-ci.yml`, etc.). O risco já é realidade. |
| **Impacto**       | Médio (2) | Sem CI, testes e auditorias de segurança dependem de disciplina manual. A probabilidade de omissão aumenta sob pressão de prazo. |
| **Nível**         | **Alto (6)** | — |

**Fatores condicionantes:**
- A combinação de R08 (sem CI) + R13 (dependências não monitoradas) + R07 (sem testes de frontend) forma um cluster de risco que se reforça mutuamente.
- O Makefile já centraliza os comandos (`make test`, `make audit`), o que facilita a criação de um pipeline de CI — a barreira de implementação é baixa.

---

## R09 — Cobertura de testes não monitorada

| Dimensão          | Valor | Justificativa                                                                                                          |
|-------------------|-------|------------------------------------------------------------------------------------------------------------------------|
| **Probabilidade** | Média (2) | A cobertura atual é alta para o backend, mas sem threshold mínimo configurado, novas funcionalidades podem reduzi-la silenciosamente. |
| **Impacto**       | Baixo (1) | O impacto imediato é baixo; o risco se materializa progressivamente e geralmente é detectado antes de causar falhas críticas. |
| **Nível**         | **Baixo (2)** | — |

**Fatores condicionantes:**
- Nenhum threshold definido no `pyproject.toml` (`fail_under` do coverage).
- O risco é secundário enquanto o projeto tem apenas um desenvolvedor com bom conhecimento do código.

---

## R10 — Escopo crescente não gerenciado (feature creep)

| Dimensão          | Valor | Justificativa                                                                                          |
|-------------------|-------|--------------------------------------------------------------------------------------------------------|
| **Probabilidade** | Alta (3) | 16 itens de backlog identificados; sem sistema de rastreamento formal (Jira, Linear, GitHub Projects). |
| **Impacto**       | Médio (2) | Trabalho incompleto e dívida técnica aumentam o custo de manutenção, mas o produto atual é funcional e estável. |
| **Nível**         | **Alto (6)** | — |

**Fatores condicionantes:**
- O projeto é acadêmico/pessoal, o que reduz a pressão formal de entrega, mas aumenta o risco de que backlog não priorizado nunca seja executado — ou seja executado de forma aleatória.
- Features de áreas diferentes (segurança, UI, infraestrutura) competem por atenção sem critério de prioridade definido.

---

## R11 — Conhecimento concentrado em um único desenvolvedor

| Dimensão          | Valor | Justificativa                                                                                                    |
|-------------------|-------|------------------------------------------------------------------------------------------------------------------|
| **Probabilidade** | Alta (3) | O contexto do projeto (pós-graduação, desenvolvimento solo) confirma que não há bus factor maior que 1. |
| **Impacto**       | Alto (3) | Em caso de indisponibilidade do desenvolvedor, qualquer incidente — desde uma dependência comprometida até uma falha de deploy — ficaria sem resposta. |
| **Nível**         | **Alto (9)** | — |

**Fatores condicionantes:**
- A documentação do projeto é boa (README detalhado, CHANGELOG, PROMPTS.md), o que mitiga parcialmente o risco de onboarding.
- O risco é inerente ao modelo de projeto solo e só pode ser transferido com a adição de colaboradores ou documentação operacional ainda mais detalhada (runbooks).

---

## R12 — Ausência de ambiente de homologação

| Dimensão          | Valor | Justificativa                                                                                                     |
|-------------------|-------|-------------------------------------------------------------------------------------------------------------------|
| **Probabilidade** | Alta (3) | Não existe referência a nenhum ambiente além do desenvolvimento local. Deploys em produção partem diretamente do ambiente local. |
| **Impacto**       | Médio (2) | Diferenças de configuração podem causar falhas silenciosas. A ausência de homologação aumenta o tempo de diagnóstico de incidentes. |
| **Nível**         | **Alto (6)** | — |

**Fatores condicionantes:**
- A ausência de containerização (R16) amplifica este risco: sem Docker, reproduzir o ambiente de produção localmente é difícil.
- O impacto sobe para Alto se features de infraestrutura (HTTPS, rate limiting) forem configuradas diretamente em produção sem teste prévio.

---

## R13 — Dependências desatualizadas com vulnerabilidades

| Dimensão          | Valor | Justificativa                                                                                               |
|-------------------|-------|-------------------------------------------------------------------------------------------------------------|
| **Probabilidade** | Média (2) | Dependências como fastapi e uvicorn recebem atualizações frequentes. Sem CI rodando `pip-audit`/`npm audit`, gaps de atualização se acumulam. |
| **Impacto**       | Alto (3) | Vulnerabilidades em dependências de servidores (uvicorn, express) podem comprometer o host. CVEs em Pydantic ou FastAPI já foram reportados no passado. |
| **Nível**         | **Alto (6)** | — |

**Fatores condicionantes:**
- O Makefile já inclui `make audit`, mas sem CI esse comando precisa ser executado manualmente.
- A documentação de gestão de dependências em `docs/gestao-dependencias.md` mitiga parcialmente o risco ao definir frequência de atualização.

---

## R14 — Incompatibilidade de licenças

| Dimensão          | Valor | Justificativa                                                                                                  |
|-------------------|-------|----------------------------------------------------------------------------------------------------------------|
| **Probabilidade** | Baixa (1) | FastAPI (MIT), Uvicorn (BSD), Pydantic (MIT) e Express (MIT) são compatíveis com a licença MIT do projeto. O risco é baixo no estado atual. |
| **Impacto**       | Médio (2) | Se o projeto evoluir para uso comercial ou redistribuição, dependências com licenças GPL ou LGPL podem impor restrições não previstas. |
| **Nível**         | **Baixo (2)** | — |

**Fatores condicionantes:**
- Risco latente: baixo agora, mas deve ser reavaliado se novas dependências forem adicionadas sem verificação de licença.

---

## R15 — Sem monitoramento de disponibilidade em produção

| Dimensão          | Valor | Justificativa                                                                                              |
|-------------------|-------|------------------------------------------------------------------------------------------------------------|
| **Probabilidade** | Alta (3) | Não existe referência a nenhuma ferramenta de monitoramento. O endpoint `/health` existe, mas não há nada que o consulte. |
| **Impacto**       | Médio (2) | Falhas silenciosas podem durar horas. O impacto é degradado pela natureza do serviço: não é crítico (não há transações financeiras ou dados de saúde). |
| **Nível**         | **Alto (6)** | — |

**Fatores condicionantes:**
- O endpoint `/health` já existe e é a base para qualquer solução de monitoramento — a barreira de implementação é baixa.
- Ferramentas gratuitas (UptimeRobot, Better Uptime) podem ser integradas sem código adicional.

---

## R16 — Ausência de containerização

| Dimensão          | Valor | Justificativa                                                                                               |
|-------------------|-------|-------------------------------------------------------------------------------------------------------------|
| **Probabilidade** | Alta (3) | O projeto não tem Dockerfile. Qualquer deploy em novo servidor exige configuração manual do ambiente.      |
| **Impacto**       | Médio (2) | Onboarding mais lento e maior risco de inconsistências de ambiente. Não afeta a funcionalidade do produto já implantado. |
| **Nível**         | **Alto (6)** | — |

**Fatores condicionantes:**
- Docker está listado nos "Próximos Passos" com prioridade não definida.
- O risco se materializa principalmente ao escalar ou ao adicionar colaboradores ao projeto.

---

## Matriz de Riscos

|     | **Impacto Baixo (1)** | **Impacto Médio (2)**        | **Impacto Alto (3)**         |
|-----|-----------------------|------------------------------|------------------------------|
| **Probabilidade Alta (3)**  | R04, R05 | R03¹, R07, R08, R10, R12, R15, R16 | R01, R11 |
| **Probabilidade Média (2)** | R09 | R02, R13 | — |
| **Probabilidade Baixa (1)** | — | R06, R14 | — |

> ¹ R03 foi classificado com Impacto Alto nesta análise. Aparece aqui agrupado por simplificação visual — ver análise detalhada acima.

---

## Riscos Prioritários (Nível Alto)

| Prioridade | ID  | Risco                                        | Nível |
|------------|-----|----------------------------------------------|-------|
| 1          | R01 | Sem HTTPS em produção                        | 9     |
| 2          | R11 | Conhecimento concentrado em 1 desenvolvedor  | 9     |
| 3          | R03 | API sem rate limiting                        | 9     |
| 4          | R07 | Sem testes no frontend                       | 6     |
| 5          | R08 | Sem pipeline CI/CD                           | 6     |
| 6          | R10 | Escopo crescente não gerenciado              | 6     |
| 7          | R12 | Ausência de ambiente de homologação          | 6     |
| 8          | R13 | Dependências com vulnerabilidades            | 6     |
| 9          | R15 | Sem monitoramento de disponibilidade         | 6     |
| 10         | R16 | Ausência de containerização                  | 6     |
