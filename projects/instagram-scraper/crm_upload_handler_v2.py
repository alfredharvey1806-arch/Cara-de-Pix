#!/usr/bin/env python3
"""
Handler para Upload no CRM v2 (Usando OpenClaw Browser + Sub-Agente)
Automatiza o fluxo: Screenshot → CRM Analysis → Supabase Update
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

CRM_URL = os.environ.get("CRM_URL", "https://pix-prospector-bot.lovable.app/")
CRM_EMAIL = os.environ.get("CRM_EMAIL")
CRM_PASSWORD = os.environ.get("CRM_PASSWORD")

SCREENSHOTS_DIR = os.path.expanduser(os.environ.get("SCREENSHOTS_DIR", "~/Documents/Seguidores"))

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise SystemExit("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY environment variables")
if not CRM_EMAIL or not CRM_PASSWORD:
    raise SystemExit("Missing CRM_EMAIL or CRM_PASSWORD environment variables")

# ============================================================
# CLASSE HANDLER (OpenClaw Browser)
# ============================================================

class CRMUploadAutomationV2:
    def __init__(self):
        """Inicializa handler (usa OpenClaw Browser API)"""
        self.supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        self.results = {
            "total": 0,
            "uploaded": 0,
            "already_uploaded": 0,
            "errors": 0,
            "profiles": []
        }
    
    def extract_username(self, filename: str) -> str:
        """Extrai @username do nome do arquivo"""
        match = re.match(r'@(.+?)_\d{8}_\d{6}\.png', filename)
        if match:
            return match.group(1)
        return None
    
    def check_supabase(self, username: str) -> dict:
        """Checa se username existe no Supabase"""
        try:
            response = self.supabase.table("instagram_followers") \
                .select("id,status") \
                .eq("username", username) \
                .execute()
            
            if response.data and len(response.data) > 0:
                return {"exists": True, "data": response.data[0]}
            return {"exists": False}
        except Exception as e:
            print(f"   ⚠️ Erro ao checar Supabase: {e}")
            return {"exists": False}
    
    def update_supabase(self, username: str):
        """Atualiza status para 'print feito' após upload bem-sucedido"""
        try:
            response = self.supabase.table("instagram_followers").update({
                "status": "print feito"
            }).eq("username", username).execute()
            
            if response.data:
                print(f"   ✅ Supabase: status → print feito")
                return True
            return False
        except Exception as e:
            print(f"   ⚠️ Erro ao atualizar Supabase: {e}")
            return False
    
    def process_batch(self, usernames_filter=None):
        """
        Processa batch de screenshots
        
        Este método gera instruções pra o sub-agente
        que fará o upload usando o browser do OpenClaw
        
        Args:
            usernames_filter: Lista de usernames específicos (None = todos)
        """
        print("=" * 60)
        print("🚀 PREPARANDO BATCH: Screenshots → CRM → Supabase")
        print("=" * 60)
        
        # Lista screenshots
        screenshots = sorted([
            f for f in os.listdir(SCREENSHOTS_DIR) 
            if f.endswith(".png")
        ])
        
        if not screenshots:
            print("⚠️ Nenhum screenshot encontrado")
            return False
        
        print(f"\n📸 {len(screenshots)} screenshots encontrados\n")
        
        # Coleta perfis pra processar
        profiles_to_upload = []
        
        for filename in screenshots:
            username = self.extract_username(filename)
            if not username:
                continue
            
            # Filtra se necessário
            if usernames_filter and username not in usernames_filter:
                continue
            
            file_path = os.path.join(SCREENSHOTS_DIR, filename)
            
            # Checa Supabase
            check = self.check_supabase(username)
            
            if check["exists"] and check["data"]["status"] == "print feito":
                print(f"⏭️ @{username} - Já foi analisado")
                self.results["already_uploaded"] += 1
            else:
                print(f"📋 @{username} - Pronto pra upload")
                profiles_to_upload.append({
                    "username": username,
                    "file": filename,
                    "file_path": file_path
                })
                self.results["uploaded"] += 1
            
            self.results["profiles"].append(username)
            self.results["total"] += 1
        
        # Gera instruções pra sub-agente
        self._generate_subagent_instructions(profiles_to_upload)
        
        return profiles_to_upload
    
    def _generate_subagent_instructions(self, profiles):
        """Gera instruções pra sub-agente"""
        print("\n" + "=" * 60)
        print("📋 INSTRUÇÕES PARA SUB-AGENTE")
        print("=" * 60)
        
        instruction = """
        Usar o OpenClaw Browser (profile 'openclaw' já iniciado) para:
        
        1. Navegarar para: https://pix-prospector-bot.lovable.app/
        2. Fazer login com:
           Email: alfredharvey1806@gmail.com
           Senha: Sucesso$$2026$$
        
        3. Para cada perfil abaixo:
           a. Clicar em "Nova Análise"
           b. Fazer upload do screenshot (drag & drop ou file input)
           c. Digitar @usuario no campo
           d. Clicar em "Analisar"
           e. Aguardar conclusão
           f. Confirmar sucesso
        
        Perfis a processar:
        """
        
        for profile in profiles:
            instruction += f"\n        - @{profile['username']} → {profile['file']}"
        
        print(instruction)
        
        # Salva instruções
        log_path = "projects/instagram-scraper/crm_upload_instructions.txt"
        with open(log_path, 'w') as f:
            f.write(instruction)
        
        print(f"\n✅ Instruções salvas em: {log_path}")
    
    def manual_upload_instructions(self):
        """Imprime instruções pra upload manual"""
        print("""
        🎯 UPLOAD MANUAL (Passo a Passo)
        
        1. Abra: https://pix-prospector-bot.lovable.app/
        2. Faça login:
           Email: alfredharvey1806@gmail.com
           Senha: Sucesso$$2026$$
        
        3. Clique em "Nova Análise"
        
        4. Para cada @usuario:
           a. Clique em "Choose File"
           b. Selecione o screenshot de ~/Documents/Seguidores/@usuario_*.png
           c. Preencha o campo "@usuario" com @username
           d. Clique em "Analisar"
           e. Aguarde a análise completar
           f. Confirme sucesso
        
        5. Após cada análise bem-sucedida:
           UPDATE instagram_followers SET status = 'print feito' WHERE username = @username
        """)

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    automation = CRMUploadAutomationV2()
    
    # Processa batch completo
    profiles = automation.process_batch()
    
    # Ou testa com 3 perfis
    # profiles = automation.process_batch(usernames_filter=["ju_bettiol", "_manuteles", "beredela"])
    
    print("\n" + "=" * 60)
    print("📊 PRÓXIMOS PASSOS")
    print("=" * 60)
    print(f"✅ {automation.results['uploaded']} perfis prontos pra upload")
    print(f"⏭️ {automation.results['already_uploaded']} já processados")
    print(f"\nChame o sub-agente pra fazer upload automático")
