import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

ENDPOINT = "/api/gerar-senha"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def post(payload: dict):
    return client.post(ENDPOINT, json=payload)


# ---------------------------------------------------------------------------
# Estrutura da resposta
# ---------------------------------------------------------------------------

def test_resposta_contem_campos_senha_e_forca():
    resp = post({"tamanho": 16, "maiusculas": True, "minusculas": True, "numeros": False, "especiais": False})
    assert resp.status_code == 200
    data = resp.json()
    assert "senha" in data
    assert "forca" in data


def test_senha_e_uma_string():
    resp = post({"tamanho": 16, "maiusculas": True, "minusculas": True, "numeros": False, "especiais": False})
    assert isinstance(resp.json()["senha"], str)


def test_forca_e_uma_string():
    resp = post({"tamanho": 16, "maiusculas": True, "minusculas": True, "numeros": False, "especiais": False})
    assert isinstance(resp.json()["forca"], str)


# ---------------------------------------------------------------------------
# Comprimento da senha
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tamanho", [8, 12, 16, 32, 64, 128])
def test_comprimento_da_senha_na_resposta(tamanho):
    resp = post({"tamanho": tamanho, "maiusculas": True, "minusculas": True, "numeros": False, "especiais": False})
    assert resp.status_code == 200
    assert len(resp.json()["senha"]) == tamanho


# ---------------------------------------------------------------------------
# Valores padrão (body vazio)
# ---------------------------------------------------------------------------

def test_body_vazio_usa_valores_padrao():
    resp = post({})
    assert resp.status_code == 200
    assert len(resp.json()["senha"]) == 16  # tamanho padrão


# ---------------------------------------------------------------------------
# Força da senha em cada nível
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("payload,forca_esperada", [
    (
        {"tamanho": 8, "maiusculas": False, "minusculas": True, "numeros": False, "especiais": False},
        "fraca",
    ),
    (
        {"tamanho": 9, "maiusculas": True, "minusculas": True, "numeros": False, "especiais": False},
        "fraca",
    ),
    (
        {"tamanho": 10, "maiusculas": True, "minusculas": True, "numeros": False, "especiais": False},
        "média",
    ),
    (
        {"tamanho": 12, "maiusculas": True, "minusculas": True, "numeros": True, "especiais": False},
        "forte",
    ),
    (
        {"tamanho": 16, "maiusculas": True, "minusculas": True, "numeros": True, "especiais": True},
        "muito forte",
    ),
])
def test_forca_retornada_pela_api(payload, forca_esperada):
    resp = post(payload)
    assert resp.status_code == 200
    assert resp.json()["forca"] == forca_esperada


# ---------------------------------------------------------------------------
# Erros de validação (HTTP 422)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("payload,descricao", [
    (
        {"tamanho": 16, "maiusculas": False, "minusculas": False, "numeros": False, "especiais": False},
        "nenhum tipo selecionado",
    ),
    (
        {"tamanho": 7, "maiusculas": True, "minusculas": False, "numeros": False, "especiais": False},
        "tamanho abaixo do mínimo (7)",
    ),
    (
        {"tamanho": 0, "maiusculas": True, "minusculas": False, "numeros": False, "especiais": False},
        "tamanho zero",
    ),
    (
        {"tamanho": 129, "maiusculas": True, "minusculas": False, "numeros": False, "especiais": False},
        "tamanho acima do máximo (129)",
    ),
    (
        {"tamanho": 200, "maiusculas": True, "minusculas": False, "numeros": False, "especiais": False},
        "tamanho muito acima do máximo (200)",
    ),
])
def test_payload_invalido_retorna_422(payload, descricao):
    resp = post(payload)
    assert resp.status_code == 422, f"Falhou para: {descricao}"


def test_resposta_422_contem_campo_detail():
    resp = post({"tamanho": 16, "maiusculas": False, "minusculas": False, "numeros": False, "especiais": False})
    assert "detail" in resp.json()


# ---------------------------------------------------------------------------
# Aleatoriedade: dois pedidos idênticos produzem senhas diferentes
# ---------------------------------------------------------------------------

def test_senhas_consecutivas_sao_diferentes():
    payload = {"tamanho": 32, "maiusculas": True, "minusculas": True, "numeros": True, "especiais": True}
    senhas = {post(payload).json()["senha"] for _ in range(5)}
    # Com charset de 4 tipos e 32 chars, a probabilidade de colisão é desprezível
    assert len(senhas) > 1
