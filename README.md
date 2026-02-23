# Cara de Pix – Instagram Follower Intelligence Pipeline

Sistema completo para classificar seguidores do Instagram, identificar perfis com alto potencial de compra ("cara de pix") usando OpenAI Vision, e visualizar resultados em um dashboard Supabase + Next.js.

## 🎯 O que faz

1. **Captura resiliente** de screenshots de perfis Instagram (via Chrome/Selenium)
2. **Análise GPT Vision** com prompt 6-em-1:
   - 🟢/🔴 Veredito (tem ou não cara de pix)
   - CRA Score (0-10, capacidade real de compra)
   - Justificativa (bullets objetivas)
   - Classificação (Vale DM | Nutrição | Ignorar)
   - Alerta (maior risco)
   - **Mensagem inicial** (social selling amigável pra DM)
3. **Dashboard** (Next.js + Tailwind) com filtros, cards, e dark theme
4. **Automação** sem parar – retry automático, health check, rate limiting

## 🚀 Quick Start

### 1. Clone e instale
```bash
git clone https://github.com/alfredharvey1806-arch/Cara-de-Pix.git
cd Cara-de-Pix
cp .env.example .env
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
npm install --prefix carapix-frontend
```

### 2. Configure `.env`
Preencha com suas credenciais:
```
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
SUPABASE_ANON_KEY=
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
```

### 3. Setup Supabase
```bash
python3 projects/instagram-scraper/migrate_schema.py
```
Copie o SQL que aparecer e execute no editor SQL do Supabase Dashboard.

### 4. Comece a capturar
```bash
# Execução única (teste)
python3 projects/instagram-scraper/capture_scheduler.py --mode once

# Produção – a cada 5 min (deixa rodando)
python3 projects/instagram-scraper/capture_scheduler.py --mode cron --interval 5 &

# Sincronizar prints pro Storage
python3 sync_screenshots_storage.py

# Rodar análise GPT
python3 projects/instagram-scraper/analyze_gpt.py

# Ver status em tempo real
python3 projects/instagram-scraper/monitor_capture.py --loop --interval 30
```

### 5. Abrir dashboard
```bash
cd carapix-frontend
npm run dev
# Acessa http://localhost:3000
```

## 📁 Estrutura

```
Cara-de-Pix/
├── projects/instagram-scraper/
│   ├── robust_capture.py          # Captura com retry + rate limit + health check
│   ├── capture_scheduler.py       # Agendador (once/loop/cron)
│   ├── analyze_gpt.py             # OpenAI Vision + prompt 6-em-1
│   ├── monitor_capture.py         # Dashboard CLI
│   ├── migrate_schema.py          # SQL pra Supabase (copiar/colar)
│   └── ROBUST_SETUP.md            # Documentação detalhada
├── carapix-frontend/              # Dashboard Next.js
├── sync_screenshots_storage.py    # Sincroniza com Supabase Storage
├── requirements.txt
├── .env.example
└── README.md
```

## 🔐 Variáveis de Ambiente

| Variável | Descrição |
|----------|-----------|
| `SUPABASE_URL` | URL do projeto Supabase |
| `SUPABASE_SERVICE_ROLE_KEY` | Chave service_role (inserts/updates) |
| `SUPABASE_ANON_KEY` | Chave anon (frontend) |
| `OPENAI_API_KEY` | API key OpenAI |
| `OPENAI_MODEL` | default: `gpt-4.1-mini` |
| `SCREENSHOTS_DIR` | Pasta de screenshots (default `~/Documents/Seguidores`) |

## 🧠 Fluxo Detalhado

```
[Screenshot] → [Supabase Storage]
                    ↓
            [analyze_gpt.py]
         (OpenAI Vision + Prompt)
                    ↓
      [gpt_verdict, score, msg DM]
                    ↓
         [carapix-frontend]
         (Dashboard + Filtros)
```

1. **Captura** – `robust_capture.py` pega `status=esperando`, tira screenshot, marca `print feito`
2. **Sincronização** – `sync_screenshots_storage.py` envia pra Supabase Storage
3. **Análise** – `analyze_gpt.py` chama OpenAI Vision, parseia resposta, preenche `gpt_*` fields
4. **Dashboard** – `carapix-frontend` lista cards com filtros por score/classificação

## 🛠️ Ferramentas Auxiliares

- **ROBUST_SETUP.md** – Guia passo a passo da automação
- **migrate_schema.py** – Gera SQL pra criar tabelas/índices no Supabase

## 🧪 Testando

```bash
# Teste local (sem cron)
python3 projects/instagram-scraper/capture_scheduler.py --mode loop --interval 5 --max-cycles 2

# Ver fila/resumo
python3 projects/instagram-scraper/monitor_capture.py

# Logs
tail -f ~/Documents/Seguidores/.metadata/capture.log
```

## 📊 Prompt GPT 6-em-1

O sistema usa um prompt brutalmente honesto que analisa:
- **Posicionamento profissional** (claro vs vago)
- **Bio** (adulto funcional vs aspiracional)
- **Conteúdo** (autoridade vs entretenimento)
- **Estética** (organizado vs amador)
- **Renda ativa** (empresa, clientes, projetos)

Resultado: **veredito 🟢/🔴 + score CRA + mensagem de DM conversacional** (não vendedora).

## ✅ Checklist Final

- [ ] `.env` preenchido
- [ ] Migrations executadas no Supabase
- [ ] `carapix-frontend/.env.local` configurado
- [ ] Rodou `pip install -r requirements.txt`
- [ ] Rodou `npm install --prefix carapix-frontend`
- [ ] Dashboard abrindo em `http://localhost:3000`
- [ ] Screenshots capturando e aparecendo no dashboard

## 📞 Suporte

Dúvidas? Veja `ROBUST_SETUP.md` pra documentação detalhada.
