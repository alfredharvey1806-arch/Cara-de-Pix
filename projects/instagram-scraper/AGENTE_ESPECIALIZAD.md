# 🤖 AGENTE ESPECIALIZADO - Instagram Followers Analyzer

## Objetivo
Automatizar a captura de screenshots de novos seguidores a partir de images enviadas para Google Drive.

## Fluxo Principal

### 1️⃣ Monitora Google Drive
- Pasta: `Novos Seguidores` (alfredharvey1806@gmail.com)
- Busca por novas imagens (PNG, JPG)
- Polling: a cada 5 minutos ou webhook

### 2️⃣ Extrai @ da Imagem
- Usa Vision AI (Claude) pra ler a imagem
- Identifica todos os usernames (@username)
- Lista completa dos novos seguidores

### 3️⃣ Verifica Duplicatas
- Consulta Google Sheets
- Verifica se @ já foi capturado
- Status: ✅ Já capturado / ⏳ Pendente

### 4️⃣ Captura Screenshots
- Para cada @ novo:
  - Abre browser (Chrome relay)
  - Navega até @username
  - Tira screenshot
  - Salva em `/home/harvey1806/Documents/Seguidores/@username_TIMESTAMP.png`

### 5️⃣ Atualiza Google Sheets
- Coluna A: @ (username)
- Coluna B: Status (✅ Capturado / ⏳ Pendente)
- Coluna C: Data/Hora da captura
- Coluna D: Link do arquivo
- Coluna E: Arquivo de origem (qual imagem de seguidores)

### 6️⃣ Notifica Pedro
- Mensagem: "✅ Processados X @ | Capturados Y novos | Duplicatas Z"
- Link para Google Sheets
- Tempo total de execução

## Tecnologias
- Google Drive API (authenticate via email/password)
- Google Sheets API (criar/atualizar planilha)
- Claude Vision (extrair @ das imagens)
- Browser Relay (screenshots automáticos)
- Polling/Cron (executar periodicamente)

## Status
🔴 **EM DESENVOLVIMENTO**
- [ ] Autenticação Google Drive
- [ ] Parser de imagens (OCR)
- [ ] Google Sheets integration
- [ ] Browser automation
- [ ] Deduplicação
- [ ] Notificação Pedro
- [ ] Deploy do agente

## Próximos Passos
1. Configurar credenciais Google
2. Criar pasta + Google Sheets
3. Montar agente com instruções
4. Testar com imagem de exemplo
5. Ativar monitor 24/7
