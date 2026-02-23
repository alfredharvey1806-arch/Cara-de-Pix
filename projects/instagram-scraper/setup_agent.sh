#!/bin/bash

# Setup Agente Followers Analyzer
# Este script configura:
# 1. Pasta "Novos Seguidores" no Google Drive
# 2. Google Sheets "Followers Tracker"
# 3. Agente monitorando automaticamente

set -e

echo "🚀 SETUP AGENTE FOLLOWERS ANALYZER"
echo "=================================="
echo ""

# Credenciais
EMAIL="alfredharvey1806@gmail.com"
PASSWORD="Sucesso\$\$2026\$\$"
DRIVE_FOLDER="Novos Seguidores"
SHEETS_NAME="Followers Tracker"
OUTPUT_DIR="/home/harvey1806/Documents/Seguidores"

echo "📧 Email: $EMAIL"
echo "📁 Pasta Drive: $DRIVE_FOLDER"
echo "📊 Google Sheets: $SHEETS_NAME"
echo "💾 Destino: $OUTPUT_DIR"
echo ""

# 1. Criar pasta local
echo "✅ PASSO 1: Criar estrutura local..."
mkdir -p "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR/.metadata"
touch "$OUTPUT_DIR/index.md"
touch "$OUTPUT_DIR/.metadata/log.txt"
echo "[$(date)] Setup iniciado" >> "$OUTPUT_DIR/.metadata/log.txt"
echo "✓ Pastas criadas"
echo ""

# 2. Criar arquivo de configuração do agente
echo "✅ PASSO 2: Criar arquivo de config..."
cat > "$OUTPUT_DIR/.metadata/agent_config.json" << EOF
{
  "email": "$EMAIL",
  "drive_folder": "$DRIVE_FOLDER",
  "sheets_name": "$SHEETS_NAME",
  "output_dir": "$OUTPUT_DIR",
  "interval_seconds": 300,
  "last_run": null,
  "processed_files": [],
  "captured_profiles": []
}
EOF
echo "✓ Config criada: $OUTPUT_DIR/.metadata/agent_config.json"
echo ""

# 3. Status
echo "✅ SETUP COMPLETO!"
echo "=================================="
echo ""
echo "Próximos passos:"
echo "1. Agente está pronto para ativar"
echo "2. Crie a pasta 'Novos Seguidores' manualmente no Drive (ou deixe o agente criar)"
echo "3. Crie o Google Sheets 'Followers Tracker' manualmente (ou deixe o agente criar)"
echo "4. Execute: openclaw cron add (para agendar monitoramento)"
echo ""
echo "Log: $OUTPUT_DIR/.metadata/log.txt"
echo "Config: $OUTPUT_DIR/.metadata/agent_config.json"
echo ""
