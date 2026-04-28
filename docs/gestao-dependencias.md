# Gestão de Dependências

Guia para manter as dependências do projeto atualizadas e seguras.

---

## Backend (Python)

### Verificar dependências desatualizadas

**Com pip:**
```
cd backend
pip list --outdated
```

**Com uv:**
```
cd backend
uv lock --upgrade-package fastapi   # atualiza uma dependência específica
uv sync                             # instala as versões atualizadas
```

### Atualizar uma dependência específica

**Com pip:**
```
pip install "fastapi>=0.116.0"
pip freeze | grep -v "^-e" > requirements.txt
```

**Com uv:**
```
uv add "fastapi>=0.116.0"   # atualiza pyproject.toml e o lock file
uv sync
```

### Auditoria de segurança

**Com pip-audit** (instale com `pip install pip-audit`):
```
pip-audit
```

**Com uv:**
```
uv run pip-audit
```

---

## Frontend (Node.js)

### Verificar dependências desatualizadas

```
cd frontend
npm outdated
```

### Atualizar dependências

```
npm update                        # atualiza dentro dos ranges do package.json
npm install express@latest        # atualiza para a versão mais recente de um pacote
```

### Auditoria de segurança

```
npm audit                  # lista vulnerabilidades conhecidas
npm audit fix              # corrige automaticamente onde possível
npm audit fix --force      # corrige quebrando ranges (usar com cautela)
```

---

## Processo recomendado de atualização

Siga estes passos para cada atualização de dependência:

1. **Verificar** quais dependências têm novas versões (`pip list --outdated` / `npm outdated`)
2. **Ler o changelog** do pacote para identificar breaking changes
3. **Atualizar uma dependência por vez**, não todas de uma vez
4. **Rodar os testes** do backend para garantir que nada quebrou:
   ```
   cd backend
   uv run pytest
   ```
5. **Testar manualmente** a aplicação (backend + frontend)
6. **Commitar** com mensagem no padrão Conventional Commits:
   ```
   chore(deps): update express to v4.20.0
   ```

---

## Frequência recomendada

| Tipo de atualização | Quando atualizar |
|---------------------|-----------------|
| **Patch** — correções de bug e segurança (ex.: `4.19.1` → `4.19.2`) | Imediatamente ao ser lançado |
| **Minor** — novas funcionalidades retrocompatíveis (ex.: `4.19.0` → `4.20.0`) | Mensalmente ou a cada sprint |
| **Major** — breaking changes (ex.: `4.x` → `5.x`) | Avaliar impacto; planejar migração em separado |

> **Dica:** configure alertas de segurança no repositório GitHub (Settings → Security → Dependabot alerts)
> para ser notificado automaticamente sobre vulnerabilidades conhecidas.

---

## Versões atuais

### Backend

| Pacote | Versão mínima | Ambiente |
|--------|--------------|----------|
| `fastapi` | `0.115.0` | produção |
| `uvicorn[standard]` | `0.30.0` | produção |
| `pytest` | `8.0.0` | desenvolvimento |
| `httpx` | `0.27.0` | desenvolvimento |
| `pytest-cov` | `5.0.0` | desenvolvimento |

### Frontend

| Pacote | Versão mínima | Ambiente |
|--------|--------------|----------|
| `express` | `4.19.0` | produção |
