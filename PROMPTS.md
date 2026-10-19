# Prompts de IA

Nesse documento, serão deixados os prompts usados em cada etapa.

O modelo usado majoritariamente foi o Claude Sonnet 4.6 via Claude Code.

### Etapa 1

```
Seja um desenvolvedor web com experiência em python em backend e frontend com html, css e js. Gostaria de fazer uma aplicação web simples que gera senhas seguras com base em critérios definidos pelos usário como

* tamanho da senha
* inclusão de caracteres especiais
* inclusão de letras maiúsculas e minúsculas
* inclusão de números

Gostaria de fazer um frontend simples e um backend em python para fazer esses passos, mas gostaria de seguir o ciclo de desenvolvimento completo de softwares sendo as fases:

1. Levantamento de requisitos
2. Projeto
3. Codificação
4. Testes e validação
5. Manutenção

Vamos fazer uma etapa de cada vez.

tecnologias a serem usadas no software: python, html, css e js.
```

### Etapa 1 - Levantamento de requisitos


Promt 01 - pedido inical:
```
Para primeira etapa, quais requisitos e especificações para o projeto são boas práticas? Algo a mais que deveria ser acrescentado ao escopo do projeto? 

Lembre-se que é uma aplicação simples.
```

Prompt 02 - Melhoria e resposta às perguntas do modelo:
```
O tamanho está bom. Os caracteres podem ser todos esses citados. Vamos gerar apenas uma senha por vez, sem salvar o histórico (cada sessão será independente). A API backend pode ser REST usando algo como FastAPI (python).

Sobre o requisito não funcional "RNF02 A interface deve ser responsiva e funcionar em mobile", bem como permitir geração de mais de uma senha por vez e histórico de sessão, vamos deixar para uma seção "Próximos passos".

Aproveitando, adicione ao README.md, cada fase do projeto, a explicação do que foi decidido bem como crie uma seção "Próximos passos" para adicionarmos o que for decidido que cabe nela.
```

### Etapa 2 - Projeto

Prompt 01 - pedido inical:
```
Podemos segir para a Fase 2 - Projeto.

Nessa fase, também vamos criar diagramas de uso, diagramas de fluxo além das definições propostas já feitas.

Crie os diagramas no formato aceito pelo mermaid de forma que seja possível visualizá-los
```

### Commits até Fase 02:

```
Observe as alterações e faça diversos commits relevantes a cada etapa usando o formato Conventional Commit de forma que seja possível fazer o registro de alterações com o histórico git
```

### Etapa 03:

Prompt 01 - pedido inical:

```
Vamos para a Fase 3, comecemos com o backend em python e api em geral. Use o FastAPI do python para esse fim. Crie também os arquivos requirements.txt (para uso com pip) e pyproject.toml (para uso com uv). No README.md, adicione uma descrição de como executar o backend, desde a instalação via pip ou uv, até a execução do arquivo python dentro de uma venv. Considere que alguém sem conhecimento técnico precisa reproduzir os passos
```

Prompt 02 - interação com modelo solicitando melhorias:
```
Para a instalação via uv, gostaria de usar o pip a menor quantidade de vezes o possível uma vez que o uv sync pode fazer mais sentido. Faça essa alteração
```

Prompt 03 - criação de um arquivo para testes local com extensão errada (.py):

```
Crie um arquivo EXEMPLOS.py e coloque exemplos com algumas das diferentes possíveis escolhas de usuários e seus payloads de chamadas REST, bem como o endpoint a ser usado e o retorno esperado. Mencione esse arquivo no README dentro da Fase 03 também
```

Prompt 04 - criação de um arquivo para testes local com extensão correta (.md):

```
Confundi os requistos, gostaria de um EXEMPLOS.md, markdown, e não .py. Os payloads devem estar apenas em formato json para que possa usar em ferramentas como postman e insomnia, bem com o endpoint necessário nessas ferramentas
```

Prompt 05 - criação de um frontend simples:

```
Agora, ainda na Fase 03, vamos fazer o frontend simples para uso web.
```

Prompt 06 - solicitando uma aplicação frontend melhor:

```
Ainda na Fase 03, pode usar NodeJS para criar um servidor frontend e deixar a aplicação mais profissional? Não esqueça de indicar, no README.md, quais passos para instalar o NodeJS (bem as dependências da aplicação frontend) e executar no terminal Windows ou Linux.
```

### Etapa 04:

Prompt 01 - pedido inical:

```
Podemos seguir para a Fase 4 — Testes e Validação. Nessa fase, crie os testes unitários relevantes para que a aplicação funciona corretamente bem como seja possível usar os testes unitários para prever quais quer erros que futuras alterações venham a causar. Para isso, use o pytest (biblioteca python) para gerar os testes de forma que possa-se ter a maior cobertura possível.
```

