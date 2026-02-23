#!/usr/bin/env python3
"""
Automação Completa: Screenshots → Supabase → CRM
Sub-agente handler que executa o fluxo de análise de seguidores
"""

import os
import re
from datetime import datetime
from pathlib import Path
from supabase import create_client, Client

# ============================================================
# CONFIGURAÇÃO
# ============================================================

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
SCREENSHOTS_DIR = os.path.expanduser(os.environ.get("SCREENSHOTS_DIR", "~/Documents/Seguidores"))
CRM_URL = os.environ.get("CRM_URL", "https://pix-prospector-bot.lovable.app/")
BASE_DIR = Path(__file__).resolve().parent
ANALYSIS_LOG = os.environ.get("ANALYSIS_LOG_PATH", str(BASE_DIR / "analysis_log.md"))

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise SystemExit("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY environment variables")

# ============================================================
# CLASSE HANDLER
# ============================================================

class InstagramCRMAutomation:
    def __init__(self):
        """Inicializa handler"""
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        self.screenshots = []
        self.results = {
            "total_screenshots": 0,
            "already_analyzed": 0,
            "newly_analyzed": 0,
            "errors": 0,
            "profiles": []
        }
    
    def list_screenshots(self):
        """Lista todos os screenshots capturados"""
        if not os.path.exists(SCREENSHOTS_DIR):
            print(f"❌ Pasta não encontrada: {SCREENSHOTS_DIR}")
            return []
        
        screenshots = [f for f in os.listdir(SCREENSHOTS_DIR) if f.endswith(".png")]
        self.screenshots = sorted(screenshots)
        print(f"📸 {len(self.screenshots)} screenshots encontrados\n")
        return self.screenshots
    
    def extract_username(self, filename: str) -> str:
        """Extrai @username do nome do arquivo"""
        # Formato: @username_YYYYMMDD_HHMMSS.png
        match = re.match(r'@(.+?)_\d{8}_\d{6}\.png', filename)
        if match:
            return match.group(1)
        return None
    
    def check_supabase(self, username: str) -> dict:
        """Checa status do username no Supabase"""
        try:
            response = self.supabase.table("instagram_followers") \
                .select("id,status,file_path") \
                .eq("username", username) \
                .execute()
            
            if response.data and len(response.data) > 0:
                return {"exists": True, "data": response.data[0]}
            return {"exists": False}
        except Exception as e:
            print(f"   ⚠️ Erro ao checar Supabase: {e}")
            return {"exists": False, "error": str(e)}
    
    def insert_supabase(self, username: str, file_path: str):
        """Insere novo username no Supabase com status 'esperando'"""
        try:
            response = self.supabase.table("instagram_followers").insert({
                "username": username,
                "status": "esperando",
                "file_path": file_path,
                "added_at": datetime.now().isoformat()
            }).execute()
            
            if response.data:
                print(f"   ✅ Novo registro criado no Supabase (status: esperando)")
                return True
            return False
        except Exception as e:
            print(f"   ❌ Erro ao inserir: {e}")
            return False
    
    def update_supabase_status(self, username: str, status: str):
        """Atualiza status no Supabase (aceita: 'esperando' ou 'print feito')"""
        valid_statuses = ["esperando", "print feito"]
        if status not in valid_statuses:
            print(f"   ⚠️ Status inválido: '{status}'. Use: {valid_statuses}")
            return False
        
        try:
            response = self.supabase.table("instagram_followers").update({
                "status": status
            }).eq("username", username).execute()
            
            if response.data:
                print(f"   ✅ Status atualizado: {status}")
                return True
            else:
                print(f"   ⚠️ Nenhum registro atualizado para @{username}")
                return False
        except Exception as e:
            print(f"   ❌ Erro ao atualizar: {e}")
            return False
    
    def process_screenshot(self, filename: str, file_path: str):
        """Processa um screenshot individual"""
        username = self.extract_username(filename)
        if not username:
            print(f"❌ {filename} - Não conseguiu extrair username")
            self.results["errors"] += 1
            return False
        
        print(f"\n📋 Processando @{username}...")
        
        # Checa se já existe no Supabase
        check = self.check_supabase(username)
        
        if check["exists"]:
            status = check["data"]["status"]
            print(f"   ℹ️  Já existe no Supabase (status: {status})")
            
            if status == "print feito":
                print(f"   ✅ Print já foi analisado")
                self.results["already_analyzed"] += 1
            else:
                print(f"   ⏳ Pendente de upload no CRM")
                self.results["newly_analyzed"] += 1
        else:
            # Novo username
            print(f"   🆕 Novo usuário - Criando registro...")
            if self.insert_supabase(username, file_path):
                self.results["newly_analyzed"] += 1
            else:
                self.results["errors"] += 1
                return False
        
        # Registra no resultado
        self.results["profiles"].append({
            "username": username,
            "file": filename,
            "status": check["data"]["status"] if check["exists"] else "esperando"
        })
        
        return True
    
    def run(self):
        """Executa o fluxo completo"""
        print("=" * 60)
        print("🤖 AUTOMAÇÃO: INSTAGRAM → SUPABASE → CRM")
        print("=" * 60)
        
        # 1. Listar screenshots
        print("\n📸 PASSO 1: Listando screenshots...")
        screenshots = self.list_screenshots()
        
        if not screenshots:
            print("⚠️ Nenhum screenshot encontrado!")
            return False
        
        self.results["total_screenshots"] = len(screenshots)
        
        # 2. Processar cada screenshot
        print("\n📋 PASSO 2: Processando screenshots...")
        for filename in screenshots:
            file_path = os.path.join(SCREENSHOTS_DIR, filename)
            self.process_screenshot(filename, file_path)
        
        # 3. Gerar relatório
        self._generate_report()
        
        return True
    
    def _generate_report(self):
        """Gera relatório do processamento"""
        print("\n" + "=" * 60)
        print("📊 RESUMO DO PROCESSAMENTO")
        print("=" * 60)
        print(f"📸 Total de screenshots: {self.results['total_screenshots']}")
        print(f"✅ Já analisados: {self.results['already_analyzed']}")
        print(f"🆕 Novos/Pendentes: {self.results['newly_analyzed']}")
        print(f"❌ Erros: {self.results['errors']}")
        
        # Salva log
        log_content = self._format_log()
        self._save_log(log_content)
        
        print(f"\n📄 Log salvo em: {ANALYSIS_LOG}")
    
    def _format_log(self) -> str:
        """Formata o log em Markdown"""
        log = f"""# 📊 Log de Análise - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Resumo
- **Total de screenshots:** {self.results['total_screenshots']}
- **Já analisados:** {self.results['already_analyzed']}
- **Novos/Pendentes:** {self.results['newly_analyzed']}
- **Erros:** {self.results['errors']}

## Detalhes dos Perfis

"""
        for profile in self.results['profiles']:
            status_emoji = "✅" if profile['status'] == "print feito" else "⏳"
            log += f"### {status_emoji} @{profile['username']}\n"
            log += f"- Arquivo: `{profile['file']}`\n"
            log += f"- Status Supabase: `{profile['status']}`\n\n"
        
        return log
    
    def _save_log(self, content: str):
        """Salva log em arquivo"""
        try:
            # Append ao log existente
            if os.path.exists(ANALYSIS_LOG):
                with open(ANALYSIS_LOG, 'a', encoding='utf-8') as f:
                    f.write("\n" + "=" * 60 + "\n")
                    f.write(content)
            else:
                # Cria novo log
                os.makedirs(os.path.dirname(ANALYSIS_LOG), exist_ok=True)
                with open(ANALYSIS_LOG, 'w', encoding='utf-8') as f:
                    f.write(content)
        except Exception as e:
            print(f"⚠️ Erro ao salvar log: {e}")

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    automation = InstagramCRMAutomation()
    automation.run()
