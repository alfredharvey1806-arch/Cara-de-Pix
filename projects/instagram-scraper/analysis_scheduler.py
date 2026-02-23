#!/usr/bin/env python3
"""
Scheduler automático para rodar análise GPT periodicamente.
Processa registros com analysis_status="pending" ou "error" (<3 tentativas).
"""

import os
import sys
import time
import logging
from datetime import datetime
import subprocess

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.expanduser("~/Documents/Seguidores/.metadata/analysis_scheduler.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Config
ANALYSIS_SCRIPT = os.path.join(os.path.dirname(__file__), "analyze_gpt.py")
BATCH_SIZE = 5  # Processa 5 de cada vez
INTERVAL_SECONDS = 300  # A cada 5 minutos

def run_analysis():
    """Executa uma rodada de análise GPT."""
    try:
        logger.info(f"🚀 Iniciando análise (batch_size={BATCH_SIZE})")
        
        env = os.environ.copy()
        env["GPT_BATCH"] = str(BATCH_SIZE)
        
        result = subprocess.run(
            [sys.executable, ANALYSIS_SCRIPT],
            env=env,
            capture_output=True,
            text=True,
            timeout=600
        )
        
        if result.returncode == 0:
            logger.info("✅ Análise concluída com sucesso")
            if result.stdout:
                logger.info(result.stdout)
            return True
        else:
            logger.error(f"❌ Erro na análise: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error(f"⏱️ Timeout ao rodar análise (>600s)")
        return False
    except Exception as e:
        logger.error(f"❌ Erro geral: {e}")
        return False

def loop_scheduler(interval=INTERVAL_SECONDS):
    """Loop contínuo de execução."""
    logger.info(f"📋 Scheduler iniciado – rodada a cada {interval}s")
    
    cycle_count = 0
    while True:
        cycle_count += 1
        try:
            logger.info(f"\n{'='*60}")
            logger.info(f"CICLO #{cycle_count} – {datetime.now().isoformat()}")
            logger.info(f"{'='*60}")
            
            success = run_analysis()
            
            if success:
                logger.info(f"⏳ Próximo ciclo em {interval}s...")
            else:
                logger.warning(f"⚠️ Ciclo #{ cycle_count} falhou. Retry em {interval}s...")
            
            time.sleep(interval)
            
        except KeyboardInterrupt:
            logger.info("\n🛑 Scheduler parado (Ctrl+C)")
            break
        except Exception as e:
            logger.error(f"❌ Erro no loop: {e}")
            time.sleep(interval)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Scheduler para análise GPT automática")
    parser.add_argument(
        "--interval",
        type=int,
        default=INTERVAL_SECONDS,
        help=f"Intervalo em segundos (default: {INTERVAL_SECONDS})"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=BATCH_SIZE,
        help=f"Batch size (default: {BATCH_SIZE})"
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Rodar apenas uma vez (no lugar de loop)"
    )
    
    args = parser.parse_args()
    
    # Validar env vars
    if not os.environ.get("SUPABASE_URL") or not os.environ.get("SUPABASE_SERVICE_ROLE_KEY"):
        logger.error("❌ Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY")
        sys.exit(1)
    
    if not os.environ.get("OPENAI_API_KEY"):
        logger.error("❌ Missing OPENAI_API_KEY")
        sys.exit(1)
    
    if args.once:
        logger.info("🎯 Modo: execução única")
        success = run_analysis()
        sys.exit(0 if success else 1)
    else:
        logger.info("🔄 Modo: loop periódico")
        loop_scheduler(interval=args.interval)
