#!/usr/bin/env python3
"""
AGENTE FOLLOWERS ANALYZER
Automação para captura de screenshots de novos seguidores do Instagram
"""

import os
import json
import time
import re
from datetime import datetime
from pathlib import Path

# Configurações
GOOGLE_ACCOUNT = "alfredharvey1806@gmail.com"
IG_ACCOUNT = "alfredharvey1806"
DRIVE_FOLDER = "Novos Seguidores"
SHEETS_NAME = "Followers Tracker"
OUTPUT_DIR = Path("/home/harvey1806/Documents/Seguidores")
WORKSPACE = Path("/home/harvey1806/.openclaw/workspace")

# Arquivo de controle local (substitui Google Sheets enquanto não estiver integrado)
TRACKING_FILE = WORKSPACE / "followers_tracking.json"
METADATA_FILE = OUTPUT_DIR / ".metadata" / "tracking.json"

class FollowersAnalyzer:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.metadata_file = METADATA_FILE
        self.tracking_data = self.load_tracking()
        
    def load_tracking(self):
        """Carrega dados de rastreamento existentes"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "followers_captured": [],
            "duplicates": [],
            "errors": [],
            "last_check": None
        }
    
    def save_tracking(self):
        """Salva dados de rastreamento"""
        self.metadata_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.metadata_file, 'w') as f:
            json.dump(self.tracking_data, f, indent=2, ensure_ascii=False)
    
    def extract_usernames_from_text(self, text):
        """Extrai todos os @usernames de um texto"""
        pattern = r'@(\w+\.?\w*)'
        matches = re.findall(pattern, text)
        return list(set([f"@{m}" for m in matches]))
    
    def is_duplicate(self, username):
        """Verifica se o username já foi processado"""
        captured = [u["username"] for u in self.tracking_data.get("followers_captured", [])]
        errors = [u["username"] for u in self.tracking_data.get("errors", [])]
        return username in captured or username in errors
    
    def log_captured(self, username, filepath, source, status="✅ Capturado"):
        """Registra um username capturado com sucesso"""
        entry = {
            "username": username,
            "status": status,
            "capture_date": datetime.now().isoformat(),
            "local_file": str(filepath),
            "source_file": source,
            "timestamp": int(time.time())
        }
        self.tracking_data["followers_captured"].append(entry)
        self.save_tracking()
        return entry
    
    def log_duplicate(self, username):
        """Registra um duplicate"""
        if username not in [d for d in self.tracking_data.get("duplicates", [])]:
            self.tracking_data["duplicates"].append(username)
            self.save_tracking()
    
    def log_error(self, username, error_msg):
        """Registra um erro"""
        entry = {
            "username": username,
            "status": "❌ Erro",
            "error": error_msg,
            "timestamp": datetime.now().isoformat()
        }
        self.tracking_data["errors"].append(entry)
        self.save_tracking()
    
    def print_status(self):
        """Imprime status atual"""
        captured_count = len(self.tracking_data.get("followers_captured", []))
        duplicate_count = len(self.tracking_data.get("duplicates", []))
        error_count = len(self.tracking_data.get("errors", []))
        
        print("\n" + "="*60)
        print(f"📊 STATUS FOLLOWERS ANALYZER")
        print("="*60)
        print(f"✅ Capturados: {captured_count}")
        print(f"♻️  Duplicatas: {duplicate_count}")
        print(f"❌ Erros: {error_count}")
        print(f"⏰ Última verificação: {self.tracking_data.get('last_check', 'Nunca')}")
        print("="*60 + "\n")
    
    def generate_sheets_csv(self):
        """Gera um CSV compatível com Google Sheets"""
        csv_path = WORKSPACE / "followers_tracker.csv"
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write("@username,Status,Data Captura,Arquivo Local,Arquivo Origem\n")
            
            # Adiciona capturados com sucesso
            for entry in self.tracking_data.get("followers_captured", []):
                f.write(f"{entry['username']},{entry['status']},{entry['capture_date']},{entry['local_file']},{entry.get('source_file', 'N/A')}\n")
            
            # Adiciona erros
            for entry in self.tracking_data.get("errors", []):
                f.write(f"{entry['username']},{entry['status']},{entry['timestamp']},N/A,N/A\n")
        
        print(f"📄 Google Sheets CSV criado: {csv_path}")
        return csv_path

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║           🤖 AGENTE FOLLOWERS ANALYZER                     ║
    ║   Automação de Captura de Novos Seguidores Instagram       ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    analyzer = FollowersAnalyzer()
    
    print("📋 Inicializando estrutura...")
    print(f"✓ Pasta de saída: {OUTPUT_DIR}")
    print(f"✓ Arquivo de rastreamento: {METADATA_FILE}")
    
    # Gera CSV inicial
    analyzer.generate_sheets_csv()
    analyzer.print_status()
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║              ⚙️  PRÓXIMOS PASSOS                            ║
    ╠═══════════════════════════════════════════════════════════╣
    ║ 1. O script está pronto para monitoramento                 ║
    ║ 2. Aguardando integração com Google Drive API              ║
    ║ 3. Aguardando integração com Instagram (via Chrome Relay)  ║
    ║ 4. Modo cron: verificará a cada 5 minutos                  ║
    ╚═══════════════════════════════════════════════════════════╝
    """)

if __name__ == "__main__":
    main()
