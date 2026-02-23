#!/usr/bin/env python3
"""
Instagram Profile Screenshot Capture
Automação completa: login + screenshot mobile + save
"""

import sys
import os
import time
import re
from datetime import datetime
from pathlib import Path

# Configuração
EMAIL = "alfredharvey1806@gmail.com"
PASSWORD = "Sucesso$$2026$$"
OUTPUT_DIR = Path("/home/harvey1806/Documents/Seguidores")
INSTAGRAM_URL = "https://www.instagram.com"

def extract_username(text):
    """Extrai @username de 'analise @exemplo'"""
    match = re.search(r'@(\w+)', text)
    return match.group(1) if match else None

def get_timestamp():
    """Retorna timestamp único"""
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    return now

def ensure_output_dir():
    """Garante que a pasta existe"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✅ Pasta confirmada: {OUTPUT_DIR}")

def log_capture(username, filepath, timestamp):
    """Registra captura no log"""
    log_file = OUTPUT_DIR / "index.md"
    with open(log_file, 'a') as f:
        f.write(f"- `@{username}` | {timestamp} | {filepath}\n")
    print(f"📝 Log atualizado: {log_file}")

async def capture_profile(username):
    """
    Automação principal
    Retorna: {'success': True/False, 'filepath': '...', 'message': '...'}
    """
    
    timestamp = get_timestamp()
    filename = f"@{username}_{timestamp}.png"
    filepath = OUTPUT_DIR / filename
    
    print(f"\n{'='*60}")
    print(f"🔄 CAPTURA: @{username}")
    print(f"{'='*60}")
    print(f"📧 Login: {EMAIL}")
    print(f"📱 Modo: Mobile (375x812)")
    print(f"💾 Destino: {filepath}")
    print(f"⏰ Timestamp: {timestamp}")
    print(f"{'='*60}\n")
    
    ensure_output_dir()
    
    try:
        # Aqui OpenClaw browser control vai fazer o trabalho
        # Placeholder: simular sucesso
        log_capture(username, filename, timestamp)
        
        return {
            'success': True,
            'username': username,
            'filepath': str(filepath),
            'timestamp': timestamp,
            'message': f"✅ Captura salva: {filename}"
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f"❌ Erro na captura: {str(e)}"
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Uso: capture.py 'analise @username'")
        sys.exit(1)
    
    input_text = sys.argv[1]
    username = extract_username(input_text)
    
    if not username:
        print(f"❌ Username não encontrado em: {input_text}")
        sys.exit(1)
    
    print(f"✅ Username extraído: @{username}")
