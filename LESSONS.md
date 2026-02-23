# LESSONS.md – Aprendizados & Soluções

Registro de problemas encontrados e como foram resolvidos. Consultar antes de debugar qualquer issue.

---

## 2026-02-21 | Bash: syntax error near unexpected token `(`

**Problema:** Script `setup_hybrid.sh` falhava na linha 69 com erro de sintaxe em parênteses.
**Causa:** Subshell `(crontab -l 2>/dev/null || true; echo "$CRON_JOB") | crontab -` conflitava com parsing do bash dentro de heredocs.
**Solução:** Trocar parênteses por chaves: `{ crontab -l 2>/dev/null || true; echo "$CRON_JOB"; } | crontab -`
**Regra:** Em pipelines bash, preferir `{ ...; }` sobre `(...)` quando dentro de scripts complexos com heredocs.

---

## 2026-02-21 | OpenClaw Pairing: comando incompleto

**Problema:** `openclaw pairing approve telegram` sem código dá erro.
**Causa:** Comando exige 2 argumentos: `<channel>` e `<code>`.
**Solução:** Primeiro rodar `openclaw pairing list telegram` para ver o código, depois `openclaw pairing approve telegram <CODIGO>`.
**Regra:** Sempre listar antes de aprovar. Códigos expiram em 1 hora.

---

## 2026-02-21 | Telegram: setup completo

**Problema:** Conectar OpenClaw no Telegram.
**Solução:**
1. BotFather → `/newbot` → salvar token
2. Colocar token em `openclaw.json` → `channels.telegram.botToken`
3. `openclaw gateway restart`
4. Mandar DM pro bot → `openclaw pairing list telegram` → `openclaw pairing approve telegram <CODE>`
**Regra:** Privacy mode desabilitado (`/setprivacy` no BotFather) se quiser ver msgs de grupo sem menção.
