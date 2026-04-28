import secrets
import string

_UPPERCASE = string.ascii_uppercase
_LOWERCASE = string.ascii_lowercase
_DIGITS = string.digits
_SPECIALS = r"!@#$%^&*()_+-=[]{}|;':\",./<>?"


def calcular_forca(tamanho: int, num_tipos: int) -> str:
    if num_tipos >= 4 and tamanho >= 16:
        return "muito forte"
    if num_tipos >= 3 and tamanho >= 12:
        return "forte"
    if num_tipos >= 2 and tamanho >= 10:
        return "média"
    return "fraca"


def gerar_senha(
    tamanho: int,
    maiusculas: bool,
    minusculas: bool,
    numeros: bool,
    especiais: bool,
) -> tuple[str, str]:
    charset = ""
    garantidos: list[str] = []

    if maiusculas:
        charset += _UPPERCASE
        garantidos.append(secrets.choice(_UPPERCASE))
    if minusculas:
        charset += _LOWERCASE
        garantidos.append(secrets.choice(_LOWERCASE))
    if numeros:
        charset += _DIGITS
        garantidos.append(secrets.choice(_DIGITS))
    if especiais:
        charset += _SPECIALS
        garantidos.append(secrets.choice(_SPECIALS))

    restante = [secrets.choice(charset) for _ in range(tamanho - len(garantidos))]
    chars = garantidos + restante

    secrets.SystemRandom().shuffle(chars)

    senha = "".join(chars)
    num_tipos = sum([maiusculas, minusculas, numeros, especiais])
    forca = calcular_forca(tamanho, num_tipos)

    return senha, forca
