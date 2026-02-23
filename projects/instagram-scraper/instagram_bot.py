#!/usr/bin/env python3
"""
Instagram Profile Screenshot Bot
Automação: Login + Screenshot Mobile + Save
"""

import asyncio
import sys
import re
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright, Page

# Config
EMAIL = "alfredharvey1806@gmail.com"
PASSWORD = "Sucesso$$2026$$"
OUTPUT_DIR = Path("/home/harvey1806/Documents/Seguidores")
INSTAGRAM_URL = "https://www.instagram.com"

async def instagram_capture(username: str):
    """
    Automação Instagram:
    1. Login
    2. Navega para perfil
    3. Screenshot em modo mobile
    4. Salva arquivo
    """
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"@{username}_{timestamp}.png"
    filepath = OUTPUT_DIR / filename
    
    print(f"\n{'='*70}")
    print(f"🔄 CAPTURA: @{username}")
    print(f"{'='*70}")
    print(f"📧 Email: {EMAIL}")
    print(f"📱 Viewport: 375x812 (iPhone)")
    print(f"💾 Destino: {filepath}")
    print(f"⏰ Timestamp: {timestamp}")
    print(f"{'='*70}\n")
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    async with async_playwright() as p:
        try:
            # Launch Firefox
            browser = await p.firefox.launch(headless=False)
            context = await browser.new_context(
                viewport={"width": 375, "height": 812},
                user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15"
            )
            page = await context.new_page()
            
            print("🌐 Abrindo Instagram...")
            await page.goto(INSTAGRAM_URL, wait_until="networkidle")
            
            # Check if already logged in
            login_needed = await page.query_selector('a[href="/accounts/login/"]') is not None
            
            if login_needed:
                print("🔐 Fazendo login...")
                await page.click('a[href="/accounts/login/"]')
                await page.wait_for_load_state("networkidle")
                
                # Input email
                email_input = await page.query_selector('input[name="username"]')
                if email_input:
                    await email_input.fill(EMAIL)
                    print(f"   ✓ Email digitado")
                
                # Input password
                password_input = await page.query_selector('input[name="password"]')
                if password_input:
                    await password_input.fill(PASSWORD)
                    print(f"   ✓ Senha digitada")
                
                # Click login button
                login_btn = await page.query_selector('button[type="button"]')
                if login_btn:
                    await login_btn.click()
                    print(f"   ✓ Botão de login clicado")
                    await page.wait_for_load_state("networkidle")
                    await asyncio.sleep(3)
            
            # Navigate to profile
            profile_url = f"{INSTAGRAM_URL}/{username}/"
            print(f"📍 Navegando para: {profile_url}")
            await page.goto(profile_url, wait_until="networkidle")
            await asyncio.sleep(2)
            
            # Check if profile exists
            not_found = await page.query_selector('span:has-text("Sorry, this page isn\'t available.")')
            if not_found:
                print(f"❌ Perfil @{username} não encontrado")
                await browser.close()
                return {"success": False, "message": f"Perfil @{username} não encontrado"}
            
            # Take screenshot
            print(f"📸 Capturando screenshot...")
            await page.screenshot(path=str(filepath), full_page=False)
            
            print(f"✅ Screenshot salvo: {filename}")
            
            # Log capture
            log_file = OUTPUT_DIR / "index.md"
            with open(log_file, 'a') as f:
                f.write(f"- `@{username}` | {timestamp} | {filename}\n")
            print(f"📝 Log atualizado")
            
            await browser.close()
            
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
            return {"success": False, "message": f"Erro na captura: {str(e)}"}

async def main():
    if len(sys.argv) < 2:
        print("❌ Uso: instagram_bot.py @username")
        sys.exit(1)
    
    input_text = sys.argv[1]
    match = re.search(r'@(\w+)', input_text)
    
    if not match:
        print(f"❌ Username não encontrado: {input_text}")
        sys.exit(1)
    
    username = match.group(1)
    print(f"✅ Username extraído: @{username}")
    
    result = await instagram_capture(username)
    print(f"\n{result['message']}")

if __name__ == "__main__":
    asyncio.run(main())
