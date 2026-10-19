# Exemplos de uso da API

Exemplos de chamadas para a API do Gerador de Senhas Seguras.
Todos os exemplos usam o endpoint abaixo com o método `POST`.

**URL:** `http://127.0.0.1:8000/api/gerar-senha`  
**Método:** `POST`  
**Header:** `Content-Type: application/json`

> A documentação interativa da API também está disponível em http://127.0.0.1:8000/docs

---

## Exemplos de sucesso

### Exemplo 1 — Senha básica: só minúsculas, tamanho 8

```json
{
  "tamanho": 8,
  "maiusculas": false,
  "minusculas": true,
  "numeros": false,
  "especiais": false
}
```

**Retorno esperado** — `200 OK`
```json
{
  "senha": "xkqtmjav",
  "forca": "fraca"
}
```

---

### Exemplo 2 — Maiúsculas e minúsculas, tamanho 12

```json
{
  "tamanho": 12,
  "maiusculas": true,
  "minusculas": true,
  "numeros": false,
  "especiais": false
}
```

**Retorno esperado** — `200 OK`
```json
{
  "senha": "AbCdEfGhIjKl",
  "forca": "média"
}
```

---

### Exemplo 3 — Letras e números, tamanho 16

```json
{
  "tamanho": 16,
  "maiusculas": true,
  "minusculas": true,
  "numeros": true,
  "especiais": false
}
```

**Retorno esperado** — `200 OK`
```json
{
  "senha": "aB3xYmQpLz7wNkRe",
  "forca": "forte"
}
```

---

### Exemplo 4 — Todos os tipos, tamanho 20

```json
{
  "tamanho": 20,
  "maiusculas": true,
  "minusculas": true,
  "numeros": true,
  "especiais": true
}
```

**Retorno esperado** — `200 OK`
```json
{
  "senha": "aB3!xYm@Qp7#Lz$wNkRe",
  "forca": "muito forte"
}
```

---

## Exemplos de erro

> A senha gerada é sempre aleatória — o valor do campo `senha` nos exemplos acima é ilustrativo.  
> O campo `forca` é determinístico e sempre corresponderá ao critério definido.

### Exemplo 5 — Nenhum tipo de caractere selecionado

```json
{
  "tamanho": 16,
  "maiusculas": false,
  "minusculas": false,
  "numeros": false,
  "especiais": false
}
```

**Retorno esperado** — `422 Unprocessable Entity`
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body"],
      "msg": "Value error, Pelo menos um tipo de caractere deve ser selecionado.",
      "input": {
        "tamanho": 16,
        "maiusculas": false,
        "minusculas": false,
        "numeros": false,
        "especiais": false
      },
      "ctx": { "error": {} }
    }
  ]
}
```

---

### Exemplo 6 — Tamanho abaixo do mínimo permitido

```json
{
  "tamanho": 4,
  "maiusculas": true,
  "minusculas": true,
  "numeros": false,
  "especiais": false
}
```

**Retorno esperado** — `422 Unprocessable Entity`
```json
{
  "detail": [
    {
      "type": "greater_than_equal",
      "loc": ["body", "tamanho"],
      "msg": "Input should be greater than or equal to 8",
      "input": 4
    }
  ]
}
```

---

### Exemplo 7 — Tamanho acima do máximo permitido

```json
{
  "tamanho": 200,
  "maiusculas": true,
  "minusculas": true,
  "numeros": true,
  "especiais": true
}
```

**Retorno esperado** — `422 Unprocessable Entity`
```json
{
  "detail": [
    {
      "type": "less_than_equal",
      "loc": ["body", "tamanho"],
      "msg": "Input should be less than or equal to 128",
      "input": 200
    }
  ]
}
```
