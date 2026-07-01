# Status do Projeto — Gerador de Senhas Seguras

**Para:** Stakeholders do Projeto (orientadores, avaliadores, patrocinadores)
**Data:** Julho de 2026
**Versão do produto:** 1.0.0
**Responsável:** Toledo Neto

---

## Contexto: o que é este projeto e por que ele existe

O **Gerador de Senhas Seguras** é uma aplicação web desenvolvida como trabalho prático da pós-graduação na UFG. O objetivo é demonstrar, na prática, o ciclo completo de desenvolvimento de software — desde o levantamento de requisitos até a manutenção — aplicando boas práticas de engenharia, segurança e documentação.

A aplicação permite que qualquer usuário gere senhas seguras diretamente no navegador, configurando critérios como tamanho e tipos de caracteres. Diferentemente de geradores populares que processam tudo no navegador, esta aplicação delega a geração ao backend Python, utilizando o gerador criptograficamente seguro do sistema operacional (`secrets`). Isso garante que a aleatoriedade seja de qualidade criptográfica — não uma simulação de aleatoriedade feita em JavaScript.

O produto está funcional e entregue na versão 1.0.0.

---

## O que foi entregue

A versão 1.0.0 contempla todas as funcionalidades previstas no escopo original:

**Funcionalidades disponíveis ao usuário:**
- Configuração do tamanho da senha (entre 8 e 128 caracteres)
- Seleção de tipos de caracteres: maiúsculas, minúsculas, números e especiais
- Geração de senha no backend, com garantia de pelo menos um caractere de cada tipo selecionado
- Indicador de força da senha (fraca / média / forte / muito forte)
- Cópia da senha para a área de transferência com um clique

**Qualidade técnica entregue:**
- 57 testes automatizados cobrindo lógica de geração, modelos de dados e API REST
- Auditoria de segurança realizada com dois problemas identificados e corrigidos (CORS configurável por variável de ambiente; URL do backend externalizada em arquivo de configuração)
- Documentação técnica completa: arquitetura, casos de uso, diagramas de sequência, guia de gestão de dependências e CHANGELOG

---

## Situação atual: estável, com pontos de atenção para produção

O produto está **estável em ambiente de desenvolvimento** e passou por todas as fases do ciclo previsto. No entanto, uma análise de riscos conduzida ao fim do projeto revelou que a aplicação, no estado atual, **não está pronta para implantação em um servidor público** sem ajustes adicionais.

Os pontos de atenção mais relevantes são:

### 1. A aplicação não usa HTTPS

Quando uma senha é gerada, ela percorre a rede entre o servidor e o navegador do usuário. Sem criptografia de transporte (HTTPS), essa senha pode ser interceptada por terceiros na mesma rede. Para um gerador de senhas, isso é uma contradição direta com a proposta do produto.

**O que precisa ser feito:** configurar um certificado TLS no servidor de deploy, utilizando serviços gratuitos como o Let's Encrypt. O código da aplicação não precisa ser alterado — é uma configuração de infraestrutura.

**Prazo recomendado:** antes de qualquer deploy público.

---

### 2. A API não tem limite de requisições por IP

Qualquer pessoa pode chamar a API de geração de senhas indefinidamente, sem restrição. Em cenários de uso real, isso pode sobrecarregar o servidor ou gerar custos inesperados de infraestrutura.

**O que precisa ser feito:** adicionar uma biblioteca de rate limiting (`slowapi`) ao backend, limitando o número de requisições por IP por minuto. É uma mudança de baixo impacto no código.

**Prazo recomendado:** antes de qualquer deploy público.

---

### 3. Não há pipeline de integração contínua (CI)

Hoje, os testes e a auditoria de segurança das dependências só são executados quando o desenvolvedor os roda manualmente. Sem automação, um commit que quebre um teste ou introduza uma vulnerabilidade pode passar despercebido.

**O que precisa ser feito:** configurar o GitHub Actions para rodar os testes e a auditoria de segurança automaticamente a cada mudança no repositório. Os comandos já estão centralizados no Makefile — a configuração do CI é a conexão que falta.

