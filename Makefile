.PHONY: help \
        install backend-install frontend-install \
        start backend-start frontend-start \
        test test-integracao coverage coverage-html \
        health audit deps-check clean

BACKEND_DIR  := backend
FRONTEND_DIR := frontend

# ─────────────────────────────────────────────────────────────────────────────
# Alvo padrão
# ─────────────────────────────────────────────────────────────────────────────

.DEFAULT_GOAL := help

help:
	@printf "\n\033[1mGerador de Senhas Seguras — comandos disponíveis\033[0m\n\n"
	@printf "  \033[36mInstalação\033[0m\n"
	@printf "    make install              Instala todas as dependências (backend + frontend)\n"
	@printf "    make backend-install      Instala dependências do backend com uv\n"
	@printf "    make frontend-install     Instala dependências do frontend com npm\n"
	@printf "\n"
	@printf "  \033[36mExecução\033[0m\n"
	@printf "    make start                Inicia backend e frontend simultaneamente\n"
	@printf "    make backend-start        Inicia apenas o backend  → http://127.0.0.1:8000\n"
	@printf "    make frontend-start       Inicia apenas o frontend → http://localhost:3000\n"
	@printf "\n"
	@printf "  \033[36mTestes\033[0m\n"
	@printf "    make test                 Executa todos os testes\n"
	@printf "    make test-integracao      Executa apenas os testes de integração (frontend ↔ backend)\n"
	@printf "    make coverage             Testes com relatório de cobertura no terminal\n"
	@printf "    make coverage-html        Testes com relatório HTML em backend/htmlcov/\n"
	@printf "\n"
	@printf "  \033[36mManutenção\033[0m\n"
	@printf "    make health               Verifica se o backend está respondendo\n"
	@printf "    make audit                Auditoria de segurança das dependências\n"
	@printf "    make deps-check           Lista dependências desatualizadas\n"
	@printf "    make clean                Remove arquivos gerados (venv, cache, node_modules)\n"
	@printf "\n"

# ─────────────────────────────────────────────────────────────────────────────
# Instalação
# ─────────────────────────────────────────────────────────────────────────────

install: backend-install frontend-install
	@printf "\n\033[32m✔ Todas as dependências instaladas.\033[0m\n"

backend-install:
	@printf "\033[1m→ Instalando dependências do backend...\033[0m\n"
	cd $(BACKEND_DIR) && uv sync

frontend-install:
	@printf "\033[1m→ Instalando dependências do frontend...\033[0m\n"
	cd $(FRONTEND_DIR) && npm install

# ─────────────────────────────────────────────────────────────────────────────
# Execução
# ─────────────────────────────────────────────────────────────────────────────

backend-start:
	@printf "\033[1m→ Iniciando backend em http://127.0.0.1:8000\033[0m\n"
	@printf "  Documentação: http://127.0.0.1:8000/docs\n"
	@printf "  Health check: http://127.0.0.1:8000/health\n\n"
	cd $(BACKEND_DIR) && uv run uvicorn main:app --reload

frontend-start:
	@printf "\033[1m→ Iniciando frontend em http://localhost:3000\033[0m\n\n"
	cd $(FRONTEND_DIR) && npm start

start:
	@printf "\033[1m→ Iniciando aplicação completa...\033[0m\n"
	@printf "  Backend  → http://127.0.0.1:8000\n"
	@printf "  Frontend → http://localhost:3000\n"
	@printf "  Use Ctrl+C para encerrar ambos.\n\n"
	@trap 'kill 0' INT; \
		(cd $(BACKEND_DIR) && uv run uvicorn main:app --reload) & \
		(cd $(FRONTEND_DIR) && npm start); \
		wait

# ─────────────────────────────────────────────────────────────────────────────
# Testes
# ─────────────────────────────────────────────────────────────────────────────

test:
	@printf "\033[1m→ Executando testes...\033[0m\n\n"
	cd $(BACKEND_DIR) && uv run pytest

test-integracao:
	@printf "\033[1m→ Executando testes de integração...\033[0m\n\n"
	cd $(BACKEND_DIR) && uv run pytest -m integracao

coverage:
	@printf "\033[1m→ Executando testes com cobertura...\033[0m\n\n"
	cd $(BACKEND_DIR) && uv run pytest --cov --cov-report=term-missing

coverage-html:
	@printf "\033[1m→ Gerando relatório HTML de cobertura...\033[0m\n\n"
	cd $(BACKEND_DIR) && uv run pytest --cov --cov-report=html
	@printf "\n\033[32m✔ Relatório disponível em: backend/htmlcov/index.html\033[0m\n"

# ─────────────────────────────────────────────────────────────────────────────
# Manutenção
# ─────────────────────────────────────────────────────────────────────────────

health:
	@printf "\033[1m→ Verificando backend...\033[0m\n"
	@curl -sf http://127.0.0.1:8000/health | python3 -m json.tool \
		&& printf "\033[32m✔ Backend em execução.\033[0m\n" \
		|| printf "\033[31m✘ Backend não está em execução. Execute: make backend-start\033[0m\n"

audit:
	@printf "\033[1m→ Auditoria de segurança — Backend\033[0m\n\n"
	cd $(BACKEND_DIR) && uv run --with pip-audit pip-audit
	@printf "\n\033[1m→ Auditoria de segurança — Frontend\033[0m\n\n"
	cd $(FRONTEND_DIR) && npm audit || true

deps-check:
	@printf "\033[1m→ Dependências desatualizadas — Backend\033[0m\n\n"
	cd $(BACKEND_DIR) && uv run pip list --outdated
	@printf "\n\033[1m→ Dependências desatualizadas — Frontend\033[0m\n\n"
	cd $(FRONTEND_DIR) && npm outdated || true

# ─────────────────────────────────────────────────────────────────────────────
# Limpeza
# ─────────────────────────────────────────────────────────────────────────────

clean:
	@printf "\033[1m→ Removendo arquivos gerados...\033[0m\n"
	rm -rf $(BACKEND_DIR)/.venv
	rm -rf $(BACKEND_DIR)/.pytest_cache
	rm -rf $(BACKEND_DIR)/.coverage
	rm -rf $(BACKEND_DIR)/htmlcov
	find $(BACKEND_DIR) -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf $(FRONTEND_DIR)/node_modules
	@printf "\033[32m✔ Limpeza concluída.\033[0m\n"
