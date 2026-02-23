#!/usr/bin/env python3
"""
Migração de schema Supabase para suportar captura robusta.
Adiciona colunas de rastreamento, retry, timestamps.
"""

import os
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise SystemExit("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY environment variables")

def run_migration():
    """
    ATENÇÃO: Execute manualmente no Supabase SQL Editor.
    Colunas necessárias:
    
    ALTER TABLE instagram_followers ADD COLUMN IF NOT EXISTS capture_retry_count INT DEFAULT 0;
    ALTER TABLE instagram_followers ADD COLUMN IF NOT EXISTS capture_error TEXT;
    ALTER TABLE instagram_followers ADD COLUMN IF NOT EXISTS capture_started_at TIMESTAMP;
    ALTER TABLE instagram_followers ADD COLUMN IF NOT EXISTS capture_completed_at TIMESTAMP;
    ALTER TABLE instagram_followers ADD COLUMN IF NOT EXISTS capture_next_retry TIMESTAMP;
    
    Então volte aqui e confirme que as colunas foram criadas.
    """
    
    print("=" * 60)
    print("🔧 MIGRAÇÃO DE SCHEMA - Captura Robusta")
    print("=" * 60)
    print()
    print("⚠️  INSTRUÇÕES:")
    print("1. Acesse: https://app.supabase.com/project/sfqsghgogwtxwzthscvw/sql/new")
    print("2. Cole e execute o SQL abaixo:")
    print()
    print("=" * 60)
    
    sql = """
-- Adicionar colunas para suportar captura robusta
ALTER TABLE instagram_followers 
ADD COLUMN IF NOT EXISTS capture_retry_count INT DEFAULT 0,
ADD COLUMN IF NOT EXISTS capture_error TEXT,
ADD COLUMN IF NOT EXISTS capture_started_at TIMESTAMP,
ADD COLUMN IF NOT EXISTS capture_completed_at TIMESTAMP,
ADD COLUMN IF NOT EXISTS capture_next_retry TIMESTAMP;

-- Criar índice para queries mais rápidas
CREATE INDEX IF NOT EXISTS idx_instagram_followers_status_capture 
ON instagram_followers(status, capture_next_retry);

-- Verificar estrutura final
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'instagram_followers' 
ORDER BY ordinal_position;
"""
    
    print(sql)
    print("=" * 60)
    print()
    print("3. Execute o SQL acima")
    print("4. Volte aqui e confirme que funcionou")
    print()
    
    # Testar conexão
    try:
        client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        result = client.table("instagram_followers").select("id").limit(1).execute()
        print("✅ Conexão com Supabase OK")
        print()
        
        # Listar colunas atuais
        print("📋 Colunas atuais na tabela:")
        if result.data:
            cols = list(result.data[0].keys())
            for col in sorted(cols):
                print(f"   - {col}")
        
    except Exception as e:
        print(f"❌ Erro ao testar Supabase: {e}")

if __name__ == "__main__":
    run_migration()
