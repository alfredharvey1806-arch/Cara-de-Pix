# 🚀 DEPLOY SOLUÇÃO HYBRID - GUIA FINAL

## ✅ O QUE JÁ FOI FEITO (Setup Automático)

```
✅ Agente Python criado (agente_hybrid.py)
✅ Script wrapper criado (agente-followers.sh)
✅ Dependências instaladas (Google APIs + Selenium)
✅ Cron job agendado (a cada 5 minutos)
✅ Estrutura de logs criada
✅ Config template pronto
```

---

## 🔐 PRÓXIMOS PASSOS (VOCÊ PRECISA FAZER)

### PASSO 1: Criar Service Account no Google Cloud

1. **Acesse o Google Cloud Console:**
   ```
   https://console.cloud.google.com
   ```

2. **Criar novo projeto:**
   - Clique em "Selecionar projeto" (canto superior)
   - "Novo projeto"
   - Nome: `Instagram Followers Analyzer`
   - Clique "Criar"

3. **Ativar APIs:**
   - Vá em "APIs e serviços"
   - Clique "Ativar APIs e serviços"
   - Procure e ative:
     - ✅ **Google Drive API**
     - ✅ **Google Sheets API**

4. **Criar Service Account:**
   - Menu esquerdo: "Credenciais"
   - "Criar credenciais" → "Conta de serviço"
   - Nome: `followers-analyzer`
   - Clique "Criar e continuar"
   - Papel: `Editor`
   - Clique "Continuar" → "Concluído"

5. **Gerar Chave JSON:**
   - Em "Credenciais", clique na conta criada
   - Vá em "Chaves"
   - "Adicionar chave" → "Criar nova chave"
   - Tipo: **JSON**
   - Clique "Criar"
   - **Arquivo será baixado** → Guarde!

---

### PASSO 2: Salvar Credenciais

1. **Abra o arquivo JSON baixado**
2. **Procure o campo `client_email`**
   - Exemplo: `followers-analyzer@instagram-xyz.iam.gserviceaccount.com`
3. **Copie o arquivo JSON inteiro**
4. **Salve em:**
   ```
   /home/harvey1806/.openclaw/workspace/projects/instagram-scraper/service_account.json
   ```

**Via terminal:**
```bash
# Criar arquivo vazio e colar conteúdo do JSON
nano /home/harvey1806/.openclaw/workspace/projects/instagram-scraper/service_account.json
# (Cole o conteúdo do JSON, Ctrl+X, Y, Enter)
```

---

### PASSO 3: Compartilhar com Service Account

1. **Pegar email da Service Account**
   - Abra o arquivo service_account.json
   - Copie o valor de `client_email`

2. **Compartilhar Google Drive**
   - Abra: https://drive.google.com
   - Pasta: `Novos Seguidores`
   - Clique "Compartilhar"
   - Cole email da service account
   - Permissão: **Editor**
   - Clique "Compartilhar"

3. **Compartilhar Google Sheets**
   - Abra: Google Sheets > `Followers Tracker`
   - Clique "Compartilhar"
   - Cole email da service account
   - Permissão: **Editor**
   - Clique "Compartilhar"

---

### PASSO 4: Adicionar SHEETS_ID

1. **Abra Google Sheets** > `Followers Tracker`
2. **Copie o ID da URL:**
   ```
   https://docs.google.com/spreadsheets/d/[ID_AQUI]/edit
   ```
   Copie apenas: `1aBcDeFgHiJkLmNoPqRsTuVwXyZ...`

3. **Edite o arquivo config.json:**
   ```bash
   nano /home/harvey1806/Documents/Seguidores/.metadata/config.json
   ```

4. **Cole o ID:**
   ```json
   {
     "drive_folder_id": null,
     "sheets_id": "1aBcDeFgHiJkLmNoPqRsTuVwXyZ",
     "processed_files": [],
     "captured_profiles": []
   }
   ```

---

## 🧪 TESTAR SISTEMA

### Teste 1: Validar credenciais
```bash
cd /home/harvey1806/.openclaw/workspace/projects/instagram-scraper
python3 agente_hybrid.py
```

