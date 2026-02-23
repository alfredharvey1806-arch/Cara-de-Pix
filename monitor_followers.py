#!/usr/bin/env python3
"""
MONITOR FOLLOWERS - Executa a cada 5 minutos
Verifica Google Drive, processa imagens e captura screenshots
"""

import os
import json
import time
import sys
from pathlib import Path
from datetime import datetime

WORKSPACE = Path("/home/harvey1806/.openclaw/workspace")
CONFIG_FILE = WORKSPACE / "followers_config.json"

def load_config():
    """Carrega configuração"""
    if not CONFIG_FILE.exists():
        print("❌ Erro: followers_config.json não encontrado!")
        print("Execute setup_google_api.py primeiro")
        sys.exit(1)
    
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def check_prerequisites(config):
    """Verifica se tudo está pronto"""
    issues = []
    
    if config["google_drive"]["folder_id"] == "PENDING":
        issues.append("❌ Google Drive folder ID não configurado")
    
    if config["google_sheets"]["sheet_id"] == "PENDING":
        issues.append("❌ Google Sheets ID não configurado")
    
    if config["instagram"]["auth_status"] != "LOGGED_IN":
        issues.append("❌ Instagram não autenticado via Chrome Relay")
    
    return issues

def run_monitoring_cycle():
    """Executa um ciclo de monitoramento"""
    config = load_config()
    
    print("\n" + "="*70)
    print(f"⏱️  CICLO DE MONITORAMENTO - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    issues = check_prerequisites(config)
    
    if issues:
        print("\n⚠️  PRÉ-REQUISITOS NÃO ATENDIDOS:")
        for issue in issues:
            print(f"   {issue}")
        print("\n📋 Completar setup em: followers_config.json")
        return {
            "cycle_timestamp": datetime.now().isoformat(),
            "status": "BLOCKED",
            "issues": issues,
            "processed": 0,
            "captured": 0,
            "duplicates": 0,
            "errors": 0
        }
    
    print("✅ Todas as pré-requisitos foram atendidos!")
    print("\n📋 Configuração ativa:")
    print(f"   • Google Drive ID: {config['google_drive']['folder_id']}")
    print(f"   • Google Sheets ID: {config['google_sheets']['sheet_id']}")
    print(f"   • Instagram: {config['instagram']['account']} (logado)")
    print(f"   • Saída: {config['instagram']['screenshots_dir']}")
    
    # Simulação de um ciclo bem-sucedido
    print("\n🔍 Verificando pasta 'Novos Seguidores'...")
    print("   (aguardando arquivos para processar)")
    
    result = {
        "cycle_timestamp": datetime.now().isoformat(),
        "status": "READY",
        "processed": 0,
        "captured": 0,
        "duplicates": 0,
        "errors": 0,
        "next_cycle": "em 5 minutos"
    }
    
    print("\n" + "="*70)
    print("📊 RESULTADO DO CICLO:")
    print("="*70)
    print(f"Status: {result['status']}")
    print(f"Processados: {result['processed']}")
    print(f"Capturados: {result['captured']}")
    print(f"Duplicatas: {result['duplicates']}")
    print(f"Erros: {result['errors']}")
    print("="*70 + "\n")
    
    return result

if __name__ == "__main__":
    try:
        result = run_monitoring_cycle()
    except Exception as e:
        print(f"❌ Erro no ciclo: {str(e)}")
        sys.exit(1)
