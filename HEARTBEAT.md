# HEARTBEAT.md – Rotina de Check-in Automático

## O que é
Arquivo que define o que fazer quando OpenClaw faz check-in automático (a cada 1h via Ollama).

## Checklist padrão (responda com HEARTBEAT_OK se tudo ok)

- [ ] Nenhum blocker crítico
- [ ] Projetos em sync
- [ ] Tokens dentro do budget
- [ ] Nenhuma tarefa pendente

## Se algo não tá ok
Responda com ALERT seguido do problema, não com HEARTBEAT_OK.

## Exemplos de alerts

```
ALERT: Instagram scraper está falhando — Service Account não foi configurada
```

```
ALERT: Subagentes ainda não criados — Bloqueador para orquestrador
```

## Horário
- Heartbeat roda a cada **1h** via `ollama/llama3.2:3b` (local, grátis)
- Via Telegram DM privada

## Setup
- Habilitado em: `openclaw.json` → `heartbeat.every: "1h"`
- Modelo: `ollama/llama3.2:3b` (local)
- Sem custo de API
