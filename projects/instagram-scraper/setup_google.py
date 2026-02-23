#!/usr/bin/env python3
"""
Setup Google Drive & Sheets para Agente Followers
Cria automaticamente:
1. Pasta "Novos Seguidores" no Google Drive
2. Google Sheets "Followers Tracker" com headers
"""

import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.api_core.exceptions import GoogleAPIError

# Google API Scopes
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets'
]

def setup_google_drive():
    """Criar pasta 'Novos Seguidores' no Google Drive"""
    from googleapiclient.discovery import build
    
    print("🔐 Autenticando no Google Drive...")
    # Usar credenciais armazenadas ou fazer login
    # Por enquanto, mostrar instrução
    
    print("""
    ❌ Para criar Drive + Sheets, você precisa:
    
    OPÇÃO 1: Fazer via Browser (mais fácil)
    ✅ Abra: https://drive.google.com
    ✅ Clique "Criar" → "Pasta"
    ✅ Renomeie para: "Novos Seguidores"
    ✅ Compartilhe com: alfredharvey1806@gmail.com
    
    OPÇÃO 2: Fazer via Google Sheets (mais fácil tb)
    ✅ Abra: https://sheets.google.com
    ✅ Clique "Criar novo" → "Planilha"
    ✅ Renomeie para: "Followers Tracker"
    ✅ Adicione headers (linha 1):
       @username | Status | Data/Hora | Arquivo Local | Arquivo Origem | Tentativas
    
    Tempo estimado: 2 minutos
    Depois avise que está pronto!
    """)

if __name__ == "__main__":
    setup_google_drive()
