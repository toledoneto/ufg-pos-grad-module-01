"""
Prompt 01 — Contrato consumidor (frontend) ↔ provedor (API).

O frontend não tem testes próprios nem tipagem compartilhada com o backend:
o contrato existe apenas implicitamente no JavaScript. Estes testes extraem
esse contrato dos arquivos do frontend e o confrontam com o backend, para que
uma mudança de um lado que quebre o outro falhe no CI.
"""
import re
from itertools import product

import pytest

from generator import calcular_forca
from main import app
from models import SenhaRequest, SenhaResponse

from .apoio import FRONTEND_DIR

pytestmark = pytest.mark.integracao

SCRIPT_JS  = (FRONTEND_DIR / "script.js").read_text(encoding="utf-8")
CONFIG_JS  = (FRONTEND_DIR / "config.js").read_text(encoding="utf-8")
INDEX_HTML = (FRONTEND_DIR / "index.html").read_text(encoding="utf-8")


def _chaves_payload_frontend() -> set[str]:
    bloco = re.search(r"const payload = \{(.*?)\};", SCRIPT_JS, re.S).group(1)
    return set(re.findall(r"(\w+)\s*:", bloco))


def _niveis_forca_frontend() -> set[str]:
    bloco = re.search(r"const STRENGTH = \{(.*?)\n\};", SCRIPT_JS, re.S).group(1)
    return set(re.findall(r"'([^']+)'\s*:\s*\{", bloco))


def _rota_config_frontend() -> str:
    url = re.search(r"API_URL:\s*'([^']+)'", CONFIG_JS).group(1)
    return re.sub(r"^https?://[^/]+", "", url)


def _restricoes_tamanho_backend() -> tuple[int, int]:
    meta = SenhaRequest.model_fields["tamanho"].metadata
    ge = next(m.ge for m in meta if hasattr(m, "ge"))
    le = next(m.le for m in meta if hasattr(m, "le"))
    return ge, le


# CI-01
def test_rota_configurada_no_frontend_existe_no_backend_como_post():
    rota = _rota_config_frontend()
    rotas_post = {r.path for r in app.routes if "POST" in getattr(r, "methods", set())}
    assert rota in rotas_post


# CI-02
def test_payload_do_frontend_tem_exatamente_os_campos_do_senha_request():
    assert _chaves_payload_frontend() == set(SenhaRequest.model_fields)


# CI-03
def test_limites_do_slider_coincidem_com_a_validacao_do_backend():
    minimo = int(re.search(r'id="lengthSlider"[^>]*min="(\d+)"', INDEX_HTML).group(1))
    maximo = int(re.search(r'id="lengthSlider"[^>]*max="(\d+)"', INDEX_HTML).group(1))
    assert (minimo, maximo) == _restricoes_tamanho_backend()


# CI-04
def test_valor_inicial_do_slider_coincide_com_o_padrao_do_backend():
    inicial = int(re.search(r'id="lengthSlider"[^>]*value="(\d+)"', INDEX_HTML).group(1))
    assert inicial == SenhaRequest.model_fields["tamanho"].default


# CI-05
def test_frontend_le_apenas_campos_presentes_na_resposta():
    lidos = set(re.findall(r"data\.(\w+)", SCRIPT_JS))
    assert lidos <= set(SenhaResponse.model_fields)


# CI-06
def test_todo_nivel_de_forca_do_backend_tem_exibicao_no_frontend():
    ge, le = _restricoes_tamanho_backend()
    produzidos = {calcular_forca(t, n) for t, n in product(range(ge, le + 1), range(1, 5))}
    assert produzidos <= _niveis_forca_frontend(), (
        "Nível sem estilo no frontend cairia silenciosamente no fallback 'fraca'"
    )


# CI-07
def test_openapi_publica_o_contrato_consumido_pelo_frontend():
    schema = app.openapi()
    operacao = schema["paths"][_rota_config_frontend()]["post"]
    assert "200" in operacao["responses"]
    assert "422" in operacao["responses"]

    resposta = schema["components"]["schemas"]["SenhaResponse"]
    assert set(resposta["required"]) == {"senha", "forca"}

    requisicao = schema["components"]["schemas"]["SenhaRequest"]["properties"]
    assert requisicao["tamanho"]["minimum"] == 8
    assert requisicao["tamanho"]["maximum"] == 128
