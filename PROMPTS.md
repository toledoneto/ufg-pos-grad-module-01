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

Prompt 01:

```
Podemos seguir para a Fase 5, Manutenção. Quais passos são recomendados para essa fase do desenvolvimento? O que podemos fazer?
```

Prompt 02:

```
Crie também, no README.md, sugestões na seção "próximos passos" se houver outras sugestões, considerando que é um sistema simples de geração de senhas
```
