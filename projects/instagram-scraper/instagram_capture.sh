#!/bin/bash

# Instagram Search + Capture via OpenClaw Browser Control
# Uso: ./instagram_capture.sh @pedrosallun

USERNAME=${1#@}
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
FILENAME="@${USERNAME}_${TIMESTAMP}.png"
FILEPATH="/home/harvey1806/Documents/Seguidores/$FILENAME"
OUTPUT_DIR="/home/harvey1806/Documents/Seguidores"

mkdir -p "$OUTPUT_DIR"

echo "🔄 Iniciando captura de @${USERNAME}..."
echo "💾 Arquivo: $FILENAME"
echo "📍 Caminho: $FILEPATH"

# Este script será chamado por Alfred quando receber "analise @username"
# O OpenClaw browser control será acionado aqui
echo "@${USERNAME}" > "$OUTPUT_DIR/.pending"
