#!/bin/bash

echo "🚀 Iniciando servidor de desenvolvimento com monitoramento..."
echo "📁 Diretório: vercel-deploy"
echo "🌐 Porta: 8080"
echo "👀 Monitorando mudanças nos arquivos..."
echo ""

# Verifica se Python 3 está disponível
if command -v python3 &> /dev/null; then
    python3 simple_watch_server.py
elif command -v python &> /dev/null; then
    python simple_watch_server.py
else
    echo "❌ Python não encontrado!"
    echo "Por favor, instale Python 3"
    exit 1
fi
