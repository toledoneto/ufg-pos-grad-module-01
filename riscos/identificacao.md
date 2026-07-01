# Identificação de Riscos — Gerador de Senhas Seguras

Este documento lista os riscos identificados ao longo de todo o ciclo de vida do projeto — do levantamento de requisitos à manutenção em produção. Cada risco recebe um identificador único, descrição e o contexto no qual pode ocorrer.

---

## Categoria 1 — Segurança e Infraestrutura

### R01 — Exposição de dados em trânsito sem HTTPS

**Descrição:** A aplicação não possui configuração de TLS/HTTPS, fazendo com que a senha gerada trafegue em texto claro entre o backend e o frontend.

**Contexto de ocorrência:** Fase de implantação em produção. Se o servidor for publicado na internet sem certificado TLS configurado, qualquer atacante com acesso à rede (man-in-the-middle) poderá interceptar as senhas geradas antes que cheguem ao usuário.

---

### R02 — CORS permissivo em produção

**Descrição:** O parâmetro `ALLOWED_ORIGINS` pode ser deixado com o valor padrão `*`, permitindo que qualquer domínio na internet faça requisições à API de geração de senhas.

**Contexto de ocorrência:** Fase de configuração do ambiente de produção. Ocorre quando o operador sobe o backend sem definir a variável de ambiente `ALLOWED_ORIGINS`, revertendo ao comportamento permissivo documentado em `.env.example`.

---

### R03 — API sem rate limiting, sujeita a abuso

**Descrição:** Não existe controle de número de requisições por IP ou por sessão. A API pode ser chamada indefinidamente sem restrição.

**Contexto de ocorrência:** Fase de operação em produção com acesso público. Um agente malicioso pode disparar milhares de requisições por segundo, sobrecarregando o servidor ou explorando a API como oráculo criptográfico.

---

### R04 — Swagger UI exposto em produção

**Descrição:** O FastAPI sobe a interface de documentação interativa (`/docs`) por padrão. Em produção, essa interface expõe o contrato completo da API a qualquer pessoa que a acesse.

**Contexto de ocorrência:** Toda vez que o backend for iniciado sem desabilitar `docs_url` no construtor do `FastAPI()`. O risco se concretiza quando o ambiente é público e o endpoint `/docs` é descoberto por crawlers ou scanners de segurança.

---

### R05 — Arquivos de configuração do servidor acessíveis pelo navegador

**Descrição:** O `server.js` (Express) serve todos os arquivos da pasta `frontend/`, incluindo o próprio `server.js` e o `package.json`. Qualquer usuário pode baixar esses arquivos pelo browser.

**Contexto de ocorrência:** Fase de produção, sem a reorganização da estrutura de pastas descrita nos "Próximos Passos" (mover estáticos para `public/`).

---

### R06 — Commit acidental de variáveis de ambiente sensíveis

**Descrição:** O arquivo `.env` com configurações reais (origens CORS, portas, chaves futuras) pode ser adicionado ao repositório por engano, expondo configurações de produção publicamente.

**Contexto de ocorrência:** Fase de codificação ou manutenção, especialmente ao commitar com `git add .` ou `git add -A`. O `.gitignore` já protege contra isso, mas commits históricos ou configurações incorretas do git podem contornar a proteção.

---

## Categoria 2 — Qualidade e Testes

### R07 — Ausência de testes automatizados no frontend

**Descrição:** A suíte de testes cobre apenas o backend (57 testes com pytest). Nenhum teste unitário ou end-to-end cobre o frontend (HTML/CSS/JS).

**Contexto de ocorrência:** Fases de codificação e manutenção. Alterações em `script.js`, `index.html` ou `style.css` podem introduzir regressões (falha no fetch, exibição incorreta da força, botão de cópia quebrado) sem que qualquer teste automatizado detecte.

---

### R08 — Sem pipeline de CI/CD configurado

**Descrição:** Não existe automação de integração e entrega contínua. Testes e auditorias de segurança só são executados quando o desenvolvedor os roda manualmente.

**Contexto de ocorrência:** Toda vez que um pull request é aberto ou código é enviado ao repositório. Na ausência de CI, um commit com teste falhando ou dependência vulnerável pode chegar ao branch principal sem ser detectado.

---

### R09 — Cobertura de testes não monitorada ao longo do tempo

**Descrição:** Embora o projeto suporte relatório de cobertura via `pytest-cov`, não há threshold mínimo configurado nem histórico de cobertura acumulado. Novas funcionalidades podem ser adicionadas sem testes correspondentes.

**Contexto de ocorrência:** Fase de manutenção e evolução do produto. À medida que features dos "Próximos Passos" forem implementadas, a cobertura pode cair progressivamente.

---

## Categoria 3 — Projeto e Escopo

