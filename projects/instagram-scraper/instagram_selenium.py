#!/usr/bin/env python3
"""
Instagram Search + Screenshot via Selenium + Undetected Chrome
Fluxo:
1. Login com credenciais
2. Clica na lupa de pesquisa
3. Digita @username
4. Screenshot do perfil
5. Salva em /home/harvey1806/Documents/Seguidores/
"""

import sys
import re
import time
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Config
EMAIL = "alfredharvey1806@gmail.com"
PASSWORD = "Sucesso$$2026$$"
OUTPUT_DIR = Path("/home/harvey1806/Documents/Seguidores")
INSTAGRAM_URL = "https://www.instagram.com"

def instagram_search_and_capture(username: str):
    """
    Automação:
    1. Abre Instagram
    2. Faz login
    3. Clica na lupa
    4. Pesquisa @username
    5. Screenshot
    6. Salva
    """
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"@{username}_{timestamp}.png"
    filepath = OUTPUT_DIR / filename
    
    print(f"\n{'='*70}")
    print(f"🔄 CAPTURA: @{username}")
    print(f"{'='*70}")
    print(f"📧 Email: {EMAIL}")
    print(f"📱 Modo: Navegador Real (Undetected Chrome)")
    print(f"💾 Destino: {filepath}")
    print(f"⏰ Timestamp: {timestamp}")
    print(f"{'='*70}\n")
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    driver = None
    try:
        # Launch Firefox
        print("🌐 Inicializando Firefox...")
        options = FirefoxOptions()
        options.add_argument("--width=375")
        options.add_argument("--height=812")
        options.set_preference("general.useragent.override", "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X)")
        
        driver = webdriver.Firefox(options=options)
        driver.set_window_size(375, 812)  # Mobile viewport
        
        # Go to Instagram
        print("📍 Abrindo Instagram...")
        driver.get(INSTAGRAM_URL)
        time.sleep(3)
        
        # Check if logged in
        try:
            driver.find_element(By.XPATH, "//svg[@aria-label='Home']")
            print("✅ Já logado no Instagram")
        except:
            print("🔐 Fazendo login...")
            # Wait for login button and click
            login_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Log in"))
            )
            login_link.click()
            time.sleep(2)
            
            # Enter email
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            email_input.send_keys(EMAIL)
            print("   ✓ Email digitado")
            time.sleep(1)
            
            # Enter password
            password_input = driver.find_element(By.NAME, "password")
            password_input.send_keys(PASSWORD)
            print("   ✓ Senha digitada")
            time.sleep(1)
            
            # Click login button
            login_btn = driver.find_element(By.XPATH, "//button[@type='button']")
            login_btn.click()
            print("   ✓ Login enviado")
            time.sleep(5)
        
        # Click search icon
        print("🔍 Clicando na lupa de pesquisa...")
        try:
            search_icon = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//svg[@aria-label='Search']"))
            )
            search_icon.click()
            time.sleep(2)
        except:
            # Alternative: click search link
            search_link = driver.find_element(By.XPATH, "//a[contains(@href, '/explore/')]")
            search_link.click()
            time.sleep(2)
        
        # Type username in search
        print(f"📝 Pesquisando: @{username}")
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']"))
        )
        search_input.send_keys(username)
        time.sleep(2)
        
        # Click on profile result
        print("🎯 Clicando no perfil...")
        profile_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[contains(@href, '/{username}/')]"))
        )
        profile_link.click()
        time.sleep(3)
        
        # Check if profile exists
        try:
            not_found = driver.find_element(By.XPATH, "//*[contains(text(), 'Sorry')]")
            print(f"❌ Perfil @{username} não encontrado")
            return {"success": False, "message": f"Perfil @{username} não encontrado"}
        except:
            pass
        
        # Take screenshot
        print(f"📸 Capturando screenshot...")
        driver.save_screenshot(str(filepath))
        print(f"✅ Screenshot salvo: {filename}")
        
        # Log capture
        log_file = OUTPUT_DIR / "index.md"
        with open(log_file, 'a') as f:
            f.write(f"- `@{username}` | {timestamp} | {filename}\n")
        print(f"📝 Log atualizado")
        
        return {
            "success": True,
            "username": username,
            "filename": filename,
            "filepath": str(filepath),
            "timestamp": timestamp,
            "message": f"✅ Captura salva: {filename}"
        }
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"success": False, "message": f"Erro na captura: {str(e)}"}
    
    finally:
        if driver:
            driver.quit()

def main():
    if len(sys.argv) < 2:
        print("❌ Uso: instagram_selenium.py @username")
        sys.exit(1)
    
    input_text = sys.argv[1]
    match = re.search(r'@(\w+)', input_text)
    
    if not match:
        print(f"❌ Username não encontrado: {input_text}")
        sys.exit(1)
    
    username = match.group(1)
    print(f"✅ Username extraído: @{username}")
    
    result = instagram_search_and_capture(username)
    print(f"\n{result['message']}")

if __name__ == "__main__":
    main()
