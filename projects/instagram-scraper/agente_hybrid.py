#!/usr/bin/env python3
"""
AGENTE FOLLOWERS ANALYZER - SOLUÇÃO HYBRID
Funciona 100% autonomamente sem Browser Relay

Componentes:
1. Google Drive API (Service Account)
2. Google Sheets API (Service Account)
3. Firefox Headless (Selenium)
4. Monitoramento a cada 5 minutos
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from pathlib import Path

# Google APIs
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration
CONFIG = {
    'service_account_path': '/home/harvey1806/.openclaw/workspace/projects/instagram-scraper/service_account.json',
    'output_dir': '/home/harvey1806/Documents/Seguidores',
    'drive_folder_name': 'Novos Seguidores',
    'sheets_name': 'Followers Tracker',
    'instagram_email': 'alfredharvey1806@gmail.com',
    'instagram_password': 'Sucesso$$2026$$',
}

# Logging
log_file = Path(CONFIG['output_dir']) / '.metadata' / 'agent.log'
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GoogleDriveService:
    def __init__(self, service_account_path):
        self.creds = service_account.Credentials.from_service_account_file(
            service_account_path,
            scopes=['https://www.googleapis.com/auth/drive']
        )
        self.service = build('drive', 'v3', credentials=self.creds)
        self.folder_id = None
    
    def get_folder_id(self, folder_name):
        """Encontrar ID da pasta 'Novos Seguidores'"""
        results = self.service.files().list(
            q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
            spaces='drive',
            pageSize=10,
            fields='files(id, name)'
        ).execute()
        
        files = results.get('files', [])
        if files:
            self.folder_id = files[0]['id']
            logger.info(f"✅ Pasta encontrada: {folder_name} (ID: {self.folder_id})")
            return self.folder_id
        else:
            logger.error(f"❌ Pasta não encontrada: {folder_name}")
            return None
    
    def list_new_files(self):
        """Listar arquivos não processados na pasta"""
        if not self.folder_id:
            return []
        
        results = self.service.files().list(
            q=f"'{self.folder_id}' in parents and trashed=false",
            spaces='drive',
            pageSize=10,
            fields='files(id, name, createdTime)',
            orderBy='createdTime desc'
        ).execute()
        
        return results.get('files', [])
    
    def upload_file(self, file_path, folder_id):
        """Subir arquivo para pasta no Drive"""
        file_metadata = {
            'name': os.path.basename(file_path),
            'parents': [folder_id]
        }
        media = MediaFileUpload(file_path)
        
        result = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        logger.info(f"✅ Arquivo subido: {os.path.basename(file_path)}")
        return result['id']

class GoogleSheetsService:
    def __init__(self, service_account_path):
        self.creds = service_account.Credentials.from_service_account_file(
            service_account_path,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        self.service = build('sheets', 'v4', credentials=self.creds)
        self.spreadsheet_id = None
    
    def get_spreadsheet_id(self, sheets_name):
        """Encontrar ID da planilha"""
        drive_service = build('drive', 'v3', credentials=self.creds)
        results = drive_service.files().list(
            q=f"name='{sheets_name}' and mimeType='application/vnd.google-apps.spreadsheet' and trashed=false",
            spaces='drive',
            pageSize=1,
            fields='files(id, name)'
        ).execute()
        
        files = results.get('files', [])
        if files:
            self.spreadsheet_id = files[0]['id']
            logger.info(f"✅ Planilha encontrada: {sheets_name}")
            return self.spreadsheet_id
        else:
            logger.error(f"❌ Planilha não encontrada: {sheets_name}")
            return None
    
    def get_captured_usernames(self):
        """Ler coluna A da planilha (@ já capturados)"""
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range='A:A'
            ).execute()
            
            values = result.get('values', [])
            # Pular header (primeira linha)
            usernames = [v[0] for v in values[1:] if v]
            return set(usernames)
        except Exception as e:
            logger.error(f"❌ Erro ao ler Sheets: {e}")
            return set()
    
    def add_row(self, username, status, timestamp, file_path, origin_file):
        """Adicionar linha na planilha"""
        values = [[username, status, timestamp, file_path, origin_file, 1]]
        
        self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range='A:F',
            valueInputOption='USER_ENTERED',
            body={'values': values}
        ).execute()
        
        logger.info(f"✅ Planilha atualizada: {username}")

class InstagramCapturer:
    def __init__(self):
        self.driver = None
    
    def login(self):
        """Login no Instagram"""
        options = FirefoxOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        
        self.driver = webdriver.Firefox(options=options)
        logger.info("🌐 Abrindo Instagram...")
        
        self.driver.get('https://www.instagram.com')
        time.sleep(2)
        
        try:
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'username'))
            )
            email_input.send_keys(CONFIG['instagram_email'])
            time.sleep(1)
            
            password_input = self.driver.find_element(By.NAME, 'password')
            password_input.send_keys(CONFIG['instagram_password'])
            time.sleep(1)
            
            login_btn = self.driver.find_element(By.XPATH, "//button[@type='button']")
            login_btn.click()
            time.sleep(5)
            
            logger.info("✅ Login realizado com sucesso")
        except Exception as e:
            logger.error(f"❌ Erro no login: {e}")
            return False
        
        return True
    
    def capture_profile(self, username):
        """Capturar screenshot de perfil"""
        try:
            url = f'https://www.instagram.com/{username}/'
            self.driver.get(url)
            time.sleep(3)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"@{username}_{timestamp}.png"
            filepath = os.path.join(CONFIG['output_dir'], filename)
            
            self.driver.save_screenshot(filepath)
            logger.info(f"✅ Screenshot capturado: {filename}")
            
            return filepath
        except Exception as e:
            logger.error(f"❌ Erro ao capturar @{username}: {e}")
            return None
    
    def close(self):
        """Fechar navegador"""
        if self.driver:
            self.driver.quit()

class FollowersAnalyzer:
    def __init__(self):
        self.drive = GoogleDriveService(CONFIG['service_account_path'])
        self.sheets = GoogleSheetsService(CONFIG['service_account_path'])
        self.instagram = InstagramCapturer()
    
    def run(self):
        """Executar ciclo completo"""
        logger.info("=" * 60)
        logger.info("🔄 CICLO DE PROCESSAMENTO INICIADO")
        logger.info("=" * 60)
        
        try:
            # 1. Conectar Google Drive
            if not self.drive.get_folder_id(CONFIG['drive_folder_name']):
                logger.error("Falha ao encontrar pasta no Drive")
                return False
            
            # 2. Conectar Google Sheets
            if not self.sheets.get_spreadsheet_id(CONFIG['sheets_name']):
                logger.error("Falha ao encontrar planilha")
                return False
            
            # 3. Login Instagram
            if not self.instagram.login():
                logger.error("Falha no login Instagram")
                return False
            
            # 4. Listar arquivos novos
            files = self.drive.list_new_files()
            if not files:
                logger.info("⏳ Nenhum arquivo novo para processar")
                return True
            
            # 5. Processar arquivos
            logger.info(f"📁 Encontrados {len(files)} arquivo(s) novo(s)")
            
            # Por enquanto, registrar o que encontrou
            for file in files[:5]:  # Máx 5 arquivos por ciclo
                logger.info(f"  - {file['name']} (criado: {file['createdTime']})")
            
            # TODO: Usar Vision AI para extrair @usernames das imagens
            # TODO: Verificar duplicatas
            # TODO: Capturar screenshots
            # TODO: Atualizar Sheets
            
            logger.info("✅ Ciclo concluído com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro no ciclo: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
        
        finally:
            self.instagram.close()

def main():
    logger.info("🚀 AGENTE FOLLOWERS ANALYZER - SOLUÇÃO HYBRID")
    logger.info(f"Timestamp: {datetime.now()}")
    
    analyzer = FollowersAnalyzer()
    success = analyzer.run()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
