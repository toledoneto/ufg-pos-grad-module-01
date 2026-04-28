# Diagrama de Casos de Uso

```mermaid
graph LR
    usuario(["👤 Usuário"])

    subgraph sistema ["Sistema — Gerador de Senhas"]
        UC1(["Definir tamanho da senha"])
        UC2(["Selecionar maiúsculas"])
        UC3(["Selecionar minúsculas"])
        UC4(["Selecionar números"])
        UC5(["Selecionar caracteres especiais"])
        UC6(["Gerar senha"])
        UC7(["Copiar senha"])
        UC8(["Visualizar força da senha"])
    end

    usuario --> UC1
    usuario --> UC2
    usuario --> UC3
    usuario --> UC4
    usuario --> UC5
    usuario --> UC6
    usuario --> UC7
    UC6 -.inclui.-> UC8
```

## Descrição dos Casos de Uso

| Caso de Uso | Ator | Descrição |
|-------------|------|-----------|
| Definir tamanho da senha | Usuário | Seleciona um valor entre 8 e 128 via slider ou campo numérico |
| Selecionar maiúsculas | Usuário | Ativa/desativa a inclusão de letras A-Z |
| Selecionar minúsculas | Usuário | Ativa/desativa a inclusão de letras a-z |
| Selecionar números | Usuário | Ativa/desativa a inclusão de dígitos 0-9 |
| Selecionar caracteres especiais | Usuário | Ativa/desativa a inclusão de `!@#$%^&*()_+-=[]{}|;':",.<>?/` |
| Gerar senha | Usuário | Envia os critérios ao backend e recebe a senha gerada |
| Copiar senha | Usuário | Copia a senha exibida para a área de transferência com um clique |
| Visualizar força da senha | Sistema | Exibido automaticamente após a geração (incluso em "Gerar senha") |
