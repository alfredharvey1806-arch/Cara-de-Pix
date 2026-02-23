# 🤖 AGENTE FOLLOWERS ANALYZER - SETUP COMPLETO

**Status:** ✅ 95% PRONTO - Aguardando 2 IDs do Google

---

## 🎯 RESUMO EXECUTIVO

Seu sistema automático de captura de novos seguidores do Instagram está **quase pronto para rodar 24/7**. 

**O que está feito:**
- ✅ Scripts de monitoramento implementados
- ✅ Sistema de rastreamento com JSON + CSV
- ✅ Chrome Relay integrado (Instagram pronto)
- ✅ Estrutura de pastas criada
- ✅ Cron job aguardando ativação

**O que falta:**
- ⏳ 2 IDs do Google (Drive + Sheets)

---

## 🚀 PRÓXIMOS PASSOS (5 MINUTOS)

### Passo 1: Copiar Google Drive Folder ID

```
1. Abra: https://drive.google.com
2. Procure a pasta "Novos Seguidores"
3. COPIE o ID da URL (após /folders/):
   
   https://drive.google.com/drive/folders/[COPIE-ISTO]
   
4. Você terá algo como:
   1a2b3c4d5e6f7g8h9i0j...
```

### Passo 2: Copiar Google Sheets ID

```
1. Abra: https://sheets.google.com
2. Procure o sheet "Followers Tracker"
3. COPIE o ID da URL (após /spreadsheets/d/):
   
   https://docs.google.com/spreadsheets/d/[COPIE-ISTO]/edit
   
4. Você terá algo como:
   1bCdEfGhIjKlMnOpQrStUvWxYz...
```

### Passo 3: Colar os IDs

```bash
# Editar o arquivo de configuração:
nano /home/harvey1806/.openclaw/workspace/followers_config.json

# Trocar estas linhas:
# "folder_id": "PENDING"     →  "folder_id": "[SEU_DRIVE_ID]"
# "sheet_id": "PENDING"      →  "sheet_id": "[SEU_SHEETS_ID]"

# Salvar (Ctrl+X, Y, Enter)
```

### Passo 4: Ativar o Monitoramento

```bash
bash /home/harvey1806/.openclaw/workspace/activate_monitoring.sh
```

---

## 📊 ARQUIVOS CRIADOS

```
/home/harvey1806/.openclaw/workspace/
├── followers_analyzer.py          # Core: extrai @usernames e captura
├── monitor_followers.py           # Script que roda a cada 5 minutos
├── setup_google_api.py            # Setup inicial
├── activate_monitoring.sh          # Ativa cron job
├── followers_config.json          # Configuração central
├── followers_tracker.csv          # Export para Google Sheets
├── status_report.md               # Relatório detalhado
└── README_FOLLOWERS_ANALYZER.md   # Este arquivo

/home/harvey1806/Documents/Seguidores/
└── .metadata/tracking.json        # Banco de dados local
```

---

## 🔄 COMO FUNCIONA (Fluxo Automático)

```
A cada 5 minutos:

1. ✅ Monitor verifica pasta "Novos Seguidores" no Drive
2. ✅ Baixa novas imagens (se houver)
3. ✅ Extrai todos os @usernames da imagem (usando IA)
4. ✅ Compara com Google Sheets para evitar duplicatas
5. ✅ Para cada @ novo:
   - Abre no Instagram (Chrome Relay)
   - Tira screenshot
   - Salva em: /home/harvey1806/Documents/Seguidores/@username_TIMESTAMP.png
6. ✅ Atualiza Google Sheets com:
   @username | ✅ Capturado | Data | Arquivo Local | Arquivo Origem
7. ✅ Envia notificação: "✅ Capturados 5 | Duplicatas 2"

Máximo: 10 @ por ciclo (evita rate limit)
Timeout: 15 segundos por screenshot
```

---

## 📋 EXEMPLO DE RESULTADO

Após 1 hora com a pasta "Novos Seguidores" recebendo uploads:

