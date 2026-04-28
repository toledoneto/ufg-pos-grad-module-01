# Changelog

Todas as mudanças relevantes deste projeto são documentadas aqui.

O formato segue o padrão [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)
e o versionamento segue o [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [1.0.0] - 2026-04-28

Primeira versão funcional do Gerador de Senhas Seguras, desenvolvida seguindo
o ciclo completo de desenvolvimento de software (fases 1 a 5).

### Adicionado

#### Documentação e projeto
- README completo com as cinco fases do ciclo de desenvolvimento
- Fase 1: requisitos funcionais (RF01–RF08), não-funcionais (RNF01–RNF03),
  regras de negócio (RN01–RN03) e decisões tomadas
- Fase 2: diagramas Mermaid de casos de uso, fluxo de geração e sequência da API
- Fase 2: contrato REST documentado em `docs/sequencia-api.md` e `backend/EXEMPLOS.md`
- Fase 2: arquitetura cliente-servidor documentada com estrutura de pastas
- Seção "Próximos Passos" com funcionalidades adiadas (mobile, lote, histórico)

#### Backend (Python / FastAPI)
- Modelos Pydantic `SenhaRequest` e `SenhaResponse` com validação de entrada
- Gerador de senhas com `secrets.choice()` (CSPRNG) garantindo ao menos
  um caractere de cada tipo ativo antes de preencher o restante
- Cálculo de força da senha em quatro níveis: fraca, média, forte, muito forte
- Rota `POST /api/gerar-senha` com validação automática via Pydantic (HTTP 422)
- Middleware CORS configurável via variável de ambiente `ALLOWED_ORIGINS`
- `requirements.txt` para instalação com pip
- `pyproject.toml` com dependências de produção e grupo `dev` para uv
- `requirements-dev.txt` para instalação de dependências de teste com pip
- `.env.example` documentando todas as variáveis de ambiente disponíveis

#### Frontend (HTML / CSS / JavaScript / Node.js)
- Interface com slider de tamanho (8–128), quatro checkboxes de tipo,
  exibição da senha gerada, indicador de força animado e botão copiar
- Barra de força com transição de cor por nível (fraca → muito forte)
- Cópia para clipboard com `navigator.clipboard` e fallback `execCommand`
- `config.js` centralizando a URL do backend para fácil configuração
- Servidor Express (`server.js`) entregando os arquivos estáticos na porta 3000

#### Testes
- Suíte com 57 testes em três módulos (`test_generator`, `test_models`, `test_api`)
- Cobertura de: todos os limites de `calcular_forca`, comprimento e charset
  de `gerar_senha`, validação de modelos Pydantic, respostas 200 e 422 da API
- Configuração de cobertura de código via `pytest-cov`

### Corrigido

- Charset de caracteres especiais incluía barra invertida por engano
  (raw string com `\"` em `generator.py`)
- Instruções de instalação do `uv` agora usam o instalador oficial `astral.sh`
  em vez de `pip install uv`

### Segurança

- CORS: origens permitidas agora lidas da variável `ALLOWED_ORIGINS`
  (padrão `*` em desenvolvimento; restrito em produção)
- URL do backend externalizada do `script.js` para `config.js`
  para evitar hardcode entre ambientes
- Arquivos `.env` protegidos pelo `.gitignore` para não serem versionados acidentalmente

### Alterado

- `EXEMPLOS.py` substituído por `EXEMPLOS.md` com payloads JSON puros,
  prontos para uso em Postman e Insomnia

---

## [Não lançado]

Funcionalidades planejadas para versões futuras:

- Interface responsiva para dispositivos móveis
- Geração em lote (múltiplas senhas por requisição)
- Histórico de senhas da sessão (sem persistência entre sessões)
- HTTPS / TLS para uso em produção
- Rate limiting na API (`slowapi`)
- Swagger UI desabilitado em produção
- Servidor frontend com arquivos estáticos em subpasta `public/`
