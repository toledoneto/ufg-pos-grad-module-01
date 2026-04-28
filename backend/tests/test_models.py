import pytest
from pydantic import ValidationError

from models import SenhaRequest, SenhaResponse


# ---------------------------------------------------------------------------
# SenhaRequest — valores padrão
# ---------------------------------------------------------------------------

def test_valores_padrao():
    req = SenhaRequest()
    assert req.tamanho == 16
    assert req.maiusculas is True
    assert req.minusculas is True
    assert req.numeros is False
    assert req.especiais is False


# ---------------------------------------------------------------------------
# SenhaRequest — tamanho válido (fronteiras)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tamanho", [8, 9, 64, 127, 128])
def test_tamanho_valido(tamanho):
    req = SenhaRequest(tamanho=tamanho, maiusculas=True, minusculas=False, numeros=False, especiais=False)
    assert req.tamanho == tamanho


# ---------------------------------------------------------------------------
# SenhaRequest — tamanho inválido
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tamanho", [0, 1, 7, 129, 200, 1000])
def test_tamanho_invalido_levanta_validation_error(tamanho):
    with pytest.raises(ValidationError):
        SenhaRequest(tamanho=tamanho, maiusculas=True, minusculas=False, numeros=False, especiais=False)


# ---------------------------------------------------------------------------
# SenhaRequest — ao menos um tipo obrigatório
# ---------------------------------------------------------------------------

def test_nenhum_tipo_selecionado_levanta_validation_error():
    with pytest.raises(ValidationError) as exc_info:
        SenhaRequest(maiusculas=False, minusculas=False, numeros=False, especiais=False)
    assert "Pelo menos um tipo" in str(exc_info.value)


@pytest.mark.parametrize("campo", ["maiusculas", "minusculas", "numeros", "especiais"])
def test_apenas_um_tipo_ativo_e_valido(campo):
    kwargs = {"maiusculas": False, "minusculas": False, "numeros": False, "especiais": False, campo: True}
    req = SenhaRequest(**kwargs)
    assert getattr(req, campo) is True


# ---------------------------------------------------------------------------
# SenhaRequest — todos os tipos ativos
# ---------------------------------------------------------------------------

def test_todos_os_tipos_ativos_e_valido():
    req = SenhaRequest(maiusculas=True, minusculas=True, numeros=True, especiais=True)
    assert req.maiusculas is True
    assert req.minusculas is True
    assert req.numeros is True
    assert req.especiais is True


# ---------------------------------------------------------------------------
# SenhaResponse
# ---------------------------------------------------------------------------

def test_senha_response_campos_obrigatorios():
    resp = SenhaResponse(senha="Abc123!", forca="forte")
    assert resp.senha == "Abc123!"
    assert resp.forca == "forte"


@pytest.mark.parametrize("forca", ["fraca", "média", "forte", "muito forte"])
def test_senha_response_aceita_todos_os_niveis_de_forca(forca):
    resp = SenhaResponse(senha="x" * 16, forca=forca)
    assert resp.forca == forca
