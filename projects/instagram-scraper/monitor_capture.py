#!/usr/bin/env python3
"""
Monitor simples para captura robusta.
Mostra status em tempo real: sucesso, erros, retry queue.
"""

import os
import sys
from supabase import create_client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise SystemExit("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY environment variables")

def clear_screen():
    os.system("clear" if os.name != "nt" else "cls")

def monitor_once():
    """Mostra status atual do sistema."""
    try:
        client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        
        # Buscar estatísticas
        all_data = client.table("instagram_followers").select("*").execute().data or []
        
        stats = {
            "esperando": [],
            "processando": [],
            "print feito": [],
            "erro": []
        }
        
        for row in all_data:
            status = row.get("status", "unknown")
            if status in stats:
                stats[status].append(row)
        
        # Montar dashboard
        clear_screen()
        print("=" * 70)
        print("📊 MONITOR DE CAPTURA ROBUSTA")
        print("=" * 70)
        print()
        
        # Summary
        total = len(all_data)
        print(f"Total de perfis: {total}")
        print()
        
        # Status breakdown
        print("STATUS ATUAL:")
        print(f"  ✅ Prontos (print feito): {len(stats['print feito'])} perfis")
        print(f"  ⏳ Aguardando (esperando): {len(stats['esperando'])} perfis")
        print(f"  🔄 Processando: {len(stats['processando'])} perfis")
        print(f"  ❌ Erros: {len(stats['erro'])} perfis")
        print()
        
        # Retry queue
        retry_queue = [p for p in stats['esperando'] if p.get('capture_retry_count', 0) > 0]
        if retry_queue:
            print(f"🔁 Fila de Retry ({len(retry_queue)}):")
            for p in retry_queue[:5]:  # Top 5
                retry_count = p.get('capture_retry_count', 0)
                print(f"   • @{p['username']:30} (tentativa {retry_count}/3)")
            if len(retry_queue) > 5:
                print(f"   ... e mais {len(retry_queue) - 5}")
            print()
        
        # Erros recentes
        if stats['erro']:
            print(f"❌ Permanentemente com Erro ({len(stats['erro'])}):")
            for p in stats['erro'][:5]:
                error = p.get('capture_error', 'unknown')[:40]
                print(f"   • @{p['username']:30} - {error}...")
            if len(stats['erro']) > 5:
                print(f"   ... e mais {len(stats['erro']) - 5}")
            print()
        
        # Taxa de sucesso
        success_rate = (len(stats['print feito']) / total * 100) if total > 0 else 0
        print(f"📈 Taxa de Sucesso: {success_rate:.1f}% ({len(stats['print feito'])}/{total})")
        print()
        
        print("=" * 70)
        print("💡 Próximo: python3 capture_scheduler.py --mode once")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        sys.exit(1)

def monitor_loop(interval_seconds=30):
    """Loop contínuo de monitoramento."""
    import time
    
    try:
        while True:
            monitor_once()
            print(f"\n⏳ Próxima atualização em {interval_seconds}s... (Ctrl+C para sair)")
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("\n\n🛑 Monitor parado")
        sys.exit(0)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Monitor de captura robusta")
    parser.add_argument(
        "--loop",
        action="store_true",
        help="Rodar em loop contínuo"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=30,
        help="Intervalo de atualização em segundos (default: 30)"
    )
    
    args = parser.parse_args()
    
    if args.loop:
        monitor_loop(interval_seconds=args.interval)
    else:
        monitor_once()
