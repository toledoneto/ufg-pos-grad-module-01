"""
Prompt 01 — Fluxo ponta a ponta sobre HTTP real e CORS.

Diferente de tests/test_api.py (TestClient em memória), aqui a API roda em um
processo uvicorn separado, como o navegador a encontraria.
"""
import pytest

from .apoio import ORIGEM_FRONTEND

pytestmark = pytest.mark.integracao

ENDPOINT = "/api/gerar-senha"
CABECALHOS_FRONTEND = {"Origin": ORIGEM_FRONTEND, "Content-Type": "application/json"}


# CI-08
def test_health_check_disponivel_sobre_http(api_real):
    resp = api_real.get("/health")
    assert resp.status_code == 200
    corpo = resp.json()
    assert corpo["status"] == "ok"
    assert corpo["version"] == "1.0.0"


# CI-09
@pytest.mark.parametrize("payload,forca", [
    ({"tamanho": 8,   "maiusculas": True, "minusculas": False, "numeros": False, "especiais": False}, "fraca"),
    ({"tamanho": 10,  "maiusculas": True, "minusculas": True,  "numeros": False, "especiais": False}, "média"),
    ({"tamanho": 12,  "maiusculas": True, "minusculas": True,  "numeros": True,  "especiais": False}, "forte"),
    ({"tamanho": 128, "maiusculas": True, "minusculas": True,  "numeros": True,  "especiais": True},  "muito forte"),
])
def test_fluxo_feliz_com_payload_identico_ao_do_frontend(api_real, payload, forca):
    resp = api_real.post(ENDPOINT, json=payload, headers=CABECALHOS_FRONTEND)

    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/json"
    corpo = resp.json()
    assert len(corpo["senha"]) == payload["tamanho"]
    assert corpo["forca"] == forca


# CI-10
def test_caracteres_especiais_sobrevivem_a_serializacao_json(api_real):
    payload = {"tamanho": 128, "maiusculas": False, "minusculas": False, "numeros": False, "especiais": True}
    senha = api_real.post(ENDPOINT, json=payload).json()["senha"]
    assert set(senha) <= set("""!@#$%^&*()_+-=[]{}|;':",.<>?/""")
    assert len(senha) == 128


# CI-11
def test_preflight_cors_do_navegador_e_aceito(api_real):
    resp = api_real.options(ENDPOINT, headers={
        "Origin": ORIGEM_FRONTEND,
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type",
    })
    assert resp.status_code == 200
    assert "POST" in resp.headers["access-control-allow-methods"]
    assert "Content-Type" in resp.headers["access-control-allow-headers"]


# CI-12
def test_resposta_de_erro_422_tambem_carrega_cabecalho_cors(api_real):
    """Sem o cabeçalho, o navegador bloqueia a leitura do erro e o usuário vê 'falha de conexão'."""
    resp = api_real.post(ENDPOINT, json={"tamanho": 7}, headers=CABECALHOS_FRONTEND)
    assert resp.status_code == 422
    assert resp.headers["access-control-allow-origin"] == "*"


# CI-13
@pytest.mark.parametrize("cabecalhos,motivo", [
    ({"Access-Control-Request-Method": "PUT"}, "Disallowed CORS method"),
    ({"Access-Control-Request-Method": "POST", "Access-Control-Request-Headers": "Authorization"},
     "Disallowed CORS headers"),
])
def test_preflight_rejeita_metodo_ou_cabecalho_nao_permitido(api_real, cabecalhos, motivo):
    resp = api_real.options(ENDPOINT, headers={"Origin": ORIGEM_FRONTEND, **cabecalhos})
    assert resp.status_code == 400
    assert motivo in resp.text


# CI-14
def test_cors_restrito_aceita_a_origem_do_frontend(api_cors_restrito):
    resp = api_cors_restrito.post(ENDPOINT, json={}, headers=CABECALHOS_FRONTEND)
    assert resp.status_code == 200
    assert resp.headers["access-control-allow-origin"] == ORIGEM_FRONTEND


# CI-15
def test_cors_restrito_nao_libera_origem_desconhecida(api_cors_restrito):
    resp = api_cors_restrito.post(ENDPOINT, json={}, headers={"Origin": "https://site-malicioso.example"})
    # O servidor processa a requisição, mas sem o cabeçalho o navegador descarta a resposta.
    assert "access-control-allow-origin" not in resp.headers

    preflight = api_cors_restrito.options(ENDPOINT, headers={
        "Origin": "https://site-malicioso.example",
        "Access-Control-Request-Method": "POST",
    })
    assert preflight.status_code == 400
    assert "Disallowed CORS origin" in preflight.text
