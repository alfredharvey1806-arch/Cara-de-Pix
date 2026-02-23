#!/bin/bash

# Instagram Profile Screenshot Automation
# Uso: ./instagram-scraper.sh "@username"

USERNAME=$1
EMAIL="alfredharvey1806@gmail.com"
PASSWORD="Sucesso\$\$2026\$\$"
OUTPUT_DIR="/home/harvey1806/Documents/Seguidores"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

if [ -z "$USERNAME" ]; then
  echo "❌ Erro: Forneça um @username"
  echo "Uso: ./instagram-scraper.sh @username"
  exit 1
fi

# Limpar o @ se vier com ele
USERNAME=${USERNAME#@}

echo "🔄 Iniciando automação Instagram..."
echo "📸 Capturando: @$USERNAME"
echo "💾 Destino: $OUTPUT_DIR"

# Aqui vai integração com o browser control do OpenClaw
# O script chama Alfred via sessions_send para executar a automação
echo "✅ Setup pronto. Aguardando captura..."

# Placeholder para integração real
echo "@$USERNAME,$TIMESTAMP" >> "$OUTPUT_DIR/.log"
