#!/usr/bin/env python3
"""
Robust Instagram Screenshot Capture com Retry, Health Check e Rate Limiting.
Não quebra a fila se um perfil falhar.
"""

import os
import time
import random
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from dataclasses import dataclass

from supabase import create_client, Client

# ============= SETUP LOGGING =============
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.expanduser("~/Documents/Seguidores/.metadata/capture.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============= CONSTANTS =============
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
SCREENSHOTS_DIR = os.path.expanduser(os.environ.get("SCREENSHOTS_DIR", "~/Documents/Seguidores"))

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise SystemExit("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY environment variables")

@dataclass
class CaptureResult:
    username: str
    success: bool
    file_path: Optional[str] = None
    error: Optional[str] = None
    retry_count: int = 0

class RateLimiter:
    """Evita rate limit do Instagram."""
    
    def __init__(self, min_delay: float = 3.0, max_delay: float = 7.0):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.last_request = 0.0
    
    def wait(self):
        """Aguarda antes da próxima captura."""
        elapsed = time.time() - self.last_request
        if elapsed < self.min_delay:
            sleep_time = random.uniform(self.min_delay, self.max_delay)
            logger.info(f"⏳ Rate limiting: aguardando {sleep_time:.1f}s")
            time.sleep(sleep_time)
        self.last_request = time.time()

class HealthCheck:
    """Monitora saúde do sistema."""
    
    def __init__(self, client: Client):
        self.client = client
    
    def check_supabase(self) -> bool:
        """Testa conexão Supabase."""
        try:
            self.client.table("instagram_followers").select("id").limit(1).execute()
            logger.info("✅ Supabase OK")
            return True
        except Exception as e:
            logger.error(f"❌ Supabase falhou: {e}")
            return False
    
    def check_browser_process(self) -> bool:
        """Verifica se Chrome está rodando."""
        import subprocess
        result = subprocess.run(["pgrep", "-f", "google-chrome"], capture_output=True)
        if result.returncode == 0:
            logger.info("✅ Chrome OK")
            return True
        logger.error("❌ Chrome não está rodando")
        return False
    
    def run_all(self) -> bool:
        """Roda todos os checks."""
        checks = [
            self.check_supabase(),
            self.check_browser_process()
        ]
        if all(checks):
            logger.info("🟢 Sistema saudável")
            return True
        logger.warning("🟡 Sistema com problemas")
        return False

class CaptureManager:
    """Orquestra captura com retry e isolamento de erros."""
    
    def __init__(self, headless: bool = False):
        self.client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        self.rate_limiter = RateLimiter(min_delay=3.0, max_delay=7.0)
        self.health = HealthCheck(self.client)
        self.headless = headless
        self.max_retries = 3
        self.browser = None
    
    def fetch_pending(self, batch_size: int = 5) -> List[Dict]:
        """Busca perfis pendentes de captura."""
        try:
            query = (
                self.client.table("instagram_followers")
                .select("id, username, status, capture_retry_count")
                .eq("status", "esperando")
                .order("id")
                .limit(batch_size)
            )
            data = query.execute().data or []
            logger.info(f"📋 {len(data)} perfis pendentes")
            return data
        except Exception as e:
            logger.error(f"Erro ao buscar pendentes: {e}")
            return []
    
    def mark_in_progress(self, profile_id: int, username: str):
        """Marca perfil como sendo processado."""
        try:
            self.client.table("instagram_followers").update({
                "status": "processando",
                "capture_started_at": datetime.utcnow().isoformat()
            }).eq("id", profile_id).execute()
            logger.info(f"🔄 @{username} marcado como 'processando'")
        except Exception as e:
            logger.error(f"Erro ao marcar processando: {e}")
    
    def mark_done(self, profile_id: int, username: str, file_path: str):
        """Marca captura como concluída."""
        try:
            self.client.table("instagram_followers").update({
                "status": "print feito",
                "file_path": file_path,
                "capture_completed_at": datetime.utcnow().isoformat(),
                "capture_retry_count": 0
            }).eq("id", profile_id).execute()
            logger.info(f"✅ @{username} capturado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao marcar done: {e}")
    
    def mark_error(self, profile_id: int, username: str, error_msg: str, retry_count: int):
        """Marca erro e agenda retry."""
        try:
            next_status = "esperando" if retry_count < self.max_retries else "erro"
            next_retry = datetime.utcnow() + timedelta(minutes=10)
            
            self.client.table("instagram_followers").update({
                "status": next_status,
                "capture_retry_count": retry_count + 1,
                "capture_error": error_msg[:250],
                "capture_next_retry": next_retry.isoformat() if next_status == "esperando" else None
            }).eq("id", profile_id).execute()
            
            if next_status == "esperando":
                logger.warning(f"⚠️ @{username} falhou ({retry_count + 1}/{self.max_retries}), retry em 10min")
            else:
                logger.error(f"❌ @{username} falhou permanentemente após {self.max_retries} tentativas")
        except Exception as e:
            logger.error(f"Erro ao marcar erro: {e}")
    
    def capture_screenshot(self, username: str) -> Optional[str]:
        """
        Captura screenshot via browser (esperando que browser.py ou similar esteja rodando).
        Retorna file_path se sucesso, None se falha.
        """
        from datetime import datetime as dt
        
        try:
            # Aguarda rate limit
            self.rate_limiter.wait()
            
            # Formata filename
            now = dt.now().strftime("%Y%m%d_%H%M%S")
            file_path = os.path.join(SCREENSHOTS_DIR, f"@{username}_{now}.png")
            
            # TODO: Integrar com OpenClaw browser ou Selenium
            # Por enquanto, retorna placeholder (você implementa a captura real)
            logger.info(f"📸 Capturando @{username}...")
            
            # Simular captura (substituir com logic real)
            import subprocess
            result = subprocess.run(
                ["openclaw", "browser", "action", "screenshot", "--username", username, "--output", file_path],
                capture_output=True,
                timeout=20
            )
            
            if result.returncode == 0 and os.path.exists(file_path):
                logger.info(f"📸 Screenshot salvo: {file_path}")
                return file_path
            else:
                logger.error(f"Screenshot falhou para @{username}")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error(f"⏱️ Timeout ao capturar @{username}")
            return None
        except Exception as e:
            logger.error(f"Erro ao capturar @{username}: {e}")
            return None
    
    def process_batch(self, batch_size: int = 5) -> Dict[str, int]:
        """Processa um batch de perfis com resilência."""
        
        # Health check
        if not self.health.run_all():
            logger.error("❌ Sistema não está saudável, abortando batch")
            return {"success": 0, "failed": 0, "retried": 0}
        
        pending = self.fetch_pending(batch_size)
        if not pending:
            logger.info("✅ Nenhum perfil pendente")
            return {"success": 0, "failed": 0, "retried": 0}
        
        stats = {"success": 0, "failed": 0, "retried": 0}
        
        for profile in pending:
            profile_id = profile["id"]
            username = profile["username"]
            retry_count = profile.get("capture_retry_count", 0) or 0
            
            # Marca como processando
            self.mark_in_progress(profile_id, username)
            
            # Tenta capturar
            result = self.capture_screenshot(username)
            
            if result:
                self.mark_done(profile_id, username, result)
                stats["success"] += 1
            else:
                self.mark_error(profile_id, username, "Falha na captura", retry_count)
                if retry_count < self.max_retries:
                    stats["retried"] += 1
                else:
                    stats["failed"] += 1
        
        logger.info(f"📊 Batch resultado: {stats['success']} sucesso, {stats['failed']} falha, {stats['retried']} retry")
        return stats

def run_capture_cycle(batch_size: int = 5):
    """Executa um ciclo completo de captura."""
    logger.info("=" * 60)
    logger.info("🚀 Iniciando ciclo de captura")
    logger.info("=" * 60)
    
    manager = CaptureManager(headless=False)
    stats = manager.process_batch(batch_size=batch_size)
    
    logger.info("=" * 60)
    logger.info(f"✅ Ciclo concluído: {stats}")
    logger.info("=" * 60)

if __name__ == "__main__":
    run_capture_cycle(batch_size=5)