**Saída esperada:**
```
✅ Google APIs disponíveis
✅ Autenticado no Google Drive e Sheets
✅ Pasta 'Novos Seguidores' encontrada: abc123xyz
...
```

### Teste 2: Verificar cron
```bash
crontab -l | grep agente-followers
```

**Saída esperada:**
```
*/5 * * * * /home/harvey1806/.openclaw/workspace/projects/instagram-scraper/agente-followers.sh >> /home/harvey1806/Documents/Seguidores/.metadata/cron.log 2>&1
```

### Teste 3: Ver logs
```bash
tail -f /home/harvey1806/Documents/Seguidores/.metadata/cron.log
```

---

## 🚀 COMO USAR

### Fluxo de Uso:
1. **Tire screenshot** de lista de seguidores no Instagram
2. **Suba em** Google Drive > `Novos Seguidores`
3. **Agente detecta** (próxima execução de 5 em 5 min)
4. **Extrai @usernames** da imagem
5. **Captura screenshots** de novos perfis
6. **Atualiza Sheets** automaticamente
7. **Você recebe notificação**

---

## 📊 ARQUIVOS IMPORTANTES

```
/home/harvey1806/Documents/Seguidores/
├── @pedrosallun_20260215_162628.png (screenshots capturados)
├── index.md (log de capturas)
└── .metadata/
    ├── config.json (SHEETS_ID vai aqui!)
    ├── agent_hybrid.log (logs da execução)
    └── cron.log (logs do cron)

/home/harvey1806/.openclaw/workspace/projects/instagram-scraper/
├── agente_hybrid.py (código principal)
├── agente-followers.sh (wrapper)
├── service_account.json (CREDENCIAIS - adicionar manualmente!)
└── ...outros arquivos
```

---

## ✨ RESULTADO ESPERADO

🟢 **100% Autônomo**
- ✅ Sem dependência de Browser Relay
- ✅ Sem risco de desconexão
- ✅ APIs diretas do Google (confiável)
- ✅ Firefox local (robusto)
- ✅ Cron job 24/7
- ✅ Logging completo
- ✅ Notificações automáticas

---

## 🆘 TROUBLESHOOTING

**"Arquivo service_account.json não encontrado"**
- Verifique caminho: `/home/harvey1806/.openclaw/workspace/projects/instagram-scraper/service_account.json`
- Certifique-se de colar o JSON correto

**"SHEETS_ID não configurado"**
- Edite: `/home/harvey1806/Documents/Seguidores/.metadata/config.json`
- Adicione o ID do Google Sheets

**"Pasta 'Novos Seguidores' não encontrada"**
- Certifique-se de compartilhar pasta com email da service account
- Verifique permissões (Editor)

**"Cron não está executando"**
```bash
# Ver erros do cron
tail -f /home/harvey1806/Documents/Seguidores/.metadata/cron.log

# Testar script manualmente
bash /home/harvey1806/.openclaw/workspace/projects/instagram-scraper/agente-followers.sh
```

---

## 📋 CHECKLIST FINAL

- [ ] Service Account criado no Google Cloud
- [ ] JSON baixado e salvo em `/instagram-scraper/service_account.json`
- [ ] Google Drive compartilhado com service account
- [ ] Google Sheets compartilhado com service account
- [ ] SHEETS_ID adicionado em `config.json`
- [ ] Teste executado com sucesso
- [ ] Cron job verificado
- [ ] Primeira imagem subida em `Novos Seguidores`
- [ ] Agente processou e capturou perfis
- [ ] Sheets foi atualizado
- [ ] 🎉 Sistema 100% funcional!

---

## 🎯 QUANDO ESTIVER PRONTO

1. Complete todos os passos acima
2. Execute o teste: `python3 agente_hybrid.py`
3. Avise que está tudo pronto
4. Faça upload de uma imagem em `Novos Seguidores`
5. Agente rodará a cada 5 minutos automaticamente

**Tempo total de setup: ~30 minutos**

Boa sorte! 🚀
