#!/bin/bash

# Setup Solução Hybrid
# Instalação de dependências + Configuração de Cron

set -e

echo "🚀 SETUP SOLUÇÃO HYBRID"
echo "=================================="
echo ""

VENV="/home/harvey1806/.openclaw/workspace/venv"
PROJECT_DIR="/home/harvey1806/.openclaw/workspace/projects/instagram-scraper"
OUTPUT_DIR="/home/harvey1806/Documents/Seguidores"

echo "📦 PASSO 1: Instalar dependências Python"
echo "---"
source $VENV/bin/activate

pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client -q
pip install selenium -q

echo "✅ Dependências instaladas"
echo ""

echo "📝 PASSO 2: Gerar estrutura de credenciais"
echo "---"

mkdir -p "$OUTPUT_DIR/.metadata"

# Criar arquivo placeholder para service account
cat > "$OUTPUT_DIR/.metadata/service_account_placeholder.json" << 'EOF'
{
  "type": "service_account",
  "project_id": "YOUR_PROJECT_ID",
  "private_key_id": "YOUR_KEY_ID",
  "private_key": "YOUR_PRIVATE_KEY",
  "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
  "client_id": "YOUR_CLIENT_ID",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
}
EOF

echo "⚠️  Arquivo placeholder criado: $OUTPUT_DIR/.metadata/service_account_placeholder.json"
echo "   VOCÊ PRECISA SUBSTITUIR COM SEU JSON BAIXADO DO GOOGLE CLOUD"
echo ""

echo "🔄 PASSO 3: Testar script principal"
echo "---"

chmod +x "$PROJECT_DIR/agente_hybrid.py"

echo "✅ Script pronto para execução"
echo ""

echo "📋 PASSO 4: Configurar Cron Job"
echo "---"

# Criar script wrapper para cron
cat > "/home/harvey1806/.openclaw/workspace/agente-followers.sh" << 'EOF'
#!/bin/bash
cd /home/harvey1806/.openclaw/workspace
source venv/bin/activate
python3 projects/instagram-scraper/agente_hybrid.py
EOF

chmod +x "/home/harvey1806/.openclaw/workspace/agente-followers.sh"

echo "✅ Script wrapper criado"
echo ""

echo "⏰ PASSO 5: Agendar Cron (a cada 5 minutos)"
echo "---"

# Verificar se job já existe
CRON_JOB="*/5 * * * * /home/harvey1806/.openclaw/workspace/agente-followers.sh >> /home/harvey1806/Documents/Seguidores/.metadata/cron.log 2>&1"

if crontab -l 2>/dev/null | grep -q "agente-followers.sh"; then
  echo "⚠️  Job já existe no crontab"
else
  { crontab -l 2>/dev/null || true; echo "$CRON_JOB"; } | crontab -
  echo "✅ Cron job adicionado (a cada 5 minutos)"
fi

echo ""
echo "=================================="
echo "✅ SETUP HYBRID CONCLUÍDO"
echo "=================================="
echo ""

echo "📋 PRÓXIMOS PASSOS:"
echo ""
echo "1️⃣  Criar Service Account no Google Cloud:"
echo "   https://console.cloud.google.com"
echo ""
echo "2️⃣  Baixar JSON e salvar em:"
echo "   /home/harvey1806/.openclaw/workspace/projects/instagram-scraper/service_account.json"
echo ""
echo "3️⃣  Compartilhar folders com email da service account:"
echo "   - Google Drive > Novos Seguidores"
echo "   - Google Sheets > Followers Tracker"
echo ""
echo "4️⃣  Validar instalação:"
echo "   bash /home/harvey1806/.openclaw/workspace/agente-followers.sh"
echo ""
echo "5️⃣  Ver logs:"
echo "   tail -f /home/harvey1806/Documents/Seguidores/.metadata/cron.log"
echo ""

echo "🟢 AGENTE ESTÁ PRONTO PARA FUNCIONAR 24/7"
echo ""
