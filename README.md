# Cara de Pix – Instagram Follower Intelligence Pipeline

Pipeline completo para classificar seguidores do Instagram, identificar perfis com "cara de pix" (alto potencial de compra) e disponibilizar os resultados em um dashboard Supabase/Next.js.

## 🧱 Arquitetura

```
[Instagram Screenshot Capture]
        │
        ▼
~/Documents/Seguidores/@username_timestamp.png
        │
        ▼
[sync_screenshots_storage.py]
  ↳ Supabase Storage (bucket instagram-screenshots)
  ↳ Tabela instagram_followers (status + file_path)
        │
        ▼
[projects/instagram-scraper/analyze_gpt.py]
  ↳ OpenAI Vision → veredito CRA + mensagem social selling
  ↳ Atualiza campos gpt_* na tabela
        │
        ├──> carapix-frontend (Next.js) consome supabase-js e mostra cards
        └──> monitor_capture.py / robust_capture.py cuidam da automação e saúde
```

Componentes principais:

| Pasta/Script | Função |
|--------------|--------|
| `projects/instagram-scraper/robust_capture.py` | Captura resiliente com retry, rate limiting e health check |
| `projects/instagram-scraper/capture_scheduler.py` | Agenda ciclos (modo once/loop/cron) |
| `sync_screenshots_storage.py` | Envia prints para Supabase Storage + sincroniza banco |
| `projects/instagram-scraper/analyze_gpt.py` | Chama OpenAI Vision com prompt 6-em-1 "Cara de Pix" |
| `carapix-frontend/` | Dashboard Next.js + Supabase (cards, filtros, dark theme) |
| `projects/instagram-scraper/monitor_capture.py` | Painel CLI com status em tempo real |
| `projects/instagram-scraper/ROBUST_SETUP.md` | Guia detalhado da automação de captura |
| `projects/instagram-scraper/automation_handler.py` e `crm_upload_handler*.py` | Fluxos auxiliares (integração CRM Lovable) |

## 🚀 Quick Start

1. **Clone e instale dependências**
   ```bash
   git clone https://github.com/alfredharvey1806-arch/Cara-de-Pix.git
   cd Cara-de-Pix
   cp .env.example .env
   python3 -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   npm install --prefix carapix-frontend
   ```
2. **Preencha `.env`** com suas chaves Supabase, OpenAI, credenciais do CRM e diretórios locais. Os scripts Python leem essas variáveis automaticamente.
3. **Atualize o schema no Supabase**
   ```bash
   source venv/bin/activate
   python3 projects/instagram-scraper/migrate_schema.py
   # siga as instruções e execute o SQL listado no dashboard Supabase
   ```
4. **Capture prints com resiliência**
   ```bash
   # Execução única (test)
   python3 projects/instagram-scraper/capture_scheduler.py --mode once --batch-size 5

   # Produção a cada 5 minutos
   python3 projects/instagram-scraper/capture_scheduler.py --mode cron --interval 5 --batch-size 5
   ```
5. **Sincronize com o Storage**
   ```bash
   python3 sync_screenshots_storage.py
   ```
6. **Rode a análise GPT**
   ```bash
   OPENAI_API_KEY=... SUPABASE_URL=... SUPABASE_SERVICE_ROLE_KEY=... \
   python3 projects/instagram-scraper/analyze_gpt.py
   ```
   - Usa prompt 6-em-1 (veredito, score CRA, bullets, classificação, alerta, mensagem inicial social selling)
   - Batch configurável via `GPT_BATCH`
7. **Suba o dashboard**
   ```bash
   cd carapix-frontend
   cp .env.example .env.local  # preencher com URL/anon key Supabase
   npm run dev   # ou npm run build && npm run start
   ```
8. **Monitorar**
   ```bash
   python3 projects/instagram-scraper/monitor_capture.py --loop --interval 30
   tail -f ~/Documents/Seguidores/.metadata/capture.log
   ```

## 🔐 Variáveis de Ambiente

`cp .env.example .env` e defina:

| Variável | Descrição |
|----------|-----------|
| `SUPABASE_URL` | URL do projeto Supabase |
| `SUPABASE_SERVICE_ROLE_KEY` | chave service_role (para inserts/updates) |
| `SUPABASE_ANON_KEY` | opcional (frontend) |
| `SUPABASE_BUCKET_NAME` | default `instagram-screenshots` |
| `SCREENSHOTS_DIR` | pasta onde ficam os PNGs (default `~/Documents/Seguidores`) |
| `OPENAI_API_KEY` / `OPENAI_MODEL` | credenciais GPT Vision |
| `CRM_URL`, `CRM_EMAIL`, `CRM_PASSWORD` | acesso ao Lovable CRM |
| `INSTAGRAM_USERNAME` / `INSTAGRAM_PASSWORD` | usados pelos agentes de captura |
| `ANALYSIS_LOG_PATH` | (opcional) caminho customizado para logs |

O frontend usa `.env.local` próprio (baseado em `carapix-frontend/.env.example`).

## 🧩 Fluxo Detalhado

1. **Captura resiliente** – `robust_capture.py` pega perfis com `status="esperando"`, tira print (via Chrome Relay ou Selenium), marca `processando → print feito`, e agenda retry automático (até 3x) se algo falhar.
2. **Sincronização Storage** – `sync_screenshots_storage.py` garante bucket, envia PNGs e atualiza `file_path` com URL pública.
3. **Análise GPT/Vision** – `analyze_gpt.py` lê registros com `analysis_status in (pending,error)`, chama OpenAI Vision, parseia resposta no formato bruto e preenche `gpt_score`, `gpt_verdict`, `gpt_classification`, `gpt_summary`, `gpt_alert`, `gpt_dm_hook`.
4. **Dashboard** – `carapix-frontend` (Next.js + Tailwind) lista cards com filtros por score/classificação, highlight dos 🟢, alertas e hooks de DM.
5. **CRM Upload (opcional)** – `crm_upload_handler.py` e `crm_upload_handler_v2.py` cuidam do envio dos prints para o Lovable Pix Prospector.
6. **Monitoramento** – `monitor_capture.py` mostra fila, retries e taxa de sucesso. Logs ficam em `~/Documents/Seguidores/.metadata/capture.log`.

## 🛠️ Ferramentas Auxiliares

- `projects/instagram-scraper/ROBUST_SETUP.md`: guia passo a passo para colocar o capturador em produção.
- `projects/instagram-scraper/FLUXO_AUTOMACAO.md`: documentação do fluxo completo (Drive → Screenshot → Supabase → GPT → CRM).
- `projects/instagram-scraper/automation_handler.py`: orquestração tudo-em-um (para sub-agentes).
- `projects/instagram-scraper/STATUS_FINAL.md`: checklist final do agente de seguidores.

## 🧪 Testes & Debug

- Use `python3 projects/instagram-scraper/capture_scheduler.py --mode loop --interval 2 --max-cycles 2` para testar sem cron.
- Rode `python3 projects/instagram-scraper/monitor_capture.py` para ver fila/resumo.
- No frontend, `npm run lint` garante consistência.

## 📁 Estrutura

```
Cara-de-Pix/
├── carapix-frontend/        # Dashboard Next.js
├── projects/instagram-scraper/
│   ├── robust_capture.py
│   ├── capture_scheduler.py
│   ├── monitor_capture.py
│   ├── analyze_gpt.py
│   ├── automation_handler.py
│   ├── ROBUST_SETUP.md
│   └── ...
├── sync_screenshots_storage.py
├── supabase_update.py
├── requirements.txt
├── README.md
└── .env.example
```

## ✅ Boas Práticas

- **Não** comitar `.env`, `memory/`, `seguidores_screenshots/` (já incluídos no `.gitignore`).
- Executar `pip install -r requirements.txt` após qualquer atualização de dependências.
- Usar `python3 -m pip install ... && pip freeze > requirements.txt` se adicionar libs.
- Documentar mudanças significativas em `projects/instagram-scraper/ROBUST_SETUP.md` ou em novos arquivos dentro de `projects/`.

## 📣 Suporte

Dúvidas ou sugestões? Abra uma issue no repositório ou atualize os arquivos em `projects/instagram-scraper/` conforme o padrão descrito em `ROBUST_SETUP.md`.