Prompt 02 - busca por vulnerabilidades:

```
Ainda na Fase 04, avalie o projeto sobre questão de segurança, possíveis variáveis de ambiente (ou informações que possam ser sensíveis e possam virar variáveis de ambiente). Se houver algo do tipo, indique quais são.
```

### Etapa 05:

Prompt 01 - pedido inical:

```
Podemos seguir para a Fase 5, Manutenção. Quais passos são recomendados para essa fase do desenvolvimento? O que podemos fazer?
```

Prompt 02 - adição de próximos passos:

```
Crie também, no README.md, sugestões na seção "próximos passos" se houver outras sugestões, considerando que é um sistema simples de geração de senhas
```

### Discovery de Arquitetura (exercício de pós-graduação)

Prompt 01 — Descrição do sistema e geração dos diagramas iniciais:

```
Estou fazendo uma pós em Eng de Software com uso de GenAI. A tarefa pede que eu conduza uma fase de discovery de documentação para um sistema da minha realidade usando a abordagem diagrams as code.

O sistema é este repositório: um Gerador de Senhas Seguras com backend FastAPI (Python) e frontend HTML/CSS/JS servido por Node.js/Express.

Preciso que você:
1. Descreva o sistema em linguagem natural cobrindo: escopo, nível da visão, limites e responsabilidades, integrações, restrições e lacunas.
2. Gere, em Mermaid, um diagrama estrutural inspirado no C4 (visão de containers) e um diagrama de sequência cobrindo a jornada crítica de geração de senha.
3. Documente tudo no README: a descrição, os diagramas renderizados e as decisões/ajustes feitos sobre o que o modelo gerou.
```

Prompt 02 — Ajuste do diagrama estrutural (migração para C4Container):

```
O diagrama de containers gerado usa graph LR com três nós simples. Migre para a sintaxe C4Container do Mermaid, separando o Servidor Estático (Node.js/Express) do Cliente Web (HTML/JS que roda no navegador), e inclua tecnologia e porta em cada container. Adicione também as setas de resposta que estavam faltando.
```

Prompt 03 — Ajuste do diagrama de sequência (adição do CSPRNG e detalhamento do backend):

```
O diagrama de sequência cobre o fluxo feliz e o erro 422, mas trata o backend como uma caixa preta. Adicione o participante secrets (CSPRNG do SO), detalhe o fluxo interno do backend (validação Pydantic → charset → secrets.choice → cobertura de tipos → força), torne a condição do alt mais precisa com as duas regras de negócio que disparam 422, e mova o fluxo de cópia para um bloco opt.
```

### Etapas posteriores

Promtp 01 - Criar Makefile

```
Crie um Makefile com as funções e passos de interesse como:
* Iniciar o backend
* Iniciar o frontend
* Realizer os testes e ter o relatório de cobertura
* Iniciar toda a aplicação

Entre outros que possam ser de interesse.
Adicione a explicação do uso desse Makefile no README.md.
```

## Módulo 9: Gerência de Projetos de Software Apoiada por Inteligência Artificial Generativa [ESP T1 ES C9]

Prompt 01 - Prompt inicial:

```
Leia o projeto desse diretório e faça o exercício de pensar em como gerenciaríamos esse projeto do começo ao fim.

Crie uma pasta chamada riscos/ e, dentro dela, adicione os seguintes arquivos com os seguintes contúdos:
* identificacao.md: arquivo de identificação de riscos com lista de riscos com descrição e contexto de ocorrência.
* analise.md: arquivo de análise de riscos com impactos e fatores condicionantes.
* respostas.md: arquivo com estratégias de respostas de como evitar, mitigar, transferir ou aceitar, todo com justificativas

Crie um pasta chamada comunicacao/ e, dentro dela, adicione o seguiunte arquivo:
* status-stackholders.md: arquivo de comunicação para stakeholders com narrativa clara com contexto, riscos e próximos passos
```

## Módulo 10: Engenharia de Requisitos com Inteligência Artificial Generativa [ESP T1 ES C10]


```
Analise meu projeto dessa pasta.

Preciso criar um documento geralmente produzido durante a etapa de elicitação de requisitos e utilizando a Inteligência Artificial Generativa como apoio para identificar requisitos, regras de negócio, requisitos não funcionais, lacunas e ambiguidades, além de selecionar e elaborar os artefatos de especificação mais adequados para representar a solução proposta.

Faça esse processo para esse projeto criando os artefatos que forem mais adequados para ele como histórias de usuário, casos de uso, critérios de aceitação, protótipos, entre outros.

Crie um documento, em requisitos/, chamado ELICITACAO.md em que explica por que esses artefatos foram considerados os mais adequados para representar os requisitos do projeto.
```
## Módulo 13: Testes de Software Automatizados com Inteligência Artificial Generativa [C13 ES T1]

