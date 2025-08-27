#!/bin/bash

# Deploy rápido usando Railway CLI con token
echo "🚀 Iniciando deployment rápido a Railway..."

# Configurar token
export RAILWAY_TOKEN=80b10a6c-d9ae-47f8-9d4c-112a2a58d699

# Login con browser
echo "📱 Abriendo navegador para login..."
railway login --browserless

echo "✅ Login completado"
echo ""
echo "🔧 Ahora ejecuta estos comandos uno por uno:"
echo ""
echo "1. Inicializar proyecto:"
echo "   railway init"
echo ""
echo "2. Agregar PostgreSQL:"
echo "   railway add"
echo ""
echo "3. Deploy backend:"
echo "   cd audite && railway up"
echo ""
echo "4. Deploy frontend:"
echo "   cd ../audite-frontend-explorer && railway up"
echo ""
echo "5. Ver URLs:"
echo "   railway domain"