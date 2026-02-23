#!/bin/bash
# ACTIVATE MONITORING - Ativa o monitoramento automático a cada 5 minutos
# Uso: bash activate_monitoring.sh

set -e

WORKSPACE="/home/harvey1806/.openclaw/workspace"
CONFIG="$WORKSPACE/followers_config.json"
MONITOR_SCRIPT="$WORKSPACE/monitor_followers.py"
CRON_JOB="*/5 * * * * python3 $MONITOR_SCRIPT >> $WORKSPACE/monitor_followers.log 2>&1"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║    ATIVANDO MONITORAMENTO AUTOMÁTICO (a cada 5 min)       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Verificar se config está completa
if grep -q '"PENDING"' "$CONFIG"; then
    echo "❌ ERRO: Configuração incompleta!"
    echo ""
    echo "Faltam preencher:"
    grep '"PENDING"' "$CONFIG" | sed 's/^/   • /'
    echo ""
    echo "Edite: $CONFIG"
    echo ""
    exit 1
fi

echo "✅ Verificação de configuração: OK"
echo ""

# Adicionar cron job
echo "📋 Adicionando cron job..."

# Remover job anterior se existir
(crontab -l 2>/dev/null | grep -v "$MONITOR_SCRIPT" || true) | crontab -

# Adicionar novo job
(crontab -l 2>/dev/null || echo "") | echo "$CRON_JOB" | crontab -

echo "✅ Cron job adicionado!"
echo ""

# Mostrar status
crontab -l | grep "$MONITOR_SCRIPT" && echo "✓ Job está ativo na crontab"

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              🚀 MONITORAMENTO ATIVADO                       ║"
echo "╠════════════════════════════════════════════════════════════╣"
echo "║                                                            ║"
echo "║  ✅ Sistema rodará a cada 5 minutos automaticamente        ║"
echo "║  📊 Log: $WORKSPACE/monitor_followers.log"
echo "║  📁 Saída: /home/harvey1806/Documents/Seguidores/         ║"
echo "║                                                            ║"
echo "║  Monitorar log em tempo real:                             ║"
echo "║  tail -f $WORKSPACE/monitor_followers.log"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

echo "Próxima execução: em até 5 minutos"
echo "Execução manual: python3 $MONITOR_SCRIPT"
