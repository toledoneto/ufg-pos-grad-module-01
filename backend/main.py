import logging
import os
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from generator import gerar_senha
from models import SenhaRequest, SenhaResponse

# ── Logging ──────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ── CORS ─────────────────────────────────────────────────────────────────────

_raw_origins = os.getenv("ALLOWED_ORIGINS", "*")
ALLOWED_ORIGINS = (
    ["*"] if _raw_origins.strip() == "*"
    else [o.strip() for o in _raw_origins.split(",") if o.strip()]
)

# ── App ───────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Gerador de Senhas Seguras",
    description="API para geração de senhas seguras com critérios definidos pelo usuário.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

logger.info("Gerador de Senhas Seguras v%s iniciado", app.version)
logger.info("CORS permitido para: %s", ALLOWED_ORIGINS)

# ── Tratamento de erros de validação ─────────────────────────────────────────

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning("Requisição inválida em %s | erros: %s", request.url.path, exc.errors())
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

# ── Rotas ─────────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    logger.debug("Health check solicitado")
    return {
        "status": "ok",
        "version": app.version,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _tipos_ativos(req: SenhaRequest) -> list[str]:
    pares = [
        ("maiusculas", req.maiusculas),
        ("minusculas", req.minusculas),
        ("numeros",    req.numeros),
        ("especiais",  req.especiais),
    ]
    return [nome for nome, ativo in pares if ativo]


@app.post("/api/gerar-senha", response_model=SenhaResponse)
def gerar(request: SenhaRequest) -> SenhaResponse:
    tipos = _tipos_ativos(request)
    logger.info("Gerando senha | tamanho=%d tipos=%s", request.tamanho, tipos)

    senha, forca = gerar_senha(
        tamanho=request.tamanho,
        maiusculas=request.maiusculas,
        minusculas=request.minusculas,
        numeros=request.numeros,
        especiais=request.especiais,
    )

    logger.info("Senha gerada com sucesso | forca=%s", forca)
    return SenhaResponse(senha=senha, forca=forca)
