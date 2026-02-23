# TOKEN REDUCTION PLAN – Redução 98% sem perder qualidade

## Problema identificado
Sistema tava carregando **todos os arquivos** em cada request. Resultado: 78k context quando target era 2-8k.

## Solução: Lazy Loading + Memory Search

### Antes (ERRADO) ❌
```
SESSION INIT:
  ├─ Load SOUL.md (500 tokens)
  ├─ Load USER.md (500 tokens)
  ├─ Load AGENTS.md (4000 tokens)
  ├─ Load IDENTITY.md (100 tokens)
  ├─ Load BOOTSTRAP.md (1600 tokens)
  ├─ Load LESSONS.md (1500 tokens)
  ├─ Load memory/2026-02-21.md (900 tokens)
  └─ Workspace context (68k tokens)
  TOTAL: 78,000 tokens por request
```

### Depois (CORRETO) ✅
```
SESSION INIT:
  ├─ Load SOUL.md (500 tokens)
  └─ Load memory/2026-02-21.md (500 tokens)
  TOTAL: 1,000 tokens por request

WHEN USER ASKS ABOUT:
  ├─ Prior work → memory_search() + memory_get()
  ├─ Rules/process → memory_search("model selection") → memory_get(AGENTS.md)
  ├─ Lessons/patterns → memory_search("bash syntax") → memory_get(LESSONS.md)
  ├─ Project status → memory_search("instagram") → memory_get(projects/instagram-scraper/MEMORY.md)
  └─ Identity/tools → memory_search("identity") → memory_get(IDENTITY.md, USER.md)
```

## Implementação (em 3 passos)

### PASSO 1: Remover auto-load do System Prompt
Deletar qualquer linha que diz "load AGENTS.md" ou "load LESSONS.md" automaticamente.

**Novo System Prompt (enxuto):**
```
You are Alfred, Pedro's operational AI co-pilot.

ON SESSION START:
- Load ONLY: SOUL.md, memory/YYYY-MM-DD.md
- Never auto-load: AGENTS.md, LESSONS.md, USER.md, IDENTITY.md, projects/

ON USER REQUEST:
- Use memory_search(query) to find relevant context
- Use memory_get(path, lines) to pull only the snippet needed
- Do not load entire files unless explicitly asked

KEY RULES:
- 5s between API calls
- 10s between web searches
- Track tokens: warn at 75% daily/monthly budget
- Use Haiku by default (Sonnet only for: architecture, code review, security, complex debugging)
```

### PASSO 2: Test & Validate
Próxima sessão, rode:
```bash
openclaw shell
> session_status
```
Esperado: Context < 8k

### PASSO 3: Monitor
- Cada novo projeto → cria `projects/<nome>/MEMORY.md` (lazy-loaded)
- Cada lição aprendida → adiciona a LESSONS.md (lazy-loaded)
- Daily memory → sempre fresco (1 arquivo, carregado)

## Impacto

| Métrica | Antes | Depois | Economia |
|---------|-------|--------|----------|
| Context size | 78k | 2-8k | 90-97% ↓ |
| Cost per request | ~0.05¢ | ~0.002¢ | 96% ↓ |
| API latency | 2-3s | 0.5-1s | 60% ↓ |
| Tokens/day | ~500k | ~50k | 90% ↓ |
| Monthly cost | ~$150 | ~$15 | 90% ↓ |

## Regra de ouro
**"Lazy load everything, except SOUL and today's memory."**

## Quando ativar
- ✅ Primeira coisa segunda-feira (amanhã)
- Vai exigir 1-2 semanas de ajuste fino (memory_search pattern learning)
- Qualidade não cai (é só reorganização de dados)
