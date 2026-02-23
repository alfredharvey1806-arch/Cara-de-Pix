# 🚀 SOLUÇÃO HYBRID - Deploy Completo

## Objetivo
Eliminar dependência de Browser Relay criando:
1. **Service Account** para Google Drive + Sheets (APIs diretas)
2. **Firefox Headless** local para Instagram (automação local)
3. **Cron Job** executando a cada 5 minutos (100% autônomo)

---

## PASSO 1: Criar Service Account Google Cloud

### 1.1 Acessar Google Cloud Console
```
https://console.cloud.google.com
```

### 1.2 Criar novo projeto
- Clique em "Selecionar projeto" (canto superior)
- "Novo projeto"
- Nome: `Instagram Followers Analyzer`
- Crie

### 1.3 Ativar APIs necessárias
1. No menu superior, clique "APIs e serviços"
2. Clique "Ativar APIs e serviços"
3. Procure e ative:
   - **Google Drive API**
   - **Google Sheets API**

### 1.4 Criar Service Account
1. No menu esquerdo: "Credenciais"
2. Clique "Criar credenciais" → "Conta de serviço"
3. Nome: `followers-analyzer`
4. Descrição: `Automação Instagram Followers`
5. Clique "Criar e continuar"
6. Conceda papel: `Editor` (ou `Viewer + Editor de folhas`)
7. Clique "Continuar"
8. Clique "Concluído"

### 1.5 Gerar Chave JSON
1. Volte em "Credenciais"
2. Clique na conta criada (`followers-analyzer`)
3. Vá em "Chaves"
4. Clique "Adicionar chave" → "Criar nova chave"
5. Selecione "JSON"
6. Clique "Criar"
7. **Arquivo JSON será baixado** → Guarde com segurança!

---

## PASSO 2: Configurar Pastas e Permissions

### 2.1 Compartilhar Google Drive com Service Account
1. Abra pasta `Novos Seguidores` em Drive
2. Clique "Compartilhar"
3. Cole email da service account (encontra no JSON como `client_email`)
4. Dê permissão: **Editor**

### 2.2 Compartilhar Google Sheets
1. Abra `Followers Tracker` em Sheets
2. Clique "Compartilhar"
3. Cole email da service account
4. Dê permissão: **Editor**

---

## PASSO 3: Implementar Scripts Python com APIs

### Script 1: Google Drive Monitor
```python
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_drive(file_path, folder_id):
    """Upload arquivo para Google Drive"""
    creds = service_account.Credentials.from_service_account_file(
        'service_account.json',
        scopes=['https://www.googleapis.com/auth/drive']
    )
    service = build('drive', 'v3', credentials=creds)
    
    file_metadata = {'name': os.path.basename(file_path), 'parents': [folder_id]}
    media = MediaFileUpload(file_path)
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()
```

### Script 2: Google Sheets Update
```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

def update_sheets(spreadsheet_id, username, status, timestamp):
    """Atualizar Google Sheets com dados"""
    creds = service_account.Credentials.from_service_account_file(
        'service_account.json',
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    service = build('sheets', 'v4', credentials=creds)
    
    values = [[username, status, timestamp, file_path, origin_file, 1]]
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range='A:F',
        valueInputOption='USER_ENTERED',
        body={'values': values}
    ).execute()
```

### Script 3: Instagram Firefox Headless
```python
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

options = Options()
options.add_argument('--headless')  # Rodar em background
options.add_argument('--no-sandbox')

driver = webdriver.Firefox(options=options)
driver.get('https://www.instagram.com/@username')
time.sleep(3)
driver.save_screenshot('screenshot.png')
driver.quit()
```

---

## PASSO 4: Arquivo de Credenciais

Salve o JSON baixado em:
```
/home/harvey1806/.openclaw/workspace/projects/instagram-scraper/service_account.json
```

⚠️ **Segurança**: Nunca comitar este arquivo no git!

---

## PASSO 5: Montar Agente Autônomo

Criar script principal que executa tudo:
```bash
#!/bin/bash
# /home/harvey1806/.openclaw/workspace/agente-followers.sh

python3 /home/harvey1806/.openclaw/workspace/projects/instagram-scraper/agente_hybrid.py
```

---

## PASSO 6: Agendar com Cron

```bash
# Adicionar ao crontab
crontab -e

# Adicionar linha:
*/5 * * * * /home/harvey1806/.openclaw/workspace/agente-followers.sh >> /home/harvey1806/Documents/Seguidores/.metadata/cron.log 2>&1
```

---

## PASSO 7: Testar

```bash
# Executar manualmente
bash /home/harvey1806/.openclaw/workspace/agente-followers.sh

# Ver logs
tail -f /home/harvey1806/Documents/Seguidores/.metadata/cron.log
```

---

## ✅ Resultado Final

🟢 **Sem dependência de Browser Relay**
🟢 **Google Drive + Sheets via APIs (100% confiável)**
🟢 **Instagram via Firefox Headless Local**
🟢 **Executa a cada 5 minutos (24/7)**
🟢 **Logging completo**
🟢 **Notificação automática**

---

## Status
📋 Pronto para implementação
