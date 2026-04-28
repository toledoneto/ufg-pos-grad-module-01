"""
EXEMPLOS.py

Demonstra diferentes cenários de uso da API do Gerador de Senhas Seguras.
Cada exemplo mostra o payload enviado, o endpoint chamado e o retorno esperado.

Pré-requisito: o servidor deve estar em execução em http://127.0.0.1:8000
               Consulte o README para instruções de execução.

Como executar este arquivo:
    python EXEMPLOS.py          # se estiver com o venv ativado
    uv run python EXEMPLOS.py   # se estiver usando uv
"""

import json
import urllib.error
import urllib.request

ENDPOINT = "http://127.0.0.1:8000/api/gerar-senha"


def chamar_api(titulo: str, payload: dict) -> None:
    print(f"{'=' * 60}")
    print(f"  {titulo}")
    print(f"{'=' * 60}")
    print(f"  Endpoint : POST {ENDPOINT}")
    print(f"  Payload  : {json.dumps(payload, ensure_ascii=False)}")

    dados = json.dumps(payload).encode()
    req = urllib.request.Request(
        ENDPOINT,
        data=dados,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            resultado = json.loads(resp.read())
            print(f"  Status   : 200 OK")
            print(f"  Retorno  : {json.dumps(resultado, ensure_ascii=False)}")
    except urllib.error.HTTPError as e:
        erro = json.loads(e.read())
        print(f"  Status   : {e.code} {e.reason}")
        print(f"  Retorno  : {json.dumps(erro, ensure_ascii=False)}")
    except urllib.error.URLError:
        print("  ERRO: não foi possível conectar ao servidor.")
        print("        Certifique-se de que o backend está em execução.")
    print()


# ---------------------------------------------------------------------------
# Exemplos de sucesso
# ---------------------------------------------------------------------------

chamar_api(
    titulo="Exemplo 1 — Senha básica: só minúsculas, tamanho 8",
    payload={
        "tamanho": 8,
        "maiusculas": False,
        "minusculas": True,
        "numeros": False,
        "especiais": False,
    },
    # Força esperada: "fraca" (1 tipo de caractere)
    # Retorno esperado:
    # { "senha": "xkqtmjav", "forca": "fraca" }
)

chamar_api(
    titulo="Exemplo 2 — Senha com maiúsculas e minúsculas, tamanho 12",
    payload={
        "tamanho": 12,
        "maiusculas": True,
        "minusculas": True,
        "numeros": False,
        "especiais": False,
    },
    # Força esperada: "média" (2 tipos, tamanho >= 10)
    # Retorno esperado:
    # { "senha": "AbCdEfGhIjKl", "forca": "média" }
)

chamar_api(
    titulo="Exemplo 3 — Senha com letras e números, tamanho 16",
    payload={
        "tamanho": 16,
        "maiusculas": True,
        "minusculas": True,
        "numeros": True,
        "especiais": False,
    },
    # Força esperada: "forte" (3 tipos, tamanho >= 12)
    # Retorno esperado:
    # { "senha": "aB3xYmQpLz7wNkRe", "forca": "forte" }
)

chamar_api(
    titulo="Exemplo 4 — Senha muito forte: todos os tipos, tamanho 20",
    payload={
        "tamanho": 20,
        "maiusculas": True,
        "minusculas": True,
        "numeros": True,
        "especiais": True,
    },
    # Força esperada: "muito forte" (4 tipos, tamanho >= 16)
    # Retorno esperado:
    # { "senha": "aB3!xYm@Qp7#Lz$wNkRe", "forca": "muito forte" }
)

# ---------------------------------------------------------------------------
# Exemplos de erro (HTTP 422 — Unprocessable Entity)
# ---------------------------------------------------------------------------

chamar_api(
    titulo="Exemplo 5 (erro) — Nenhum tipo de caractere selecionado",
    payload={
        "tamanho": 16,
        "maiusculas": False,
        "minusculas": False,
        "numeros": False,
        "especiais": False,
    },
    # A API rejeita a requisição pois nenhum tipo foi selecionado.
    # Retorno esperado:
    # { "detail": [{ "msg": "Pelo menos um tipo de caractere deve ser selecionado." }] }
)

chamar_api(
    titulo="Exemplo 6 (erro) — Tamanho abaixo do mínimo permitido (4)",
    payload={
        "tamanho": 4,
        "maiusculas": True,
        "minusculas": True,
        "numeros": False,
        "especiais": False,
    },
    # A API rejeita a requisição pois o tamanho mínimo é 8.
    # Retorno esperado:
    # { "detail": [{ "msg": "Input should be greater than or equal to 8" }] }
)

chamar_api(
    titulo="Exemplo 7 (erro) — Tamanho acima do máximo permitido (200)",
    payload={
        "tamanho": 200,
        "maiusculas": True,
        "minusculas": True,
        "numeros": True,
        "especiais": True,
    },
    # A API rejeita a requisição pois o tamanho máximo é 128.
    # Retorno esperado:
    # { "detail": [{ "msg": "Input should be less than or equal to 128" }] }
)
