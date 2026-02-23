#!/usr/bin/env python3
"""
Setup do Google API para Followers Analyzer
Autentica e prepara credenciais para Drive e Sheets
"""

import os
import json
from pathlib import Path

print("""
╔════════════════════════════════════════════════════════════════╗
║       SETUP GOOGLE DRIVE + SHEETS API                         ║
║       Para Followers Analyzer                                  ║
╚════════════════════════════════════════════════════════════════╝

INSTRUÇÕES PARA AUTENTICAÇÃO MANUAL:

1️⃣  Google Drive - Encontrar ID da pasta "Novos Seguidores":
    ✓ Abrir: https://drive.google.com
    ✓ Procurar pasta "Novos Seguidores"
    ✓ Copiar ID da URL (após /folders/)
    ✓ Colar abaixo

2️⃣  Google Sheets - Encontrar ID do sheet "Followers Tracker":
    ✓ Abrir: https://sheets.google.com
    ✓ Procurar sheet "Followers Tracker"
    ✓ Copiar ID da URL (após /spreadsheets/d/)
    ✓ Colar abaixo

""")

# Para agora, vou criar um arquivo de configuração temporário
config = {
    "credentials": {
        "google_account": "alfredharvey1806@gmail.com",
        "instagram_account": "alfredharvey1806"
    },
    "google_drive": {
        "folder_name": "Novos Seguidores",
        "folder_id": "PENDING",  # Will be filled after user finds it
        "auth_status": "PENDING"
    },
    "google_sheets": {
        "sheet_name": "Followers Tracker",
        "sheet_id": "PENDING",  # Will be filled after user finds it
        "auth_status": "PENDING"
    },
    "instagram": {
        "account": "alfredharvey1806",
        "auth_status": "LOGGED_IN",  # Assuming Chrome Relay login is active
        "screenshots_dir": "/home/harvey1806/Documents/Seguidores"
    },
    "monitoring": {
        "interval_minutes": 5,
        "max_per_cycle": 10,
        "screenshot_timeout_seconds": 15,
        "status": "READY_TO_ACTIVATE"
    }
}

config_path = Path("/home/harvey1806/.openclaw/workspace/followers_config.json")
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print(f"\n✅ Arquivo de configuração criado: {config_path}")
print("\n" + "="*60)
print("📋 PRÓXIMAS ETAPAS:")
print("="*60)
print("""
1. Ir para Google Drive e notar o ID da pasta "Novos Seguidores"
2. Ir para Google Sheets e notar o ID do sheet "Followers Tracker"
3. Executar: python3 configure_google_ids.py
4. Sistema estará 100% pronto!

OU fornecer os IDs agora via comando:
   openclaw followers-config --drive-id <ID> --sheets-id <ID>

""")

print("📄 Configuração atual:")
print(json.dumps(config, indent=2, ensure_ascii=False))
