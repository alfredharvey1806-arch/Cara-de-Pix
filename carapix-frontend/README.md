# CaraPix Frontend

Painel em Next.js para visualizar os seguidores analisados pelo pipeline "Cara de Pix" – com screenshot, score, veredito, justificativa, alerta e mensagem inicial sugerida.

## 📦 Stack
- Next.js (App Router + TypeScript)
- Tailwind CSS
- Supabase (`instagram_followers` table)

## 🚀 Setup Local
1. Copie o arquivo de variáveis:
   ```bash
   cp .env.example .env.local
   ```
2. Preencha com o **Supabase URL** e **anon key**.
3. Rode o servidor:
   ```bash
   npm install
   npm run dev
   ```
4. Abra `http://localhost:3000`.

> O app faz consultas server-side usando o Supabase anon key (somente leitura).

## 🔧 Campos utilizados
A página consome os campos:
- `username`
- `file_path`
- `gpt_score`
- `gpt_verdict`
- `gpt_classification`
- `gpt_summary`
- `gpt_alert`
- `gpt_dm_hook`
- `gpt_analyzed_at`
- `analysis_status`

Certifique-se que o script `analyze_gpt.py` está preenchendo os campos antes de abrir o painel.

## ☁️ Deploy no Vercel
1. Crie o projeto via `vercel` ou painel do Vercel.
2. Adicione as mesmas variáveis (`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`).
3. Deploy (`vercel --prod`).

Pronto: o dashboard estará pronto para filtrar leads, copiar mensagens iniciais e priorizar quem realmente tem “cara de pix”.
