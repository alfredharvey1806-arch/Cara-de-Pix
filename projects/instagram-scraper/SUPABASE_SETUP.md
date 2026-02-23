# 🚀 Supabase Setup - Instagram Followers Tracker

## O que temos
- ✅ Credenciais Supabase
- ✅ Script Python para integração (`supabase_client.py`)
- ✅ `.env` com chaves armazenadas (seguro, não comita no git!)

## PASSO 1: Criar Tabela no Supabase

1. Acesse: https://app.supabase.com
2. Vá em "SQL Editor" no painel esquerdo
3. Execute este script:

```sql
-- Criar tabela instagram_followers
CREATE TABLE instagram_followers (
  id BIGSERIAL PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  status TEXT DEFAULT 'esperando' CHECK (status IN ('esperando', 'print feito')),
  file_path TEXT,
  added_at TIMESTAMP DEFAULT NOW(),
  print_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Criar índices para performance
CREATE INDEX idx_username ON instagram_followers(username);
CREATE INDEX idx_status ON instagram_followers(status);

-- Habilitar RLS (Row Level Security)
ALTER TABLE instagram_followers ENABLE ROW LEVEL SECURITY;

-- Policy: Permitir leitura pública
CREATE POLICY "Enable read access for all users" ON instagram_followers
AS PERMISSIVE FOR SELECT USING (true);

-- Policy: Permitir insert/update com chave anon
CREATE POLICY "Enable insert/update for authenticated users" ON instagram_followers
AS PERMISSIVE FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable update for authenticated users" ON instagram_followers
AS PERMISSIVE FOR UPDATE USING (true);
```

Clique em "Run" e confirme.

---

## PASSO 2: Testar Integração Python

```bash
cd /home/harvey1806/.openclaw/workspace/projects/instagram-scraper

# Instalar dependências
pip install python-dotenv supabase

# Rodar teste
python3 supabase_client.py
```

Deve retornar algo como:
```
✅ Table 'instagram_followers' already exists
🔍 Testing check_username_exists:
{"exists": true, "data": {...}}
```

---

## PASSO 3: Integrar no Agente Hybrid

O agente vai fazer:
1. **Ao tirar print**: Checar se @username já existe em Supabase
2. **Se não existe**: Adicionar com status `esperando`
3. **Se existe com status `esperando`**: Atualizar para `print feito` + salvar file_path
4. **Se existe com status `print feito`**: Ignorar (já foi processado)

Exemplo de fluxo:
```
Pedro envia print via Telegram: "@thiagofinch @boludogamer @influencer123"
↓
Alfred extrai cada @username
↓
Para cada:
  - Checa no Supabase se existe
  - Se não, add com status "esperando"
  - Se sim e status "esperando", continua no fluxo
  - Se sim e status "print feito", pula
↓
Tira print de cada um (via Firefox headless)
↓
Salva em Seguidores/
↓
Atualiza Supabase: status = "print feito", file_path = caminho local
↓
Confirma para Pedro: "✅ 3 prints capturados e salvos"
```

---

## PASSO 4: Extrair @usernames de Imagem

Para ler @usernames de um print do Telegram, precisamos de **OCR**:

```bash
pip install pytesseract pillow
```

Script auxiliar:
```python
import pytesseract
from PIL import Image
import re

def extract_usernames_from_image(image_path: str) -> list:
    """Extract Instagram usernames from image using OCR"""
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    
    # Regex para encontrar @username
    usernames = re.findall(r'@([a-zA-Z0-9_.]+)', text)
    return list(set(usernames))  # Remove duplicatas

# Uso
usernames = extract_usernames_from_image("novo_seguidores.png")
# ['thiagofinch', 'boludogamer', 'influencer123']
```

---

## ⚠️ SEGURANÇA

**IMPORTANTE:**
- `.env` está no `.gitignore` (não comita!)
- Credenciais Supabase são **reais** → Não exponha em logs ou repositórios públicos
- A `ANON_KEY` é para operações públicas (leitura/escrita básica)
- A `SERVICE_KEY` é para admin (use só em backend seguro)

Verificar `.gitignore`:
```bash
echo ".env" >> /home/harvey1806/.openclaw/workspace/projects/instagram-scraper/.gitignore
```

---

## Status Atual
- ✅ Tabela schema pronto
- ✅ Script `supabase_client.py` pronto
- ⏳ Aguardando: Criar tabela no Supabase (PASSO 1)
- ⏳ Aguardando: Integração com OCR e Telegram webhook
