from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from generator import gerar_senha
from models import SenhaRequest, SenhaResponse

app = FastAPI(
    title="Gerador de Senhas Seguras",
    description="API para geração de senhas seguras com critérios definidos pelo usuário.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


@app.post("/api/gerar-senha", response_model=SenhaResponse)
def gerar(request: SenhaRequest) -> SenhaResponse:
    senha, forca = gerar_senha(
        tamanho=request.tamanho,
        maiusculas=request.maiusculas,
        minusculas=request.minusculas,
        numeros=request.numeros,
        especiais=request.especiais,
    )
    return SenhaResponse(senha=senha, forca=forca)
