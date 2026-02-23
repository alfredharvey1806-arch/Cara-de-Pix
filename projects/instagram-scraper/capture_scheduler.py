#!/usr/bin/env python3
"""
Scheduler para rodar captura periódica via OpenClaw cron ou script direto.
Use: python3 capture_scheduler.py --interval 5 --batch-size 5
"""

import argparse
import logging
import json
from datetime import datetime
from robust_capture import run_capture_cycle

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

def create_cron_job(interval_minutes: int = 5, batch_size: int = 5):
    """
    Cria job cron via OpenClaw Gateway.
    Requer: openclaw CLI instalado e gateway rodando.
    """
    import subprocess
    
    job_config = {
        "name": "instagram-capture-robust",
        "schedule": {
            "kind": "every",
            "everyMs": interval_minutes * 60 * 1000
        },
        "payload": {
            "kind": "systemEvent",
            "text": f"Rodar captura robusta: batch_size={batch_size}"
        },
        "sessionTarget": "main",
        "enabled": True
    }
    
    logger.info(f"📋 Criando cron job com intervalo {interval_minutes}min...")
    logger.info(json.dumps(job_config, indent=2))
    
    # Usar OpenClaw CLI pra criar o job
    try:
        result = subprocess.run(
            ["openclaw", "cron", "add", json.dumps(job_config)],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            logger.info("✅ Cron job criado com sucesso")
            return True
        else:
            logger.error(f"❌ Erro ao criar cron: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"❌ Erro ao chamar openclaw CLI: {e}")
        return False

def run_interval_loop(interval_minutes: int = 5, batch_size: int = 5, max_cycles: int = None):
    """
    Loop contínuo que roda captura a cada X minutos.
    Use para desenvolvimento/debug (em produção, prefira cron).
    """
    import time
    
    logger.info(f"🔄 Iniciando loop periódico: {interval_minutes}min, batch_size={batch_size}")
    
    cycle_count = 0
    while True:
        cycle_count += 1
        if max_cycles and cycle_count > max_cycles:
            logger.info(f"🛑 Atingido limite de {max_cycles} ciclos, parando")
            break
        
        logger.info(f"\n{'='*60}")
        logger.info(f"CICLO #{cycle_count} - {datetime.now().isoformat()}")
        logger.info(f"{'='*60}")
        
        try:
            run_capture_cycle(batch_size=batch_size)
        except Exception as e:
            logger.error(f"❌ Erro no ciclo #{cycle_count}: {e}")
        
        logger.info(f"⏳ Próximo ciclo em {interval_minutes} minutos...")
        time.sleep(interval_minutes * 60)

def main():
    parser = argparse.ArgumentParser(
        description="Scheduler robusto para captura de Instagram"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help="Intervalo em minutos entre ciclos (default: 5)"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=5,
        help="Número de perfis por ciclo (default: 5)"
    )
    parser.add_argument(
        "--mode",
        choices=["loop", "cron", "once"],
        default="once",
        help="Modo de execução (default: once)"
    )
    parser.add_argument(
        "--max-cycles",
        type=int,
        default=None,
        help="Máximo de ciclos (só para mode=loop)"
    )
    
    args = parser.parse_args()
    
    if args.mode == "once":
        logger.info("🚀 Modo: Execução única")
        run_capture_cycle(batch_size=args.batch_size)
    
    elif args.mode == "loop":
        logger.info("🚀 Modo: Loop periódico (desenvolvimento)")
        run_interval_loop(
            interval_minutes=args.interval,
            batch_size=args.batch_size,
            max_cycles=args.max_cycles
        )
    
    elif args.mode == "cron":
        logger.info("🚀 Modo: Cron (produção)")
        create_cron_job(
            interval_minutes=args.interval,
            batch_size=args.batch_size
        )

if __name__ == "__main__":
    main()