**Prazo recomendado:** próxima iteração de desenvolvimento.

---

### 4. O frontend não tem testes automatizados

Os 57 testes existentes cobrem apenas o backend. Mudanças na interface — como novos campos, ajustes no indicador de força ou no botão de cópia — não são verificadas automaticamente.

**O que precisa ser feito:** adicionar testes de frontend com Vitest (unitários) e Playwright (fluxo completo no navegador).

**Prazo recomendado:** próxima iteração de desenvolvimento, em paralelo com o CI.

---

## O que vem a seguir

Além dos pontos de atenção de produção, o backlog do projeto contém 16 melhorias identificadas durante o desenvolvimento. As mais relevantes para a próxima fase, em ordem de prioridade, são:

| Prioridade | Melhoria                                | Área             | Benefício principal                                        |
|------------|-----------------------------------------|------------------|------------------------------------------------------------|
| 1          | Configurar CI/CD no GitHub Actions      | Qualidade        | Detecta erros automaticamente antes de chegarem ao produto |
| 2          | Adicionar HTTPS + rate limiting         | Segurança        | Viabiliza o deploy público com segurança                   |
| 3          | Containerizar com Docker                | Infraestrutura   | Garante reprodutibilidade do ambiente em qualquer máquina  |
| 4          | Adicionar testes de frontend            | Qualidade        | Reduz risco de regressões na interface                     |
| 5          | Geração em lote de senhas               | Funcionalidade   | Atende o caso de uso de criar múltiplas senhas de uma vez  |
| 6          | Cálculo de entropia real                | Funcionalidade   | Torna o indicador de força matematicamente preciso         |

---

## Riscos sob acompanhamento

A análise de riscos identificou 16 riscos distribuídos em cinco categorias. Os três de maior criticidade são:

**Crítico — Sem HTTPS em produção (R01):** qualquer deploy público sem TLS expõe a senha gerada em trânsito. Mitigação planejada antes do 1º deploy.

**Crítico — API sem rate limiting (R03):** a ausência de controle de requisições expõe o servidor a sobrecarga. Mitigação planejada junto com HTTPS.

**Alto — Conhecimento concentrado em um único desenvolvedor (R11):** o projeto é de responsabilidade de uma única pessoa. A mitigação é contínua via documentação operacional (runbook, decisões registradas no CHANGELOG).

Os demais riscos identificados têm nível Médio ou Baixo e estão documentados com estratégias de resposta no arquivo `riscos/respostas.md`.

---

## Pontos positivos a destacar

Para equilibrar a perspectiva, vale registrar o que o projeto entregou bem:

- **Segurança de geração:** o uso de `secrets` (CSPRNG do SO) é a abordagem correta para geração de senhas — não é `random` disfarçado.
- **Backend stateless:** nenhuma senha é armazenada em servidor, banco ou log. O dado existe apenas na resposta HTTP e é responsabilidade do usuário a partir daí.
- **Documentação abrangente:** o README cobre todas as cinco fases do ciclo de desenvolvimento com exemplos executáveis, facilitando onboarding e auditoria.
- **Auditoria de segurança realizada:** dois problemas reais foram identificados e corrigidos durante o desenvolvimento (não apenas documentados).
- **57 testes com alta cobertura no backend:** a suíte cobre limites, casos de erro e comportamento esperado da API.

---

## Resumo executivo

O Gerador de Senhas Seguras v1.0.0 cumpriu o escopo definido e está funcional. O produto demonstra domínio das práticas do ciclo de desenvolvimento de software, com qualidade técnica documentada e auditoria de segurança realizada.

Para evolução a produto público, três ações são pré-requisitos: configuração de HTTPS, adição de rate limiting e criação do pipeline de CI. Essas ações têm baixo custo de implementação e alto impacto na confiabilidade do serviço.

O projeto está bem posicionado para as próximas iterações: o código é limpo, a documentação é completa e o backlog está identificado. O principal investimento necessário agora é em automação de qualidade e configuração de infraestrutura, não em reescrita ou redesign.

---

*Documentação técnica completa disponível no repositório: `README.md`, `riscos/`, `docs/` e `CHANGELOG.md`.*
