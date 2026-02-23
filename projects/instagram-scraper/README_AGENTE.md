# 🤖 AGENTE FOLLOWERS ANALYZER - PRONTO PARA USAR

## ✅ O QUE FOI CRIADO

### 1. 📁 Estrutura Local
```
/home/harvey1806/Documents/Seguidores/
├── @pedrosallun_20260215_162628.png (exemplo)
├── index.md (log de capturas)
├── .metadata/
│   ├── agent_config.json
│   └── log.txt
```

### 2. 📊 Google Sheets (VOCÊ PRECISA CRIAR)
**Nome**: `Followers Tracker`
**Headers**:
- A: @username
- B: Status (✅ Capturado / ⏳ Pendente / ❌ Erro)
- C: Data/Hora
- D: Arquivo Local
- E: Arquivo Origem
- F: Tentativas

### 3. 📱 Pasta Google Drive (VOCÊ PRECISA CRIAR)
**Nome**: `Novos Seguidores`
**O que vai receber**: Imagens PNG/JPG com prints de novos seguidores

### 4. 🤖 Agente Especializado
- **Status**: ✅ ATIVADO E PRONTO
- **Modo**: Autonomous (roda 24/7)
- **Verificação**: A cada 5 minutos
- **Ações**: Extrai @ → Verifica duplicatas → Captura → Atualiza Sheets → Notifica

---

## 🚀 COMO USAR

### Passo 1: Criar Google Sheets (MANUAL)
1. Acesse [Google Sheets](https://sheets.google.com)
2. Clique "Criar novo" → "Planilha"
3. Renomeie para: `Followers Tracker`
4. Crie os headers na linha 1:
   ```
   @username | Status | Data/Hora | Arquivo Local | Arquivo Origem | Tentativas
   ```
5. **Compartilhe com**: alfredharvey1806@gmail.com (edição)

### Passo 2: Criar Pasta Google Drive (MANUAL)
1. Acesse [Google Drive](https://drive.google.com)
2. Clique "Criar" → "Pasta"
3. Renomeie para: `Novos Seguidores`
4. **Compartilhe com**: alfredharvey1806@gmail.com (edição)

### Passo 3: Subir Imagens
1. Abra a pasta `Novos Seguidores`
2. Suba uma imagem PNG/JPG com print de novos seguidores
3. **Exemplo**: foto da tela do Instagram com lista "Novos Seguidores: @user1, @user2, @user3"

### Passo 4: Agente Processa Automaticamente
O agente irá:
- ✅ Detectar a imagem
- ✅ Extrair @usernames
- ✅ Verificar se já foram capturados
- ✅ Tirar screenshots dos novos
- ✅ Atualizar Google Sheets
- ✅ Notificar quando terminar

---

## 📋 EXEMPLO DE FLUXO

```
[17:00] Você sobe "followers_screenshot.png" em Novos Seguidores
         ↓
[17:01] Agente detecta arquivo
         ↓
[17:02] Agente extrai: @pedrosallun, @john_doe, @maria_silva
         ↓
[17:03] Agente verifica em Sheets:
         - @pedrosallun → ✅ Já capturado (SKIP)
         - @john_doe → ⏳ Novo (CAPTURAR)
         - @maria_silva → ⏳ Novo (CAPTURAR)
         ↓
[17:05] Agente tira 2 screenshots
         - /home/harvey1806/Documents/Seguidores/@john_doe_20260215_170500.png
         - /home/harvey1806/Documents/Seguidores/@maria_silva_20260215_170510.png
         ↓
[17:06] Agente atualiza Sheets:
         @john_doe | ✅ Capturado | 2026-02-15 17:05:00 | ... | followers_screenshot.png
         @maria_silva | ✅ Capturado | 2026-02-15 17:05:10 | ... | followers_screenshot.png
         ↓
[17:07] Agente notifica Pedro:
         "✅ Processados 3 @ | Capturados 2 novos | Duplicatas 1"
```

---

## 🎯 AGENTE ESTÁ FAZENDO

✅ Monitorar Google Drive a cada 5 minutos
✅ Extrair @usernames usando visão (Claude Vision)
✅ Verificar duplicatas em Google Sheets
✅ Capturar screenshots via Chrome Relay
✅ Salvar em /home/harvey1806/Documents/Seguidores/
✅ Atualizar planilha automaticamente
✅ Notificar após cada ciclo
✅ Logar todas as ações

---

## 🔧 CONFIGURAÇÃO AVANÇADA

Se quiser ajustar intervalo de verificação:
- Editar: `/home/harvey1806/Documents/Seguidores/.metadata/agent_config.json`
- Campo: `"interval_seconds": 300` (mude para outro valor em segundos)

Se quiser parar o agente:
- Use: `openclaw cron remove` (se estiver usando cron)
- Ou: Clique "stop" em Sessions

---

## ✨ STATUS FINAL

🟢 **AGENTE 100% PRONTO**

- ✅ Estrutura local criada
- ✅ Agente ativado e aguardando
- ✅ Chrome Relay logado no Instagram
- ✅ Sistema de logging ativo
- ✅ Notificações configuradas

**Próximo passo**: Criar Google Sheets + Drive (manual) → Subir primeira imagem → Agente começa a processar

**Tempo estimado para primeira execução**: 5 minutos

---

## 📞 SUPORTE

Se tiver dúvidas:
1. Verifique o log: `/home/harvey1806/Documents/Seguidores/.metadata/log.txt`
2. Verifique config: `/home/harvey1806/Documents/Seguidores/.metadata/agent_config.json`
3. Avise Alfred (eu) e vou corrigir

