import string

import pytest

from generator import _SPECIALS, calcular_forca, gerar_senha


# ---------------------------------------------------------------------------
# calcular_forca
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tamanho,num_tipos,esperado", [
    # fraca: 1 tipo (qualquer tamanho)
    (8,   1, "fraca"),
    (16,  1, "fraca"),
    (128, 1, "fraca"),
    # fraca: 2+ tipos mas tamanho < 10
    (8,  2, "fraca"),
    (9,  2, "fraca"),
    (8,  3, "fraca"),
    (9,  4, "fraca"),
    # média: 2 tipos, tamanho >= 10 (fronteira inferior)
    (10, 2, "média"),
    (11, 2, "média"),
    (15, 2, "média"),
    # média: 3 tipos mas tamanho < 12
    (10, 3, "média"),
    (11, 3, "média"),
    # forte: 3 tipos, tamanho >= 12 (fronteira inferior)
    (12, 3, "forte"),
    (15, 3, "forte"),
    # forte: 4 tipos mas tamanho < 16
    (12, 4, "forte"),
    (15, 4, "forte"),
    # muito forte: 4 tipos, tamanho >= 16 (fronteira inferior)
    (16,  4, "muito forte"),
    (32,  4, "muito forte"),
    (128, 4, "muito forte"),
])
def test_calcular_forca(tamanho, num_tipos, esperado):
    assert calcular_forca(tamanho, num_tipos) == esperado


# ---------------------------------------------------------------------------
# gerar_senha — comprimento
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tamanho", [8, 12, 16, 32, 64, 128])
def test_tamanho_da_senha_corresponde_ao_solicitado(tamanho):
    senha, _ = gerar_senha(tamanho, True, True, True, True)
    assert len(senha) == tamanho


# ---------------------------------------------------------------------------
# gerar_senha — garantia de ao menos 1 char de cada tipo ativo
# ---------------------------------------------------------------------------

def test_contem_maiuscula_quando_ativado():
    senha, _ = gerar_senha(16, True, False, False, False)
    assert any(c in string.ascii_uppercase for c in senha)


def test_contem_minuscula_quando_ativado():
    senha, _ = gerar_senha(16, False, True, False, False)
    assert any(c in string.ascii_lowercase for c in senha)


def test_contem_numero_quando_ativado():
    senha, _ = gerar_senha(16, False, False, True, False)
    assert any(c in string.digits for c in senha)


def test_contem_especial_quando_ativado():
    senha, _ = gerar_senha(16, False, False, False, True)
    assert any(c in _SPECIALS for c in senha)


# ---------------------------------------------------------------------------
# gerar_senha — ausência de tipos desativados
# ---------------------------------------------------------------------------

def test_nao_contem_maiuscula_quando_desativado():
    # tamanho grande para cobrir bem o charset aleatório
    senha, _ = gerar_senha(64, False, True, True, False)
    assert not any(c in string.ascii_uppercase for c in senha)


def test_nao_contem_minuscula_quando_desativado():
    senha, _ = gerar_senha(64, True, False, True, False)
    assert not any(c in string.ascii_lowercase for c in senha)


def test_nao_contem_numero_quando_desativado():
    senha, _ = gerar_senha(64, True, True, False, False)
    assert not any(c in string.digits for c in senha)


def test_nao_contem_especial_quando_desativado():
    senha, _ = gerar_senha(64, True, True, True, False)
    assert not any(c in _SPECIALS for c in senha)


# ---------------------------------------------------------------------------
# gerar_senha — charset exclusivo
# ---------------------------------------------------------------------------

def test_apenas_minusculas_usa_somente_minusculas():
    senha, _ = gerar_senha(32, False, True, False, False)
    assert all(c in string.ascii_lowercase for c in senha)


def test_apenas_numeros_usa_somente_digitos():
    senha, _ = gerar_senha(32, False, False, True, False)
    assert all(c in string.digits for c in senha)


def test_apenas_especiais_usa_somente_especiais():
    senha, _ = gerar_senha(32, False, False, False, True)
    assert all(c in _SPECIALS for c in senha)


# ---------------------------------------------------------------------------
# gerar_senha — força retornada
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tamanho,maiusculas,minusculas,numeros,especiais,forca_esperada", [
    (8,  False, True,  False, False, "fraca"),       # 1 tipo
    (9,  True,  True,  False, False, "fraca"),        # 2 tipos, tamanho < 10
    (10, True,  True,  False, False, "média"),        # 2 tipos, tamanho = 10
    (12, True,  True,  True,  False, "forte"),        # 3 tipos, tamanho = 12
    (16, True,  True,  True,  True,  "muito forte"),  # 4 tipos, tamanho = 16
])
def test_forca_retornada_pela_geracao(tamanho, maiusculas, minusculas, numeros, especiais, forca_esperada):
    _, forca = gerar_senha(tamanho, maiusculas, minusculas, numeros, especiais)
    assert forca == forca_esperada


# ---------------------------------------------------------------------------
# gerar_senha — charset de especiais correto (sem barra invertida)
# ---------------------------------------------------------------------------

def test_especiais_nao_contem_barra_invertida():
    assert "\\" not in _SPECIALS


def test_especiais_contem_aspas_duplas():
    assert '"' in _SPECIALS


def test_especiais_contem_aspas_simples():
    assert "'" in _SPECIALS


def test_especiais_contem_barra():
    assert "/" in _SPECIALS
