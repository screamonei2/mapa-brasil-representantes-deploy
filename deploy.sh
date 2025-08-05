#!/bin/bash

echo "🚀 Preparando deploy para Vercel..."
echo ""

# Verificar se o Vercel CLI está instalado
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI não encontrado. Instalando..."
    npm install -g vercel
fi

# Verificar se está logado
if ! vercel whoami &> /dev/null; then
    echo "🔐 Fazendo login no Vercel..."
    vercel login
fi

echo "📦 Fazendo deploy..."
vercel --prod

echo ""
echo "✅ Deploy concluído!"
echo "🌐 Acesse o link fornecido acima para ver sua aplicação." 