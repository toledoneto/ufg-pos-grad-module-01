"""
Fixtures dos testes de integração.

Sobe a API real com uvicorn em um processo separado (porta livre aleatória),
de forma que as requisições atravessem a pilha HTTP completa:
socket → uvicorn → middleware CORS → validação Pydantic → gerador → handler de erros.
"""
import os
import socket
import subprocess
import sys
import time

import httpx
import pytest

from .apoio import BACKEND_DIR, ORIGEM_FRONTEND


def _porta_livre() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _subir_servidor(env_extra: dict[str, str] | None = None):
    porta = _porta_livre()
    env = {**os.environ, **(env_extra or {})}
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", str(porta)],
        cwd=BACKEND_DIR,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    base_url = f"http://127.0.0.1:{porta}"

    limite = time.monotonic() + 15
    while time.monotonic() < limite:
        if proc.poll() is not None:
            raise RuntimeError("uvicorn encerrou antes de ficar disponível")
        try:
            if httpx.get(f"{base_url}/health", timeout=0.5).status_code == 200:
                return proc, base_url
        except httpx.TransportError:
            time.sleep(0.1)

    proc.terminate()
    raise RuntimeError("uvicorn não respondeu ao /health em 15s")


def _derrubar(proc: subprocess.Popen):
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


@pytest.fixture(scope="session")
def api_real():
    """Cliente HTTP para a API rodando com a configuração padrão (ALLOWED_ORIGINS=*)."""
    proc, base_url = _subir_servidor({"ALLOWED_ORIGINS": "*"})
    with httpx.Client(base_url=base_url, timeout=5) as client:
        yield client
    _derrubar(proc)


@pytest.fixture(scope="session")
def api_cors_restrito():
    """Cliente HTTP para a API com CORS restrito à origem do frontend."""
    proc, base_url = _subir_servidor({"ALLOWED_ORIGINS": ORIGEM_FRONTEND})
    with httpx.Client(base_url=base_url, timeout=5) as client:
        yield client
    _derrubar(proc)
