# BOOTSTRAP.md – Setup Inicial para Economia de Tokens

## 📊 Objetivo
Reduzir context size de **~50KB → 2-8KB** + Heartbeat grátis via Ollama

## ✅ Checklist

### 1. Session Initialization (CONCLUÍDO)
- [x] SOUL.md enxuto
- [x] USER.md enxuto
- [x] IDENTITY.md enxuto
- [x] memory/2026-02-21.md criado
- [x] Carrega apenas esses 4 arquivos por padrão

### 2. Model Routing (CONCLUÍDO)
- [x] openclaw.json com Haiku default
- [x] Aliases "haiku" e "sonnet" configurados
- [x] Model Selection Rule no AGENTS.md

### 3. Heartbeat Ollama (PENDENTE)
**Você precisa fazer isso:**

```bash
# 1. Instalar Ollama (macOS/Linux)
# macOS:
brew install ollama

# Linux:
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Puxar o modelo leve
ollama pull llama3.2:3b

# 3. Testar (em outro terminal)
ollama serve

# 4. Em outro terminal, validar:
ollama run llama3.2:3b "respond with OK"
```

Depois volta aqui que valida tudo.

### 4. Rate Limits + Budgets (PENDENTE)
Você precisa colocar no seu workflow:
- 5s mínimo entre chamadas
- 10s entre buscas
- Máx 5 buscas por batch
- Daily: $5 warning em 75%
- Monthly: $200 warning em 75%

### 5. Prompt Caching (CONCLUÍDO EM CONFIG)
- [x] Cache habilitado no openclaw.json (ttl 5m)
- [x] Estrutura de arquivos pronta:
  - Estável (SOUL, USER, IDENTITY, projetos): cacheável
  - Dinâmico (memory/, tool outputs): não cachear

### 6. Validação Final
```bash
# Rodar quando Ollama estiver pronto:
openclaw shell
> session_status

# Você deve ver:
# - Context: 2-8KB (era ~50KB)
# - Default Model: haiku
# - Heartbeat: ollama/llama3.2:3b (local, sem API)
```

## 📝 Notas
- Arquivo criado: 2026-02-21 10:35 GMT-3
- próximo refresh: quando Ollama subir