```
Google Sheets "Followers Tracker":

@username1          ✅ Capturado  15/02/2026 16:35  @username1_20260215_163501.png  image1.png
@username2          ✅ Capturado  15/02/2026 16:40  @username2_20260215_164001.png  image2.png
@username3          ✅ Capturado  15/02/2026 16:45  @username3_20260215_164501.png  image2.png
@olduser1           ♻️ Duplicata 15/02/2026 16:50  -                               image3.png
@username4          ❌ Erro      15/02/2026 16:55  Timeout capturando screenshot    image3.png
@username5          ✅ Capturado  15/02/2026 17:00  @username5_20260215_170001.png  image4.png
```

---

## 🔧 CONFIGURAÇÃO ATUAL

```json
{
  "monitoring": {
    "interval_minutes": 5,              # A cada 5 minutos
    "max_per_cycle": 10,                # Máximo 10 @ por ciclo
    "screenshot_timeout_seconds": 15,   # Timeout 15s
    "status": "READY_TO_ACTIVATE"       # Aguardando ativação
  },
  "instagram": {
    "account": "alfredharvey1806",
    "auth_status": "LOGGED_IN",
    "screenshots_dir": "/home/harvey1806/Documents/Seguidores"
  }
}
```

---

## 📞 NOTIFICAÇÕES

Após cada ciclo, você receberá resumos como:

```
✅ Ciclo às 16:35
   Processados: 5
   ✅ Capturados: 3 (@user1, @user2, @user3)
   ♻️  Duplicatas: 2 (@old1, @old2)
   ❌ Erros: 0
   Próximo ciclo: em 5 minutos
```

---

## ✅ CHECKLIST DE ATIVAÇÃO

- [ ] Copiar Google Drive Folder ID
- [ ] Copiar Google Sheets Spreadsheet ID
- [ ] Colar os IDs em `followers_config.json`
- [ ] Executar: `bash activate_monitoring.sh`
- [ ] Verificar se cron job foi adicionado
- [ ] Sistema rodando 24/7 ✅

---

## 🐛 TROUBLESHOOTING

### "Configuração incompleta"
```bash
# Verificar o que falta:
grep '"PENDING"' /home/harvey1806/.openclaw/workspace/followers_config.json

# Editar e preencher os IDs
nano /home/harvey1806/.openclaw/workspace/followers_config.json
```

### Verificar se monitoramento está ativo
```bash
crontab -l
# Deve aparecer uma linha com "monitor_followers.py"
```

### Ver log em tempo real
```bash
tail -f /home/harvey1806/.openclaw/workspace/monitor_followers.log
```

### Executar ciclo manualmente
```bash
python3 /home/harvey1806/.openclaw/workspace/monitor_followers.py
```

---

## 📁 ESTRUTURA FINAL

```
HOME
├── .openclaw/workspace/
│   ├── followers_analyzer.py       ✅
│   ├── monitor_followers.py        ✅
│   ├── activate_monitoring.sh      ✅
│   ├── followers_config.json       ✅ (NEEDS: IDs)
│   ├── followers_tracker.csv       ✅
│   ├── status_report.md            ✅
│   └── README_FOLLOWERS_ANALYZER.md ✅
│
└── Documents/Seguidores/
    ├── .metadata/
    │   └── tracking.json           ✅
    ├── @user1_20260215_163501.png  ⏳
    ├── @user2_20260215_164001.png  ⏳
    └── ...
```

---

## 🎉 STATUS FINAL

```
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║  ✅ AGENTE FOLLOWERS ANALYZER PRONTO!                      ║
║                                                            ║
║  Faltam apenas 2 IDs do Google                            ║
║  Tempo estimado: 5 minutos                                ║
║                                                            ║
║  Depois: Sistema roda 24/7 com monitoramento a cada       ║
║          5 minutos, capturando screenshots automaticamente ║
║                                                            ║
║  Pedro, forneça os IDs e estarei 100% operacional! 🚀     ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

---

**Criado em:** 15/02/2026 às 16:34 GMT-3  
**Versão:** 1.0  
**Desenvolvido por:** AGENTE FOLLOWERS ANALYZER
