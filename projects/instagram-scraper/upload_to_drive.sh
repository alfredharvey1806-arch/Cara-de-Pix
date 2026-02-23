#!/bin/bash

# Upload para Google Drive + atualizar Google Sheets
# Arquivos: @pedrosallun_20260215_162628.png

set -e

echo "📤 UPLOAD PARA GOOGLE DRIVE"
echo "===================================="

FILE="/home/harvey1806/Documents/Seguidores/@pedrosallun_20260215_162628.png"
FILENAME=$(basename "$FILE")

if [ ! -f "$FILE" ]; then
  echo "❌ Arquivo não encontrado: $FILE"
  exit 1
fi

echo "✅ Arquivo encontrado: $FILENAME"
echo "📁 Tamanho: $(du -h "$FILE" | cut -f1)"

# Instruções para upload manual
echo ""
echo "Para subir no Drive automaticamente, você precisa:"
echo "1. Usar google-drive-cli (requer autenticação)"
echo "2. Ou usar Python + Google Drive API"
echo ""
echo "POR ENQUANTO, faça manualmente:"
echo ""
echo "PASSO 1: Subir arquivo para Drive"
echo "  ✅ Acesse: https://drive.google.com"
echo "  ✅ Entre em pasta: 'Novos Seguidores'"
echo "  ✅ Clique 'Fazer upload de arquivos'"
echo "  ✅ Selecione: $FILE"
echo ""
echo "PASSO 2: Atualizar Google Sheets"
echo "  ✅ Abra: Google Sheets > Followers Tracker"
echo "  ✅ Adicione linha:"
echo ""
echo "┌─────────────────────────────────────────────────────────────┐"
echo "│ @pedrosallun │ ✅ Capturado │ 2026-02-15 16:26:28 │ ... │ ... │"
echo "└─────────────────────────────────────────────────────────────┘"
echo ""
echo "    Coluna A: @pedrosallun"
echo "    Coluna B: ✅ Capturado"
echo "    Coluna C: 2026-02-15 16:26:28"
echo "    Coluna D: /home/harvey1806/Documents/Seguidores/@pedrosallun_20260215_162628.png"
echo "    Coluna E: (deixe vazio, é pra arquivo de origem)"
echo "    Coluna F: 1"
echo ""
