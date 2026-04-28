# Diagrama de Fluxo — Geração de Senha

```mermaid
flowchart TD
    A([Usuário acessa a aplicação]) --> B[Valores padrão carregados\ntamanho=16, minúsculas=✓, maiúsculas=✓]
    B --> C[Usuário ajusta critérios]
    C --> D{Pelo menos um\ntipo selecionado?}
    D -- Não --> E[Botão Gerar desabilitado\nMensagem de aviso exibida]
    E --> C
    D -- Sim --> F[Botão Gerar habilitado]
    F --> G[Usuário clica em Gerar Senha]
    G --> H[Frontend monta payload JSON\ncom os critérios]
    H --> I[POST /api/gerar-senha]

    subgraph backend ["Backend — FastAPI"]
        I --> J{Parâmetros válidos?\ntamanho 8-128\n≥ 1 tipo ativo}
        J -- Não --> K[Retorna HTTP 422\ncom mensagem de erro]
        J -- Sim --> L[Monta charset com\nos tipos selecionados]
        L --> M[Garante ≥ 1 char\nde cada tipo ativo]
        M --> N[Preenche restante\ncom secrets.choice]
        N --> O[Embaralha a senha\ncom secrets.SystemRandom]
        O --> P[Calcula força da senha]
        P --> Q[Retorna HTTP 200\n senha + forca ]
    end

    K --> R[Frontend exibe\nmensagem de erro]
    R --> C
    Q --> S[Frontend exibe senha gerada]
    S --> T[Frontend exibe\nindicador de força]
    T --> U{Usuário quer\ncopiar a senha?}
    U -- Sim --> V[navigator.clipboard.writeText]
    V --> W[Feedback visual: Copiado!]
    W --> X{Gerar nova senha?}
    U -- Não --> X
    X -- Sim --> C
    X -- Não --> Y([Fim])
```

## Cálculo da Força da Senha

| Força | Critério |
|-------|----------|
| **Fraca** | apenas 1 tipo de caractere **ou** tamanho < 10 |
| **Média** | 2 tipos de caracteres **e** tamanho ≥ 10 |
| **Forte** | 3 tipos de caracteres **e** tamanho ≥ 12 |
| **Muito Forte** | 4 tipos de caracteres **e** tamanho ≥ 16 |