### Unidade 3 — Testes de integração apoiados por GenAI

Modelo usado: Claude Opus 5.5 via Claude Code.

Cenário de integração escolhido: **fluxo front‑end ↔ back‑end** do Gerador de Senhas — o Cliente Web (`frontend/script.js` + `config.js`, servido pelo Express) chamando a API REST FastAPI (`POST /api/gerar-senha`), passando pelo middleware de CORS, pela validação Pydantic (`models.py`), pelo gerador (`generator.py`) e pelo handler de erros (`main.py`).

Foram definidos dois tipos de prompt, cada um com um objetivo diferente dentro do teste de integração. Os artefatos gerados estão em [testes-integracao/](testes-integracao/) e os testes executáveis em [backend/tests/integracao/](backend/tests/integracao/).

Prompt 01 — Tipo **"Cenários de integração + contrato de API"** (consumidor ↔ provedor):

```
Atue como engenheiro de QA especialista em testes de integração de APIs REST.

Contexto: este repositório é um Gerador de Senhas Seguras. O consumidor é o frontend (frontend/script.js, frontend/config.js e frontend/index.html) e o provedor é a API FastAPI (backend/main.py, backend/models.py, backend/generator.py). Leia esses arquivos antes de responder; não presuma nada que não esteja no código.

Tarefa:
1. Extraia o contrato implícito que o frontend espera da API: URL e método, campos e tipos do payload enviado, limites do slider, campos lidos da resposta, valores de "forca" que o frontend sabe exibir e como ele trata respostas de erro.
2. Compare esse contrato com o que o backend realmente implementa (rotas, SenhaRequest, SenhaResponse, calcular_forca, CORS, OpenAPI) e com o contrato documentado no README.md. Aponte divergências.
3. Gere cenários de integração cobrindo: contrato consumidor ↔ provedor, fluxo feliz ponta a ponta sobre HTTP real (uvicorn em processo separado), health check e CORS (preflight, método e cabeçalho não permitidos, ALLOWED_ORIGINS restrito via variável de ambiente).

Formato de saída:
- testes-integracao/cenarios-integracao.md com uma tabela (ID CI-xx, objetivo, componentes integrados, pré-condição, passos, resultado esperado, teste automatizado correspondente).
- Testes pytest em backend/tests/integracao/, sem novas dependências além das já existentes no pyproject.toml (pytest, httpx), marcados com @pytest.mark.integracao.
- Não altere o código da aplicação: se um teste revelar defeito, mantenha o teste com o comportamento correto esperado e registre o defeito como achado.
```

Prompt 02 — Tipo **"Casos de erro + dados de teste"** (testes negativos e de fronteira orientados a dados):

```
Atue como testador especializado em testes negativos e análise de valor limite.

Contexto: mesmo cenário do prompt anterior (frontend → POST /api/gerar-senha → FastAPI/Pydantic → handler de erros). O frontend faz `await resp.json()` antes de checar `resp.ok`, portanto qualquer resposta de erro que não seja JSON é exibida ao usuário como "Não foi possível conectar ao servidor".

Tarefa:
1. Gere um conjunto de dados de teste em JSON (backend/tests/integracao/dados/casos_erro.json) com casos de erro e de fronteira que atravessem as camadas da integração: JSON malformado, corpo vazio, corpo que não é objeto, Content-Type incorreto (text/plain e form), tipos errados, null, número fracionário, booleanos inválidos, limites de tamanho (7, 8, 128, 129 e valores muito grandes), regra de negócio "nenhum tipo selecionado", método HTTP errado e rota inexistente.
2. Para cada caso informe: id (CE-xx), descrição, método, rota, Content-Type, corpo bruto (string, para permitir JSON inválido), status HTTP esperado e o "type" de erro Pydantic esperado, quando houver.
3. Inclua também casos de coerção que o Pydantic aceita em modo lax (ex.: "16" como tamanho, "true" e 1 como booleano) e classifique-os como comportamento a ser decidido pelo time, não como erro.
4. Crie um teste pytest parametrizado que leia esse JSON e valide status, Content-Type application/json e estrutura do corpo de erro ({"detail": [...]}) para todos os casos.
5. Documente em testes-integracao/casos-de-erro.md a tabela de casos, o resultado esperado e o resultado observado após executar os testes, destacando os defeitos encontrados e a sugestão de correção.
```

Prompt 03 — Documentação do exercício:

```
Crie testes-integracao/ESTRATEGIA.md explicando o cenário de integração escolhido, os dois tipos de prompt usados e por que cada um foi escolhido, como executar os testes de integração, o resultado da execução, os defeitos encontrados e quais ajustes foram feitos sobre o que a LLM gerou. Adicione um alvo `make test-integracao` no Makefile e referencie a nova pasta no README.md.
```
