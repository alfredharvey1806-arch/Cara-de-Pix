-- Cara de Pix - Supabase Migration
-- Execute este SQL no editor SQL do Supabase Dashboard
-- Caminho: https://app.supabase.com/project/[seu-projeto]/sql/new

-- Criar tabela instagram_followers (se não existir)
CREATE TABLE IF NOT EXISTS instagram_followers (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    status TEXT CHECK (status IN ('esperando', 'print feito', 'processando', 'erro')),
    file_path TEXT,
    
    -- Campos de captura
    capture_retry_count INT DEFAULT 0,
    capture_error TEXT,
    capture_started_at TIMESTAMP,
    capture_completed_at TIMESTAMP,
    capture_next_retry TIMESTAMP,
    
    -- Campos de análise GPT
    gpt_score NUMERIC(3,1),
    gpt_verdict TEXT,
    gpt_summary TEXT,
    gpt_classification TEXT,
    gpt_alert TEXT,
    gpt_dm_hook TEXT,
    gpt_raw TEXT,
    gpt_analyzed_at TIMESTAMP,
    gpt_model TEXT,
    analysis_status TEXT CHECK (analysis_status IN ('pending', 'done', 'error')),
    
    -- Timestamps
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT instagram_followers_status_check CHECK (status IN ('esperando', 'print feito', 'processando', 'erro'))
);

-- Criar índices para queries rápidas
CREATE INDEX IF NOT EXISTS idx_instagram_followers_status 
ON instagram_followers(status);

CREATE INDEX IF NOT EXISTS idx_instagram_followers_gpt_score 
ON instagram_followers(gpt_score DESC NULLS LAST);

CREATE INDEX IF NOT EXISTS idx_instagram_followers_analysis_status 
ON instagram_followers(analysis_status);

CREATE INDEX IF NOT EXISTS idx_instagram_followers_status_capture 
ON instagram_followers(status, capture_next_retry);

-- Criar Storage bucket "instagram-screenshots" (se não existir)
-- Nota: Para criar bucket via SQL, use:
-- INSERT INTO storage.buckets (id, name, public)
-- VALUES ('instagram-screenshots', 'instagram-screenshots', true)
-- ON CONFLICT (id) DO NOTHING;

-- Ou crie manualmente no dashboard Storage:
-- 1. Clique em "Buckets"
-- 2. Clique em "Create Bucket"
-- 3. Nome: instagram-screenshots
-- 4. Marque "Public bucket"
-- 5. Clique "Create"

-- Verificar estrutura final
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'instagram_followers' 
ORDER BY ordinal_position;
