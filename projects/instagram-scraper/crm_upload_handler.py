#!/usr/bin/env python3
"""
Handler para Upload no CRM (Pix Prospector)
Automatiza o fluxo: Screenshot → CRM Analysis → Supabase Update
"""

import os
import re
from datetime import datetime
from pathlib import Path
from supabase import create_client, Client
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

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
# CLASSE HANDLER
# ============================================================

class CRMUploadAutomation:
    def __init__(self, headless=False):
        """Inicializa handler com Selenium"""
        self.supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        self.driver = None
        self.headless = headless
        self.results = {
            "total": 0,
            "uploaded": 0,
            "already_uploaded": 0,
            "errors": 0,
            "profiles": []
        }
    
    def setup_driver(self):
        """Configura Selenium WebDriver"""
        options = Options()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        try:
            self.driver = webdriver.Chrome(options=options)
            print("✅ WebDriver inicializado")
            return True
        except Exception as e:
            print(f"❌ Erro ao inicializar WebDriver: {e}")
            return False
    
    def login_crm(self):
        """Faz login no CRM"""
        try:
            self.driver.get(CRM_URL)
            wait = WebDriverWait(self.driver, 10)
            
            # Aguarda página carregar
            email_input = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, "//input[@placeholder='seu@email.com']"))
            )
            if not email_input:
                print("⚠️ Campo de email não encontrado")
                return False
            
            # Preenche email
            email_input[0].send_keys(CRM_EMAIL)
            
            # Preenche senha
            password_input = self.driver.find_elements(By.XPATH, "//input[@placeholder='••••••']")[0]
            password_input.send_keys(CRM_PASSWORD)
            
            # Clica em Entrar
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Entrar')]")
            login_button.click()
            
            # Aguarda redirecionamento
            wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Nova Análise')]")))
            print("✅ Login realizado com sucesso")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao fazer login: {e}")
            return False
    
    def upload_screenshot(self, file_path: str, username: str) -> bool:
        """
        Faz upload de screenshot e análise no CRM
        
        Args:
            file_path: Caminho completo do arquivo PNG
            username: @username para análise
        
        Returns:
            True se upload bem-sucedido, False caso contrário
        """
        try:
            wait = WebDriverWait(self.driver, 10)
            
            # Clica em "Nova Análise"
            nova_analise = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Nova Análise')]")
            nova_analise.click()
            
            # Aguarda página carregar
            wait.until(EC.url_changes(self.driver.current_url))
            wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='@usuario ou usuario']")))
            
            # Encontra input de arquivo e envia screenshot
            file_input = self.driver.find_element(By.XPATH, "//input[@type='file']")
            file_input.send_keys(os.path.abspath(file_path))
            
            # Aguarda upload processar
            import time
            time.sleep(2)
            
            # Preenche campo de @usuario
            username_input = self.driver.find_element(By.XPATH, "//input[@placeholder='@usuario ou usuario']")
            username_input.clear()
            username_input.send_keys(f"@{username}")
            
            # Clica em "Analisar"
            analisar_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Analisar')]"))
            )
            analisar_button.click()
            
            # Aguarda conclusão da análise
            time.sleep(3)
            wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Nova Análise')]")))
            
            print(f"   ✅ @{username} - Upload e análise concluídos")
            return True
            
        except Exception as e:
            print(f"   ❌ @{username} - Erro no upload: {str(e)[:80]}")
            return False
    
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
                print(f"   ✅ Status Supabase atualizado: print feito")
                return True
            return False
        except Exception as e:
            print(f"   ⚠️ Erro ao atualizar Supabase: {e}")
            return False
    
    def process_batch(self, usernames_filter=None):
        """
        Processa batch de screenshots
        
        Args:
            usernames_filter: Lista de usernames específicos (None = todos)
        """
        print("=" * 60)
        print("🚀 UPLOAD NO CRM: Screenshots → Análise → Supabase")
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
        
        # Faz login
        if not self.login_crm():
            return False
        
        # Processa cada screenshot
        for filename in screenshots:
            username = self.extract_username(filename)
            if not username:
                continue
            
            # Filtra se necessário
            if usernames_filter and username not in usernames_filter:
                continue
            
            file_path = os.path.join(SCREENSHOTS_DIR, filename)
            
            print(f"📋 @{username}...")
            
            # Checa Supabase
            check = self.check_supabase(username)
            
            if check["exists"] and check["data"]["status"] == "print feito":
                print(f"   ⏭️ Já foi analisado")
                self.results["already_uploaded"] += 1
            else:
                # Faz upload
                if self.upload_screenshot(file_path, username):
                    self.update_supabase(username)
                    self.results["uploaded"] += 1
                else:
                    self.results["errors"] += 1
            
            self.results["profiles"].append(username)
            self.results["total"] += 1
        
        # Gera relatório
        self._generate_report()
        
        return True
    
    def _generate_report(self):
        """Gera relatório final"""
        print("\n" + "=" * 60)
        print("📊 RESUMO DO UPLOAD")
        print("=" * 60)
        print(f"📸 Total processado: {self.results['total']}")
        print(f"✅ Uploads bem-sucedidos: {self.results['uploaded']}")
        print(f"⏭️ Já analisados: {self.results['already_uploaded']}")
        print(f"❌ Erros: {self.results['errors']}")
    
    def cleanup(self):
        """Fecha WebDriver"""
        if self.driver:
            self.driver.quit()
            print("\n✅ WebDriver encerrado")

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    automation = CRMUploadAutomation(headless=False)
    
    try:
        if automation.setup_driver():
            # Processa todos os screenshots
            automation.process_batch()
            # Ou processa apenas alguns:
            # automation.process_batch(usernames_filter=["ju_bettiol", "_manuteles", "beredela"])
    finally:
        automation.cleanup()
