#!/usr/bin/env python3
"""
Atualiza status de análise no Supabase para os 15 perfis de Instagram
"""

import os
from supabase import create_client, Client
from datetime import datetime

# Credenciais Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise SystemExit("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY environment variables")

# Perfis capturados
PROFILES = [
    "ju_bettiol",
    "_manuteles",
    "beredela",
    "vanessamelolac",
    "hugobelo4st",
    "ulisses_samaniego",
    "gleiziburdzki",
    "josysantosvga",
    "sophs.xos",
    "_donzq",
    "soslimpezas2026",
    "iammsara__",
    "ferosemberg",
    "_majubittencourt",
    "deiseoliverr"
]

def update_profiles_status():
    """Atualiza status de todos os perfis para 'analise feita'"""
    try:
        # Conecta ao Supabase
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        
        print("🔄 Conectando ao Supabase...")
        print(f"📊 Atualizando {len(PROFILES)} perfis...\n")
        
        success_count = 0
        failed_count = 0
        
        for profile in PROFILES:
            try:
                # Atualiza status para 'analise feita'
                response = supabase.table("instagram_followers").update({
                    "status": "analise feita",
                    "updated_at": datetime.now().isoformat()
                }).eq("username", profile).execute()
                
                if response.data:
                    print(f"✅ @{profile} - Status atualizado para 'analise feita'")
                    success_count += 1
                else:
                    print(f"⚠️ @{profile} - Nenhum registro encontrado")
                    # Tenta adicionar se não existir
                    insert_response = supabase.table("instagram_followers").insert({
                        "username": profile,
                        "status": "analise feita",
                        "added_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat()
                    }).execute()
                    if insert_response.data:
                        print(f"   ➕ @{profile} - Novo registro criado")
                        success_count += 1
                    else:
                        failed_count += 1
                        
            except Exception as e:
                print(f"❌ @{profile} - Erro: {str(e)}")
                failed_count += 1
        
        print(f"\n📈 Resumo:")
        print(f"✅ Sucesso: {success_count}/{len(PROFILES)}")
        print(f"❌ Falhas: {failed_count}/{len(PROFILES)}")
        
        return success_count, failed_count
        
    except Exception as e:
        print(f"❌ Erro ao conectar ao Supabase: {str(e)}")
        return 0, len(PROFILES)

if __name__ == "__main__":
    update_profiles_status()
