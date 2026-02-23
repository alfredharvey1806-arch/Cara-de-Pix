#!/bin/bash

echo "🚀 Setup Ollama para Heartbeat Grátis"
echo "======================================"
echo ""

# Verificar SO
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  echo "📦 Linux detectado. Instalando Ollama..."
  curl -fsSL https://ollama.ai/install.sh | sh
  
elif [[ "$OSTYPE" == "darwin"* ]]; then
  echo "🍎 macOS detectado. Instalando Ollama via Homebrew..."
  brew install ollama
  
else
  echo "⚠️  SO não suportado. Instale manualmente: https://ollama.ai"
  exit 1
fi

echo ""
echo "✅ Ollama instalado"
echo ""

echo "📥 Puxando modelo leve (llama3.2:3b)..."
ollama pull llama3.2:3b

echo ""
echo "✅ Modelo pronto"
echo ""

echo "⏰ Para iniciar o heartbeat:"
echo "  1. Em um terminal: ollama serve"
echo "  2. Em outro terminal: openclaw gateway restart"
echo "  3. Validar: openclaw shell > session_status"
echo ""
