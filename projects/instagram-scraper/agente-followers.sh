#!/bin/bash

# AGENTE FOLLOWERS ANALYZER - Script Wrapper
# Executa agente_hybrid.py a cada 5 minutos via cron

SCRIPT_DIR="/home/harvey1806/.openclaw/workspace/projects/instagram-scraper"
PYTHON_SCRIPT="$SCRIPT_DIR/agente_hybrid.py"
VENV="$SCRIPT_DIR/../../../venv"
LOG_DIR="/home/harvey1806/Documents/Seguidores/.metadata"

# Criar diretório de logs se não existir
mkdir -p "$LOG_DIR"

# Ativar virtual environment se existir
if [ -f "$VENV/bin/activate" ]; then
    source "$VENV/bin/activate"
fi

# Executar agente
cd "$SCRIPT_DIR"
python3 "$PYTHON_SCRIPT"

exit 0