### R10 — Escopo crescente não gerenciado (feature creep)

**Descrição:** O README documenta 16 melhorias futuras em áreas distintas (funcionalidades, UI, qualidade, infraestrutura). Sem priorização formal, há risco de o projeto crescer de forma desordenada, diluindo foco e aumentando complexidade.

**Contexto de ocorrência:** Fase de manutenção e evolução. Ocorre quando múltiplas melhorias são iniciadas em paralelo sem critério de prioridade, gerando trabalho incompleto e dívida técnica acumulada.

---

### R11 — Concentração de conhecimento em um único desenvolvedor

**Descrição:** O projeto foi desenvolvido e é mantido por uma única pessoa. Todo o conhecimento sobre decisões de arquitetura, configuração de ambiente e lógica de negócio está centralizado nesse indivíduo.

**Contexto de ocorrência:** Fases de codificação, manutenção e operação. Em caso de indisponibilidade do desenvolvedor (férias, saída do projeto), qualquer incidente em produção ou demanda de evolução ficará bloqueada.

---

### R12 — Ausência de ambiente de homologação

**Descrição:** Não existe um ambiente intermediário (staging/homologação) entre o desenvolvimento local e a produção. Mudanças são validadas apenas em ambiente de desenvolvimento.

**Contexto de ocorrência:** Fase de implantação de novas versões. Diferenças de configuração entre o ambiente local e o servidor de produção (portas, variáveis de ambiente, versões de SO) podem causar falhas que não foram detectadas localmente.

---

## Categoria 4 — Dependências e Conformidade

### R13 — Vulnerabilidades introduzidas por dependências desatualizadas

**Descrição:** O projeto depende de pacotes externos (fastapi, uvicorn, pydantic, anyio, express) que podem receber CVEs ao longo do tempo. Sem atualização periódica, versões vulneráveis ficam em uso.

**Contexto de ocorrência:** Fase de manutenção contínua. O risco aumenta proporcionalmente ao tempo desde a última atualização de dependências e é agravado pela ausência de pipeline de CI que rode `pip-audit` e `npm audit` automaticamente.

---

### R14 — Incompatibilidade de licenças entre dependências

**Descrição:** O projeto está licenciado sob MIT, mas depende de bibliotecas de terceiros cujas licenças precisam ser verificadas para garantir compatibilidade, especialmente se o projeto for redistribuído ou integrado a produtos comerciais.

**Contexto de ocorrência:** Fase de distribuição ou comercialização do produto. A ausência de uma análise formal de licenças pode gerar obrigações legais não previstas.

---

## Categoria 5 — Operação e Monitoramento

### R15 — Sem monitoramento de disponibilidade em produção

**Descrição:** O backend expõe um endpoint `/health`, mas não existe nenhum sistema de monitoramento externo que o consulte periodicamente e alerte em caso de falha.

**Contexto de ocorrência:** Fase de operação em produção. Uma falha no backend (processo morto, out-of-memory, erro de inicialização) pode passar despercebida por horas ou dias, dependendo apenas de um usuário reportar o problema.

---

### R16 — Ausência de containerização dificulta replicação de ambiente

**Descrição:** O projeto não possui `Dockerfile` nem `docker-compose.yml`. A configuração do ambiente depende da instalação manual de Python 3.12+, uv e Node.js nas versões corretas.

**Contexto de ocorrência:** Fases de onboarding de novos colaboradores e implantação em novos servidores. Diferenças nas versões instaladas podem causar comportamentos inesperados difíceis de diagnosticar.

---

## Resumo dos Riscos Identificados

| ID  | Risco                                            | Categoria              |
|-----|--------------------------------------------------|------------------------|
| R01 | Sem HTTPS em produção                            | Segurança              |
| R02 | CORS permissivo em produção                      | Segurança              |
| R03 | API sem rate limiting                            | Segurança              |
| R04 | Swagger UI exposto em produção                   | Segurança              |
| R05 | Arquivos de servidor acessíveis pelo browser     | Segurança              |
| R06 | Commit acidental de variáveis de ambiente        | Segurança              |
| R07 | Sem testes no frontend                           | Qualidade              |
| R08 | Sem pipeline de CI/CD                            | Qualidade              |
| R09 | Cobertura de testes não monitorada               | Qualidade              |
| R10 | Escopo crescente não gerenciado                  | Projeto e Escopo       |
| R11 | Conhecimento concentrado em um desenvolvedor     | Projeto e Escopo       |
| R12 | Ausência de ambiente de homologação              | Projeto e Escopo       |
| R13 | Dependências desatualizadas com vulnerabilidades | Dependências           |
| R14 | Incompatibilidade de licenças                    | Conformidade           |
| R15 | Sem monitoramento de disponibilidade             | Operação               |
| R16 | Ausência de containerização                      | Operação               |
