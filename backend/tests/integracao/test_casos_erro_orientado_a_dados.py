"""
Prompt 02 — Casos de erro e dados de teste.

Os casos vêm de dados/casos_erro.json e são enviados como bytes brutos para a
API real (uvicorn), permitindo JSON inválido e Content-Type arbitrário.

Contrato exigido pelo consumidor: o frontend faz `await resp.json()` antes de
checar `resp.ok`; logo, TODA resposta de erro precisa ser JSON, senão o
usuário vê "Não foi possível conectar ao servidor" em vez do erro real.
"""
import json

import pytest

from .apoio import DADOS_DIR

pytestmark = pytest.mark.integracao

DADOS = json.loads((DADOS_DIR / "casos_erro.json").read_text(encoding="utf-8"))
ENDPOINT = "/api/gerar-senha"


def _enviar(cliente, caso):
    headers = {"Content-Type": caso["content_type"]} if caso.get("content_type") else {}
    corpo = caso["corpo"].encode("utf-8") if caso.get("corpo") is not None else None
    return cliente.request(caso.get("metodo", "POST"), caso.get("rota", ENDPOINT),
                           content=corpo, headers=headers)


def _ids(casos):
    return [f'{c["id"]} {c["descricao"]}' for c in casos]


@pytest.mark.parametrize("caso", DADOS["erros"], ids=_ids(DADOS["erros"]))
def test_caso_de_erro_retorna_status_e_corpo_json_esperados(api_real, caso):
    resp = _enviar(api_real, caso)

    assert resp.status_code == caso["status"], resp.text
    assert resp.headers["content-type"].startswith("application/json"), (
        f"Erro em texto puro quebra o frontend: {resp.text!r}"
    )

    corpo = resp.json()
    assert "detail" in corpo

    if caso["tipo_erro"]:
        assert isinstance(corpo["detail"], list)
        assert caso["tipo_erro"] in {e["type"] for e in corpo["detail"]}
        for erro in corpo["detail"]:
            assert {"type", "loc", "msg"} <= erro.keys()


@pytest.mark.parametrize("caso", DADOS["fronteira_validos"], ids=_ids(DADOS["fronteira_validos"]))
def test_valor_de_fronteira_valido_gera_senha(api_real, caso):
    resp = _enviar(api_real, {**caso, "content_type": "application/json"})
    assert resp.status_code == 200, resp.text
    assert len(resp.json()["senha"]) == caso["tamanho_senha"]


@pytest.mark.parametrize("caso", DADOS["coercoes_a_decidir"], ids=_ids(DADOS["coercoes_a_decidir"]))
def test_coercao_lax_do_pydantic_e_aceita_hoje(api_real, caso):
    """
    Documenta o comportamento atual (Pydantic em modo lax). Não é defeito,
    mas é uma decisão em aberto: se o time adotar `strict=True` nos campos,
    estes casos passam a retornar 422 e este teste deve ser invertido.
    """
    resp = _enviar(api_real, {**caso, "content_type": "application/json"})
    assert resp.status_code == 200, resp.text
    assert len(resp.json()["senha"]) == caso["tamanho_senha"]
