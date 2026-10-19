from pathlib import Path

BACKEND_DIR  = Path(__file__).resolve().parents[2]
FRONTEND_DIR = BACKEND_DIR.parent / "frontend"
DADOS_DIR    = Path(__file__).resolve().parent / "dados"

ORIGEM_FRONTEND = "http://localhost:3000"
