# Diagrama de Sequência — Interação Frontend ↔ Backend

```mermaid
sequenceDiagram
    actor U as Usuário
    participant F as Frontend (HTML/JS)
    participant B as Backend (FastAPI)

    U->>F: Acessa a aplicação
    F-->>U: Renderiza interface com valores padrão

    U->>F: Ajusta critérios (tamanho, tipos)
    F->>F: Valida: ao menos 1 tipo selecionado
    F-->>U: Habilita/desabilita botão Gerar

    U->>F: Clica em "Gerar Senha"
    F->>B: POST /api/gerar-senha<br/>{ tamanho, maiusculas, minusculas, numeros, especiais }

    alt Parâmetros inválidos
        B-->>F: HTTP 422 { detail: "mensagem de erro" }
        F-->>U: Exibe mensagem de erro
    else Parâmetros válidos
        B->>B: Monta charset conforme tipos ativos
        B->>B: Gera senha com secrets.choice()
        B->>B: Calcula força da senha
        B-->>F: HTTP 200 { senha, forca }
        F-->>U: Exibe senha gerada
        F-->>U: Exibe indicador de força
    end

    U->>F: Clica em "Copiar"
    F->>F: navigator.clipboard.writeText(senha)
    F-->>U: Feedback visual "Copiado!"
```

## Contrato da API

### `POST /api/gerar-senha`

**Request Body**
```json
{
  "tamanho": 16,
  "maiusculas": true,
  "minusculas": true,
  "numeros": true,
  "especiais": false
}
```

**Response 200 — OK**
```json
{
  "senha": "aB3xYmQpLz7wNkRe",
  "forca": "forte"
}
```

**Response 422 — Unprocessable Entity**
```json
{
  "detail": "Pelo menos um tipo de caractere deve ser selecionado."
}
```

### Valores válidos

| Campo | Tipo | Restrição |
|-------|------|-----------|
| `tamanho` | `integer` | 8 ≤ valor ≤ 128 |
| `maiusculas` | `boolean` | — |
| `minusculas` | `boolean` | — |
| `numeros` | `boolean` | — |
| `especiais` | `boolean` | — |

> Ao menos um dos campos booleanos deve ser `true`.
